import os
import ndstextgen
import tkinter
import colorsys
import math
import threading
from tkinter import *
from PIL import Image,ImageTk

# hold messages
allMsgIDs = {0: None}
lastProcessedID = 0
msgLabel = [None]

# load all images only once
msgBoxTop = Image.open("msgTop.png")
msgBoxTop = msgBoxTop.convert("RGBA")
msgBoxMiddle = Image.open("msgMiddle.png")
msgBoxMiddle = msgBoxMiddle.convert("RGBA")
msgBoxBottom = Image.open("msgBottom.png")
msgBoxBottom = msgBoxBottom.convert("RGBA")
userBoxMultiLeft = Image.open("userMultiLeft.png")
userBoxMultiLeft = userBoxMultiLeft.convert("RGBA")
userBoxMultiMiddle = Image.open("userMultiMiddle.png")
userBoxMultiMiddle = userBoxMultiMiddle.convert("RGBA")
userBoxMultiRight = Image.open("userMultiRight.png")
userBoxMultiRight = userBoxMultiRight.convert("RGBA")
userBoxMulti = Image.open("userMulti.png")
userBoxMulti = userBoxMulti.convert("RGBA") 
msgBoxSingle = Image.open("msg.png")
msgBoxSingle = msgBoxSingle.convert("RGBA")
userBoxSingleLeft = Image.open("userLeft.png")
userBoxSingleLeft = userBoxSingleLeft.convert("RGBA")
userBoxSingleMiddle = Image.open("userMiddle.png")
userBoxSingleMiddle = userBoxSingleMiddle.convert("RGBA")
userBoxSingleRight = Image.open("userRight.png")
userBoxSingleRight = userBoxSingleRight.convert("RGBA")
userBoxSingle = Image.open("user.png")
userBoxSingle = userBoxSingle.convert("RGBA")

# Function to read textbox and add text   
def genImg(userText, color, msgText):
    # make vars global  
    # global msgGen, msgImg, canvas, msgNum, staleMsgNum
    # load & calculate colors
    colorR = int(color[0:2],16)
    colorG = int(color[2:4],16)
    colorB = int(color[4:6],16)
    colorH = colorsys.rgb_to_hls(colorR / 255, colorG / 255, colorB / 255)[0]
    colorL = colorsys.rgb_to_hls(colorR / 255, colorG / 255, colorB / 255)[1]
    colorS = colorsys.rgb_to_hls(colorR / 255, colorG / 255, colorB / 255)[2]
    if colorS != 0 and 0.3 <= colorL <= 0.7:
        modR = colorsys.hls_to_rgb(colorH, min(colorL * 1.73, 1), max(colorS * 0.89, 0))[0] * 255
        modG = colorsys.hls_to_rgb(colorH, min(colorL * 1.73, 1), max(colorS * 0.89, 0))[1] * 255
        modB = colorsys.hls_to_rgb(colorH, min(colorL * 1.73, 1), max(colorS * 0.89, 0))[2] * 255
    else:
        modR = colorsys.hls_to_rgb(colorH, 0.5, 0)[0] * 255
        modG = colorsys.hls_to_rgb(colorH, 0.5, 0)[1] * 255
        modB = colorsys.hls_to_rgb(colorH, 0.5, 0)[2] * 255
    # load username text    
    userText = "Îq" + userText
    # generate username image
    userGen = ndstextgen.gen("NTR_IPL_font_s.NFTR", userText, out=os.devnull, spacing=1, color="#010101", encoding="utf_16", no_esc=True)
    # load message text
    msgText = "Îqiiiiiiiiiiiiiiiiiiiiiii" + msgText
    if userGen.width > 50 and userGen.width % 2 == 0:
        for i in range(int(((userGen.width - 62) / 2))):
            msgText = "i" + msgText
    elif userGen.width > 50 and userGen.width % 2 == 1:
        for i in range(int(((userGen.width - 62) / 2)) - 1):
            msgText = "i" + msgText
        msgText = "l" + msgText
    # generate message image
    msgGen = ndstextgen.gen("NTR_IPL_font_s.NFTR", msgText, out=os.devnull, vert=4, spacing=1, color="black", width=222, wwrap=True, encoding="utf_16", no_esc=True)
    # crop out dumb hack
    userGen = userGen.crop((11, 0, userGen.width, userGen.height))
    # process all images and assemble message box
    if msgGen.height > 12:
        newMsgBoxH = 22 + (16 * ((math.ceil(msgGen.height / 16) - 1)))
        msgBox = msgBoxMiddle.resize((234, newMsgBoxH), 4)
        msgBox.paste(msgBoxTop, (0, 0))
        msgBox.paste(msgBoxBottom, (0, msgBox.height - 6))
        msgBox.paste(msgGen, (6,4), msgGen)
        if userGen.width > 50:
            newUserBoxW = userGen.width + 13
            userBox = userBoxMultiMiddle.resize((newUserBoxW, 19), 4)
            userBox.paste(userBoxMultiLeft, (0, 0), userBoxMultiLeft)
            userBox.paste(userBoxMultiRight, (newUserBoxW - 6, 0), userBoxMultiRight)
            userBox.paste(userGen, (6, 4), userGen)
        else:
            userBoxMulti.paste(userGen, (6, 4), userGen)
            userBox = userBoxMulti
        msgBox.paste(userBox, (0, 0))
    else:
       
        msgBoxSingle.paste(msgGen, (6, 4), msgGen)
        if userGen.width > 50:
           
            newUserBoxW = userGen.width + 13
            userBox = userBoxSingleMiddle.resize((newUserBoxW, 22), 4)
            userBox.paste(userBoxSingleLeft, (0, 0))
            userBox.paste(userBoxSingleRight, (newUserBoxW - 6, 0))
            userBox.paste(userGen, (6, 4), userGen)
        else:
            userBoxSingle.paste(userGen, (6, 4), userGen)
            userBox = userBoxSingle
        msgBoxSingle.paste(userBox, (0, 0), userBox)
        msgBox = msgBoxSingle
    recolor = msgBox.load()
    for i in range(msgBox.size[0]):
        for j in range(msgBox.size[1]):
            if msgBox.getpixel((i, j)) == (1, 1, 1, 255):
                msgBox.putpixel((i, j),(colorR, colorG, colorB, 255))
            elif msgBox.getpixel((i, j)) == (2, 2, 2, 255):
                msgBox.putpixel((i, j),(round(modR), round(modG), round(modB), 255))
    return msgBox
    
def addImg(userText, color, msgText, curMsgID):
    msgImg = genImg(userText, color, msgText)
    msgID = {curMsgID + 1: ImageTk.PhotoImage(msgImg)}
    return msgID
    
def addID(preID, img):
    id = preID + 1
    allMsgIDs.update({id: img})
    return allMsgIDs
    
def sendFromTextbox():
    global allMsgIDs
    msgBox = addImg(userTextbox.get(), colorTextbox.get(), msgTextbox.get(), getCurID())
    allMsgIDs.update(msgBox)
    chat.update()
    chat.after(1, drawMsg)
    
def getCurID():
    return list(allMsgIDs.items())[-1][0]

def drawMsg():
    global lastProcessedID
    if getCurID() > lastProcessedID:
        curID = getCurID()
        msgLabel.insert(curID, Label(messageFrame, image=allMsgIDs.get(curID), bd=1, anchor="nw"))
        msgLabel[curID].pack(side="top", anchor="nw")
        # update canvas stuff
        canvas.update_idletasks() 
        canvas.configure(scrollregion = canvas.bbox("all"))
        canvas.yview_moveto(1)
        # update IDs
        lastProcessedID = curID
    chat.after(1, drawMsg)
    
# window init
chat=tkinter.Tk()
chat.title("Twitch Chat")
chat.configure(background="white")

## frame
frame = tkinter.Frame(chat)
frame.pack(fill=BOTH, expand=1)

# canvas
canvas = Canvas(frame, width=300, height=300)
canvas.pack(side="left", anchor="nw")

# message frame
messageFrame = tkinter.Frame(canvas)
canvas.create_window(0, 0, window=messageFrame, anchor="nw")

# scrollbar
scrollbar = Scrollbar(frame, command=canvas.yview)
scrollbar.pack(side="right", fill="y", anchor="nw")

# canvas config
canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion = canvas.bbox("all")))
canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1* (e.delta / 120)),  "units"))

# username textbox
userTextbox = tkinter.Entry(chat)
userTextbox.pack()

# color textbox
colorTextbox = tkinter.Entry(chat)
colorTextbox.pack()

# message textbox
msgTextbox = tkinter.Entry(chat)
msgTextbox.pack()

# gay button
gayButton = tkinter.Button(chat, text="Gay", command=sendFromTextbox)
gayButton.pack()

# tkinter stuff
chat.mainloop()