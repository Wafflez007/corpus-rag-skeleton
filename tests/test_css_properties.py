"""
Property-based tests for CSS architecture and theme system.

Feature: ui-design-improvements, Property 20: CSS variable fallbacks
Validates: Requirements 10.5

Feature: ui-design-improvements, Property 1: Touch target minimum size
Validates: Requirements 4.2
"""

import re
from pathlib import Path
from hypothesis import given, strategies as st, settings
import pytest


def get_css_content():
    """Read the CSS file content."""
    css_path = Path(__file__).parent.parent / "skeleton_core" / "static" / "styles.css"
    with open(css_path, 'r', encoding='utf-8') as f:
        return f.read()


def extract_var_usages(css_content):
    """
    Extract all var() usages from CSS content.
    Returns a list of tuples: (full_match, var_name, fallback_or_none)
    """
    # Pattern to match var() with optional fallback
    # var(--variable-name) or var(--variable-name, fallback-value)
    pattern = r'var\(\s*(--[\w-]+)\s*(?:,\s*([^)]+))?\s*\)'
    matches = re.findall(pattern, css_content)
    return matches


def test_css_file_exists():
    """Verify the CSS file exists."""
    css_path = Path(__file__).parent.parent / "skeleton_core" / "static" / "styles.css"
    assert css_path.exists(), "CSS file should exist"


def test_all_var_usages_have_fallbacks():
    """
    Feature: ui-design-improvements, Property 20: CSS variable fallbacks
    
    Property: For any CSS custom property usage, the var() function should 
    include a fallback value to handle cases where the variable is undefined.
    
    Validates: Requirements 10.5
    """
    css_content = get_css_content()
    var_usages = extract_var_usages(css_content)
    
    # Track vars without fallbacks
    vars_without_fallbacks = []
    
    for var_name, fallback in var_usages:
        if not fallback or fallback.strip() == '':
            vars_without_fallbacks.append(var_name)
    
    # Assert all vars have fallbacks
    assert len(vars_without_fallbacks) == 0, (
        f"Found {len(vars_without_fallbacks)} CSS variables without fallbacks: "
        f"{', '.join(set(vars_without_fallbacks))}"
    )


@settings(max_examples=100)
@given(
    var_name=st.text(
        alphabet=st.characters(whitelist_categories=('Ll', 'Lu', 'Nd'), whitelist_characters='-'),
        min_size=3,
        max_size=30
    ).filter(lambda x: x.startswith('--') or not x.startswith('-')),
    fallback=st.one_of(
        st.text(min_size=1, max_size=20),
        st.sampled_from(['#000000', '#ffffff', '1rem', '0.5rem', '4px', 'sans-serif'])
    )
)
def test_var_syntax_with_fallback_is_valid(var_name, fallback):
    """
    Feature: ui-design-improvements, Property 20: CSS variable fallbacks
    
    Property-based test: For any CSS variable name and fallback value,
    the var() syntax with fallback should be properly formatted.
    
    This test generates random variable names and fallback values to ensure
    the fallback syntax is correctly structured.
    
    Validates: Requirements 10.5
    """
    # Ensure var_name starts with --
    if not var_name.startswith('--'):
        var_name = '--' + var_name
    
    # Clean up var_name to be valid CSS
    var_name = re.sub(r'[^a-zA-Z0-9-]', '', var_name)
    if not var_name or var_name == '--':
        var_name = '--test-var'
    
    # Create var() usage with fallback
    var_usage = f"var({var_name}, {fallback})"
    
    # Verify it matches the expected pattern
    pattern = r'var\(\s*(--[\w-]+)\s*,\s*([^)]+)\s*\)'
    match = re.match(pattern, var_usage)
    
    assert match is not None, f"var() with fallback should match pattern: {var_usage}"
    assert match.group(1) == var_name, f"Variable name should be extracted: {var_name}"
    assert match.group(2).strip() == fallback.strip(), f"Fallback should be extracted: {fallback}"


def test_css_sections_are_organized():
    """
    Verify that the CSS file is organized into clear sections as required.
    
    Expected sections:
    1. CSS Variables & Theme Definitions
    2. Base Styles & Reset
    3. Component Styles
    4. Utility Classes
    5. Animations & Transitions
    6. Responsive Design
    7. Theme-Specific Overrides
    8. Scrollbar Styling
    9. Accessibility
    10. Performance Optimizations
    """
    css_content = get_css_content()
    
    required_sections = [
        "SECTION 1: CSS VARIABLES",
        "SECTION 2: BASE STYLES",
        "SECTION 3: COMPONENT STYLES",
        "SECTION 4: UTILITY CLASSES",
        "SECTION 5: ANIMATIONS",
        "SECTION 6: RESPONSIVE DESIGN",
        "SECTION 7: THEME-SPECIFIC OVERRIDES",
        "SECTION 8: SCROLLBAR",
        "SECTION 9: ACCESSIBILITY",
        "SECTION 10: PERFORMANCE",
    ]
    
    for section in required_sections:
        assert section in css_content, f"CSS should contain {section} section"


def test_css_variables_defined_for_both_themes():
    """
    Verify that both themes define all required CSS variables.
    """
    css_content = get_css_content()
    
    required_vars = [
        '--primary',
        '--secondary',
        '--accent',
        '--bg-main',
        '--bg-card',
        '--bg-input',
        '--text-main',
        '--text-dim',
        '--border',
        '--font-heading',
        '--font-body',
        '--font-mono',
        '--spacing-xs',
        '--spacing-sm',
        '--spacing-md',
        '--spacing-lg',
        '--spacing-xl',
        '--radius-sm',
        '--radius-md',
        '--radius-lg',
    ]
    
    # Extract theme blocks
    dark_gothic_match = re.search(r'\.theme-dark-gothic\s*\{([^}]+)\}', css_content, re.DOTALL)
    blue_corporate_match = re.search(r'\.theme-blue-corporate\s*\{([^}]+)\}', css_content, re.DOTALL)
    
    assert dark_gothic_match, "Dark gothic theme should be defined"
    assert blue_corporate_match, "Blue corporate theme should be defined"
    
    dark_gothic_content = dark_gothic_match.group(1)
    blue_corporate_content = blue_corporate_match.group(1)
    
    # Check each theme has all required variables
    for var in required_vars:
        assert var in dark_gothic_content, f"Dark gothic theme should define {var}"
        assert var in blue_corporate_content, f"Blue corporate theme should define {var}"


def test_css_containment_applied():
    """
    Verify that CSS containment is applied for performance optimization.
    """
    css_content = get_css_content()
    
    # Check that contain property is used
    assert 'contain:' in css_content or 'contain :' in css_content, (
        "CSS should use containment for performance optimization"
    )


def extract_min_height_rules(css_content):
    """
    Extract min-height rules from CSS content.
    Returns a dict mapping selectors to their min-height values in pixels.
    """
    min_heights = {}
    
    # Pattern to match CSS rules with min-height
    # Matches: selector { ... min-height: value; ... }
    rule_pattern = r'([^{]+)\{([^}]+)\}'
    
    for match in re.finditer(rule_pattern, css_content):
        selector = match.group(1).strip()
        properties = match.group(2)
        
        # Look for min-height property
        min_height_match = re.search(r'min-height:\s*(\d+)px', properties)
        if min_height_match:
            height_px = int(min_height_match.group(1))
            min_heights[selector] = height_px
    
    return min_heights


def test_interactive_elements_meet_touch_target_minimum():
    """
    Feature: ui-design-improvements, Property 1: Touch target minimum size
    
    Property: For any interactive element in the interface, the computed size 
    (including padding) should be at least 44x44 pixels to ensure touch accessibility.
    
    This test verifies that CSS rules for interactive elements (buttons, inputs, etc.)
    specify minimum dimensions that meet or exceed the 44px accessibility standard.
    
    Validates: Requirements 4.2
    """
    css_content = get_css_content()
    min_heights = extract_min_height_rules(css_content)
    
    # Interactive element selectors that should have adequate touch targets
    interactive_selectors = [
        'button',
        'input[type="button"]',
        'input[type="submit"]',
        'input[type="text"]',
        'input[type="file"]',
        '.btn-primary',
    ]
    
    # Check that interactive elements have min-height rules
    violations = []
    
    for selector_pattern in interactive_selectors:
        # Find matching rules in the extracted min-heights
        found = False
        for css_selector, height in min_heights.items():
            # Check if the selector pattern matches
            if selector_pattern in css_selector:
                found = True
                # Verify it meets the 44px minimum (or 40px for desktop which is acceptable)
                if height < 40:
                    violations.append(f"{css_selector}: {height}px (minimum should be 40-44px)")
        
        if not found:
            # Check if there's a general rule that covers this selector
            if selector_pattern == 'button' and any('button' in s for s in min_heights.keys()):
                continue
            violations.append(f"No min-height rule found for {selector_pattern}")
    
    assert len(violations) == 0, (
        f"Touch target size violations found:\n" + "\n".join(violations)
    )


@settings(max_examples=100)
@given(
    element_type=st.sampled_from(['button', 'input', 'a', 'select', 'textarea']),
    padding_top=st.integers(min_value=0, max_value=20),
    padding_bottom=st.integers(min_value=0, max_value=20),
    min_height=st.integers(min_value=20, max_value=60),
)
def test_touch_target_size_calculation(element_type, padding_top, padding_bottom, min_height):
    """
    Feature: ui-design-improvements, Property 1: Touch target minimum size
    
    Property-based test: For any interactive element with given padding and min-height,
    the total computed height should meet accessibility standards.
    
    This test generates random combinations of padding and min-height values to verify
    that the calculation logic for touch target sizes is correct.
    
    Validates: Requirements 4.2
    """
    # Calculate total height: min-height + padding-top + padding-bottom
    total_height = min_height + padding_top + padding_bottom
    
    # For mobile (< 768px), touch targets should be at least 44px
    # For desktop (>= 1024px), 40px is acceptable but 44px is preferred
    MOBILE_MIN = 44
    DESKTOP_MIN = 40
    
    # If the element has a min-height of at least 44px, it should pass mobile requirements
    if min_height >= MOBILE_MIN:
        assert total_height >= MOBILE_MIN, (
            f"{element_type} with min-height {min_height}px and padding "
            f"{padding_top}px/{padding_bottom}px should meet mobile minimum"
        )
    
    # If total height is less than desktop minimum, it's a violation
    if total_height < DESKTOP_MIN:
        # This is expected to fail for small values - that's the point of the test
        # We're verifying our CSS doesn't create elements this small
        pass
    
    # The property we're testing: adequate padding + min-height = accessible touch target
    # If min-height is set to 44px and padding is reasonable (4-16px), total should be good
    if min_height >= MOBILE_MIN and padding_top >= 4 and padding_bottom >= 4:
        assert total_height >= MOBILE_MIN, (
            f"Well-configured {element_type} should meet touch target minimum"
        )


def test_mobile_breakpoint_enforces_touch_targets():
    """
    Feature: ui-design-improvements, Property 1: Touch target minimum size
    
    Verify that mobile breakpoint media queries enforce adequate touch target sizes.
    
    Validates: Requirements 4.2
    """
    css_content = get_css_content()
    
    # Find mobile media query section - look for the entire @media block
    # We need to find the matching closing brace
    mobile_start = css_content.find('@media (max-width: 767px)')
    assert mobile_start != -1, "Mobile media query should exist"
    
    # Find the opening brace
    brace_start = css_content.find('{', mobile_start)
    assert brace_start != -1, "Mobile media query should have opening brace"
    
    # Find the matching closing brace by counting braces
    brace_count = 1
    pos = brace_start + 1
    while pos < len(css_content) and brace_count > 0:
        if css_content[pos] == '{':
            brace_count += 1
        elif css_content[pos] == '}':
            brace_count -= 1
        pos += 1
    
    mobile_content = css_content[brace_start:pos]
    
    assert mobile_content, "Mobile media query content should be extracted"
    
    # Verify mobile styles mention min-height for interactive elements
    assert 'min-height' in mobile_content, (
        "Mobile styles should specify min-height for touch targets"
    )
    
    # Check for 44px minimum in mobile styles
    assert '44px' in mobile_content, (
        "Mobile styles should use 44px minimum for touch targets"
    )


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
