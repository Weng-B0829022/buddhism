import React, { useState, useEffect } from 'react';

// 控制是否使用mock模式
const USE_MOCK = true;
// 定義分鏡稿數據的接口
interface StoryboardScene {
    畫面描述: string;
    [key: string]: any; // 允許其他可能的屬性
}

// 定義生成圖像的接口
interface GeneratedImage {
    description: string;
    url: string;
    path: string;
    originalIndex: number;
}

// 定義組件 Props 的接口
interface RecommendationProps {
    storyboardData: StoryboardScene[];
    storyboardTitle: string;
    onImageSelect?: (groupIndex: number | string, imageUrl?: string) => void;
    setImgs_url?: (urls: string[]) => void;
}

// 定義選擇圖像狀態的接口
interface SelectedImages {
    [key: number]: number;
}

// 定義環境變量的接口
declare global {
    interface ImportMetaEnv {
        VITE_OPENAI_API_KEY?: string;
        VITE_LEONARDO_API_KEY?: string;
    }
    
    interface ImportMeta {
        readonly env: ImportMetaEnv;
    }
}



// Mock圖片列表 - 每個分鏡稿會推薦4張圖片
const MOCK_IMAGES = [
    '/image1.png',
    '/image2.png',
    '/image3.png',
    '/image4.png',
];


const Recommendation: React.FC<RecommendationProps> = ({ 
    storyboardData, 
    storyboardTitle, 
    onImageSelect, 
    setImgs_url 
}) => {
    const [generatedImages, setGeneratedImages] = useState<GeneratedImage[]>([]);
    const [isGeneratingImages, setIsGeneratingImages] = useState<boolean>(false);
    const [selectedImages, setSelectedImages] = useState<SelectedImages>({});
    const [hasGeneratedOnce, setHasGeneratedOnce] = useState<boolean>(false);

    // 添加翻譯函數
    const translateToEnglish = async (text: string): Promise<string> => {
        try {
            const response = await fetch('https://api.openai.com/v1/chat/completions', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${process.env.NEXT_PUBLIC_OPENAI_API_KEY}`
                },
                body: JSON.stringify({
                    model: "gpt-3.5-turbo",
                    messages: [
                        {
                            "role": "system", "content": "You are a helpful assistant that translates text to English and generates effective prompt phrases for news image generation. Given a news title or article content, you should first translate the input into fluent English, and then generate a descriptive prompt that can be used to create a relevant image. The prompt should focus on the key people, places, actions, and emotions involved in the news story. "
                        },
                        { 
                            "role": "user", "content": `${text}`
                        }
                        
                    ],
                    max_tokens: 200,
                    temperature: 0.5
                })
            });
            const data = await response.json();
            return data.choices[0].message.content.trim();
        } catch (error) {
            console.error('Translation failed:', error);
            return text; // 如果翻譯失敗，返回原文
        }
    };

    // 生成圖片
    const generateImages = async (): Promise<void> => {
        if (storyboardData.length === 0 || hasGeneratedOnce) return;
        
        setIsGeneratingImages(true);
        try {
            if (USE_MOCK) {
                // 使用mock圖片 - 每個分鏡稿生成4張圖片
                const mockImages = storyboardData.flatMap((scene: StoryboardScene, sceneIndex: number) => {
                    return MOCK_IMAGES.map((mockImage, imageIndex) => ({
                        description: scene.畫面描述,
                        url: mockImage,
                        path: mockImage,
                        originalIndex: sceneIndex
                    }));
                });
                setGeneratedImages(mockImages);
                setHasGeneratedOnce(true);
                return;
            }

            // 準備要發送的數據
            const imageDescriptions = storyboardData.map((scene: StoryboardScene) => scene.畫面描述);
            
            // 翻譯所有描述
            const translatedDescriptions = await Promise.all(
                imageDescriptions.map((description: string) => translateToEnglish(description))
            );

            const generationPromises = translatedDescriptions.map((description: string) => 
                fetch('https://cloud.leonardo.ai/api/rest/v1/generations', {
                    method: 'POST',
                    headers: {
                        'accept': 'application/json',
                        'content-type': 'application/json',
                        'Authorization': `Bearer ${process.env.NEXT_PUBLIC_LEONARDO_API_KEY}`
                    },
                    body: JSON.stringify({
                        prompt: description,
                        modelId: "aa77f04e-3eec-4034-9c07-d0f619684628",
                        width: 1024,
                        height: 768,
                        num_images: 4,
                        guidance_scale: 7,
                        num_inference_steps: 30,
                        alchemy: true,
                        photoReal: true,
                        expandedDomain: true,
                        photoRealVersion: "v2",
                        public: false,
                        negative_prompt: "low resolution, bad quality, unrealistic"
                    }),
                })
            );

            // 並行發送所有請求
            const responses = await Promise.all(generationPromises);
            const results = await Promise.all(responses.map(response => response.json()));
            
            // 獲取所有生成ID
            const generationIds = results.map(result => result.sdGenerationJob?.generationId).filter(Boolean);
            
            if (generationIds.length > 0) {
                // 為每個描述輪詢獲取生成的圖片
                const allImages = await Promise.all(
                    generationIds.map((id: string, index: number) => 
                        pollForGeneratedImages(id, [translatedDescriptions[index]])
                    )
                );
                
                // 將所有圖片結果扁平化並設置
                const flattenedImages = allImages.flat();
                setGeneratedImages(flattenedImages);
                setHasGeneratedOnce(true);
            }
        } catch (error) {
            console.error('Error generating images:', error);
        } finally {
            setIsGeneratingImages(false);
        }
    };

    // 輪詢獲取生成的圖片
    const pollForGeneratedImages = async (generationId: string, imageDescriptions: string[]): Promise<GeneratedImage[]> => {
        const maxAttempts = 40;
        const delayMs = 5000; // 5秒
        
        for (let attempt = 0; attempt < maxAttempts; attempt++) {
            try {
                const response = await fetch(`https://cloud.leonardo.ai/api/rest/v1/generations/${generationId}`, {
                    headers: {
                        'accept': 'application/json',
                        'Authorization': `Bearer ${process.env.NEXT_PUBLIC_LEONARDO_API_KEY}`
                    }
                });
                
                if (!response.ok) {
                    const errorData = await response.json();
                    console.error(`Poll attempt ${attempt + 1} failed:`, errorData);
                    throw new Error(`Failed to fetch generation status: ${errorData.error || response.statusText}`);
                }
                
                const result = await response.json();
                const generatedImages = result.generations_by_pk?.generated_images || [];
                
                if (generatedImages.length > 0) {
                    return generatedImages.map((img: any) => ({
                        description: imageDescriptions[0],
                        url: img.url,
                        path: `generated_${generationId}_${img.id}.png`,
                        originalIndex: storyboardData.findIndex((scene: StoryboardScene) => scene.畫面描述 === imageDescriptions[0])
                    }));
                }
                
                await new Promise(resolve => setTimeout(resolve, delayMs));
            } catch (error) {
                console.error(`Attempt ${attempt + 1} failed:`, error);
                await new Promise(resolve => setTimeout(resolve, delayMs));
            }
        }
        
        console.error('Failed to get generated images after maximum attempts');
        return [];
    };

    // 當分鏡稿數據變化時，只在首次生成圖片
    useEffect(() => {
        if (storyboardData.length > 0 && !hasGeneratedOnce) {
            generateImages();
        }
    }, [storyboardData]);

    const handleImageSelect = (groupIndex: number, imageIndex: number | string): void => {
        // 檢查是否是直接傳入 URL（從 SearchImg 來的情況）
        if (typeof imageIndex === 'string') {
            // 直接使用 URL
            if (onImageSelect) {
                onImageSelect(imageIndex);
            }
            return;
        }

        setSelectedImages(prev => {
            const newSelected = { ...prev };
            
            // 如果點擊的是已選中的圖片，則取消選擇
            if (prev[groupIndex] === imageIndex) {
                delete newSelected[groupIndex];
            } else {
                // 否則更新選擇
                newSelected[groupIndex] = imageIndex;
            }
            
            return newSelected;
        });

        // 調用父組件的回調函數
        if (onImageSelect) {
            const imageGroup = generatedImages.slice(groupIndex * 4, (groupIndex + 1) * 4);
            const selectedImageUrl = imageGroup[imageIndex].url;
            onImageSelect(groupIndex, selectedImageUrl);
        }
    };

    return (
        <div className="mt-4">
            <h1 className="text-lg font-bold mb-2">推薦圖片</h1>
            <p className="text-sm text-gray-600 mb-2">可選擇 {storyboardData.length} 張圖片</p>
            {isGeneratingImages ? (
                <div className="flex items-center justify-center h-40">
                    <div className="animate-spin h-8 w-8 border-2 border-blue-500 rounded-full border-t-transparent"></div>
                    <p className="ml-2">正在生成圖片...</p>
                </div>
            ) : (
                <div className="grid grid-cols-1 gap-2 max-h-96 overflow-y-auto">
                    {generatedImages.length > 0 ? (
                        [...generatedImages]
                            .sort((a, b) => a.originalIndex - b.originalIndex)
                            .reduce((acc: GeneratedImage[][], image: GeneratedImage, index: number) => {
                                const groupIndex = Math.floor(index / 4);
                                if (!acc[groupIndex]) {
                                    acc[groupIndex] = [];
                                }
                                acc[groupIndex].push(image);
                                return acc;
                            }, [])
                            .map((imageGroup: GeneratedImage[], groupIndex: number) => (
                                <div 
                                    key={groupIndex}
                                    className="flex flex-col gap-2 mb-4"
                                >
                                    <div className="w-full text-left font-medium">
                                        段落 {groupIndex}
                                    </div>
                                    <div className="flex gap-2">
                                        {imageGroup.map((image: GeneratedImage, imageIndex: number) => (
                                            <div 
                                                key={imageIndex}
                                                className={`relative cursor-pointer transition-all ${
                                                    selectedImages[groupIndex] === imageIndex
                                                        ? 'ring-2 ring-blue-500 rounded-lg' 
                                                        : 'hover:opacity-80'
                                                }`}
                                                onClick={() => handleImageSelect(groupIndex, imageIndex)}
                                            >
                                                <img 
                                                    src={image.url}
                                                    alt={`推薦圖片 ${groupIndex + 1}-${imageIndex + 1}`}
                                                    className="w-[100px] h-[50px] object-cover rounded"
                                                />
                                                {selectedImages[groupIndex] === imageIndex && (
                                                    <div className="absolute top-1 right-1 bg-blue-500 text-white rounded-full w-5 h-5 flex items-center justify-center text-xs">
                                                        ✓
                                                    </div>
                                                )}
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            ))
                    ) : (
                        <div className="text-center p-4">
                            <p>沒有可用的推薦圖片</p>
                            <button 
                                onClick={generateImages}
                                className="mt-2 bg-blue-500 hover:bg-blue-700 text-white font-bold py-1 px-3 rounded text-sm"
                            >
                                重新生成圖片
                            </button>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
};

export default Recommendation;
