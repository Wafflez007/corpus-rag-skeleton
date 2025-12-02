"""
Test document library functionality after DaisyUI migration
Validates Requirements: 6.5, 7.3
"""
import pytest
from skeleton_core.app import create_app
from app_legal.config import Config as LegalConfig
from skeleton_core.vector_store import VectorStore
import tempfile
import os


@pytest.fixture
def legal_app():
    """Create Legal Eagle app instance for testing"""
    app = create_app(LegalConfig)
    app.config['TESTING'] = True
    return app


@pytest.fixture
def legal_client(legal_app):
    """Create test client for Legal Eagle app"""
    return legal_app.test_client()


@pytest.fixture
def vector_store():
    """Create vector store instance"""
    return VectorStore()


def test_document_list_endpoint_returns_json(legal_client):
    """Test that /documents endpoint returns proper JSON"""
    response = legal_client.get('/documents')
    assert response.status_code == 200
    
    data = response.get_json()
    assert 'documents' in data, "Response should contain 'documents' key"
    assert isinstance(data['documents'], list), "Documents should be a list"


def test_document_upload_and_list(legal_client, vector_store):
    """Test uploading a document and listing it"""
    # Create a temporary test file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("Test document content for library testing.")
        temp_file = f.name
    
    try:
        # Upload the file
        with open(temp_file, 'rb') as f:
            data = {'file': (f, 'test_doc.txt')}
            response = legal_client.post('/upload', 
                                        data=data,
                                        content_type='multipart/form-data')
            assert response.status_code == 200
        
        # List documents
        response = legal_client.get('/documents')
        assert response.status_code == 200
        
        data = response.get_json()
        documents = data['documents']
        
        # Check that our document is in the list
        doc_names = [doc['source'] for doc in documents]
        assert 'test_doc.txt' in doc_names, "Uploaded document should appear in list"
        
        # Find our document and check its structure
        test_doc = next(doc for doc in documents if doc['source'] == 'test_doc.txt')
        assert 'pages' in test_doc, "Document should have 'pages' field"
        assert 'chunks' in test_doc, "Document should have 'chunks' field"
        assert test_doc['pages'] >= 1, "Document should have at least 1 page"
        assert test_doc['chunks'] >= 1, "Document should have at least 1 chunk"
        
    finally:
        # Clean up
        if os.path.exists(temp_file):
            os.unlink(temp_file)
        
        # Delete the document from vector store
        try:
            vector_store.delete_document('test_doc.txt')
        except:
            pass


def test_document_delete_functionality(legal_client, vector_store):
    """Test deleting a document through the API"""
    # Create and upload a test document
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("Test document for deletion.")
        temp_file = f.name
    
    try:
        # Upload the file
        with open(temp_file, 'rb') as f:
            data = {'file': (f, 'delete_test.txt')}
            response = legal_client.post('/upload',
                                        data=data,
                                        content_type='multipart/form-data')
            assert response.status_code == 200
        
        # Verify it exists
        response = legal_client.get('/documents')
        data = response.get_json()
        doc_names = [doc['source'] for doc in data['documents']]
        assert 'delete_test.txt' in doc_names
        
        # Delete the document
        response = legal_client.delete('/documents/delete_test.txt')
        assert response.status_code == 200
        
        result = response.get_json()
        assert result['success'] is True, "Delete should return success"
        assert 'deleted_chunks' in result, "Delete should return deleted_chunks count"
        
        # Verify it's gone
        response = legal_client.get('/documents')
        data = response.get_json()
        doc_names = [doc['source'] for doc in data['documents']]
        assert 'delete_test.txt' not in doc_names, "Deleted document should not appear in list"
        
    finally:
        # Clean up temp file
        if os.path.exists(temp_file):
            os.unlink(temp_file)


def test_empty_document_list(legal_client, vector_store):
    """Test that empty document list is handled properly"""
    # Clear all documents first
    docs = vector_store.list_documents()
    for doc in docs:
        try:
            vector_store.delete_document(doc['source'])
        except:
            pass
    
    # Get document list
    response = legal_client.get('/documents')
    assert response.status_code == 200
    
    data = response.get_json()
    assert data['documents'] == [], "Empty list should return empty array"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
