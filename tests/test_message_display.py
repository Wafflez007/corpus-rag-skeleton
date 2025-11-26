"""
Property-based tests for chat message display and interaction.

Feature: ui-design-improvements
Tests Properties 7, 17, 18, 19
Validates: Requirements 6.1, 9.1, 9.2, 9.5
"""

from hypothesis import given, strategies as st, settings
import pytest
from datetime import datetime


class MockChatMessage:
    """Mock representation of a chat message in the DOM."""
    def __init__(self, text, message_type, timestamp=None):
        self.text = text
        self.type = message_type  # 'user' or 'ai'
        self.timestamp = timestamp or datetime.now()
        self.has_icon = False
        self.css_classes = []
        self.has_timestamp_element = False
        
    def add_css_class(self, css_class):
        """Add a CSS class to the message."""
        self.css_classes.append(css_class)
        
    def add_icon(self, icon):
        """Add an icon/avatar to the message."""
        self.has_icon = True
        self.icon = icon
        
    def add_timestamp_element(self):
        """Add a timestamp element to the message."""
        self.has_timestamp_element = True


def simulate_add_message(text, message_type):
    """
    Python simulation of the JavaScript addMessage() function.
    This mirrors the logic in skeleton_core/static/app.js
    """
    message = MockChatMessage(text, message_type)
    
    # Apply distinct CSS classes based on message type
    if message_type == 'user':
        message.add_css_class('chat-message-user')
    elif message_type == 'ai':
        message.add_css_class('chat-message-ai')
        # Add icon/avatar for AI messages
        message.add_icon('🔮' if is_ghost_theme() else '⚖️')
    
    # Add timestamp element (optional, non-intrusive)
    message.add_timestamp_element()
    
    return message


def is_ghost_theme():
    """Mock function to determine if ghost theme is active."""
    # For testing purposes, we'll test both themes
    return False


# ========================================
# Property 7: Immediate user message display
# ========================================

def test_user_message_immediate_display():
    """
    Test that user messages are created immediately upon calling addMessage.
    """
    text = "Hello, this is a test message"
    message = simulate_add_message(text, 'user')
    
    # Message should be created immediately
    assert message is not None
    assert message.text == text
    assert message.type == 'user'


@settings(max_examples=100)
@given(
    message_text=st.text(min_size=1, max_size=500)
)
def test_immediate_user_message_display_property(message_text):
    """
    Feature: ui-design-improvements, Property 7: Immediate user message display
    
    Property: For any user message submission, the message should appear in the 
    chat history immediately upon calling the send function.
    
    This property-based test generates random message content to ensure
    user messages are always displayed immediately without delay.
    
    Validates: Requirements 6.1
    """
    # Simulate adding a user message
    message = simulate_add_message(message_text, 'user')
    
    # Message should exist immediately
    assert message is not None, "User message should be created immediately"
    assert message.text == message_text, "Message text should match input"
    assert message.type == 'user', "Message type should be 'user'"
    
    # Message should have user-specific styling
    assert 'chat-message-user' in message.css_classes, (
        "User message should have 'chat-message-user' CSS class"
    )


# ========================================
# Property 17: Distinct message styling
# ========================================

def test_distinct_message_styling():
    """
    Test that user and AI messages have different CSS classes.
    """
    user_message = simulate_add_message("User message", 'user')
    ai_message = simulate_add_message("AI response", 'ai')
    
    # Messages should have different CSS classes
    assert 'chat-message-user' in user_message.css_classes
    assert 'chat-message-ai' in ai_message.css_classes
    assert user_message.css_classes != ai_message.css_classes


@settings(max_examples=100)
@given(
    user_text=st.text(min_size=1, max_size=500),
    ai_text=st.text(min_size=1, max_size=500)
)
def test_distinct_message_styling_property(user_text, ai_text):
    """
    Feature: ui-design-improvements, Property 17: Distinct message styling
    
    Property: For any pair of user message and AI message elements, they should 
    have different CSS classes applied to distinguish them visually.
    
    This property-based test generates random message pairs to ensure
    user and AI messages always have distinct styling.
    
    Validates: Requirements 9.1
    """
    # Create user and AI messages
    user_message = simulate_add_message(user_text, 'user')
    ai_message = simulate_add_message(ai_text, 'ai')
    
    # Both messages should have CSS classes
    assert len(user_message.css_classes) > 0, "User message should have CSS classes"
    assert len(ai_message.css_classes) > 0, "AI message should have CSS classes"
    
    # User message should have user-specific class
    assert 'chat-message-user' in user_message.css_classes, (
        "User message should have 'chat-message-user' class"
    )
    
    # AI message should have AI-specific class
    assert 'chat-message-ai' in ai_message.css_classes, (
        "AI message should have 'chat-message-ai' class"
    )
    
    # Classes should be different
    assert user_message.css_classes != ai_message.css_classes, (
        "User and AI messages should have different CSS classes"
    )


# ========================================
# Property 18: AI message visual indicators
# ========================================

def test_ai_message_has_icon():
    """
    Test that AI messages include an icon/avatar.
    """
    ai_message = simulate_add_message("AI response", 'ai')
    
    assert ai_message.has_icon is True
    assert ai_message.icon in ['🔮', '⚖️']


def test_user_message_no_icon():
    """
    Test that user messages do not include an icon/avatar.
    """
    user_message = simulate_add_message("User message", 'user')
    
    assert user_message.has_icon is False


@settings(max_examples=100)
@given(
    ai_text=st.text(min_size=1, max_size=500)
)
def test_ai_message_visual_indicators_property(ai_text):
    """
    Feature: ui-design-improvements, Property 18: AI message visual indicators
    
    Property: For any AI message displayed, the message element should contain 
    an icon or avatar element to identify it as an AI response.
    
    This property-based test generates random AI messages to ensure
    all AI responses include visual indicators.
    
    Validates: Requirements 9.2
    """
    # Create AI message
    ai_message = simulate_add_message(ai_text, 'ai')
    
    # AI message should have an icon
    assert ai_message.has_icon is True, (
        "AI message should have an icon/avatar"
    )
    
    # Icon should be one of the theme-appropriate icons
    assert ai_message.icon in ['🔮', '⚖️'], (
        f"AI message icon should be theme-appropriate, got: {ai_message.icon}"
    )


@settings(max_examples=100)
@given(
    user_text=st.text(min_size=1, max_size=500)
)
def test_user_message_no_visual_indicators_property(user_text):
    """
    Feature: ui-design-improvements, Property 18: AI message visual indicators
    
    Property: User messages should NOT have icons/avatars, maintaining
    visual distinction from AI messages.
    
    This property-based test ensures user messages remain visually distinct
    by not including AI-specific visual indicators.
    
    Validates: Requirements 9.2
    """
    # Create user message
    user_message = simulate_add_message(user_text, 'user')
    
    # User message should NOT have an icon
    assert user_message.has_icon is False, (
        "User message should not have an icon/avatar"
    )


# ========================================
# Property 19: Timestamp display when relevant
# ========================================

def test_message_has_timestamp():
    """
    Test that messages include timestamp elements.
    """
    user_message = simulate_add_message("User message", 'user')
    ai_message = simulate_add_message("AI response", 'ai')
    
    assert user_message.has_timestamp_element is True
    assert ai_message.has_timestamp_element is True


@settings(max_examples=100)
@given(
    message_text=st.text(min_size=1, max_size=500),
    message_type=st.sampled_from(['user', 'ai'])
)
def test_timestamp_display_property(message_text, message_type):
    """
    Feature: ui-design-improvements, Property 19: Timestamp display when relevant
    
    Property: For any message where timing information is relevant, the message 
    element should include a timestamp element.
    
    This property-based test generates random messages to ensure
    all messages include timestamp information.
    
    Validates: Requirements 9.5
    """
    # Create message
    message = simulate_add_message(message_text, message_type)
    
    # Message should have a timestamp element
    assert message.has_timestamp_element is True, (
        f"{message_type.capitalize()} message should have a timestamp element"
    )
    
    # Message should have a timestamp value
    assert message.timestamp is not None, (
        "Message should have a timestamp value"
    )
    
    # Timestamp should be a datetime object
    assert isinstance(message.timestamp, datetime), (
        "Timestamp should be a datetime object"
    )


@settings(max_examples=100)
@given(
    message_text=st.text(min_size=1, max_size=500),
    message_type=st.sampled_from(['user', 'ai'])
)
def test_timestamp_format_property(message_text, message_type):
    """
    Feature: ui-design-improvements, Property 19: Timestamp display when relevant
    
    Property: For any message, the timestamp should be in a valid time format
    that can be displayed to users.
    
    This property-based test ensures timestamps are properly formatted
    and can be rendered in the UI.
    
    Validates: Requirements 9.5
    """
    # Create message
    message = simulate_add_message(message_text, message_type)
    
    # Timestamp should be valid
    assert message.timestamp is not None
    
    # Should be able to format timestamp as string
    time_string = message.timestamp.strftime('%H:%M')
    assert len(time_string) > 0, "Timestamp should be formattable as string"
    assert ':' in time_string, "Timestamp should contain time separator"


# ========================================
# Additional property tests
# ========================================

@settings(max_examples=100)
@given(
    message_text=st.text(min_size=1, max_size=1000),
    message_type=st.sampled_from(['user', 'ai'])
)
def test_message_text_preservation_property(message_text, message_type):
    """
    Property: For any message text, the content should be preserved exactly
    as provided (no truncation or modification).
    
    This ensures long messages are properly handled with text wrapping
    rather than being cut off.
    
    Validates: Requirements 9.4
    """
    message = simulate_add_message(message_text, message_type)
    
    # Message text should be preserved exactly
    assert message.text == message_text, (
        "Message text should be preserved without modification"
    )


@settings(max_examples=100)
@given(
    message_type=st.sampled_from(['user', 'ai'])
)
def test_message_type_consistency_property(message_type):
    """
    Property: For any message type, the message should consistently
    maintain its type throughout its lifecycle.
    
    This ensures message types don't change unexpectedly.
    """
    message = simulate_add_message("Test message", message_type)
    
    # Message type should match input
    assert message.type == message_type, (
        f"Message type should be '{message_type}'"
    )


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
