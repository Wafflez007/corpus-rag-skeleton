"""
Tests for DaisyUI theme rendering in HTML templates
"""
import sys
import os
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from skeleton_core.app import create_app
from app_legal.config import Config as LegalConfig
from app_ghost.config import Config as GhostConfig


def test_legal_theme_config_in_html():
    """Test that Legal Eagle theme configuration is rendered in HTML"""
    app = create_app(LegalConfig)
    
    with app.test_client() as client:
        response = client.get('/')
        html = response.data.decode('utf-8')
        
        # Check that DaisyUI theme config is present
        assert 'daisyui' in html
        assert 'themes' in html
        assert 'legal-eagle' in html
        
        # Check that theme colors are present
        assert '#0f172a' in html  # primary color
        assert '#ca8a04' in html  # accent color


def test_ghost_theme_config_in_html():
    """Test that Ouija Board theme configuration is rendered in HTML"""
    app = create_app(GhostConfig)
    
    with app.test_client() as client:
        response = client.get('/')
        html = response.data.decode('utf-8')
        
        # Check that DaisyUI theme config is present
        assert 'daisyui' in html
        assert 'themes' in html
        assert 'ouija-board' in html
        
        # Check that theme colors are present
        assert '#8b0000' in html  # primary color
        assert '#ff3f3f' in html  # accent color


def test_theme_data_attribute():
    """Test that data-theme attribute is correctly set on body tag"""
    legal_app = create_app(LegalConfig)
    ghost_app = create_app(GhostConfig)
    
    with legal_app.test_client() as client:
        response = client.get('/')
        html = response.data.decode('utf-8')
        assert 'data-theme="legal-eagle"' in html
    
    with ghost_app.test_client() as client:
        response = client.get('/')
        html = response.data.decode('utf-8')
        assert 'data-theme="ouija-board"' in html


def test_tailwind_config_includes_daisyui():
    """Test that Tailwind config includes DaisyUI configuration"""
    app = create_app(LegalConfig)
    
    with app.test_client() as client:
        response = client.get('/')
        html = response.data.decode('utf-8')
        
        # Check that tailwind.config includes daisyui section
        assert 'tailwind.config' in html
        assert 'daisyui:' in html or 'daisyui' in html
