#!/usr/bin/env python3
"""
測試 CDN 上傳功能
"""

import os
import sys
import django

# 設定 Django 環境
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projectNews.settings')
django.setup()

from storyboard.services_new.main_pipeline import MainPipeline


def test_cdn_uploader():
    """測試 CDN 上傳器"""
    print("=== 測試 CDN 上傳器 ===")
    
    # 初始化上傳器
    uploader = CDNUploader()
    
    # 測試目錄路徑（使用現有的生成目錄）
    test_directory = os.path.join(os.path.dirname(__file__), 'generated', 'ppxsrz95b7')
    
    if os.path.exists(test_directory):
        print(f"測試目錄: {test_directory}")
        
        # 上傳整個目錄
        result = uploader.upload_directory(test_directory, "test_project")
        
        print("\n=== 上傳結果 ===")
        for file_type, urls in result.items():
            print(f"{file_type}: {len(urls)} 個檔案")
            for url in urls:
                print(f"  - {url}")
    else:
        print(f"測試目錄不存在: {test_directory}")


def test_main_pipeline():
    """測試主流程的 CDN 上傳"""
    print("\n=== 測試主流程 CDN 上傳 ===")
    
    # 創建模擬的分鏡資料
    mock_storyboard = {
        'title': '測試影片',
        'storyboard': [
            {
                'imageUrl': 'https://example.com/image1.jpg',
                'voiceover': '這是第一段旁白'
            },
            {
                'imageUrl': 'https://example.com/image2.jpg',
                'voiceover': '這是第二段旁白'
            }
        ]
    }
    
    # 初始化主流程
    pipeline = MainPipeline()
    
    # 初始化
    if pipeline.initialize(mock_storyboard):
        print("主流程初始化成功")
        
        # 執行流程（這裡只測試上傳部分）
        if hasattr(pipeline, 'output_path') and pipeline.output_path:
            print(f"輸出目錄: {pipeline.output_path}")
            
            # 測試上傳
            pipeline.upload_assets_to_cdn()
            
            if hasattr(pipeline, 'uploaded_assets'):
                print("上傳結果:", pipeline.uploaded_assets)
            else:
                print("沒有上傳結果")
        else:
            print("沒有輸出目錄")
    else:
        print("主流程初始化失敗")


if __name__ == "__main__":
    # 檢查環境變數
    required_env_vars = [
        'CLOUDINARY_CLOUD_NAME',
        'CLOUDINARY_API_KEY', 
        'CLOUDINARY_API_SECRET'
    ]
    
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    
    if missing_vars:
        print("警告: 缺少以下環境變數:")
        for var in missing_vars:
            print(f"  - {var}")
        print("\n請在 .env 檔案中設定這些變數")
        print("或者設定為預設值進行測試")
    
    # 執行測試
    test_main_pipeline() 