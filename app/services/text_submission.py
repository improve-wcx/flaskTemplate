"""
Text submission storage service.
Handles loading, saving, and querying submission data from JSON Lines file.
"""
import os
import json
import uuid
from datetime import datetime
from typing import List, Dict, Optional, Any
from pathlib import Path
import threading
import logging

# Configure logger
logger = logging.getLogger(__name__)

# Thread lock for file operations
_lock = threading.Lock()

# Data file path
DATA_DIR = Path(__file__).parent.parent.parent / "data" / "submissions"
DATA_FILE = DATA_DIR / "submissions.jsonl"

# Ensure data directory exists
DATA_DIR.mkdir(parents=True, exist_ok=True)


class SubmissionStorage:
    """Storage service for text submissions."""
    
    def __init__(self):
        self._data: List[Dict[str, Any]] = []
        self._loaded = False
        self._lock = _lock
    
    def _load_data(self):
        """Load data from JSON Lines file into memory."""
        if self._loaded:
            return
        
        with self._lock:
            if self._loaded:
                return
            
            if DATA_FILE.exists():
                try:
                    with open(DATA_FILE, 'r', encoding='utf-8') as f:
                        for line in f:
                            line = line.strip()
                            if line:
                                try:
                                    self._data.append(json.loads(line))
                                except json.JSONDecodeError:
                                    # Skip invalid lines
                                    continue
                    logger.info(f"Loaded {len(self._data)} submissions from {DATA_FILE}")
                except Exception as e:
                    logger.error(f"Failed to load submissions: {e}")
                    self._data = []
            else:
                self._data = []
            
            self._loaded = True
    
    def _save_data(self):
        """Save all data to JSON Lines file (overwrite)."""
        with self._lock:
            try:
                with open(DATA_FILE, 'w', encoding='utf-8') as f:
                    for item in self._data:
                        f.write(json.dumps(item, ensure_ascii=False) + '\n')
                logger.info(f"Saved {len(self._data)} submissions to {DATA_FILE}")
            except Exception as e:
                logger.error(f"Failed to save submissions: {e}")
                raise
    
    def _append_submission(self, submission: Dict[str, Any]):
        """Append a single submission to the file."""
        with self._lock:
            try:
                with open(DATA_FILE, 'a', encoding='utf-8') as f:
                    f.write(json.dumps(submission, ensure_ascii=False) + '\n')
                logger.info(f"Appended submission {submission['id']}")
            except Exception as e:
                logger.error(f"Failed to append submission: {e}")
                raise
    
    def add_submission(self, content: str, ip_address: str = None, user_agent: str = None) -> Dict[str, Any]:
        """
        Add a new submission.
        
        Args:
            content: The submitted text content
            ip_address: Client IP address
            user_agent: Client user agent string
            
        Returns:
            Created submission record
        """
        self._load_data()
        
        submission = {
            'id': str(uuid.uuid4()),
            'content': content,  # Keep original content with all whitespace
            'created_at': datetime.now().strftime('%Y-%m-%dT%H:%M:%S+08:00'),
            'ip_address': ip_address or '',
            'user_agent': user_agent or ''
        }
        
        # Add to memory first
        self._data.insert(0, submission)  # Insert at beginning for newest first
        
        # Then append to file
        self._append_submission(submission)
        
        return submission
    
    def get_submissions(
        self,
        page: int = 1,
        per_page: int = 20,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        keyword: Optional[str] = None,
        case_sensitive: bool = False
    ) -> Dict[str, Any]:
        """
        Get paginated submissions with optional filters.
        
        Args:
            page: Page number (1-indexed)
            per_page: Number of items per page
            start_date: Start date filter (YYYY-MM-DD)
            end_date: End date filter (YYYY-MM-DD)
            keyword: Search keyword
            case_sensitive: Whether keyword search is case-sensitive
            
        Returns:
            Paginated result with items and metadata
        """
        self._load_data()
        
        # Filter data
        filtered = self._data.copy()
        
        # Date range filter
        if start_date:
            filtered = [
                item for item in filtered
                if item['created_at'][:10] >= start_date
            ]
        
        if end_date:
            filtered = [
                item for item in filtered
                if item['created_at'][:10] <= end_date
            ]
        
        # Keyword search
        if keyword:
            if case_sensitive:
                filtered = [
                    item for item in filtered
                    if keyword in item['content']
                ]
            else:
                keyword_lower = keyword.lower()
                filtered = [
                    item for item in filtered
                    if keyword_lower in item['content'].lower()
                ]
        
        # Calculate pagination
        total = len(filtered)
        total_pages = (total + per_page - 1) // per_page if total > 0 else 1
        
        # Get page items
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        items = filtered[start_idx:end_idx]
        
        return {
            'items': items,
            'total': total,
            'page': page,
            'per_page': per_page,
            'total_pages': total_pages
        }
    
    def get_total_count(self) -> int:
        """Get total number of submissions."""
        self._load_data()
        return len(self._data)
    
    def clear_all(self):
        """Clear all submissions (for testing)."""
        with self._lock:
            self._data = []
            self._loaded = False
            if DATA_FILE.exists():
                DATA_FILE.unlink()
            logger.info("Cleared all submissions")


# Global storage instance
storage = SubmissionStorage()


def add_submission(content: str, ip_address: str = None, user_agent: str = None) -> Dict[str, Any]:
    """Add a new submission."""
    return storage.add_submission(content, ip_address, user_agent)


def get_submissions(
    page: int = 1,
    per_page: int = 20,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    keyword: Optional[str] = None,
    case_sensitive: bool = False
) -> Dict[str, Any]:
    """Get paginated submissions with filters."""
    return storage.get_submissions(page, per_page, start_date, end_date, keyword, case_sensitive)


def get_total_count() -> int:
    """Get total number of submissions."""
    return storage.get_total_count()


def clear_all_submissions():
    """Clear all submissions (for testing)."""
    storage.clear_all()
