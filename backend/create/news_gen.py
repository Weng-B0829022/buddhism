import os
from dotenv import load_dotenv
from openai import OpenAI
import json
from django.conf import settings
import os
import json


def access_gpt(messages, max_retries=3, model='gpt-4o'):
    load_dotenv(os.path.join(settings.BASE_DIR, '.env'))
    client = OpenAI(
        api_key=os.environ.get('OPENAI_API_KEY'),
    )

    for attempt in range(max_retries):
        try:
            chat_completion = client.chat.completions.create(
                messages=messages,
                model=model,
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            print(f"Attempt {attempt + 1} failed: {str(e)}. Retrying...")
            continue

def extract_news_fact(articles):
    integrated_news_list = []

    PROMPT_EXTRACT_AND_INTEGRATE_1 = '# Step 1\n\nArticle 1: '
    PROMPT_EXTRACT_AND_INTEGRATE_2 = None
    with open('prompt_extract_and_integrate/2.txt', 'r', encoding='utf-8') as file:
        PROMPT_EXTRACT_AND_INTEGRATE_2 = file.read()
    PROMPT_EXTRACT_AND_INTEGRATE_3 = None
    with open('prompt_extract_and_integrate/3.txt', 'r', encoding='utf-8') as file:
        PROMPT_EXTRACT_AND_INTEGRATE_3 = file.read()

    for article in articles:
        content = article.get('content')

        gpt_messages = []

        # Extract news fact
        prompt_extract_fact = (
            f'{PROMPT_EXTRACT_AND_INTEGRATE_1}'
            f'{content}\n'
            f'{PROMPT_EXTRACT_AND_INTEGRATE_2}'
        )

        gpt_messages.append({
            'role': 'user',
            'content': prompt_extract_fact,
        })

        extracted_fact = access_gpt(gpt_messages)
        print(extracted_fact)

        print('\n\n--\n\n')

        gpt_messages.append({
            'role': 'user',
            'content': extracted_fact,
        })

        # Integrate multiple similar news
        prompt_integrate_news = PROMPT_EXTRACT_AND_INTEGRATE_3
        gpt_messages.append({
            'role': 'user',
            'content': prompt_integrate_news,
        })
        integrated_news = access_gpt(gpt_messages)
        print(integrated_news)

        integrated_news_list.append(integrated_news)

    return integrated_news_list



def extract_keyword_news_fact(articles):
    print("Step 1: 開始處理新聞內容")
    print("已開始處理新聞內容")

    # 合併所有文章內容
    content = ''
    for article in articles['articles']:
        content = content + article.get('content')

    print("Step 2: 合併文章內容完成")
    print(f"已合併文章內容，總長度: {len(content)} 字符")
    print(f"合併後內容預覽: {content[:200]}...")

    # 範例格式
    example_format = {
        "main_article": {
            "title": "川普對等關稅政策掀全球經濟震盪",
            "content": "美國總統川普日前宣布的對等關稅政策，透過調整進口稅率與全球主要經濟體展開貿易戰，引發全球市場震盪。該政策希望透過對中國商品增加高達34%的懲罰性關稅，迫使對方取消報復性措施，同時要求蘋果等美國企業遷回生產線至美國。然而，因勞工成本與供應鏈配置問題，僅引發廣泛質疑與抵制。此外，川普團隊使用的關稅計算公式被揭發灌水，實際稅率應僅為政府宣布的四分之一。此消息不僅使貿易夥伴對川普政策產生更多懷疑，更加劇了已因全球供應鏈不穩而面臨挑戰的國際經濟格局。",
            "category": "Business"
        },
        "articles": [
            {
                "title": "關稅政策對全球經濟的影響分析",
                "content": "川普推行的對等關稅政策致使全球市場震盪，打擊了包括台灣、日本和歐盟在內多國經濟。該政策的核心，是試圖通過高關稅迫使他國讓步。然而，根據經濟專家表示，此類關稅將提高進口成本，打擊消費者購買力，同時增加製造業成本，對全球化供應鏈帶來深遠影響。此外，長期的貿易摩擦將對多邊經貿體制構成威脅，可能進一步推升全球衰退風險。在關稅壓力外，川普政府不確定的政策走向加劇了市場恐慌，許多投資者轉向避險資產，如黃金和美國國債，進一步影響資金流動。",
                "storyboard": [
                    "1\n00:00:00,000 --> 00:00:12,000\nImage: 白宮夏日日景和國會大樓特寫，搭配全球股市指數下跌圖表\nVoiceover Text: '川普政府近期宣布的對等關稅政策，引發全球金融市場的劇烈震盪，從亞洲到歐洲，各大主要股市表現疲軟，投資者信心受到顯著衝擊。'",
                    "2\n00:00:12,000 --> 00:00:24,000\nImage: 中國出口貨船在繁忙貨港裝載貨物的動態場景，遠處堆滿集裝箱\nVoiceover Text: '川普針對中國進口商品加徵高達34%的關稅，旨在縮減美國貿易赤字並限制中國商品的全球競爭力，但此舉已引發貿易夥伴國的強烈反彈與報復性措施。'",
                    "3\n00:00:24,000 --> 00:00:36,000\nVideo: 美國商場貨架陳列商品，顧客檢視價格標籤，臉上帶有憂慮神情\nVoiceover Text: '對美國消費者而言，關稅推高了進口商品價格，從電子產品到日常用品，購買力的下降正對家庭預算造成壓力，進一步影響消費信心與市場需求。'",
                    "4\n00:00:36,000 --> 00:00:48,000\nVideo: 日本車企工廠內生產線運作，工人與機器人協同作業的場景\nVoiceover Text: '日本和歐盟的跨國企業對此表達深切憂慮，部分汽車和科技公司已暫停在美國的投資計劃，擔心關稅對其全球業務與供應鏈的長期破壞性影響。'",
                    "5\n00:00:48,000 --> 00:00:58,000\nImage: 國際股市圖表顯示波動加劇，背景為全球貿易路線地圖\nVoiceover Text: '分析師警告，全球關稅戰不僅威脅市場需求，還可能導致供需失衡，進而引發經濟衰退，尤其在新興市場和中小型經濟體中影響更為顯著。'",
                    "6\n00:00:58,000 --> 00:01:08,000\nImage: 世界工廠、煉油廠與煙囪林立的工業設施，顯示供應鏈複雜性\nVoiceover Text: '全球化供應鏈正面臨數十年來最嚴峻的挑戰，關稅導致生產成本上升，企業被迫重新評估供應鏈布局，影響全球製造業的穩定與效率。'",
                    "7\n00:01:08,000 --> 00:01:20,000\nVideo: 經濟學專家在會議室接受媒體專訪，背景為數據圖表\nVoiceover Text: '經濟專家指出，對等關稅政策可能引發中小企業的生存危機，這些企業難以應對持續緊張的商業環境和高企的運營成本，面臨市場競爭劣勢。'",
                    "8\n00:01:20,000 --> 00:01:32,000\nImage: 歐洲議會內部，政府首腦會議現場，代表們熱烈討論\nVoiceover Text: '各國政府正針對川普的激進關稅政策進行多邊協商，試圖通過外交談判與聯合行動，減輕對其經濟的衝擊並維護全球貿易體系的穩定。'",
                    "9\n00:01:32,000 --> 00:01:47,000\nVideo: 經濟研究報告呈現，搭配金融數據走勢與全球市場分析\nVoiceover Text: '研究報告顯示，長期執行對等關稅將抑制全球投資意願，增加經濟不確定性，特別是在新興市場與依賴出口的經濟體中影響尤為深遠。'",
                    "10\n00:01:47,000 --> 00:02:00,000\nImage: 國際貿易標誌與全球地圖，畫面緩慢平移展現互聯世界\nVoiceover Text: '這場經濟戰的結局仍充滿變數，各國政府需迅速調整政策，制定應對策略，以減緩關稅對全球經濟的衝擊並尋求合作共贏的解決方案。'"
                ]
            }
        ]
    }

    # 創建一個簡化的 prompt，直接使用範例作為參考
    combined_prompt = f"""
請根據以下新聞內容，生成八篇關於同一主題的文章（包括三篇衍生文章）。每篇文章都需要包含標題、內容和分鏡表。

新聞內容：
{content}

請參考以下範例格式，生成八篇關於同一主題的文章：

範例格式(以下為範例格式請勿抄襲內容)：
<example>
{json.dumps(example_format, ensure_ascii=False, indent=2)}
</example>

請確保：
1. 所有內容必須使用繁體中文
2. 每篇文章的分鏡表必須包含10個段落，每個段落包含時間軸、圖像/視頻描述和旁白文字
3. 輸出必須是有效的JSON對象
4. 必須包含8篇衍生文章
5. 每篇文章都必須有完整的分鏡表
6. 所有文章都應該圍繞同一主題，但從不同角度進行分析
7. 衍生文章必須包含以下角度選擇：以政治新聞撰寫方式分析上述事實、經濟新聞、社會新聞、社會學角度、經濟學角度、法律學角度、人類學角度、心理學角度


請直接提供JSON格式的輸出，不要包含任何額外的文字或解釋。
"""

    print("\n開始生成新聞內容...")
    print("Step 3: 發送請求到 GPT")

    # 發送單一 GPT 請求
    gpt_messages = [{
        'role': 'user',
        'content': combined_prompt,
    }]

    max_retries = 3
    for retry_count in range(max_retries):
        try:
            # 使用 GPT-4 以獲得更好的輸出質量
            result = access_gpt(gpt_messages, model='gpt-4o')
            print("Step 4: 收到 GPT 回應")
            print(f"GPT回應預覽: {result[:200]}...")
            
            # 清理 GPT 回應中可能包含的 ```json 和結尾的 ``` 標記
            cleaned_result = result
            if "```json" in cleaned_result:
                print("檢測到 ```json 標記，正在清理...")
                cleaned_result = cleaned_result.replace("```json", "")
            
            if "```" in cleaned_result:
                print("檢測到結尾的 ``` 標記，正在清理...")
                cleaned_result = cleaned_result.replace("```", "")
            
            # 解析 JSON 響應
            output = json.loads(cleaned_result)
            print("Step 5: 成功解析 JSON 響應")
            
            # 打印生成內容的摘要
            print("\n生成內容摘要:")
            print(output)
            
            print("\n所有內容生成完成")
            return output
            
        except json.JSONDecodeError as e:
            print(f"嘗試 {retry_count + 1}/{max_retries} 失敗")
            print(f"JSON解析錯誤: {e}")
            print(f"原始GPT回應: {result}")
            print(f"清理後的回應: {cleaned_result}")
            if retry_count == max_retries - 1:
                raise
            print("重新嘗試生成...")
            continue
        except Exception as e:
            print(f"GPT請求錯誤: {e}")
            raise

def fetch_financial_data():
    PROMPT_FINANCIAL_DATA = None
    with open('prompt_financial_data.txt', 'r', encoding='utf-8') as file:
        PROMPT_FINANCIAL_DATA = file.read()

    gpt_messages = []
    gpt_messages.append({
        'role': 'user',
        'content': PROMPT_FINANCIAL_DATA,
    })

    financial_data = access_gpt(gpt_messages)
    return financial_data

    
def run_news_gen(keyword_taiwan_news):
    derivative_articles_and_storyboards = extract_keyword_news_fact(keyword_taiwan_news)
    return derivative_articles_and_storyboards

if __name__ == '__main__':
    run_news_gen()  # 這裡可以保留原本的測試邏輯