"""
主要流程控制器
負責協調整個影片生成流程
"""

from typing import Dict, List, Any, Optional
import logging
import os
from .managers.asset_manager import AssetManager
from .processors.image_processor import ImageProcessor
from .processors.audio_processor import AudioProcessor
from .processors.character_processor import CharacterProcessor
from .processors.scene_compositor import SceneCompositor
from .processors.final_compositor import FinalCompositor
from .utils.validation import validate_storyboard_data
from .config.settings import get_default_config
from projectNews.settings import BASE_DIR

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
        self.asset_manager = None
        self.progress_manager = None
        self.output_path = None
        # 處理器
        self.processors = {}
        
    def initialize(self, storyboard: Dict) -> bool:
        """初始化工作環境"""
        try:
            self.logger.info("開始初始化主流程")
            

            # 2. 生成唯一 ID
            self.random_id = self._generate_random_id()
            
            self.storyboard = storyboard
            
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
            
            # 檢查是否已經初始化
            if self.storyboard is None or self.random_id is None:
                raise ValueError("尚未執行初始化，請先調用 initialize() 方法")
            
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
        image_urls = [scene.get('imageUrl') for scene in self.storyboard.get('storyboard', [])]
        title = self.storyboard.get('title', 'untitled')
        
        image_processor = ImageProcessor(image_urls, self.output_path, title)
        image_processor.process()
        #下載聲音
        for scene in self.scenes:
            audio_processor = AudioProcessor(self.config.get('audio_processor', {}))
            audio_processor.process(scene)
        #生成人偶
        for scene in self.scenes:
            character_processor = CharacterProcessor(self.config.get('character_processor', {}))
            character_processor.process(scene)
        #合成場景
        for scene in self.scenes:
            scene_compositor = SceneCompositor(self.config.get('scene_compositor', {}))
            scene_compositor.process(scene)
        return []
    
    def process_single_scene(self, scene_index: int, scene_data: Dict) -> str:
        """處理單一場景"""
        # TODO: 實作單一場景處理邏輯
        return f"/generated/{self.random_id}/scene_{scene_index}.mp4"
    
    def final_composition(self) -> str:
        """最終合成階段"""
        # TODO: 實作最終合成邏輯
        return f"/generated/{self.random_id}/final_video.mp4"
    
    def _initialize_processors(self):
        """初始化所有處理器"""
        self.processors = {
            'image': ImageProcessor(self.config.get('image_processor', {})),
            'audio': AudioProcessor(self.config.get('audio_processor', {})),
            'character': CharacterProcessor(self.config.get('character_processor', {})),
            'scene_compositor': SceneCompositor(self.config.get('scene_compositor', {})),
            'final_compositor': FinalCompositor(self.config.get('final_compositor', {}))
        }
        
        self.logger.debug(f"已初始化 {len(self.processors)} 個處理器")
    
    def _generate_random_id(self) -> str:
        """生成唯一識別碼"""
        import random
        import string
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=10)) 