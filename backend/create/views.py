import json
from rest_framework.views import APIView
from django.http import JsonResponse
import requests
import re  # 在文件頂部添加
from bs4 import BeautifulSoup

class NewsScrapeView(APIView):
    def post(self, request):
        try:
            data = json.loads(request.body)
            articles = []
            total_news = len(data['newsApi'])
            
            print(f"\n開始處理 {data['metadata']['keyword']} 相關新聞")
            print("=" * 50)
            print(f"總計 {total_news} 篇文章待處理")
            print("=" * 50)
            
            # 處理每個新聞連結
            
            for index, news in enumerate(data['newsApi']):
                try:
                    print(f"\n[{index + 1}/{total_news}] 處理中...")
                    print(f"標題: {news['title']}")
                    print(f"來源: {news['source']}")
                    print(f"連結: {news['link']}")
                    print("-" * 30)
                    
                    print("開始抓取文章內容...")
                    content = self.scrape_article_content(news['link'])
                    
                    if content:
                        articles.append({
                            "content": content,
                            "storyboard": None,
                            "title": news['title'],
                            "url": news['link']
                        })
                        print(f"✓ 成功! 擷取到 {len(content)} 字")
                    else:
                        print("✗ 失敗: 無法取得文章內容")
                        
                except Exception as e:
                    print(f"✗ 錯誤: {str(e)}")
                    continue

            print("\n" + "=" * 50)
            print(f"文章處理完成:")
            print(f"- 成功: {len(articles)} 篇")
            print(f"- 失敗: {total_news - len(articles)} 篇")
            print("=" * 50)

            if not articles:
                print("\n❌ 錯誤: 沒有成功抓取任何文章內容")
                return JsonResponse({
                    'status': {
                        'total': total_news,
                        'success': len(articles),
                        'failed': total_news - len(articles)
                    },
                    'error': '無法獲取任何文章內容'
                }, status=400)

            print("\n✅ 爬蟲完成，直接回傳結果")
            # 爬蟲完成後直接回傳文章內容，不進行生成處理
            return JsonResponse({
                'articles': articles,
                'status': {
                    'total': total_news,
                    'success': len(articles),
                    'failed': total_news - len(articles)
                },
                'message': '文章爬取完成'
            })
            
        except Exception as e:
            print(f"\n❌ 處理過程發生錯誤: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'error': str(e)
            }, status=500)

    def scrape_article_content(self, url):


        """抓取文章內容的函數"""
        try:
            print("連接網站中...")
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers, stream=True)
            
            if response.status_code == 200:
                print("網頁下載成功")
                soup = BeautifulSoup(response.content, 'html.parser')
                
                target_tags = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'span'])
                if target_tags:
                    combined_text = ' '.join(tag.get_text(strip=True) for tag in target_tags if tag.get_text(strip=True))
                    if combined_text:
                        return combined_text
                
                print("無法找到任何內容")
                return None
            else:
                print(f"網頁下載失敗: HTTP {response.status_code}")
                return None
                
        except requests.exceptions.Timeout:
            print("連接超時")
            return None
        except requests.exceptions.RequestException as e:
            print(f"請求錯誤: {str(e)}")
            return None
        except Exception as e:
            print(f"解析錯誤: {str(e)}")
            return None

class WordCountView(APIView):
    def post(self, request):
        url = request.data.get('url')
        word_count = self.get_words(url)
        return JsonResponse({'word_count': word_count})

    def get_words(self, url):
        """計算文章字數的函數"""
        try:
            print("\n開始計算文章字數...")
            print(f"網址: {url}")
            print("-" * 30)
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            print("連接網站中...")
            response = requests.get(url, headers=headers, stream=True)
            
            if response.status_code == 200:
                print("網頁下載成功")
                soup = BeautifulSoup(response.content, 'html.parser')
                
                target_tags = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'span'])
                if target_tags:
                    combined_text = ' '.join(tag.get_text(strip=True) for tag in target_tags if tag.get_text(strip=True))
                    if combined_text:
                        word_count = len(combined_text)
                        print(f"✓ 成功! 文章字數: {word_count}")
                        return word_count
                
                print("無法找到任何內容")
                return 0
                
            else:
                print(f"網頁下載失敗: HTTP {response.status_code}")
                return 0
                
        except requests.exceptions.Timeout:
            print("連接超時")
            return 0
        except requests.exceptions.RequestException as e:
            print(f"請求錯誤: {str(e)}")
            return 0
        except Exception as e:
            print(f"解析錯誤: {str(e)}")
            return 0
