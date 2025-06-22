# CDN 上傳功能使用說明

## 概述

本專案已整合 Cloudinary CDN 上傳功能，可以自動將生成的音訊、圖片和影片檔案上傳到 CDN，並返回可用的 URL。

## 設定

### 1. 安裝依賴

確保已安裝 `cloudinary` 套件：

```bash
pip install cloudinary==1.40.0
```

### 2. 環境變數設定

在 `.env` 檔案中設定 Cloudinary 憑證：

```env
CLOUDINARY_CLOUD_NAME=你的cloud_name
CLOUDINARY_API_KEY=你的api_key
CLOUDINARY_API_SECRET=你的api_secret
```

## 使用方法

### 方法一：使用主流程（推薦）

主流程會自動處理 CDN 上傳：

```python
from storyboard.services_new.main_pipeline import MainPipeline

# 初始化主流程
pipeline = MainPipeline()

# 初始化並執行
if pipeline.initialize(storyboard_data):
    result = pipeline.execute()
    
    # 檢查上傳結果
    if result['status'] == 'success':
        uploaded_assets = result.get('uploaded_assets', {})
        print("音訊檔案:", uploaded_assets.get('audio_urls', []))
        print("圖片檔案:", uploaded_assets.get('image_urls', []))
        print("影片檔案:", uploaded_assets.get('video_urls', []))
```

### 方法二：直接使用 CDN 上傳器

```python
from storyboard.services_new.utils.cdn_uploader import CDNUploader

# 初始化上傳器
uploader = CDNUploader()

# 上傳整個目錄
result = uploader.upload_directory(
    directory_path="/path/to/generated/files",
    project_id="unique_project_id"
)

# 上傳單一檔案
audio_url = uploader.upload_single_file(
    file_path="/path/to/audio.mp3",
    project_id="unique_project_id",
    file_type="raw"
)
```

## 檔案組織

上傳的檔案會按以下結構組織在 Cloudinary 中：

```
cloudinary.com/
├── audio/project_id/
│   ├── audio_file_1
│   ├── audio_file_2
│   └── ...
├── images/project_id/
│   ├── image_file_1
│   ├── image_file_2
│   └── ...
└── videos/project_id/
    ├── video_file_1
    ├── video_file_2
    └── ...
```

## 支援的檔案類型

- **音訊檔案**: `.mp3` (resource_type: "raw")
- **圖片檔案**: `.png` (resource_type: "image")
- **影片檔案**: `.mp4` (resource_type: "video")

## 錯誤處理

上傳過程中會自動處理以下情況：

1. **檔案不存在**: 跳過並記錄警告
2. **上傳失敗**: 記錄錯誤但繼續處理其他檔案
3. **網路問題**: 自動重試（可配置）

## 測試

執行測試腳本來驗證功能：

```bash
cd backend
python test_cdn_upload.py
```

## 注意事項

1. 確保 Cloudinary 帳戶有足夠的儲存空間和頻寬
2. 大型檔案上傳可能需要較長時間
3. 建議在生產環境中設定適當的錯誤處理和重試機制
4. 定期清理不需要的檔案以節省儲存空間

## 範例輸出

```python
{
    'audio_urls': [
        'https://res.cloudinary.com/your-cloud/raw/upload/v123/audio/project_id/audio_1.mp3',
        'https://res.cloudinary.com/your-cloud/raw/upload/v123/audio/project_id/audio_2.mp3'
    ],
    'image_urls': [
        'https://res.cloudinary.com/your-cloud/image/upload/v123/images/project_id/image_1.png',
        'https://res.cloudinary.com/your-cloud/image/upload/v123/images/project_id/image_2.png'
    ],
    'video_urls': [
        'https://res.cloudinary.com/your-cloud/video/upload/v123/videos/project_id/video_1.mp4'
    ]
}
``` 