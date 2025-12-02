"""
Tests for template rendering verification.

Validates that all templates render without errors and that Jinja2 variables
are properly interpolated.

Validates: Requirements 1.5
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from flask import Flask
from skeleton_core.app import create_app
from app_legal.config import Config as LegalConfig
from app_ghost.config import Config as GhostConfig
from launcher import landing_app


class TestLegalEagleTemplateRendering:
    """Test Legal Eagle template rendering"""
    
    def test_legal_eagle_template_renders_without_errors(self):
        """
        Verify that Legal Eagle template renders without errors.
        
        Validates: Requirements 1.5
        """
        app = create_app(LegalConfig)
        
        with app.test_client() as client:
            response = client.get('/')
            
            # Should return 200 OK
            assert response.status_code == 200, (
                "Legal Eagle template should render successfully"
            )
            
            # Should return HTML content
            assert response.content_type.startswith('text/html'), (
                "Legal Eagle should return HTML content"
            )
            
            # Should have content
            html = response.data.decode('utf-8')
            assert len(html) > 0, (
                "Legal Eagle template should have content"
            )
    
    def test_legal_eagle_app_name_interpolated(self):
        """
        Verify that app_name Jinja2 variable is properly interpolated.
        
        Validates: Requirements 1.5
        """
        app = create_app(LegalConfig)
        
        with app.test_client() as client:
            response = client.get('/')
            html = response.data.decode('utf-8')
            
            # Check that app name is in the HTML
            assert LegalConfig.APP_NAME in html, (
                f"Legal Eagle template should contain app name: {LegalConfig.APP_NAME}"
            )
            
            # Check that it's in the title tag
            assert f'<title>{LegalConfig.APP_NAME}</title>' in html, (
                "App name should be in title tag"
            )
    
    def test_legal_eagle_theme_interpolated(self):
        """
        Verify that theme Jinja2 variable is properly interpolated.
        
        Validates: Requirements 1.5
        """
        app = create_app(LegalConfig)
        
        with app.test_client() as client:
            response = client.get('/')
            html = response.data.decode('utf-8')
            
            # Check that theme is in the HTML
            assert LegalConfig.THEME_CSS in html, (
                f"Legal Eagle template should contain theme: {LegalConfig.THEME_CSS}"
            )
            
            # Check that it's in the body class
            assert f'theme-{LegalConfig.THEME_CSS}' in html, (
                "Theme should be in body class"
            )
    
    def test_legal_eagle_daisyui_theme_interpolated(self):
        """
        Verify that daisyui_theme Jinja2 variable is properly interpolated.
        
        Validates: Requirements 1.5
        """
        app = create_app(LegalConfig)
        
        with app.test_client() as client:
            response = client.get('/')
            html = response.data.decode('utf-8')
            
            # Check that DaisyUI theme is in the HTML
            assert LegalConfig.DAISYUI_THEME in html, (
                f"Legal Eagle template should contain DaisyUI theme: {LegalConfig.DAISYUI_THEME}"
            )
            
            # Check that it's in the data-theme attribute
            assert f'data-theme="{LegalConfig.DAISYUI_THEME}"' in html, (
                "DaisyUI theme should be in data-theme attribute"
            )
    
    def test_legal_eagle_daisyui_theme_config_interpolated(self):
        """
        Verify that daisyui_theme_config Jinja2 variable is properly interpolated.
        
        Validates: Requirements 1.5
        """
        app = create_app(LegalConfig)
        
        with app.test_client() as client:
            response = client.get('/')
            html = response.data.decode('utf-8')
            
            # Check that theme config colors are in the HTML
            assert LegalConfig.DAISYUI_THEME_CONFIG["legal-eagle"]["primary"] in html, (
                "Legal Eagle template should contain theme config primary color"
            )
    
    def test_legal_eagle_model_name_interpolated(self):
        """
        Verify that model_name Jinja2 variable is properly interpolated.
        
        Validates: Requirements 1.5
        """
        app = create_app(LegalConfig)
        
        with app.test_client() as client:
            response = client.get('/')
            html = response.data.decode('utf-8')
            
            # Check that model name or default is in the HTML
            assert 'Gemini AI' in html or 'gemini' in html.lower(), (
                "Legal Eagle template should contain model name"
            )
    
    def test_legal_eagle_url_for_static_files(self):
        """
        Verify that url_for() function works for static files.
        
        Validates: Requirements 1.5
        """
        app = create_app(LegalConfig)
        
        with app.test_client() as client:
            response = client.get('/')
            html = response.data.decode('utf-8')
            
            # Check that static file URLs are generated
            assert '/static/styles.css' in html, (
                "Template should generate URL for styles.css"
            )
            assert '/static/app.js' in html, (
                "Template should generate URL for app.js"
            )
            assert '/static/favicon-legal.svg' in html, (
                "Template should generate URL for legal favicon"
            )
    
    def test_legal_eagle_conditional_rendering(self):
        """
        Verify that Jinja2 conditionals work correctly for Legal Eagle theme.
        
        Validates: Requirements 1.5
        """
        app = create_app(LegalConfig)
        
        with app.test_client() as client:
            response = client.get('/')
            html = response.data.decode('utf-8')
            
            # Legal Eagle should show legal-specific content
            assert 'Case File Ingestion' in html, (
                "Legal Eagle should show legal-specific upload text"
            )
            assert 'Counsel Inquiry' in html, (
                "Legal Eagle should show legal-specific chat text"
            )
            assert 'Library' in html, (
                "Legal Eagle should show legal-specific library text"
            )
            
            # Legal Eagle should NOT show ghost-specific content
            assert 'Summon Document' not in html, (
                "Legal Eagle should not show ghost-specific upload text"
            )
            assert 'Commune with the Entity' not in html, (
                "Legal Eagle should not show ghost-specific chat text"
            )


class TestOuijaBoardTemplateRendering:
    """Test Ouija Board template rendering"""
    
    def test_ouija_board_template_renders_without_errors(self):
        """
        Verify that Ouija Board template renders without errors.
        
        Validates: Requirements 1.5
        """
        app = create_app(GhostConfig)
        
        with app.test_client() as client:
            response = client.get('/')
            
            # Should return 200 OK
            assert response.status_code == 200, (
                "Ouija Board template should render successfully"
            )
            
            # Should return HTML content
            assert response.content_type.startswith('text/html'), (
                "Ouija Board should return HTML content"
            )
            
            # Should have content
            html = response.data.decode('utf-8')
            assert len(html) > 0, (
                "Ouija Board template should have content"
            )
    
    def test_ouija_board_app_name_interpolated(self):
        """
        Verify that app_name Jinja2 variable is properly interpolated.
        
        Validates: Requirements 1.5
        """
        app = create_app(GhostConfig)
        
        with app.test_client() as client:
            response = client.get('/')
            html = response.data.decode('utf-8')
            
            # Check that app name is in the HTML
            assert GhostConfig.APP_NAME in html, (
                f"Ouija Board template should contain app name: {GhostConfig.APP_NAME}"
            )
            
            # Check that it's in the title tag
            assert f'<title>{GhostConfig.APP_NAME}</title>' in html, (
                "App name should be in title tag"
            )
    
    def test_ouija_board_theme_interpolated(self):
        """
        Verify that theme Jinja2 variable is properly interpolated.
        
        Validates: Requirements 1.5
        """
        app = create_app(GhostConfig)
        
        with app.test_client() as client:
            response = client.get('/')
            html = response.data.decode('utf-8')
            
            # Check that theme is in the HTML
            assert GhostConfig.THEME_CSS in html, (
                f"Ouija Board template should contain theme: {GhostConfig.THEME_CSS}"
            )
            
            # Check that it's in the body class
            assert f'theme-{GhostConfig.THEME_CSS}' in html, (
                "Theme should be in body class"
            )
    
    def test_ouija_board_daisyui_theme_interpolated(self):
        """
        Verify that daisyui_theme Jinja2 variable is properly interpolated.
        
        Validates: Requirements 1.5
        """
        app = create_app(GhostConfig)
        
        with app.test_client() as client:
            response = client.get('/')
            html = response.data.decode('utf-8')
            
            # Check that DaisyUI theme is in the HTML
            assert GhostConfig.DAISYUI_THEME in html, (
                f"Ouija Board template should contain DaisyUI theme: {GhostConfig.DAISYUI_THEME}"
            )
            
            # Check that it's in the data-theme attribute
            assert f'data-theme="{GhostConfig.DAISYUI_THEME}"' in html, (
                "DaisyUI theme should be in data-theme attribute"
            )
    
    def test_ouija_board_daisyui_theme_config_interpolated(self):
        """
        Verify that daisyui_theme_config Jinja2 variable is properly interpolated.
        
        Validates: Requirements 1.5
        """
        app = create_app(GhostConfig)
        
        with app.test_client() as client:
            response = client.get('/')
            html = response.data.decode('utf-8')
            
            # Check that theme config colors are in the HTML
            assert GhostConfig.DAISYUI_THEME_CONFIG["ouija-board"]["primary"] in html, (
                "Ouija Board template should contain theme config primary color"
            )
    
    def test_ouija_board_url_for_static_files(self):
        """
        Verify that url_for() function works for static files.
        
        Validates: Requirements 1.5
        """
        app = create_app(GhostConfig)
        
        with app.test_client() as client:
            response = client.get('/')
            html = response.data.decode('utf-8')
            
            # Check that static file URLs are generated
            assert '/static/styles.css' in html, (
                "Template should generate URL for styles.css"
            )
            assert '/static/app.js' in html, (
                "Template should generate URL for app.js"
            )
            assert '/static/favicon-ghost.svg' in html, (
                "Template should generate URL for ghost favicon"
            )
    
    def test_ouija_board_conditional_rendering(self):
        """
        Verify that Jinja2 conditionals work correctly for Ouija Board theme.
        
        Validates: Requirements 1.5
        """
        app = create_app(GhostConfig)
        
        with app.test_client() as client:
            response = client.get('/')
            html = response.data.decode('utf-8')
            
            # Ouija Board should show ghost-specific content
            assert 'Summon Document' in html, (
                "Ouija Board should show ghost-specific upload text"
            )
            assert 'Commune with the Entity' in html, (
                "Ouija Board should show ghost-specific chat text"
            )
            assert 'Summoned Texts' in html, (
                "Ouija Board should show ghost-specific library text"
            )
            
            # Ouija Board should NOT show legal-specific content
            assert 'Case File Ingestion' not in html, (
                "Ouija Board should not show legal-specific upload text"
            )
            assert 'Counsel Inquiry' not in html, (
                "Ouija Board should not show legal-specific chat text"
            )


class TestLauncherTemplateRendering:
    """Test launcher template rendering"""
    
    def test_launcher_template_renders_without_errors(self):
        """
        Verify that launcher template renders without errors.
        
        Validates: Requirements 1.5
        """
        with landing_app.test_client() as client:
            response = client.get('/')
            
            # Should return 200 OK
            assert response.status_code == 200, (
                "Launcher template should render successfully"
            )
            
            # Should return HTML content
            assert response.content_type.startswith('text/html'), (
                "Launcher should return HTML content"
            )
            
            # Should have content
            html = response.data.decode('utf-8')
            assert len(html) > 0, (
                "Launcher template should have content"
            )
    
    def test_launcher_contains_both_app_links(self):
        """
        Verify that launcher contains links to both apps.
        
        Validates: Requirements 1.5
        """
        with landing_app.test_client() as client:
            response = client.get('/')
            html = response.data.decode('utf-8')
            
            # Check for Legal Eagle link
            assert '/legal/' in html, (
                "Launcher should contain link to Legal Eagle"
            )
            assert 'Legal Eagle' in html, (
                "Launcher should contain Legal Eagle text"
            )
            
            # Check for Ouija Board link
            assert '/ghost/' in html, (
                "Launcher should contain link to Ouija Board"
            )
            assert 'Ouija Board' in html, (
                "Launcher should contain Ouija Board text"
            )
    
    def test_launcher_has_proper_html_structure(self):
        """
        Verify that launcher has proper HTML structure.
        
        Validates: Requirements 1.5
        """
        with landing_app.test_client() as client:
            response = client.get('/')
            html = response.data.decode('utf-8')
            
            # Check for essential HTML elements
            assert '<!DOCTYPE html>' in html, (
                "Launcher should have DOCTYPE declaration"
            )
            assert '<html' in html, (
                "Launcher should have html tag"
            )
            assert '<head>' in html, (
                "Launcher should have head tag"
            )
            assert '<body' in html, (
                "Launcher should have body tag"
            )
            assert '</html>' in html, (
                "Launcher should close html tag"
            )
    
    def test_launcher_includes_tailwind_and_daisyui(self):
        """
        Verify that launcher includes Tailwind CSS and DaisyUI.
        
        Validates: Requirements 1.5
        """
        with landing_app.test_client() as client:
            response = client.get('/')
            html = response.data.decode('utf-8')
            
            # Check for Tailwind CSS
            assert 'cdn.tailwindcss.com' in html, (
                "Launcher should include Tailwind CSS CDN"
            )
            
            # Check for DaisyUI
            assert 'daisyui' in html, (
                "Launcher should include DaisyUI CDN"
            )


class TestTemplateInheritance:
    """Test template inheritance and structure"""
    
    def test_legal_eagle_uses_base_template_structure(self):
        """
        Verify that Legal Eagle template has proper structure.
        
        Validates: Requirements 1.5
        """
        app = create_app(LegalConfig)
        
        with app.test_client() as client:
            response = client.get('/')
            html = response.data.decode('utf-8')
            
            # Check for essential sections
            assert '<header' in html, (
                "Template should have header section"
            )
            assert '<main' in html, (
                "Template should have main section"
            )
            assert '<footer' in html, (
                "Template should have footer section"
            )
    
    def test_ouija_board_uses_base_template_structure(self):
        """
        Verify that Ouija Board template has proper structure.
        
        Validates: Requirements 1.5
        """
        app = create_app(GhostConfig)
        
        with app.test_client() as client:
            response = client.get('/')
            html = response.data.decode('utf-8')
            
            # Check for essential sections
            assert '<header' in html, (
                "Template should have header section"
            )
            assert '<main' in html, (
                "Template should have main section"
            )
            assert '<footer' in html, (
                "Template should have footer section"
            )
    
    def test_templates_have_consistent_structure(self):
        """
        Verify that both app templates have consistent structure.
        
        Validates: Requirements 1.5
        """
        legal_app = create_app(LegalConfig)
        ghost_app = create_app(GhostConfig)
        
        with legal_app.test_client() as legal_client, \
             ghost_app.test_client() as ghost_client:
            
            legal_response = legal_client.get('/')
            ghost_response = ghost_client.get('/')
            
            legal_html = legal_response.data.decode('utf-8')
            ghost_html = ghost_response.data.decode('utf-8')
            
            # Both should have upload section
            assert 'upload-section' in legal_html, (
                "Legal Eagle should have upload section"
            )
            assert 'upload-section' in ghost_html, (
                "Ouija Board should have upload section"
            )
            
            # Both should have chat section
            assert 'chat-section' in legal_html, (
                "Legal Eagle should have chat section"
            )
            assert 'chat-section' in ghost_html, (
                "Ouija Board should have chat section"
            )
            
            # Both should have library section
            assert 'library-section' in legal_html, (
                "Legal Eagle should have library section"
            )
            assert 'library-section' in ghost_html, (
                "Ouija Board should have library section"
            )


class TestJinja2VariableInterpolation:
    """Test that all Jinja2 variables are properly interpolated"""
    
    def test_all_jinja2_variables_interpolated_legal(self):
        """
        Verify that all Jinja2 variables are interpolated in Legal Eagle.
        
        Validates: Requirements 1.5
        """
        app = create_app(LegalConfig)
        
        with app.test_client() as client:
            response = client.get('/')
            html = response.data.decode('utf-8')
            
            # Check that no Jinja2 template syntax remains in the output
            # Note: {{ and }} can appear in JavaScript/JSON, so we check for Jinja2 patterns
            import re
            
            # Check for unprocessed Jinja2 variable syntax (with spaces)
            assert not re.search(r'\{\{\s+\w+', html), (
                "Template should not contain uninterpolated {{ variable syntax"
            )
            
            # Check for unprocessed Jinja2 control structures
            assert '{%' not in html, (
                "Template should not contain unprocessed {% syntax"
            )
            assert '%}' not in html, (
                "Template should not contain unprocessed %} syntax"
            )
            
            # Verify that expected variables were interpolated
            assert LegalConfig.APP_NAME in html, (
                "app_name variable should be interpolated"
            )
            assert LegalConfig.THEME_CSS in html, (
                "theme variable should be interpolated"
            )
            assert LegalConfig.DAISYUI_THEME in html, (
                "daisyui_theme variable should be interpolated"
            )
    
    def test_all_jinja2_variables_interpolated_ghost(self):
        """
        Verify that all Jinja2 variables are interpolated in Ouija Board.
        
        Validates: Requirements 1.5
        """
        app = create_app(GhostConfig)
        
        with app.test_client() as client:
            response = client.get('/')
            html = response.data.decode('utf-8')
            
            # Check that no Jinja2 template syntax remains in the output
            # Note: {{ and }} can appear in JavaScript/JSON, so we check for Jinja2 patterns
            import re
            
            # Check for unprocessed Jinja2 variable syntax (with spaces)
            assert not re.search(r'\{\{\s+\w+', html), (
                "Template should not contain uninterpolated {{ variable syntax"
            )
            
            # Check for unprocessed Jinja2 control structures
            assert '{%' not in html, (
                "Template should not contain unprocessed {% syntax"
            )
            assert '%}' not in html, (
                "Template should not contain unprocessed %} syntax"
            )
            
            # Verify that expected variables were interpolated
            assert GhostConfig.APP_NAME in html, (
                "app_name variable should be interpolated"
            )
            assert GhostConfig.THEME_CSS in html, (
                "theme variable should be interpolated"
            )
            assert GhostConfig.DAISYUI_THEME in html, (
                "daisyui_theme variable should be interpolated"
            )


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
