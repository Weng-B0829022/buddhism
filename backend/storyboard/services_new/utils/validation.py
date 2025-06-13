"""
資料驗證工具
提供分鏡稿資料驗證功能
"""

from typing import Any, Dict, List


def validate_storyboard_data(data: Any) -> bool:
    """
    驗證分鏡稿資料格式
    
    Args:
        data: 待驗證的分鏡稿資料
        
    Returns:
        bool: 驗證結果
    """
    if not isinstance(data, dict):
        return False
    
    # 檢查必要欄位
    required_fields = ['storyboard', 'title']
    if not all(field in data for field in required_fields):
        return False
    
    # 檢查分鏡稿是否為列表
    storyboard = data.get('storyboard', [])
    if not isinstance(storyboard, list):
        return False
    
    # 檢查每個場景的格式
    for scene in storyboard:
        if not validate_scene_data(scene):
            return False
    
    return True


def validate_scene_data(scene: Any) -> bool:
    """
    驗證單一場景資料
    
    Args:
        scene: 場景資料
        
    Returns:
        bool: 驗證結果
    """
    if not isinstance(scene, dict):
        return False
    
    # 檢查場景必要欄位
    required_fields = ['text']  # 至少需要文字內容
    return all(field in scene for field in required_fields)


def validate_config_data(config: Any) -> bool:
    """
    驗證配置資料
    
    Args:
        config: 配置資料
        
    Returns:
        bool: 驗證結果
    """
    if not isinstance(config, dict):
        return False
    
    # TODO: 添加配置驗證邏輯
    return True


def validate_file_path(file_path: str) -> bool:
    """
    驗證檔案路徑格式
    
    Args:
        file_path: 檔案路徑
        
    Returns:
        bool: 驗證結果
    """
    if not isinstance(file_path, str) or not file_path.strip():
        return False
    
    # TODO: 添加更詳細的路徑驗證邏輯
    return True 