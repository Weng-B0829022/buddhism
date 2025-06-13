import { 
    StoryboardScene, 
    ProcessedStoryboard, 
    StoryboardDataResult, 
    Article 
} from '../types/storyboard';

/**
 * StoryboardProcessor - 分鏡稿處理器
 * 
 * 用於處理和轉換分鏡稿數據的工具對象
 */
export const StoryboardProcessor = {
    /**
     * 將分鏡稿文本轉換為JSON格式
     */
    convertStoryboardToJson(storyboardText: string | string[]): StoryboardScene[] {
        // 檢查輸入是否為數組
        if (Array.isArray(storyboardText)) {
            return storyboardText.map((scene: string, index: number) => {
                // 解析每個場景字符串
                const lines = scene.split('\n');
                const timeCode = lines[1] || '';
                let visualElement = '';
                let voiceoverText = '';
                
                for (let i = 2; i < lines.length; i++) {
                    if (lines[i].startsWith('Image:') || lines[i].startsWith('Video:')) {
                        visualElement = lines[i];
                    } else if (lines[i].startsWith('Voiceover Text:')) {
                        voiceoverText = lines[i].split('Voiceover Text:')[1].trim();
                    }
                }
                
                return {
                    sceneNumber: index + 1,
                    timeCode: timeCode,
                    visualElements: visualElement ? [{
                        type: visualElement.toLowerCase().startsWith('image:') ? 'image' : 'video',
                        content: visualElement.split(':')[1].trim()
                    }] : [],
                    voiceoverText: voiceoverText.replace(/^"|"$/g, '')
                };
            });
        } else if (typeof storyboardText === 'string') {
            // 保留原有的字符串處理邏輯作為備用
            const cleanedText = "\n\n" + storyboardText;
            const scenes = cleanedText.split("\n\n").filter(Boolean);
            return scenes.map((scene: string, index: number) => {
                const lines = scene.trim().split('\n');
                const timeCode = lines[1];
                let visualElement = '';
                let voiceoverText = '';
                
                for (let i = 1; i < lines.length; i++) {
                    if (lines[i].startsWith('Image:') || lines[i].startsWith('Video:')) {
                        visualElement = lines[i];
                    } else if (lines[i].startsWith('Voiceover Text:')) {
                        voiceoverText = lines[i].split('Voiceover Text:')[1].trim();
                    }
                }
                
                return {
                    sceneNumber: index + 1,
                    timeCode: timeCode,
                    visualElements: visualElement ? [{
                        type: visualElement.toLowerCase().startsWith('image:') ? 'image' : 'video',
                        content: visualElement.split(':')[1].trim()
                    }] : [],
                    voiceoverText: voiceoverText.replace(/^"|"$/g, '')
                };
            });
        } else {
            console.error('Invalid storyboard format:', storyboardText);
            return [];
        }
    },

    /**
     * 將文章數據轉換為JSON格式
     */
    convertArticlesToJson(data: any): ProcessedStoryboard[] {
        console.log('🔧 StoryboardProcessor.convertArticlesToJson 接收數據:', data);
        
        // 處理新的數據結構 (直接包含 articles)
        if (data && data.articles && Array.isArray(data.articles)) {
            console.log('✅ 檢測到直接的 articles 數組');
            const articles = data.articles;
            return articles.map((article: Article) => ({
                title: article.title,
                content: article.content,
                storyboard: this.convertStoryboardToJson(article.storyboard)
            }));
        }
        
        // 處理舊的數據結構 (generated_content.articles)
        if (data && data.generated_content && data.generated_content.articles) {
            console.log('✅ 檢測到 generated_content.articles 結構');
            const articles = data.generated_content.articles;
            return articles.map((article: Article) => ({
                title: article.title,
                content: article.content,
                storyboard: this.convertStoryboardToJson(article.storyboard)
            }));
        }
        
        console.error('❌ 無效的數據結構:', data);
        return [];
    },

    /**
     * 將文章JSON轉換為分鏡稿數據格式
     */
    convertToStoryboardData(input: ProcessedStoryboard): StoryboardDataResult | null {
        if (!input || typeof input !== 'object') {
            console.error('Invalid input: expected an object');
            return null;
        }
    
        const defaultScene: StoryboardScene = {
            sceneNumber: 0,
            timeCode: '0',
            visualElements: [{ type: 'image', content: 'No description available' }],
            voiceoverText: ''
        };
    
        return {
            title: input.title || 'Untitled',
            content: input.content || '',
            storyboard: Array.isArray(input.storyboard) ? input.storyboard.map((scene: StoryboardScene, index: number) => {
                const safeScene = { ...defaultScene, ...scene };
                return {
                    段落: (index).toString().padStart(2, '0'),
                    秒數: safeScene.timeCode,
                    畫面描述: safeScene.visualElements[0]?.content || 'No description available',
                    旁白: (safeScene.voiceoverText || '').replace(/^「|」$/g, ''),
                    字數: `${(safeScene.voiceoverText || '').replace(/^「|」$/g, '').length}字`
                };
            }) : []
        };
    },
};

/**
 * 計算時間碼的持續時間（毫秒）
 */
export function calculateDuration(timeString: string): number {
    // 清除字符串中的所有空格
    timeString = timeString.replace(/\s/g, '');
    
    // 分割時間字符串
    const [startTime, endTime] = timeString.split('-->');
    
    // 將時間轉換為毫秒
    function timeToMilliseconds(t: string): number {
        const [time, ms] = t.split(',');
        const [h, m, s] = time.split(':');
        return parseInt(h) * 3600000 + parseInt(m) * 60000 + parseInt(s) * 1000 + parseInt(ms);
    }
    
    // 計算開始和結束時間（毫秒）
    const startMs = timeToMilliseconds(startTime);
    const endMs = timeToMilliseconds(endTime);
    
    // 計算並返回持續時間（毫秒）
    return endMs - startMs;
} 