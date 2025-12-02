"""
Tests for Legal Eagle upload section migration to DaisyUI.

Validates that the upload section uses DaisyUI components correctly.
"""

import pytest
from bs4 import BeautifulSoup
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


def test_upload_section_uses_daisyui_card(client):
    """Test that upload section uses DaisyUI card component."""
    response = client.get('/')
    assert response.status_code == 200
    
    soup = BeautifulSoup(response.data, 'html.parser')
    upload_section = soup.find('div', id='upload-section')
    
    assert upload_section is not None, "Upload section not found"
    assert 'card' in upload_section.get('class', []), "Upload section should use DaisyUI card class"
    assert 'bg-base-200' in upload_section.get('class', []), "Upload section should use DaisyUI bg-base-200 class"
    assert 'shadow-xl' in upload_section.get('class', []), "Upload section should use DaisyUI shadow-xl class"


def test_upload_section_has_card_body(client):
    """Test that upload section has card-body wrapper."""
    response = client.get('/')
    soup = BeautifulSoup(response.data, 'html.parser')
    
    upload_section = soup.find('div', id='upload-section')
    card_body = upload_section.find('div', class_='card-body')
    
    assert card_body is not None, "Upload section should have card-body div"


def test_file_input_uses_daisyui_component(client):
    """Test that file input uses DaisyUI file-input component."""
    response = client.get('/')
    soup = BeautifulSoup(response.data, 'html.parser')
    
    file_input = soup.find('input', id='fileInput')
    
    assert file_input is not None, "File input not found"
    assert 'file-input' in file_input.get('class', []), "File input should use DaisyUI file-input class"
    assert 'file-input-bordered' in file_input.get('class', []), "File input should use DaisyUI file-input-bordered class"


def test_upload_button_uses_daisyui_component(client):
    """Test that upload button uses DaisyUI button component."""
    response = client.get('/')
    soup = BeautifulSoup(response.data, 'html.parser')
    
    # Find the upload button (it has onclick="uploadFile()")
    upload_button = soup.find('button', onclick='uploadFile()')
    
    assert upload_button is not None, "Upload button not found"
    assert 'btn' in upload_button.get('class', []), "Upload button should use DaisyUI btn class"
    assert 'btn-primary' in upload_button.get('class', []), "Upload button should use DaisyUI btn-primary class"


def test_upload_button_meets_touch_target_size(client):
    """Test that upload button meets minimum touch target size (44px)."""
    response = client.get('/')
    soup = BeautifulSoup(response.data, 'html.parser')
    
    upload_button = soup.find('button', onclick='uploadFile()')
    
    assert upload_button is not None, "Upload button not found"
    classes = upload_button.get('class', [])
    
    # Check for min-h-[44px] class
    has_min_height = any('min-h-' in cls for cls in classes)
    assert has_min_height, "Upload button should have minimum height class for touch targets"


def test_progress_bar_uses_daisyui_component(client):
    """Test that progress bar uses DaisyUI progress component."""
    response = client.get('/')
    soup = BeautifulSoup(response.data, 'html.parser')
    
    progress_bar = soup.find('progress', id='progress-bar')
    
    assert progress_bar is not None, "Progress bar not found"
    assert 'progress' in progress_bar.get('class', []), "Progress bar should use DaisyUI progress class"
    assert 'progress-primary' in progress_bar.get('class', []), "Progress bar should use DaisyUI progress-primary class"


def test_progress_bar_has_correct_attributes(client):
    """Test that progress bar has correct HTML5 attributes."""
    response = client.get('/')
    soup = BeautifulSoup(response.data, 'html.parser')
    
    progress_bar = soup.find('progress', id='progress-bar')
    
    assert progress_bar is not None, "Progress bar not found"
    assert progress_bar.get('value') == '0', "Progress bar should have initial value of 0"
    assert progress_bar.get('max') == '100', "Progress bar should have max value of 100"


def test_upload_status_uses_tailwind_utilities(client):
    """Test that upload status message uses Tailwind utilities."""
    response = client.get('/')
    soup = BeautifulSoup(response.data, 'html.parser')
    
    upload_status = soup.find('p', id='upload-status')
    
    assert upload_status is not None, "Upload status not found"
    classes = upload_status.get('class', [])
    
    # Check for Tailwind utility classes
    assert 'text-xs' in classes, "Upload status should use Tailwind text-xs class"
    assert 'font-mono' in classes, "Upload status should use Tailwind font-mono class"
    assert 'tracking-wider' in classes, "Upload status should use Tailwind tracking-wider class"


def test_responsive_layout_classes(client):
    """Test that upload section uses responsive Tailwind classes."""
    response = client.get('/')
    soup = BeautifulSoup(response.data, 'html.parser')
    
    # Find the flex container with file input and button
    upload_section = soup.find('div', id='upload-section')
    flex_container = upload_section.find('div', class_='flex')
    
    assert flex_container is not None, "Flex container not found"
    classes = flex_container.get('class', [])
    
    # Check for responsive classes
    assert 'flex-col' in classes, "Should have flex-col for mobile"
    assert 'md:flex-row' in classes, "Should have md:flex-row for desktop"


def test_card_title_uses_daisyui_class(client):
    """Test that card title uses DaisyUI card-title class."""
    response = client.get('/')
    soup = BeautifulSoup(response.data, 'html.parser')
    
    upload_section = soup.find('div', id='upload-section')
    card_title = upload_section.find('h2', class_='card-title')
    
    assert card_title is not None, "Card title not found"
    assert 'card-title' in card_title.get('class', []), "Title should use DaisyUI card-title class"


def test_no_custom_css_classes_on_upload_section(client):
    """Test that upload section doesn't use old custom CSS classes."""
    response = client.get('/')
    soup = BeautifulSoup(response.data, 'html.parser')
    
    upload_section = soup.find('div', id='upload-section')
    classes = upload_section.get('class', [])
    
    # These are old custom CSS classes that should be removed
    old_classes = ['ouija-border', 'legal-border', 'professional-shadow']
    
    for old_class in old_classes:
        assert old_class not in classes, f"Upload section should not use old custom class: {old_class}"


def test_queue_status_uses_tailwind_utilities(client):
    """Test that queue status uses Tailwind utilities."""
    response = client.get('/')
    soup = BeautifulSoup(response.data, 'html.parser')
    
    queue_status = soup.find('div', id='queue-status')
    
    assert queue_status is not None, "Queue status not found"
    classes = queue_status.get('class', [])
    
    # Check for Tailwind utility classes
    assert 'hidden' in classes, "Queue status should be hidden by default"
    assert 'mt-2' in classes, "Queue status should have margin-top"
    assert 'text-sm' in classes, "Queue status should use text-sm class"
