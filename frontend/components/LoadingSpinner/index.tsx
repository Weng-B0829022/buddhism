import React from 'react';

interface LoadingSpinnerProps {
    size?: number;
    className?: string;
}

export const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({ size = 40, className = "" }) => {
    return (
        <div className={`flex items-center justify-center ${className}`}>
            <div 
                className="animate-spin rounded-full border-4 border-blue-200 border-t-blue-600"
                style={{ width: `${size}px`, height: `${size}px` }}
            ></div>
        </div>
    );
};

interface FullScreenLoadingProps {
    message?: string;
}

export const FullScreenLoading: React.FC<FullScreenLoadingProps> = ({ message = "載入中..." }) => {
    return (
        <div className="fixed inset-0 bg-white bg-opacity-90 flex items-center justify-center z-50">
            <div className="text-center">
                <LoadingSpinner size={60} className="mb-4" />
                <p className="text-lg text-gray-600 font-medium">{message}</p>
            </div>
        </div>
    );
};

interface ContentLoadingProps {
    message?: string;
}

export const ContentLoading: React.FC<ContentLoadingProps> = ({ message = "處理數據中..." }) => {
    return (
        <div className="flex flex-col items-center justify-center py-12">
            <LoadingSpinner size={50} className="mb-4" />
            <p className="text-gray-600 font-medium">{message}</p>
        </div>
    );
}; 