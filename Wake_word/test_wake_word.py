import snowboydecoder

print('Speak please...')

interrupted = False

def detected_callback():
    print("hotword detected")
def interrupt_callback():
    global interrupted
    return interrupted
model = 'Users/baileyvu/desktop/wake_word_test/Hey_Ivy.pmdl'
detector = snowboydecoder.HotwordDetector(model, sensitivity=0.5, audio_gain=1)
print('Listening... Press Ctrl+C to exit')

# main loop
detector.start(detected_callback=snowboydecoder.play_audio_file,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)

detector.terminate()