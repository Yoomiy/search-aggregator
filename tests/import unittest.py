import unittest
from unittest.mock import patch, mock_open, MagicMock
from speech import convert_and_transcribe, split_audio

# FILE: test_speech.py


class TestSpeech(unittest.TestCase):

    @patch("speech.AudioSegment.from_file")
    @patch("speech.sr.Recognizer")
    def test_convert_and_transcribe(self, mock_recognizer, mock_audio_segment):
        # Mock the audio segment and recognizer
        mock_audio = MagicMock()
        mock_audio.export = MagicMock()
        mock_audio_segment.return_value = mock_audio

        mock_recognizer_instance = MagicMock()
        mock_recognizer.return_value = mock_recognizer_instance
        mock_recognizer_instance.record = MagicMock()
        mock_recognizer_instance.recognize_google = MagicMock(return_value="test transcription")

        result = convert_and_transcribe("test_audio.m4a", language="en-US")
        self.assertEqual(result, "test transcription")

    @patch("speech.AudioSegment.from_file")
    def test_split_audio(self, mock_audio_segment):
        # Mock the audio segment
        mock_audio = MagicMock()
        mock_audio.__len__.return_value = 120000  # 2 minutes
        mock_audio_segment.return_value = mock_audio

        segments = split_audio("test_audio.m4a", segment_length_ms=60000)
        self.assertEqual(len(segments), 2)

if __name__ == "__main__":
    unittest.main()