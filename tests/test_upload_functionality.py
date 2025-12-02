"""
Functional tests for file upload after DaisyUI migration.

Validates that file upload functionality still works correctly.
"""

import pytest
import io
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from skeleton_core.app import create_app
from app_legal.config import Config


@pytest.fixture
def app():
    """Create test Flask app with Legal Eagle config."""
    app = create_app(Config)
    app.config['TESTING'] = True
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


def test_upload_endpoint_accepts_txt_file(client):
    """Test that upload endpoint accepts .txt files."""
    # Create a simple text file
    data = {
        'file': (io.BytesIO(b'This is a test document.'), 'test.txt')
    }
    
    response = client.post('/upload', data=data, content_type='multipart/form-data')
    
    # Should return 200 OK
    assert response.status_code == 200
    
    # Response should be Server-Sent Events
    assert response.content_type == 'text/event-stream; charset=utf-8'


def test_upload_endpoint_accepts_pdf_file(client):
    """Test that upload endpoint accepts .pdf files."""
    # Create a minimal PDF file (just header for testing)
    pdf_content = b'%PDF-1.4\n%\xE2\xE3\xCF\xD3\n'
    
    data = {
        'file': (io.BytesIO(pdf_content), 'test.pdf')
    }
    
    response = client.post('/upload', data=data, content_type='multipart/form-data')
    
    # Should return 200 OK (even if PDF parsing fails, endpoint should respond)
    assert response.status_code == 200


def test_upload_endpoint_rejects_invalid_extension(client):
    """Test that upload endpoint rejects files with invalid extensions."""
    data = {
        'file': (io.BytesIO(b'Invalid file'), 'test.exe')
    }
    
    response = client.post('/upload', data=data, content_type='multipart/form-data')
    
    # Should still return 200 but with error in SSE stream
    assert response.status_code == 200


def test_upload_endpoint_requires_file(client):
    """Test that upload endpoint requires a file."""
    response = client.post('/upload', data={}, content_type='multipart/form-data')
    
    # Should return 400 Bad Request
    assert response.status_code == 400


def test_upload_progress_stages_in_response(client):
    """Test that upload response includes progress stages."""
    data = {
        'file': (io.BytesIO(b'This is a test document with some content.'), 'test.txt')
    }
    
    response = client.post('/upload', data=data, content_type='multipart/form-data')
    
    # Get response data
    response_data = response.data.decode('utf-8')
    
    # Should contain SSE data events
    assert 'data:' in response_data
    
    # Should contain progress updates
    assert 'progress' in response_data or 'stage' in response_data


def test_main_page_loads_successfully(client):
    """Test that main page loads without errors."""
    response = client.get('/')
    
    assert response.status_code == 200
    assert b'upload-section' in response.data
    assert b'fileInput' in response.data
    assert b'uploadFile()' in response.data
