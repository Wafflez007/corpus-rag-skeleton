"""
Tests for launcher page Tailwind and DaisyUI migration.

Validates that the launcher page uses Tailwind utilities and DaisyUI components
instead of custom CSS classes.
"""

import re
from pathlib import Path
import pytest


def get_launcher_content():
    """Read the launcher.py content."""
    launcher_path = Path(__file__).parent.parent / "launcher.py"
    with open(launcher_path, 'r', encoding='utf-8') as f:
        return f.read()


def test_launcher_uses_tailwind_flex_utilities():
    """
    Verify that the launcher uses Tailwind flex utilities instead of custom CSS.
    
    Validates: Requirements 4.1, 4.2
    """
    content = get_launcher_content()
    
    # Check for Tailwind flex classes
    tailwind_flex_patterns = [
        r'class="[^"]*flex[^"]*"',
        r'class="[^"]*flex-col[^"]*"',
        r'class="[^"]*flex-row[^"]*"',
        r'class="[^"]*flex-1[^"]*"',
        r'class="[^"]*items-center[^"]*"',
        r'class="[^"]*justify-center[^"]*"'
    ]
    
    for pattern in tailwind_flex_patterns:
        assert re.search(pattern, content), (
            f"Launcher should use Tailwind flex utilities: {pattern}"
        )


def test_launcher_uses_daisyui_button_components():
    """
    Verify that the launcher uses DaisyUI button components.
    
    Validates: Requirements 4.1, 4.2
    """
    content = get_launcher_content()
    
    # Check for DaisyUI button classes
    assert re.search(r'class="[^"]*btn[^"]*"', content), (
        "Launcher should use DaisyUI btn component"
    )
    
    assert re.search(r'class="[^"]*btn-outline[^"]*"', content), (
        "Launcher should use DaisyUI btn-outline variant"
    )


def test_launcher_uses_tailwind_hover_utilities():
    """
    Verify that the launcher uses Tailwind hover utilities.
    
    Validates: Requirements 4.3
    """
    content = get_launcher_content()
    
    # Check for Tailwind hover classes
    hover_patterns = [
        r'hover:',
        r'group-hover:'
    ]
    
    for pattern in hover_patterns:
        assert pattern in content, (
            f"Launcher should use Tailwind hover utilities: {pattern}"
        )


def test_launcher_uses_tailwind_responsive_utilities():
    """
    Verify that the launcher uses Tailwind responsive utilities.
    
    Validates: Requirements 4.5, 8.1, 8.2, 8.3
    """
    content = get_launcher_content()
    
    # Check for Tailwind responsive breakpoint classes
    responsive_patterns = [
        r'md:',
        r'flex-col',
        r'md:flex-row'
    ]
    
    for pattern in responsive_patterns:
        assert pattern in content, (
            f"Launcher should use Tailwind responsive utilities: {pattern}"
        )


def test_launcher_touch_targets_meet_minimum_size():
    """
    Verify that interactive elements have minimum touch target sizes.
    
    Validates: Requirements 8.2
    """
    content = get_launcher_content()
    
    # Check for minimum height/width classes on buttons
    assert re.search(r'min-h-\[44px\]', content), (
        "Buttons should have minimum height of 44px"
    )
    
    assert re.search(r'min-w-\[44px\]', content), (
        "Buttons should have minimum width of 44px"
    )


def test_launcher_uses_tailwind_transition_utilities():
    """
    Verify that the launcher uses Tailwind transition utilities.
    
    Validates: Requirements 9.2
    """
    content = get_launcher_content()
    
    # Check for Tailwind transition classes
    transition_patterns = [
        r'transition-all',
        r'duration-',
        r'ease-in-out'
    ]
    
    for pattern in transition_patterns:
        assert pattern in content, (
            f"Launcher should use Tailwind transition utilities: {pattern}"
        )


def test_launcher_uses_tailwind_spacing_utilities():
    """
    Verify that the launcher uses Tailwind spacing utilities instead of custom CSS.
    
    Validates: Requirements 6.1
    """
    content = get_launcher_content()
    
    # Check for Tailwind spacing classes (at least some of these should be present)
    spacing_patterns = [
        r'p-\d+',
        r'px-\d+',
        r'm-\d+',
        r'mb-\d+',
        r'mt-\d+'
    ]
    
    # At least 3 different spacing patterns should be used
    matches = sum(1 for pattern in spacing_patterns if re.search(pattern, content))
    assert matches >= 3, (
        f"Launcher should use at least 3 different Tailwind spacing utilities, found {matches}"
    )


def test_launcher_uses_tailwind_text_utilities():
    """
    Verify that the launcher uses Tailwind text utilities.
    
    Validates: Requirements 6.1
    """
    content = get_launcher_content()
    
    # Check for Tailwind text classes
    text_patterns = [
        r'text-\w+',
        r'text-\d+xl',
        r'font-',
        r'tracking-',
        r'uppercase'
    ]
    
    for pattern in text_patterns:
        assert re.search(pattern, content), (
            f"Launcher should use Tailwind text utilities: {pattern}"
        )


def test_launcher_uses_tailwind_color_utilities():
    """
    Verify that the launcher uses Tailwind color utilities with custom colors.
    
    Validates: Requirements 2.1, 3.1
    """
    content = get_launcher_content()
    
    # Check for custom color usage
    custom_colors = [
        'legal-navy',
        'legal-gold',
        'ghost-dark'
    ]
    
    for color in custom_colors:
        # Check if color is used in classes (bg-, text-, border-, etc.)
        assert color in content, (
            f"Launcher should use custom color: {color}"
        )


def test_launcher_minimal_custom_css():
    """
    Verify that custom CSS is minimal and only contains unique effects.
    
    Validates: Requirements 6.1, 6.2, 6.3, 6.4, 6.5
    """
    content = get_launcher_content()
    
    # Extract the style section
    style_start = content.find('<style>')
    style_end = content.find('</style>')
    
    if style_start != -1 and style_end != -1:
        style_section = content[style_start:style_end]
        
        # Custom CSS should only contain unique effects
        allowed_custom_patterns = [
            'legal-grid-bg',
            'ghost-fog-bg',
            'ghost-glow-overlay',
            '@keyframes',
            'scrollGrid',
            'float',
            'pulseGlow'
        ]
        
        # Verify that custom CSS only contains allowed patterns
        for pattern in allowed_custom_patterns:
            if pattern in ['@keyframes', 'scrollGrid', 'float', 'pulseGlow']:
                # These are animation-related and should be present
                assert pattern in style_section, (
                    f"Custom CSS should contain animation: {pattern}"
                )
        
        # Verify that layout utilities are NOT in custom CSS
        disallowed_patterns = [
            '.container {',
            'display: flex;',
            'width: 50%;',
            'position: relative;'
        ]
        
        # These patterns should be replaced by Tailwind utilities
        for pattern in disallowed_patterns:
            assert pattern not in style_section, (
                f"Custom CSS should not contain layout utilities: {pattern}"
            )


def test_launcher_uses_group_hover_pattern():
    """
    Verify that the launcher uses Tailwind's group hover pattern.
    
    Validates: Requirements 4.3
    """
    content = get_launcher_content()
    
    # Check for group class
    assert re.search(r'class="[^"]*group[^"]*"', content), (
        "Launcher should use Tailwind group class for hover effects"
    )
    
    # Check for group-hover usage
    assert 'group-hover:' in content, (
        "Launcher should use group-hover: prefix for child hover effects"
    )


def test_launcher_preserves_custom_animations():
    """
    Verify that custom animations that can't be replicated with Tailwind are preserved.
    
    Validates: Requirements 10.1
    """
    content = get_launcher_content()
    
    # Check for custom animations in style section
    custom_animations = [
        'scrollGrid',
        'float',
        'pulseGlow'
    ]
    
    for animation in custom_animations:
        assert animation in content, (
            f"Custom animation should be preserved: {animation}"
        )


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
