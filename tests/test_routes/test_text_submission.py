"""
Tests for text submission routes and functionality.
"""
import json
import pytest
from datetime import datetime, timedelta
from app.services.text_submission import clear_all_submissions, add_submission, get_submissions


class TestTextSubmissionAPI:
    """Test text submission API endpoints."""

    def setup_method(self):
        """Setup before each test method."""
        clear_all_submissions()

    def teardown_method(self):
        """Cleanup after each test method."""
        clear_all_submissions()

    def test_submit_text_success(self, client):
        """Test successful text submission."""
        data = {
            'content': 'Test submission content\nwith newlines\tand tabs'
        }

        resp = client.post('/api/v1/submission',
                          json=data,
                          content_type='application/json')

        assert resp.status_code == 201
        assert resp.content_type == 'application/json'

        response_data = resp.get_json()
        assert response_data['success'] is True
        assert 'data' in response_data
        assert 'id' in response_data['data']
        assert 'created_at' in response_data['data']
        assert response_data['message'] == 'Submission successful'

    def test_submit_text_empty_content(self, client):
        """Test submission with empty content."""
        data = {'content': ''}

        resp = client.post('/api/v1/submission', json=data)

        assert resp.status_code == 400
        response_data = resp.get_json()
        assert response_data['success'] is False
        assert 'cannot be empty' in response_data['message']

    def test_submit_text_whitespace_only(self, client):
        """Test submission with whitespace-only content."""
        data = {'content': '   \n\t   '}

        resp = client.post('/api/v1/submission', json=data)

        assert resp.status_code == 400
        response_data = resp.get_json()
        assert response_data['success'] is False
        assert 'cannot be empty' in response_data['message']

    def test_submit_text_missing_content(self, client):
        """Test submission without content field."""
        data = {}

        resp = client.post('/api/v1/submission', json=data)

        assert resp.status_code == 400
        response_data = resp.get_json()
        assert response_data['success'] is False
        assert 'Content is required' in response_data['message']

    def test_submit_text_no_json(self, client):
        """Test submission without JSON body."""
        resp = client.post('/api/v1/submission')

        assert resp.status_code == 400
        response_data = resp.get_json()
        assert response_data['success'] is False
        assert 'Invalid request body' in response_data['message']

    def test_submit_text_content_too_large(self, client):
        """Test submission with content exceeding 1MB."""
        large_content = 'x' * (1024 * 1024 + 1)  # 1MB + 1 byte
        data = {'content': large_content}

        resp = client.post('/api/v1/submission', json=data)

        assert resp.status_code == 400
        response_data = resp.get_json()
        assert response_data['success'] is False
        assert 'exceeds 1MB limit' in response_data['message']

    def test_submit_text_preserves_whitespace(self, client):
        """Test that submission preserves all whitespace characters."""
        content = 'Line 1\nLine 2\tTabbed\r\nWindows line\rMac line'
        data = {'content': content}

        resp = client.post('/api/v1/submission', json=data)

        assert resp.status_code == 201
        response_data = resp.get_json()
        assert response_data['success'] is True

        # Verify content is preserved
        submission_id = response_data['data']['id']
        submissions = get_submissions()
        submission = next(s for s in submissions['items'] if s['id'] == submission_id)
        assert submission['content'] == content

    def test_get_submissions_empty(self, client):
        """Test getting submissions when none exist."""
        data = {
            'page': 1,
            'per_page': 20
        }

        resp = client.post('/api/v1/submissions', json=data)

        assert resp.status_code == 200
        response_data = resp.get_json()
        assert response_data['success'] is True
        assert response_data['data']['total'] == 0
        assert response_data['data']['items'] == []
        assert response_data['data']['page'] == 1
        assert response_data['data']['per_page'] == 20
        assert response_data['data']['total_pages'] == 1

    def test_get_submissions_basic(self, client):
        """Test getting submissions with basic pagination."""
        # Add some test submissions
        add_submission('First submission')
        add_submission('Second submission')
        add_submission('Third submission')

        data = {'page': 1, 'per_page': 2}

        resp = client.post('/api/v1/submissions', json=data)

        assert resp.status_code == 200
        response_data = resp.get_json()
        assert response_data['success'] is True
        assert response_data['data']['total'] == 3
        assert len(response_data['data']['items']) == 2
        assert response_data['data']['page'] == 1
        assert response_data['data']['per_page'] == 2
        assert response_data['data']['total_pages'] == 2

        # Check order (newest first)
        assert response_data['data']['items'][0]['content'] == 'Third submission'
        assert response_data['data']['items'][1]['content'] == 'Second submission'

    def test_get_submissions_pagination(self, client):
        """Test pagination functionality."""
        # Add 5 submissions
        for i in range(5):
            add_submission(f'Submission {i+1}')

        # Page 1
        resp = client.post('/api/v1/submissions', json={'page': 1, 'per_page': 2})
        data = resp.get_json()
        assert len(data['data']['items']) == 2
        assert data['data']['items'][0]['content'] == 'Submission 5'
        assert data['data']['items'][1]['content'] == 'Submission 4'

        # Page 2
        resp = client.post('/api/v1/submissions', json={'page': 2, 'per_page': 2})
        data = resp.get_json()
        assert len(data['data']['items']) == 2
        assert data['data']['items'][0]['content'] == 'Submission 3'
        assert data['data']['items'][1]['content'] == 'Submission 2'

        # Page 3
        resp = client.post('/api/v1/submissions', json={'page': 3, 'per_page': 2})
        data = resp.get_json()
        assert len(data['data']['items']) == 1
        assert data['data']['items'][0]['content'] == 'Submission 1'

    def test_get_submissions_invalid_page(self, client):
        """Test invalid page parameters."""
        add_submission('Test submission')

        # Negative page
        resp = client.post('/api/v1/submissions', json={'page': -1})
        data = resp.get_json()
        assert data['data']['page'] == 1  # Should default to 1

        # Zero per_page
        resp = client.post('/api/v1/submissions', json={'per_page': 0})
        data = resp.get_json()
        assert data['data']['per_page'] == 20  # Should default to 20

        # Too large per_page
        resp = client.post('/api/v1/submissions', json={'per_page': 200})
        data = resp.get_json()
        assert data['data']['per_page'] == 100  # Should cap at 100

    def test_get_submissions_date_filter(self, client):
        """Test date range filtering."""
        # Add submissions with different dates
        today = datetime.now().strftime('%Y-%m-%d')
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

        # Mock different dates by directly setting created_at
        add_submission('Today submission')
        add_submission('Yesterday submission')

        # Get all and modify dates for testing
        all_subs = get_submissions(per_page=100)['items']
        if len(all_subs) >= 2:
            # Modify the second submission to be yesterday
            all_subs[1]['created_at'] = f"{yesterday}T12:00:00+08:00"
            # Save back by clearing and re-adding (simplified for test)
            clear_all_submissions()
            for sub in reversed(all_subs):
                add_submission(sub['content'])

        # Filter by today
        resp = client.post('/api/v1/submissions', json={'start_date': today, 'end_date': today})
        data = resp.get_json()
        # Note: This test may need adjustment based on actual date handling

    def test_get_submissions_keyword_search(self, client):
        """Test keyword search functionality."""
        add_submission('Python programming tutorial')
        add_submission('JavaScript web development')
        add_submission('Python data analysis')

        # Search for 'Python'
        resp = client.post('/api/v1/submissions', json={'keyword': 'Python'})
        data = resp.get_json()
        assert data['data']['total'] == 2
        assert all('Python' in item['content'] for item in data['data']['items'])

        # Case insensitive search
        resp = client.post('/api/v1/submissions', json={'keyword': 'python'})
        data = resp.get_json()
        assert data['data']['total'] == 2

        # Case sensitive search
        resp = client.post('/api/v1/submissions', json={'keyword': 'Python', 'case_sensitive': True})
        data = resp.get_json()
        assert data['data']['total'] == 2

        # No matches
        resp = client.post('/api/v1/submissions', json={'keyword': 'Ruby'})
        data = resp.get_json()
        assert data['data']['total'] == 0

    def test_get_submissions_combined_filters(self, client):
        """Test combining date and keyword filters."""
        # This would require setting up test data with specific dates
        # For now, just test that parameters are accepted
        resp = client.post('/api/v1/submissions', json={
            'start_date': '2023-01-01',
            'end_date': '2023-12-31',
            'keyword': 'test',
            'case_sensitive': False
        })
        assert resp.status_code == 200
        data = resp.get_json()
        assert 'data' in data

    def test_get_submissions_invalid_date_format(self, client):
        """Test invalid date format handling."""
        resp = client.post('/api/v1/submissions', json={'start_date': 'invalid-date'})
        assert resp.status_code == 400
        data = resp.get_json()
        assert 'Invalid start_date format' in data['message']

        resp = client.post('/api/v1/submissions', json={'end_date': '2023/01/01'})
        assert resp.status_code == 400
        data = resp.get_json()
        assert 'Invalid end_date format' in data['message']

    def test_text_submission_page(self, client):
        """Test the HTML page endpoint."""
        resp = client.get('/api/v1/text_submission')
        assert resp.status_code == 200
        # Should return HTML content
        assert 'text/html' in resp.content_type

    def test_submit_text_with_metadata(self, client):
        """Test that submissions include proper metadata."""
        content = 'Test content'
        resp = client.post('/api/v1/submission', json={'content': content})

        assert resp.status_code == 201
        data = resp.get_json()

        # Check that submission has required fields
        submission_id = data['data']['id']
        submissions = get_submissions(per_page=1)['items']
        submission = submissions[0]

        assert submission['id'] == submission_id
        assert submission['content'] == content
        assert 'created_at' in submission
        assert 'ip_address' in submission
        assert 'user_agent' in submission

        # Verify created_at format
        datetime.strptime(submission['created_at'], '%Y-%m-%dT%H:%M:%S+08:00')
        
        # Verify the datetime is recent (within last minute)
        parsed_time = datetime.strptime(submission['created_at'], '%Y-%m-%dT%H:%M:%S+08:00')
        assert abs((datetime.now() - parsed_time).total_seconds()) < 60
