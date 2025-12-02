"""
Tests for chat bubble rendering with DaisyUI components.

Feature: tailwind-daisyui-integration
Task: 5. Migrate Legal Eagle chat interface
"""

from bs4 import BeautifulSoup
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_chat_bubble_classes_in_javascript():
    """Verify JavaScript uses DaisyUI chat bubble classes."""
    with open('skeleton_core/static/app.js', 'r', encoding='utf-8') as f:
        js_content = f.read()
    
    # Check for DaisyUI chat classes
    assert 'chat-end' in js_content, "Should use 'chat-end' for user messages"
    assert 'chat-start' in js_content, "Should use 'chat-start' for AI messages"
    assert 'chat-bubble' in js_content, "Should use 'chat-bubble' class"
    assert 'chat-bubble-primary' in js_content, "Should use 'chat-bubble-primary' for user messages"


def test_chat_footer_for_timestamp():
    """Verify JavaScript uses chat-footer for timestamps."""
    with open('skeleton_core/static/app.js', 'r', encoding='utf-8') as f:
        js_content = f.read()
    
    assert 'chat-footer' in js_content, "Should use 'chat-footer' for timestamps"


def test_no_old_custom_message_classes():
    """Verify old custom message classes are removed from JavaScript."""
    with open('skeleton_core/static/app.js', 'r', encoding='utf-8') as f:
        js_content = f.read()
    
    # Check that old custom classes are not in the addMessage function
    # We look for the function definition and check its content
    add_message_start = js_content.find('function addMessage(text, type)')
    add_message_end = js_content.find('function formatMessageText', add_message_start)
    
    if add_message_start != -1 and add_message_end != -1:
        add_message_content = js_content[add_message_start:add_message_end]
        
        # Old classes that should not be present
        assert 'chat-message-user' not in add_message_content, "Should not use old 'chat-message-user' class"
        assert 'chat-message-ai' not in add_message_content, "Should not use old 'chat-message-ai' class"
        assert 'rounded-2xl rounded-tr-none' not in add_message_content, "Should not use old custom rounding"
        assert 'rounded-2xl rounded-tl-none' not in add_message_content, "Should not use old custom rounding"


def test_message_structure_uses_daisyui():
    """Verify message structure follows DaisyUI chat component pattern."""
    with open('skeleton_core/static/app.js', 'r', encoding='utf-8') as f:
        js_content = f.read()
    
    # Find the addMessage function
    add_message_start = js_content.find('function addMessage(text, type)')
    add_message_end = js_content.find('function formatMessageText', add_message_start)
    
    if add_message_start != -1 and add_message_end != -1:
        add_message_content = js_content[add_message_start:add_message_end]
        
        # Check for DaisyUI structure
        assert 'chatDiv.className' in add_message_content, "Should create chat div"
        assert 'bubbleDiv.className' in add_message_content, "Should create bubble div"
        assert 'chatDiv.appendChild(bubbleDiv)' in add_message_content, "Should append bubble to chat"


def test_user_message_uses_chat_end():
    """Verify user messages use chat-end class."""
    with open('skeleton_core/static/app.js', 'r', encoding='utf-8') as f:
        js_content = f.read()
    
    # Check that user messages (type === 'user') use chat-end
    assert "type === 'user' ? 'chat-end'" in js_content, "User messages should use chat-end"


def test_ai_message_uses_chat_start():
    """Verify AI messages use chat-start class."""
    with open('skeleton_core/static/app.js', 'r', encoding='utf-8') as f:
        js_content = f.read()
    
    # Check that AI messages use chat-start
    assert "'chat-start'" in js_content, "AI messages should use chat-start"


def test_user_message_uses_primary_bubble():
    """Verify user messages use chat-bubble-primary class."""
    with open('skeleton_core/static/app.js', 'r', encoding='utf-8') as f:
        js_content = f.read()
    
    # Check that user messages use chat-bubble-primary
    assert "type === 'user'" in js_content, "Should check for user type"
    assert "'chat-bubble chat-bubble-primary" in js_content, "User messages should use chat-bubble-primary"


def test_typewriter_effect_preserved():
    """Verify typewriter effect is preserved for AI messages."""
    with open('skeleton_core/static/app.js', 'r', encoding='utf-8') as f:
        js_content = f.read()
    
    # Check that typewriter effect is still present
    assert 'function typeWriter()' in js_content, "Typewriter function should exist"
    assert "if (type === 'ai')" in js_content, "Should check for AI message type"
    assert 'audioManager.playResponseSound()' in js_content, "Should play sound for AI messages"


def test_timestamp_preserved():
    """Verify timestamp functionality is preserved."""
    with open('skeleton_core/static/app.js', 'r', encoding='utf-8') as f:
        js_content = f.read()
    
    # Check that timestamp is still added
    assert 'toLocaleTimeString' in js_content, "Should format timestamp"
    assert 'chat-footer' in js_content, "Should use chat-footer for timestamp"


def test_scroll_to_bottom_preserved():
    """Verify scroll to bottom functionality is preserved."""
    with open('skeleton_core/static/app.js', 'r', encoding='utf-8') as f:
        js_content = f.read()
    
    # Check that scrollToBottom is called
    add_message_start = js_content.find('function addMessage(text, type)')
    add_message_end = js_content.find('function formatMessageText', add_message_start)
    
    if add_message_start != -1 and add_message_end != -1:
        add_message_content = js_content[add_message_start:add_message_end]
        assert 'scrollToBottom()' in add_message_content, "Should call scrollToBottom"
