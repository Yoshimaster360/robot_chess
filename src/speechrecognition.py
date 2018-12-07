import speech_recognition as sr

def get_audio_input():
	# obtain audio from the microphone
	# recognize speech using Google Speech Recognition
	try:
		r = sr.Recognizer()
		with sr.Microphone() as source:
			print("Say something!")
			audio = r.listen(source,timeout=1,phrase_time_limit=10)
			recognized_input = r.recognize_google(audio)
			print("Google Speech Recognition thinks you said " + recognized_input)
			return recognized_input
	except sr.UnknownValueError:
		print("Google Speech Recognition could not understand audio")
		return False
	except sr.RequestError as e:
		print("Could not request results from Google Speech Recognition service; {0}".format(e))
		return False
	except LookupError:
		print("Could not understand you")
		return False
	except sr.WaitTimeoutError as e:
		print("didn't get anything")
		return False