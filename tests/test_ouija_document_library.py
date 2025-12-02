"""
Test Ouija Board Document Library Migration
Verifies that the document library uses DaisyUI components with mystical styling
"""

import pytest
from skeleton_core.app import create_app
from app_ghost.config import Config as GhostConfig


@pytest.fixture
def ghost_client():
    """Create a test client for the Ghost/Ouija Board app"""
    app = create_app(GhostConfig)
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_ouija_document_library_uses_daisyui_card(ghost_client):
    """Test that document library uses DaisyUI card component"""
    response = ghost_client.get('/')
    html = response.data.decode('utf-8')
    
    # Check for DaisyUI card classes in library section
    assert 'id="library-section"' in html
    assert 'class="card bg-base-200 shadow-xl' in html
    assert 'class="card-body"' in html


def test_ouija_document_library_has_mystical_title(ghost_client):
    """Test that document library has mystical title"""
    response = ghost_client.get('/')
    html = response.data.decode('utf-8')
    
    # Check for mystical title
    assert 'Summoned Texts' in html or '📚' in html


def test_ouija_checkboxes_use_daisyui(ghost_client):
    """Test that checkboxes use DaisyUI checkbox component"""
    response = ghost_client.get('/')
    html = response.data.decode('utf-8')
    
    # Check for select-all checkbox in HTML (static)
    assert 'id="select-all-docs"' in html
    assert 'onchange="toggleAllDocuments()"' in html
    assert 'class="checkbox checkbox-sm"' in html


def test_ouija_delete_buttons_use_daisyui(ghost_client):
    """Test that delete buttons use DaisyUI button component with mystical styling"""
    # This test verifies the JavaScript rendering logic
    # The actual buttons are rendered dynamically by app.js
    response = ghost_client.get('/static/app.js')
    js_code = response.data.decode('utf-8')
    
    # Check that the JavaScript renders DaisyUI button classes
    assert 'btn btn-ghost btn-xs text-error' in js_code
    assert 'min-h-[44px] min-w-[44px]' in js_code


def test_ouija_document_list_container(ghost_client):
    """Test that document list container has proper styling"""
    response = ghost_client.get('/')
    html = response.data.decode('utf-8')
    
    # Check for document list container
    assert 'id="document-list"' in html
    assert 'max-h-[500px] overflow-y-auto' in html
    assert 'bg-base-100 border border-base-300' in html


def test_ouija_theme_applied(ghost_client):
    """Test that Ouija Board theme is applied"""
    response = ghost_client.get('/')
    html = response.data.decode('utf-8')
    
    # Check for dark-gothic theme class
    assert 'theme-dark-gothic' in html
    assert 'data-theme="ouija-board"' in html


def test_ouija_document_library_responsive(ghost_client):
    """Test that document library has responsive layout classes"""
    response = ghost_client.get('/')
    html = response.data.decode('utf-8')
    
    # Check for responsive grid classes (mobile: 1 col, tablet: 2 cols, desktop: 3 cols)
    assert 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3' in html
    assert 'md:col-span-1 lg:col-span-1' in html  # Library column
    assert 'md:col-span-1 lg:col-span-2' in html  # Chat column


def test_ouija_selection_count_display(ghost_client):
    """Test that selection count display is present"""
    response = ghost_client.get('/')
    html = response.data.decode('utf-8')
    
    # Check for selection count display
    assert 'id="selection-count"' in html
    assert '0 selected' in html


def test_ouija_mystical_empty_state(ghost_client):
    """Test that empty state has mystical message"""
    response = ghost_client.get('/')
    html = response.data.decode('utf-8')
    
    # Check for mystical empty state message
    assert 'No spirits bound yet...' in html


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
