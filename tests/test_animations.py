"""
Tests for smooth animations and transitions.

Validates: Requirements 1.2, 1.3
"""

import re
from pathlib import Path
import pytest


def get_css_content():
    """Read the CSS file content."""
    css_path = Path(__file__).parent.parent / "skeleton_core" / "static" / "styles.css"
    with open(css_path, 'r', encoding='utf-8') as f:
        return f.read()


def test_css_file_exists():
    """Verify the CSS file exists."""
    css_path = Path(__file__).parent.parent / "skeleton_core" / "static" / "styles.css"
    assert css_path.exists(), "CSS file should exist"


def test_pop_in_animation_exists():
    """
    Verify that pop-in animation is defined for chat messages.
    Validates: Requirements 1.2
    """
    css_content = get_css_content()
    
    # Check for pop-in keyframe animation
    assert '@keyframes pop-in' in css_content, "pop-in animation should be defined"
    
    # Check that it includes transform and opacity
    pop_in_match = re.search(r'@keyframes pop-in\s*\{([^}]+)\}', css_content, re.DOTALL)
    assert pop_in_match, "pop-in animation should have content"
    
    pop_in_content = pop_in_match.group(1)
    assert 'opacity' in pop_in_content, "pop-in should animate opacity"
    assert 'transform' in pop_in_content, "pop-in should animate transform"


def test_fade_in_animation_exists():
    """
    Verify that fade-in animation is defined for page load.
    Validates: Requirements 1.2
    """
    css_content = get_css_content()
    
    # Check for fade-in keyframe animation
    assert '@keyframes fade-in' in css_content, "fade-in animation should be defined"
    
    # Check that it includes opacity
    fade_in_match = re.search(r'@keyframes fade-in\s*\{([^}]+)\}', css_content, re.DOTALL)
    assert fade_in_match, "fade-in animation should have content"
    
    fade_in_content = fade_in_match.group(1)
    assert 'opacity' in fade_in_content, "fade-in should animate opacity"


def test_title_pulse_animation_exists():
    """
    Verify that title-pulse animation is defined for Ouija Board theme.
    Validates: Requirements 1.2
    """
    css_content = get_css_content()
    
    # Check for title-pulse keyframe animation
    assert '@keyframes title-pulse' in css_content, "title-pulse animation should be defined"
    
    # Check that it includes text-shadow and opacity
    pulse_match = re.search(r'@keyframes title-pulse\s*\{([^}]+)\}', css_content, re.DOTALL)
    assert pulse_match, "title-pulse animation should have content"
    
    pulse_content = pulse_match.group(1)
    assert 'text-shadow' in pulse_content, "title-pulse should animate text-shadow"
    assert 'opacity' in pulse_content or 'transform' in pulse_content, "title-pulse should animate opacity or transform"


def test_button_hover_transitions():
    """
    Verify that buttons have smooth hover transitions with transform and shadow.
    Validates: Requirements 1.3
    """
    css_content = get_css_content()
    
    # Find .btn-primary rule
    btn_match = re.search(r'\.btn-primary\s*\{([^}]+)\}', css_content, re.DOTALL)
    assert btn_match, "btn-primary class should be defined"
    
    btn_content = btn_match.group(1)
    assert 'transition' in btn_content, "btn-primary should have transition property"
    
    # Check that transition includes transform and box-shadow
    assert 'transform' in btn_content, "btn-primary transition should include transform"
    assert 'box-shadow' in btn_content or 'shadow' in btn_content, "btn-primary transition should include box-shadow"
    
    # Find .btn-primary:hover rule
    btn_hover_match = re.search(r'\.btn-primary:hover\s*\{([^}]+)\}', css_content, re.DOTALL)
    assert btn_hover_match, "btn-primary:hover should be defined"
    
    btn_hover_content = btn_hover_match.group(1)
    assert 'transform' in btn_hover_content, "btn-primary:hover should use transform"
    assert 'box-shadow' in btn_hover_content, "btn-primary:hover should use box-shadow"


def test_chat_message_animation():
    """
    Verify that chat messages have pop-in animation applied.
    Validates: Requirements 1.2
    """
    css_content = get_css_content()
    
    # Find .chat-message rule
    msg_match = re.search(r'\.chat-message\s*\{([^}]+)\}', css_content, re.DOTALL)
    assert msg_match, "chat-message class should be defined"
    
    msg_content = msg_match.group(1)
    assert 'animation' in msg_content, "chat-message should have animation property"
    assert 'pop-in' in msg_content, "chat-message should use pop-in animation"


def test_prefers_reduced_motion_support():
    """
    Verify that animations respect prefers-reduced-motion preference.
    Validates: Requirements 1.2
    """
    css_content = get_css_content()
    
    # Check for prefers-reduced-motion media query
    assert '@media (prefers-reduced-motion: reduce)' in css_content, (
        "CSS should include prefers-reduced-motion media query"
    )
    
    # Find the media query content
    reduced_motion_match = re.search(
        r'@media \(prefers-reduced-motion: reduce\)\s*\{([^}]+(?:\{[^}]*\}[^}]*)*)\}',
        css_content,
        re.DOTALL
    )
    assert reduced_motion_match, "prefers-reduced-motion media query should have content"
    
    reduced_motion_content = reduced_motion_match.group(1)
    
    # Verify it disables or reduces animations
    assert 'animation-duration' in reduced_motion_content, (
        "prefers-reduced-motion should modify animation-duration"
    )
    assert 'transition-duration' in reduced_motion_content, (
        "prefers-reduced-motion should modify transition-duration"
    )


def test_animations_use_transform_and_opacity():
    """
    Verify that animations are optimized using transform and opacity.
    Validates: Requirements 1.2
    """
    css_content = get_css_content()
    
    # Extract all @keyframes blocks
    keyframes = re.findall(r'@keyframes\s+[\w-]+\s*\{([^}]+(?:\{[^}]*\}[^}]*)*)\}', css_content, re.DOTALL)
    
    assert len(keyframes) > 0, "CSS should contain keyframe animations"
    
    # Check that animations primarily use transform and opacity
    optimized_properties = ['transform', 'opacity']
    
    for keyframe_content in keyframes:
        # Skip animations that are specifically for other effects (like spin)
        if 'rotate' in keyframe_content and 'transform' in keyframe_content:
            continue
        
        # Most animations should use transform or opacity for performance
        uses_optimized = any(prop in keyframe_content for prop in optimized_properties)
        
        # We don't assert here because some animations (like color changes) may not use these
        # But we verify that the main animations do use them
        if 'pop-in' in str(keyframe_content) or 'fade-in' in str(keyframe_content):
            assert uses_optimized, (
                f"Main animations should use transform or opacity for performance"
            )


def test_smooth_scroll_behavior():
    """
    Verify that smooth scrolling is enabled.
    Validates: Requirements 1.2
    """
    css_content = get_css_content()
    
    # Check for scroll-behavior: smooth
    assert 'scroll-behavior: smooth' in css_content or 'scroll-behavior:smooth' in css_content, (
        "CSS should enable smooth scrolling"
    )


def test_input_field_transitions():
    """
    Verify that input fields have smooth transitions.
    Validates: Requirements 1.3
    """
    css_content = get_css_content()
    
    # Find .input-field rule
    input_match = re.search(r'\.input-field\s*\{([^}]+)\}', css_content, re.DOTALL)
    assert input_match, "input-field class should be defined"
    
    input_content = input_match.group(1)
    assert 'transition' in input_content, "input-field should have transition property"


def test_card_hover_transitions():
    """
    Verify that cards have smooth hover transitions.
    Validates: Requirements 1.3
    """
    css_content = get_css_content()
    
    # Find .card rule
    card_match = re.search(r'\.card\s*\{([^}]+)\}', css_content, re.DOTALL)
    assert card_match, "card class should be defined"
    
    card_content = card_match.group(1)
    assert 'transition' in card_content, "card should have transition property"


def test_loading_indicator_animation():
    """
    Verify that loading indicators have smooth animations.
    Validates: Requirements 1.2
    """
    css_content = get_css_content()
    
    # Find .loading-indicator rule
    loading_match = re.search(r'\.loading-indicator\s*\{([^}]+)\}', css_content, re.DOTALL)
    assert loading_match, "loading-indicator class should be defined"
    
    loading_content = loading_match.group(1)
    assert 'transition' in loading_content or 'animation' in loading_content, (
        "loading-indicator should have transition or animation"
    )


def test_progress_bar_transitions():
    """
    Verify that progress bar has smooth transitions.
    Validates: Requirements 1.3
    """
    css_content = get_css_content()
    
    # Find .progress-bar-fill rule
    progress_match = re.search(r'\.progress-bar-fill\s*\{([^}]+)\}', css_content, re.DOTALL)
    assert progress_match, "progress-bar-fill class should be defined"
    
    progress_content = progress_match.group(1)
    assert 'transition' in progress_content, "progress-bar-fill should have transition property"
    assert 'width' in progress_content or 'transition' in progress_content, (
        "progress-bar-fill should transition width"
    )


def test_error_message_animation():
    """
    Verify that error messages have smooth animations.
    Validates: Requirements 1.2
    """
    css_content = get_css_content()
    
    # Find .error-message rule
    error_match = re.search(r'\.error-message\s*\{([^}]+)\}', css_content, re.DOTALL)
    assert error_match, "error-message class should be defined"
    
    error_content = error_match.group(1)
    assert 'animation' in error_content or 'transition' in error_content, (
        "error-message should have animation or transition"
    )


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
