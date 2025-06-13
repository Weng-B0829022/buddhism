import os
import json
import requests
from django.http import JsonResponse
from django.conf import settings
from dotenv import load_dotenv
import time
import logging
from openai import OpenAI
import threading
import re
import concurrent.futures
from collections import OrderedDict
from datetime import datetime

load_dotenv(os.path.join(settings.BASE_DIR, '.env'))
# 設定 logger
logger = logging.getLogger(__name__)

def log_and_print(message):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    formatted_message = f"{timestamp} - {message}"
    try:
        logger.info(formatted_message)
    except Exception as e:
        print(f"日志記錄失敗: {str(e)}")

# 初始化 OpenAI API Key
client = OpenAI(
        api_key=os.environ.get('OPENAI_API_KEY'),
    )
def fetch_generation_images(generation_id):
    url = f"https://cloud.leonardo.ai/api/rest/v1/generations/{generation_id}"
    headers = {
        'accept': 'application/json',
        'authorization': f'Bearer {os.environ.get("LEONARDO_API_KEY")}',
    }

    for attempt in range(40):
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            api_response = response.json()

            generated_images = api_response.get("generations_by_pk", {}).get("generated_images", [])
            image_urls = [img.get("url") for img in generated_images if img.get("url")]

            if image_urls:
                return image_urls[0]  # 返回第一個圖片 URL
            else:
                #print(f"等待生成圖片... 嘗試 {attempt + 1}/40")
                time.sleep(5)  # 沒有圖片則延遲後重試

        except requests.exceptions.RequestException as e:
            logger.error(f"Attempt {attempt + 1}: API request failed: {e}")
            continue

    logger.error("無法獲取生成的圖片")
    return None

# 翻譯描述為英文的函數
def translate_to_english(text):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # 使用 gpt-3.5-turbo 或 gpt-4
            messages=[
                {"role": "system", "content": "You are a helpful assistant that translates text to English and generates effective prompt phrases for news image generation. Given a news title or article content, you should first translate the input into fluent English, and then generate a descriptive prompt that can be used to create a relevant image. The prompt should focus on the key people, places, actions, and emotions involved in the news story. "
                },
                {"role": "user", "content": f" {text}"}
            ],
            max_tokens=100,
            temperature=0.5,
        )
        english_text = response.choices[0].message.content.strip()
        return english_text
    except Exception as e:
        logger.error(f"翻譯失敗: {str(e)}")
        return text  # 如果翻譯失敗，返回原始文本

# 獲取生成圖片的 URL
def generate_images_from_descriptions(title, image_descriptions, random_id):
    save_directory=os.path.join(settings.MEDIA_ROOT, 'generated', random_id)
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
    
    leonardo_url = "https://cloud.leonardo.ai/api/rest/v1/generations"
    headers = {
        'accept': 'application/json',
        'authorization': f'Bearer {os.environ.get("LEONARDO_API_KEY")}',
        'content-type': 'application/json'
    }
    
    total_images = len(image_descriptions)
    progress_counter = 0
    progress_lock = threading.Lock()
    results = OrderedDict()

    def generate_image(idx, description):
        nonlocal progress_counter
        try:
            payload = {
                "prompt": description,
                "alchemy": True,
                "height": 768,
                "modelId": "aa77f04e-3eec-4034-9c07-d0f619684628",
                "num_images": 1,
                "presetStyle": "NONE",
                "width": 1024,
                "photoReal": True,
                "expandedDomain": True,
                "photoRealVersion": "v2",
                "public": False,
                "guidance_scale": 7,
                "num_inference_steps": 30,
                "contrastRatio": 0.8,
                "highResolution": True,
                "negative_prompt": "low resolution, bad quality, unrealistic"
            }
            response = requests.post(leonardo_url, headers=headers, json=payload)
            response.raise_for_status()
            api_response = response.json()

            generation_id = api_response.get("sdGenerationJob", {}).get("generationId")
            if generation_id:
                image_url = fetch_generation_images(generation_id)

                if image_url:
                    image_response = requests.get(image_url)
                    if image_response.status_code == 200:
                        safe_title = re.sub(r'[^\w\-_\. ]', '_', title)
                        image_filename = f'{safe_title}_{idx+1}.png'
                        image_path = os.path.join(save_directory, image_filename)
                        with open(image_path, 'wb') as f:
                            f.write(image_response.content)

                        # 只保留檔名，不包含路徑
                        return idx, (image_url, image_filename)
                    else:
                        logger.error(f"圖片下載失敗: {description}")
                else:
                    logger.error(f"生成圖片失敗: {description}")
            else:
                logger.error(f"Leonardo API 沒有返回 generation_id")
        except Exception as e:
            logger.error(f"生成圖片失敗: {str(e)}")
        finally:
            with progress_lock:
                progress_counter += 1
                log_and_print(f"圖片生成進度: {progress_counter}/{total_images}")
        return idx, None

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_idx = {executor.submit(generate_image, idx, desc): idx for idx, desc in enumerate(image_descriptions)}
        for future in concurrent.futures.as_completed(future_to_idx):
            idx, result = future.result()
            if result:
                results[idx] = result

    # 按照原始順序整理結果
    image_results = [results[i] for i in range(len(image_descriptions)) if i in results]

    return image_results

# 測試新聞生成邏輯
def run_news_gen_img(manager, storyboard_object, random_id, coordinates, extend_coordinates):
    try:
        log_and_print("開始下載新聞圖片")
        
        save_directory = os.path.join(settings.MEDIA_ROOT, 'generated', random_id)
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)

        title = storyboard_object.get('title')
        image_results = []

        for idx, item in enumerate(storyboard_object.get('storyboard', [])):
            image_url = item.get('imageUrl')
            if image_url:
                log_and_print(f"開始處理 Paragraph {idx + 1} 的圖片")
                try:
                    # 檢查是否為 base64 圖片
                    if image_url.startswith('data:image'):
                        # 直接從 base64 字符串中提取圖片數據
                        image_data = image_url.split(',')[1]
                        import base64
                        image_content = base64.b64decode(image_data)
                    else:
                        # 下載圖片
                        image_response = requests.get(image_url)
                        if image_response.status_code != 200:
                            log_and_print(f"下載圖片失敗: {image_url}")
                            continue
                        image_content = image_response.content

                    # 使用原有的命名方式
                    safe_title = re.sub(r'[^\w\-_\. ]', '_', title)
                    image_filename = f'{safe_title}_{idx+1}.png'
                    image_path = os.path.join(save_directory, image_filename)
                    
                    # 保存圖片
                    with open(image_path, 'wb') as f:
                        f.write(image_content)
                    
                    # 更新圖片配置
                    if manager.get_storyboard()['storyboard'][idx]['needAvatar']:
                        image_info = {
                            "img_path": image_filename,
                            "url": image_url if not image_url.startswith('data:image') else None,
                            "top_left": coordinates["top_left"],
                            "top_right": coordinates["top_right"],
                            "bottom_right": coordinates["bottom_right"],
                            "bottom_left": coordinates["bottom_left"],
                            "z_index": 0
                        }
                    else:
                        image_info = {
                            "img_path": image_filename,
                            "url": image_url if not image_url.startswith('data:image') else None,
                            "top_left": extend_coordinates["top_left"],
                            "top_right": extend_coordinates["top_right"],
                            "bottom_right": extend_coordinates["bottom_right"],
                            "bottom_left": extend_coordinates["bottom_left"],
                            "z_index": 0
                        }
                    
                    manager.update_paragraph(idx, {"images": [image_info]})
                    image_results.append((image_url if not image_url.startswith('data:image') else None, image_path))
                    log_and_print(f"成功處理 Paragraph {idx + 1} 的圖片")
                except Exception as e:
                    log_and_print(f"處理圖片時發生錯誤: {str(e)}")
                    continue

        manager.wait_for_queue()
        log_and_print("完成所有圖片處理")
        return image_results

    except Exception as e:
        log_and_print(f"圖片處理過程中發生錯誤: {str(e)}")
        return []

if __name__ == '__main__':
    run_news_gen_img()
