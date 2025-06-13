"""
配置設定
提供系統預設配置和配置載入功能
"""

import os
from typing import Dict, Any
from django.conf import settings


def get_default_config() -> Dict[str, Any]:
    """
    取得預設配置
    
    Returns:
        Dict: 預設配置字典
    """
    return {
        # 基本設定
        'output_path': getattr(settings, 'MEDIA_ROOT', '/tmp/generated'),
        'temp_dir': '/tmp/video_generation',
        'max_parallel_tasks': 2,
        
        # 處理器配置
        'image_processor': {
            'timeout': 300,  # 5分鐘
            'max_retries': 3,
            'quality': 'high'
        },
        'audio_processor': {
            'timeout': 180,  # 3分鐘
            'max_retries': 3,
            'sample_rate': 44100
        },
        'character_processor': {
            'timeout': 600,  # 10分鐘
            'max_retries': 2,
            'quality': 'medium'
        },
        'scene_compositor': {
            'timeout': 300,  # 5分鐘
            'max_retries': 2,
            'output_format': 'mp4'
        },
        'final_compositor': {
            'timeout': 900,  # 15分鐘
            'max_retries': 1,
            'output_format': 'mp4',
            'logo_path': None,
            'watermark': None
        },
        
        # 最終合成配置
        'final_composition': {
            'add_logo': False,
            'add_watermark': False,
            'intro_duration': 0,
            'outro_duration': 0
        },
        
        # 日誌配置
        'logging': {
            'level': 'INFO',
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        }
    }


def load_config(config_path: str = None) -> Dict[str, Any]:
    """
    載入配置檔案
    
    Args:
        config_path: 配置檔案路徑
        
    Returns:
        Dict: 配置字典
    """
    # 先取得預設配置
    config = get_default_config()
    
    # TODO: 實際的配置檔案載入邏輯
    if config_path and os.path.exists(config_path):
        # 載入外部配置檔案並合併
        pass
    
    # 環境變數覆蓋
    config = _apply_env_overrides(config)
    
    return config


def _apply_env_overrides(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    套用環境變數覆蓋
    
    Args:
        config: 原始配置
        
    Returns:
        Dict: 更新後的配置
    """
    # 從環境變數覆蓋設定
    if 'VIDEO_OUTPUT_PATH' in os.environ:
        config['output_path'] = os.environ['VIDEO_OUTPUT_PATH']
    
    if 'VIDEO_TEMP_DIR' in os.environ:
        config['temp_dir'] = os.environ['VIDEO_TEMP_DIR']
    
    if 'MAX_PARALLEL_TASKS' in os.environ:
        try:
            config['max_parallel_tasks'] = int(os.environ['MAX_PARALLEL_TASKS'])
        except ValueError:
            pass
    
    return config


def validate_config(config: Dict[str, Any]) -> bool:
    """
    驗證配置有效性
    
    Args:
        config: 配置字典
        
    Returns:
        bool: 驗證結果
    """
    required_keys = ['output_path', 'temp_dir']
    
    for key in required_keys:
        if key not in config:
            return False
    
    # 檢查路徑是否有效
    try:
        os.makedirs(config['output_path'], exist_ok=True)
        os.makedirs(config['temp_dir'], exist_ok=True)
    except Exception:
        return False
    
    return True 