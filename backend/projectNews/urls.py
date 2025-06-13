from django.urls import path, include

urlpatterns = [
    path('', include('create.urls')),  # 這會包含 create 應用的所有 URL
    path('', include('storyboard.urls')),  # 這會包含 storyboard 應用的所有 URL
]