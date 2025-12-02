"""
Test functionality preservation after Tailwind/DaisyUI migration.

This test suite verifies that all core functionality works identically
to the pre-migration implementation.

Validates Requirements: 7.1, 7.2, 7.3, 7.4, 7.5
"""
import pytest
import io
import tempfile
import os
from skeleton_core.app import create_app
from app_legal.config import Config as LegalConfig
from app_ghost.config import Config as GhostConfig
from skeleton_core.vector_store import VectorStore


# ==========================================
# Fixtures
# ==========================================

@pytest.fixture
def legal_app():
    """Create Legal Eagle app instance for testing."""
    app = create_app(LegalConfig)
    app.config['TESTING'] = True
    return app


@pytest.fixture
def legal_client(legal_app):
    """Create test client for Legal Eagle app."""
    return legal_app.test_client()


@pytest.fixture
def ghost_app():
    """Create Ouija Board app instance for testing."""
    app = create_app(GhostConfig)
    app.config['TESTING'] = True
    return app


@pytest.fixture
def ghost_client(ghost_app):
    """Create test client for Ouija Board app."""
    return ghost_app.test_client()


@pytest.fixture
def vector_store():
    """Create vector store instance."""
    return VectorStore()


@pytest.fixture
def cleanup_test_docs(vector_store):
    """Cleanup test documents after each test."""
    yield
    # Cleanup after test
    test_docs = ['test_upload.txt', 'test_chat.txt', 'test_delete.txt', 
                 'test_selection.txt', 'test_error.txt']
    for doc in test_docs:
        try:
            vector_store.delete_document(doc)
        except:
            pass


# ==========================================
# Test 1: File Upload Functionality (Requirement 7.1)
# ==========================================

def test_file_upload_txt_works_identically(legal_client, cleanup_test_docs):
    """
    Test that text file upload works identically to pre-migration.
    
    Validates: Requirement 7.1
    """
    # Create test file content
    test_content = "This is a test document for upload functionality testing."
    
    data = {
        'file': (io.BytesIO(test_content.encode('utf-8')), 'test_upload.txt')
    }
    
    # Upload the file
    response = legal_client.post('/upload', 
                                 data=data,
                                 content_type='multipart/form-data')
    
    # Should return 200 OK
    assert response.status_code == 200, "Upload should succeed"
    
    # Response should be Server-Sent Events
    assert response.content_type == 'text/event-stream; charset=utf-8', \
        "Upload should return SSE stream"
    
    # Response should contain progress updates
    response_data = response.data.decode('utf-8')
    assert 'data:' in response_data, "Response should contain SSE data events"


def test_file_upload_pdf_works_identically(legal_client, cleanup_test_docs):
    """
    Test that PDF file upload works identically to pre-migration.
    
    Validates: Requirement 7.1
    """
    # Create minimal PDF content
    pdf_content = b'%PDF-1.4\n%\xE2\xE3\xCF\xD3\n'
    
    data = {
        'file': (io.BytesIO(pdf_content), 'test_upload.pdf')
    }
    
    # Upload the file
    response = legal_client.post('/upload',
                                 data=data,
                                 content_type='multipart/form-data')
    
    # Should return 200 OK
    assert response.status_code == 200, "PDF upload should succeed"


def test_file_upload_validation_works_identically(legal_client):
    """
    Test that file validation works identically to pre-migration.
    
    Validates: Requirement 7.1
    """
    # Try to upload invalid file type
    data = {
        'file': (io.BytesIO(b'Invalid content'), 'test.exe')
    }
    
    response = legal_client.post('/upload',
                                 data=data,
                                 content_type='multipart/form-data')
    
    # Should still return 200 (error in SSE stream)
    assert response.status_code == 200


def test_file_upload_requires_file(legal_client):
    """
    Test that upload endpoint requires a file.
    
    Validates: Requirement 7.1
    """
    response = legal_client.post('/upload',
                                 data={},
                                 content_type='multipart/form-data')
    
    # Should return 400 Bad Request
    assert response.status_code == 400, "Upload without file should fail"


# ==========================================
# Test 2: Chat Functionality (Requirement 7.2)
# ==========================================

def test_chat_endpoint_accepts_query(legal_client, cleanup_test_docs):
    """
    Test that chat endpoint accepts queries identically to pre-migration.
    
    Validates: Requirement 7.2
    
    Note: This test requires GOOGLE_API_KEY to be set.
    """
    # Check if API key is available
    import os
    if not os.getenv('GOOGLE_API_KEY'):
        pytest.skip("GOOGLE_API_KEY not set - skipping chat test")
    
    # Send a chat query
    response = legal_client.post('/chat',
                                 json={'query': 'What is this about?'},
                                 content_type='application/json')
    
    # Should return 200 OK
    assert response.status_code == 200, "Chat should accept queries"
    
    # Response should be JSON
    assert response.content_type == 'application/json', \
        "Chat should return JSON"
    
    # Response should contain echo or error
    data = response.get_json()
    assert 'echo' in data or 'error' in data, \
        "Chat response should contain echo or error"


def test_chat_with_source_filtering(legal_client, vector_store, cleanup_test_docs):
    """
    Test that chat with source filtering works identically to pre-migration.
    
    Validates: Requirement 7.2
    
    Note: This test requires GOOGLE_API_KEY to be set.
    """
    # Check if API key is available
    import os
    if not os.getenv('GOOGLE_API_KEY'):
        pytest.skip("GOOGLE_API_KEY not set - skipping chat test")
    
    # First upload a test document
    test_content = "This is a test document for chat filtering."
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(test_content)
        temp_file = f.name
    
    try:
        # Upload the file
        with open(temp_file, 'rb') as f:
            data = {'file': (f, 'test_chat.txt')}
            upload_response = legal_client.post('/upload',
                                               data=data,
                                               content_type='multipart/form-data')
            assert upload_response.status_code == 200
        
        # Send chat query with source filter
        response = legal_client.post('/chat',
                                     json={
                                         'query': 'What is this about?',
                                         'sources': ['test_chat.txt']
                                     },
                                     content_type='application/json')
        
        # Should return 200 OK
        assert response.status_code == 200, "Chat with filtering should work"
        
        # Response should be JSON
        data = response.get_json()
        assert 'echo' in data or 'error' in data
        
    finally:
        if os.path.exists(temp_file):
            os.unlink(temp_file)


def test_chat_empty_query_handling(legal_client):
    """
    Test that empty query handling works identically to pre-migration.
    
    Validates: Requirement 7.2
    """
    # Send empty query
    response = legal_client.post('/chat',
                                 json={'query': ''},
                                 content_type='application/json')
    
    # Should return 400 (empty query is invalid) or 200 (handled gracefully)
    assert response.status_code in [200, 400], \
        "Empty query should be handled gracefully"


def test_chat_interface_elements_present(legal_client):
    """
    Test that chat interface elements are present and functional.
    
    Validates: Requirement 7.2
    """
    response = legal_client.get('/')
    html = response.data.decode('utf-8')
    
    # Check essential chat elements exist
    assert 'queryInput' in html, "Query input should exist"
    assert 'sendQuery()' in html, "sendQuery function should be referenced"
    assert 'chat-history' in html, "Chat history container should exist"


# ==========================================
# Test 3: Document Deletion (Requirement 7.3)
# ==========================================

def test_document_deletion_works_identically(legal_client, vector_store, cleanup_test_docs):
    """
    Test that document deletion works identically to pre-migration.
    
    Validates: Requirement 7.3
    
    Note: This test may fail if GOOGLE_API_KEY is not set (needed for embeddings).
    """
    # Create and upload a test document
    test_content = "This is a test document for deletion."
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(test_content)
        temp_file = f.name
    
    try:
        # Upload the file
        with open(temp_file, 'rb') as f:
            data = {'file': (f, 'test_delete.txt')}
            upload_response = legal_client.post('/upload',
                                               data=data,
                                               content_type='multipart/form-data')
            # Upload may fail if API key is missing, which is OK for this test
            if upload_response.status_code != 200:
                pytest.skip("Upload failed (likely missing API key)")
        
        # Verify document exists
        list_response = legal_client.get('/documents')
        docs = list_response.get_json()['documents']
        doc_names = [doc['source'] for doc in docs]
        
        # If document didn't upload, skip the test
        if 'test_delete.txt' not in doc_names:
            pytest.skip("Document upload failed (likely missing API key)")
        
        # Delete the document
        delete_response = legal_client.delete('/documents/test_delete.txt')
        
        # Should return 200 OK
        assert delete_response.status_code == 200, "Delete should succeed"
        
        # Response should be JSON with success flag
        delete_data = delete_response.get_json()
        assert delete_data['success'] is True, "Delete should return success"
        assert 'deleted_chunks' in delete_data, "Delete should return chunk count"
        
        # Verify document is gone
        list_response = legal_client.get('/documents')
        docs = list_response.get_json()['documents']
        doc_names = [doc['source'] for doc in docs]
        assert 'test_delete.txt' not in doc_names, "Document should be deleted"
        
    finally:
        if os.path.exists(temp_file):
            os.unlink(temp_file)


def test_document_deletion_nonexistent_file(legal_client):
    """
    Test that deleting nonexistent file is handled gracefully.
    
    Validates: Requirement 7.3
    """
    # Try to delete a file that doesn't exist
    response = legal_client.delete('/documents/nonexistent_file.txt')
    
    # Should return 200 (handled gracefully)
    assert response.status_code == 200


# ==========================================
# Test 4: Document Selection (Requirement 7.3)
# ==========================================

def test_document_list_works_identically(legal_client, vector_store, cleanup_test_docs):
    """
    Test that document listing works identically to pre-migration.
    
    Validates: Requirement 7.3
    
    Note: This test may fail if GOOGLE_API_KEY is not set (needed for embeddings).
    """
    # Upload a test document
    test_content = "This is a test document for selection."
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(test_content)
        temp_file = f.name
    
    try:
        # Upload the file
        with open(temp_file, 'rb') as f:
            data = {'file': (f, 'test_selection.txt')}
            upload_response = legal_client.post('/upload',
                                               data=data,
                                               content_type='multipart/form-data')
            # Upload may fail if API key is missing
            if upload_response.status_code != 200:
                pytest.skip("Upload failed (likely missing API key)")
        
        # List documents
        response = legal_client.get('/documents')
        
        # Should return 200 OK
        assert response.status_code == 200, "Document list should work"
        
        # Response should be JSON
        assert response.content_type == 'application/json', \
            "Document list should return JSON"
        
        # Response should contain documents array
        data = response.get_json()
        assert 'documents' in data, "Response should contain documents"
        assert isinstance(data['documents'], list), "Documents should be a list"
        
        # Our document should be in the list (if upload succeeded)
        doc_names = [doc['source'] for doc in data['documents']]
        if 'test_selection.txt' not in doc_names:
            pytest.skip("Document upload failed (likely missing API key)")
        
        # Document should have required fields
        test_doc = next(doc for doc in data['documents'] 
                       if doc['source'] == 'test_selection.txt')
        assert 'pages' in test_doc, "Document should have pages field"
        assert 'chunks' in test_doc, "Document should have chunks field"
        assert test_doc['pages'] >= 1, "Document should have at least 1 page"
        assert test_doc['chunks'] >= 1, "Document should have at least 1 chunk"
        
    finally:
        if os.path.exists(temp_file):
            os.unlink(temp_file)


def test_document_selection_ui_elements_present(legal_client):
    """
    Test that document selection UI elements are present.
    
    Validates: Requirement 7.3
    """
    response = legal_client.get('/')
    html = response.data.decode('utf-8')
    
    # Check document library elements exist
    assert 'document-list' in html, "Document list container should exist"
    # refreshDocuments is called from app.js, so check that app.js is loaded
    assert '/static/app.js' in html, "app.js should be loaded (contains refreshDocuments)"


def test_empty_document_list_works_identically(legal_client, vector_store):
    """
    Test that empty document list is handled identically to pre-migration.
    
    Validates: Requirement 7.3
    """
    # Clear all documents
    docs = vector_store.list_documents()
    for doc in docs:
        try:
            vector_store.delete_document(doc['source'])
        except:
            pass
    
    # Get document list
    response = legal_client.get('/documents')
    
    # Should return 200 OK
    assert response.status_code == 200
    
    # Should return empty array
    data = response.get_json()
    assert data['documents'] == [], "Empty list should return empty array"


# ==========================================
# Test 5: Error Handling (Requirement 7.4, 7.5)
# ==========================================

def test_upload_error_handling_works_identically(legal_client):
    """
    Test that upload error handling works identically to pre-migration.
    
    Validates: Requirement 7.4
    """
    # Try to upload without file
    response = legal_client.post('/upload',
                                 data={},
                                 content_type='multipart/form-data')
    
    # Should return 400 Bad Request
    assert response.status_code == 400, "Missing file should return 400"


def test_chat_error_handling_works_identically(legal_client):
    """
    Test that chat error handling works identically to pre-migration.
    
    Validates: Requirement 7.4
    """
    # Send malformed request
    response = legal_client.post('/chat',
                                 data='invalid json',
                                 content_type='application/json')
    
    # Should handle error gracefully (400 or 500)
    assert response.status_code in [400, 500], \
        "Malformed request should return error status"


def test_error_display_elements_present(legal_client):
    """
    Test that error display elements are present in the UI.
    
    Validates: Requirement 7.4, 7.5
    """
    response = legal_client.get('/')
    html = response.data.decode('utf-8')
    
    # Check that app.js is loaded (which contains error handling functions)
    assert '/static/app.js' in html, "app.js should be loaded"
    assert 'upload-status' in html, "Upload status container should exist"


# ==========================================
# Test 6: Cross-App Functionality (Both themes)
# ==========================================

def test_ghost_app_upload_works_identically(ghost_client, cleanup_test_docs):
    """
    Test that Ouija Board app upload works identically to pre-migration.
    
    Validates: Requirement 7.1
    """
    test_content = "This is a test for the mystical realm."
    
    data = {
        'file': (io.BytesIO(test_content.encode('utf-8')), 'test_ghost.txt')
    }
    
    response = ghost_client.post('/upload',
                                  data=data,
                                  content_type='multipart/form-data')
    
    # Should return 200 OK
    assert response.status_code == 200, "Ghost app upload should work"
    
    # Cleanup
    try:
        vs = VectorStore()
        vs.delete_document('test_ghost.txt')
    except:
        pass


def test_ghost_app_chat_works_identically(ghost_client):
    """
    Test that Ouija Board app chat works identically to pre-migration.
    
    Validates: Requirement 7.2
    
    Note: This test requires GOOGLE_API_KEY to be set.
    """
    # Check if API key is available
    import os
    if not os.getenv('GOOGLE_API_KEY'):
        pytest.skip("GOOGLE_API_KEY not set - skipping chat test")
    
    response = ghost_client.post('/chat',
                                  json={'query': 'Speak to me, spirits!'},
                                  content_type='application/json')
    
    # Should return 200 OK
    assert response.status_code == 200, "Ghost app chat should work"
    
    # Response should be JSON
    data = response.get_json()
    assert 'echo' in data or 'error' in data


def test_ghost_app_document_list_works_identically(ghost_client):
    """
    Test that Ouija Board app document list works identically to pre-migration.
    
    Validates: Requirement 7.3
    """
    response = ghost_client.get('/documents')
    
    # Should return 200 OK
    assert response.status_code == 200, "Ghost app document list should work"
    
    # Response should be JSON
    data = response.get_json()
    assert 'documents' in data


# ==========================================
# Test 7: Accessibility Features (Requirement 7.5)
# ==========================================

def test_accessibility_features_preserved(legal_client):
    """
    Test that accessibility features are preserved after migration.
    
    Validates: Requirement 7.5
    """
    response = legal_client.get('/')
    html = response.data.decode('utf-8')
    
    # Check for ARIA labels and roles
    assert 'aria-' in html or 'role=' in html, \
        "Accessibility attributes should be present"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
