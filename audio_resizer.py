from pydub import AudioSegment

def resize_audio(input_path, output_path, frame_rate):
    try:
        audio = AudioSegment.from_file(input_path)
        audio = audio.set_frame_rate(frame_rate)
        audio.export(output_path, format="mp3")
        return output_path
    except Exception as e:
        print(f"Error resizing audio: {e}")
        return None
