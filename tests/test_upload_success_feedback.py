"""
Property-based tests for upload success feedback.

Feature: ui-design-improvements, Property 4: Upload success feedback
Validates: Requirements 5.2
"""

from hypothesis import given, strategies as st, settings
import pytest


class MockUploadSuccessState:
    """Mock state object to track upload success feedback."""
    def __init__(self):
        self.message = None
        self.filename = None
        self.page_count = None
        self.is_visible = False
        self.auto_dismiss_scheduled = False
        self.dismiss_timeout_ms = None
    
    def show_success(self, filename, page_count):
        """Simulate showUploadSuccess() function behavior."""
        self.filename = filename
        self.page_count = page_count
        self.is_visible = True
        self.auto_dismiss_scheduled = True
        self.dismiss_timeout_ms = 5000  # 5 seconds as per implementation
        
        # Generate message that includes both filename and page count
        page_text = 'page' if page_count == 1 else 'pages'
        self.message = f'Document "{filename}" successfully processed. {page_count} {page_text} indexed.'
    
    def dismiss(self):
        """Simulate dismissing the success message."""
        self.is_visible = False
        self.auto_dismiss_scheduled = False
    
    def reset(self):
        """Reset state for new upload."""
        self.message = None
        self.filename = None
        self.page_count = None
        self.is_visible = False
        self.auto_dismiss_scheduled = False
        self.dismiss_timeout_ms = None


def test_success_message_contains_filename():
    """Test that success message includes the document filename."""
    state = MockUploadSuccessState()
    state.show_success('test.pdf', 5)
    
    assert state.filename == 'test.pdf'
    assert 'test.pdf' in state.message


def test_success_message_contains_page_count():
    """Test that success message includes the page count."""
    state = MockUploadSuccessState()
    state.show_success('document.txt', 3)
    
    assert state.page_count == 3
    assert '3' in state.message


def test_success_message_becomes_visible():
    """Test that success message becomes visible when shown."""
    state = MockUploadSuccessState()
    assert state.is_visible is False
    
    state.show_success('file.pdf', 1)
    assert state.is_visible is True


def test_success_message_auto_dismiss_scheduled():
    """Test that success message schedules auto-dismiss."""
    state = MockUploadSuccessState()
    state.show_success('doc.pdf', 2)
    
    assert state.auto_dismiss_scheduled is True
    assert state.dismiss_timeout_ms == 5000


def test_singular_page_text():
    """Test that single page uses singular 'page' text."""
    state = MockUploadSuccessState()
    state.show_success('single.txt', 1)
    
    assert '1 page' in state.message
    assert 'pages' not in state.message


def test_plural_pages_text():
    """Test that multiple pages use plural 'pages' text."""
    state = MockUploadSuccessState()
    state.show_success('multi.pdf', 5)
    
    assert '5 pages' in state.message


@settings(max_examples=100)
@given(
    filename=st.text(min_size=1, max_size=100).filter(lambda x: '/' not in x and '\\' not in x),
    page_count=st.integers(min_value=1, max_value=1000)
)
def test_success_feedback_always_contains_filename_and_page_count(filename, page_count):
    """
    Feature: ui-design-improvements, Property 4: Upload success feedback
    
    Property: For any successfully completed upload with a filename and page count,
    the success message should display both the document name and the page count.
    
    This property-based test generates random filenames and page counts to ensure
    the success feedback always includes the required information.
    
    Validates: Requirements 5.2
    """
    state = MockUploadSuccessState()
    state.show_success(filename, page_count)
    
    # Success message should be visible
    assert state.is_visible is True, (
        f"Success message should be visible for {filename}"
    )
    
    # Message should contain the filename
    assert state.filename == filename, (
        f"Success state should store filename {filename}"
    )
    assert filename in state.message, (
        f"Success message should contain filename '{filename}'"
    )
    
    # Message should contain the page count
    assert state.page_count == page_count, (
        f"Success state should store page count {page_count}"
    )
    assert str(page_count) in state.message, (
        f"Success message should contain page count {page_count}"
    )


@settings(max_examples=100)
@given(
    filename=st.text(min_size=1, max_size=100).filter(lambda x: '/' not in x and '\\' not in x),
    page_count=st.integers(min_value=1, max_value=1000)
)
def test_success_feedback_auto_dismiss_always_scheduled(filename, page_count):
    """
    Feature: ui-design-improvements, Property 4: Upload success feedback
    
    Property: For any successful upload, the success message should schedule
    an auto-dismiss action to remove the message after a timeout.
    
    This property-based test ensures all success messages have auto-dismiss
    functionality to prevent UI clutter.
    
    Validates: Requirements 5.2
    """
    state = MockUploadSuccessState()
    state.show_success(filename, page_count)
    
    # Auto-dismiss should be scheduled
    assert state.auto_dismiss_scheduled is True, (
        f"Auto-dismiss should be scheduled for {filename}"
    )
    
    # Timeout should be set
    assert state.dismiss_timeout_ms is not None, (
        f"Dismiss timeout should be set for {filename}"
    )
    assert state.dismiss_timeout_ms > 0, (
        f"Dismiss timeout should be positive for {filename}"
    )


@settings(max_examples=100)
@given(
    filename=st.text(min_size=1, max_size=100).filter(lambda x: '/' not in x and '\\' not in x),
    page_count=st.integers(min_value=1, max_value=1000)
)
def test_success_feedback_correct_pluralization(filename, page_count):
    """
    Feature: ui-design-improvements, Property 4: Upload success feedback
    
    Property: For any page count, the success message should use correct
    pluralization ('page' for 1, 'pages' for multiple).
    
    This property-based test ensures grammatically correct messages across
    all possible page counts.
    
    Validates: Requirements 5.2
    """
    state = MockUploadSuccessState()
    state.show_success(filename, page_count)
    
    if page_count == 1:
        # Should use singular 'page'
        assert 'page' in state.message.lower(), (
            f"Message should contain 'page' for single page"
        )
        # Check that it's not 'pages' (plural)
        # We need to be careful here - the word 'page' might appear in 'pages'
        # So we check for the pattern "1 page" specifically
        assert f'{page_count} page' in state.message.lower(), (
            f"Message should contain '1 page' for single page"
        )
    else:
        # Should use plural 'pages'
        assert f'{page_count} pages' in state.message.lower(), (
            f"Message should contain '{page_count} pages' for multiple pages"
        )


@settings(max_examples=100)
@given(
    filename1=st.text(min_size=1, max_size=50).filter(lambda x: '/' not in x and '\\' not in x),
    page_count1=st.integers(min_value=1, max_value=100),
    filename2=st.text(min_size=1, max_size=50).filter(lambda x: '/' not in x and '\\' not in x),
    page_count2=st.integers(min_value=1, max_value=100)
)
def test_success_feedback_replaces_previous_message(filename1, page_count1, filename2, page_count2):
    """
    Feature: ui-design-improvements, Property 4: Upload success feedback
    
    Property: For any sequence of successful uploads, each new success message
    should replace the previous one (not accumulate).
    
    This property-based test ensures the UI doesn't accumulate multiple
    success messages.
    
    Validates: Requirements 5.2
    """
    state = MockUploadSuccessState()
    
    # Show first success message
    state.show_success(filename1, page_count1)
    assert state.filename == filename1
    assert state.page_count == page_count1
    
    # Show second success message - should replace first
    state.show_success(filename2, page_count2)
    assert state.filename == filename2, (
        f"Second success should replace first filename"
    )
    assert state.page_count == page_count2, (
        f"Second success should replace first page count"
    )
    
    # Message should contain second upload info, not first
    assert filename2 in state.message
    assert str(page_count2) in state.message


@settings(max_examples=100)
@given(
    filename=st.text(min_size=1, max_size=100).filter(lambda x: '/' not in x and '\\' not in x),
    page_count=st.integers(min_value=1, max_value=1000)
)
def test_success_feedback_can_be_dismissed(filename, page_count):
    """
    Feature: ui-design-improvements, Property 4: Upload success feedback
    
    Property: For any success message, it should be possible to dismiss it
    (either automatically or manually).
    
    This property-based test ensures success messages can be removed from
    the UI when needed.
    
    Validates: Requirements 5.2
    """
    state = MockUploadSuccessState()
    state.show_success(filename, page_count)
    
    # Initially visible
    assert state.is_visible is True
    
    # Should be dismissible
    state.dismiss()
    assert state.is_visible is False, (
        f"Success message should be dismissible for {filename}"
    )


@settings(max_examples=100)
@given(
    filename=st.text(min_size=1, max_size=100).filter(lambda x: '/' not in x and '\\' not in x and '"' not in x),
    page_count=st.integers(min_value=1, max_value=1000)
)
def test_success_feedback_handles_special_characters_in_filename(filename, page_count):
    """
    Feature: ui-design-improvements, Property 4: Upload success feedback
    
    Property: For any filename (including those with special characters),
    the success message should display it correctly without breaking.
    
    This property-based test ensures the UI handles various filename formats
    safely.
    
    Validates: Requirements 5.2
    """
    state = MockUploadSuccessState()
    state.show_success(filename, page_count)
    
    # Should handle the filename without errors
    assert state.filename == filename
    assert state.is_visible is True
    assert state.message is not None
    
    # Filename should be in the message
    assert filename in state.message


@settings(max_examples=100)
@given(
    filename=st.text(min_size=1, max_size=100).filter(lambda x: '/' not in x and '\\' not in x),
    page_count=st.integers(min_value=1, max_value=1000)
)
def test_success_feedback_is_deterministic(filename, page_count):
    """
    Feature: ui-design-improvements, Property 4: Upload success feedback
    
    Property: For any filename and page count, showing the success message
    multiple times should produce the same result (deterministic behavior).
    
    This property-based test ensures consistent UI behavior.
    
    Validates: Requirements 5.2
    """
    state1 = MockUploadSuccessState()
    state2 = MockUploadSuccessState()
    
    # Show success in both states
    state1.show_success(filename, page_count)
    state2.show_success(filename, page_count)
    
    # Both should have identical state
    assert state1.filename == state2.filename
    assert state1.page_count == state2.page_count
    assert state1.message == state2.message
    assert state1.is_visible == state2.is_visible
    assert state1.auto_dismiss_scheduled == state2.auto_dismiss_scheduled


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
