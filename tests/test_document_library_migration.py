"""
Test document library migration to DaisyUI components
Validates Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 6.5, 7.3
"""
import pytest
from bs4 import BeautifulSoup
from skeleton_core.app import create_app
from app_legal.config import Config as LegalConfig


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


def test_document_library_uses_daisyui_card(legal_client):
    """Test that document library section uses DaisyUI card component"""
    response = legal_client.get('/')
    assert response.status_code == 200
    
    html = response.data.decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    
    # Find the document library section
    library_section = soup.find('div', id='library-section')
    assert library_section is not None, "Document library section not found"
    
    # Check that it contains a DaisyUI card
    card = library_section.find('div', class_=lambda x: x and 'card' in x.split())
    assert card is not None, "DaisyUI card component not found in document library"
    
    # Check for card-body
    card_body = card.find('div', class_=lambda x: x and 'card-body' in x.split())
    assert card_body is not None, "card-body not found in document library card"


def test_document_library_has_card_title(legal_client):
    """Test that document library has proper card-title"""
    response = legal_client.get('/')
    assert response.status_code == 200
    
    html = response.data.decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    
    # Find the document library section
    library_section = soup.find('div', id='library-section')
    
    # Check for card-title
    card_title = library_section.find('h2', class_=lambda x: x and 'card-title' in x.split())
    assert card_title is not None, "card-title not found in document library"
    
    # Verify it contains "Library" text
    assert 'Library' in card_title.get_text(), "Card title should contain 'Library'"


def test_select_all_checkbox_uses_daisyui(legal_client):
    """Test that select-all checkbox uses DaisyUI checkbox component"""
    response = legal_client.get('/')
    assert response.status_code == 200
    
    html = response.data.decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    
    # Find the select-all checkbox
    select_all = soup.find('input', id='select-all-docs')
    assert select_all is not None, "Select-all checkbox not found"
    
    # Check that it has DaisyUI checkbox classes
    classes = select_all.get('class', [])
    assert 'checkbox' in classes, "Select-all checkbox should have 'checkbox' class"


def test_document_list_container_styling(legal_client):
    """Test that document list container uses Tailwind utilities"""
    response = legal_client.get('/')
    assert response.status_code == 200
    
    html = response.data.decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    
    # Find the document list container
    doc_list = soup.find('div', id='document-list')
    assert doc_list is not None, "Document list container not found"
    
    # Check for Tailwind utility classes
    classes = doc_list.get('class', [])
    assert 'bg-base-100' in classes, "Document list should use bg-base-100"
    assert 'border-base-300' in classes, "Document list should use border-base-300"


def test_document_library_shadow_styling(legal_client):
    """Test that document library card has proper shadow styling"""
    response = legal_client.get('/')
    assert response.status_code == 200
    
    html = response.data.decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    
    # Find the document library card
    library_section = soup.find('div', id='library-section')
    card = library_section.find('div', class_=lambda x: x and 'card' in x.split())
    
    # Check for shadow-xl class
    classes = card.get('class', [])
    assert 'shadow-xl' in classes, "Document library card should have shadow-xl class"


def test_document_library_responsive_layout(legal_client):
    """Test that document library uses responsive grid layout"""
    response = legal_client.get('/')
    assert response.status_code == 200
    
    html = response.data.decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    
    # Find the library section
    library_section = soup.find('div', id='library-section')
    assert library_section is not None
    
    # Check for responsive column classes
    classes = library_section.get('class', [])
    assert 'lg:col-span-1' in classes, "Document library should use lg:col-span-1 for responsive layout"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
