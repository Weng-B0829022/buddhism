export interface VisualElement {
    type: string;
    content: string;
}

export interface StoryboardScene {
    sceneNumber: number;
    timeCode: string;
    visualElements: VisualElement[];
    voiceoverText: string;
}

export interface StoryboardData {
    段落: string;
    秒數: string;
    畫面?: string;
    畫面描述: string;
    旁白: string;
    字數: string;
    imageFile?: File | null;
}

export interface Article {
    title: string;
    content: string;
    storyboard: string[];
    category?: string;
}

export interface GeneratedContent {
    main_article?: {
        title: string;
        content: string;
        category: string;
    };
    articles: Article[];
}

export interface CreatedContent {
    status: string;
    generated_content: GeneratedContent;
    stats: {
        total: number;
        success: number;
        failed: number;
    };
}

export interface GenerationResult {
    message?: string;
    error?: string;
    random_id?: string;
    video_paths?: string[];
}

export interface UploadInfo {
    uploadId: string;
    uploadTitle: string;
    public_url: string;
}

export interface ProcessedStoryboard {
    title: string;
    content: string;
    storyboard: StoryboardScene[];
}

export interface StoryboardDataResult {
    title: string;
    content: string;
    storyboard: StoryboardData[];
}

export interface StoryboardProps {
    storyboardData: StoryboardData[];
    storyboardTitle: string;
    selectedIndex: number;
    isEditMode: boolean;
    onStoryboardDataChange?: (data: StoryboardData[]) => void;
} 