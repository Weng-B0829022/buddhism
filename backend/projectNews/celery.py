from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

# 設置默認的 Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projectNews.settings')

app = Celery('projectNews')

# 使用 Django 的配置文件來配置 Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# 自動發現任務
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# 配置定期任務
app.conf.beat_schedule = {
    'process-video-requests': {
        'task': 'storyboard.tasks.process_video_requests',
        'schedule': crontab(minute='*/15'),  # 每15分鐘執行一次
    },
    'cleanup-old-files': {
        'task': 'storyboard.tasks.cleanup_old_files',
        'schedule': crontab(hour=0, minute=0),  # 每天午夜執行
    },
} 