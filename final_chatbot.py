import datetime
from tkinter import *
from PIL import Image
from time import ctime
import time
import speech_recognition as sr
import webbrowser
import random
import pyttsx3
from threading import Thread
import os
import requests
from bs4 import BeautifulSoup

global flag
flag=False

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
rate=engine.getProperty('rate')
engine.setProperty('rate' , rate-10)


def animination(count_images):
    global anim,label_for_image1
    label_for_image1=Label(putting_label,width=742,height=511,bg='gray17')
    label_for_image1.place(x=6,y=2)
    new_image_variable = images[count_images]
    label_for_image1.configure(image=new_image_variable)
    count_images = count_images + 1
    if count_images == no_of_frames:
        count_images = 0
    anim = root.after(70,lambda: animination(count_images))

def alexa_speak(audio_string):
    global anim,chatting_text_label,change1,change2
    r = random.randint(1, 1000000)
    audio_file = 'audio-' + str(r) + '.mp3'
    engine.say(audio_string)
    engine.runAndWait()
    print(audio_file)
    root.after_cancel(anim)
    canvas2.itemconfig(change1, text=" ")
    canvas2.itemconfig(change2, text=" ")


def actual_result_executing(data):
    alexa_speak(data)

def web_scrapping(qs):
    global flag,change1,change2,wiki
    print(" sun be ")
    url = 'https://google.com/search?q=' + qs
    #webbrowser.get().open(url)
    page=requests.get(url)
    soup=BeautifulSoup(page.content,'html.parser')
    links=soup.findAll("a")
    all_links=[]
    for link in links:
        link_href=link.get('href')
        if "url?q" in link_href and not "webcache" in link_href:
            all_links.append((link.get('href').split("?q=")[1].split("&sa=U")[0]))

    for link in all_links:
        if 'https://en.wikipedia.org/wiki/' in link:
            wiki = link
            flag=True
            break

    div0=soup.find_all('div',class_="KvKEAb")
    div1=soup.find_all("div",class_="Ap5OSd")
    div3=soup.find_all("div",class_="BNeawe iBp4i AP7Wnd")
    if len(div0)!=0:
        answer=div0[0].text
    elif len(div1)!=0:
        answer=div1[0].text+"\n"+div1[0].find_next_sibling("div").text
    elif len(div3)!=0:
        answer=div3[1].text

    elif flag==True:
        page2=requests.get(wiki)
        soup=BeautifulSoup(page2.text,'html.parser')
        title=soup.select("#firstHeading")[0].text
        paragraph=soup.select("p")
        for para in paragraph:
            if bool(para.text.strip()):
                answer=title+"\n"+para.text
                break
    else:
        answer="Sorry. I could not find the desired results"

    print("you search is processing please wait....")
    canvas2.itemconfig(change1, text="you search is processing please wait....")
    time.sleep(2)
    canvas2.itemconfig(change1, text=qs)
    canvas2.itemconfig(change2,text=answer,font=("Candara Light",14,'italic bold'),fill='white',width=350)
    task5 = Thread(target=animination(count_images))
    task5.start()
    task4 = Thread(target=actual_result_executing(answer))
    task4.start()

def record_audio():
    global anim,not_getting_text,change1, count_images
    r = sr.Recognizer()
    canvas2.itemconfig(change1, text="I am Listening.....")
    actual_result_executing("I am Listening")
    canvas2.itemconfig(change1, text="I am Listening.....")
    with sr.Microphone() as source:
        print("I am listening \n")
        r.pause_threshold = 1
        audio = r.listen(source)
        print("check")
        voice_data = " "
        try:
            voice_data = r.recognize_google(audio)
            print("check")
        except sr.UnknownValueError:
            not_getting_text="Sorry , I did not get that "
            canvas2.itemconfig(change1, text=" ")
            canvas2.itemconfig(change1,text=not_getting_text)
            task9=Thread(target=actual_result_executing(not_getting_text))
            task9.start()
            task10=Thread(target=animination(count_images))
            task10.start()
            print("check")
        except sr.RequestError:
            not_getting_text="Sorry , my speech services is down "
            canvas2.itemconfig(change1, text=" ")
            canvas2.itemconfig(change1,text=not_getting_text)
            task9 = Thread(target=actual_result_executing(not_getting_text))
            task9.start()
            task10 = Thread(target=animination(count_images))
            task10.start()
            print("check")
        print("check")
        print(voice_data)
        return voice_data

def respond(voice_data):
    global count_images,change1,change2
    print(voice_data)
    if 'what time is it' in voice_data:
        canvas2.itemconfig(change1,text="what time is it ?")
        t=ctime()
        canvas2.itemconfig(change2, text=t)
        task6 = Thread(target=animination(count_images))
        task6.start()
        task7 = Thread(target=actual_result_executing(ctime()))
        task7.start()
    if 'open YouTube' in voice_data:
        print(voice_data)
        canvas2.itemconfig(change1, text="opening youtube please wait....")
        time.sleep(1)
        th2=Thread(target=animination(count_images))
        th2.start()
        th1=Thread(target=actual_result_executing("opening youtube please wait"))
        th1.start()
        webbrowser.get().open("https://www.youtube.com/")
        canvas2.itemconfig(change1, text=" You tube opened.. ")
    if 'open Google' in voice_data:
        canvas2.itemconfig(change1, text="opening google please wait....")
        time.sleep(1)
        th1=Thread(target=actual_result_executing("opening google please wait"))
        th1.start()
        th2=Thread(target=animination(count_images))
        th2.start()
        webbrowser.open("www.google.com")
        canvas2.itemconfig(change1, text=" google opened.. ")
    if 'open stack overflow' in voice_data:
        canvas2.itemconfig(change1, text="opening stack overflow please wait....")
        time.sleep(1)
        th1=Thread(target=actual_result_executing("opening stack overflow please wait"))
        th1.start()
        th2=Thread(target=animination(count_images))
        th2.start()
        webbrowser.open("www.stackoverflow.com")
        canvas2.itemconfig(change1, text="stack overflow opened.. ")
    if 'open Gmail' in voice_data:
        canvas2.itemconfig(change1, text="opening gmail please wait....")
        time.sleep(1)
        th1=Thread(target=actual_result_executing("opening gmail please wait"))
        th1.start()
        th2=Thread(target=animination(count_images))
        th2.start()
        webbrowser.open("www.gmail.com")
        canvas2.itemconfig(change1, text="gmail opened.. ")
    if 'open Github' in voice_data:
        canvas2.itemconfig(change1, text="opening github please wait....")
        time.sleep(1)
        th1=Thread(target=actual_result_executing("opening github please wait"))
        th1.start()
        th2=Thread(target=animination(count_images))
        th2.start()
        webbrowser.open("https://github.com/")
        canvas2.itemconfig(change1, text="github is opened .. ")
    if "play song" in voice_data:
        canvas2.itemconfig(change1, text="playing songs please wait....")
        time.sleep(1)
        th1=Thread(target=actual_result_executing("playing songs please wait"))
        th1.start()
        th2=Thread(target=animination(count_images))
        th2.start()
        music_dir = "C:\\Users\\hp\\Music\\python project songs"
        songs = os.listdir(music_dir)
        print(songs)
        canvas2.itemconfig(change1, text="Song played...")
        os.startfile(os.path.join(music_dir, random.choice(songs)))
    if 'search' in voice_data:
        canvas2.itemconfig(change1, text="what do you want to search for?")
        task5 = Thread(target=animination(count_images))
        task5.start()
        task4 = Thread(target=actual_result_executing("what do you want to search for?"))
        task4.start()
        search = record_audio()
        print("voice recorded please wait....")
        canvas2.itemconfig(change1, text="voice recorded\nplease wait....")
        time.sleep(1)
        url = 'https://google.com/search?q=' + search
        webbrowser.get().open(url)
        web_scrapping(search)
    if 'find location' in voice_data:
        canvas2.itemconfig(change1, text="what is the location you want to find ?")
        task5 = Thread(target=animination(count_images))
        task5.start()
        task4 = Thread(target=actual_result_executing("what is the location you want to find ?"))
        task4.start()
        location = record_audio()
        print("voice recorded please wait....")
        canvas2.itemconfig(change1, text="voice recorded\nplease wait....")
        time.sleep(1)
        url = 'https://google.nl/maps/place/' + location + '/&amp;'
        webbrowser.get().open(url)
        web_scrapping(location)
    if 'exit' in voice_data:
        canvas2.itemconfig(change1, text=" Thanks for using our service \n shuting down....")
        actual_result_executing( "Thanks for using our service  shuting down" )
        root.destroy()
        exit()

def take_response():
    global change1
    while 1:
        voice=record_audio()
        print(voice)
        respond(voice)

def alexa_speak1(audio_string1):
    global anim, flag
    r = random.randint(1, 1000000)
    audio_file = 'audio-' + str(r) + '.mp3'
    engine.say(audio_string1)
    engine.runAndWait()

    print(audio_file)
    root.after_cancel(anim)
    take_response()


def wishme():
    global canvas2,change1,change2
    hours=datetime.datetime.now().hour
    if 0<=hours<12:
        text="Good Morning Dear User \n I am Alexa \n How can I Help You?"
    elif 12<= hours<18:
        text="Good Afternoon Dear User\n I am Alexa\n How can I Help You?"
    else:
        text="Good Evening Dear User \n I am Alexa \n How can I Help You?"
    change1=canvas2.create_text(10, 10, anchor=NW, justify=LEFT,text=text, font=('comicsansms', 14, 'italic bold'),fill='cyan2'
                                )
    change2=canvas2.create_text(400,450, anchor=E, justify=LEFT,text=" ", font=('comicsansms', 14, 'italic bold'),fill='pink')
    alexa_speak1(text)

def greetings():
    task=Thread(target=wishme)
    task.start()
    p2=Thread(target=animination(count_images))
    p2.start()

global call
call=1

def animination1(count_images1):
    global anim1,call

    label_for_loading = Label(Calling_Alexa_Label, width=120, height=120, bg='gray20')
    label_for_loading.place(x=300, y=270)

    new_image_variable1 = images1[count_images1]
    label_for_loading.configure(image=new_image_variable1)

    count_images1 = count_images1 + 1
    call=call+1
    if count_images1 == no_of_frames1:
        count_images1= 0
    if(call==100):
        greetings()
    else:
        anim1= root.after(40,lambda: animination1(count_images1))

def call_loading():
    smilefacebutton3.place_forget()
    smilefacebutton2.place_forget()
    smilefacebutton1.place_forget()
    Calling_Alexa_Label.configure(text="Please Wait... \n Alexa Will Connect Wtih You In Few Seconds",
                                  font=('arial',25,'italic bold'))
    animination1(count_images1)

def create():
    global label_for_image,no_of_frames,count_images,anim,images,start,putting_label,smile1,smile2,smile3,smilefacebutton1
    global smilefacebutton2,smilefacebutton3,anim1,count_images1,no_of_frames1,images1,label_for_loading,Calling_Alexa_Label
    global see_text_frame,canvas2,chat_bot_image

    #################### putting gif #################
    start = PhotoImage(file='game_start_button.png')
    smile1 =PhotoImage(file='smile.png')
    smile2 = PhotoImage(file='smile.png')
    smile3 = PhotoImage(file='smile.png')
    chat_bot_image=PhotoImage(file="chatbot1.png")


    ########## resizing the images ############
    start = start.subsample(9, 9)
    smile1 = smile1.subsample(8, 8)
    smile2 = smile2.subsample(8, 8)
    smile3 = smile3.subsample(8, 8)
    chat_bot_image=chat_bot_image.subsample(2,1)

    information = Image.open('raikwal.gif')
    no_of_frames = information.n_frames
    print(no_of_frames)
    images = []
    for i in range(no_of_frames):
        Gif=PhotoImage(file='raikwal.gif', format=f'gif -index {i}')
        Gif=Gif.subsample(2,1)
        images.append(Gif)

    count_images=0

    anim = None

    #################### creating the label for two frames ###################
    chatbot_image_label=Label(root,bg="aquamarine",width=118,height=60)
    chatbot_image_label.grid(row=0,column=0,padx=2,pady=2)

    chatting_label=Label(root,bg='aquamarine',width=67,height=45)
    chatting_label.grid(row=0,column=1,padx=5,pady=8)

    ##################  creating the frames for chatbot_image_label and chatting_label ################

    chatbot_image_frame=LabelFrame(chatbot_image_label,bg='gray17',width=800,height=678,text="Chatbot",font=('arial',15,'italic bold'),
                                   fg='cyan2',bd=8)
    chatbot_image_frame.grid(row=0,column=0,padx=2,pady=2)

    see_text = LabelFrame(chatting_label, width=540, height=636, text="SEE TEXT", font=('comicsansms', 12, 'italic bold'),
                          fg='aquamarine',
                          bg='gray17', bd=8)
    see_text.place(x=2, y=3)

    canvas2 = Canvas(see_text, width=420, height=636, bg="gray17", scrollregion=(0, 0, 12, 1000), bd=2)
    canvas2.pack(side=LEFT, expand=True, fill=BOTH, padx=2)
    scroll = Scrollbar(see_text, orient=VERTICAL)
    scroll.pack(side=RIGHT, fill=Y)
    scroll.configure(command=canvas2.yview)
    canvas2.configure(yscrollcommand=scroll.set)

    label_for_design=Label(chatbot_image_frame,width=110,height=37,bg='cyan2')
    label_for_design.place(x=6,y=1)

    putting_label=LabelFrame(label_for_design,width=769,height=555,bg='gray17',bd=8,text='Alexa',
                             font=('arial',15,'italic bold'),fg='cyan2')
    putting_label.place(x=1,y=1)


    label_for_image=Label(putting_label,width=106,height=34,bg='gray20')
    label_for_image.place(x=6,y=2)


    #################### calling the alexa ##########################
    Calling_Alexa_Label=Label(label_for_image,width=37,height=10,bg="gray20",text='Please Click On Start Button \n For Calling Alexa',
                              font=('arial',26,'italic bold'),fg='cyan2')
    Calling_Alexa_Label.place(x=1,y=20)

    label_for_loading = Label(Calling_Alexa_Label, width=120, height=120, bg='yellow')
    label_for_loading.place(x=300, y=270)

    label_for_loading.place_forget()

    smilefacebutton1 = Label(Calling_Alexa_Label, width=80, height=80, image=smile1, bg='gray20', bd=0)
    smilefacebutton1.place(x=225, y=250)

    smilefacebutton2 = Label(Calling_Alexa_Label, width=80, height=80, image=smile2, bg='gray20', bd=0)
    smilefacebutton2.place(x=325, y=250)

    smilefacebutton3 = Label(Calling_Alexa_Label, width=80, height=80, image=smile3, bg='gray20', bd=0)
    smilefacebutton3.place(x=425, y=250)



    information1 = Image.open('loading.gif')
    no_of_frames1 = information1.n_frames
    print(no_of_frames1)
    images1 = []
    for i in range(no_of_frames1):
        Gif1=PhotoImage(file='loading.gif', format=f'gif -index {i}')
        Gif1=Gif1.subsample(2,2)
        images1.append(Gif1)

    count_images1=0

    anim1 = None

    Start_image_label=Label(chatbot_image_frame,bg="gray17",width=20,height=2)
    Start_image_label.place(x=340,y=565)

    Start_button=Button(Start_image_label,image=start,width=90,height=70,bg="gray17",activebackground="gray17",bd=0
                        ,command=call_loading)
    Start_button.grid(row=0,column=0,padx=1,pady=1)

root=Tk()
root.geometry("1300x720+34+0")
root.title("Amazing ChatBot ")
root.configure(bg='gray17')
root.resizable(False,False)
create()
root.mainloop()