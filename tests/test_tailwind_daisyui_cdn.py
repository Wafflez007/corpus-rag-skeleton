"""
Tests for Tailwind CSS and DaisyUI CDN integration.

Feature: tailwind-daisyui-integration, Property 1: CDN resources are included
Validates: Requirements 1.1, 1.2
"""

import re
from pathlib import Path
import pytest


def get_index_template_content():
    """Read the index.html template content."""
    template_path = Path(__file__).parent.parent / "skeleton_core" / "templates" / "index.html"
    with open(template_path, 'r', encoding='utf-8') as f:
        return f.read()


def get_launcher_content():
    """Read the launcher.py content."""
    launcher_path = Path(__file__).parent.parent / "launcher.py"
    with open(launcher_path, 'r', encoding='utf-8') as f:
        return f.read()


def test_index_template_includes_tailwind_cdn():
    """
    Verify that the index.html template includes Tailwind CSS CDN link.
    
    Validates: Requirements 1.1
    """
    content = get_index_template_content()
    
    # Check for Tailwind CSS CDN
    assert 'cdn.tailwindcss.com' in content, (
        "index.html should include Tailwind CSS CDN link"
    )
    
    # Verify it's in a script tag
    tailwind_pattern = r'<script\s+src="https://cdn\.tailwindcss\.com"'
    assert re.search(tailwind_pattern, content), (
        "Tailwind CSS should be loaded via script tag"
    )


def test_index_template_includes_daisyui_cdn():
    """
    Verify that the index.html template includes DaisyUI CDN link.
    
    Validates: Requirements 1.2
    """
    content = get_index_template_content()
    
    # Check for DaisyUI CDN
    assert 'daisyui' in content, (
        "index.html should include DaisyUI CDN link"
    )
    
    # Verify it's in a link tag with correct attributes
    daisyui_pattern = r'<link\s+href="https://cdn\.jsdelivr\.net/npm/daisyui@[\d.]+/dist/full\.min\.css"\s+rel="stylesheet"\s+type="text/css"'
    assert re.search(daisyui_pattern, content), (
        "DaisyUI should be loaded via link tag with proper attributes"
    )


def test_index_template_includes_tailwind_config():
    """
    Verify that the index.html template includes inline Tailwind configuration.
    
    Validates: Requirements 1.3
    """
    content = get_index_template_content()
    
    # Check for Tailwind config
    assert 'tailwind.config' in content, (
        "index.html should include Tailwind configuration"
    )
    
    # Verify custom colors are defined
    custom_colors = [
        'legal-navy',
        'legal-gold',
        'ghost-dark',
        'ghost-glow',
        'ghost-blood'
    ]
    
    for color in custom_colors:
        assert color in content, (
            f"Tailwind config should define custom color: {color}"
        )


def test_launcher_includes_tailwind_cdn():
    """
    Verify that the launcher.py includes Tailwind CSS CDN link.
    
    Validates: Requirements 1.1
    """
    content = get_launcher_content()
    
    # Check for Tailwind CSS CDN
    assert 'cdn.tailwindcss.com' in content, (
        "launcher.py should include Tailwind CSS CDN link"
    )
    
    # Verify it's in a script tag
    tailwind_pattern = r'<script\s+src="https://cdn\.tailwindcss\.com"'
    assert re.search(tailwind_pattern, content), (
        "Tailwind CSS should be loaded via script tag in launcher"
    )


def test_launcher_includes_daisyui_cdn():
    """
    Verify that the launcher.py includes DaisyUI CDN link.
    
    Validates: Requirements 1.2
    """
    content = get_launcher_content()
    
    # Check for DaisyUI CDN
    assert 'daisyui' in content, (
        "launcher.py should include DaisyUI CDN link"
    )
    
    # Verify it's in a link tag
    daisyui_pattern = r'<link\s+href="https://cdn\.jsdelivr\.net/npm/daisyui@[\d.]+/dist/full\.min\.css"'
    assert re.search(daisyui_pattern, content), (
        "DaisyUI should be loaded via link tag in launcher"
    )


def test_launcher_includes_tailwind_config():
    """
    Verify that the launcher.py includes inline Tailwind configuration.
    
    Validates: Requirements 1.3
    """
    content = get_launcher_content()
    
    # Check for Tailwind config
    assert 'tailwind.config' in content, (
        "launcher.py should include Tailwind configuration"
    )
    
    # Verify custom colors are defined
    custom_colors = [
        'legal-navy',
        'legal-gold',
        'ghost-dark',
        'ghost-glow'
    ]
    
    for color in custom_colors:
        assert color in content, (
            f"Tailwind config in launcher should define custom color: {color}"
        )


def test_cdn_links_order():
    """
    Verify that CDN links are in the correct order (Tailwind before DaisyUI).
    
    DaisyUI depends on Tailwind, so Tailwind must be loaded first.
    """
    content = get_index_template_content()
    
    tailwind_pos = content.find('cdn.tailwindcss.com')
    daisyui_pos = content.find('daisyui')
    
    assert tailwind_pos < daisyui_pos, (
        "Tailwind CSS should be loaded before DaisyUI"
    )


def test_tailwind_config_after_cdn():
    """
    Verify that Tailwind configuration comes after the CDN script.
    
    The configuration must be defined after Tailwind is loaded.
    """
    content = get_index_template_content()
    
    tailwind_cdn_pos = content.find('cdn.tailwindcss.com')
    tailwind_config_pos = content.find('tailwind.config')
    
    assert tailwind_cdn_pos < tailwind_config_pos, (
        "Tailwind configuration should come after CDN script"
    )


def test_custom_colors_have_valid_hex_values():
    """
    Verify that custom colors in Tailwind config use valid hex color values.
    """
    content = get_index_template_content()
    
    # Extract the tailwind.config section
    config_start = content.find('tailwind.config')
    config_end = content.find('</script>', config_start)
    config_section = content[config_start:config_end]
    
    # Find all color definitions
    color_pattern = r"'([\w-]+)':\s*'(#[0-9a-fA-F]{6})'"
    colors = re.findall(color_pattern, config_section)
    
    assert len(colors) > 0, "Should find custom color definitions"
    
    # Verify each color has a valid hex value
    for color_name, hex_value in colors:
        assert hex_value.startswith('#'), f"{color_name} should have hex color starting with #"
        assert len(hex_value) == 7, f"{color_name} should have 6-digit hex color"
        assert re.match(r'^#[0-9a-fA-F]{6}$', hex_value), (
            f"{color_name} should have valid hex color: {hex_value}"
        )


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
