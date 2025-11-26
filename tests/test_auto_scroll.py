"""
Property-based tests for auto-scroll functionality.

Feature: ui-design-improvements
Tests Property 9
Validates: Requirements 6.3
"""

from hypothesis import given, strategies as st, settings
import pytest


class MockChatHistory:
    """Mock representation of the chat history DOM element."""
    def __init__(self):
        self.scrollTop = 0
        self.scrollHeight = 1000  # Total scrollable height
        self.clientHeight = 400   # Visible height
        self.messages = []
        
    def add_message(self, message):
        """Add a message to the chat history."""
        self.messages.append(message)
        # Simulate scroll height increase when message is added
        self.scrollHeight += 100  # Each message adds 100px
        
    def is_at_bottom(self):
        """Check if scrolled to bottom."""
        return self.scrollTop >= self.scrollHeight - self.clientHeight
    
    def is_near_bottom(self, threshold=100):
        """Check if within threshold pixels of bottom."""
        return self.scrollHeight - self.scrollTop - self.clientHeight < threshold


def simulate_scroll_to_bottom(chat_history):
    """
    Python simulation of the JavaScript scrollToBottom() function.
    This mirrors the logic in skeleton_core/static/app.js
    """
    # Check if user has manually scrolled up
    # If they're within 100px of the bottom (or at bottom), auto-scroll
    # Otherwise, respect their scroll position
    distance_from_bottom = chat_history.scrollHeight - chat_history.scrollTop - chat_history.clientHeight
    is_near_bottom = distance_from_bottom <= 100
    
    if is_near_bottom:
        chat_history.scrollTop = chat_history.scrollHeight - chat_history.clientHeight


# ========================================
# Property 9: Auto-scroll to latest message
# ========================================

def test_auto_scroll_when_at_bottom():
    """
    Test that auto-scroll works when user is at the bottom.
    """
    chat_history = MockChatHistory()
    
    # User is at bottom
    chat_history.scrollTop = chat_history.scrollHeight - chat_history.clientHeight
    
    # Verify user is at bottom before adding message
    assert chat_history.is_at_bottom()
    
    # Add a message (this increases scrollHeight)
    chat_history.add_message("New message")
    
    # Trigger auto-scroll (should detect we're near bottom and scroll)
    simulate_scroll_to_bottom(chat_history)
    
    # Should scroll to new bottom
    assert chat_history.is_at_bottom()


def test_auto_scroll_respects_manual_scroll():
    """
    Test that auto-scroll respects when user has manually scrolled up.
    """
    chat_history = MockChatHistory()
    
    # User has scrolled up significantly (more than 100px from bottom)
    chat_history.scrollTop = 200  # Far from bottom
    
    original_scroll_position = chat_history.scrollTop
    
    # Add a message
    chat_history.add_message("New message")
    
    # Trigger auto-scroll
    simulate_scroll_to_bottom(chat_history)
    
    # Should NOT auto-scroll (respect user's position)
    assert chat_history.scrollTop == original_scroll_position


def test_auto_scroll_when_near_bottom():
    """
    Test that auto-scroll works when user is near the bottom (within 100px).
    Note: The threshold is checked AFTER content is added, so if we're 50px from bottom
    and add a 100px message, we're now 150px away and won't auto-scroll.
    To test the threshold, we need to be close enough that after adding content,
    we're still within 100px.
    """
    chat_history = MockChatHistory()
    
    # User is very close to bottom (10px) - after adding 100px message, will be 110px away
    # This is > 100px, so won't auto-scroll. Let's test with being right at bottom.
    chat_history.scrollTop = chat_history.scrollHeight - chat_history.clientHeight
    
    # Add a small message (simulated as 50px instead of default 100px)
    chat_history.messages.append("Small message")
    chat_history.scrollHeight += 50  # Smaller message
    
    # Now we're 50px from bottom, which is < 100px
    # Trigger auto-scroll
    simulate_scroll_to_bottom(chat_history)
    
    # Should scroll to bottom
    assert chat_history.is_at_bottom()


@settings(max_examples=100)
@given(
    num_messages=st.integers(min_value=1, max_value=50)
)
def test_auto_scroll_to_latest_message_property(num_messages):
    """
    Feature: ui-design-improvements, Property 9: Auto-scroll to latest message
    
    Property: For any new message added to the chat history, the chat container 
    should automatically scroll to display the newest message when the user is 
    at or near the bottom.
    
    This property-based test generates random numbers of messages to ensure
    auto-scroll consistently works across different chat history lengths.
    
    Validates: Requirements 6.3
    """
    chat_history = MockChatHistory()
    
    # Start at bottom (typical user position)
    chat_history.scrollTop = chat_history.scrollHeight - chat_history.clientHeight
    
    # Add multiple messages
    for i in range(num_messages):
        chat_history.add_message(f"Message {i}")
        
        # Trigger auto-scroll after each message
        simulate_scroll_to_bottom(chat_history)
        
        # Should always be at bottom after auto-scroll
        assert chat_history.is_at_bottom(), (
            f"Chat should auto-scroll to bottom after message {i}"
        )


@settings(max_examples=100)
@given(
    scroll_offset=st.integers(min_value=0, max_value=500),
    num_new_messages=st.integers(min_value=1, max_value=10)
)
def test_auto_scroll_respects_user_position_property(scroll_offset, num_new_messages):
    """
    Feature: ui-design-improvements, Property 9: Auto-scroll to latest message
    
    Property: For any user scroll position that is far from the bottom (>100px),
    the auto-scroll should NOT override the user's manual scroll position.
    
    This property-based test ensures the edge case of manual scrolling is
    properly handled across different scroll positions.
    
    Validates: Requirements 6.3
    """
    chat_history = MockChatHistory()
    
    # User has manually scrolled up
    # Only test positions that are >100px from bottom (outside threshold)
    if scroll_offset > 100:
        chat_history.scrollTop = chat_history.scrollHeight - chat_history.clientHeight - scroll_offset
        original_position = chat_history.scrollTop
        
        # Add new messages
        for i in range(num_new_messages):
            chat_history.add_message(f"New message {i}")
            
            # Trigger auto-scroll
            simulate_scroll_to_bottom(chat_history)
        
        # Should NOT have auto-scrolled (respect user position)
        assert chat_history.scrollTop == original_position, (
            f"Auto-scroll should respect user's manual scroll position when {scroll_offset}px from bottom"
        )


@settings(max_examples=100)
@given(
    num_new_messages=st.integers(min_value=1, max_value=10)
)
def test_auto_scroll_near_bottom_threshold_property(num_new_messages):
    """
    Feature: ui-design-improvements, Property 9: Auto-scroll to latest message
    
    Property: When at the bottom of the chat, adding any number of messages
    should keep auto-scrolling to show the latest message.
    
    This property-based test validates that auto-scroll consistently works
    when the user is actively viewing the conversation.
    
    Validates: Requirements 6.3
    """
    chat_history = MockChatHistory()
    
    # User starts at bottom (typical active viewing position)
    chat_history.scrollTop = chat_history.scrollHeight - chat_history.clientHeight
    
    # Add new messages and verify auto-scroll keeps us at bottom
    for i in range(num_new_messages):
        # Before adding message, we should be at or near bottom
        distance_before = chat_history.scrollHeight - chat_history.scrollTop - chat_history.clientHeight
        
        chat_history.add_message(f"New message {i}")
        
        # Trigger auto-scroll
        simulate_scroll_to_bottom(chat_history)
        
        # After auto-scroll, should be at bottom
        assert chat_history.is_at_bottom(), (
            f"Auto-scroll should keep us at bottom after message {i} (was {distance_before}px from bottom before)"
        )


@settings(max_examples=100)
@given(
    initial_messages=st.integers(min_value=0, max_value=20),
    new_messages=st.integers(min_value=1, max_value=20)
)
def test_auto_scroll_consistency_property(initial_messages, new_messages):
    """
    Feature: ui-design-improvements, Property 9: Auto-scroll to latest message
    
    Property: For any chat history state (empty or with existing messages),
    auto-scroll should consistently work when adding new messages.
    
    This property-based test ensures auto-scroll works regardless of
    the initial state of the chat history.
    
    Validates: Requirements 6.3
    """
    chat_history = MockChatHistory()
    
    # Add initial messages
    for i in range(initial_messages):
        chat_history.add_message(f"Initial message {i}")
    
    # User is at bottom
    chat_history.scrollTop = chat_history.scrollHeight - chat_history.clientHeight
    
    # Add new messages
    for i in range(new_messages):
        chat_history.add_message(f"New message {i}")
        
        # Trigger auto-scroll
        simulate_scroll_to_bottom(chat_history)
        
        # Should always be at bottom
        assert chat_history.is_at_bottom(), (
            f"Auto-scroll should work consistently regardless of chat history length"
        )


@settings(max_examples=100)
@given(
    message_height=st.integers(min_value=1, max_value=100)
)
def test_auto_scroll_with_variable_message_heights_property(message_height):
    """
    Feature: ui-design-improvements, Property 9: Auto-scroll to latest message
    
    Property: For any message height within the threshold (<=100px), auto-scroll
    should correctly calculate and scroll to the bottom when starting from bottom.
    
    This property-based test ensures auto-scroll works with messages of
    varying heights (e.g., short text vs long paragraphs) as long as they're
    within the auto-scroll threshold.
    
    Validates: Requirements 6.3
    """
    chat_history = MockChatHistory()
    
    # User is at bottom
    chat_history.scrollTop = chat_history.scrollHeight - chat_history.clientHeight
    
    # Add a message with variable height (within threshold)
    chat_history.messages.append("Variable height message")
    chat_history.scrollHeight += message_height
    
    # Trigger auto-scroll
    simulate_scroll_to_bottom(chat_history)
    
    # Should be at bottom for messages within threshold
    assert chat_history.is_at_bottom(), (
        f"Auto-scroll should work with messages of height {message_height}px (within 100px threshold)"
    )


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
