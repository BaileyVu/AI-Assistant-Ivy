import speech_recognition as sr
import re
import wolframalpha
import webbrowser
import yagmail
import json
import random
import requests
from time import strftime
import datetime
import subprocess
from pyowm import OWM
from weatherbit.api import Api
import wikipedia
#libraries for IvyResponse
from urllib.parse import quote
from urllib.request import urlopen
import wave
from contextlib import closing
import pyaudio

#Ivy's logic cube
player = None
def playwav(path_or_file):
    global player
    if player is None:
        player = pyaudio.PyAudio()
    with closing(wave.open(path_or_file, 'rb')) as wavfile, \
         closing(player.open(
             format=player.get_format_from_width(wavfile.getsampwidth()),
             channels=wavfile.getnchannels(),
             rate=wavfile.getframerate(),
             output=True)) as stream:
        while True:
            data = wavfile.readframes(1024) # read 1024 frames at once
            if not data: # EOF
                break
            stream.write(data)
            
def IvyResponse(output):
    print("Ivy: ", output)
    language = 'en_us'
    text = quote(output)
    playwav(urlopen('https://tts.readspeaker.com/a/speak'
                '?key=b701aadfff8ed0d8be35ec601ba86c31&audioformat=pcm&streaming=0&lang={language}&voice=Julie&text={text}'.format(**vars())))
    
def myCommand():
    "listen for commands"
    r = sr.Recognizer()
    
    with sr.Microphone() as source:
        print('Speak please...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration = 1)
        audio = r.listen(source, phrase_time_limit = 8)
    try:
        command = r.recognize_google(audio, language = 'en-US').lower()
        print("You: ", command)
        return command
    except sr.UnknownValueError:
        first_response = "I am sorry, I couldn\'t understand your command. Maybe it is a little noisy with the environment. Please try again!"
        second_response = 'Sorry, I could\'t get that. Can you try again, please!'
        third_response = ' I can\'t recognize the command. Please repeat it. Thank you!'
        fourth_response = 'Sorry? What did you say?'
        fifth_response = 'The command is a little bit unclear for me. Please try again!'
        response = random.choice([first_response, second_response, third_response, fourth_response, fifth_response])
        IvyResponse(response)
        command = myCommand()
    return command

#Ivy's Ability

def IvyAbility(command):
    
    #open website function/ability
    if "open reddit" in command:
        reg_ex = re.search('open reddit (.*)', command)
        url = 'https://www.reddit.com/'
        if reg_ex:
            subreddit = reg_ex.group(1)
            url = url + 'r/' + subreddit
        webbrowser.open(url)
        IvyResponse("Your cool shit reddit site has openned for you")
    elif 'open google' in command:
        reg_ex = re.search('open google(.*)', command)
        url = 'https://www.google.co.uk/'
        webbrowser.open(url)
        IvyResponse("Your requested website has opened for you")
    elif 'open' in command:
        reg_ex = re.search('open(.*)', command)
        if reg_ex:
            domain = reg_ex.group(1)
            url = 'https://www.' + domain
            webbrowser.open(url)
            IvyResponse('Opened')
    elif 'google' in command:
        reg_ex = re.search('google(.*)', command)
        if reg_ex:
            domain = reg_ex.group(1)
            url = 'https://www.google.com/search?q=' + domain
            webbrowser.open(url)
            IvyResponse("I has searched your requested on website. Take a look at what I found")
        else:
            pass
        
    #find weather and weather forecast function/ability
    elif 'current weather in' in command:
        reg_ex = re.search('current weather in (.*)', command)
        if reg_ex:
            city = reg_ex.group(1)
            owm = OWM(API_key='37a0944f43b76456cbc580615fe4c676')
            obs = owm.weather_at_place(city)
            w = obs.get_weather()
            k = w.get_status()
            x = w.get_temperature(unit='celsius')
            IvyResponse('Current weather in %s is %s. The maximum temperature is %0.2f and the minimum temperature is %0.2f degree celcius' % (city, k, x['temp_max'], x['temp_min']))
    elif 'weather forecast in' in command:
        reg_ex = re.search('weather forecast in (.*)', command)
        if reg_ex:
            api_key = 'fb14f083b77e4c99baf4f4b6e1d8c50d'
            api = Api(api_key)
            location = reg_ex.group(1)
            IvyResponse('How many days you want to forecast?')
            day_of_forecast = myCommand()
            forecast = api.get_forecast(days = day_of_forecast, city = location)
            forecast_list = forecast.get_series(['temp','max_temp','min_temp','weather'])
            IvyResponse("The weather forecast for " + str(location))
            weather_data = []
            for forecast in forecast_list:
                weather_data.append(f''' On {forecast['datetime'] : %d %B %Y},
                         the weather is {forecast['weather']['description']}. The temperature will be {forecast['temp']} celsius degree
                         with maximum temperature will be {forecast['max_temp']} and minimum temperature will be {forecast['min_temp']}.
                         '''
                         )
            b = ''.join(weather_data)
            IvyResponse(b)
        
    #send email/mail funcion
    elif 'email' in command or 'mail' in command:
        IvyResponse("Who is the recipient?")
        recipient = myCommand()
        if "john" in recipient or "david" in recipient:
            recipient_mail_add = 'bailey121294@gmail.com'
        elif "mine" in recipient or "my" in recipient:
            IvyResponse("You meant Mai, isn't it?")
            y_n = myCommand()
            if 'yes' in y_n or 'yeah' in y_n:
                recipient_mail_add = 'dangmai276@gmail.com'
            else:
                pass
        else:
            IvyResponse("What is his or her mail address please?")
            recipient_mail_add = myCommand()
        IvyResponse('What is the subject of this email please?')
        subject_mail = myCommand()
        IvyResponse('What do you want to say in the email?')
        body = myCommand()
        IvyResponse('Do you want to attach anything to the mail?')
        att_ans = myCommand()
        if 'yes' in att_ans or 'yea' in att_ans:
            IvyResponse('What do you want to send sir?')
            file = myCommand()
            if 'song' in file:
                path = '/Users/baileyvu/Desktop/Bad Guy - Billie Eilish_Justin Bieber.m4a'
                file_name = path
                IvyResponse('Sending email through Gmail')
            elif 'ivy' in file:
                path = '/Users/baileyvu/Desktop/test_7.py'
                file_name = path
                IvyResponse('Sending email though gmail')
                try:
                    yag = yagmail.SMTP('vuquoccuong121994@gmail.com')
                    yag.send(
                            to=recipient_mail_add,
                            subject=subject_mail,
                            contents=body,
                            attachments=file_name)
                    IvyResponse('Mail sent')
                except sr.UnknownValueError:
                    IvyResponse('I can\'t understand what you mean!')
            
        else:
            IvyResponse('Sending your requested Mail')
            try:
                yag = yagmail.SMTP('vuquoccuong121994@gmail.com')
                yag.send(
                        to=recipient_mail_add,
                        subject=subject_mail,
                        contents=body
                        )
                IvyResponse('Mail sent')
            except sr.UnknownValueError:
                IvyResponse('I can\'t understand what you mean!')
    
    #'tell me about' function
    elif 'tell me about' in command:
        reg_ex = re.search('tell me about (.*)', command)
        try:
            if reg_ex:
                topic = reg_ex.group(1)
                ny = wikipedia.page(topic)
                detail = ny.content[:1000].encode('utf-8')
                IvyResponse(str(detail))
        except Exception as e:
            IvyResponse(e)
            
    #telling time function
    elif 'time' in command:
        now = datetime.datetime.now()
        format_time = '%I:%M %p'
        ans1 = 'It is ' + now.strftime(format_time) + ' at the moment.'
        ans2 = 'Current time is ' + now.strftime(format_time)
        IvyResponse(random.choice([ans1, ans2]))
    elif 'what day is' in command:
        reg_ex = re.search('what day is (.*)', command)
        try:
            if reg_ex:
                dt = reg_ex.group(1)
                time_format = datetime.datetime.strptime(dt, '%d %B %Y')
                tf = datetime.datetime.strftime(time_format, '%d/%-m/%Y')
                day, month, year = (int(x) for x in tf.split('/'))    
                ans = datetime.date(year, month, day)
                IvyResponse(' It is ' + ans.strftime("%A") + ' on ' + dt)
        except Exception as e:
                now = datetime.datetime.now()
                format_day = '%A %d %B, %Y'
                IvyResponse('Today is ' + now.strftime(format_day))
    
    #open application
    elif 'launch' in command:
        reg_ex = re.search('launch\s(.*)', command)
        if reg_ex:
            appname = reg_ex.group(1)
            appname1 = appname + ".app"
            subprocess.Popen(["open", "-n", "/Applications/" + appname1], stdout=subprocess.PIPE)
        IvyResponse("I have launch the application as you wanted, No thanks needed!")
    
    #Using wolframalpha to calculate, tell weather in a specific city + specific day.
    elif 'calculate' in command:
        app_id = "PUK3TX-59QXTTY2EY"
        client = wolframalpha.Client(app_id)
        indx = command.lower().split().index('calculate')
        query = command.split()[indx +1:]
        res = client.query(' '.join(query))
        answer = next(res.results).text
        IvyResponse("The answer is " + answer)
        return
    elif 'information' in command:
        IvyResponse('What do you need to know, ' + name + '?')
        ans = myCommand()
        if 'specific' in str(ans) or 'temperature' in str(ans):
            IvyResponse("Where to, sir?")
            temp_location = myCommand()
            IvyResponse('Which day?')
            temp_time = myCommand()
            IvyResponse('On it! Give me a sec')
            app_id = "PUK3TX-59QXTTY2EY"
            client = wolframalpha.Client(app_id)
            res = client.query('temperture in ' + temp_location + ' on ' + temp_time)
            answer = next(res.results).text
            IvyResponse("It is " + answer)
        else:
            pass
    
    
#Ivy text processing

def Ivytext(command):
    try:
        if "Who are you" in command or "define yourself" in command or "tell me about you" in command or "tell me about yourself" in command:
            speak = '''Hello, I am Ivy. Your personal assistant.
                    I am here to help you with your daily tasks.
                    If you want to know what I can do, please say "help me"!'''
            IvyResponse(speak)
            return

        elif "who made you" in command or 'who created you' in command:
            speak = ''' I have been created by Bailey Vu'''
            IvyResponse(speak)
            return
        elif 'crazy' in command:
            speak = '''Well, it is hard to keep cool in this dipshit life though!'''
            IvyResponse(speak)
            return
        elif 'what\'s up' in command:
            IvyResponse('Nothing.Just doing my thing')
            return
        elif 'joke' in command:
            res = requests.get(
                'https://icanhazdadjoke.com/',
                headers={"Accept":"application/json"}
                )
            if res.status_code == requests.codes.ok:
                IvyResponse(str(res.json()['joke']))
            else:
                IvyResponse('oops!I ran out of jokes')
        elif 'hello' in command:
            day_time = int(strftime('%H'))
            if day_time < 12:
                IvyResponse("Morning " + name + '. What cool thing you want to do today?')
            elif 12 <= day_time < 18:
                IvyResponse("Good afternoon! " + name)
            else:
                IvyResponse("Hello! It is the evening at the moment, How may I help you?")
        elif 'help me' in command:
            IvyResponse("""
                        My ability will be listed as the follwoing number, just use those word and I will make the magic happen:
                        1. Open reddit subreddit : I will open the subreddit in default browser
                        2. Open xyz.com: Please replace xyz with any website name and I will open it for you.
                        3. Google anything: I am able to 'google' anything for you. Just say 'google' plus the thing you want to search.
                        4. Send email: Follow up questions such as recipient name, content will be asked in order.
                        5. Current weather and forecast weather in {cityname}: I will tell you the current weather and forecast status in a specific place.
                        6. Hello : You know what is this for, right?
                        7. Calculating: I am capable of calculate almost everything. Try me!
                        8. Time: Displaying current system time
                        9. Tell me about xyz: Replace xyz with what you wanna know, I got the whole wiki and google library so give me your best shot!!
                        """)
        elif "calculate" or "calcation" in command:
            IvyAbility(command.lower())
        elif "launch" in command:
            IvyAbility(command.lower())
        elif "email" in command or "mail" in command:
            IvyAbility(command.lower())
        elif "current weather in" in command or "weather forecast" in command:
            IvyAbility(command.lower())
        elif "open google" in command or "open reddit" in command:
            IvyAbility(command.lower())
        elif 'open' in command:
            IvyAbility(command.lower())
        elif "google" in command:
            IvyAbility(command.lower())
        elif "information" in command:
            IvyAbility(command.lower())
        elif 'time' in command:
            IvyAbility(command.lower())
        elif 'what day is' in command:
            IvyAbility(command.lower())
        elif 'tell me about' in command:
            IvyAbility(command.lower())
        else:
            IvyResponse('I can search the web for you on this. Do you want me to continue?')
            ans = myCommand()
            if "yes" in str(ans) or "yeah" in str(ans):
                reg_ex = re.search('find(.*)', command)
                if reg_ex:
                    domain = reg_ex.group(1)
                    url = 'https://www.google.com/search?q=' + domain
                    webbrowser.open(url)
                    IvyResponse("I has searched your requested on website. Take a look at what I found")
                else:
                    return
    except Exception as e:
        print(e)
        IvyResponse("I don\'t understand but I can search it for you. Do you want me to continue?")
        ans = myCommand()
        if "yes" in str(ans) or "yeah" in str(ans):
            reg_ex = re.search('find(.*)', command)
            if reg_ex:
                domain = reg_ex.group(1)
                url = 'https://www.google.com/search?q=' + domain
                webbrowser.open(url)
                IvyResponse("I has searched your requested on website. Take a look at what I found")
            else:
                return


if __name__ == "__main__":
    IvyResponse("This is Ivy!Hello and welcome! How can I call you?")
    name = 'bailey'
    greeting1 = "Hello, " + str(name) + '. What a lovely day isn\'t it!'
    greeting2 = 'O la, ' + str(name) + '.'
    greeting3 = 'What\'s up, ' + str(name) + '.'
    if 'my' in name or 'mine' in name:
        IvyResponse('It should be Mai, right gal?')
        ans = myCommand()
        name = 'Mai'
        IvyResponse(random.choice([greeting1, greeting2, greeting3]))
    else:
        IvyResponse(random.choice([greeting1, greeting2, greeting3]))
    helper1 = 'Before we start anything, please say help me if you wish to know about my ability. And it is quite impressive though.'
    helper2 = 'For begining, if you want to know what I am capable of. Please say help me. and by the way, I love working with you.' 
    #IvyResponse(random.choice([helper1, helper2]))
    while(1):
        IvyResponse('What can I do for you?')
        text = myCommand()
        if text == 0:
            continue
        elif "shut down" in str(text) or 'bye' in str(text) or 'sleep' in str(text) or 'nothing' in str(text):
            IvyResponse("Bye bye, " + str(name) + '.' + 'See you later then!')
            break
        Ivytext(text)
       
        
        
           
            
        