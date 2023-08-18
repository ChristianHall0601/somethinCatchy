import customtkinter
import tkinter
import tkinter.filedialog
import os
import shutil
import pygame
import time


customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

pygame.mixer.init()
allOfFiles = os.listdir()
listOfPlaylist = []

win = customtkinter.CTk()
win.geometry("720x576")
win.title("somethinCatchy")
win.resizable(False, False)

def convertTime(seconds):
    timeMin = str(seconds//60)
    timeSecond = str(seconds%60)
    while len(timeMin)<2:
        timeMin = "0" + timeMin
    while len(timeSecond)<2:
        timeSecond = "0" + timeSecond
    myTime = timeMin + ":" + timeSecond
    return myTime

def isAudio(myFile):
    if(myFile.endswith(".mp3") or myFile.endswith(".wav") or myFile.endswith(".pcm") or myFile.endswith(".aiff") or myFile.endswith(".aac") or myFile.endswith(".ogg") or myFile.endswith(".wma") or myFile.endswith(".flac") or myFile.endswith(".alac") or myFile.endswith(".wma")):
        return True
    return False

def errorMsg(msg):
    errorWindow=customtkinter.CTk()
    errorWindow.geometry("360x200")
    errorWindow.title("Error")
    errorWindow.resizable(False,False)
    errorLbl = customtkinter.CTkLabel(master=errorWindow, font=("Times New Roman", 16), text=msg, fg_color="transparent", text_color="white")
    errorLbl.place(relx = 0.5, y = 20, anchor="n")
    okBtn = customtkinter.CTkButton(master=errorWindow, font=("Times New Roman", 16), text="OK", command=errorWindow.destroy)
    okBtn.place(relx=0.5, rely=0.5, anchor="center")
    errorWindow.mainloop()

def switchToPlaylistFrame():
    framePlaylist.tkraise()

def switchToHome():
    frameOnOpen.tkraise()

def switchToSongs():
    #playlistListbox.config(master=frameSongs) This is not possible
    #everytime we switch to song get all items in playlistListbox, and place them in another listbox
    selectPlaylistListbox.delete(0, "end")
    for i in range(playlistListbox.size()):
        selectPlaylistListbox.insert("end", playlistListbox.get(i))
    frameSongs.tkraise()

def switchToRecommended():
    frameRecommendations.tkraise()

#This function is the function that has the mp3 player inside!!!!
def openPlaylist():
    global songInMp3
    global run
    songInMp3 = False
    run = True
    def loadMySong(event):
        global songInMp3
        global run
        if songInMp3:
            run = False
        mySong = mySongListbox.get(mySongListbox.curselection()[0])
        mySongDest = myPlaylistDest + "\\" + mySong
        mySongSound = pygame.mixer.Sound(mySongDest)
        mySongLength = int(mySongSound.get_length())
        mySongLength_format = convertTime(mySongLength)
        myLengthLbl.configure(text = mySongLength_format)
        pygame.mixer.music.load(mySongDest)
        pygame.mixer.music.play()
        playOrPauseBtn.configure(text="⏸️", state="normal")
        skipBtn.configure(state="normal")
        prevBtn.configure(state="normal")
        songSlider.configure(to = mySongLength, state="normal")
        songSlider.set(0)
        myPosLbl.configure(text = "00:00")
        myPosLbl.after(1000, getMyTime)
        songInMp3 = True
            
    
    def playOrPause():
        if playOrPauseBtn.cget("text") == "▶":
            pygame.mixer.music.unpause()
            playOrPauseBtn.configure(text="⏸️")
        else:
            pygame.mixer.music.pause()
            playOrPauseBtn.configure(text="▶")
            
    def getMyTime():
        global run
        current_time = int(pygame.mixer.music.get_pos()/1000)
        current_time_format = convertTime(current_time)
        
        if (int(songSlider.get()) - int(current_time)) <= -1:
            #songSlider wasn't moved
            songSlider.set(int(current_time))
            myPosLbl.configure(text = convertTime(current_time))
        else:
            #songSlider has moved
            myPosLbl.configure(text = convertTime(int(songSlider.get())))
            #update the slider and Lbl after scroll
            if playOrPauseBtn.cget("text") == "⏸️":
                oneSecond = int(songSlider.get()) + 1
                songSlider.set(oneSecond)
        if run: 
            myPosLbl.after(1000, getMyTime)
        else:
            run = True

    def seek(event):
        mySong = mySongListbox.get(mySongListbox.curselection()[0])
        mySongDest = myPlaylistDest + "\\" + mySong
        songSlider_format = convertTime(int(songSlider.get()))
        pygame.mixer.music.load(mySongDest)
        pygame.mixer.music.play(loops=0, start=int(songSlider.get()))
        myPosLbl.configure(text = convertTime(int(songSlider.get())))
        if playOrPauseBtn.cget("text") == "▶":
            pygame.mixer.music.pause()

    def switchBackToSelectPlaylist():
        frameMp3Player.destroy()
        pygame.mixer.music.pause()
        switchToSongs()

    def skip():
        x=0
        nextSongPos = mySongListbox.curselection()[0]+1
        if nextSongPos >= mySongListbox.size():
            nextSongPos = 0
        mySongListbox.selection_clear(0, "end")
        mySongListbox.activate(nextSongPos)
        mySongListbox.selection_set(nextSongPos)
        loadMySong(x)

    def prev():
        x=0
        prevSongPos = mySongListbox.curselection()[0]-1
        if prevSongPos < 0:
            prevSongPos = mySongListbox.size()-1
        mySongListbox.selection_clear(0, "end")
        mySongListbox.activate(prevSongPos)
        mySongListbox.selection_set(prevSongPos)
        loadMySong(x)
        
    myPlaylist = selectPlaylistListbox.get(selectPlaylistListbox.curselection()[0])
    myPlaylistDest = (os.getcwd() + "\\" + myPlaylist)
    framePlaySongs.tkraise()
    frameMp3Player = customtkinter.CTkFrame(master=framePlaySongs, width = 330, height= 576, corner_radius = 60, fg_color="#BF177A")
    frameMp3Player.place(relx=0.5, rely=0.5, anchor ="center")
    backToPlaylistSelectBtn = customtkinter.CTkButton(master=framePlaySongs, text_color = "white", text="🠔", font=("Times New Roman", 24), corner_radius = 120, width=40, height=40, fg_color="transparent", hover_color = "#951024", border_width = 2, border_color = "#951024", command = switchBackToSelectPlaylist)
    backToPlaylistSelectBtn.place(anchor="nw", x=40, y=40)
    mySongListbox = tkinter.Listbox(master = frameMp3Player, font=("ds-digital", 16, "bold"), bg="black", fg="#B4E5AF", width = 20, height = 10)
    mySongListbox.bind("<<ListboxSelect>>", loadMySong)
    unfilteredFiles = os.listdir(myPlaylistDest)
    for i in range(len(unfilteredFiles)):
        if isAudio(unfilteredFiles[i]):
            mySongListbox.insert("end", unfilteredFiles[i])
    mySongListbox.place(anchor="center", relx=0.5, rely=0.5, y=-100)
    myPosLbl = customtkinter.CTkLabel(master = frameMp3Player, font=("ds-digital", 16), text_color="white", text="")
    myPosLbl.place(anchor="center", relx=0.5, rely=0.5, y=50, x=-130)
    myLengthLbl = customtkinter.CTkLabel(master = frameMp3Player, font= ("ds-digital", 16), text_color = "#FFF", text = "")
    myLengthLbl.place(anchor="center", relx=0.5, rely = 0.5, y=50, x=130)
    #This is my play/pause button
    playOrPauseBtn = customtkinter.CTkButton(master = frameMp3Player, font=(None, 20), fg_color="transparent", border_width=2, border_color="#0AA3BD", hover_color = "#0AA3BD", text = "▶", width = 50, height = 50, command=playOrPause, state="disabled")
    playOrPauseBtn.place(anchor="center", relx=0.5, rely = 0.5, y=150)

    #This is my skip button
    skipBtn = customtkinter.CTkButton(master=frameMp3Player, fg_color="transparent", border_width=2, font=(None, 20), border_color="#0AA3BD", hover_color = "#0AA3BD", text = "⏭️", width = 50, height = 50, command=skip, state="disabled")
    skipBtn.place(anchor="center", relx=0.5, rely=0.5, y=150, x = 55)

    #this is my previous button
    prevBtn = customtkinter.CTkButton(master=frameMp3Player, fg_color="transparent", border_width=2, font=(None, 20), border_color="#0AA3BD", hover_color = "#0AA3BD", text = "⏮️", width = 50, height = 50, command=prev, state="disabled")
    prevBtn.place(anchor="center", relx=0.5, rely=0.5, y=150, x = -55)

    #This is my slider
    songSlider = customtkinter.CTkSlider(master = frameMp3Player, from_=0, to=100, state="disabled", command=seek)
    songSlider.set(0)
    songSlider.place(anchor="center", relx=0.5, rely=0.5, y=50)

def removePlaylist():
    #Removes the folder
    selectedPlaylist = playlistListbox.get(playlistListbox.curselection()[0])
    shutil.rmtree(selectedPlaylist)

    #Removes from playlistListbox
    playlistListbox.delete(0,"end")
    allOfFiles = os.listdir()
    for i in range(len(allOfFiles)):
        if os.path.isdir(allOfFiles[i]):
            playlistListbox.insert("end", allOfFiles[i])

def editPlaylist():
    selectedPlaylist = playlistListbox.get(playlistListbox.curselection()[0])
    myPlaylistDir = os.getcwd() + "\\" + selectedPlaylist
    edit = customtkinter.CTk()
    edit.geometry("640x360")
    edit.title("Edit " + selectedPlaylist)
    edit.resizable(False,False)
    def addToPlaylist():
        mySong = tkinter.filedialog.askopenfilename(title="Choose a song", filetypes=[("Audio files", "*.mp3 *.wav *.pcm *.aiff *.aac *.ogg *.wma *.flac *.alac *.wma")])
        shutil.copy(mySong, myPlaylistDir)
        songListbox.delete(0, "end")
        unfilteredSongs = os.listdir(selectedPlaylist)
        for i in range(len(unfilteredSongs)):
            if isAudio(unfilteredSongs[i]):
                songListbox.insert("end", unfilteredSongs[i])
    def removeFromPlaylist():
        selectedSongIndex = songListbox.curselection()[0]
        selectedSong = songListbox.get(songListbox.curselection()[0])
        os.remove(myPlaylistDir + "\\" + selectedSong)
        songListbox.delete(0, "end")
        unfilteredSongs = os.listdir(selectedPlaylist)
        for i in range(len(unfilteredSongs)):
            if isAudio(unfilteredSongs[i]):
                songListbox.insert("end", unfilteredSongs[i])
        
    frameSong = customtkinter.CTkFrame(master=edit, bg_color="#000116", fg_color="#000116", height = 360, width = 320)
    frameSong.place(rely=0.5, relx=1, anchor="e")
    frameBtnOptions = customtkinter.CTkFrame(master=edit, bg_color="#000116", fg_color="#000116", height = 360, width = 320)
    frameBtnOptions.place(rely=0.5, anchor="w")
    addSongBtn = customtkinter.CTkButton(master=frameBtnOptions, width=180, height=90, corner_radius=10, border_width=2, border_color="#0AA3BD", text="+\nAdd Song", fg_color="transparent", hover_color = "#0AA3BD", font=("Times New Roman", 24), command=addToPlaylist)
    addSongBtn.place(relx=0.5, rely=0.5, y = -50, anchor="center")
    removeSongBtn = customtkinter.CTkButton(master=frameBtnOptions, width=180, height=90, corner_radius=10, border_width=2, border_color="#0AA3BD", text="🗑\nRemove Song", fg_color="transparent", hover_color = "#0AA3BD", font=("Times New Roman", 24), command=removeFromPlaylist)
    removeSongBtn.place(relx=0.5, rely=0.5, y = 50, anchor="center")
    songListbox = tkinter.Listbox(master=frameSong, width=20, height= 15, bg ="black", font=("ds-digital", 16, "bold"), fg="#B4E5AF")
    unfilteredSongs = os.listdir(selectedPlaylist)
    for i in range(len(unfilteredSongs)):
        if isAudio(unfilteredSongs[i]):
            songListbox.insert("end", unfilteredSongs[i])
    songListbox.place(relx=0.5, rely=0.5, anchor="center")
    edit.mainloop()
    
def createPlaylist():

    popup=customtkinter.CTk()
    popup.geometry("480x250")
    popup.title("Name Playlist")
    popup.resizable(False,False)
    
    def namePlaylist():
        playlistName = playlistNameEntry.get()
        myDirectory = os.getcwd()
        flag = True
        while flag:
            try:
                os.mkdir(myDirectory+"/"+playlistName)
                flag = False
                playlistListbox.insert("end", playlistName)
            except:
                errorMsg("You can't name a playlist that")
        popup.destroy()
        playlistName = None

    def chooseExistingPlaylist():
        popup.destroy()
        existingPlaylist = tkinter.filedialog.askdirectory()
        folderName = ""
        revExistingPlaylist = existingPlaylist[::-1]
        i = 0
        while revExistingPlaylist[i] != "/":
            folderName= revExistingPlaylist[i] + folderName
            i = i + 1
        try:
            shutil.copytree(existingPlaylist, folderName)
            playlistListbox.insert('end', folderName)
        except:
            errorMsg("The playlist already exists")

    
    #All of these widgets show up on a window after the add playlist button is clicked
    frameNamePlaylist = customtkinter.CTkFrame(master=popup, width=240, height=250, bg_color = "#000116", fg_color = "#000116")
    frameNamePlaylist.place(rely=0.5,anchor="w")
    frameChooseExistingPlaylist = customtkinter.CTkFrame(master=popup, width=240, height=250, bg_color = "#000116", fg_color = "#000116")
    frameChooseExistingPlaylist.place(relx=1,rely=0.5, anchor="e")
    orLbl = customtkinter.CTkLabel(master=popup, text="OR", font=("Times New Roman", 16), text_color="white", fg_color="#000116")
    orLbl.place(relx=0.5, rely=0.5, anchor="center")
    orLbl.tkraise()
    playlistNameEntry = customtkinter.CTkEntry(master=frameNamePlaylist, text_color= "white", placeholder_text= "Enter Playlist Name")
    playlistNameEntry.place(relx=0.5, rely=0.5, y=-16, anchor="center")
    createBtn = customtkinter.CTkButton(master=frameNamePlaylist, text_color="white", font=("Times New Roman", 16), text="Create", hover_color="#0AA3BD", fg_color="transparent", border_width=2, border_color="#0AA3BD", command=namePlaylist)
    createBtn.place(relx=0.5, rely=0.5,y = 16, anchor="center")
    choosePlaylistBtn = customtkinter.CTkButton(master=frameChooseExistingPlaylist, text_color="white", font=("Times New Roman", 16), hover_color="#0AA3BD", text="Choose Existing Playlist", fg_color="transparent", border_width=2, border_color="#0AA3BD", command=chooseExistingPlaylist)
    choosePlaylistBtn.place(relx=0.5, rely=0.5, anchor="center")
    popup.mainloop()
    

#Frames    
frameOnOpen = customtkinter.CTkFrame(master=win, width=720, height=576, corner_radius=20, bg_color="#000116", fg_color="#000116")
frameOnOpen.place(relx = 0.5, rely=0.5, anchor="center")
framePlaylist = customtkinter.CTkFrame(master=win, width=720, height=576, corner_radius=60, bg_color="#0AA3BD", fg_color="#000116")
framePlaylist.place(relx = 0.5, rely=0.5, anchor="center")
frameSongs = customtkinter.CTkFrame(master=win, width=720, height=576, corner_radius=60, bg_color="#BF177A", fg_color="#000116")
frameSongs.place(relx=0.5, rely=0.5, anchor="center")
frameRecommendations = customtkinter.CTkFrame(master=win, width=720, height=576, corner_radius=60, bg_color="#ff5e72", fg_color="#000116")
frameRecommendations.place(relx=0.5, rely=0.5, anchor="center")
framePlaySongs = customtkinter.CTkFrame(master=win, width=720, height=576, corner_radius=60, bg_color="#BF177A", fg_color="#000116")
framePlaySongs.place(relx=0.5, rely=0.5, anchor="center")

frameOnOpen.tkraise()
#All widgets that belong on the home frame go here
titleLbl = customtkinter.CTkLabel(master=frameOnOpen, text_color = "white", text="Somethin' Catchy 🐟", font=("Times New Roman", 36, "bold"))
titleLbl.place(relx = 0.5, y=40, anchor="n")
playListBtn = customtkinter.CTkButton(master=frameOnOpen, width=180, height=180, corner_radius=10, border_width=2, border_color="#0AA3BD", text="🎶\nView Playlists", fg_color="transparent", hover_color = "#0AA3BD", font=("Times New Roman", 24), command=switchToPlaylistFrame)
playListBtn.place(relx= 0.5, rely=0.5, x=95, anchor="center")
playBtn = customtkinter.CTkButton(master=frameOnOpen, width=180, height=180, corner_radius=10, border_width=2, border_color="#BF177A", text="📱\nPlay", fg_color="transparent", hover_color = "#BF177A", font=("Times New Roman", 24), command=switchToSongs)
playBtn.place(relx = 0.5, rely = 0.5, x=-95, anchor="center")
#recommendBtn = customtkinter.CTkButton(master=frameOnOpen, width=180, height=180, corner_radius=10, border_width=2, border_color="#ff5e72", text="👂\nRecommended\n(internet req.)", fg_color="transparent", hover_color = "#ff5e72", font=("Times New Roman", 24), command=switchToRecommended)
#recommendBtn.place(rely = 0.5, x=40, anchor="w")

#All widgets that belong on the Playlist frame go here
backToHomeBtnPl = customtkinter.CTkButton(master=framePlaylist, text_color = "white", text="🠔", font=("Times New Roman", 24), corner_radius = 120, width=40, height=40, fg_color="transparent", hover_color = "#951024", border_width = 2, border_color = "#951024", command=switchToHome)
backToHomeBtnPl.place(anchor="nw", x=40, y=40)
addPlayListBtn = customtkinter.CTkButton(master=framePlaylist, width=180, height=90, corner_radius=10, border_width=2, border_color="#0AA3BD", text="+\nAdd Playlist", fg_color="transparent", hover_color = "#0AA3BD", font=("Times New Roman", 24), command=createPlaylist)
addPlayListBtn.place(anchor="w", rely=0.5, x = 40, y=-95)
editPlayListBtn = customtkinter.CTkButton(master=framePlaylist, width=180, height=90, corner_radius=10, border_width=2, border_color="#0AA3BD", text="✏\nEdit Playlist", fg_color="transparent", hover_color = "#0AA3BD", font=("Times New Roman", 24), command=editPlaylist)
editPlayListBtn.place(anchor="w", rely=0.5, x = 40)
removePlayListBtn = customtkinter.CTkButton(master=framePlaylist, width=180, height=90, corner_radius=10, border_width=2, border_color="#0AA3BD", text="🗑\nDelete Playlist", fg_color="transparent", hover_color = "#0AA3BD", font=("Times New Roman", 24), command=removePlaylist)
removePlayListBtn.place(anchor="w", rely=0.5, x = 40, y = 95)
playlistListbox = tkinter.Listbox(master=framePlaylist, width =35, height = 15, bg ="black", font=("ds-digital", 16, "bold"), fg="#B4E5AF")
for i in range(len(allOfFiles)):
    if os.path.isdir(allOfFiles[i]):
        listOfPlaylist.append(allOfFiles[i])
for i in range(len(listOfPlaylist)):
    playlistListbox.insert(i+1, listOfPlaylist[i])
playlistListbox.place(relx=1, rely= 0.5, x= -40, anchor="e")

#All widgets that appear after clicking the play button on the home screen go here
selectPlaylistBtn = customtkinter.CTkButton(master=frameSongs, width=180, height=90, corner_radius=10, border_width=2, border_color="#BF177A", text="☞\nSelect Playlist", fg_color="transparent", hover_color = "#BF177A", font=("Times New Roman", 24), command=openPlaylist)
selectPlaylistBtn.place(relx=0.5, rely=1, y= -60, anchor="s")
sizeOfListbox = 20
selectPlaylistListbox = tkinter.Listbox(master=frameSongs, width = 30, height = 15, bg="black", font=("ds-digital", 16, "bold"), fg="#B4E5AF", justify="center")
selectPlaylistListbox.place(relx=0.5, rely=0.5, y = -40, anchor="center")

#All widgets that belong on the all song frame go here
backToHomeBtnS = customtkinter.CTkButton(master=frameSongs, text_color = "white", text="🠔", font=("Times New Roman", 24), corner_radius = 120, width=40, height=40, fg_color="transparent", hover_color = "#951024", border_width = 2, border_color = "#951024", command=switchToHome)
backToHomeBtnS.place(anchor="nw", x=40, y=40)

#All widgets that belong on the recommended frame go here
backToHomeBtnR = customtkinter.CTkButton(master=frameRecommendations, text_color = "white", text="🠔", font=("Times New Roman", 24), corner_radius = 120, width=40, height=40, fg_color="transparent", hover_color = "#951024", border_width = 2, border_color = "#951024", command=switchToHome)
backToHomeBtnR.place(anchor="nw", x=40, y=40)

win.mainloop()

