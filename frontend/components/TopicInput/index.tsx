import React from 'react';


interface ComponentState {
    topicKeyword: string;
    selectedSources: string[];
}

interface TopicInputProps {
    topicKeyword: string;
    selectedSources: string[];
    updateState: (key: keyof ComponentState, value: string | string[]) => void;
}

const TopicInput: React.FC<TopicInputProps> = ({ topicKeyword, updateState }) => {
    return (
        <div className="space-y-4">
            <div className="relative rounded-lg text-white">
                <input 
                    type="text" 
                    value={topicKeyword}
                    onChange={(e) => updateState('topicKeyword', e.target.value)}
                    placeholder="輸入想要生成新聞主題的關鍵字" 
                    className="w-full p-2 pl-10 sm:pl-12 h-10 sm:h-14 bg-bgPrimaryLight rounded-lg text-textLight text-sm sm:text-base border-2 border-gray-100 focus:outline-none focus:ring-0 focus:ring-gray-100 transition duration-150 ease-in-out"
                />
                <div className="absolute left-3 sm:left-4 top-1/2 transform -translate-y-1/2 text-gray-400 pointer-events-none">
                    🔍
                </div>
            </div>
        </div>
    );
};

export default TopicInput;