"""
圖片處理器
負責下載/生成場景圖片
"""

import os
import re
import base64
import requests
from typing import Any, Dict, List, Tuple, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from .base_processor import BaseProcessor


class ImageProcessor(BaseProcessor):
    """
    圖片處理器
    根據場景文字生成/下載對應的圖片
    """
    
    def __init__(self, image_urls: List[str], output_path: str, title: str):
        super().__init__("ImageProcessor")
        self.image_urls = image_urls
        self.output_path = output_path
        self.title = title
    
    def update_progress(self, progress: float):
        """更新處理進度"""
        self.progress = progress
        self.logger.debug(f"圖片處理進度: {progress:.1f}%")

    def _download_single_image(self, idx: int, image_url: str, safe_title: str) -> Optional[str]:
        """
        下載單個圖片
        
        Args:
            idx: 圖片索引
            image_url: 圖片URL
            safe_title: 安全的標題名稱
            
        Returns:
            Optional[str]: 成功保存的圖片路徑，失敗則返回 None
        """
        if not image_url:
            return None
            
        try:
            self.logger.info(f"開始下載第 {idx + 1} 張圖片")
            
            # 檢查是否為 base64 圖片
            if image_url.startswith('data:image'):
                # 直接從 base64 字符串中提取圖片數據
                image_data = image_url.split(',')[1]
                image_content = base64.b64decode(image_data)
            else:
                # 下載圖片
                image_response = requests.get(image_url, timeout=30)
                if image_response.status_code != 200:
                    self.logger.warning(f"下載圖片失敗: {image_url}")
                    return None
                image_content = image_response.content

            # 生成圖片檔名
            image_filename = f'{safe_title}_{idx+1}.png'
            image_path = os.path.join(self.output_path, image_filename)
            
            # 保存圖片
            with open(image_path, 'wb') as f:
                f.write(image_content)
            
            self.logger.info(f"成功保存圖片: {image_path}")
            return image_path
            
        except Exception as e:
            self.logger.error(f"處理第 {idx + 1} 張圖片時發生錯誤: {str(e)}")
            return None

    def process(self) -> List[str]:
        """
        使用並發方式處理圖片下載和保存
        
        Returns:
            List[str]: 已保存的圖片檔案路徑列表
        """
        # 確保輸出目錄存在
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)
            
        image_paths = []
        safe_title = re.sub(r'[^\w\-_\. ]', '_', self.title)
        
        # 過濾掉空的 URL
        valid_downloads = [(idx, url) for idx, url in enumerate(self.image_urls) if url]
        
        if not valid_downloads:
            self.logger.warning("沒有有效的圖片 URL 需要下載")
            return []
        
        self.logger.info(f"開始並發下載 {len(valid_downloads)} 張圖片")
        
        # 使用線程池並發下載
        max_workers = min(len(valid_downloads), 5)  # 最多5個並發連接
        completed_count = 0
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # 提交所有下載任務
            future_to_idx = {
                executor.submit(self._download_single_image, idx, url, safe_title): idx 
                for idx, url in valid_downloads
            }
            
            # 處理完成的任務
            for future in as_completed(future_to_idx):
                idx = future_to_idx[future]
                completed_count += 1
                
                try:
                    image_path = future.result()
                    if image_path:
                        image_paths.append(image_path)
                    
                    # 更新進度
                    progress = (completed_count / len(valid_downloads)) * 100
                    self.update_progress(progress)
                    
                except Exception as e:
                    self.logger.error(f"下載任務執行失敗 (索引 {idx}): {str(e)}")
        
        # 按照原始索引順序排序結果
        image_paths.sort()
        
        self.logger.info(f"完成所有圖片處理，共成功下載 {len(image_paths)} 張圖片")
        return image_paths