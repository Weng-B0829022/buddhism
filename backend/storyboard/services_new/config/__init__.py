"""
配置模組 - 管理系統配置和常數
"""

from .settings import get_default_config, load_config
from .constants import *

__all__ = [
    'get_default_config',
    'load_config',
    'DEFAULT_OUTPUT_PATH',
    'SUPPORTED_IMAGE_FORMATS',
    'SUPPORTED_AUDIO_FORMATS',
    'SUPPORTED_VIDEO_FORMATS'
] 