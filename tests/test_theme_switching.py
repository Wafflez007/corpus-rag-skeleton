"""
Tests for theme switching mechanism in Flask app
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from skeleton_core.app import create_app
from app_legal.config import Config as LegalConfig
from app_ghost.config import Config as GhostConfig


def test_legal_app_has_theme_config():
    """Test that Legal Eagle app has DaisyUI theme configuration"""
    app = create_app(LegalConfig)
    
    assert app.config.get('DAISYUI_THEME') == "legal-eagle"
    assert app.config.get('DAISYUI_THEME_CONFIG') is not None
    assert "legal-eagle" in app.config.get('DAISYUI_THEME_CONFIG')


def test_ghost_app_has_theme_config():
    """Test that Ouija Board app has DaisyUI theme configuration"""
    app = create_app(GhostConfig)
    
    assert app.config.get('DAISYUI_THEME') == "ouija-board"
    assert app.config.get('DAISYUI_THEME_CONFIG') is not None
    assert "ouija-board" in app.config.get('DAISYUI_THEME_CONFIG')


def test_legal_app_renders_with_theme():
    """Test that Legal Eagle app renders template with theme data"""
    app = create_app(LegalConfig)
    
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200
        
        # Check that the theme is applied in the HTML
        html = response.data.decode('utf-8')
        assert 'data-theme="legal-eagle"' in html
        assert 'legal-eagle' in html


def test_ghost_app_renders_with_theme():
    """Test that Ouija Board app renders template with theme data"""
    app = create_app(GhostConfig)
    
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200
        
        # Check that the theme is applied in the HTML
        html = response.data.decode('utf-8')
        assert 'data-theme="ouija-board"' in html
        assert 'ouija-board' in html


def test_theme_isolation_in_apps():
    """Test that each app maintains its own theme configuration"""
    legal_app = create_app(LegalConfig)
    ghost_app = create_app(GhostConfig)
    
    # Verify Legal Eagle theme
    assert legal_app.config.get('DAISYUI_THEME') == "legal-eagle"
    legal_theme_config = legal_app.config.get('DAISYUI_THEME_CONFIG')
    assert legal_theme_config["legal-eagle"]["primary"] == "#0f172a"
    
    # Verify Ouija Board theme
    assert ghost_app.config.get('DAISYUI_THEME') == "ouija-board"
    ghost_theme_config = ghost_app.config.get('DAISYUI_THEME_CONFIG')
    assert ghost_theme_config["ouija-board"]["primary"] == "#8b0000"
    
    # Verify they are different
    assert legal_app.config.get('DAISYUI_THEME') != ghost_app.config.get('DAISYUI_THEME')
