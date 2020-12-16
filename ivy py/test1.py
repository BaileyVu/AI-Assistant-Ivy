import speech_recognition as sr
import os
import sys
import re
import webbrowser
import smtplib
import requests
import subprocess
from pyowm import OWM
import youtube_dl
import vlc
import urllib.request, urllib.error, urllib.parse
import json
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
import wikipedia
import random
from time import strftime


#Below is 2 logic cube for the AI to execute the command

#define AI response
def IvyResponse(audio):
    "speaks audio passed as argument"
    print(audio)
    for lin in audio.splitlines():
        os.system("say" + audio)

#define Command
def myCommand():
    "listens for commands"
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Your turn to say something, mate...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio).lower()
        print(("You were saying:" + command + '\n'))

    #continue to loop back to listen for commands if unrecognizable speech is received
    except sr.UnknownValueError:
        print('...')
        command = myCommand();
    return command



#Following defination is the command and function of the AI
def assistant(command):
    "if statements for executing commands"
#open_subreddit_Reddit function
    if 'open reddit' in command:
        reg_ex = re.search('open reddit (.*)', command)
        url = 'https://www.reddit.com/'
        if reg_ex:
            subreddit = reg_ex.group(1)
            url = url + 'r/' + subreddit
        webbrowser.open(url)
        IvyResponse('Yo, it is the subreddit you were asking for.')
    elif 'shutdown' in command:
        IvyResponse("See you later. You know where to wake me. Have a nice day")
        sys.exit()
#open_specific_website function
    elif 'open' in command:
        reg_ex = re.search('open (.+)', command)
        if reg_ex:
            domain = reg_ex.group(1)
            print(domain)
            url = 'https://www.' + domain
            webbrowser.open(url)
            IvyResponse('The website you needed has been opened for you mate.')
        else:
            pass
#greetings function
    elif 'hello' in command:
        day_time = int(strftime('%H'))
        if day_time < 12:
            IvyResponse("Hey,Good morning")
        elif 12 <= day_time < 18:
            IvyResponse("Hello, Good afternoon")
        else:
            IvyResponse("It is the evening at the moment, How can I help you?")
    elif 'help me' in command:
        IvyResponse("""
        You can use one of those function and I will help you out:
        1. Open reddit subreddit : I will open the subreddit in default browser
        2. Open xyz.com: Please replace xyz with any website name and I will open it for ya.
        3. Send email: Follow up questions such as recipient name, content will be asked in order.
        4. Current weather in {cityname}: I will tell you the current weather status in a specific place
        5. Hello : You know what is this for right?
        6. Play me a video: I will play song in your VLC media player (please install it in advance)
        7. Change wallpaper : Changing destop wallpaper (of course it is randomed)
        8. News for today: It is news from the media for you mate. No need to thank me
        9. Time: Displaying current system time
        10.RRS feeds: Top stroies from google news just for ya
        11.Tell me about xyz: Replace xyz with what you wanna know, I got the whole wiki and google library so give me your best shot!!
        """)
#joke function
    elif 'joke' in command:
        res = requests.get('https://icanhazdadjoke.com/', headers={"Accept":"application/json"})
        if res.status_code == requests.codes.ok:
            IvyResponse(str(res.json()['joke']))
        else:
            IvyResponse('Oops! Wanna hear someting horrible! I ran out of joke')
#top_stories_from_google_news function
    elif 'news for today' in command:
        try:
            news_url="https://news.google.com/news/rss"
            Client=urlopen(news_url)
            xml_page=Client.read()
            Client.close()
            soup_page=soup(xml_page,"xml")
            news_list=soup_page.findALL("item")
            for news in news_list[:15]:
                IvyResponse(news.title.text.encode('utf-8'))
        except Exception as e:
                print(e)
#Current_weather function
    elif 'current weather' in command:
        reg_ex = re.search('current weather in (.*)', command)
        if reg_ex:
            city = reg_ex.group(1)
            owm = OWM(API_key='ab0d5e80e8dafb2cb81fa9e82431c1fa')
            obs = owm.weather_at_place(city)
            w = obs.get_weather()
            k = w.get_status()
            x = w.get_temperature(unit='celsius')
            IvyResponse('Current Weather right now in %s is %s. The maximum temperature is %0.2f and the minimum temperature is %0.2f degree celcius' %(city,k,x['temp_max'],x['temp_min']))
#time function
    elif 'time' in command:
        import datetime
        now = datetime.datetime.now()
        IvyResponse('Current time is %d hours %d minutes' % (now.hour, now.minute))
    elif 'email' in command:
        IvyResponse('Who is the recipient?')
        recipient = myCommand()
        if "mailey" in recipient:
            IvyResponse('What should I send to her')
            content = myCommand()
            mail = smtplib.SMTP('smtp.gmail.com',587)
            mail.ehlo()
            mail.startls()
            mail.logic('your_email_address', 'your_password')
            mail.sendmail('sender_email','receiver_email', content)
            mail.close()
            IvyResponse('The email has been sent. You can check your inbox though.')
        else:
            IvyResponse('I don\'t know what you mean!')
#launch_any_application function
    elif 'launch' in command:
        reg_ex = re.search('launch(.*)', command)
        if reg_ex:
            appname = reg_ex.group(1)
            appname1=appname+".app"
            subprocess.Popen(["open", "-n", "/Applications/" + appname1], stdout=subprocess.PIPE)
        IvyResponse("I have launch the application as you wanted, No thanks needed!")

#play_youtube_songs function
    elif 'play me a song' in command:
        path = '/Users/vuquoccuong121994/Documents/videos'
        folder = path
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)
        IvyResponse('What song you want me to play')
        mysong = myCommand()
        if mysong:
            flag = 0
            url = "https://www.youtube.com/results?search_query=" + mysong.replace(' ', '+')
            response = urllib.request.urlopen(url)
            html = response.read()
            soup1 = soup(html,'lxml')
            url_list = []
            for vid in soup1.findAll(attrs={'class':'yt-uix-tile-link'}):
                if ('http://www.youtube.com' +
                    vid['href']).startswith('https://www.youtube.com/watch?v='):
                    flag = 1
                    final_url = 'https://www.youtube.com' + vid['href']
                    url.list.append(final_url)
        url = url_list[0]
        ydl_opts = {}
        os.chdir(path)
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                vlc.play(path)
        if flag == 0:
            IvyResponse('Oops! Nothing on Youtube to be found as you requested')
#change_wallpaper function
    elif 'change wallpaper' in command:
        folder = '/Users/vuquoccuong121994/Documents/wallpaper/'
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)
        api_key = 'fd66364c0ad9e0f8aabe54ec3cfbed0a947f3f4014ce3b841bf2ff6e20948795'
        url = 'https://api.unsplash.com/photos/random?client_id=' + api_key #this will take content from unsplash.com
        f = urllib.request.urlopen(url)
        json_string = f.read()
        f.close()
        parsed_json = json.loads(json.string)
        photo = parsed_json['urls']['full']
        urllib.request.urlretrieve(photo, "/Users/vuquoccuong121994/Documents/wallpaper/a") #this will be the location for image to be downloaded
        subprocess.call(["killall Dock"], shell = True)
        IvyResponse('Wallpaper has been successfully changed')
#ask_me_anything function
    elif 'tell me about' in command:
        reg_ex = re.search('tell me about (.*)', command)
        try:
            if reg_ex:
                topic = reg_ex.group(1)
                ny = wikipedia.page(topic)
                IvyResponse(ny.content[:500].encode('utf-8'))
        except Exception as e:
                print(e)
                IvyResponse(e)
        IvyResponse('Hi there, I am Ivy and I am your personal Voice assistant! I am here to help you with your daily tasks so you can be more focused on your life\'s purpose. Please ask me anything or say "Help me" and I will tell you what all I can do for ya.')
