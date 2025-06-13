"""
新版影片生成服務模組
重構版本，採用 OOP 設計模式與模組化架構
主要流程：場景循環處理 + 最終合成
"""

__version__ = "2.0.0"
__author__ = "Video Generation Team"

# 導出主要介面
from .main_pipeline import MainPipeline

__all__ = [
    'MainPipeline'
] 