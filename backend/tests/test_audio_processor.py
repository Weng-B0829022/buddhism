import os
import pytest
from storyboard.services_new.processors.audio_processor import AudioProcessor

@pytest.mark.django_db
def test_audio_processor_generate_single_audio(tmp_path):
    # 準備測試資料
    audio_description = ["這是一段測試語音。", "這是另一段測試語音。"]
    output_path = tmp_path
    title = "test_title"
    processor = AudioProcessor(audio_description, str(output_path), title)
    # 執行 process
    audio_files = processor.process()
    # 驗證結果
    assert len(audio_files) == 1
    assert os.path.exists(audio_files[0])
    assert audio_files[0].endswith(".mp3") 