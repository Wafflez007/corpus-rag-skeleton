"""
Test that custom mystical effects for Ouija Board theme are preserved in CSS.

These effects cannot be replicated with Tailwind/DaisyUI and must remain in custom CSS.
"""

import pytest
from pathlib import Path


def read_css_file():
    """Read the custom CSS file."""
    css_path = Path("skeleton_core/static/styles.css")
    with open(css_path, 'r', encoding='utf-8') as f:
        return f.read()


def test_blood_drip_animation_exists():
    """Test that blood drip animation CSS is present."""
    css_content = read_css_file()
    
    # Check for blood drip container
    assert '.theme-dark-gothic .blood-drip-container' in css_content
    
    # Check for blood drip elements
    assert '.theme-dark-gothic .blood-drip-container .blood-drip' in css_content
    
    # Check for pseudo-elements
    assert '.theme-dark-gothic .blood-drip-container .blood-drip::before' in css_content
    assert '.theme-dark-gothic .blood-drip-container .blood-drip::after' in css_content
    
    # Check for animation
    assert '@keyframes blood-gooey-fall' in css_content
    assert 'animation: blood-gooey-fall' in css_content


def test_mystical_fog_effect_exists():
    """Test that mystical fog overlay CSS is present."""
    css_content = read_css_file()
    
    # Check for fog overlay using ::before pseudo-element
    assert '.theme-dark-gothic::before' in css_content
    
    # Check for radial gradients
    assert 'radial-gradient(circle at 20% 30%, rgba(139, 0, 0, 0.25)' in css_content
    
    # Check for mystical fog animation
    assert '@keyframes mystical-fog' in css_content


def test_floating_particles_effect_exists():
    """Test that floating particles effect CSS is present."""
    css_content = read_css_file()
    
    # Check for particles overlay using ::after pseudo-element
    assert '.theme-dark-gothic::after' in css_content
    
    # Check for floating particles animation
    assert '@keyframes floating-particles' in css_content
    assert 'animation: floating-particles' in css_content


def test_custom_planchette_cursor_exists():
    """Test that custom planchette cursor CSS is present."""
    css_content = read_css_file()
    
    # Check for cursor definitions
    assert 'cursor: url("data:image/svg+xml' in css_content
    
    # Check for planchette SVG path
    assert 'M16 2 L28 26 Q16 30 4 26 Z' in css_content
    
    # Check for different cursor states
    assert '.theme-dark-gothic button' in css_content or '.theme-dark-gothic a' in css_content


def test_title_pulse_animation_exists():
    """Test that title pulse animation CSS is present."""
    css_content = read_css_file()
    
    # Check for title pulse styling
    assert '.theme-dark-gothic h1' in css_content or '.theme-dark-gothic .spooky-title' in css_content
    
    # Check for title pulse animation
    assert '@keyframes title-pulse' in css_content
    assert 'animation: title-pulse' in css_content
    
    # Check for text-shadow
    assert 'text-shadow:' in css_content


def test_button_glow_animation_exists():
    """Test that button glow animation CSS is present."""
    css_content = read_css_file()
    
    # Check for button glow animation
    assert '@keyframes button-glow' in css_content
    assert 'animation: button-glow' in css_content


def test_mystical_effects_marked_with_warnings():
    """Test that custom mystical effects are marked with warning comments."""
    css_content = read_css_file()
    
    # Check for warning markers
    warning_marker = '⚠️ CUSTOM MYSTICAL EFFECT'
    
    # Count occurrences - should have multiple warnings
    warning_count = css_content.count(warning_marker)
    
    assert warning_count >= 5, f"Expected at least 5 mystical effect warnings, found {warning_count}"


def test_gooey_filter_reference_exists():
    """Test that SVG gooey filter reference is present in CSS."""
    css_content = read_css_file()
    
    # Check for filter reference
    assert "filter: url('#blood-goo')" in css_content
    assert "-webkit-filter: url('#blood-goo')" in css_content


def test_reduced_motion_support():
    """Test that mystical effects respect prefers-reduced-motion."""
    css_content = read_css_file()
    
    # Check for reduced motion media query
    assert '@media (prefers-reduced-motion: reduce)' in css_content
    
    # Check that blood drip animation is disabled for reduced motion
    assert 'animation: none !important' in css_content


def test_mystical_effects_use_theme_variables():
    """Test that mystical effects use CSS custom properties."""
    css_content = read_css_file()
    
    # Check that effects use theme variables
    assert 'var(--primary' in css_content
    assert 'var(--accent' in css_content
    assert 'var(--bg-card' in css_content


def test_blood_drip_staggered_timing():
    """Test that blood drips have staggered animation timing."""
    css_content = read_css_file()
    
    # Check for multiple nth-child selectors with different delays
    assert ':nth-child(1)' in css_content
    assert ':nth-child(2)' in css_content
    assert ':nth-child(3)' in css_content
    assert ':nth-child(4)' in css_content
    assert ':nth-child(5)' in css_content
    
    # Check for animation delays
    assert 'animation-delay:' in css_content


def test_mystical_card_styling_preserved():
    """Test that mystical card styling with glow effects is preserved."""
    css_content = read_css_file()
    
    # Check for card mystical styling
    assert '.theme-dark-gothic .card' in css_content
    
    # Check for multiple box-shadows (mystical glow)
    # Should have both outset and inset shadows
    card_section = css_content[css_content.find('.theme-dark-gothic .card'):]
    assert 'box-shadow:' in card_section[:500]
    assert 'inset' in card_section[:500]


def test_creepster_font_reference():
    """Test that Creepster font is referenced for gothic headings."""
    css_content = read_css_file()
    
    # Check for Creepster font
    assert 'Creepster' in css_content
    assert '--font-heading:' in css_content


def test_documentation_file_exists():
    """Test that mystical effects documentation file exists."""
    doc_path = Path(".kiro/specs/tailwind-daisyui-integration/MYSTICAL_EFFECTS_PRESERVED.md")
    assert doc_path.exists(), "Mystical effects documentation file should exist"
    
    # Read and verify content
    with open(doc_path, 'r', encoding='utf-8') as f:
        doc_content = f.read()
    
    # Check for key sections
    assert "Blood Drip Animations" in doc_content
    assert "Mystical Fog Effects" in doc_content
    assert "Floating Particles Effect" in doc_content
    assert "Custom Planchette Cursor" in doc_content
    assert "Title Pulse Animation" in doc_content
    assert "Button Glow Animation" in doc_content


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
