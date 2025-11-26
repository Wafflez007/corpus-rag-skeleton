"""
Property-based tests for file upload validation.

Feature: ui-design-improvements, Property 2: File validation before upload
Validates: Requirements 5.4
"""

from hypothesis import given, strategies as st, settings, assume
import pytest


# Constants matching the JavaScript validation logic
ALLOWED_EXTENSIONS = ['.txt', '.pdf']
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB in bytes


class MockFile:
    """Mock file object for testing validation logic."""
    def __init__(self, name, size):
        self.name = name
        self.size = size


def validate_file_python(file):
    """
    Python implementation of the JavaScript validateFile() function.
    This mirrors the logic in skeleton_core/static/app.js
    """
    # File type validation
    file_name_lower = file.name.lower()
    has_valid_extension = any(file_name_lower.endswith(ext) for ext in ALLOWED_EXTENSIONS)
    
    if not has_valid_extension:
        return {'valid': False, 'error': 'Invalid file type'}
    
    # File size validation
    if file.size > MAX_FILE_SIZE:
        return {'valid': False, 'error': 'File too large'}
    
    # Empty file check
    if file.size == 0:
        return {'valid': False, 'error': 'File is empty'}
    
    # All validations passed
    return {'valid': True, 'error': None}


def test_valid_txt_file():
    """Test that valid .txt files pass validation."""
    file = MockFile('document.txt', 1024)
    result = validate_file_python(file)
    assert result['valid'] is True
    assert result['error'] is None


def test_valid_pdf_file():
    """Test that valid .pdf files pass validation."""
    file = MockFile('document.pdf', 1024)
    result = validate_file_python(file)
    assert result['valid'] is True
    assert result['error'] is None


def test_invalid_file_type():
    """Test that invalid file types are rejected."""
    invalid_files = [
        MockFile('document.docx', 1024),
        MockFile('image.jpg', 1024),
        MockFile('script.js', 1024),
        MockFile('data.csv', 1024),
    ]
    
    for file in invalid_files:
        result = validate_file_python(file)
        assert result['valid'] is False
        assert result['error'] is not None


def test_file_too_large():
    """Test that files exceeding size limit are rejected."""
    file = MockFile('large.pdf', MAX_FILE_SIZE + 1)
    result = validate_file_python(file)
    assert result['valid'] is False
    assert 'large' in result['error'].lower()


def test_empty_file():
    """Test that empty files are rejected."""
    file = MockFile('empty.txt', 0)
    result = validate_file_python(file)
    assert result['valid'] is False
    assert 'empty' in result['error'].lower()


def test_case_insensitive_extension():
    """Test that file extensions are case-insensitive."""
    files = [
        MockFile('document.TXT', 1024),
        MockFile('document.PDF', 1024),
        MockFile('document.Pdf', 1024),
        MockFile('document.TxT', 1024),
    ]
    
    for file in files:
        result = validate_file_python(file)
        assert result['valid'] is True, f"File {file.name} should be valid"


@settings(max_examples=100)
@given(
    file_name=st.text(min_size=1, max_size=50).filter(lambda x: '/' not in x and '\\' not in x),
    extension=st.sampled_from(['.txt', '.pdf', '.TXT', '.PDF', '.Txt', '.Pdf']),
    file_size=st.integers(min_value=1, max_value=MAX_FILE_SIZE)
)
def test_valid_files_always_pass(file_name, extension, file_size):
    """
    Feature: ui-design-improvements, Property 2: File validation before upload
    
    Property: For any file with a valid extension (.txt or .pdf, case-insensitive)
    and size between 1 byte and MAX_FILE_SIZE, the validation should pass.
    
    This property-based test generates random valid file configurations to ensure
    the validation logic correctly accepts all valid files.
    
    Validates: Requirements 5.4
    """
    # Create a valid file name with valid extension
    full_name = file_name + extension
    file = MockFile(full_name, file_size)
    
    result = validate_file_python(file)
    
    assert result['valid'] is True, (
        f"Valid file {full_name} with size {file_size} should pass validation"
    )
    assert result['error'] is None


@settings(max_examples=100)
@given(
    file_name=st.text(min_size=1, max_size=50).filter(lambda x: '/' not in x and '\\' not in x),
    extension=st.sampled_from(['.docx', '.jpg', '.png', '.exe', '.zip', '.csv', '.json', '.xml']),
    file_size=st.integers(min_value=1, max_value=MAX_FILE_SIZE)
)
def test_invalid_extensions_always_fail(file_name, extension, file_size):
    """
    Feature: ui-design-improvements, Property 2: File validation before upload
    
    Property: For any file with an invalid extension (not .txt or .pdf),
    the validation should fail with an appropriate error message.
    
    This property-based test generates random invalid file types to ensure
    the validation logic correctly rejects all unsupported formats.
    
    Validates: Requirements 5.4
    """
    full_name = file_name + extension
    file = MockFile(full_name, file_size)
    
    result = validate_file_python(file)
    
    assert result['valid'] is False, (
        f"Invalid file type {full_name} should fail validation"
    )
    assert result['error'] is not None
    assert 'type' in result['error'].lower() or 'invalid' in result['error'].lower()


@settings(max_examples=100)
@given(
    file_name=st.text(min_size=1, max_size=50).filter(lambda x: '/' not in x and '\\' not in x),
    extension=st.sampled_from(['.txt', '.pdf']),
    file_size=st.integers(min_value=MAX_FILE_SIZE + 1, max_value=MAX_FILE_SIZE * 2)
)
def test_oversized_files_always_fail(file_name, extension, file_size):
    """
    Feature: ui-design-improvements, Property 2: File validation before upload
    
    Property: For any file exceeding MAX_FILE_SIZE, regardless of valid extension,
    the validation should fail with a size-related error message.
    
    This property-based test generates random oversized files to ensure
    the validation logic correctly enforces size limits.
    
    Validates: Requirements 5.4
    """
    full_name = file_name + extension
    file = MockFile(full_name, file_size)
    
    result = validate_file_python(file)
    
    assert result['valid'] is False, (
        f"Oversized file {full_name} ({file_size} bytes) should fail validation"
    )
    assert result['error'] is not None
    assert 'large' in result['error'].lower() or 'size' in result['error'].lower()


@settings(max_examples=100)
@given(
    file_name=st.text(min_size=1, max_size=50).filter(lambda x: '/' not in x and '\\' not in x),
    extension=st.sampled_from(['.txt', '.pdf'])
)
def test_empty_files_always_fail(file_name, extension):
    """
    Feature: ui-design-improvements, Property 2: File validation before upload
    
    Property: For any file with size 0 bytes, regardless of valid extension,
    the validation should fail with an empty file error message.
    
    This property-based test generates random empty files to ensure
    the validation logic correctly rejects files with no content.
    
    Validates: Requirements 5.4
    """
    full_name = file_name + extension
    file = MockFile(full_name, 0)
    
    result = validate_file_python(file)
    
    assert result['valid'] is False, (
        f"Empty file {full_name} should fail validation"
    )
    assert result['error'] is not None
    assert 'empty' in result['error'].lower()


@settings(max_examples=100)
@given(
    file_name=st.text(min_size=1, max_size=50).filter(lambda x: '/' not in x and '\\' not in x),
    extension=st.sampled_from(['.txt', '.pdf', '.TXT', '.PDF']),
    file_size=st.integers(min_value=1, max_value=MAX_FILE_SIZE)
)
def test_validation_is_deterministic(file_name, extension, file_size):
    """
    Feature: ui-design-improvements, Property 2: File validation before upload
    
    Property: For any file, running validation multiple times should always
    produce the same result (validation is deterministic).
    
    This property-based test ensures validation logic is consistent and
    doesn't have any random or time-dependent behavior.
    
    Validates: Requirements 5.4
    """
    full_name = file_name + extension
    file = MockFile(full_name, file_size)
    
    # Run validation multiple times
    result1 = validate_file_python(file)
    result2 = validate_file_python(file)
    result3 = validate_file_python(file)
    
    # All results should be identical
    assert result1['valid'] == result2['valid'] == result3['valid'], (
        f"Validation should be deterministic for {full_name}"
    )
    assert result1['error'] == result2['error'] == result3['error']


@settings(max_examples=100)
@given(
    base_name=st.text(min_size=1, max_size=40).filter(lambda x: '/' not in x and '\\' not in x),
    extension=st.sampled_from(['.txt', '.pdf']),
    file_size=st.integers(min_value=1, max_value=MAX_FILE_SIZE)
)
def test_file_names_with_multiple_dots(base_name, extension, file_size):
    """
    Feature: ui-design-improvements, Property 2: File validation before upload
    
    Property: For any file name containing multiple dots (e.g., "my.document.txt"),
    the validation should correctly identify the extension and validate accordingly.
    
    This property-based test ensures the validation logic handles complex
    file names correctly.
    
    Validates: Requirements 5.4
    """
    # Add extra dots to the base name
    file_name_with_dots = base_name + '.backup' + extension
    file = MockFile(file_name_with_dots, file_size)
    
    result = validate_file_python(file)
    
    # Should be valid because it ends with a valid extension
    assert result['valid'] is True, (
        f"File {file_name_with_dots} with valid extension should pass validation"
    )


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
