"""
檔案操作工具
提供通用的檔案處理功能
"""

import os
import shutil
import logging
from typing import List, Optional


class FileOperations:
    """
    檔案操作工具類
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    @staticmethod
    def ensure_directory(directory_path: str) -> bool:
        """確保目錄存在"""
        try:
            os.makedirs(directory_path, exist_ok=True)
            return True
        except Exception as e:
            logging.error(f"創建目錄失敗: {directory_path}, 錯誤: {e}")
            return False
    
    @staticmethod
    def copy_file(source: str, destination: str) -> bool:
        """複製檔案"""
        try:
            shutil.copy2(source, destination)
            return True
        except Exception as e:
            logging.error(f"複製檔案失敗: {source} -> {destination}, 錯誤: {e}")
            return False
    
    @staticmethod
    def move_file(source: str, destination: str) -> bool:
        """移動檔案"""
        try:
            shutil.move(source, destination)
            return True
        except Exception as e:
            logging.error(f"移動檔案失敗: {source} -> {destination}, 錯誤: {e}")
            return False
    
    @staticmethod
    def delete_file(file_path: str) -> bool:
        """刪除檔案"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
            return True
        except Exception as e:
            logging.error(f"刪除檔案失敗: {file_path}, 錯誤: {e}")
            return False
    
    @staticmethod
    def delete_directory(directory_path: str) -> bool:
        """刪除目錄"""
        try:
            if os.path.exists(directory_path):
                shutil.rmtree(directory_path)
            return True
        except Exception as e:
            logging.error(f"刪除目錄失敗: {directory_path}, 錯誤: {e}")
            return False
    
    @staticmethod
    def get_file_size(file_path: str) -> int:
        """取得檔案大小"""
        try:
            return os.path.getsize(file_path)
        except Exception:
            return 0
    
    @staticmethod
    def list_files(directory_path: str, extension: Optional[str] = None) -> List[str]:
        """列出目錄中的檔案"""
        try:
            files = []
            for file in os.listdir(directory_path):
                file_path = os.path.join(directory_path, file)
                if os.path.isfile(file_path):
                    if extension is None or file.endswith(extension):
                        files.append(file_path)
            return files
        except Exception as e:
            logging.error(f"列出檔案失敗: {directory_path}, 錯誤: {e}")
            return []
    
    @staticmethod
    def file_exists(file_path: str) -> bool:
        """檢查檔案是否存在"""
        return os.path.exists(file_path) and os.path.isfile(file_path)
    
    @staticmethod
    def directory_exists(directory_path: str) -> bool:
        """檢查目錄是否存在"""
        return os.path.exists(directory_path) and os.path.isdir(directory_path) 