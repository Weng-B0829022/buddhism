const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL;
// 計算文章字數的函數 - 調用後端 API
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