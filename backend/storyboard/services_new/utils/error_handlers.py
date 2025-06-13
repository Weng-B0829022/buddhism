"""
錯誤處理工具
提供統一的錯誤處理和重試機制
"""

import logging
import time
from typing import Callable, Any, Optional, Dict
from functools import wraps


class ErrorHandler:
    """
    錯誤處理工具類
    """
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
    
    @staticmethod
    def retry_on_failure(max_retries: int = 3, delay: float = 1.0):
        """
        重試裝飾器
        
        Args:
            max_retries: 最大重試次數
            delay: 重試間隔（秒）
        """
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs) -> Any:
                last_exception = None
                
                for attempt in range(max_retries + 1):
                    try:
                        return func(*args, **kwargs)
                    except Exception as e:
                        last_exception = e
                        if attempt < max_retries:
                            logging.warning(f"函數 {func.__name__} 第 {attempt + 1} 次執行失敗，將重試: {e}")
                            time.sleep(delay)
                        else:
                            logging.error(f"函數 {func.__name__} 執行失敗，已達最大重試次數: {e}")
                
                raise last_exception
            return wrapper
        return decorator
    
    @staticmethod
    def safe_execute(func: Callable, default_value: Any = None, 
                    log_errors: bool = True) -> Any:
        """
        安全執行函數
        
        Args:
            func: 要執行的函數
            default_value: 失敗時的預設值
            log_errors: 是否記錄錯誤
            
        Returns:
            函數執行結果或預設值
        """
        try:
            return func()
        except Exception as e:
            if log_errors:
                logging.error(f"安全執行失敗: {e}")
            return default_value
    
    def handle_processor_error(self, processor_name: str, error: Exception) -> Dict[str, Any]:
        """
        處理處理器錯誤
        
        Args:
            processor_name: 處理器名稱
            error: 錯誤物件
            
        Returns:
            錯誤資訊字典
        """
        error_info = {
            'processor': processor_name,
            'error_type': type(error).__name__,
            'error_message': str(error),
            'timestamp': time.time(),
            'recoverable': self._is_recoverable_error(error)
        }
        
        self.logger.error(f"處理器 {processor_name} 發生錯誤: {error_info}")
        return error_info
    
    def _is_recoverable_error(self, error: Exception) -> bool:
        """
        判斷錯誤是否可恢復
        
        Args:
            error: 錯誤物件
            
        Returns:
            bool: 是否可恢復
        """
        # 網路相關錯誤通常可重試
        recoverable_errors = [
            'ConnectionError',
            'TimeoutError',
            'RequestException'
        ]
        
        return type(error).__name__ in recoverable_errors
    
    def create_error_report(self, errors: list) -> Dict[str, Any]:
        """
        創建錯誤報告
        
        Args:
            errors: 錯誤列表
            
        Returns:
            錯誤報告
        """
        return {
            'total_errors': len(errors),
            'error_summary': [
                {
                    'processor': error.get('processor'),
                    'error_type': error.get('error_type'),
                    'recoverable': error.get('recoverable')
                }
                for error in errors
            ],
            'generated_at': time.time()
        } 