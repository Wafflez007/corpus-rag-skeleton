"""
Tests for Ouija Board upload section migration to DaisyUI.

Validates that the upload section uses DaisyUI components correctly in Ghost theme.
"""

import pytest
from bs4 import BeautifulSoup
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from skeleton_core.app import create_app
from app_ghost.config import Config


@pytest.fixture
def app():
    """Create test Flask app with Ghost/Ouija Board config."""
    app = create_app(Config)
    app.config['TESTING'] = True
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


def test_ghost_upload_section_uses_daisyui_card(client):
    """Test that Ghost theme upload section uses DaisyUI card component."""
    response = client.get('/')
    assert response.status_code == 200
    
    soup = BeautifulSoup(response.data, 'html.parser')
    upload_section = soup.find('div', id='upload-section')
    
    assert upload_section is not None, "Upload section not found"
    assert 'card' in upload_section.get('class', []), "Upload section should use DaisyUI card class"
    assert 'bg-base-200' in upload_section.get('class', []), "Upload section should use DaisyUI bg-base-200 class"


def test_ghost_file_input_uses_daisyui_component(client):
    """Test that Ghost theme file input uses DaisyUI file-input component."""
    response = client.get('/')
    soup = BeautifulSoup(response.data, 'html.parser')
    
    file_input = soup.find('input', id='fileInput')
    
    assert file_input is not None, "File input not found"
    assert 'file-input' in file_input.get('class', []), "File input should use DaisyUI file-input class"
    assert 'file-input-bordered' in file_input.get('class', []), "File input should use DaisyUI file-input-bordered class"


def test_ghost_upload_button_uses_daisyui_component(client):
    """Test that Ghost theme upload button uses DaisyUI button component."""
    response = client.get('/')
    soup = BeautifulSoup(response.data, 'html.parser')
    
    upload_button = soup.find('button', onclick='uploadFile()')
    
    assert upload_button is not None, "Upload button not found"
    assert 'btn' in upload_button.get('class', []), "Upload button should use DaisyUI btn class"
    assert 'btn-primary' in upload_button.get('class', []), "Upload button should use DaisyUI btn-primary class"


def test_ghost_progress_bar_uses_daisyui_component(client):
    """Test that Ghost theme progress bar uses DaisyUI progress component."""
    response = client.get('/')
    soup = BeautifulSoup(response.data, 'html.parser')
    
    progress_bar = soup.find('progress', id='progress-bar')
    
    assert progress_bar is not None, "Progress bar not found"
    assert 'progress' in progress_bar.get('class', []), "Progress bar should use DaisyUI progress class"
    assert 'progress-primary' in progress_bar.get('class', []), "Progress bar should use DaisyUI progress-primary class"


def test_ghost_theme_button_text(client):
    """Test that Ghost theme uses 'OFFER' instead of 'UPLOAD' for button text."""
    response = client.get('/')
    soup = BeautifulSoup(response.data, 'html.parser')
    
    upload_button = soup.find('button', onclick='uploadFile()')
    
    assert upload_button is not None, "Upload button not found"
    assert 'OFFER' in upload_button.text, "Ghost theme button should say 'OFFER'"


def test_ghost_theme_card_title(client):
    """Test that Ghost theme uses mystical title for upload section."""
    response = client.get('/')
    soup = BeautifulSoup(response.data, 'html.parser')
    
    upload_section = soup.find('div', id='upload-section')
    card_title = upload_section.find('h2', class_='card-title')
    
    assert card_title is not None, "Card title not found"
    assert 'Summon Document' in card_title.text, "Ghost theme should use 'Summon Document' title"
