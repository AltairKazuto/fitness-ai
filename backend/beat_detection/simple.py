import librosa
import io
import beat_detection.lib.beat as beat
import os

"""
Detect the beats in a desired song (using the sub and low frequency bands).
"""

# Load the song from a mp3 file
def get_beats(path):
	# temp_path = os.path.join('/tmp', path.filename) # Use a temporary directory
	audio_buffer = io.BytesIO(path)
	# print(path.filename)
	# audio_file.save(temp_path)
	y, sr = librosa.load(audio_buffer)

	# Detect the beats
	beats = beat.detect_combi_beats(y, sr)
	return beats

