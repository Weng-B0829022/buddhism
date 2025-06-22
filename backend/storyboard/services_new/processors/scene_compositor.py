"""
場景合成器
負責合成單一場景的所有元素
"""

from typing import Any, Dict
from .base_processor import BaseProcessor
import os

class SceneCompositor(BaseProcessor):
    """
    場景合成器
    合成單一場景的所有元素（圖片、音訊、人偶）
    """
    
    def __init__(self, output_path: str, title: str):
        super().__init__("SceneCompositor", {})
        self.output_path = output_path
        self.title = title
        self.output_paths = []
    def process(self, input_data: Dict) -> str:
        #獲取mp3檔案
        audio_files = [f for f in os.listdir(self.output_path) if f.startswith(self.title) and f.endswith('.mp3')]
        #獲取圖片檔案
        image_files = [f for f in os.listdir(self.output_path) if f.startswith(self.title) and f.endswith('.png')]
        #獲取背景 將背景由素材庫複製到output_path 並讀取
        return  
        