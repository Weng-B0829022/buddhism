"""
基礎處理器抽象類
定義所有處理器的通用介面和行為
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict, Optional
import logging
import time


class ProcessorStatus(Enum):
    """處理器狀態枚舉"""
    PENDING = "pending"
    RUNNING = "running" 
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class BaseProcessor(ABC):
    """
    基礎處理器抽象類
    所有具體處理器都應該繼承此類
    """
    
    def __init__(self, name: str, config: Optional[Dict] = None):
        self.name = name
        self.config = config or {}
        self.status = ProcessorStatus.PENDING
        self.progress = 0.0
        self.error_message = ""
        self.start_time = None
        self.end_time = None
        self.logger = logging.getLogger(f"{__name__}.{name}")
        
    @abstractmethod
    def process(self, input_data: Any) -> Any:
        """
        抽象處理方法，子類必須實作
        
        Args:
            input_data: 輸入資料
            
        Returns:
            處理結果
        """
        pass
        
    
        
    def execute(self, input_data: Any) -> Any:
        """
        執行處理流程的主要方法
        包含狀態管理、錯誤處理、進度追蹤
        
        Args:
            input_data: 輸入資料
            
        Returns:
            處理結果
        """
        try:
            self.logger.info(f"開始執行處理器: {self.name}")
            self._set_status(ProcessorStatus.RUNNING)
            self.start_time = time.time()
            
            # 驗證輸入
            if not self.validate_input(input_data):
                raise ValueError(f"輸入資料驗證失敗: {self.name}")
            
            # 執行實際處理
            result = self.process(input_data)
            
            # 標記完成
            self._set_status(ProcessorStatus.COMPLETED)
            self.progress = 100.0
            self.end_time = time.time()
            
            self.logger.info(f"處理器執行完成: {self.name}, 耗時: {self.get_execution_time():.2f}秒")
            return result
            
        except Exception as e:
            self._handle_error(e)
            raise
            
    def _set_status(self, status: ProcessorStatus):
        """設定處理器狀態"""
        self.status = status
        self.logger.debug(f"處理器 {self.name} 狀態變更為: {status.value}")
        
    def _handle_error(self, error: Exception):
        """處理錯誤"""
        self.status = ProcessorStatus.FAILED
        self.error_message = str(error)
        self.end_time = time.time()
        self.logger.error(f"處理器 {self.name} 執行失敗: {error}")
        
    def get_status(self) -> Dict[str, Any]:
        """
        取得處理器狀態資訊
        
        Returns:
            包含狀態資訊的字典
        """
        return {
            "name": self.name,
            "status": self.status.value,
            "progress": self.progress,
            "error_message": self.error_message,
            "execution_time": self.get_execution_time()
        }
        
    def get_execution_time(self) -> float:
        """取得執行時間（秒）"""
        if self.start_time is None:
            return 0.0
        end_time = self.end_time or time.time()
        return end_time - self.start_time
        
    def update_progress(self, progress: float):
        """
        更新處理進度
        
        Args:
            progress: 進度百分比 (0-100)
        """
        self.progress = max(0.0, min(100.0, progress))
        self.logger.debug(f"處理器 {self.name} 進度更新: {self.progress:.1f}%")
        
    def cleanup(self):
        """
        清理資源，子類可以覆寫此方法
        """
        self.logger.debug(f"處理器 {self.name} 執行清理")
        pass
        
    def cancel(self):
        """
        取消處理，子類可以覆寫實作取消邏輯
        """
        self.status = ProcessorStatus.CANCELLED
        self.logger.info(f"處理器 {self.name} 已取消")
        
    def is_completed(self) -> bool:
        """檢查是否已完成"""
        return self.status == ProcessorStatus.COMPLETED
        
    def is_running(self) -> bool:
        """檢查是否正在執行"""
        return self.status == ProcessorStatus.RUNNING
        
    def has_failed(self) -> bool:
        """檢查是否執行失敗"""
        return self.status == ProcessorStatus.FAILED 