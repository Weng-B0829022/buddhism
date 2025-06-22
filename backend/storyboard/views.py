from django.shortcuts import render
from datetime import datetime
import logging
from rest_framework.views import APIView
from django.views import View
from django.http import FileResponse, HttpResponseNotFound, HttpResponseBadRequest, JsonResponse
from django.conf import settings
import traceback
import os
import logging
from storyboard.services_new.main_pipeline import MainPipeline

logger = logging.getLogger(__name__)

# Create your views here.

class NewsGenVideoView(APIView):
    def post(self, request):
        
        storyboard = request.data

        if not storyboard:
            return JsonResponse({'error': 'Missing storyboard parameter'}, status=400)
        try:
            
            pipeline = MainPipeline()  # 不傳參數到 __init__
            if not pipeline.initialize(storyboard):  # 檢查初始化是否成功
                return JsonResponse({'error': '初始化失敗'}, status=500)
            result = pipeline.execute()
            random_id = pipeline.random_id
            
        except Exception as e:
            print(f"Error in combine_media: {str(e)}")
            print(traceback.format_exc())
            return JsonResponse({'message': 'error'}, status=500)
        return JsonResponse({'message': 'success', 'image_urls': random_id}, status=200)

class GetGeneratedVideoView(View):
    def get(self, request):
        id = request.GET.get('id')
        
        if not id:
            logger.warning("Missing id parameter in request")
            return HttpResponseBadRequest("Missing id parameter")

        video_dir = os.path.join(settings.MEDIA_ROOT, 'generated', id)

        # 確保目錄存在
        if not os.path.exists(video_dir):
            logger.warning(f"Directory not found: {video_dir}")
            return HttpResponseNotFound("Video directory not found")

        # 搜尋包含 'final_video' 的檔案
        final_video_file = None
        for filename in os.listdir(video_dir):
            if 'final_video' in filename:
                final_video_file = filename
                break

        if final_video_file:
            video_path = os.path.join(video_dir, final_video_file)
            logger.info(f"Serving video file: {video_path}")
            return FileResponse(open(video_path, 'rb'), content_type='video/mp4')
        else:
            logger.warning(f"Final video file not found in directory: {video_dir}")
            return HttpResponseNotFound("Final video not found")
        
