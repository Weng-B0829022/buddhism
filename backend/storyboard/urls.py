from django.urls import path
from .views import (
    NewsGenVideoView,
    GetGeneratedVideoView,
)
from . import views

urlpatterns = [
    path('storyboard/gen-video', NewsGenVideoView.as_view(), name='execute_news_gen_video'),
    path('storyboard/get-generated-video', GetGeneratedVideoView.as_view(), name='get_generated_videos'),  # Add this line
]