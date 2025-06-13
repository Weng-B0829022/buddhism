import React from 'react';

interface SimpleModalProps {
    isOpen: boolean;
    onClose: () => void;
    title: string;
    children: React.ReactNode;
    width?: number;
}

export const SimpleModal: React.FC<SimpleModalProps> = ({ 
    isOpen, 
    onClose, 
    title, 
    children, 
    width = 600 
}) => {
    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 bg-transparent flex items-center justify-center z-50">
            <div 
                className="bg-white rounded-lg shadow-lg max-h-90vh overflow-y-auto"
                style={{ width: `${width}px`, maxWidth: '90vw' }}
            >
                <div className="flex justify-between items-center p-4 border-b">
                    <h2 className="text-xl font-semibold">{title}</h2>
                    <button 
                        onClick={onClose}
                        className="text-gray-500 hover:text-gray-700 text-2xl"
                    >
                        ×
                    </button>
                </div>
                <div className="p-4">
                    {children}
                </div>
            </div>
        </div>
    );
}; 