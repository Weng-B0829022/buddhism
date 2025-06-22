"""
人偶處理器
負責基於音訊生成對應的人偶動畫
"""

from typing import Any, Dict
from .base_processor import BaseProcessor


class CharacterProcessor(BaseProcessor):
    """
    人偶處理器
    基於音訊生成對應的人偶動畫
    依賴: AudioProcessor 必須先完成
    """
    
    def __init__(self, config: Dict = None):
        super().__init__("CharacterProcessor", config)

    def process(self, input_data: Dict) -> str:
        """
        處理人偶生成
        
        Args:
            input_data: 包含音訊路徑等資料的字典
            
        Returns:
            str: 人偶動畫檔案路徑
        """

        return character_path 