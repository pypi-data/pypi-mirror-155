import os
import pickle
from functools import partial
import wave
import pyaudio
import time
import tempfile

from appPublic.app_logger import AppLogger, create_logger

class Audio(AppLogger, pyaudio.PyAudio):
	def __init__(self, save_file=None):
		AppLogger.__init__(self)
		pyaudio.PyAudio.__init__(self)
		self.temp_filename = None
		self.chunk = 1024
		self.devices = [ self.get_device_info_by_index(i) \
								for i in range(self.get_device_count()) ]

	def get_input_device(self):
		return [ d for d in self.devices if d.maxInputChannels > 0 ]

	def get_output_device(self):
		return [ d for d in self.devices if d.maxOutputChannels > 0 ]

	def tmpfile(self):
		x = tempfile.mkstemp(suffix='.wav')
		os.close(x[0])
		self.temp_filename = x[1]

	def record_cb(self, in_data, frame_count, time_info, status):
		bdata = pickle.dumps(in_data)
		self.info('frame_count=%s, time_info=%s, status=%s, bytes count=%s', \
						frame_count, time_info, status, len(bdata))
		self.rec_frames += frame_count
		self.current_ts = time.time()
		self.wavfile.writeframesraw(in_data)
		if self.running:
			return (None, pyaudio.paContinue)

		return (None, pyaudio.paComplete)

	def replay_cb(self, in_data, frame_count, time_info, status):
		data = self.wavfile.readframes(frame_count)
		bdata = pickle.dumps(data)
		self.info('frame_count=%s, data length in bytes=%s', \
						frame_count, len(bdata))
		if not data:
			return (None, pyaudio.paComplete)

		return (data, pyaudio.paContinue)

	def get_output_index(self):
		dev_cnt = self.get_device_count()
		for i in range(dev_cnt):
			x = self.get_device_info_by_index(i)
			print(x)
		return dev_cnt - 1

	def record(self, save_file=None, stop_cond_func=None):
		filename = save_file
		if filename is None:
			self.tmpfile()
			filename = self.temp_filename

		self.wavfile = wave.open(filename, 'wb')
		self.wavfile.setnchannels(2)
		self.wavfile.setsampwidth(2)
		self.wavfile.setframerate(44100.00)
		self.stream = self.open(format=pyaudio.paInt16,
						channels=2,
						rate=44100,
						input=True,
						frames_per_buffer=self.chunk,
						stream_callback=self.record_cb)
		self.stream.start_stream()
		self.running = True
		self.rec_frames = 0
		self.start_ts = self.current_ts = time.time()
		while self.stream.is_active():
			if stop_cond_func and stop_cond_func():
				self.running = False
			time.sleep(0.05)
		self.stream.stop_stream()
		self.stream.close()
		self.wavfile.close()
		if save_file is None:
			self.replay()

	def replay(self, play_file=None):
		idx = self.get_output_index()
		x = self.get_device_info_by_index(idx)
		y = self.get_default_input_device_info()
		self.info('default_input=%s, default_output=%s', y, x)
		if play_file is None:
			play_file = self.temp_filename
		self.wavfile = wave.open(play_file, 'rb')
		format = self.get_format_from_width(self.wavfile.getsampwidth())
		framerate=self.wavfile.getframerate()
		self.info('format=%s, framerate=%s', format, framerate)
		self.stream = self.open(format=format,
						channels=self.wavfile.getnchannels(),
						rate=framerate,
						output=True,
						output_device_index=idx,
						frames_per_buffer=self.chunk,
						stream_callback=self.replay_cb)
		self.stream.start_stream()
		while self.stream.is_active():
			time.sleep(0.05)
		self.stream.stop_stream()
		self.stream.close()
		self.wavfile.close()

	def __del__(self):
		if self.temp_filename:
			os.remove(self.temp_filename)

if __name__ == '__main__':
	import sys
	def stop_func(audio):
		if audio.current_ts - audio.start_ts >= 10:
			audio.running = False

	create_logger('audio', levelname='debug')
	a = Audio()
	
	if 'replay' in sys.argv[0]:
		if len(sys.argv) < 2:
			print(f'usage:\n{sys.argv[0]} WAVFILE')
			sys.exit(1)
		a.replay(sys.argv[1])
	elif 'record' in sys.argv[0]:
		sf = None
		if len(sys.argv) >= 2:
			sf = sys.argv[1]
		f = partial(stop_func, a)
		a.record(sf, stop_cond_func=f)
