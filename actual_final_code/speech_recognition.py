import speech_recognition as sr

def get_audio_input():
	# obtain audio from the microphone
	r = sr.Recognizer()
	with sr.Microphone() as source:
	    print("Say something!")
	    audio = r.listen(source,timeout=1,phrase_time_limit=5)

	# recognize speech using Google Speech Recognition
	try:
	    # for testing purposes, we're just using the default API key
	    # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
	    # instead of `r.recognize_google(audio)`
	    recognized_input = r.recognize_google(audio)
	    print("Google Speech Recognition thinks you said " + recognized_input)
	    return recognized_input
	except sr.UnknownValueError:
	    print("Google Speech Recognition could not understand audio")
	    return False
	except sr.RequestError as e:
	    print("Could not request results from Google Speech Recognition service; {0}".format(e))
	    return False