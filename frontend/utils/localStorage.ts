/**
 * 從 localStorage 讀取分鏡稿場景數據
 */
export const loadScenesFromLocalStorage = () => {
  try {
    console.log('🔍 正在從 localStorage 讀取數據...');
    const savedData = localStorage.getItem('createdContent');
    console.log('📦 localStorage 原始數據:', savedData);
    
    if (savedData) {
      const parsedData = JSON.parse(savedData);
      console.log('✅ 成功解析 localStorage 數據:', parsedData);
      console.log('📊 Storyboard 數量:', parsedData.storyboard?.length || 0);
      return parsedData;
    } else {
      console.log('⚠️ localStorage 中沒有找到 currentStoryboard 數據');
    }
  } catch (error) {
    console.error('❌ 讀取 localStorage 時發生錯誤:', error);
  }
  
  // 如果沒有保存的數據，返回預設數據
  console.log('🔄 返回預設數據');
  return {
    "title": "尚未生成分鏡稿",
    "avatar": "man1",
    "avatarType": "half",
    "background": "background1",
    "storyboard": [],
    "random_id": "default"
  };
}; 