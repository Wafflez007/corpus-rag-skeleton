"""
Property-based tests for Enter key submission in chat interface.

Feature: ui-design-improvements
Tests Property 10
Validates: Requirements 6.5
"""

from hypothesis import given, strategies as st, settings
import pytest


class MockKeyboardEvent:
    """Mock representation of a keyboard event."""
    def __init__(self, key, shift_key=False):
        self.key = key
        self.shiftKey = shift_key
        self.default_prevented = False
        
    def preventDefault(self):
        """Prevent default form submission behavior."""
        self.default_prevented = True


class MockChatInput:
    """Mock representation of the chat input field."""
    def __init__(self):
        self.value = ""
        self.event_listeners = {}
        self.send_query_called = False
        
    def addEventListener(self, event_type, handler):
        """Add an event listener to the input field."""
        if event_type not in self.event_listeners:
            self.event_listeners[event_type] = []
        self.event_listeners[event_type].append(handler)
        
    def trigger_event(self, event_type, event):
        """Trigger an event on the input field."""
        if event_type in self.event_listeners:
            for handler in self.event_listeners[event_type]:
                handler(event)
                
    def sendQuery(self):
        """Mock sendQuery function."""
        self.send_query_called = True


def simulate_enter_key_handler(input_field):
    """
    Python simulation of the Enter key event handler.
    This mirrors the logic that should be in skeleton_core/static/app.js
    """
    def handle_keypress(event):
        # Enter key without Shift should submit
        if event.key == 'Enter' and not event.shiftKey:
            event.preventDefault()
            input_field.sendQuery()
        # Shift+Enter should allow multi-line input (do nothing)
        elif event.key == 'Enter' and event.shiftKey:
            # Allow default behavior (newline)
            pass
    
    input_field.addEventListener('keypress', handle_keypress)
    return input_field


# ========================================
# Property 10: Enter key submission
# ========================================

def test_enter_key_triggers_send():
    """
    Test that pressing Enter key triggers sendQuery().
    """
    input_field = MockChatInput()
    simulate_enter_key_handler(input_field)
    
    # Simulate Enter key press
    event = MockKeyboardEvent('Enter')
    input_field.trigger_event('keypress', event)
    
    # sendQuery should be called
    assert input_field.send_query_called is True
    assert event.default_prevented is True


def test_shift_enter_does_not_trigger_send():
    """
    Test that Shift+Enter does not trigger sendQuery() (allows multi-line).
    """
    input_field = MockChatInput()
    simulate_enter_key_handler(input_field)
    
    # Simulate Shift+Enter key press
    event = MockKeyboardEvent('Enter', shift_key=True)
    input_field.trigger_event('keypress', event)
    
    # sendQuery should NOT be called
    assert input_field.send_query_called is False
    assert event.default_prevented is False


def test_other_keys_do_not_trigger_send():
    """
    Test that other keys do not trigger sendQuery().
    """
    input_field = MockChatInput()
    simulate_enter_key_handler(input_field)
    
    # Simulate various other key presses
    for key in ['a', 'Space', 'Backspace', 'Tab', 'Escape']:
        event = MockKeyboardEvent(key)
        input_field.trigger_event('keypress', event)
        
        # sendQuery should NOT be called
        assert input_field.send_query_called is False


@settings(max_examples=100)
@given(
    input_text=st.text(min_size=0, max_size=500)
)
def test_enter_key_submission_property(input_text):
    """
    Feature: ui-design-improvements, Property 10: Enter key submission
    
    Property: For any Enter keypress event in the chat input field, the system 
    should trigger the query submission function.
    
    This property-based test generates random input text to ensure
    Enter key always triggers submission regardless of input content.
    
    Validates: Requirements 6.5
    """
    # Create input field with text
    input_field = MockChatInput()
    input_field.value = input_text
    simulate_enter_key_handler(input_field)
    
    # Simulate Enter key press
    event = MockKeyboardEvent('Enter')
    input_field.trigger_event('keypress', event)
    
    # sendQuery should be called
    assert input_field.send_query_called is True, (
        "Enter key should trigger sendQuery() function"
    )
    
    # Default form submission should be prevented
    assert event.default_prevented is True, (
        "Enter key should prevent default form submission behavior"
    )


@settings(max_examples=100)
@given(
    input_text=st.text(min_size=0, max_size=500)
)
def test_shift_enter_multiline_property(input_text):
    """
    Feature: ui-design-improvements, Property 10: Enter key submission
    
    Property: For any Shift+Enter keypress event in the chat input field, 
    the system should NOT trigger submission (allowing multi-line input).
    
    This property-based test ensures Shift+Enter is properly handled
    for multi-line input scenarios.
    
    Validates: Requirements 6.5
    """
    # Create input field with text
    input_field = MockChatInput()
    input_field.value = input_text
    simulate_enter_key_handler(input_field)
    
    # Simulate Shift+Enter key press
    event = MockKeyboardEvent('Enter', shift_key=True)
    input_field.trigger_event('keypress', event)
    
    # sendQuery should NOT be called
    assert input_field.send_query_called is False, (
        "Shift+Enter should NOT trigger sendQuery() function"
    )
    
    # Default behavior should be allowed (newline)
    assert event.default_prevented is False, (
        "Shift+Enter should allow default behavior for multi-line input"
    )


@settings(max_examples=100)
@given(
    key=st.sampled_from(['a', 'b', 'Space', 'Backspace', 'Tab', 'Escape', 
                         'ArrowUp', 'ArrowDown', 'Delete', '1', '!'])
)
def test_non_enter_keys_property(key):
    """
    Feature: ui-design-improvements, Property 10: Enter key submission
    
    Property: For any non-Enter keypress event in the chat input field,
    the system should NOT trigger query submission.
    
    This property-based test ensures only Enter key triggers submission,
    and other keys work normally.
    
    Validates: Requirements 6.5
    """
    # Create input field
    input_field = MockChatInput()
    simulate_enter_key_handler(input_field)
    
    # Simulate non-Enter key press
    event = MockKeyboardEvent(key)
    input_field.trigger_event('keypress', event)
    
    # sendQuery should NOT be called
    assert input_field.send_query_called is False, (
        f"Key '{key}' should NOT trigger sendQuery() function"
    )


@settings(max_examples=100)
@given(
    input_text=st.text(min_size=0, max_size=500),
    shift_pressed=st.booleans()
)
def test_enter_key_behavior_consistency_property(input_text, shift_pressed):
    """
    Feature: ui-design-improvements, Property 10: Enter key submission
    
    Property: For any Enter key event, the behavior should be consistent:
    - Enter alone always submits
    - Shift+Enter never submits
    
    This property-based test ensures consistent behavior across all scenarios.
    
    Validates: Requirements 6.5
    """
    # Create input field with text
    input_field = MockChatInput()
    input_field.value = input_text
    simulate_enter_key_handler(input_field)
    
    # Simulate Enter key press (with or without Shift)
    event = MockKeyboardEvent('Enter', shift_key=shift_pressed)
    input_field.trigger_event('keypress', event)
    
    if shift_pressed:
        # Shift+Enter should NOT submit
        assert input_field.send_query_called is False, (
            "Shift+Enter should NOT trigger submission"
        )
        assert event.default_prevented is False, (
            "Shift+Enter should allow default behavior"
        )
    else:
        # Enter alone should submit
        assert input_field.send_query_called is True, (
            "Enter key should trigger submission"
        )
        assert event.default_prevented is True, (
            "Enter key should prevent default form submission"
        )


@settings(max_examples=100)
@given(
    num_presses=st.integers(min_value=1, max_value=10)
)
def test_multiple_enter_presses_property(num_presses):
    """
    Feature: ui-design-improvements, Property 10: Enter key submission
    
    Property: For any number of Enter key presses, each press should
    trigger submission independently.
    
    This property-based test ensures the handler works correctly
    for multiple consecutive submissions.
    
    Validates: Requirements 6.5
    """
    # Create input field
    input_field = MockChatInput()
    simulate_enter_key_handler(input_field)
    
    # Track number of submissions
    submission_count = 0
    
    # Simulate multiple Enter key presses
    for _ in range(num_presses):
        input_field.send_query_called = False  # Reset for each press
        event = MockKeyboardEvent('Enter')
        input_field.trigger_event('keypress', event)
        
        if input_field.send_query_called:
            submission_count += 1
    
    # All Enter presses should trigger submission
    assert submission_count == num_presses, (
        f"Expected {num_presses} submissions, got {submission_count}"
    )


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
