import React from 'react';

// 類型定義
interface SearchResult {
    title: string;
    link: string;
    snippet: string;
    date?: string;
}

interface WordCounts {
    [index: number]: number;
}

interface LoadingStates {
    [index: number]: boolean;
}

interface ProgressState {
    message: string;
    elapsedTime: number;
    isComplete: boolean;
}

interface NewsModalProps {
    isOpen: boolean;
    searchResults: SearchResult[] | null;
    selectedNews: SearchResult[];
    wordCounts: WordCounts;
    isLoadingWordCount: LoadingStates;
    totalWordCount: number;
    topicKeyword: string;
    isGenerating: boolean;
    progress: ProgressState;
    observer: IntersectionObserver | null;
    onClose: () => void;
    onNewsSelection: (result: SearchResult, index: number) => void;
    onGenerateResult: () => void;
    onRemoveNews: (link: string) => void;
    getSourceLabel: (link: string) => string;
}

const NewsModal: React.FC<NewsModalProps> = ({
    isOpen,
    searchResults,
    selectedNews,
    wordCounts,
    isLoadingWordCount,
    totalWordCount,
    topicKeyword,
    isGenerating,
    progress,
    observer,
    onClose,
    onNewsSelection,
    onGenerateResult,
    onRemoveNews,
    getSourceLabel
}) => {
    if (!isOpen || !searchResults) return null;

    return (
        <div 
            className="fixed inset-0 flex items-center justify-center p-4 z-50"
            style={{
                background: 'rgba(0, 0, 0, 0.3)',
                backdropFilter: 'blur(8px)',
                WebkitBackdropFilter: 'blur(8px)'
            }}
        >
            <div className="bg-white rounded-lg shadow-xl w-full max-w-6xl">
                <div className="flex justify-between items-center p-4 border-b">
                    <div>
                        <h2 className="text-lg font-semibold text-gray-800">
                            搜尋結果：{topicKeyword}
                        </h2>
                        <p className="text-sm text-gray-600">
                            已選擇 {selectedNews.length} 則新聞 {selectedNews.length < 1 && '(至少需選擇1則)'}
                        </p>
                    </div>
                </div>
                
                <div className="p-4">
                    <div className="max-h-[calc(100vh-400px)] overflow-y-auto">
                        <table className="min-w-full bg-white">
                            <thead className="bg-gray-100 sticky top-0">
                                <tr>
                                    <th className="px-2 py-1 text-left text-xs font-medium text-gray-600">選擇</th>
                                    <th className="px-2 py-1 text-left text-xs font-medium text-gray-600">新聞主題</th>
                                    <th className="px-2 py-1 text-left text-xs font-medium text-gray-600">關鍵字</th>
                                    <th className="px-2 py-1 text-left text-xs font-medium text-gray-600">日期(排序)</th>
                                    <th className="px-2 py-1 text-left text-xs font-medium text-gray-600">來源</th>
                                    <th className="px-2 py-1 text-left text-xs font-medium text-gray-600">字數</th>
                                    <th className="px-2 py-1 text-left text-xs font-medium text-gray-600">備註</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-gray-200">
                                {(searchResults || []).map((result, index) => (
                                    <tr 
                                        key={index} 
                                        className="hover:bg-gray-50"
                                        ref={el => {
                                            if (el && observer) {
                                                el.dataset.index = index.toString();
                                                el.dataset.link = result.link;
                                                observer.observe(el);
                                            }
                                        }}
                                    >
                                        <td className="px-1 py-1">
                                            <input
                                                type="checkbox"
                                                checked={selectedNews.some(news => news.link === result.link)}
                                                onChange={() => onNewsSelection(result, index)}
                                                className="rounded text-blue-600"
                                            />
                                        </td>
                                        <td className="px-1 py-1 text-xs text-gray-900">
                                            {result.title}
                                        </td>
                                        <td className="px-1 py-1 text-xs text-gray-900">
                                            {topicKeyword}
                                        </td>
                                        <td className="px-1 py-1 text-xs text-gray-900">
                                            {result.date || '日期未知'}
                                        </td>
                                        <td className="px-1 py-1 text-xs text-gray-900">
                                            {getSourceLabel(result.link)}
                                        </td>
                                        <td className="px-1 py-1 text-xs text-gray-900">
                                            {wordCounts[index] !== undefined ? (
                                                <span>{wordCounts[index]} 字</span>
                                            ) : (
                                                <span className="text-gray-400">
                                                    {isLoadingWordCount[index] ? '計算中...' : '等待計算'}
                                                </span>
                                            )}
                                        </td>
                                        <td className="px-1 py-1 text-xs text-gray-900">
                                            {/* Add any additional notes or comments */}
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>

                {/* 已選擇的新聞列表 */}
                <div className="border-t border-gray-200 p-4">
                    <h3 className="text-md font-medium text-gray-700 mb-2">已選擇的新聞 ({selectedNews.length}/15)</h3>
                    <div className="max-h-[80px] overflow-y-auto bg-gray-50 rounded p-2">
                        <div className="grid grid-cols-10 gap-2">
                            {Array.from({ length: 15 }).map((_, index) => {
                                const news = selectedNews[index];
                                return (
                                    <div 
                                        key={index} 
                                        className={`relative h-[40px] rounded ${
                                            news ? 'bg-white shadow-sm' : 'bg-gray-100 border border-dashed border-gray-300'
                                        }`}
                                    >
                                        {news ? (
                                            <>
                                                <div className="absolute inset-0 p-1 text-[8px] overflow-hidden">
                                                    <div className="flex flex-col justify-between h-full">
                                                        <div className="line-clamp-2 font-medium text-gray-900">
                                                            {news.title}
                                                        </div>
                                                        <div className="text-blue-600 truncate text-[6px]">
                                                            {getSourceLabel(news.link)}
                                                        </div>
                                                    </div>
                                                </div>
                                                <button
                                                    onClick={() => onRemoveNews(news.link)}
                                                    className="absolute -top-1 -right-1 bg-red-500 text-white rounded-full w-3 h-3 flex items-center justify-center text-[6px] hover:bg-red-600"
                                                >
                                                    ✕
                                                </button>
                                            </>
                                        ) : (
                                            <div className="absolute inset-0 flex items-center justify-center text-gray-400 text-[8px]">
                                                {index + 1}
                                            </div>
                                        )}
                                    </div>
                                );
                            })}
                        </div>
                    </div>
                </div>

                <div className="border-t p-4">
                    <div className="flex justify-between items-center w-full">
                        {/* 左側：生成狀態 */}
                        <div className="flex-1">
                            {isGenerating && (
                                <div className="text-center">
                                    <p className="text-gray-700">
                                        {progress.message}
                                        <br />
                                        已等待時間 {progress.elapsedTime}秒
                                    </p>
                                </div>
                            )}
                        </div>

                        {/* 中間：生成按鈕 */}
                        <div className="flex-1 flex justify-center">
                            <button 
                                className={`h-10 bg-blue-600 text-white p-1 sm:p-1 rounded w-32 sm:w-40 text-sm sm:text-base ${isGenerating ? 'opacity-50 cursor-not-allowed' : ''}`}
                                onClick={onGenerateResult}
                                disabled={isGenerating}
                            >
                                {isGenerating ? '生成中' : '生成分鏡稿'}
                            </button>
                        </div>

                        {/* 右側：返回按鈕和總字數 */}
                        <div className="flex-1 flex justify-end items-center gap-4">
                            <div className="text-sm text-gray-700">
                                總字數：{totalWordCount} / 20000
                            </div>
                            <button 
                                disabled={isGenerating}
                                onClick={onClose}
                                className={`h-10 px-4 py-1 bg-gray-100 text-gray-700 rounded hover:bg-gray-200 ${isGenerating ? 'opacity-50 cursor-not-allowed' : ''}`}
                            >
                                回上一頁
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default NewsModal; 