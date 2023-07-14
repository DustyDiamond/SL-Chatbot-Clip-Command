#!/usr/bin/python
# -*- coding: utf-8 -*-
#---------------------------------------------------------
# Import Libraries
#---------------------------------------------------------
import os
import json
import codecs
import socket

from datetime import datetime
from wsgiref import headers

#---------------------------------------------------------
# TODO:
#---------------------------------------------------------
#
# - Twitch Auth and Access Token geschiss machen
# - Twitch Clip API ansprechen und Clip machen --> Stream muss laufen :/
# - Discord Webhook Clip posten (in hübsch)
#
#---------------------------------------------------------
# Script information
#---------------------------------------------------------
ScriptName = "Clip Command"
Website = "https://github.com/DustyDiamond/SL-Chatbot-Clip-Command/blob/main/README.md"
Description = "Creates a clip from your twitch stream and additionally posts it to your Discord."
Creator = "DustyDiamond"
Version = "1.0.1"
Command = "!clip"

#---------------------------------------------------------
# Globals
#---------------------------------------------------------
settings = {}


def Init() :
    global settings

    work_dir = os.path.dirname(__file__)

    try:
        with codecs.open(os.path.join(work_dir, "settings.json"), encoding='utf-8-sig') as json_file:
            settings = json.load(json_file, encoding='utf-8-sig')
    
    except:
        log("ERROR", "Unable to load settings during execution! (Init)")

    return

def Execute(data) :
    global settings, auth_code
    if data.IsChatMessage():
        if data.GetParam(0) == "":
            log("No Param.")
            return
        
        if data.GetParam(0) != settings["command"] :
            log("ERROR", "False Command!")
            return
        
        #Chat Message is command
        client_id = "agndv2i9pthjjr826s7k0y5fnrlbn1"
        client_secret = "icedfycphp5v5tz0k5up9i98ahazvr"
        auth_code = "piwuksfhwoo04fgln0l7dan4whf1u5"
        app_token = ""
        headers= {"Client_ID" : client_id, "Authorization" : "OAuth " +app_token}
        content= {}
        validToken = 0

        
        validateRequest = json.loads(Parent.PostRequest("https://id.twitch.tv/oauth2/validate",headers,content,True))
        #log("TEST", validateRequest)

        if validateRequest["status"] == 200 :
            validToken = 1
            log("INFO", "Twitch Token Valid")

        if validToken == 0 :
            log("INFO", "Twitch Token not Valid. Trying to get a Valid one")
            headers={}
            tokenRequest = json.loads(Parent.PostRequest('https://id.twitch.tv/oauth2/token?client_id=' + client_id +'&client_secret=' + client_secret + '&grant_type=client_credentials',headers,content,True))
            if tokenRequest["status"] == 200:
                log("INFO", "Twitch Token Valid")
                log("TEST", str(tokenRequest))
                response = json.loads(tokenRequest["response"])
                app_token = response["access_token"]



        send_message(settings["bot_response"])

        return

         
    return

# Misc Functions
#def http_post(url, data):
#    post = urlencode(data)
#    req = urllib2.Request(url, post)
#    response = urllib2.urlopen(req)
#    return response.getcode()

def log(severity, message):
    now = datetime.now()
    dt_string = now.strftime("%d.%m.%Y %H:%M:%S")
    Parent.Log(severity +": ","[" + ScriptName + "] " + dt_string + ": " + message)
    return

def send_message(message):
    Parent.SendStreamMessage(message)
    log("INFO", "Message Sent: " + message)
    return

def opentwitchtoken():
    log("INFO", "Twitch OAuth BTN Pressed")
    global auth_code

    HOST = '127.0.0.1'
    PORT = 3000

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST,PORT))
        s.listen()
    
    #auth_code = Parent.GetRequest("https://id.twitch.tv/oauth2/authorize?response_type=token&client_id=agndv2i9pthjjr826s7k0y5fnrlbn1&redirect_uri=http://localhost:3000&scope=clips%3Aedit")
    #log("TEST", str(auth_code))
    OpenWebSite("https://id.twitch.tv/oauth2/authorize?response_type=token&client_id=agndv2i9pthjjr826s7k0y5fnrlbn1&redirect_uri=http://localhost:3000&scope=clips%3Aedit")

    conn, addr = s.accept()
    with conn:
        log("INFO", "Connected by ", addr)
    while True:
        data = conn.recv(1024)
        if not data:
            break
        conn.sendall(data)

    
    

def opengithub():
    OpenWebSite(Website)

def OpenWebSite(url):
	os.startfile(url)
    
def ReloadSettings(jsonData):
    Init()
    return

def Tick():
    return

def Unload():
    return

# Define Helper Functions
def left(s, amount):
    return s[:amount]

def right(s, amount):
    return s[-amount:]

def mid(s, offset, amount):
    return s[offset:offset+amount]