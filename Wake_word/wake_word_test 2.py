import snowboydecoder
import signal
import speech_recognition as sr

interrupted = False

def audioRecorderCallback():
    
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration = 1)
        audio = r.listen(source, phrase_time_limit = 5)  # read the entire audio file
    # recognize speech using Google Speech Recognition
    try: 
        print(r.recognize_google(audio))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

    
    
def detectedCallback():
  print('recording audio...', end='', flush=True)

def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted

model = '/Users/baileyvu/desktop/wake_word_test/Hey_Ivy.pmdl'

# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

detector = snowboydecoder.HotwordDetector(model, sensitivity=0.38)
print('Listening... Press Ctrl+C to exit')

# main loop
detector.start(detected_callback=detectedCallback,
               audio_recorder_callback=audioRecorderCallback,
               interrupt_check=interrupt_callback,
               sleep_time=0.01)

detector.terminate()



audioRecorderCallback('I just want to say Hey Ivy if it is possible')