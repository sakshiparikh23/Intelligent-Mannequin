import speech_recognition as sr


def run_stt(name):
    mic_name = name
    sample_rate = 48000                                                                     # Sample rate is how often values are recorded
    chunk_size = 2048                                                                       # Chunk is like a buffer. It stores 2048 samples (bytes of data) here.
                                                                                            # it is advisable to use powers of 2 such as 1024 or 2048
    r = sr.Recognizer()                                                                     # Initialize the recognizer

    # generate a list of all audio cards/microphones
    mic_list = sr.Microphone.list_microphone_names()

    # the following loop aims to set the device ID of the mic that
    # we specifically want to use to avoid ambiguity.
    for i, microphone_name in enumerate(mic_list):
        if microphone_name == mic_name:
            device_id = i

            # use the microphone as source for input. Here, we also specify
            # which device ID to specifically look for incase the microphone
            # is not working, an error will pop up saying "device_id undefined"
            with sr.Microphone(device_index=device_id, sample_rate=sample_rate,
                               chunk_size=chunk_size) as source:
                # wait for a second to let the recognizer adjust the
                # energy threshold based on the surrounding noise level
                r.adjust_for_ambient_noise(source)
                print("Say Something")
                # listens for the user's input
                audio = r.listen(source)

                try:
                    text = r.recognize_google(audio)
                    #print("you said: " + text)

                # error occurs when google could not understand what was said

                except sr.UnknownValueError:
                    #print("Google Speech Recognition could not understand audio")
                    text = 'Google Speech Recognition could not understand audio'

                except sr.RequestError as e:
                    #print("Could not request results from Google Speech Recognition service;{0}".format(e))
                    text = 'Could not request results from Google Speech Recognition service;{0}'.format(e)

    return text