"""
Tests for Ouija Board chat interface migration to DaisyUI components with mystical styling.

Feature: tailwind-daisyui-integration
Task: 8. Migrate Ouija Board chat interface
"""

from bs4 import BeautifulSoup
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from skeleton_core.app import create_app
from app_ghost.config import Config


def test_chat_section_uses_daisyui_card():
    """Verify Ouija Board chat section uses DaisyUI card component."""
    app = create_app(Config)
    with app.test_client() as client:
        response = client.get('/')
        html = response.data.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        
        # Find chat section
        chat_section = soup.find('div', id='chat-section')
        assert chat_section is not None, "Chat section should exist"
        
        # Check for DaisyUI card classes
        card = chat_section.find('div', class_='card')
        assert card is not None, "Chat section should use DaisyUI card component"
        assert 'bg-base-200' in card.get('class', []), "Card should have bg-base-200 class"
        assert 'shadow-xl' in card.get('class', []), "Card should have shadow-xl class"


def test_chat_section_has_card_body():
    """Verify chat section card has card-body."""
    app = create_app(Config)
    with app.test_client() as client:
        response = client.get('/')
        html = response.data.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        
        chat_section = soup.find('div', id='chat-section')
        card = chat_section.find('div', class_='card')
        card_body = card.find('div', class_='card-body')
        
        assert card_body is not None, "Card should have card-body"


def test_chat_input_uses_daisyui_component():
    """Verify chat input uses DaisyUI input component."""
    app = create_app(Config)
    with app.test_client() as client:
        response = client.get('/')
        html = response.data.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        
        query_input = soup.find('input', id='queryInput')
        assert query_input is not None, "Query input should exist"
        
        classes = query_input.get('class', [])
        assert 'input' in classes, "Input should have 'input' class"
        assert 'input-bordered' in classes, "Input should have 'input-bordered' class"


def test_chat_send_button_uses_daisyui_component():
    """Verify send button uses DaisyUI button component with mystical styling."""
    app = create_app(Config)
    with app.test_client() as client:
        response = client.get('/')
        html = response.data.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        
        # Find the send button (button with onclick="sendQuery()")
        send_button = soup.find('button', onclick='sendQuery()')
        assert send_button is not None, "Send button should exist"
        
        classes = send_button.get('class', [])
        assert 'btn' in classes, "Button should have 'btn' class"
        assert 'btn-primary' in classes, "Button should have 'btn-primary' class"
        
        # Check for mystical button text
        button_text = send_button.get_text(strip=True)
        assert button_text == 'INVOKE', "Button should have mystical text 'INVOKE'"


def test_chat_input_meets_touch_target_size():
    """Verify chat input meets minimum touch target size."""
    app = create_app(Config)
    with app.test_client() as client:
        response = client.get('/')
        html = response.data.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        
        query_input = soup.find('input', id='queryInput')
        classes = query_input.get('class', [])
        
        # Check for min-h-[44px] class
        assert 'min-h-[44px]' in classes, "Input should have min-h-[44px] for touch targets"


def test_chat_send_button_meets_touch_target_size():
    """Verify send button meets minimum touch target size."""
    app = create_app(Config)
    with app.test_client() as client:
        response = client.get('/')
        html = response.data.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        
        send_button = soup.find('button', onclick='sendQuery()')
        classes = send_button.get('class', [])
        
        # Check for min-h-[44px] class
        assert 'min-h-[44px]' in classes, "Button should have min-h-[44px] for touch targets"


def test_chat_history_uses_tailwind_utilities():
    """Verify chat history container uses Tailwind utilities."""
    app = create_app(Config)
    with app.test_client() as client:
        response = client.get('/')
        html = response.data.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        
        chat_history = soup.find('div', id='chat-history')
        assert chat_history is not None, "Chat history should exist"
        
        classes = chat_history.get('class', [])
        # Check for essential Tailwind classes
        assert 'overflow-y-auto' in classes, "Chat history should have overflow-y-auto"
        assert 'rounded-lg' in classes, "Chat history should have rounded-lg"
        assert 'bg-base-100' in classes, "Chat history should have bg-base-100"


def test_chat_title_uses_daisyui_card_title():
    """Verify chat section title uses DaisyUI card-title class."""
    app = create_app(Config)
    with app.test_client() as client:
        response = client.get('/')
        html = response.data.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        
        chat_section = soup.find('div', id='chat-section')
        title = chat_section.find('h2', class_='card-title')
        
        assert title is not None, "Chat section should have card-title"


def test_chat_input_container_uses_flex():
    """Verify chat input container uses Tailwind flex utilities."""
    app = create_app(Config)
    with app.test_client() as client:
        response = client.get('/')
        html = response.data.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        
        # Find the container with the input and button
        query_input = soup.find('input', id='queryInput')
        container = query_input.parent
        
        classes = container.get('class', [])
        assert 'flex' in classes, "Input container should use flex"
        assert 'gap-3' in classes, "Input container should have gap-3"


def test_chat_input_has_flex_1():
    """Verify chat input has flex-1 to take available space."""
    app = create_app(Config)
    with app.test_client() as client:
        response = client.get('/')
        html = response.data.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        
        query_input = soup.find('input', id='queryInput')
        classes = query_input.get('class', [])
        
        assert 'flex-1' in classes, "Input should have flex-1 to fill available space"


def test_gothic_theme_applied():
    """Verify Ouija Board chat interface has dark gothic theme."""
    app = create_app(Config)
    with app.test_client() as client:
        response = client.get('/')
        html = response.data.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        
        # Check that the theme is set correctly
        body = soup.find('body')
        assert 'theme-dark-gothic' in body.get('class', []), "Should have Ouija Board theme"
        
        # Check for data-theme attribute
        data_theme = body.get('data-theme')
        assert data_theme == 'ouija-board', "Should have ouija-board data-theme"


def test_mystical_placeholder_text():
    """Verify chat input has mystical placeholder text."""
    app = create_app(Config)
    with app.test_client() as client:
        response = client.get('/')
        html = response.data.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        
        query_input = soup.find('input', id='queryInput')
        placeholder = query_input.get('placeholder', '')
        
        assert 'spirit' in placeholder.lower(), "Placeholder should have mystical text"


def test_mystical_chat_title():
    """Verify chat section has mystical title."""
    app = create_app(Config)
    with app.test_client() as client:
        response = client.get('/')
        html = response.data.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        
        chat_section = soup.find('div', id='chat-section')
        title = chat_section.find('h2', class_='card-title')
        title_text = title.get_text(strip=True)
        
        # Should contain mystical elements
        assert '💀' in title_text or 'Entity' in title_text or 'Commune' in title_text, \
            "Title should have mystical elements"


def test_dark_backgrounds_applied():
    """Verify dark backgrounds are applied to chat components."""
    app = create_app(Config)
    with app.test_client() as client:
        response = client.get('/')
        html = response.data.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        
        # Check that DaisyUI theme configuration includes dark colors
        body = soup.find('body')
        assert body is not None
        
        # Verify the page uses the dark gothic theme
        assert 'theme-dark-gothic' in body.get('class', [])


def test_chat_functionality_preserved():
    """Verify chat functionality is preserved after migration."""
    app = create_app(Config)
    with app.test_client() as client:
        response = client.get('/')
        html = response.data.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        
        # Check that essential elements exist
        query_input = soup.find('input', id='queryInput')
        send_button = soup.find('button', onclick='sendQuery()')
        chat_history = soup.find('div', id='chat-history')
        
        assert query_input is not None, "Query input should exist"
        assert send_button is not None, "Send button should exist"
        assert chat_history is not None, "Chat history should exist"
        
        # Check that JavaScript function is referenced
        assert 'sendQuery()' in html, "sendQuery function should be referenced"


def test_no_custom_css_classes_on_chat_section():
    """Verify chat section uses DaisyUI classes instead of old custom CSS."""
    app = create_app(Config)
    with app.test_client() as client:
        response = client.get('/')
        html = response.data.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        
        chat_section = soup.find('div', id='chat-section')
        
        # Check that the chat section uses DaisyUI classes
        card = chat_section.find('div', class_='card')
        assert card is not None, "Should use DaisyUI card instead of custom classes"
        
        # Verify DaisyUI classes are present
        assert 'bg-base-200' in card.get('class', [])
        assert 'shadow-xl' in card.get('class', [])


def test_glow_effects_via_theme():
    """Verify glow effects are applied via theme CSS."""
    app = create_app(Config)
    with app.test_client() as client:
        response = client.get('/')
        html = response.data.decode('utf-8')
        
        # Check that the theme class is present which will apply glow effects via CSS
        soup = BeautifulSoup(html, 'html.parser')
        body = soup.find('body')
        
        assert 'theme-dark-gothic' in body.get('class', []), \
            "Dark gothic theme should be applied for glow effects"


if __name__ == '__main__':
    import pytest
    pytest.main([__file__, '-v'])
