#!/usr/bin/env python3
"""
簡單的 CDN 上傳功能測試
"""

import os
import tempfile
from unittest.mock import patch, MagicMock
import cloudinary
import cloudinary.uploader


class SimpleCDNUploader:
    """簡化的 CDN 上傳器"""
    
    def __init__(self):
        # 設定 Cloudinary 配置
        cloudinary.config(
            cloud_name='test_cloud',
            api_key='test_key',
            api_secret='test_secret'
        )
    
    def upload_audio_files(self, directory_path: str, project_id: str):
        """上傳音訊檔案"""
        import glob
        
        urls = []
        file_pattern = os.path.join(directory_path, "*.mp3")
        files = glob.glob(file_pattern)
        
        print(f"找到 {len(files)} 個 MP3 檔案")
        
        for file_path in files:
            try:
                filename = os.path.basename(file_path)
                public_id = os.path.splitext(filename)[0]
                
                print(f"正在上傳: {filename}")
                
                result = cloudinary.uploader.upload(
                    file_path,
                    resource_type="raw",
                    folder=f"audio/{project_id}",
                    public_id=public_id
                )
                urls.append(result["secure_url"])
                print(f"✅ 上傳成功: {result['secure_url']}")
                
            except Exception as e:
                print(f"❌ 上傳失敗 {file_path}: {e}")
        
        return urls


def test_upload_functionality():
    """測試上傳功能"""
    print("=== 測試 CDN 上傳功能 ===")
    
    # 創建臨時目錄和測試檔案
    with tempfile.TemporaryDirectory() as temp_dir:
        # 創建測試 MP3 檔案
        test_files = []
        for i in range(3):
            mp3_file = os.path.join(temp_dir, f"test_audio_{i}.mp3")
            with open(mp3_file, 'w') as f:
                f.write(f"fake mp3 content {i}")
            test_files.append(mp3_file)
            print(f"創建測試檔案: {mp3_file}")
        
        uploader = SimpleCDNUploader()
        
        # Mock Cloudinary 上傳回應
        mock_result = {
            "secure_url": "https://res.cloudinary.com/test/raw/upload/v123/audio/test_project/test_audio.mp3"
        }
        
        with patch('cloudinary.uploader.upload', return_value=mock_result) as mock_upload:
            print("\n開始測試上傳...")
            audio_urls = uploader.upload_audio_files(temp_dir, "test_project")
            
            # 驗證結果
            print(f"\n上傳結果: {len(audio_urls)} 個檔案")
            for url in audio_urls:
                print(f"  - {url}")
            
            # 驗證上傳調用
            assert mock_upload.call_count == 3, f"預期 3 次上傳，實際 {mock_upload.call_count} 次"
            
            # 驗證上傳參數
            for call in mock_upload.call_args_list:
                args, kwargs = call
                assert kwargs['resource_type'] == 'raw', "resource_type 應該是 'raw'"
                assert kwargs['folder'] == 'audio/test_project', "folder 路徑不正確"
            
            print("\n✅ 所有測試通過！")


def test_empty_directory():
    """測試空目錄"""
    print("\n=== 測試空目錄 ===")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        uploader = SimpleCDNUploader()
        
        with patch('cloudinary.uploader.upload') as mock_upload:
            audio_urls = uploader.upload_audio_files(temp_dir, "test_project")
            
            assert len(audio_urls) == 0, "空目錄應該返回空列表"
            assert mock_upload.call_count == 0, "空目錄不應該調用上傳"
            
            print("✅ 空目錄測試通過！")


def test_error_handling():
    """測試錯誤處理"""
    print("\n=== 測試錯誤處理 ===")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # 創建一個測試檔案
        mp3_file = os.path.join(temp_dir, "test_audio.mp3")
        with open(mp3_file, 'w') as f:
            f.write("fake mp3 content")
        
        uploader = SimpleCDNUploader()
        
        # Mock 上傳失敗
        with patch('cloudinary.uploader.upload', side_effect=Exception("Upload failed")):
            audio_urls = uploader.upload_audio_files(temp_dir, "test_project")
            
            assert len(audio_urls) == 0, "上傳失敗應該返回空列表"
            print("✅ 錯誤處理測試通過！")


if __name__ == "__main__":
    try:
        test_upload_functionality()
        test_empty_directory()
        test_error_handling()
        print("\n🎉 所有測試完成！")
    except Exception as e:
        print(f"\n❌ 測試失敗: {e}")
        import traceback
        traceback.print_exc() 