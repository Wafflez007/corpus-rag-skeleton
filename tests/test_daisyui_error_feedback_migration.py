"""
Tests to verify error handling and feedback components use DaisyUI.

Feature: tailwind-daisyui-integration
Task: 14. Migrate error handling and feedback components
Validates: Requirements 6.4, 7.4
"""

import re


def get_app_js_content():
    """Read the app.js file content."""
    with open('skeleton_core/static/app.js', 'r', encoding='utf-8') as f:
        return f.read()


class TestDaisyUIErrorFeedbackMigration:
    """Test that error handling and feedback components use DaisyUI."""
    
    def test_loading_indicator_uses_daisyui_loading_component(self):
        """Loading indicators should use DaisyUI loading component."""
        content = get_app_js_content()
        
        # Find the showLoading function
        show_loading_match = re.search(
            r'function showLoading\(\).*?return id;',
            content,
            re.DOTALL
        )
        
        assert show_loading_match, "showLoading function not found"
        show_loading_code = show_loading_match.group(0)
        
        # Should use DaisyUI loading component
        assert 'loading loading-dots' in show_loading_code, (
            "Loading indicator should use DaisyUI 'loading loading-dots' class"
        )
        assert 'loading-sm' in show_loading_code, (
            "Loading indicator should use 'loading-sm' size class"
        )
    
    def test_upload_success_uses_daisyui_alert(self):
        """Upload success messages should use DaisyUI alert component."""
        content = get_app_js_content()
        
        # Find the showUploadSuccess function
        show_success_match = re.search(
            r'function showUploadSuccess\(.*?\n\}',
            content,
            re.DOTALL
        )
        
        assert show_success_match, "showUploadSuccess function not found"
        show_success_code = show_success_match.group(0)
        
        # Should use DaisyUI alert-success component
        assert 'alert alert-success' in show_success_code, (
            "Upload success should use DaisyUI 'alert alert-success' class"
        )
        assert 'role="alert"' in show_success_code, (
            "Upload success should have role='alert' for accessibility"
        )
    
    def test_upload_error_uses_daisyui_alert(self):
        """Upload error messages should use DaisyUI alert component."""
        content = get_app_js_content()
        
        # Find the showUploadError function
        show_error_match = re.search(
            r'function showUploadError\(.*?\n\}',
            content,
            re.DOTALL
        )
        
        assert show_error_match, "showUploadError function not found"
        show_error_code = show_error_match.group(0)
        
        # Should use DaisyUI alert-error component
        assert 'alert alert-error' in show_error_code, (
            "Upload error should use DaisyUI 'alert alert-error' class"
        )
        assert 'role="alert"' in show_error_code, (
            "Upload error should have role='alert' for accessibility"
        )
    
    def test_upload_error_dismiss_button_uses_daisyui(self):
        """Upload error dismiss button should use DaisyUI button component."""
        content = get_app_js_content()
        
        # Find the showUploadError function
        show_error_match = re.search(
            r'function showUploadError\(.*?\n\}',
            content,
            re.DOTALL
        )
        
        assert show_error_match, "showUploadError function not found"
        show_error_code = show_error_match.group(0)
        
        # Should use DaisyUI button classes
        assert 'btn btn-sm btn-ghost' in show_error_code, (
            "Upload error dismiss button should use DaisyUI 'btn btn-sm btn-ghost' classes"
        )
        assert 'min-h-[44px] min-w-[44px]' in show_error_code, (
            "Upload error dismiss button should meet minimum touch target size"
        )
    
    def test_general_error_uses_daisyui_alert(self):
        """General error messages should use DaisyUI alert component."""
        content = get_app_js_content()
        
        # Find the showError function
        show_error_match = re.search(
            r'function showError\(.*?return errorDiv;',
            content,
            re.DOTALL
        )
        
        assert show_error_match, "showError function not found"
        show_error_code = show_error_match.group(0)
        
        # Should use DaisyUI alert-error component
        assert 'alert alert-error' in show_error_code, (
            "General error should use DaisyUI 'alert alert-error' class"
        )
        assert 'role="alert"' in show_error_code or 'setAttribute' in show_error_code, (
            "General error should have role='alert' for accessibility"
        )
    
    def test_error_retry_button_uses_daisyui(self):
        """Error retry button should use DaisyUI button component."""
        content = get_app_js_content()
        
        # Find the showError function
        show_error_match = re.search(
            r'function showError\(.*?return errorDiv;',
            content,
            re.DOTALL
        )
        
        assert show_error_match, "showError function not found"
        show_error_code = show_error_match.group(0)
        
        # Should use DaisyUI button classes for retry button
        assert 'btn btn-sm btn-error' in show_error_code, (
            "Error retry button should use DaisyUI 'btn btn-sm btn-error' classes"
        )
        assert 'error-retry-btn' in show_error_code, (
            "Error retry button should have 'error-retry-btn' class"
        )
    
    def test_error_dismiss_button_uses_daisyui(self):
        """Error dismiss button should use DaisyUI button component."""
        content = get_app_js_content()
        
        # Find the showError function
        show_error_match = re.search(
            r'function showError\(.*?return errorDiv;',
            content,
            re.DOTALL
        )
        
        assert show_error_match, "showError function not found"
        show_error_code = show_error_match.group(0)
        
        # Should use DaisyUI button classes for dismiss button
        assert 'btn btn-sm btn-ghost' in show_error_code, (
            "Error dismiss button should use DaisyUI 'btn btn-sm btn-ghost' classes"
        )
        assert 'error-dismiss-btn' in show_error_code, (
            "Error dismiss button should have 'error-dismiss-btn' class"
        )
    
    def test_all_buttons_meet_touch_target_size(self):
        """All error and feedback buttons should meet minimum touch target size."""
        content = get_app_js_content()
        
        # Find all button elements in error/feedback functions
        button_patterns = [
            r'function showUploadError\(.*?\n\}',
            r'function showError\(.*?return errorDiv;'
        ]
        
        for pattern in button_patterns:
            match = re.search(pattern, content, re.DOTALL)
            if match:
                code = match.group(0)
                # Find all button elements
                buttons = re.findall(r'<button[^>]*>', code)
                for button in buttons:
                    assert 'min-h-[44px]' in button, (
                        f"Button should have min-h-[44px]: {button}"
                    )
                    assert 'min-w-[44px]' in button, (
                        f"Button should have min-w-[44px]: {button}"
                    )
    
    def test_no_custom_error_styling_remains(self):
        """Custom error styling should be replaced with DaisyUI classes."""
        content = get_app_js_content()
        
        # Find error-related functions
        error_functions = [
            'showUploadError',
            'showError',
            'showUploadSuccess'
        ]
        
        for func_name in error_functions:
            func_match = re.search(
                rf'function {func_name}\(.*?\n\}}',
                content,
                re.DOTALL
            )
            
            if func_match:
                func_code = func_match.group(0)
                
                # Should not have inline background/border styles for alerts
                # (DaisyUI handles this)
                if 'alert alert-' in func_code:
                    # Check that we're not using custom inline styles for the alert itself
                    # (some inline styles are OK for animations, but not for colors/borders)
                    alert_divs = re.findall(r'<div class="alert alert-[^"]*"[^>]*>', func_code)
                    for alert_div in alert_divs:
                        # Should not have inline background or border styles
                        assert 'style="background:' not in alert_div, (
                            f"Alert should use DaisyUI styling, not inline background: {alert_div}"
                        )
                        assert 'style="border:' not in alert_div, (
                            f"Alert should use DaisyUI styling, not inline border: {alert_div}"
                        )
    
    def test_loading_indicator_simplified(self):
        """Loading indicator should be simplified to use DaisyUI component."""
        content = get_app_js_content()
        
        # Find the showLoading function
        show_loading_match = re.search(
            r'function showLoading\(\).*?return id;',
            content,
            re.DOTALL
        )
        
        assert show_loading_match, "showLoading function not found"
        show_loading_code = show_loading_match.group(0)
        
        # Should NOT have custom animated dots (DaisyUI handles this)
        assert 'animate-bounce' not in show_loading_code, (
            "Loading indicator should use DaisyUI component, not custom animated dots"
        )
        
        # Should use DaisyUI loading component
        assert '<span class="loading loading-dots' in show_loading_code, (
            "Loading indicator should use DaisyUI <span class='loading loading-dots'>"
        )


if __name__ == '__main__':
    import pytest
    pytest.main([__file__, '-v'])
