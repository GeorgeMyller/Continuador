"""
Test Helper Utilities
Provides utilities for safe testing in CI/headless environments
"""

import os
from typing import Any


def is_test_environment() -> bool:
    """
    Check if we're running in a test/CI environment where GUI libraries might not be available
    """
    return (
        os.environ.get('CI_ENVIRONMENT') == 'true'
        or os.environ.get('HEADLESS_MODE') == 'true'
        or os.environ.get('CI') == 'true'
        or os.environ.get('GITHUB_ACTIONS') == 'true'
        or 'pytest' in str(os.environ.get('_', ''))
    )


def safe_import(module_name: str, mock_class: Any = None) -> Any:
    """
    Safely import a module, returning a mock if in test environment or import fails
    """
    if is_test_environment():
        import unittest.mock as mock
        return mock_class or mock.MagicMock()
    
    try:
        if module_name == 'tkinter':
            import tkinter
            return tkinter
        elif module_name == 'tkinter.ttk':
            from tkinter import ttk
            return ttk
        elif module_name == 'pyautogui':
            import pyautogui
            return pyautogui
        elif module_name == 'cv2':
            import cv2
            return cv2
        else:
            return __import__(module_name)
    except ImportError:
        import unittest.mock as mock
        return mock_class or mock.MagicMock()