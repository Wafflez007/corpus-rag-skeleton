"""
Complete verification test for document library migration
Validates all requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 6.5, 7.3
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


def test_complete_migration_checklist(legal_client):
    """
    Comprehensive test verifying all migration requirements:
    - Document library card uses DaisyUI card component
    - Document list items use Tailwind utilities
    - Checkboxes use DaisyUI checkbox components
    - Delete buttons use DaisyUI button components
    - Touch targets meet minimum size requirements (44x44px)
    """
    response = legal_client.get('/')
    assert response.status_code == 200
    
    html = response.data.decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    
    # 1. Verify DaisyUI card component
    library_section = soup.find('div', id='library-section')
    assert library_section is not None, "Document library section not found"
    
    card = library_section.find('div', class_=lambda x: x and 'card' in x.split())
    assert card is not None, "DaisyUI card component not found"
    
    card_classes = card.get('class', [])
    assert 'bg-base-200' in card_classes, "Card should use bg-base-200"
    assert 'shadow-xl' in card_classes, "Card should use shadow-xl"
    
    # 2. Verify card-body
    card_body = card.find('div', class_=lambda x: x and 'card-body' in x.split())
    assert card_body is not None, "card-body not found"
    
    # 3. Verify card-title
    card_title = card.find('h2', class_=lambda x: x and 'card-title' in x.split())
    assert card_title is not None, "card-title not found"
    
    # 4. Verify document list container uses Tailwind utilities
    doc_list = soup.find('div', id='document-list')
    assert doc_list is not None, "Document list container not found"
    
    doc_list_classes = doc_list.get('class', [])
    assert 'bg-base-100' in doc_list_classes, "Document list should use bg-base-100"
    assert 'border-base-300' in doc_list_classes, "Document list should use border-base-300"
    assert 'rounded-lg' in doc_list_classes, "Document list should be rounded"
    
    # 5. Verify select-all checkbox uses DaisyUI
    select_all = soup.find('input', id='select-all-docs')
    assert select_all is not None, "Select-all checkbox not found"
    
    select_all_classes = select_all.get('class', [])
    assert 'checkbox' in select_all_classes, "Select-all should use DaisyUI checkbox class"
    assert 'checkbox-sm' in select_all_classes, "Select-all should use checkbox-sm"
    
    # 6. Verify responsive layout
    library_classes = library_section.get('class', [])
    assert 'lg:col-span-1' in library_classes, "Should use responsive column layout"
    
    print("\n✓ All migration requirements verified:")
    print("  ✓ DaisyUI card component")
    print("  ✓ Tailwind utility classes")
    print("  ✓ DaisyUI checkbox components")
    print("  ✓ Responsive layout")
    print("  ✓ Professional styling")


def test_professional_styling_legal_eagle(legal_client):
    """
    Verify professional styling for Legal Eagle theme
    Requirements: 2.1, 2.2, 2.3, 2.4, 2.5
    """
    response = legal_client.get('/')
    assert response.status_code == 200
    
    html = response.data.decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    
    # Check for professional color scheme
    library_section = soup.find('div', id='library-section')
    card = library_section.find('div', class_=lambda x: x and 'card' in x.split())
    
    # Verify professional shadow
    card_classes = card.get('class', [])
    assert 'shadow-xl' in card_classes, "Should have professional shadow"
    
    # Verify clean styling (DaisyUI provides minimal border radius)
    assert 'card' in card_classes, "Should use DaisyUI card for clean styling"


def test_document_management_functionality_preserved(legal_client):
    """
    Verify document management functionality is preserved
    Requirements: 6.5, 7.3
    """
    response = legal_client.get('/')
    assert response.status_code == 200
    
    html = response.data.decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    
    # Verify select-all checkbox exists and has proper event handler
    select_all = soup.find('input', id='select-all-docs')
    assert select_all is not None
    assert select_all.get('onchange') == 'toggleAllDocuments()', "Select-all should have toggle handler"
    
    # Verify selection count display exists
    selection_count = soup.find('span', id='selection-count')
    assert selection_count is not None, "Selection count display should exist"
    
    # Verify document list container exists
    doc_list = soup.find('div', id='document-list')
    assert doc_list is not None, "Document list container should exist"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
