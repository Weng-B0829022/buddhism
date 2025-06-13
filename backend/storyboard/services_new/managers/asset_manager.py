"""
資產管理器
負責管理檔案路徑、創建目錄結構、註冊資產
"""

import os
import logging
from typing import Dict, List, Optional


class AssetManager:
    """
    資產管理器
    管理工作目錄結構和資產檔案
    """
    
    def __init__(self, base_path: str, random_id: str):
        self.base_path = base_path
        self.random_id = random_id
        self.work_dir = os.path.join(base_path, random_id)
        self.asset_registry = {}
        self.logger = logging.getLogger(__name__)
        
    def create_directory_structure(self):
        """創建工作目錄結構"""
        directories = [
            self.work_dir,
            os.path.join(self.work_dir, 'images'),
            os.path.join(self.work_dir, 'audio'),
            os.path.join(self.work_dir, 'characters'),
            os.path.join(self.work_dir, 'scenes'),
            os.path.join(self.work_dir, 'temp')
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            self.logger.debug(f"創建目錄: {directory}")
    
    def register_asset(self, asset_type: str, asset_id: str, file_path: str):
        """註冊資產"""
        if asset_type not in self.asset_registry:
            self.asset_registry[asset_type] = {}
        self.asset_registry[asset_type][asset_id] = file_path
        self.logger.debug(f"註冊資產: {asset_type}/{asset_id} -> {file_path}")
    
    def get_asset_path(self, asset_type: str, asset_id: str) -> Optional[str]:
        """取得資產路徑"""
        return self.asset_registry.get(asset_type, {}).get(asset_id)
    
    def cleanup_temp_files(self):
        """清理暫存檔案"""
        temp_dir = os.path.join(self.work_dir, 'temp')
        if os.path.exists(temp_dir):
            # TODO: 實際的清理邏輯
            self.logger.info(f"清理暫存目錄: {temp_dir}")
    
    def get_scene_directory(self, scene_index: int) -> str:
        """取得場景目錄路徑"""
        return os.path.join(self.work_dir, 'scenes', f'scene_{scene_index:03d}')
    
    def get_image_path(self, scene_index: int) -> str:
        """取得圖片檔案路徑"""
        return os.path.join(self.work_dir, 'images', f'scene_{scene_index:03d}.png')
    
    def get_audio_path(self, scene_index: int) -> str:
        """取得音訊檔案路徑"""
        return os.path.join(self.work_dir, 'audio', f'scene_{scene_index:03d}.wav')
    
    def get_character_path(self, scene_index: int) -> str:
        """取得人偶檔案路徑"""
        return os.path.join(self.work_dir, 'characters', f'scene_{scene_index:03d}.mp4') 