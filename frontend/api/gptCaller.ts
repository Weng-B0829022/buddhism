// 簡單的 GPT API 調用工具

// 調用 GPT API
export const callGPT = async (prompt: string): Promise<string> => {
    const apiKey = process.env.NEXT_PUBLIC_OPENAI_API_KEY;
    
    if (!apiKey) {
        throw new Error('請設置 NEXT_PUBLIC_OPENAI_API_KEY 環境變數');
    }

    try {
        const response = await fetch('https://api.openai.com/v1/chat/completions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${apiKey}`,
            },
            body: JSON.stringify({
                model: 'gpt-4o-mini',
                messages: [
                    {
                        role: 'user',
                        content: prompt
                    }
                ],
                max_tokens: 10000,
                temperature: 0.7
            })
        });

        if (!response.ok) {
            throw new Error(`API 錯誤: ${response.status}`);
        }

        const data = await response.json();
        return data.choices[0].message.content;

    } catch (error) {
        console.error('GPT API 調用失敗:', error);
        throw new Error('GPT API 調用失敗');
    }
};

export default callGPT;
