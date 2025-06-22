"""
聲音處理器
負責根據場景文字生成語音
"""

from typing import Any, Dict, List
from .base_processor import BaseProcessor
import os
import re
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed


class AudioProcessor(BaseProcessor):
    """
    聲音處理器
    使用 ElevenLabs API 生成語音檔案（用 requests 呼叫）
    """
    
    def __init__(self,audio_description: List[str], output_path: str, title: str):
        super().__init__("AudioProcessor")
        self.api_key = 'sk_c6c66e47cbdab456ddebb493e348f0e6df4c82e509ffaa5f'
        self.voice_id = '21m00Tcm4TlvDq8ikWAM' # Antoni 預設 voice_id
        self.model_id = 'eleven_multilingual_v2'
        self.output_path = output_path
        self.base_url = 'https://api.elevenlabs.io/v1'
        self.audio_description = audio_description
        self.title = title
        self.max_concurrency = 2

    def _generate_single_audio(self, text: str, scene_index: int, safe_title: str) -> str:
        """
        生成單個場景的語音檔案（用 ElevenLabs API）
        可使用 self.max_concurrency 控制最大併發數。
        """
        try:
            os.makedirs(self.output_path, exist_ok=True)
            # 音檔名稱為 {title}_1.mp3 ~ {title}_N.mp3
            filename = f"{self.title}_{scene_index+1}.mp3"
            output_path = os.path.join(self.output_path, filename)

            url = f"{self.base_url}/text-to-speech/{self.voice_id}"
            headers = {
                'Content-Type': 'application/json',
                'xi-api-key': self.api_key
            }
            payload = {
                "text": text,
                "model_id": self.model_id,
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.5
                }
            }
            response = requests.post(url, headers=headers, json=payload, stream=True)
            if response.status_code != 200:
                self.logger.error(f"ElevenLabs API 回應錯誤: {response.status_code} {response.text}")
                return None
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            self.logger.info(f"成功生成場景 {scene_index} 的語音檔案: {filename}")
            return output_path
        except Exception as e:
            self.logger.error(f"生成場景 {scene_index} 語音時發生錯誤: {str(e)}")
            return None

    def process(self) -> List[str]:
        """
        處理語音生成
        """

        safe_title = re.sub(r'[^\w\-_\. ]', '_', self.title)
        if not self.audio_description:
            self.logger.warning("沒有場景需要生成語音")
            return []
        self.logger.info(f"開始生成 {len(self.audio_description)} 個場景的語音")
        audio_paths = []
        completed_count = 0
        max_workers = min(len(self.audio_description), self.max_concurrency)
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_idx = {
                executor.submit(
                    self._generate_single_audio,
                    scene,
                    idx,
                    safe_title
                ): idx 
                for idx, scene in enumerate(self.audio_description)
            }
            for future in as_completed(future_to_idx):
                idx = future_to_idx[future]
                completed_count += 1
                try:
                    audio_path = future.result()
                    if audio_path:
                        audio_paths.append(audio_path)
                    progress = (completed_count / len(self.audio_description)) * 100
                    self.update_progress(progress)
                except Exception as e:
                    self.logger.error(f"語音生成任務執行失敗 (場景 {idx}): {str(e)}")
        audio_paths.sort()
        self.logger.info(f"完成所有語音生成，共成功生成 {len(audio_paths)} 個音檔")
        return audio_paths 

    def generate_audios(self) -> bool:
        """
        根據 audio_description 內容，並發產生語音檔案，只回傳是否全部成功。
        """
        if not hasattr(self, 'audio_description') or not self.audio_description:
            self.logger.warning("audio_description 為空，無需生成語音")
            return False
        safe_title = "audio"
        max_workers = min(len(self.audio_description), self.max_concurrency)
        results = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_idx = {
                executor.submit(
                    self._generate_single_audio,
                    text,
                    idx,
                    safe_title
                ): idx
                for idx, text in enumerate(self.audio_description)
            }
            for future in as_completed(future_to_idx):
                try:
                    audio_path = future.result()
                    results.append(audio_path is not None)
                except Exception as e:
                    self.logger.error(f"語音生成任務執行失敗: {str(e)}")
                    results.append(False)
        all_success = all(results) and len(results) == len(self.audio_description)
        if all_success:
            self.logger.info(f"全部語音生成成功，共 {len(results)} 段")
        else:
            self.logger.warning(f"有語音生成失敗，成功 {results.count(True)} / {len(results)} 段")
        return all_success 