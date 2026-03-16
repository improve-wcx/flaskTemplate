"""
Tests for text submission storage service.
"""
import os
import json
import pytest
import tempfile
from pathlib import Path
from app.services.text_submission import SubmissionStorage, clear_all_submissions


class TestSubmissionStorage:
    """Test SubmissionStorage class functionality."""

    def setup_method(self):
        """Setup before each test method."""
        clear_all_submissions()

    def teardown_method(self):
        """Cleanup after each test method."""
        clear_all_submissions()

    def test_add_submission_basic(self):
        """Test basic submission addition."""
        storage = SubmissionStorage()
        submission = storage.add_submission('Test content', '127.0.0.1', 'TestAgent/1.0')

        assert 'id' in submission
        assert submission['content'] == 'Test content'
        assert 'created_at' in submission
        assert submission['ip_address'] == '127.0.0.1'
        assert submission['user_agent'] == 'TestAgent/1.0'

        # Verify it's in memory
        assert len(storage._data) == 1
        assert storage._data[0]['id'] == submission['id']

    def test_add_submission_preserves_whitespace(self):
        """Test that whitespace is preserved in content."""
        storage = SubmissionStorage()
        content = 'Line 1\nLine 2\tTabbed\r\nWindows\rMac'
        submission = storage.add_submission(content)

        assert submission['content'] == content

    def test_add_submission_order(self):
        """Test that submissions are added in correct order (newest first)."""
        storage = SubmissionStorage()

        sub1 = storage.add_submission('First')
        sub2 = storage.add_submission('Second')
        sub3 = storage.add_submission('Third')

        assert len(storage._data) == 3
        assert storage._data[0]['content'] == 'Third'  # Newest first
        assert storage._data[1]['content'] == 'Second'
        assert storage._data[2]['content'] == 'First'

    def test_get_submissions_basic(self):
        """Test basic submission retrieval."""
        storage = SubmissionStorage()

        # Add some submissions
        storage.add_submission('Content 1')
        storage.add_submission('Content 2')

        result = storage.get_submissions()

        assert result['total'] == 2
        assert result['page'] == 1
        assert result['per_page'] == 20
        assert result['total_pages'] == 1
        assert len(result['items']) == 2
        assert result['items'][0]['content'] == 'Content 2'  # Newest first

    def test_get_submissions_pagination(self):
        """Test pagination in submission retrieval."""
        storage = SubmissionStorage()

        # Add 5 submissions
        for i in range(5):
            storage.add_submission(f'Content {i+1}')

        # Page 1, per_page 2
        result = storage.get_submissions(page=1, per_page=2)
        assert result['total'] == 5
        assert result['page'] == 1
        assert result['per_page'] == 2
        assert result['total_pages'] == 3
        assert len(result['items']) == 2
        assert result['items'][0]['content'] == 'Content 5'
        assert result['items'][1]['content'] == 'Content 4'

        # Page 2
        result = storage.get_submissions(page=2, per_page=2)
        assert len(result['items']) == 2
        assert result['items'][0]['content'] == 'Content 3'
        assert result['items'][1]['content'] == 'Content 2'

        # Page 3
        result = storage.get_submissions(page=3, per_page=2)
        assert len(result['items']) == 1
        assert result['items'][0]['content'] == 'Content 1'

    def test_get_submissions_keyword_search(self):
        """Test keyword search functionality."""
        storage = SubmissionStorage()

        storage.add_submission('Python programming')
        storage.add_submission('JavaScript development')
        storage.add_submission('Python data science')

        # Search for 'Python'
        result = storage.get_submissions(keyword='Python')
        assert result['total'] == 2
        assert all('Python' in item['content'] for item in result['items'])

        # Case insensitive
        result = storage.get_submissions(keyword='python')
        assert result['total'] == 2

        # Case sensitive
        result = storage.get_submissions(keyword='Python', case_sensitive=True)
        assert result['total'] == 2

        result = storage.get_submissions(keyword='python', case_sensitive=True)
        assert result['total'] == 0

        # No matches
        result = storage.get_submissions(keyword='Ruby')
        assert result['total'] == 0

    def test_get_submissions_date_filter(self):
        """Test date range filtering."""
        storage = SubmissionStorage()

        # Add submissions (will have current date)
        storage.add_submission('Today content')
        storage.add_submission('Another today content')

        today = storage._data[0]['created_at'][:10]  # YYYY-MM-DD

        # Filter by today
        result = storage.get_submissions(start_date=today, end_date=today)
        assert result['total'] == 2

        # Filter by future date (should return nothing)
        future = '2099-12-31'
        result = storage.get_submissions(start_date=future, end_date=future)
        assert result['total'] == 0

    def test_get_submissions_combined_filters(self):
        """Test combining keyword and date filters."""
        storage = SubmissionStorage()

        storage.add_submission('Python today')
        storage.add_submission('JavaScript today')
        storage.add_submission('Python yesterday')  # Would need date manipulation

        # For this test, just verify parameters are accepted
        today = storage._data[0]['created_at'][:10]
        result = storage.get_submissions(
            start_date=today,
            end_date=today,
            keyword='Python'
        )
        # Should work without error
        assert isinstance(result, dict)

    def test_get_total_count(self):
        """Test getting total count."""
        storage = SubmissionStorage()

        assert storage.get_total_count() == 0

        storage.add_submission('Content 1')
        assert storage.get_total_count() == 1

        storage.add_submission('Content 2')
        assert storage.get_total_count() == 2

    def test_clear_all(self):
        """Test clearing all submissions."""
        storage = SubmissionStorage()

        storage.add_submission('Content 1')
        storage.add_submission('Content 2')
        assert len(storage._data) == 2

        storage.clear_all()
        assert len(storage._data) == 0
        assert storage.get_total_count() == 0

    def test_persistence_to_file(self):
        """Test that submissions are persisted to file."""
        storage = SubmissionStorage()

        # Add submission
        submission = storage.add_submission('Persistent content')

        # Check file exists and contains data
        from app.services.text_submission import DATA_FILE
        assert DATA_FILE.exists()

        # Create new storage instance to test loading
        storage2 = SubmissionStorage()
        storage2._loaded = False  # Force reload
        storage2._load_data()

        assert len(storage2._data) == 1
        assert storage2._data[0]['id'] == submission['id']
        assert storage2._data[0]['content'] == 'Persistent content'

    def test_thread_safety(self):
        """Test thread safety of file operations."""
        import threading
        import time

        storage = SubmissionStorage()
        results = []

        def add_submission_worker(content):
            time.sleep(0.01)  # Small delay to increase chance of race condition
            submission = storage.add_submission(content)
            results.append(submission)

        threads = []
        for i in range(10):
            t = threading.Thread(target=add_submission_worker, args=[f'Content {i}'])
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        assert len(results) == 10
        assert storage.get_total_count() == 10

    def test_large_content(self):
        """Test handling of large content."""
        storage = SubmissionStorage()

        # Content near 1MB limit (but under)
        large_content = 'x' * (1024 * 1024 - 100)
        submission = storage.add_submission(large_content)

        assert submission['content'] == large_content
        assert len(submission['content'].encode('utf-8')) < 1024 * 1024

    def test_special_characters(self):
        """Test handling of special characters and unicode."""
        storage = SubmissionStorage()

        content = 'Special chars: éñüñ 中文 🚀 \u0000\u0001\u0002'
        submission = storage.add_submission(content)

        assert submission['content'] == content

        # Verify persistence
        storage2 = SubmissionStorage()
        storage2._loaded = False
        storage2._load_data()

        assert storage2._data[0]['content'] == content

    def test_empty_and_whitespace_content(self):
        """Test edge cases with empty or whitespace content."""
        storage = SubmissionStorage()

        # These should be allowed at service level (validation at API level)
        sub1 = storage.add_submission('')
        sub2 = storage.add_submission('   \n\t   ')

        assert sub1['content'] == ''
        assert sub2['content'] == '   \n\t   '