"use client"
import React, { useEffect, useState } from 'react';
import TopicInput from '../../components/TopicInput';
import NewsModal from '../../components/NewsModal';
import { getWordCount } from '../../api/getWordCount';
import useSnack from '../../hooks/useSnack';
import { extractKeywordNewsFact } from '../../utils/newsProcessor';
import newsProcessor from '../../utils/newsProcessor';
// Type definitions

interface SearchResult {
    title: string;
    link: string;
    snippet: string;
    date?: string;
}

interface NewsItem {
    title: string;
    link: string;
    snippet: string;
    source: string;
}

interface ProgressState {
    message: string;
    elapsedTime: number;
    isComplete: boolean;
}

interface WordCounts {
    [index: number]: number;
}

interface LoadingStates {
    [index: number]: boolean;
}

interface ComponentState {
    topicKeyword: string;
    selectedSources: string[];
}


const NEWS_SOURCES = [
    { value: 'cnn.com', label: 'CNN News' }
];

// 移除不需要的型別定義

// Mock API endpoints (you'll need to import these from your actual API file)
const API_BASE_URL = process.env.NEXT_PUBLIC_BACKEND_URL;


// 使用真實的字數計算函數
const getWords = async (link: string): Promise<number> => {
    try {
        return await getWordCount(link);
    } catch (error) {
        console.error('Error getting words:', error);
        return 0;
    }
};


// Mock SnackContainer component
const SnackContainer: React.FC<{snacks: Array<{id: string, message: string, type: string}>}> = ({ snacks }) => null;

const Create = () => {
    // === 搜索相關狀態 ===
    const [searchResults, setSearchResults] = useState<SearchResult[] | null>(null);
    const [isSearching, setIsSearching] = useState<boolean>(false);
    const [noContent, setNoContent] = useState<string | null>(null);
    const [state, setState] = useState<ComponentState>({
        topicKeyword: '',
        selectedSources: [] // 移除預設全選
    });

    // === 新聞選擇相關狀態 ===
    const [selectedNews, setSelectedNews] = useState<SearchResult[]>([]);
    const [wordCounts, setWordCounts] = useState<WordCounts>({});
    const [isLoadingWordCount, setIsLoadingWordCount] = useState<LoadingStates>({});
    const [totalWordCount, setTotalWordCount] = useState<number>(0);
    const [observer, setObserver] = useState<IntersectionObserver | null>(null);

    // === 生成相關狀態 ===
    const [isGenerating, setIsGenerating] = useState<boolean>(false);
    const [progress, setProgress] = useState<ProgressState>({
        message: '',
        elapsedTime: 0,
        isComplete: false
    });
    const [timer, setTimer] = useState<NodeJS.Timeout | null>(null);

    // === UI 狀態 ===
    const [isModalOpen, setIsModalOpen] = useState<boolean>(false);
    const { snacks, showSnack } = useSnack();

    // Mock navigation functions
    const navigate = (path: string) => {
        console.log('Navigate to:', path);
        // Replace with actual navigation logic
    };
    
    // Mock useParams
    const id = 'mock-id';

    const updateState = (key: keyof ComponentState, value: string | string[]) => {
        setState(prev => ({
            ...prev,
            [key]: value
        }));
    };

    const handleGenerateResult = async () => {
        if (selectedNews.length < 1) {
            showSnack('請至少選擇1則新聞', 'error');
            return;
        }
    
        setIsGenerating(true);
        setProgress({
            message: '正在生成分鏡稿中',
            elapsedTime: 0,
            isComplete: false
        });
    
        // 設置計時器
        const newTimer = setInterval(() => {
            setProgress(prev => ({
                ...prev,
                elapsedTime: prev.elapsedTime + 1
            }));
        }, 1000);
        setTimer(newTimer);
    
        try {
            // 準備要傳送的資料
            const contentData = {
                metadata: {
                    id: id,
                    timestamp: new Date().toISOString(),
                    keyword: state.topicKeyword
                },
                newsApi: selectedNews.map(news => ({
                    title: news.title,
                    link: news.link,
                    snippet: news.snippet,
                    source: NEWS_SOURCES.find(
                        source => new URL(news.link).hostname.includes(source.value)
                    )?.label || new URL(news.link).hostname
                }))
            };
    
            // 發送 POST 請求到後端
            const response = await fetch(`${API_BASE_URL + '/create/news-scrape/'}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(contentData)
            });
    
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            await extractKeywordNewsFact(data);
            
            // 保存分镜稿数据到 localStorage
            if (data && data.storyboard) {
                const storyboardData = {
                    title: data.title || state.topicKeyword,
                    avatar: data.avatar || "man1",
                    avatarType: data.avatarType || "half",
                    background: data.background || "background1",
                    storyboard: data.storyboard || [],
                    random_id: data.random_id || Date.now().toString(),
                    timestamp: new Date().toISOString()
                };
                
                localStorage.setItem('currentStoryboard', JSON.stringify(storyboardData));
                console.log('Storyboard saved to localStorage:', storyboardData);
            }
            
        } catch (error) {
            console.error('Error processing selected news:', error);
            showSnack('處理選擇的新聞時發生錯誤', 'error');
        } finally {
            setIsGenerating(false);
            // 清除計時器
            if (newTimer) {
                clearInterval(newTimer);
            }

            window.location.href = `/generate`;
        }
    };

    const handleSearch = async () => {
        if (!state.topicKeyword.trim()) {
            showSnack('請輸入關鍵字', 'error');
            return;
        }
        setSelectedNews([]);
        setIsSearching(true);
        try {
            // 簡化搜尋查詢，只使用關鍵字和單一新聞源
            let searchQuery = state.topicKeyword;

            // 使用唯一的新聞來源
            const selectedSources = NEWS_SOURCES.map(source => source.value);

            // 構建站點查詢字符串
            const sitesQuery = selectedSources
                .map(site => `site:${site}`)
                .join(' OR ');

            searchQuery = `${searchQuery} (${sitesQuery})`;
            
            console.log('Search Query:', searchQuery); // 用於調試

            const response = await fetch('https://google.serper.dev/search', {
                method: 'POST',
                headers: {
                    'X-API-KEY': '4c93a675a581d2f8e8064bc938d2433fd88fb6f1',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    q: searchQuery,
                    location: "Taiwan",
                    "num": 50,
                    gl: "tw",
                    hl: "zh-tw"
                })
            });
    
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
    
            const data = await response.json();
            if (!data.organic || data.organic.length === 0) {
                setSearchResults(null);
                setNoContent('沒有找到相關新聞');
                setIsModalOpen(false);
                return;
            }
            setSearchResults(data.organic);
            setIsModalOpen(true);
            
            // 移除自動選取前15個新聞
            // 改為在搜尋結果出現後依序選取前5個
            // const first5News = data.organic.slice(0, 5);
            
            // // 使用 Promise.all 和 setTimeout 來依序選取新聞
            // for (let i = 0; i < first5News.length; i++) {
            //     setTimeout(async () => {
            //         await handleNewsSelection(first5News[i], i);
            //     }, i * 10); // 每500毫秒選取一個新聞
            // }

        } catch (error) {
            console.error('搜尋錯誤:', error);
            showSnack('搜尋時發生錯誤', 'error');
        } finally {
            setIsSearching(false);
        }
    };

    // 移除不需要的函數，因為只有一個新聞源

    const getSourceLabel = (link: string): string => {
        try {
            const hostname = new URL(link).hostname;
            return NEWS_SOURCES.find(source => hostname.includes(source.value))?.label || hostname;
        } catch (error) {
            console.error('Invalid URL:', link);
            return '未知來源';
        }
    };

    // Add this function to handle word count
    const handleWordCount = async (link: string, index: number): Promise<number> => {
        if (isLoadingWordCount[index] || wordCounts[index] !== undefined) {
            return wordCounts[index] || 0;
        }

        setIsLoadingWordCount(prev => ({ ...prev, [index]: true }));
        try {
            const result = await getWords(link);
            const wordCount = Number(result) || 0; // 确保结果是数字
            setWordCounts(prev => ({ ...prev, [index]: wordCount }));
            return wordCount;
        } catch (error) {
            console.error('Error counting words:', error);
            return 0;
        } finally {
            setIsLoadingWordCount(prev => ({ ...prev, [index]: false }));
        }
    };

    // 在選擇新聞時自動計算字數
    const handleNewsSelection = async (result: SearchResult, index: number): Promise<void> => {
        if (selectedNews.some(news => news.link === result.link)) {
            // 取消選擇
            setSelectedNews(prev => prev.filter(news => news.link !== result.link));
            setTotalWordCount(prev => prev - (wordCounts[index] || 0));
        } else {
            if (selectedNews.length >= 15) {
                showSnack('最多只能選擇15則新聞', 'error');
                return;
            }

            // 如果還沒計算過字數，先計算
            let currentWordCount = wordCounts[index];
            if (currentWordCount === undefined) {
                currentWordCount = await handleWordCount(result.link, index);
            }

            // 檢查總字數是否會超過20000
            const newTotalWordCount = totalWordCount + (currentWordCount || 0); // 添加 || 0 防止 NaN
            if (newTotalWordCount > 20000) {
                showSnack('選擇的新聞總字數不能超過20000字', 'error');
                return;
            }

            // 新增選擇
            setSelectedNews(prev => [...prev, result]);
            setTotalWordCount(newTotalWordCount);
        }
    };

    // 處理移除新聞
    const handleRemoveNews = (link: string): void => {
        const newsIndex = selectedNews.findIndex(news => news.link === link);
        if (newsIndex !== -1) {
            const wordCountToRemove = Object.values(wordCounts).find((_, index) => {
                return searchResults && searchResults[index]?.link === link;
            }) || 0;
            
            setSelectedNews(prev => prev.filter(news => news.link !== link));
            setTotalWordCount(prev => prev - wordCountToRemove);
        }
    };

    // 處理Modal關閉
    const handleModalClose = (): void => {
        setIsModalOpen(false);
        setSelectedNews([]); // 清空選擇的新聞
        setWordCounts({}); // 清空字數統計
        setTotalWordCount(0); // 重置總字數
        setIsLoadingWordCount({}); // 重置加載狀態
    };

    // 修改 useEffect，添加必要的依賴
    useEffect(() => {
        const options = {
            root: null,
            rootMargin: '0px',
            threshold: 0.5
        };

        const observerInstance = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const target = entry.target as HTMLElement;
                    const index = parseInt(target.dataset.index || '0');
                    const link = target.dataset.link || '';
                    
                    // 檢查是否已經在計算中或已有結果
                    if (link && 
                        wordCounts[index] === undefined && 
                        !isLoadingWordCount[index]) {
                        handleWordCount(link, index);
                    }
                    
                    // 如果已經有結果或正在計算，就取消觀察
                    if (wordCounts[index] !== undefined || isLoadingWordCount[index]) {
                        observerInstance.unobserve(entry.target);
                    }
                }
            });
        }, options);

        setObserver(observerInstance);

        return () => {
            if (observerInstance) {
                observerInstance.disconnect();
            }
        };
    }, [wordCounts, isLoadingWordCount]); // 添加依賴

    return (
        <>
            <SnackContainer snacks={snacks} />
            {/* 背景圖片容器 */}
            <div 
                className="min-h-screen w-full relative"
                style={{
                    backgroundImage: `url('/background.png')`,
                    backgroundSize: 'cover',
                    backgroundPosition: 'center',
                    backgroundRepeat: 'no-repeat'
                }}
            >
                {/* 毛玻璃效果的搜尋區域 */}
                <div className="flex items-center justify-center min-h-screen w-full">
                    <div 
                        className="w-[90%] h-[35vh] relative"
                        style={{
                            background: 'rgba(255, 255, 255, 0.1)',
                            backdropFilter: 'blur(10px)',
                            borderRadius: '20px',
                            border: '1px solid rgba(255, 255, 255, 0.2)',
                            boxShadow: '0 8px 32px 0 rgba(31, 38, 135, 0.37)'
                        }}
                    >
                        <div className="flex flex-col items-center justify-center h-full px-4 py-6">
                            <div className="text-center mb-6">
                                <h1 className="text-2xl sm:text-3xl lg:text-4xl font-bold mb-4 text-white drop-shadow-lg">
                                    新建內容
                                </h1>
                            </div>

                            <div className="w-full max-w-2xl">
                                <TopicInput
                                    topicKeyword={state.topicKeyword}
                                    selectedSources={state.selectedSources}
                                    updateState={updateState}
                                />
                            </div>

                            <div className="flex flex-col items-center gap-4 mt-6">
                                <div className="flex gap-2 w-full max-w-[480px] justify-center">
                                    <button 
                                        className={`bg-green-600 hover:bg-green-700 text-white px-8 py-3 rounded-lg text-lg font-medium shadow-lg backdrop-blur-sm ${isSearching ? 'opacity-50 cursor-not-allowed' : ''}`}
                                        onClick={handleSearch}
                                        disabled={isSearching}
                                    >
                                        {isSearching ? '搜尋中...' : '搜尋'}
                                    </button>
                                </div>
                            </div>

                            {noContent && (
                                <div className="mt-6 text-center">
                                    <p className="text-white text-lg drop-shadow-lg">
                                        {noContent}
                                    </p>
                                </div>
                            )}
                        </div>
                    </div>
                </div>

            {/* 使用新的NewsModal組件 */}
            <NewsModal 
                isOpen={isModalOpen}
                searchResults={searchResults}
                selectedNews={selectedNews}
                wordCounts={wordCounts}
                isLoadingWordCount={isLoadingWordCount}
                totalWordCount={totalWordCount}
                topicKeyword={state.topicKeyword}
                isGenerating={isGenerating}
                progress={progress}
                observer={observer}
                onClose={handleModalClose}
                onNewsSelection={handleNewsSelection}
                onGenerateResult={handleGenerateResult}
                onRemoveNews={handleRemoveNews}
                getSourceLabel={getSourceLabel}
            />
            </div>
        </>
        );
};

export default Create;