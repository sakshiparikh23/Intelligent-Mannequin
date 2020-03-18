import os
import random
import cv2
import speech_recognition as sr
import time
import datetime as dt

from gtts import gTTS

from email_user import email_user
from run_stt
import timeit
#import playsound
import time

import pymysql

## Video Start Part
cap = cv2.VideoCapture(0)                                                               # Start Video Camera
# Define Video Resolution of 320 by 240 pixels
cap.set(3,320)
cap.set(4,240)

def add_data(Input_List):

    connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='',
                                     db='intelligent_mannequin',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
    Colour = Input_List[0]
    Size   = Input_List[1]
    if(Colour != 0 and Size !=0):
        try:
            with connection.cursor() as cursor:
                # Read a single record
                sql = "INSERT INTO user_response (size,colour) VALUES (%s, %s)"
                cursor.execute(sql, (Size, Colour))
                connection.commit()
        finally:
            connection.close()

    elif(Colour == 0 and Size !=0):
        try:
            with connection.cursor() as cursor:
                # Read a single record
                sql = "INSERT INTO user_response (size) VALUES (%s)"
                cursor.execute(sql, Size)
                connection.commit()
        finally:
            connection.close()

    elif(Colour != 0 and Size == 0):
        try:
            with connection.cursor() as cursor:
                # Read a single record
                sql = "INSERT INTO user_response (colour) VALUES (%s)"
                cursor.execute(sql, Colour)
                connection.commit()
        finally:
            connection.close()

    else:
        return

## Face Detection Part
# Create the haar cascade for face detection
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

Input_List = [0,0];
Input_List2 = [0,0];

# Start Camera
while True:
    # Loop until the camera is working
    rval, frame = cap.read()                                                            # Read every frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)                                      # Convert it to grayscale
            # Detect faces in the image using this properties
    faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
                #flags=cv2.cv.CV_HAAR_SCALE_IMAGE
    )

    # Print this in command window
    print("Found {0} faces!".format(len(faces)))

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Show figure window to preview camera
    cv2.imshow("Faces found", frame)


    # Press "q" to stop capturing video and start scenario 1 or
    # Press "z" to stop capturing video and start scenario 2

    if cv2.waitKey(10) & 0xFF == ord('q'):
        sub_face = frame[y:y + h, x:x + w]                                          # Crop the face region from entire frame using coordinates
        face_file_name = "Faces/" + "test" + "_" + "face" + ".jpg"                  # Concatenate the filename to add cropped image to "Faces" folder with .jpg extension
        cv2.imwrite(face_file_name, sub_face)                                       # Write the extracted image with the imagename
        rval = True                                                                 # For looping purpose

        start_time = time.time()
        scenario = '1'
        sttr1 = 'y'
        break                                                                       # For stopping webcam video capture

    elif cv2.waitKey(10) & 0xFF == ord('z'):
        scenario = '2'
        sttr2 = 'y'
        break

# Destroy and close all the video objects
cap.release()
cv2.destroyAllWindows()


if scenario == '1' :
    # Scenario 1 begins
    ## TTS and STT Part
    # Scenario 1 - When Customer starts conversation
    scenario1_data = ""
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        if index == 0:
            mic_name = name
            print(name)

            while(sttr1 == 'y'):
                time.sleep(4)
                text = run_stt(name)

                print(text)
                if text == 'hi' or text == 'hello' or text == 'Hi' or text == 'Hello':
                    ti = dt.datetime.now().hour
                    if ti <= 12:
                        print("GM")
                        tts1 = gTTS(text='Good Morning !!', lang='en')
                        tts1.save("./Audios/gm.mp3")
                        os.system("start ./Audios/gm.mp3")
                        text_M = "Mannequin : \t" + "Good Morning !! \n"
                    elif ti > 12 and ti <= 17:
                        print("GA")
                        tts1 = gTTS(text='Good Afternoon !!', lang='en')
                        tts1.save("./Audios/ga.mp3")
                        os.system("start ./Audios/ga.mp3")
                        text_M = "Mannequin : \t" + "Good Afternoon !! \n"
                    elif ti > 17 and ti <= 20:
                        print("GE")
                        #tts1 = gTTS(text='Good Evening !!', lang='en')
                        #tts1.save("./Audios/ge.mp3")
                        os.system("start ./Audios/ge.mp3")
      
                        text_M = "Mannequin : \t" + "Good Evening !! \n"
                    elif ti > 20:
                        print("GN")
                        tts1 = gTTS(text='Good Night !!', lang='en')
                        tts1.save("./Audios/gn.mp3")
                        os.system("start ./Audios/gn.mp3")
                        text_M = "Mannequin : \t" + "Good Night !! \n"
                    sttr1 = 'y'

                    text_C = "Customer : \t" + text + "\n"
                    scenario1_data += text_C
                    scenario1_data += text_M
                    

                elif text == 'What is the material of this dress' or text == 'what is the material of this dress' or text == 'Which material is used' or text == 'which material is used':
                    rand_no = random.randint(1, 2)
                    if rand_no == 1 :
                        tts1 = gTTS(text='The material is Cotton', lang='en')
                        tts1.save("./Audios/material1.mp3")
                        os.system("start ./Audios/material1.mp3")
                        text_M = "Mannequin : \t" + "The material is Cotton. \n"
                        sttr1 = 'y'
                    elif rand_no == 2 :
                        tts1 = gTTS(text='The material is Velvet', lang='en')
                        tts1.save("./Audios/material2.mp3")
                        os.system("start ./Audios/material2.mp3")
                        text_M = "Mannequin : \t" + "The material is Cotton. \n"
                        sttr1 = 'y'

                    text_C = "Customer : \t" + text + "\n"
                    scenario1_data += text_C
                    scenario1_data += text_M



                elif text == 'What sizes are available' or text == 'what sizes are available' or text == 'what sizes available':
                    tts1 = gTTS(text='From small to XL are available.', lang='en')
                    tts1.save("./Audios/size.mp3")
                    os.system("start ./Audios/size.mp3")
                    text_M = "Mannequin : \t" + "From small to XL are available. \n"
                    sttr1 = 'y'

                    text_C = "Customer : \t" + text + "\n"
                    scenario1_data += text_C
                    scenario1_data += text_M

                elif text == 'XL' or text == 'small' or text == 'L' or text=='Large' or text == 'xl' or text == 'Small' or text == 'l' or text=='large':
                    tts1 = gTTS(text='Sure we have that!', lang='en')
                    tts1.save("./Audios/sizein.mp3")
                    os.system("start ./Audios/sizein.mp3")
                    sttr1 = 'y'
                    text_M = "Mannequin : \t" + "Sure we have that!. \n"

                    text_C = "Customer : \t" + text + "\n"
                    scenario1_data += text_C
                    scenario1_data += text_M
                    Input_List[1] = text;

                elif text == 'Which colours are available' or text == 'which colours are available' or text == 'which colours available':
                    tts1 = gTTS(text='Red,Blue,White.', lang='en')
                    tts1.save("./Audios/color.mp3")
                    os.system("start ./Audios/color.mp3")
                    text_M = "Mannequin : \t" + "Red,Blue,White. \n"
                    sttr1 = 'y'

                    text_C = "Customer : \t" + text + "\n"
                    scenario1_data += text_C
                    scenario1_data += text_M


                elif text == 'Red' or text == 'Blue' or text == 'White' or text == 'red' or text == 'blue' or text == 'white':
                    tts1 = gTTS(text='Sure we have that!', lang='en')
                    tts1.save("./Audios/colourin.mp3")
                    os.system("start ./Audios/colourin.mp3")
                    sttr1 = 'y'
                    text_M = "Mannequin : \t" + "Sure we have that!. \n"

                    text_C = "Customer : \t" + text + "\n"
                    scenario1_data += text_C
                    scenario1_data += text_M                   
                    Input_List[0] = text;


                elif text == 'What is the cost' or text == 'what is the cost' or text == 'What is the price' or text == 'what is the price':
                    tts1 = gTTS(text='1250 Rupees only', lang='en')
                    tts1.save("./Audios/amount.mp3")
                    os.system("start ./Audios/amount.mp3")
                    text_M = "Mannequin : \t" + "1250 Rupees only \n"
                    sttr1 = 'y'

                    text_C = "Customer : \t" + text + "\n"
                    scenario1_data += text_C
                    scenario1_data += text_M


                elif text == 'I want to buy this dress' or text == 'i want to buy this dress' :
                    tts1 = gTTS(text='I will place the order, kindly make the payment and collect your product from the counter.', lang='en')
                    tts1.save("./Audios/conclude.mp3")
                    os.system("start ./Audios/conclude.mp3")
                    text_M = "Mannequin : \t" + "I will place the order, kindly make the payment and collect your product from the counter. \n"
                    sttr1 = 'n'

                    text_C = "Customer : \t" + text + "\n"
                    scenario1_data += text_C
                    scenario1_data += text_M


                elif text == 'Google Speech Recognition could not understand audio' :
                    sttr1 = 'y'

            print("The conversation ends here. THANK YOU")

            email_status = email_user(scenario1_data)
            with open("Conversation.txt", "a") as text_file:text_file.write("\n%s" % scenario1_data)
            add_data(Input_List)
            Input_List = [0,0];

            break



elif scenario == '2' :
    # Scenario 2 begins
    ## TTS and STT Part
    # Scenario 2 - When Mannequin starts conversation
    scenario2_data = ""
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        if index == 0:
            mic_name = name
            print(name)


            ti = dt.datetime.now().hour
            if ti <= 12:
                print("GM")
                tts1 = gTTS(text='Good Morning !!', lang='en')
                tts1.save("./Audios/gm.mp3")
                os.system("start ./Audios/gm.mp3")
                text_M = "Mannequin : \t" + "Good Morning !! \n"
            elif ti > 12 and ti <= 17:
                print("GA")
                tts1 = gTTS(text='Good Afternoon !!', lang='en')
                tts1.save("./Audios/ga.mp3")
                os.system("start ./Audios/ga.mp3")
                text_M = "Mannequin : \t" + "Good Afternoon !! \n"
            elif ti > 17 and ti <= 20:
                print("GE")
                tts1 = gTTS(text='Good Evening !!', lang='en')
                tts1.save("./Audios/ge.mp3")
                os.system("start ./Audios/ge.mp3")
                text_M = "Mannequin : \t" + "Good Evening !! \n"
            elif ti > 20:
                print("GN")
                tts1 = gTTS(text='Good Night !!', lang='en')
                tts1.save("./Audios/gn.mp3")
                os.system("start ./Audios/gn.mp3")
                text_M = "Mannequin : \t" + "Good Night !! \n"
            time.sleep(2)
            tts1 = gTTS(text='You can ask me anything about this dress, I will try my best to answer your question.',
                        lang='en')
            tts1.save("./Audios/start_mann.mp3")
            os.system("start ./Audios/start_mann.mp3")

            scenario2_data += text_M
            text_M = "Mannequin : \t" + "You can ask me anything about this dress, I will try my best to answer your question. \n"
            scenario2_data += text_M
            sttr2 = 'y'
            time.sleep(7)
            while (sttr2 == 'y'):
                time.sleep(2)
                text = run_stt(name)
                if(text != 'Google Speech Recognition could not understand audio'):
                    with open("Conversation.txt", "a") as text_file:text_file.write("\n%s" % text)
                print(text)
                if text == 'What is the material of this dress' or text == 'what is the material of this dress' or text == 'Which material is used' or text == 'which material is used' or text == 'what is the material of distress'or text == 'What is the material of distress':
                    rand_no = random.randint(1, 2)
                    if rand_no == 1 :
                        tts1 = gTTS(text='The material is Cotton', lang='en')
                        tts1.save("./Audios/material1.mp3")
                        os.system("start ./Audios/material1.mp3")
                        sttr2 = 'y'
                        text_M = "Mannequin : \t" + "The material is Cotton. \n"
                    elif rand_no == 2 :
                        tts1 = gTTS(text='The material is Velvet', lang='en')
                        tts1.save("./Audios/material2.mp3")
                        os.system("start ./Audios/material2.mp3")
                        sttr2 = 'y'
                        text_M = "Mannequin : \t" + "The material is Velvet. \n"

                    text_C = "Customer : \t" + text + "\n"
                    scenario2_data += text_C
                    scenario2_data += text_M

                elif text == 'What sizes are available' or text == 'what sizes are available' or text == 'what sizes available':
                    tts1 = gTTS(text='From small to XL are available, What size will you like to buy?', lang='en')
                    tts1.save("./Audios/size.mp3")
                    os.system("start ./Audios/size.mp3")
                    sttr2 = 'y'
                    text_M = "Mannequin : \t" + "From small to XL are available, What size will you like to buy?. \n"

                    text_C = "Customer : \t" + text + "\n"
                    scenario2_data += text_C
                    scenario2_data += text_M

                elif text == 'XL' or text == 'small' or text == 'L' or text=='Large' or text == 'xl' or text == 'Small' or text == 'l' or text=='large':
                    tts1 = gTTS(text='Sure we have that!', lang='en')
                    tts1.save("./Audios/sizein.mp3")
                    os.system("start ./Audios/sizein.mp3")
                    sttr2 = 'y'
                    text_M = "Mannequin : \t" + "Sure we have that!. \n"

                    text_C = "Customer : \t" + text + "\n"
                    scenario2_data += text_C
                    scenario2_data += text_M
                    Input_list2[1] = text

                elif text == 'Which colours are available' or text == 'which colours are available' or text == 'which colours available':
                    tts1 = gTTS(text='Red,Blue,White, which one would you like?.', lang='en')
                    tts1.save("./Audios/color.mp3")
                    os.system("start ./Audios/color.mp3")
                    sttr2 = 'y'
                    text_M = "Mannequin : \t" + "Red,Blue,White, which one would you like?. \n"

                    text_C = "Customer : \t" + text + "\n"
                    scenario2_data += text_C
                    scenario2_data += text_M

                elif text == 'Red' or text == 'Blue' or text == 'White' or text == 'red' or text == 'blue' or text == 'white':
                    tts1 = gTTS(text='Sure we have that!', lang='en')
                    tts1.save("./Audios/colourin.mp3")
                    os.system("start ./Audios/colourin.mp3")
                    sttr2 = 'y'
                    text_M = "Mannequin : \t" + "Sure we have that!. \n"

                    text_C = "Customer : \t" + text + "\n"
                    scenario2_data += text_C
                    scenario2_data += text_M
                    Input_List2[0] = text

                elif text == 'What is the cost' or text == 'what is the cost' or text == 'What is the price' or text == 'what is the price':
                    tts1 = gTTS(text='1250 Rupees only', lang='en')
                    tts1.save("./Audios/amount.mp3")
                    os.system("start ./Audios/amount.mp3")
                    sttr2 = 'y'
                    text_M = "Mannequin : \t" + "1250 Rupees only \n"

                    text_C = "Customer : \t" + text + "\n"
                    scenario2_data += text_C
                    scenario2_data += text_M


                elif text == 'I want to buy this dress' or text == 'i want to buy this dress' :
                    tts1 = gTTS(text='I will place the order, kindly make the payment and collect your product from the counter.', lang='en')
                    tts1.save("./Audios/conclude.mp3")
                    os.system("start ./Audios/conclude.mp3")
                    sttr2 = 'n'
                    text_M = "Mannequin : \t" + "I will place the order, kindly make the payment and collect your product from the counter. \n"

                    text_C = "Customer : \t" + text + "\n"
                    scenario2_data += text_C
                    scenario2_data += text_M



                elif text == 'Google Speech Recognition could not understand audio' :
                    sttr2 = 'y'

            print("The conversation ends here. THANK YOU")

            email_status = email_user(scenario2_data)
            with open("Conversation.txt", "a") as text_file:text_file.write("\n%s" % scenario2_data)
            add_data(Input_List2)
            Input_List2 = [0,0];
            break







