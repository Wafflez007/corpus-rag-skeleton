"""
Tests for DaisyUI theme configuration
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app_legal.config import Config as LegalConfig
from app_ghost.config import Config as GhostConfig


def test_legal_eagle_theme_config_exists():
    """Test that Legal Eagle has DaisyUI theme configuration"""
    assert hasattr(LegalConfig, 'DAISYUI_THEME')
    assert hasattr(LegalConfig, 'DAISYUI_THEME_CONFIG')


def test_legal_eagle_theme_name():
    """Test that Legal Eagle uses the correct theme name"""
    assert LegalConfig.DAISYUI_THEME == "legal-eagle"


def test_legal_eagle_theme_colors():
    """Test that Legal Eagle theme has correct color palette"""
    theme_config = LegalConfig.DAISYUI_THEME_CONFIG
    assert "legal-eagle" in theme_config
    
    legal_theme = theme_config["legal-eagle"]
    assert legal_theme["primary"] == "#0f172a"  # Deep slate navy
    assert legal_theme["secondary"] == "#334155"  # Steel grey
    assert legal_theme["accent"] == "#ca8a04"  # Muted gold
    assert legal_theme["base-100"] == "#f8fafc"  # Light grey background


def test_ouija_board_theme_config_exists():
    """Test that Ouija Board has DaisyUI theme configuration"""
    assert hasattr(GhostConfig, 'DAISYUI_THEME')
    assert hasattr(GhostConfig, 'DAISYUI_THEME_CONFIG')


def test_ouija_board_theme_name():
    """Test that Ouija Board uses the correct theme name"""
    assert GhostConfig.DAISYUI_THEME == "ouija-board"


def test_ouija_board_theme_colors():
    """Test that Ouija Board theme has correct color palette"""
    theme_config = GhostConfig.DAISYUI_THEME_CONFIG
    assert "ouija-board" in theme_config
    
    ouija_theme = theme_config["ouija-board"]
    assert ouija_theme["primary"] == "#8b0000"  # Deep blood red
    assert ouija_theme["secondary"] == "#2b0505"  # Dried blood
    assert ouija_theme["accent"] == "#ff3f3f"  # Bright red glow
    assert ouija_theme["base-100"] == "#050505"  # Void black


def test_theme_isolation():
    """Test that Legal Eagle and Ouija Board themes are different"""
    legal_theme = LegalConfig.DAISYUI_THEME
    ouija_theme = GhostConfig.DAISYUI_THEME
    
    assert legal_theme != ouija_theme
    assert legal_theme == "legal-eagle"
    assert ouija_theme == "ouija-board"


def test_theme_color_isolation():
    """Test that theme colors are distinct between apps"""
    legal_colors = LegalConfig.DAISYUI_THEME_CONFIG["legal-eagle"]
    ouija_colors = GhostConfig.DAISYUI_THEME_CONFIG["ouija-board"]
    
    # Primary colors should be different
    assert legal_colors["primary"] != ouija_colors["primary"]
    
    # Base backgrounds should be different
    assert legal_colors["base-100"] != ouija_colors["base-100"]
