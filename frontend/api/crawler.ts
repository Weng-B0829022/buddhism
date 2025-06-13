// 前端爬蟲工具 - 調用 Django NewsScrapeView

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000'

// 單篇文章爬蟲 - 通過 NewsScrapeView 處理單篇文章
export const scrapeArticleContent = async (url: string): Promise<string | null> => {
    try {
        console.log("通過後端抓取文章內容...");
        console.log(`網址: ${url}`);
        console.log(`後端地址: ${BACKEND_URL}`);
        
        // 構建單篇文章的請求格式
        const requestData = {
            metadata: {
                keyword: '單篇文章',
                timestamp: new Date().toISOString()
            },
            newsApi: [{
                title: '單篇文章',
                link: url,
                source: '未知來源',
                snippet: ''
            }]
        };
        
        const response = await fetch(`${BACKEND_URL}/create/news-scrape/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestData)
        });
        
        if (response.ok) {
            const data = await response.json();
            if (data.status === 'success' && data.articles && data.articles.length > 0) {
                const content = data.articles[0].content;
                console.log(`✓ 成功! 擷取到 ${content.length} 字`);
                return content;
            } else {
                console.log(`✗ 失敗: 無法取得文章內容`);
                return null;
            }
        } else {
            console.log(`✗ API 錯誤: ${response.status}`);
            return null;
        }
        
    } catch (error) {
        console.error("後端爬取錯誤:", error);
        return null;
    }
};

// 計算文章字數 - 對接 WordCountView
export const getWordCount = async (url: string): Promise<number> => {
    try {
        console.log("\n通過後端計算文章字數...");
        console.log(`網址: ${url}`);
        
        const response = await fetch(`${BACKEND_URL}/create/word-count/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url })
        });
        
        if (response.ok) {
            const data = await response.json();
            console.log(`✓ 成功! 文章字數: ${data.word_count}`);
            return data.word_count || 0;
        } else {
            console.log(`✗ API 錯誤: ${response.status}`);
            return 0;
        }
        
    } catch (error) {
        console.error("字數計算錯誤:", error);
        return 0;
    }
};

// 批次處理多個新聞 - 對接 NewsScrapeView
export const batchScrapeNews = async (newsItems: Array<{
    title: string;
    link: string;
    source: string;
}>): Promise<any> => {
    try {
        console.log(`\n通過後端批次處理 ${newsItems.length} 篇新聞`);
        console.log("=".repeat(50));
        
        // 構建發送給後端的數據格式（對應 Django NewsScrapeView）
        const requestData = {
            metadata: {
                keyword: '新聞批次處理',
                timestamp: new Date().toISOString()
            },
            newsApi: newsItems.map(item => ({
                title: item.title,
                link: item.link,
                source: item.source,
                snippet: '' // 可選
            }))
        };
        
        const response = await fetch(`${BACKEND_URL}/create/news-scrape/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestData)
        });
        
        if (response.ok) {
            const data = await response.json();
            if (data.status === 'success') {
                console.log("✓ 批次爬蟲成功!");
                console.log(`- 成功: ${data.stats.success} 篇`);
                console.log(`- 失敗: ${data.stats.failed} 篇`);
                console.log(`- 訊息: ${data.message}`);
                return data;
            } else {
                console.log(`✗ 批次爬蟲失敗: ${data.error}`);
                return null;
            }
        } else {
            console.log(`✗ API 錯誤: ${response.status}`);
            return null;
        }
        
    } catch (error) {
        console.error("批次處理錯誤:", error);
        return null;
    }
};

// 導出主要函數
export { scrapeArticleContent as default };
