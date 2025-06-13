HALF_CONFIG = {
    "scene_place_coordinates": {
        "top_left": [771, 73],  # 圖片左上角的坐標
        "top_right": [1841, 73],  # 圖片右上角的坐標
        "bottom_right": [1841, 869],  # 圖片右下角的坐標
        "bottom_left": [771, 869],  # 圖片左下角的坐標
    },
    "extend_scene_place_coordinates": {
        "top_left": [147, 71],  # 圖片左上角的坐標
        "top_right": [1772, 71],  # 圖片右上角的坐標
        "bottom_right": [1772, 869],  # 圖片右下角的坐標
        "bottom_left": [147, 869],  # 圖片左下角的坐標
    },
    "canvas_size": (1920, 1080),
    "crop_coords": (760, 110, 450, 485),# x, y, w, h
    "avatar_place_coordinates": {
        "top_left": [73, 73],  # avatar 左上角的坐標
        "top_right": [737, 73],  # avatar 右上角的坐標
        "bottom_right": [737, 869],  # avatar 右下角的坐標
        "bottom_left": [73, 869],  # avatar 左下角的坐標
    },
    "background": {
        "img_path": "background_half.jpg",
        "top_left": [0, 0],
        "top_right": [1920, 0],
        "bottom_right": [1920, 1080],
        "bottom_left": [0, 1080],
        "z_index": -1,
    },
    "extend_background": {
        "img_path": "background_half_extend.jpg",  # 背景圖片文件名
        "top_left": [0, 0],  # 背景圖片的左上角坐標
        "top_right": [1920, 0],  # 背景圖片的右上角坐標
        "bottom_right": [1920, 1080],  # 背景圖片的右下角坐標
        "bottom_left": [0, 1080],  # 背景圖片的左下角坐標
        "z_index": -1,  # 背景圖片的 z_index，控制層次順序
    },
    "title": {
        "top_left": [146, 890],
        "top_right": [1049, 890],
        "bottom_right": [1049, 1002],
        "bottom_left": [146, 1002],
        "z_index": 100,
    },
    "international": {
        "top_left": [1400, 885],
        "top_right": [1572, 885],
        "bottom_right": [1572, 931],
        "bottom_left": [1400, 931],
        "z_index": 100,
    },
}
FULL_CONFIG = {
    # 定義 full 配置
    # 這裡可以根據需要定義 FULL_CONFIG 的具體內容
    # 例如：
    "scene_place_coordinates": {
        "top_left": [111, 97],  # 圖片左上角的坐標
        "top_right": [1324, 183],  # 圖片右上角的坐標
        "bottom_right": [1324, 818],  # 圖片右下角的坐標
        "bottom_left": [111, 904],  # 圖片左下角的坐標
    },
    "extend_scene_place_coordinates": {
        "top_left": [165, 117],  # 圖片左上角的坐標
        "top_right": [1756, 117],  # 圖片右上角的坐標
        "bottom_right": [1756, 945],  # 圖片右下角的坐標
        "bottom_left": [165, 945],  # 圖片左下角的坐標
    },
    "canvas_size": (1920, 1080),  # 影片的寬度和高度
    "crop_coords": (790, 110, 390, 970),  # 定義裁減 avatar 圖片的區域 x, y, w, h
    "avatar_place_coordinates": {
        "top_left": [1420, 200],  # avatar 左上角的坐標
        "top_right": [1770, 200],  # avatar 右上角的坐標
        "bottom_right": [1770, 980],  # avatar 右下角的坐標
        "bottom_left": [1420, 980],  # avatar 左下角的坐標
    },
    "background": {
        "img_path": "background_full.jpg",  # 背景圖片文件名
        "top_left": [0, 0],  # 背景圖片的左上角坐標
        "top_right": [1920, 0],  # 背景圖片的右上角坐標
        "bottom_right": [1920, 1080],  # 背景圖片的右下角坐標
        "bottom_left": [0, 1080],  # 背景圖片的左下角坐標
        "z_index": -1,  # 背景圖片的 z_index，控制層次順序
    },
    "extend_background": {
        "img_path": "background_full_extend.jpg",  # 背景圖片文件名
        "top_left": [0, 0],  # 背景圖片的左上角坐標
        "top_right": [1920, 0],  # 背景圖片的右上角坐標
        "bottom_right": [1920, 1080],  # 背景圖片的右下角坐標
        "bottom_left": [0, 1080],  # 背景圖片的左下角坐標
        "z_index": -1,  # 背景圖片的 z_index，控制層次順序
    },
    "title": {
        "top_left": [230, 1000],  # 標題圖片的左上角坐標
        "top_right": [1240, 1000],  # 標題圖片的右上角坐標
        "bottom_right": [1240, 1080],  # 標題圖片的右下角坐標
        "bottom_left": [230, 1080],  # 標題圖片的左下角坐標
        "z_index": 100,  # 標題圖片的 z_index，控制層次順序
    },
    "international": {
        "top_left": [1604, 60],  # 標題圖片的左上角坐標
        "top_right": [1784, 60],  # 標題圖片的右上角坐標
        "bottom_right": [1784, 113],  # 標題圖片的右下角坐標
        "bottom_left": [1604, 113],  # 標題圖片的左下角坐標
        "z_index": 100,  # 標題圖片的 z_index，控制層次順序
    },
}
HALF_CONFIG2 = {
    # 定義 full 配置
    # 這裡可以根據需要定義 FULL_CONFIG 的具體內容
    # 例如：
    "scene_place_coordinates": {
        "top_left": [661, 195],  # 圖片左上角的坐標
        "top_right": [1808, 195],  # 圖片右上角的坐標
        "bottom_right": [1808, 801],  # 圖片右下角的坐標
        "bottom_left": [661, 801],  # 圖片左下角的坐標
    },
    "extend_scene_place_coordinates": {
        "top_left": [258, 120],  # 圖片左上角的坐標
        "top_right": [1655, 120],  # 圖片右上角的坐標
        "bottom_right": [1655, 844],  # 圖片右下角的坐標
        "bottom_left": [258, 844],  # 圖片左下角的坐標
    },
    "canvas_size": (1920, 1080),  # 影片的寬度和高度
    "crop_coords": (760, 110, 450, 485),# x, y, w, h
    "avatar_place_coordinates": {
        "top_left": [44, 175],  # avatar 左上角的坐標
        "top_right": [748, 175],  # avatar 右上角的坐標
        "bottom_right": [748, 898],  # avatar 右下角的坐標
        "bottom_left": [44, 898],  # avatar 左下角的坐標
    },
    "background": {
        "img_path": "background_half2.jpg",  # 背景圖片文件名
        "top_left": [0, 0],  # 背景圖片的左上角坐標
        "top_right": [1920, 0],  # 背景圖片的右上角坐標
        "bottom_right": [1920, 1080],  # 背景圖片的右下角坐標
        "bottom_left": [0, 1080],  # 背景圖片的左下角坐標
        "z_index": -1,  # 背景圖片的 z_index，控制層次順序
    },
    "extend_background": {
        "img_path": "background_half2_extend.jpg",  # 背景圖片文件名
        "top_left": [0, 0],  # 背景圖片的左上角坐標
        "top_right": [1920, 0],  # 背景圖片的右上角坐標
        "bottom_right": [1920, 1080],  # 背景圖片的右下角坐標
        "bottom_left": [0, 1080],  # 背景圖片的左下角坐標
        "z_index": -1,  # 背景圖片的 z_index，控制層次順序
    },
    "title": {
        "top_left": [217, 917],  # 標題圖片的左上角坐標
        "top_right": [1157, 917],  # 標題圖片的右上角坐標
        "bottom_right": [1157, 1000],  # 標題圖片的右下角坐標
        "bottom_left": [217, 1000],  # 標題圖片的左下角坐標
        "z_index": 100,  # 標題圖片的 z_index，控制層次順序
    },
    "international": {
        "top_left": [1604, 60],  # 標題圖片的左上角坐標
        "top_right": [1784, 60],  # 標題圖片的右上角坐標
        "bottom_right": [1784, 113],  # 標題圖片的右下角坐標
        "bottom_left": [1604, 113],  # 標題圖片的左下角坐標
        "z_index": 100,  # 標題圖片的 z_index，控制層次順序
    },
}
