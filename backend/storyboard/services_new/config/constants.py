"""
常數定義
定義系統中使用的常數
"""

# 預設路徑
DEFAULT_OUTPUT_PATH = "/tmp/generated"
DEFAULT_TEMP_DIR = "/tmp/video_generation"

# 支援的檔案格式
SUPPORTED_IMAGE_FORMATS = [
    'png', 'jpg', 'jpeg', 'webp', 'gif'
]

SUPPORTED_AUDIO_FORMATS = [
    'wav', 'mp3', 'aac', 'ogg'
]

SUPPORTED_VIDEO_FORMATS = [
    'mp4', 'avi', 'mov', 'mkv'
]

# 處理器名稱
PROCESSOR_NAMES = {
    'IMAGE': 'ImageProcessor',
    'AUDIO': 'AudioProcessor', 
    'CHARACTER': 'CharacterProcessor',
    'SCENE_COMPOSITOR': 'SceneCompositor',
    'FINAL_COMPOSITOR': 'FinalCompositor'
}

# 處理階段
PROCESSING_STAGES = {
    'INITIALIZATION': 'initialization',
    'IMAGE_GENERATION': 'image_generation',
    'AUDIO_GENERATION': 'audio_generation', 
    'CHARACTER_GENERATION': 'character_generation',
    'SCENE_COMPOSITION': 'scene_composition',
    'FINAL_COMPOSITION': 'final_composition',
    'CLEANUP': 'cleanup'
}

# 檔案大小限制（bytes）
MAX_FILE_SIZES = {
    'IMAGE': 50 * 1024 * 1024,    # 50MB
    'AUDIO': 100 * 1024 * 1024,   # 100MB
    'VIDEO': 500 * 1024 * 1024,   # 500MB
    'FINAL_VIDEO': 1024 * 1024 * 1024  # 1GB
}

# 超時設定（秒）
DEFAULT_TIMEOUTS = {
    'IMAGE_PROCESSOR': 300,
    'AUDIO_PROCESSOR': 180,
    'CHARACTER_PROCESSOR': 600,
    'SCENE_COMPOSITOR': 300,
    'FINAL_COMPOSITOR': 900
}

# 重試設定
DEFAULT_RETRY_COUNTS = {
    'IMAGE_PROCESSOR': 3,
    'AUDIO_PROCESSOR': 3,
    'CHARACTER_PROCESSOR': 2,
    'SCENE_COMPOSITOR': 2,
    'FINAL_COMPOSITOR': 1
}

# 日誌級別
LOG_LEVELS = {
    'DEBUG': 10,
    'INFO': 20,
    'WARNING': 30,
    'ERROR': 40,
    'CRITICAL': 50
}

# 錯誤代碼
ERROR_CODES = {
    'VALIDATION_ERROR': 1001,
    'FILE_NOT_FOUND': 1002,
    'DISK_SPACE_ERROR': 1003,
    'TIMEOUT_ERROR': 1004,
    'PROCESSING_ERROR': 1005,
    'NETWORK_ERROR': 1006
} 