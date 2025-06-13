"use client"
import React, { useState, useEffect } from 'react';
import { 
    StoryboardData, 
    Article, 
    CreatedContent 
} from '../../../types/storyboard';
import { LoadingSpinner, FullScreenLoading, ContentLoading } from '../../../components/LoadingSpinner';
import { Storyboard } from '../../../components/Storyboard';
import { StoryboardProcessor } from '../../../utils/storyboardProcessor';
import { loadScenesFromLocalStorage } from '../../../utils/localStorage';

// 生成預設圖片的工具函數
const createPlaceholderImage = (width: number, height: number, text: string = '請上傳圖片') => {
    const svg = `<svg width="${width}" height="${height}" xmlns="http://www.w3.org/2000/svg">
        <rect width="100%" height="100%" fill="#f0f0f0"/>
        <text x="50%" y="50%" font-family="Arial, sans-serif" font-size="${Math.min(width, height) / 8}" fill="#666666" text-anchor="middle" dominant-baseline="middle">${text}</text>
    </svg>`;
    return `data:image/svg+xml;utf8,${encodeURIComponent(svg)}`;
};

/**
 * Generate 組件 - 生成結果頁面
 * 
 * 顯示生成的新聞內容和分鏡稿，並提供編輯和生成視頻的功能
 */
const Generate: React.FC = () => {
    const [storyboardData, setStoryboardData] = useState<StoryboardData[]>([]);
    const [storyboardTitle, setStoryboardTitle] = useState<string>('');
    const [selectedDataIndex, setSelectedDataIndex] = useState<number>(0);
    const [generatedContent, setGeneratedContent] = useState<CreatedContent | null>(null);
    const [isEditMode, setIsEditMode] = useState<boolean>(false);
    const [scenes, setScenes] = useState<any>(null);
    const [availableArticles, setAvailableArticles] = useState<Article[]>([]);
    const [isLoading, setIsLoading] = useState<boolean>(true);
    const [isProcessing, setIsProcessing] = useState<boolean>(false);

    // 從 localStorage 載入數據
    useEffect(() => {
        console.log('🚀 useEffect: 開始載入 localStorage 數據');
        setIsLoading(true);
        
        // 模擬載入時間，讓用戶看到 loading 動畫
        setTimeout(() => {
            const loadedScenes = loadScenesFromLocalStorage();
            console.log('🎯 useEffect: 載入的場景數據:', loadedScenes);
            setScenes(loadedScenes);
            setIsLoading(false);
        }, 800);
    }, []);

    // 通用的數據處理函數
    const processDataToStoryboard = (data: any, dataSource: string) => {
        if (!data) {
            console.log(`⚠️ ${dataSource}: 數據為空`);
            setIsProcessing(false);
            return;
        }

        try {
            // 處理直接的 storyboard 格式數據
            if (data.storyboard && data.storyboard.length > 0) {
                console.log(`✅ ${dataSource}: 找到 storyboard 格式的數據`);
                setStoryboardTitle(data.title || '生成的分鏡稿');
                
                const convertedData: StoryboardData[] = data.storyboard.map((scene: any, index: number) => ({
                    段落: scene.paragraph || scene.段落 || (index + 1).toString().padStart(2, '0'),
                    秒數: scene.duration || scene.秒數 || '00:00:00,000 --> 00:00:05,000',
                    畫面: scene.imageUrl || scene.畫面 || createPlaceholderImage(300, 200),
                    畫面描述: scene.imageDescription || scene.畫面描述 || 'No description',
                    旁白: (scene.voiceover || scene.旁白 || '').replace(/'/g, ''),
                    字數: scene.avatarCount ? `${scene.avatarCount}字` : (scene.字數 || '0字'),
                    imageFile: null
                }));
                
                setStoryboardData(convertedData);
                setIsProcessing(false);
                return;
            }

            // 處理 articles 格式數據
            const articles = data.articles || data.generated_content?.articles;
            if (articles && articles.length > 0) {
                console.log(`✅ ${dataSource}: 找到 articles 格式的數據`, articles);
                
                setAvailableArticles(articles);
                
                const selectedArticle = articles[selectedDataIndex] || articles[0];
                if (selectedArticle?.storyboard?.length > 0) {
                    const mainTitle = data.main_article?.title || data.title || '生成的分鏡稿';
                    setStoryboardTitle(selectedArticle.title || mainTitle);
                    
                    const jsonResult = StoryboardProcessor.convertArticlesToJson(data);
                    if (jsonResult?.[selectedDataIndex]) {
                        const storyboardResult = StoryboardProcessor.convertToStoryboardData(jsonResult[selectedDataIndex]);
                        if (storyboardResult?.storyboard) {
                            console.log(`🎨 ${dataSource}: 轉換完成`, storyboardResult.storyboard);
                            setStoryboardData(storyboardResult.storyboard);
                            setIsProcessing(false);
                            return;
                        }
                    }
                }
            }

            // 處理只有 main_article 的情況
            if (data.main_article) {
                console.log(`📝 ${dataSource}: 只找到 main_article`);
                setStoryboardTitle(data.main_article.title || '生成的內容');
                setIsProcessing(false);
                return;
            }

            // 處理其他情況
            if (data.title && data.title !== "尚未生成分鏡稿") {
                console.log(`⚠️ ${dataSource}: 數據格式不符合預期，但有標題`);
                setStoryboardTitle(data.title);
            } else {
                console.log(`⚠️ ${dataSource}: 無有效數據`);
            }
            
        } catch (error) {
            console.error(`❌ ${dataSource}: 處理數據時發生錯誤:`, error);
        } finally {
            setIsProcessing(false);
        }
    };

    // 處理 scenes 數據變化
    useEffect(() => {
        if (!scenes) return;
        
        console.log('🔄 開始處理 scenes 數據', scenes);
        setIsProcessing(true);
        
        if (scenes.title === "尚未生成分鏡稿") {
            console.log('⚠️ scenes: 尚未生成分鏡稿');
            setIsProcessing(false);
            return;
        }

        processDataToStoryboard(scenes, 'localStorage');
    }, [scenes, selectedDataIndex]);

    // 處理 generatedContent 數據變化
    useEffect(() => {
        if (!generatedContent?.generated_content?.articles) return;
        
        console.log('🔄 開始處理 generatedContent 數據', generatedContent);
        setIsProcessing(true);
        processDataToStoryboard(generatedContent, 'generatedContent');
    }, [generatedContent, selectedDataIndex]);

    const handleSelectionChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
        setSelectedDataIndex(parseInt(event.target.value));
    };

    // 如果正在初始載入，顯示全屏 loading
    if (isLoading) {
        return <FullScreenLoading message="載入分鏡稿數據中..." />;
    }

    return (
        <div className="p-6">
            <div className="flex justify-between items-center">
                <div className="flex items-center">
                    <div className="mr-4">
                        <a href="/">
                            <svg width="24" height="24" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                            </svg>
                        </a>
                    </div>
                    <h1 className="text-3xl font-bold mb-0 ml-4">Express Mode 生成結果</h1>
                    {isProcessing && (
                        <LoadingSpinner size={24} className="ml-4" />
                    )}
                </div>
            </div>
            
            <div className="mb-4 mt-4 flex items-center flex-wrap gap-4">
                <div className="flex items-center">
                    <label htmlFor="storyboardSelect" className="mr-2">選擇新聞主題:</label>
                    {availableArticles.length > 0 ? (
                        <div className="flex items-center">
                            <select 
                                id="storyboardSelect"
                                value={selectedDataIndex} 
                                onChange={handleSelectionChange}
                                className="border rounded p-2 bg-white min-w-[300px]"
                                disabled={isProcessing}
                            >
                                {availableArticles.map((article, index) => (
                                    <option key={index} value={index}>
                                        {article.title || `文章 ${index + 1}`}
                                    </option>
                                ))}
                            </select>
                            {isProcessing && (
                                <LoadingSpinner size={20} className="ml-2" />
                            )}
                        </div>
                    ) : (
                        <div className="border rounded p-2 bg-gray-50">
                            {storyboardTitle || '載入中...'}
                        </div>
                    )}
                </div>
                {scenes?.random_id && (
                    <div className="text-sm text-gray-500">
                        ID: {scenes.random_id}
                    </div>
                )}
                {availableArticles.length > 0 && (
                    <div className="text-sm text-blue-600">
                        共 {availableArticles.length} 篇文章
                    </div>
                )}
            </div>
            
            {isProcessing ? (
                <ContentLoading message="正在處理分鏡稿數據..." />
            ) : !isEditMode ? (
                <Storyboard 
                    storyboardData={storyboardData}
                    storyboardTitle={storyboardTitle}
                    selectedIndex={selectedDataIndex}
                    isEditMode={isEditMode}
                    onStoryboardDataChange={setStoryboardData}
                />
            ) : (
                <div className="p-4 border rounded-lg">
                    <h2 className="text-xl font-bold mb-4">編輯模式</h2>
                    <p className="text-gray-600">編輯功能正在開發中...</p>
                </div>
            )}
        </div>
    );
};

export default Generate; 