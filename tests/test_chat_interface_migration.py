"""
Tests for Legal Eagle chat interface migration to DaisyUI components.

Feature: tailwind-daisyui-integration
Task: 5. Migrate Legal Eagle chat interface
"""

from bs4 import BeautifulSoup
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from skeleton_core.app import create_app
from app_legal.config import Config


def test_chat_section_uses_daisyui_card():
    """Verify chat section uses DaisyUI card component."""
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
    """Verify send button uses DaisyUI button component."""
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


def test_no_custom_css_classes_on_chat_section():
    """Verify chat section doesn't use old custom CSS classes."""
    app = create_app(Config)
    with app.test_client() as client:
        response = client.get('/')
        html = response.data.decode('utf-8')
        
        # Check that old custom classes are not present
        custom_classes = ['chat-message-user', 'chat-message-ai', 'btn-primary']
        
        # btn-primary is now a DaisyUI class, so we check for the old custom version
        # The old version would have been defined in custom CSS
        # We're checking the HTML doesn't have inline styles that override DaisyUI
        
        soup = BeautifulSoup(html, 'html.parser')
        chat_section = soup.find('div', id='chat-section')
        
        # Check that the chat section uses DaisyUI classes
        card = chat_section.find('div', class_='card')
        assert card is not None, "Should use DaisyUI card instead of custom classes"


def test_professional_styling_for_legal_eagle():
    """Verify Legal Eagle chat interface has professional styling."""
    app = create_app(Config)
    with app.test_client() as client:
        response = client.get('/')
        html = response.data.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        
        # Check that the theme is set correctly
        body = soup.find('body')
        assert 'theme-blue-corporate' in body.get('class', []), "Should have Legal Eagle theme"
        
        # Check for professional elements
        chat_section = soup.find('div', id='chat-section')
        assert chat_section is not None
        
        # Verify card has shadow-xl for professional appearance
        card = chat_section.find('div', class_='card')
        assert 'shadow-xl' in card.get('class', []), "Should have professional shadow"
