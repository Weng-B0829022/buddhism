import React, { useState, useEffect } from 'react';
import { 
    StoryboardData, 
    StoryboardProps, 
    GenerationResult, 
    UploadInfo 
} from '../../types/storyboard';
import { SimpleModal } from '../SimpleModal';
import { calculateDuration } from '../../utils/storyboardProcessor';
import Recommendation from '../Recommendation';

// 生成預設圖片的工具函數
const createPlaceholderImage = (width: number, height: number, text: string = '請上傳圖片') => {
    const svg = `<svg width="${width}" height="${height}" xmlns="http://www.w3.org/2000/svg">
        <rect width="100%" height="100%" fill="#f0f0f0"/>
        <text x="50%" y="50%" font-family="Arial, sans-serif" font-size="${Math.min(width, height) / 8}" fill="#666666" text-anchor="middle" dominant-baseline="middle">${text}</text>
    </svg>`;
    return `https://picsum.photos/200/300`;
};

/**
 * Storyboard 組件 - 分鏡稿顯示組件
 */
export const Storyboard: React.FC<StoryboardProps> = ({ 
    storyboardData, 
    storyboardTitle, 
    selectedIndex, 
    isEditMode, 
    onStoryboardDataChange 
}) => {
    const [generatingVideo, setGeneratingVideo] = useState<boolean>(false);
    const [generationResult, setGenerationResult] = useState<GenerationResult | null>(null);
    const [uploadInfo, setUploadInfo] = useState<UploadInfo | null>(null);
    const [generationTime, setGenerationTime] = useState<number>(0);
    const [selectedAvatar, setSelectedAvatar] = useState<string>('man1-half-background1');
    const [randomId, setRandomId] = useState<string | null>(null);
    const [localStoryboardData, setLocalStoryboardData] = useState<StoryboardData[]>(storyboardData);
    const [imgs_url, setImgs_url] = useState<string[]>(Array(storyboardData.length).fill(createPlaceholderImage(139, 104)));
    const [popupImageUrl, setPopupImageUrl] = useState<string | null>(null);
    const [editingVoiceoverIndex, setEditingVoiceoverIndex] = useState<number | null>(null);
    const [editingVoiceoverText, setEditingVoiceoverText] = useState<string>('');
    const [isVoiceoverModalVisible, setIsVoiceoverModalVisible] = useState<boolean>(false);

    // 當 storyboardData 變化時更新本地狀態
    useEffect(() => {
        setLocalStoryboardData(storyboardData.map((scene: StoryboardData) => ({
            ...scene,
            imageFile: null
        })));
    }, [storyboardData]);

    useEffect(() => {
        let timer: NodeJS.Timeout | undefined;
        if (generatingVideo) {
            timer = setInterval(() => {
                setGenerationTime((prevTime) => prevTime + 1);
            }, 1000);
        } else {
            setGenerationTime(0);
        }

        return () => {
            if (timer) clearInterval(timer);
        };
    }, [generatingVideo]);

    useEffect(() => {
        setImgs_url(storyboardData.map((scene: StoryboardData) => 
            scene.畫面 || createPlaceholderImage(139, 104)
        ));
    }, [storyboardData]);

    // 添加將圖片轉換為 base64 的輔助函數
    const convertImageToBase64 = (imageUrl: string | File): Promise<string> => {
        return new Promise((resolve, reject) => {
            // 如果是文件對象，使用 FileReader
            if (imageUrl instanceof File) {
                const reader = new FileReader();
                reader.onload = () => resolve(reader.result as string);
                reader.onerror = reject;
                reader.readAsDataURL(imageUrl);
                return;
            }
            
            // 如果是 URL，先獲取圖片然後轉換
            fetch(imageUrl)
                .then(response => response.blob())
                .then(blob => {
                    const reader = new FileReader();
                    reader.onload = () => resolve(reader.result as string);
                    reader.onerror = reject;
                    reader.readAsDataURL(blob);
                })
                .catch(reject);
        });
    };

    const handleGenerateVideo = async () => {
        setGeneratingVideo(true);
        setGenerationResult(null);
        setGenerationTime(0);
        setUploadInfo(null);
        setRandomId(null);

        try {
            // 處理所有圖片
            const processedImages = await Promise.all(
                imgs_url.map(async (imageUrl: string, index: number) => {
                    // 如果是 URL，直接使用 URL
                    return imageUrl;
                })
            );

            // 準備要發送的數據
            const dataToSend = {
                title: storyboardTitle,
                avatar: selectedAvatar.split('-')[0],
                avatarType: selectedAvatar.split('-')[1],
                background: selectedAvatar.split('-')[2],
                storyboard: localStoryboardData.map((scene: StoryboardData, index: number) => {
                    return {
                        paragraph: scene.段落,
                        duration: scene.秒數,
                        calculatedDuration: calculateDuration(scene.秒數),
                        imageDescription: scene.畫面描述,
                        voiceover: scene.旁白,
                        avatarCount: parseInt(scene.字數.replace(/[^0-9]/g, '')),
                        imageUrl: processedImages[index],
                        needAvatar: index < 2
                    };
                })
            };

            const result = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/storyboard/gen-video`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(dataToSend)
            });
            
        } catch (error) {
            console.error('Error generating video:', error);
            setGenerationResult({ error: 'Failed to generate video' });
        } finally {
            setGeneratingVideo(false);
        }
    };

    const handleVoiceoverEdit = (index: number, text: string) => {
        setEditingVoiceoverIndex(index);
        setEditingVoiceoverText(text);
        setIsVoiceoverModalVisible(true);
    };

    const handleVoiceoverSave = () => {
        if (editingVoiceoverIndex === null) return;
        
        const newStoryboardData = [...localStoryboardData];
        newStoryboardData[editingVoiceoverIndex] = {
            ...newStoryboardData[editingVoiceoverIndex],
            旁白: editingVoiceoverText,
            字數: `${editingVoiceoverText.length}字`
        };
        setLocalStoryboardData(newStoryboardData);
        if (typeof onStoryboardDataChange === 'function') {
            onStoryboardDataChange(newStoryboardData);
        }
        setIsVoiceoverModalVisible(false);
        setEditingVoiceoverIndex(null);
    };

    // 處理 Recommendation 組件的圖片選擇
    const handleRecommendationImageSelect = (groupIndex: number | string, imageUrl?: string) => {
        if (typeof groupIndex === 'number' && imageUrl) {
            // 更新對應位置的圖片
            setImgs_url(prev => prev.map((url, i) => i === groupIndex ? imageUrl : url));
            console.log(`Selected image for scene ${groupIndex}: ${imageUrl}`);
        }
    };

    // 檢查是否所有圖片都已選擇
    const allImagesSelected = imgs_url.every(url => !url.includes('請上傳圖片'));

    const renderGenerationResult = () => {
        if (!generationResult) return null;

        return (
            <div className="mt-4 p-4 bg-gray-100 rounded-md">
                <h2 className="text-xl font-bold mb-2">生成結果：</h2>
                <div>{generationResult.message === 'success' 
                    ? (uploadInfo 
                        ? <div className="mt-4">
                            <p>{uploadInfo.uploadTitle}</p>
                            <video 
                                controls 
                                className="w-full max-w-2xl mt-2"
                                src={`${'/get-generated-video/'}?id=${randomId}`}
                            >
                                Your browser does not support the video tag.
                            </video>
                            <a 
                                href={`/admin/video/${randomId}`}
                                className="text-blue-500 hover:text-blue-700 underline"
                            >
                                在新頁面中查看影片
                            </a>
                        </div> :
                        <div className="flex items-center gap-2">
                            <div className="animate-spin h-5 w-5 border-2 border-blue-500 rounded-full border-t-transparent"></div>
                            <p>檔案正在上傳中</p>
                        </div>)
                    : <p>發生未知的錯誤 請重新生成</p>
                }</div>
                {generationResult.video_paths && (
                    <div className="mt-4">
                        <video 
                            controls 
                            className="w-full max-w-2xl mt-2"
                            src={`${'/get-generated-video/'}?id=${randomId}`}
                        >
                            Your browser does not support the video tag.
                        </video>
                    </div>
                )}
            </div>
        );
    };

    const headers = ['段落', '秒數', '畫面', '畫面描述', '旁白', '字數'];

    return (
        <div>
            <div className="overflow-x-auto p-3 sm:p-4 group mt-4 font-bold border-2 rounded-md">
                <div className='mb-4'>
                    <h1 className="text-3xl font-bold ml-2 mt-2">分鏡稿</h1>
                    <p className="mt-2 text-m ml-2 mb-2">為單則影片之分鏡稿，依選擇模式可進行不同程度的調整</p>
                </div>
                <div>
                    <div className="flex justify-between p-2 bg-white">
                        <div className='mr-4 p-2 ml-2'>
                            <div className='border border-gray-300 w-48 mb-4 rounded'>
                                <div className="flex justify-between">
                                    <h1 className="text-lg font-bold p-2">主標題</h1>
                                    {storyboardTitle && 
                                    <p className="text-lg p-2">
                                        {storyboardTitle}
                                    </p>}
                                </div>
                                <div className="flex justify-between">
                                    <h1 className="text-lg font-bold p-2">副標題</h1>
                                    <p className="text-lg p-2">這是副標題</p>
                                </div>
                            </div>
                            <div>
                                <h1 className="text-lg font-bold mb-2">主播</h1>
                                <select 
                                    value={selectedAvatar}
                                    onChange={(event) => setSelectedAvatar(event.target.value)}
                                    className="border rounded p-1 mb-2"
                                >
                                    <option value="man1-half-background1">林知曦(男性主播 1) 場景1</option>
                                    <option value="man2-half-background1">李澄風(男性主播 2) 場景1</option>
                                    <option value="man1-half-background2">林知曦(男性主播 1) 場景2</option>
                                    <option value="man2-half-background2">李澄風(男性主播 2) 場景2</option>
                                    <option value="woman1-full-background1">陳予恩(女性主播 1) </option>
                                    <option value="woman2-full-background1">張安晴(女性主播 2) </option>
                                </select>
                            </div>
                            
                            <div className="mt-4">
                                <Recommendation 
                                    storyboardData={localStoryboardData}
                                    storyboardTitle={storyboardTitle}
                                    onImageSelect={handleRecommendationImageSelect}
                                    setImgs_url={setImgs_url}
                                />
                            </div>
                            
                            <div className="mt-4">
                                <button 
                                    onClick={handleGenerateVideo}
                                    disabled={generatingVideo || !allImagesSelected}
                                    className={`bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded ${
                                        (generatingVideo || !allImagesSelected) ? 'opacity-50 cursor-not-allowed' : ''
                                    }`}
                                >
                                    {generatingVideo ? `生成中 (${generationTime}s)` : 
                                    !allImagesSelected ? '請選擇所有圖片' : '生成影片'}
                                </button>
                            </div>
                        </div>

                        <div className="pr-2 pb-2 overflow-x-auto">
                            <table className="min-w-full border-collapse mt-2 text-black">
                                <tbody>
                                    {headers.map((header, index) => (
                                    <tr key={header}>
                                        <th className="text-center border px-2 py-2">{header}</th>
                                        {storyboardData.map((scene: StoryboardData, sceneIndex: number) => (
                                        <td key={sceneIndex} className="text-center border px-2 py-2">
                                            {header === '畫面' ? (
                                                <div className="flex flex-col items-center">
                                                    <img 
                                                        src={imgs_url[sceneIndex]} 
                                                        alt={scene.畫面描述} 
                                                        className="w-28 h-20 object-cover mx-auto cursor-pointer hover:opacity-80 mb-2 rounded bg-black bg-opacity-30" 
                                                        style={{ backgroundColor: 'rgba(0,0,0,0.15)' }}
                                                        onClick={() => setPopupImageUrl(imgs_url[sceneIndex])}
                                                    />
                                                </div>
                                            ) : header === '旁白' ? (
                                                <div 
                                                    className="cursor-pointer hover:bg-gray-100 p-2 rounded transition-colors min-h-[80px] flex items-center justify-center"
                                                    onClick={() => handleVoiceoverEdit(sceneIndex, scene[header as keyof StoryboardData] as string)}
                                                >
                                                    {String(scene[header as keyof StoryboardData])}
                                                </div>
                                            ) : (
                                                String(scene[header as keyof StoryboardData] ?? '')
                                            )}
                                        </td>
                                        ))}
                                    </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
            {renderGenerationResult()}

            {/* 图片预览 Modal */}
            <SimpleModal
                isOpen={!!popupImageUrl}
                onClose={() => setPopupImageUrl(null)}
                title="圖片預覽"
                width={500}
            >
                {popupImageUrl && (
                    <div style={{ background: 'rgba(0,0,0,0.3)', borderRadius: '8px', padding: '12px', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
                        <img 
                            src={popupImageUrl} 
                            alt="Preview" 
                            style={{ width: '320px', height: '180px', objectFit: 'cover', background: 'rgba(0,0,0,0.15)', borderRadius: '6px' }}
                        />
                    </div>
                )}
            </SimpleModal>

            {/* 旁白編輯 Modal */}
            <SimpleModal
                isOpen={isVoiceoverModalVisible}
                onClose={() => {
                    setIsVoiceoverModalVisible(false);
                    setEditingVoiceoverIndex(null);
                }}
                title="編輯旁白"
                width={800}
            >
                <div className="space-y-4">
                    <textarea
                        value={editingVoiceoverText}
                        onChange={(e) => setEditingVoiceoverText(e.target.value)}
                        className="w-full p-4 border rounded resize-none focus:outline-none focus:ring-2 focus:ring-blue-500"
                        rows={10}
                        style={{ minHeight: '300px' }}
                    />
                    <div className="text-gray-500">
                        字數：{editingVoiceoverText.length} 字
                    </div>
                    <div className="flex justify-end space-x-2">
                        <button
                            onClick={() => {
                                setIsVoiceoverModalVisible(false);
                                setEditingVoiceoverIndex(null);
                            }}
                            className="bg-gray-500 hover:bg-gray-600 text-white px-4 py-2 rounded"
                        >
                            取消
                        </button>
                        <button
                            onClick={handleVoiceoverSave}
                            className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded"
                        >
                            保存
                        </button>
                    </div>
                </div>
            </SimpleModal>
        </div>
    );
}; 