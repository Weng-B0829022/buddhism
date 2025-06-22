"""
主要流程控制器
負責協調整個影片生成流程
"""

from typing import Dict, List, Any, Optional
import logging
import os
from .processors.image_processor import ImageProcessor
from .processors.audio_processor import AudioProcessor
from .processors.character_processor import CharacterProcessor
from .processors.scene_compositor import SceneCompositor
from .processors.final_compositor import FinalCompositor
from .utils.validation import validate_storyboard_data
from .config.settings import get_default_config
from projectNews.settings import BASE_DIR
import cloudinary
import cloudinary.uploader

from dotenv import load_dotenv
load_dotenv()

class MainPipeline:
    """
    主要影片生成流程控制器
    
    流程:
    1. 初始化階段
    2. 場景處理循環 (圖片 -> 聲音 -> 人偶 -> 合成)
    3. 最終合成階段
    """
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or get_default_config()
        self.logger = logging.getLogger(__name__)
        
        # 基本屬性
        self.storyboard = None
        self.random_id = None
        self.scenes = []
        self.scene_videos = []
        
        # 管理器
        self.progress_manager = None
        self.output_path = None
        # 處理器
        self.processors = {}
        
    def initialize(self, storyboard: Dict) -> bool:
        """初始化工作環境"""
        try:
            self.logger.info("開始初始化主流程")
            

            # 2. 生成唯一 ID
            self.random_id = 'ppxsrz95b7'
            
            self.storyboard = storyboard
            self.title = self.storyboard.get('title', 'untitled')
            self.scenes = storyboard.get('storyboard', [])
            
            #創建輸出目錄

            self.output_path = os.path.join(BASE_DIR, 'generated', self.random_id)
            self.logger.info(f"初始化完成，場景數量: {len(self.scenes)}, ID: {self.random_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"初始化失敗: {e}")
            return False
    
    def execute(self) -> Dict[str, Any]:
        """執行完整流程"""
        try:
            self.logger.info("開始執行主流程")
            
            # Phase 1: 處理所有場景
            self.process_scenes()
            
            # Phase 2: 最終合成
            self.final_composition()
            
            # Phase 3: 清理和返回結果
            result = {
                'status': 'success',
                'random_id': self.random_id,
            }
            
            self.logger.info(f"主流程執行完成: {result}")
            return result
            
        except Exception as e:
            self.logger.error(f"主流程執行失敗: {e}")
            return {
                'status': 'error',
                'error_message': str(e),
                'random_id': self.random_id
            }
    
    def process_scenes(self) -> List[str]:
        """處理所有場景"""
        if not self.storyboard or not self.scenes:
            self.logger.warning("沒有可處理的場景資料")
            return []
        
        #下載圖片
        # image_urls = [scene.get('imageUrl') for scene in self.scenes]
        # image_processor = ImageProcessor(image_urls, self.output_path, self.title)
        # image_processor.process()

        #下載聲音
        # audio_description = [scene.get('voiceover') for scene in self.scenes]
        # print(audio_description)
        # audio_processor = AudioProcessor(audio_description, self.output_path, self.title)
        # audio_processor.process()
        

        #audio_urls = self.upload_assets_to_cdn()

        #生成人偶
        
        # character_processor = CharacterProcessor(audio_urls, self.output_path, self.title)
        # character_processor.process()

        
        # return []

    #對每一個場景合成
    def process_single_scene(self) -> str:
        #合成場景
        scene_compositor = SceneCompositor(self.output_path, self.title)
        scene_compositor.process()


        return scene_compositor.result_paths
    
    #最終合成
    def final_composition(self) -> str:
        """最終合成階段"""
        # TODO: 實作最終合成邏輯
        return 
    

    def _generate_random_id(self) -> str:
        """生成唯一識別碼"""
        import random
        import string
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=10)) 
    
    def upload_assets_to_cdn(self) -> List[str]:
        """上傳所有生成的 MP3 資源到 CDN"""
        try:
            self.logger.info("開始上傳 MP3 資源到 CDN")
            
            if not self.output_path or not os.path.exists(self.output_path):
                self.logger.warning("輸出目錄不存在，跳過 CDN 上傳")
                return []
            
            # Cloudinary 設定（建議用環境變數管理）
            cloudinary.config(
                cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME'),
                api_key = os.getenv('CLOUDINARY_API_KEY'),
                api_secret = os.getenv('CLOUDINARY_API_SECRET')
            )
            
            # 找出所有 mp3 檔案
            audio_files = [f for f in os.listdir(self.output_path) if f.endswith('.mp3')]
            audio_urls = []
            for filename in audio_files:
                file_path = os.path.join(self.output_path, filename)
                response = cloudinary.uploader.upload(
                    file_path,
                    resource_type="video",  # MP3 屬於 Cloudinary 的「video」資源類型
                    public_id=f"{filename}"
                )
                audio_urls.append(response["secure_url"])
                self.logger.info(f"已上傳: {filename} -> {response['secure_url']}")
            
            self.uploaded_assets = {
                'audio_urls': audio_urls
            }
            self.logger.info(f"CDN 上傳完成，共上傳 {len(audio_urls)} 個 MP3 檔案")
            return audio_urls
        
        except Exception as e:
            self.logger.error(f"CDN 上傳失敗: {e}")
            self.uploaded_assets = {'audio_urls': []}
            return []