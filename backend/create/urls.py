from django.urls import path
from .views import (
    NewsScrapeView,
    WordCountView,
)

urlpatterns = [
    path('create/news-scrape/', NewsScrapeView.as_view(), name='news_scrape'),
    path('create/word-count/', WordCountView.as_view(), name='word_count'),
    path('create/execute-generate-storyboard/', NewsScrapeView.as_view(), name='execute_generate_storyboard'),
]