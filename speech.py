import os
from pydub import AudioSegment
import speech_recognition as sr

def split_audio(audio_file_path, segment_length_ms=10000):  # 10 secondes segments
    audio = AudioSegment.from_file(audio_file_path)
    segments = []
    for i in range(0, len(audio), segment_length_ms):
        segments.append(audio[i:i+segment_length_ms])
    return segments

def transcribe_audio(audio_file_path, language_code="en-US"):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file_path) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio, language=language_code)
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError as e:
        return f"Could not request results; {e}"

def main():
    audio_path = input("Enter the path to your audio file (e.g., path_to_your_audio_file.m4a): ")
    language_code = input("Enter the language code (e.g., en-US for English, he-IL for Hebrew): ")

    if not os.path.exists(audio_path):
        print("Audio file does not exist.")
        return

    segments = split_audio(audio_path)
    transcriptions = []

    for idx, segment in enumerate(segments):
        segment_path = f"segment_{idx}.wav"
        segment.export(segment_path, format="wav")
        transcription = transcribe_audio(segment_path, language_code)
        transcriptions.append(transcription)
        os.remove(segment_path)  # Clean up the segment file after transcription

    with open("transcriptions.txt", "w") as f:
        for idx, transcription in enumerate(transcriptions):
            f.write(f"Segment {idx}:\n{transcription}\n\n")

    print("Transcriptions saved to transcriptions.txt")

if __name__ == "__main__":
    main()
