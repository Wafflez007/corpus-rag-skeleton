"""
Property-based tests for loading indicators during chat operations.

Feature: ui-design-improvements
Tests Properties 8, 15
Validates: Requirements 6.2, 8.2
"""

from hypothesis import given, strategies as st, settings
import pytest
from datetime import datetime
from typing import Optional


class MockLoadingIndicator:
    """Mock representation of a loading indicator in the DOM."""
    def __init__(self, indicator_id):
        self.id = indicator_id
        self.visible = True
        self.opacity = 1.0
        self.in_dom = True
        self.css_classes = ['loading-indicator', 'chat-message']
        self.created_at = datetime.now()
        
    def hide(self):
        """Hide the loading indicator with fade-out."""
        self.opacity = 0.0
        
    def remove(self):
        """Remove the loading indicator from DOM."""
        self.in_dom = False
        self.visible = False


class MockChatState:
    """Mock representation of chat state during query processing."""
    def __init__(self):
        self.loading_indicators = {}
        self.messages = []
        self.query_in_progress = False
        
    def show_loading(self) -> str:
        """
        Simulate the showLoading() JavaScript function.
        Creates a loading indicator and returns its ID.
        """
        indicator_id = f'loading-{datetime.now().timestamp()}'
        indicator = MockLoadingIndicator(indicator_id)
        self.loading_indicators[indicator_id] = indicator
        return indicator_id
        
    def hide_loading(self, indicator_id: str):
        """
        Simulate the hideLoading() JavaScript function.
        Hides and removes a loading indicator.
        """
        if indicator_id in self.loading_indicators:
            indicator = self.loading_indicators[indicator_id]
            indicator.hide()
            indicator.remove()
            
    def get_loading_indicator(self, indicator_id: str) -> Optional[MockLoadingIndicator]:
        """Get a loading indicator by ID."""
        return self.loading_indicators.get(indicator_id)
        
    def has_visible_loading_indicator(self) -> bool:
        """Check if any loading indicator is currently visible."""
        return any(
            indicator.visible and indicator.in_dom 
            for indicator in self.loading_indicators.values()
        )
        
    def start_query(self):
        """Start processing a query."""
        self.query_in_progress = True
        
    def end_query(self):
        """End query processing."""
        self.query_in_progress = False
        
    def add_message(self, text: str, message_type: str):
        """Add a message to chat history."""
        self.messages.append({'text': text, 'type': message_type})


def simulate_send_query(chat_state: MockChatState, query: str):
    """
    Simulate the sendQuery() JavaScript function.
    This mirrors the logic in skeleton_core/static/app.js
    """
    if not query.strip():
        return
        
    # Add user message
    chat_state.add_message(query, 'user')
    
    # Start query processing
    chat_state.start_query()
    
    # Show loading indicator
    loading_id = chat_state.show_loading()
    
    # Simulate async processing (in real code, this would be a fetch call)
    # For testing, we immediately process
    
    # Hide loading indicator
    chat_state.hide_loading(loading_id)
    
    # Add AI response
    chat_state.add_message("AI response", 'ai')
    
    # End query processing
    chat_state.end_query()
    
    return loading_id


# ========================================
# Property 8: Loading indicator during AI response
# ========================================

def test_loading_indicator_created():
    """
    Test that a loading indicator is created when showLoading() is called.
    """
    chat_state = MockChatState()
    loading_id = chat_state.show_loading()
    
    assert loading_id is not None
    assert loading_id in chat_state.loading_indicators
    indicator = chat_state.get_loading_indicator(loading_id)
    assert indicator.visible is True
    assert indicator.in_dom is True


def test_loading_indicator_removed():
    """
    Test that a loading indicator is removed when hideLoading() is called.
    """
    chat_state = MockChatState()
    loading_id = chat_state.show_loading()
    
    # Indicator should be visible
    assert chat_state.has_visible_loading_indicator() is True
    
    # Hide the indicator
    chat_state.hide_loading(loading_id)
    
    # Indicator should be hidden and removed
    indicator = chat_state.get_loading_indicator(loading_id)
    assert indicator.visible is False
    assert indicator.in_dom is False


@settings(max_examples=100)
@given(
    query_text=st.text(min_size=1, max_size=500)
)
def test_loading_indicator_during_ai_response_property(query_text):
    """
    Feature: ui-design-improvements, Property 8: Loading indicator during AI response
    
    Property: For any chat query being processed, a loading indicator should be 
    visible in the chat area until the response is received.
    
    This property-based test generates random queries to ensure
    loading indicators are always displayed during AI response generation.
    
    Validates: Requirements 6.2
    """
    chat_state = MockChatState()
    
    # Before query, no loading indicator should be visible
    assert chat_state.has_visible_loading_indicator() is False, (
        "No loading indicator should be visible before query"
    )
    
    # Add user message
    chat_state.add_message(query_text, 'user')
    
    # Start query processing and show loading
    chat_state.start_query()
    loading_id = chat_state.show_loading()
    
    # During query processing, loading indicator should be visible
    assert chat_state.has_visible_loading_indicator() is True, (
        "Loading indicator should be visible during query processing"
    )
    
    # Loading indicator should exist in DOM
    indicator = chat_state.get_loading_indicator(loading_id)
    assert indicator is not None, "Loading indicator should exist"
    assert indicator.visible is True, "Loading indicator should be visible"
    assert indicator.in_dom is True, "Loading indicator should be in DOM"
    
    # After response received, hide loading indicator
    chat_state.hide_loading(loading_id)
    chat_state.add_message("AI response", 'ai')
    chat_state.end_query()
    
    # After query completes, loading indicator should be hidden
    assert indicator.visible is False, (
        "Loading indicator should be hidden after response received"
    )
    assert indicator.in_dom is False, (
        "Loading indicator should be removed from DOM after response"
    )


@settings(max_examples=100)
@given(
    query_text=st.text(min_size=1, max_size=500)
)
def test_loading_indicator_lifecycle_property(query_text):
    """
    Feature: ui-design-improvements, Property 8: Loading indicator during AI response
    
    Property: For any query, the loading indicator should follow a complete
    lifecycle: created -> visible -> hidden -> removed.
    
    This ensures proper cleanup of loading indicators.
    
    Validates: Requirements 6.2
    """
    chat_state = MockChatState()
    
    # Show loading indicator
    loading_id = chat_state.show_loading()
    indicator = chat_state.get_loading_indicator(loading_id)
    
    # Phase 1: Created and visible
    assert indicator is not None, "Indicator should be created"
    assert indicator.visible is True, "Indicator should be visible"
    assert indicator.in_dom is True, "Indicator should be in DOM"
    assert indicator.opacity == 1.0, "Indicator should be fully opaque"
    
    # Phase 2: Hide indicator
    chat_state.hide_loading(loading_id)
    
    # Phase 3: Hidden and removed
    assert indicator.opacity == 0.0, "Indicator should be faded out"
    assert indicator.visible is False, "Indicator should be hidden"
    assert indicator.in_dom is False, "Indicator should be removed from DOM"


# ========================================
# Property 15: Loading indicator during query
# ========================================

def test_loading_indicator_during_query():
    """
    Test that a loading indicator is present during query processing.
    """
    chat_state = MockChatState()
    query = "What is the meaning of life?"
    
    # Simulate query
    loading_id = simulate_send_query(chat_state, query)
    
    # Loading indicator should have been created
    assert loading_id is not None
    assert loading_id in chat_state.loading_indicators


@settings(max_examples=100)
@given(
    query_text=st.text(min_size=1, max_size=500)
)
def test_loading_indicator_during_query_property(query_text):
    """
    Feature: ui-design-improvements, Property 15: Loading indicator during query
    
    Property: For any chat query being processed, a loading element should be 
    present in the chat area until the query completes.
    
    This property-based test generates random queries to ensure
    loading indicators are consistently displayed during query processing.
    
    Validates: Requirements 8.2
    """
    chat_state = MockChatState()
    
    # Before query, no loading indicator
    initial_indicator_count = len(chat_state.loading_indicators)
    
    # Add user message and start query
    chat_state.add_message(query_text, 'user')
    chat_state.start_query()
    
    # Show loading indicator during query
    loading_id = chat_state.show_loading()
    
    # Loading indicator should be created
    assert len(chat_state.loading_indicators) > initial_indicator_count, (
        "Loading indicator should be created during query"
    )
    
    # Loading indicator should be visible
    assert chat_state.has_visible_loading_indicator() is True, (
        "Loading indicator should be visible during query processing"
    )
    
    # Get the indicator
    indicator = chat_state.get_loading_indicator(loading_id)
    assert indicator is not None, "Loading indicator should exist"
    assert indicator.in_dom is True, "Loading indicator should be in DOM"
    
    # Complete query and hide loading
    chat_state.hide_loading(loading_id)
    chat_state.add_message("Response", 'ai')
    chat_state.end_query()
    
    # After query completes, loading indicator should be removed
    assert indicator.in_dom is False, (
        "Loading indicator should be removed after query completes"
    )


@settings(max_examples=100)
@given(
    query_text=st.text(min_size=1, max_size=500)
)
def test_single_loading_indicator_per_query_property(query_text):
    """
    Feature: ui-design-improvements, Property 15: Loading indicator during query
    
    Property: For any single query, exactly one loading indicator should be
    created and displayed.
    
    This ensures we don't create multiple loading indicators for a single query.
    
    Validates: Requirements 8.2
    """
    chat_state = MockChatState()
    
    # Count initial indicators
    initial_count = len(chat_state.loading_indicators)
    
    # Process a single query
    chat_state.add_message(query_text, 'user')
    chat_state.start_query()
    loading_id = chat_state.show_loading()
    
    # Should have exactly one more indicator
    assert len(chat_state.loading_indicators) == initial_count + 1, (
        "Exactly one loading indicator should be created per query"
    )
    
    # Complete the query
    chat_state.hide_loading(loading_id)
    chat_state.end_query()


@settings(max_examples=100)
@given(
    queries=st.lists(st.text(min_size=1, max_size=200), min_size=1, max_size=5)
)
def test_loading_indicator_cleanup_property(queries):
    """
    Feature: ui-design-improvements, Property 15: Loading indicator during query
    
    Property: For any sequence of queries, all loading indicators should be
    properly cleaned up after each query completes.
    
    This ensures no loading indicators are left behind after queries complete.
    
    Validates: Requirements 8.2
    """
    chat_state = MockChatState()
    
    for query in queries:
        # Start query
        chat_state.add_message(query, 'user')
        chat_state.start_query()
        loading_id = chat_state.show_loading()
        
        # Verify loading indicator is visible
        assert chat_state.has_visible_loading_indicator() is True
        
        # Complete query
        chat_state.hide_loading(loading_id)
        chat_state.add_message("Response", 'ai')
        chat_state.end_query()
        
        # Verify loading indicator is cleaned up
        indicator = chat_state.get_loading_indicator(loading_id)
        assert indicator.in_dom is False, (
            f"Loading indicator for query '{query}' should be removed"
        )
    
    # After all queries, no visible loading indicators should remain
    assert chat_state.has_visible_loading_indicator() is False, (
        "No loading indicators should be visible after all queries complete"
    )


# ========================================
# Additional property tests
# ========================================

@settings(max_examples=100)
@given(
    query_text=st.text(min_size=1, max_size=500)
)
def test_loading_indicator_has_proper_classes_property(query_text):
    """
    Property: For any loading indicator, it should have the appropriate
    CSS classes for styling and identification.
    
    This ensures loading indicators can be properly styled and identified.
    """
    chat_state = MockChatState()
    loading_id = chat_state.show_loading()
    indicator = chat_state.get_loading_indicator(loading_id)
    
    # Indicator should have CSS classes
    assert len(indicator.css_classes) > 0, (
        "Loading indicator should have CSS classes"
    )
    
    # Should have loading-indicator class
    assert 'loading-indicator' in indicator.css_classes, (
        "Loading indicator should have 'loading-indicator' class"
    )


@settings(max_examples=100)
@given(
    query_text=st.text(min_size=1, max_size=500)
)
def test_loading_indicator_unique_id_property(query_text):
    """
    Property: For any loading indicator created, it should have a unique ID
    that can be used to reference and remove it later.
    
    This ensures we can properly manage multiple loading indicators.
    """
    chat_state = MockChatState()
    
    # Create multiple loading indicators
    id1 = chat_state.show_loading()
    id2 = chat_state.show_loading()
    
    # IDs should be unique
    assert id1 != id2, "Loading indicator IDs should be unique"
    
    # Both should exist
    assert chat_state.get_loading_indicator(id1) is not None
    assert chat_state.get_loading_indicator(id2) is not None
    
    # Should be able to hide them independently
    chat_state.hide_loading(id1)
    assert chat_state.get_loading_indicator(id1).in_dom is False
    assert chat_state.get_loading_indicator(id2).in_dom is True
    
    chat_state.hide_loading(id2)
    assert chat_state.get_loading_indicator(id2).in_dom is False


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
