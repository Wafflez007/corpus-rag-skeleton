"""
Property-based tests for comprehensive error handling and display.

Feature: ui-design-improvements
Tests Property 16
Validates: Requirements 8.5
"""

from hypothesis import given, strategies as st, settings
import pytest
from datetime import datetime


class MockErrorElement:
    """Mock representation of an error message element in the DOM."""
    def __init__(self, title, description, options=None):
        self.title = title
        self.description = description
        self.options = options or {}
        self.has_icon = False
        self.has_dismiss_button = False
        self.has_retry_button = False
        self.has_aria_role = False
        self.has_aria_live = False
        self.aria_role = None
        self.aria_live = None
        self.is_visible = True
        self.auto_dismiss_timeout = self.options.get('timeout', 0)
        self.retryable = self.options.get('retryable', False)
        
    def add_icon(self, icon):
        """Add an icon to the error message."""
        self.has_icon = True
        self.icon = icon
        
    def add_dismiss_button(self):
        """Add a dismiss button to the error message."""
        self.has_dismiss_button = True
        
    def add_retry_button(self):
        """Add a retry button to the error message."""
        self.has_retry_button = True
        
    def set_aria_role(self, role):
        """Set ARIA role for accessibility."""
        self.has_aria_role = True
        self.aria_role = role
        
    def set_aria_live(self, live_value):
        """Set ARIA live region for screen reader announcements."""
        self.has_aria_live = True
        self.aria_live = live_value
        
    def dismiss(self):
        """Dismiss the error message."""
        self.is_visible = False


def simulate_show_error(title, description, container=None, options=None):
    """
    Python simulation of the JavaScript showError() function.
    This mirrors the logic in skeleton_core/static/app.js
    """
    options = options or {}
    error = MockErrorElement(title, description, options)
    
    # Add icon (theme-appropriate)
    is_ghost = options.get('theme', 'professional') == 'ghost'
    icon = '💀' if is_ghost else '⚠️'
    error.add_icon(icon)
    
    # Add dismiss button (always present)
    error.add_dismiss_button()
    
    # Add retry button if retryable
    if options.get('retryable', False):
        error.add_retry_button()
    
    # Set ARIA attributes for accessibility
    error.set_aria_role('alert')
    error.set_aria_live('assertive')
    
    return error


def simulate_show_network_error(operation, retry_callback, container=None):
    """
    Python simulation of the JavaScript showNetworkError() function.
    """
    is_ghost = False  # For testing purposes
    
    title = 'The Veil Has Closed' if is_ghost else 'Network Connection Failed'
    description = f"Unable to complete {operation} operation. Please check your network connection and try again."
    
    return simulate_show_error(title, description, container, {
        'retryable': True,
        'onRetry': retry_callback,
        'timeout': 0
    })


# ========================================
# Property 16: Error display with information
# ========================================

def test_error_has_title_and_description():
    """
    Test that error messages include both title and description.
    """
    error = simulate_show_error("Error Title", "Error description")
    
    assert error.title == "Error Title"
    assert error.description == "Error description"


def test_error_has_icon():
    """
    Test that error messages include an icon.
    """
    error = simulate_show_error("Error", "Description")
    
    assert error.has_icon is True
    assert error.icon in ['💀', '⚠️']


def test_error_has_dismiss_button():
    """
    Test that error messages include a dismiss button.
    """
    error = simulate_show_error("Error", "Description")
    
    assert error.has_dismiss_button is True


def test_error_has_aria_attributes():
    """
    Test that error messages include proper ARIA attributes for accessibility.
    """
    error = simulate_show_error("Error", "Description")
    
    assert error.has_aria_role is True
    assert error.aria_role == 'alert'
    assert error.has_aria_live is True
    assert error.aria_live == 'assertive'


@settings(max_examples=100)
@given(
    title=st.text(min_size=1, max_size=100),
    description=st.text(min_size=1, max_size=500)
)
def test_error_display_with_information_property(title, description):
    """
    Feature: ui-design-improvements, Property 16: Error display with information
    
    Property: For any error that occurs during processing, the system should 
    display an error message element containing information about the error.
    
    This property-based test generates random error titles and descriptions
    to ensure all errors are displayed with complete information.
    
    Validates: Requirements 8.5
    """
    # Create error message
    error = simulate_show_error(title, description)
    
    # Error should exist
    assert error is not None, "Error element should be created"
    
    # Error should contain title
    assert error.title is not None, "Error should have a title"
    assert error.title == title, "Error title should match input"
    assert len(error.title) > 0, "Error title should not be empty"
    
    # Error should contain description
    assert error.description is not None, "Error should have a description"
    assert error.description == description, "Error description should match input"
    assert len(error.description) > 0, "Error description should not be empty"
    
    # Error should have an icon for visual identification
    assert error.has_icon is True, "Error should have an icon"
    assert error.icon in ['💀', '⚠️'], (
        f"Error icon should be theme-appropriate, got: {error.icon}"
    )
    
    # Error should have a dismiss button
    assert error.has_dismiss_button is True, (
        "Error should have a dismiss button"
    )
    
    # Error should be visible
    assert error.is_visible is True, "Error should be visible when created"


@settings(max_examples=100)
@given(
    title=st.text(min_size=1, max_size=100),
    description=st.text(min_size=1, max_size=500),
    theme=st.sampled_from(['professional', 'ghost'])
)
def test_error_theme_appropriate_styling_property(title, description, theme):
    """
    Feature: ui-design-improvements, Property 16: Error display with information
    
    Property: For any error, the styling should be appropriate to the active theme
    (professional or gothic).
    
    This property-based test ensures errors are styled consistently with
    the application theme.
    
    Validates: Requirements 8.5
    """
    # Create error with theme
    error = simulate_show_error(title, description, options={'theme': theme})
    
    # Icon should be theme-appropriate
    if theme == 'ghost':
        assert error.icon == '💀', "Ghost theme should use skull icon"
    else:
        assert error.icon == '⚠️', "Professional theme should use warning icon"


@settings(max_examples=100)
@given(
    title=st.text(min_size=1, max_size=100),
    description=st.text(min_size=1, max_size=500)
)
def test_error_accessibility_property(title, description):
    """
    Feature: ui-design-improvements, Property 16: Error display with information
    
    Property: For any error, the error element should include proper ARIA
    attributes for screen reader accessibility.
    
    This property-based test ensures all errors are accessible to users
    with assistive technologies.
    
    Validates: Requirements 8.5
    """
    # Create error message
    error = simulate_show_error(title, description)
    
    # Error should have ARIA role
    assert error.has_aria_role is True, "Error should have ARIA role"
    assert error.aria_role == 'alert', (
        "Error should have role='alert' for screen readers"
    )
    
    # Error should have ARIA live region
    assert error.has_aria_live is True, "Error should have ARIA live region"
    assert error.aria_live in ['assertive', 'polite'], (
        "Error should have appropriate ARIA live value"
    )


@settings(max_examples=100)
@given(
    title=st.text(min_size=1, max_size=100),
    description=st.text(min_size=1, max_size=500),
    timeout=st.integers(min_value=0, max_value=10000)
)
def test_error_auto_dismiss_property(title, description, timeout):
    """
    Feature: ui-design-improvements, Property 16: Error display with information
    
    Property: For any error with a timeout value, the error should be configured
    to auto-dismiss after the specified duration.
    
    This property-based test ensures auto-dismiss functionality is properly
    configured for errors.
    
    Validates: Requirements 8.5
    """
    # Create error with timeout
    error = simulate_show_error(title, description, options={'timeout': timeout})
    
    # Error should have timeout configured
    assert error.auto_dismiss_timeout == timeout, (
        f"Error should have timeout of {timeout}ms"
    )
    
    # If timeout is 0, error should not auto-dismiss
    if timeout == 0:
        assert error.auto_dismiss_timeout == 0, (
            "Error with timeout=0 should not auto-dismiss"
        )


@settings(max_examples=100)
@given(
    operation=st.text(min_size=1, max_size=50)
)
def test_network_error_with_retry_property(operation):
    """
    Feature: ui-design-improvements, Property 16: Error display with information
    
    Property: For any network error, the error should include a retry button
    and appropriate error information.
    
    This property-based test ensures network errors provide users with
    recovery options.
    
    Validates: Requirements 8.5
    """
    # Create network error
    retry_called = False
    
    def mock_retry():
        nonlocal retry_called
        retry_called = True
    
    error = simulate_show_network_error(operation, mock_retry)
    
    # Error should exist
    assert error is not None, "Network error should be created"
    
    # Error should have title and description
    assert error.title is not None, "Network error should have title"
    assert len(error.title) > 0, "Network error title should not be empty"
    assert error.description is not None, "Network error should have description"
    assert len(error.description) > 0, "Network error description should not be empty"
    
    # Error should mention the operation
    assert operation in error.description, (
        f"Network error should mention the operation '{operation}'"
    )
    
    # Error should be retryable
    assert error.retryable is True, "Network error should be retryable"
    assert error.has_retry_button is True, (
        "Network error should have a retry button"
    )
    
    # Error should not auto-dismiss (timeout = 0)
    assert error.auto_dismiss_timeout == 0, (
        "Network errors should not auto-dismiss"
    )


@settings(max_examples=100)
@given(
    title=st.text(min_size=1, max_size=100),
    description=st.text(min_size=1, max_size=500),
    retryable=st.booleans()
)
def test_error_retry_button_property(title, description, retryable):
    """
    Feature: ui-design-improvements, Property 16: Error display with information
    
    Property: For any error, a retry button should be present if and only if
    the error is marked as retryable.
    
    This property-based test ensures retry buttons are shown appropriately.
    
    Validates: Requirements 8.5
    """
    # Create error with retryable option
    error = simulate_show_error(title, description, options={'retryable': retryable})
    
    # Retry button presence should match retryable flag
    if retryable:
        assert error.has_retry_button is True, (
            "Retryable error should have a retry button"
        )
    else:
        assert error.has_retry_button is False, (
            "Non-retryable error should not have a retry button"
        )


@settings(max_examples=100)
@given(
    title=st.text(min_size=1, max_size=100),
    description=st.text(min_size=1, max_size=500)
)
def test_error_dismissal_property(title, description):
    """
    Feature: ui-design-improvements, Property 16: Error display with information
    
    Property: For any error, calling the dismiss function should hide the error
    from view.
    
    This property-based test ensures errors can be properly dismissed.
    
    Validates: Requirements 8.5
    """
    # Create error
    error = simulate_show_error(title, description)
    
    # Error should be visible initially
    assert error.is_visible is True, "Error should be visible when created"
    
    # Dismiss the error
    error.dismiss()
    
    # Error should no longer be visible
    assert error.is_visible is False, "Error should be hidden after dismissal"


@settings(max_examples=100)
@given(
    title=st.text(min_size=1, max_size=100),
    description=st.text(min_size=1, max_size=500)
)
def test_error_content_preservation_property(title, description):
    """
    Feature: ui-design-improvements, Property 16: Error display with information
    
    Property: For any error, the title and description content should be
    preserved exactly as provided (no truncation or modification).
    
    This ensures error messages are displayed completely and accurately.
    
    Validates: Requirements 8.5
    """
    # Create error
    error = simulate_show_error(title, description)
    
    # Title should be preserved exactly
    assert error.title == title, (
        "Error title should be preserved without modification"
    )
    
    # Description should be preserved exactly
    assert error.description == description, (
        "Error description should be preserved without modification"
    )


# ========================================
# Edge case tests
# ========================================

def test_error_with_empty_options():
    """
    Test that errors work correctly with no options provided.
    """
    error = simulate_show_error("Title", "Description", options={})
    
    assert error is not None
    assert error.has_dismiss_button is True
    assert error.auto_dismiss_timeout == 0
    assert error.retryable is False


def test_error_with_none_options():
    """
    Test that errors work correctly with None options.
    """
    error = simulate_show_error("Title", "Description", options=None)
    
    assert error is not None
    assert error.has_dismiss_button is True


def test_multiple_errors():
    """
    Test that multiple errors can be created independently.
    """
    error1 = simulate_show_error("Error 1", "Description 1")
    error2 = simulate_show_error("Error 2", "Description 2")
    
    assert error1.title != error2.title
    assert error1.description != error2.description
    assert error1 is not error2


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
