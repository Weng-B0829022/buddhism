#!/usr/bin/env python3
"""
執行 CDN 上傳功能測試
"""

import os
import sys
import subprocess

def run_tests():
    """執行測試"""
    print("=== 執行 CDN 上傳功能測試 ===")
    
    # 確保在正確的目錄
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # 執行測試
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "tests/test_cdn_upload.py", 
            "-v",
            "--tb=short"
        ], capture_output=True, text=True)
        
        print("測試輸出:")
        print(result.stdout)
        
        if result.stderr:
            print("錯誤輸出:")
            print(result.stderr)
        
        if result.returncode == 0:
            print("\n✅ 所有測試通過！")
        else:
            print(f"\n❌ 測試失敗，退出碼: {result.returncode}")
            
    except Exception as e:
        print(f"❌ 執行測試時發生錯誤: {e}")


if __name__ == "__main__":
    run_tests() 