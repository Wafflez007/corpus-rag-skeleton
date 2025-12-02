"""
Tests for touch target size requirements (44x44px minimum)
Validates Requirements 8.2
"""

import pytest
import re
from bs4 import BeautifulSoup


def get_template_content():
    """Read the main template file"""
    with open('skeleton_core/templates/index.html', 'r', encoding='utf-8') as f:
        return f.read()


def get_launcher_content():
    """Read the launcher.py file"""
    with open('launcher.py', 'r', encoding='utf-8') as f:
        return f.read()


def get_app_js_content():
    """Read the app.js file"""
    with open('skeleton_core/static/app.js', 'r', encoding='utf-8') as f:
        return f.read()


class TestTouchTargetSizes:
    """Test suite for touch target size requirements"""
    
    def test_file_input_has_minimum_height(self):
        """File input should have min-h-[44px]"""
        content = get_template_content()
        soup = BeautifulSoup(content, 'html.parser')
        
        file_input = soup.find('input', {'id': 'fileInput'})
        assert file_input is not None, "File input not found"
        
        classes = file_input.get('class', [])
        assert 'min-h-[44px]' in classes, "File input missing min-h-[44px]"
    
    def test_upload_button_has_minimum_size(self):
        """Upload button should have min-h-[44px] and min-w-[44px]"""
        content = get_template_content()
        soup = BeautifulSoup(content, 'html.parser')
        
        # Find upload button by onclick attribute
        upload_button = soup.find('button', string=re.compile(r'UPLOAD|OFFER'))
        assert upload_button is not None, "Upload button not found"
        
        classes = upload_button.get('class', [])
        assert 'min-h-[44px]' in classes, "Upload button missing min-h-[44px]"
        assert 'min-w-[44px]' in classes, "Upload button missing min-w-[44px]"
    
    def test_query_input_has_minimum_height(self):
        """Query input should have min-h-[44px]"""
        content = get_template_content()
        soup = BeautifulSoup(content, 'html.parser')
        
        query_input = soup.find('input', {'id': 'queryInput'})
        assert query_input is not None, "Query input not found"
        
        classes = query_input.get('class', [])
        assert 'min-h-[44px]' in classes, "Query input missing min-h-[44px]"
    
    def test_send_button_has_minimum_size(self):
        """Send button should have min-h-[44px] and min-w-[44px]"""
        content = get_template_content()
        soup = BeautifulSoup(content, 'html.parser')
        
        # Find send button by onclick attribute
        send_button = soup.find('button', string=re.compile(r'SEND|INVOKE'))
        assert send_button is not None, "Send button not found"
        
        classes = send_button.get('class', [])
        assert 'min-h-[44px]' in classes, "Send button missing min-h-[44px]"
        assert 'min-w-[44px]' in classes, "Send button missing min-w-[44px]"
    
    def test_select_all_checkbox_has_minimum_size(self):
        """Select all checkbox should have min-h-[44px] and min-w-[44px]"""
        content = get_template_content()
        soup = BeautifulSoup(content, 'html.parser')
        
        select_all = soup.find('input', {'id': 'select-all-docs'})
        assert select_all is not None, "Select all checkbox not found"
        
        classes = select_all.get('class', [])
        assert 'min-h-[44px]' in classes, "Select all checkbox missing min-h-[44px]"
        assert 'min-w-[44px]' in classes, "Select all checkbox missing min-w-[44px]"
    
    def test_back_to_launcher_link_has_minimum_size(self):
        """Back to launcher link should have min-h-[44px] and min-w-[44px]"""
        content = get_template_content()
        soup = BeautifulSoup(content, 'html.parser')
        
        back_link = soup.find('a', {'class': 'back-to-launcher-btn'})
        assert back_link is not None, "Back to launcher link not found"
        
        classes = back_link.get('class', [])
        assert 'min-h-[44px]' in classes, "Back to launcher link missing min-h-[44px]"
        assert 'min-w-[44px]' in classes, "Back to launcher link missing min-w-[44px]"
    
    def test_sound_toggle_button_has_minimum_size(self):
        """Sound toggle button should have min-h-[44px] and min-w-[44px]"""
        content = get_template_content()
        soup = BeautifulSoup(content, 'html.parser')
        
        sound_toggle = soup.find('button', {'id': 'sound-toggle'})
        assert sound_toggle is not None, "Sound toggle button not found"
        
        classes = sound_toggle.get('class', [])
        assert 'min-h-[44px]' in classes, "Sound toggle button missing min-h-[44px]"
        assert 'min-w-[44px]' in classes, "Sound toggle button missing min-w-[44px]"
    
    def test_launcher_buttons_have_minimum_size(self):
        """Launcher buttons should have min-h-[44px] and min-w-[44px]"""
        content = get_launcher_content()
        
        # Check for both Legal Eagle and Ouija Board buttons
        assert 'min-h-[44px]' in content, "Launcher buttons missing min-h-[44px]"
        assert 'min-w-[44px]' in content, "Launcher buttons missing min-w-[44px]"
        
        # Count occurrences - should have at least 2 (one for each side)
        min_h_count = content.count('min-h-[44px]')
        min_w_count = content.count('min-w-[44px]')
        
        assert min_h_count >= 2, f"Expected at least 2 buttons with min-h-[44px], found {min_h_count}"
        assert min_w_count >= 2, f"Expected at least 2 buttons with min-w-[44px], found {min_w_count}"
    
    def test_dynamically_created_checkboxes_have_minimum_size(self):
        """Dynamically created document checkboxes should have min-h-[44px] and min-w-[44px]"""
        content = get_app_js_content()
        
        # Find the checkbox creation in refreshDocuments function
        checkbox_pattern = r'class="checkbox.*?doc-checkbox"'
        matches = re.findall(checkbox_pattern, content, re.DOTALL)
        
        assert len(matches) > 0, "No dynamically created checkboxes found"
        
        for match in matches:
            assert 'min-h-[44px]' in match, f"Dynamically created checkbox missing min-h-[44px]: {match}"
            assert 'min-w-[44px]' in match, f"Dynamically created checkbox missing min-w-[44px]: {match}"
    
    def test_dynamically_created_delete_buttons_have_minimum_size(self):
        """Dynamically created delete buttons should have min-h-[44px] and min-w-[44px]"""
        content = get_app_js_content()
        
        # Find the delete button creation in refreshDocuments function
        delete_button_pattern = r'onclick="deleteDocument.*?class="[^"]*btn[^"]*"'
        matches = re.findall(delete_button_pattern, content, re.DOTALL)
        
        assert len(matches) > 0, "No dynamically created delete buttons found"
        
        for match in matches:
            assert 'min-h-[44px]' in match, f"Delete button missing min-h-[44px]: {match}"
            assert 'min-w-[44px]' in match, f"Delete button missing min-w-[44px]: {match}"
    
    def test_error_dismiss_buttons_have_minimum_size(self):
        """Error dismiss buttons should have min-h-[44px] and min-w-[44px]"""
        content = get_app_js_content()
        
        # Find error dismiss buttons - look for the class attribute itself
        dismiss_pattern = r'class="error-dismiss-btn[^"]*"'
        matches = re.findall(dismiss_pattern, content, re.DOTALL)
        
        assert len(matches) > 0, "No error dismiss buttons found"
        
        for match in matches:
            assert 'min-h-[44px]' in match, f"Error dismiss button missing min-h-[44px]: {match}"
            assert 'min-w-[44px]' in match, f"Error dismiss button missing min-w-[44px]: {match}"
    
    def test_error_retry_buttons_have_minimum_size(self):
        """Error retry buttons should have min-h-[44px] and min-w-[44px]"""
        content = get_app_js_content()
        
        # Find error retry buttons - look for the class attribute itself
        retry_pattern = r'class="error-retry-btn[^"]*"'
        matches = re.findall(retry_pattern, content, re.DOTALL)
        
        assert len(matches) > 0, "No error retry buttons found"
        
        for match in matches:
            assert 'min-h-[44px]' in match, f"Error retry button missing min-h-[44px]: {match}"
            assert 'min-w-[44px]' in match, f"Error retry button missing min-w-[44px]: {match}"
    
    def test_modal_buttons_have_minimum_size(self):
        """Modal dialog buttons should have min-height: 44px and min-width: 44px"""
        content = get_app_js_content()
        
        # Find modal buttons with inline styles
        modal_button_pattern = r'modal-btn-(?:cancel|confirm).*?style="[^"]*"'
        matches = re.findall(modal_button_pattern, content, re.DOTALL)
        
        assert len(matches) >= 2, "Expected at least 2 modal buttons (cancel and confirm)"
        
        for match in matches:
            assert 'min-height: 44px' in match, f"Modal button missing min-height: 44px: {match}"
            assert 'min-width: 44px' in match, f"Modal button missing min-width: 44px: {match}"
    
    def test_upload_error_dismiss_button_has_minimum_size(self):
        """Upload error dismiss button should have min-h-[44px] and min-w-[44px]"""
        content = get_app_js_content()
        
        # Find the upload error dismiss button in showUploadError function
        # Look for the button with onclick="dismissUploadError"
        upload_error_pattern = r'onclick="dismissUploadError[^>]*class="[^"]*"'
        matches = re.findall(upload_error_pattern, content, re.DOTALL)
        
        assert len(matches) > 0, "No upload error dismiss button found"
        
        for match in matches:
            assert 'min-h-[44px]' in match, f"Upload error dismiss button missing min-h-[44px]: {match}"
            assert 'min-w-[44px]' in match, f"Upload error dismiss button missing min-w-[44px]: {match}"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
