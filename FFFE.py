# Python 3
# Tkinter needed

"Parses Firefox 4+ databases. Press start, select path to Firefox profile\
(on a live system or exportet from the system under examination) and path where the output\
shall be written. Output files are TAB separated csv to import in Excel, Open Office etc."

from tkinter.constants import END

def get_places(sqlitepath):
    historypath = os.path.join(sqlitepath, "places.sqlite")
    places = {} #Dictionary to take the history
    connection = sqlite3.connect(historypath)
    cursor = connection.cursor()
    cursor.execute("select last_visit_date, id, url, title, rev_host, visit_count, hidden, typed, favicon_id, frecency, guid from moz_places")

    for data in cursor:
        lastvisitunixtime = data[0]
        lastvisitlocaltime = "None"
        lastvisitutctime ="None"

        if lastvisitunixtime:
            lastvisitunixtime = str(int(lastvisitunixtime/1000000))
            lastvisitlocaltime = time.strftime("%d.%m.%Y %H:%M:%S", time.localtime(int(lastvisitunixtime)))
            lastvisitutctime = time.strftime("%d.%m.%Y %H:%M:%S", time.gmtime(int(lastvisitunixtime)))

        id = data[1]
        url = data[2]
        title = data[3]
        if not title:
            title = "None"

        rev_host = data[4]
        if rev_host:
            host = rev_host[::-1]
            if host[0] == ".":
                host = host[1:]        
        else:
            rev_host = "None"
            host = "None"

        visit_count = data[5]
        hidden = data[6]
        typed = data[7]

        favicon_id = data[8]
        if not favicon_id:
            favicon_id = "None"

        frecency = data[9]
        guid = data[10]

        places[id] = url, title, rev_host, host, lastvisitlocaltime, lastvisitutctime, visit_count, hidden, typed, favicon_id, frecency, guid

    connection.close()
    return(places)

def get_inputhistory(sqlitepath, places):
    historypath = os.path.join(sqlitepath, "places.sqlite")
    inputhistory = [] # List to take the results. Not a dict, because the same ID exists more than once
    
    connection = sqlite3.connect(historypath)
    cursor = connection.cursor()
    cursor.execute("select place_id, input, use_count from moz_inputhistory")
    
    for data in cursor:
        place_id = data[0]
        input = data[1]
        use_count = data[2]

        connected_url = places[place_id][0] # Take the url from the dict "history" with the coresponding place_id and put it in dict inputhistory

        inputhistory.append(place_id)
        inputhistory.append(input)
        inputhistory.append(use_count)
        inputhistory.append(connected_url)

    connection.close()
    return(inputhistory)

def get_bookmarks(sqlitepath, places):
    historypath = os.path.join(sqlitepath, "places.sqlite")
    bookmarks = {} #Dict to take the bookmarks

    connection = sqlite3.connect(historypath)
    cursor = connection.cursor()
    cursor.execute("select id, type, fk, parent, position, title, keyword_id, folder_type, dateAdded, lastModified, guid from moz_bookmarks")
 
    for data in cursor:
        id = data[0]
        type = data[1]
        if type == 1:
            type = "Normal Bookmark"
        if type == 2:
            type = "Tag (Folder)"
        if type == 3:
            type = "Separator"

        foreignkey = data[2]  
        if not foreignkey:    
            fk = "None"
        else:
            fk = places[foreignkey][0]

        parent = data [3]
        position = data[4]
        title = data [5]
        keyword_id = data[6]
        folder_type = data[7]

        dateAddedUnix = data[8]
        dateAddedUnix = str(int(dateAddedUnix/1000000))
        dateAddedlocaltime = time.strftime("%d.%m.%Y %H:%M:%S", time.localtime(int(dateAddedUnix)))
        dateAddedUTC = time.strftime("%d.%m.%Y %H:%M:%S", time.gmtime(int(dateAddedUnix)))

        lastModifiedUnix = data[9]
        lastModifiedUnix = str(int(lastModifiedUnix/1000000))
        lastModifiedlocaltime = time.strftime("%d.%m.%Y %H:%M:%S", time.localtime(int(lastModifiedUnix)))
        lastModifiedUTC = time.strftime("%d.%m.%Y %H:%M:%S", time.gmtime(int(lastModifiedUnix)))

        guid = data [10]
        bookmarks[id] = type, fk, parent, position, title, keyword_id, dateAddedUTC, dateAddedlocaltime, lastModifiedUTC, lastModifiedlocaltime, guid

    connection.close()
    return(bookmarks)

def get_historyvisits(sqlitepath, places):
    historypath = os.path.join(sqlitepath, "places.sqlite")
    historyvisits = {} #Dict to take historyvisits

    connection = sqlite3.connect(historypath)
    cursor = connection.cursor()
    cursor.execute("select id, from_visit, place_id, visit_date, visit_type, session from moz_historyvisits")

    for data in cursor:

        id = data[0]
        from_visit = data[1]
        place_id = data[2]
        visit_date = data [3]
        visit_type = data[4]
        session = data [5]

        visit_date = str(int(visit_date/1000000))
        visit_datelocaltime = time.strftime("%d.%m.%Y %H:%M:%S", time.localtime(int(visit_date)))
        visit_dateUTC = time.strftime("%d.%m.%Y %H:%M:%S", time.gmtime(int(visit_date)))

        place_id_string = places[place_id][0]
        historyvisits[id] = from_visit, place_id_string, visit_datelocaltime, visit_dateUTC, visit_type, session

    connection.close()
    return(historyvisits)

def get_cookies(sqlitepath):
    cookiespath = os.path.join(sqlitepath, "cookies.sqlite")
    cookies = {} #Dict to take cookies

    connection = sqlite3.connect(cookiespath)
    cursor = connection.cursor()
    cursor.execute("select id, name, value, host, path, expiry, lastAccessed, isSecure, isHttpOnly, baseDomain, creationTime from moz_cookies")

    for data in cursor:
        id = data[0]
        name = data[1]
        value = data[2]
        host = data [3]
        path = data[4]
        expiry = data [5]
        lastAccessed = data [6]
        isSecure = data [7]
        isHttpOnly = data [8]
        baseDomain = data [9]
        creationTime = data [10]

        lastAccessed = str(int(lastAccessed/1000000))
        lastAccessedlocaltime = time.strftime("%d.%m.%Y %H:%M:%S", time.localtime(int(lastAccessed)))
        lastAccessedUTC = time.strftime("%d.%m.%Y %H:%M:%S", time.gmtime(int(lastAccessed)))

        creationTime = str(int(creationTime/1000000))
        creationTimelocaltime = time.strftime("%d.%m.%Y %H:%M:%S", time.localtime(int(creationTime)))
        creationTimeUTC = time.strftime("%d.%m.%Y %H:%M:%S", time.gmtime(int(creationTime)))

        cookies[id] = name, value, host, path, expiry, lastAccessedlocaltime, lastAccessedUTC, isSecure, isHttpOnly, baseDomain, creationTimelocaltime, creationTimeUTC

    connection.close()
    return(cookies)

def get_signons(sqlitepath):
    signonspath = os.path.join(sqlitepath, "signons.sqlite")
    signonslogin = {} #Dict for accepted logins

    connection = sqlite3.connect(signonspath)
    cursor = connection.cursor()
    cursor.execute("select id, hostname, httpRealm, formSubmitURL, usernameField, passwordField, encryptedUsername, encryptedPassword, guid, encType, timeCreated,timeLastUsed, timePasswordChanged, timesUsed from moz_logins")

    for data in cursor:
        id = data[0]
        hostname = data[1]
        httpRealm = data[2]
        formSubmitURL = data [3]
        usernameField = data[4]
        passwordField = data [5]
        encryptedUsername = data [6]
        encryptedPassword = data [7]
        guid = data [8]
        encType = data [9]
        timeCreated = data [10]
        timeLastUsed = data [11]
        timePasswordChanged = data[12]
        timesUsed = data [13]
        
        timeCreated = str(int(timeCreated/1000))
        timeCreatedlocaltime = time.strftime("%d.%m.%Y %H:%M:%S", time.localtime(int(timeCreated)))
        timeCreatedUTC = time.strftime("%d.%m.%Y %H:%M:%S", time.gmtime(int(timeCreated)))

        timeLastUsed = str(int(timeLastUsed/1000))
        timeLastUsedlocaltime = time.strftime("%d.%m.%Y %H:%M:%S", time.localtime(int(timeLastUsed)))
        timeLastUsedUTC = time.strftime("%d.%m.%Y %H:%M:%S", time.gmtime(int(timeLastUsed)))

        timePasswordChanged = str(int(timePasswordChanged/1000))
        timePasswordChangedlocaltime = time.strftime("%d.%m.%Y %H:%M:%S", time.localtime(int(timePasswordChanged)))
        timePasswordChangedUTC = time.strftime("%d.%m.%Y %H:%M:%S", time.gmtime(int(timePasswordChanged)))

        signonslogin[id] = hostname, httpRealm, formSubmitURL, usernameField, passwordField, encryptedUsername, encryptedPassword, guid, encType, timeCreatedlocaltime,timeCreatedUTC, timeLastUsedlocaltime, timeLastUsedUTC, timePasswordChangedlocaltime, timePasswordChangedUTC, timesUsed

    connection.close()
    return(signonslogin)

def get_disabledHosts(sqlitepath):
    signonspath = os.path.join(sqlitepath, "signons.sqlite")
    signonsdisabled = {} #Dict for failed logins

    connection = sqlite3.connect(signonspath)
    cursor = connection.cursor()
    cursor.execute("select id, hostname from moz_disabledHosts")
 
    for data in cursor:
        id = data[0]
        hostname = data[1]
        signonsdisabled[id] = hostname

    connection.close()
    return(signonsdisabled)

def get_formhistory(sqlitepath):
    formhistorypath = os.path.join(sqlitepath, "formhistory.sqlite")
    formhistory = {} #Dict for formhistory

    connection = sqlite3.connect(formhistorypath)
    cursor = connection.cursor()

    cursor.execute("select id, fieldname, value, timesUsed, firstUsed, lastUsed, guid from moz_formhistory")

    for data in cursor:
        id = data[0]
        fieldname = data[1]
        value = data[2]
        timesUsed = data [3]
        firstUsed = data[4]
        lastUsed = data [5]
        guid = data [6]

        firstUsed = str(int(firstUsed/1000000))
        firstUsedlocaltime = time.strftime("%d.%m.%Y %H:%M:%S", time.localtime(int(firstUsed)))
        firstUsedUTC = time.strftime("%d.%m.%Y %H:%M:%S", time.gmtime(int(firstUsed)))

        lastUsed = str(int(lastUsed/1000000))
        lastUsedlocaltime = time.strftime("%d.%m.%Y %H:%M:%S", time.localtime(int(lastUsed)))
        lastUsedUTC = time.strftime("%d.%m.%Y %H:%M:%S", time.gmtime(int(lastUsed)))

        formhistory[id] = fieldname, value, timesUsed, firstUsedlocaltime, firstUsedUTC, lastUsedlocaltime, lastUsedUTC, guid

    connection.close()
    return(formhistory)

def get_downloads(sqlitepath):
    downloadspath = os.path.join(sqlitepath, "downloads.sqlite")
    downloads = {} #Downloads dict

    connection = sqlite3.connect(downloadspath)
    cursor = connection.cursor()
    cursor.execute("select id, name, source, target, tempPath, startTime, endTime, state, referrer, entityID, currBytes, maxBytes, mimeType, preferredApplication, preferredAction, autoResume from moz_downloads")

    for data in cursor:
        id = data[0]
        name = data[1]
        source = data[2]
        target = data [3]
        tempPath = data[4]
        startTime = data [5]
        endTime = data [6]
        state = data [7]
        referrer = data [8]
        entityID = data [9]
        currBytes = data [10]
        maxBytes = data [11]
        mimeType = data[12]
        preferredApplication = data [13]
        preferredAction = data [14]
        autoResume = data [15]

        startTime = str(int(startTime/1000000))
        startTimelocaltime = time.strftime("%d.%m.%Y %H:%M:%S", time.localtime(int(startTime)))
        startTimeUTC = time.strftime("%d.%m.%Y %H:%M:%S", time.gmtime(int(startTime)))

        endTime = str(int(endTime/1000000))
        endTimelocaltime = time.strftime("%d.%m.%Y %H:%M:%S", time.localtime(int(endTime)))
        endTimeUTC = time.strftime("%d.%m.%Y %H:%M:%S", time.gmtime(int(endTime)))

        downloads[id] = name, source, target, tempPath, startTimelocaltime, startTimeUTC, endTimelocaltime, endTimeUTC, state, referrer, entityID, currBytes, maxBytes, mimeType, preferredApplication, preferredAction, autoResume

    connection.close()
    return(downloads)

def writefiles(outputpath, places, historyvisits,inputhistory, bookmarks, cookies, signonslogin, signonsdisabled, formhistory, downloads):

    write_to_infoscreen("\nWriting Output...\n")
    write_to_infoscreen("Writing places file `places.csv'")
    historyvisitsfile = (os.path.join(outputpath,"places.csv"))
    writer = csv.writer(open(historyvisitsfile, "w", encoding = "utf-8"),"excel-tab") #TODO: newline="" for Windows?
    writer.writerow(["ID", "URL", "Title", "Rev Host", "Host", "Last Visit Locale", "LastVisit UTC", "Visit Count", "Hidden", "Typed", "Favicon ID", "Frecency", "GUID"])
    for id in places:
        writer.writerow([str(id), places[id][0], places[id][1], places[id][2],places[id][3],places[id][4], places[id][5], places[id][6], places[id][7], places[id][8],places[id][9],places[id][10], places[id][11]])

    write_to_infoscreen("Writing history file `historyvisits.csv`")
    historyvisitsfile = (os.path.join(outputpath,"historyvisits.csv"))
    writer = csv.writer(open(historyvisitsfile, "w", encoding="utf-8"),"excel-tab") #TODO: newline="" for Windows?
    writer.writerow(["ID", "From Visit", "Place ID", "Visit Date Local", "Visit Date UTC", "Visit Type", "Session"])
    for id in historyvisits:
        templist = [str(id), historyvisits[id][0], historyvisits[id][1], historyvisits[id][2],historyvisits[id][3],historyvisits[id][4], historyvisits[id][5]]
        writer.writerow(templist)

    write_to_infoscreen("Writing history file `inputhistory.csv")
    inputhistoryfile = (os.path.join(outputpath,"inputhistory.csv"))
    writer = csv.writer(open(inputhistoryfile, "w", encoding="utf-8"),"excel-tab") #TODO: newline="" for Windows?
    writer.writerow(["Place ID", "Input", "Use Count", "Connected URL"])
    for i in range(0,len(inputhistory),4):
        templist = [inputhistory[i], inputhistory[i+1], inputhistory[i+2], inputhistory[i+3]]
        writer.writerow(templist)

    write_to_infoscreen("Writing cookies file `bookmarks.csv'")
    bookmarksfile = (os.path.join(outputpath, "bookmarks.csv"))
    writer = csv.writer(open(bookmarksfile, "w", encoding = "utf-8"),"excel-tab") #TODO: newline="" for Windows?
    writer.writerow(["ID", "Type", "FK", "Parent", "Position", "Title", "Keyword ID", "Date Added UTC", "Date Added Local", "Last Modified UTC", "Last Modified Local", "GUID"])
    for id in bookmarks:
        writer.writerow([str(id), bookmarks[id][0], bookmarks[id][1], bookmarks[id][2],bookmarks[id][3],bookmarks[id][4], bookmarks[id][5], bookmarks[id][6], bookmarks[id][7], bookmarks[id][8],bookmarks[id][9],bookmarks[id][10]])

    write_to_infoscreen("Writing cookies file `cookies.csv'")
    cookiesfile = (os.path.join(outputpath,"cookies.csv"))
    writer = csv.writer(open(cookiesfile, "w", encoding = "utf-8"),"excel-tab") #TODO: newline="" for Windows?
    writer.writerow(["ID", "Name", "Value", "Host", "Path", "Expiry", "Last Accessed Local", "Last Accessed UTC", "Is Secure", "Is HTTP Only", "Base Domain", "Creation Time Local", "Creation Time UTC"])
    for id in cookies:
        writer.writerow([str(id), cookies[id][0], cookies[id][1], cookies[id][2],cookies[id][3],cookies[id][4], cookies[id][5], cookies[id][6], cookies[id][7], cookies[id][8],cookies[id][9],cookies[id][10],cookies[id][11]])

    write_to_infoscreen("Writing saved logins file `signons.csv'")
    signonsfile = (os.path.join(outputpath,"signons.csv"))
    writer = csv.writer(open(signonsfile, "w", encoding = "utf-8"),"excel-tab") #TODO: newline="" for Windows?
    writer.writerow(["ID", "Hostname", "Http Realm", "Form Submit URL", "Username Field", "Password Field", "Encrypted Username", "Encrypted Password", "GUID", "Enc Type", "Time Created Local","Time Created UTC", "Time Last Used Local", "Time Last Used UTC", "Time Password Changed Local", "Time Password Changed UTC", "Times Used"])
    for id in signonslogin:
        writer.writerow([str(id), signonslogin[id][0], signonslogin[id][1], signonslogin[id][2],signonslogin[id][3],signonslogin[id][4], signonslogin[id][5], signonslogin[id][6], signonslogin[id][7], signonslogin[id][8],signonslogin[id][9],signonslogin[id][10],signonslogin[id][11],signonslogin[id][12],signonslogin[id][13],signonslogin[id][14],signonslogin[id][15]])

    write_to_infoscreen("Writing disabled logins file `signons_disabled.csv'")
    signonsdisabledfile = (os.path.join(outputpath,"signons_disabled.csv"))
    writer = csv.writer(open(signonsdisabledfile, "w", encoding = "utf-8"),"excel-tab") #TODO: newline="" for Windows?
    writer.writerow(["ID", "Hostname"])
    for id in signonsdisabled:
        writer.writerow([str(id), signonsdisabled[id][0]])

    write_to_infoscreen("Writing formhistory file `formhistory.csv'")
    formhistoryfile = (os.path.join(outputpath,"formhistory.csv"))
    writer = csv.writer(open(formhistoryfile, "w", encoding = "utf-8"),"excel-tab") #TODO: newline="" for Windows?
    writer.writerow(["ID", "Fieldname", "Value", "Times Used", "First Used Local", "First Used UTC", "Last Used Local", "Last Used UTC", "GUID"])
    for id in formhistory:
        writer.writerow([str(id), formhistory[id][0], formhistory[id][1], formhistory[id][2],formhistory[id][3],formhistory[id][4], formhistory[id][5], formhistory[id][6], formhistory[id][7]])

    write_to_infoscreen("Writing downloads file `downloads.csv'")
    downloadsfile = (os.path.join(outputpath,"downloads.csv"))
    writer = csv.writer(open(downloadsfile, "w", encoding = "utf-8"),"excel-tab") #TODO: newline="" for Windows?
    writer.writerow(["ID", "Name", "Source", "Target", "Temp Path", "Start Time Local", "Start Time UTC", "End Time Local", "End Time UTC", "State", "referrer", "Entity ID", "Bytes Downloaded", "Total Filesize", "Mime Type", "Preferred Application", "Preferred Action", "Auto Resume"])
    for id in downloads:
        writer.writerow([str(id), downloads[id][0], downloads[id][1], downloads[id][2],downloads[id][3],downloads[id][4], downloads[id][5], downloads[id][6], downloads[id][7], downloads[id][8],downloads[id][9],downloads[id][10],downloads[id][11],downloads[id][12],downloads[id][13],downloads[id][14],downloads[id][15],downloads[id][16]])

    write_to_infoscreen("\nDone.\n\nResulting files are tab separated CSV (utf-8 encoded).\n")
    
    return()

def checkpaths(sqlitepath, outputpath): 
    write_to_infoscreen("\nChecking Files...\n")

    if sqlitepath == "":
        write_to_infoscreen("\nPath to FF profile not correct! Press Start, Exit or Info\n")
        window_main.mainloop()
    if outputpath == "":
        write_to_infoscreen("\nPath for output not correct! Press Start, Exit or Info\n")
        window_main.mainloop()
    try:
        #checkfile = open(sqlitepath + "\places.sqlite", "r")
        checkfile = open(os.path.join(sqlitepath, "places.sqlite"), "r") #TODO: Die anderen Pfadüberprüfungen auch so machen
        #print(checkfile)
        checkfile.close()
        write_to_infoscreen("places.sqlite found")
    except:
        write_to_infoscreen("places.sqlite not found! Press Start, Exit or Info.\n")
        window_main.mainloop()

    try:
        checkfile = open(os.path.join(sqlitepath, "cookies.sqlite"), "r")
        checkfile.close()
        write_to_infoscreen("cookies.sqlite found")
    except:
        write_to_infoscreen("cookies.sqlite not found! Aborting...\n")
        window_main.mainloop()

    try:
        checkfile = open(os.path.join(sqlitepath,"downloads.sqlite"), "r")
        checkfile.close()
        write_to_infoscreen("downloads.sqlite found")
    except:
        write_to_infoscreen("downloads.sqlite not found! Aborting...\n")
        window_main.mainloop()
    try:
        checkfile = open(os.path.join(sqlitepath, "formhistory.sqlite"), "r")
        checkfile.close()
        write_to_infoscreen("formhistory.sqlite found")
    except:
        write_to_infoscreen("formhistory.sqlite not found! Aborting...\n")
        window_main.mainloop()

    try:
        checkfile = open(os.path.join(sqlitepath, "signons.sqlite"), "r")
        checkfile.close()
        write_to_infoscreen("signons.sqlite found\n")
    except:
        write_to_infoscreen("signons.sqlite not found! Aborting...\n")
        window_main.mainloop()

    try:
        checkfile = open(os.path.join(outputpath, "places.csv"), "w")
        checkfile.write("Testing")
        checkfile.close
        write_to_infoscreen("Outputpath found. Rights to write files granted")
    except:
        write_to_infoscreen("Outputpath not found or no write rights! Aborting...\n")
        window_main.mainloop()

    return()

def get_dirs():
    write_to_infoscreen("Enter path to Firefox profile")
    sqlitepath = filedialog.askdirectory(title="Choose Firefox profile directory")
    write_to_infoscreen("\nEnter path for the output")
    outputpath = filedialog.askdirectory(title = "Choose output directory")
    write_to_infoscreen("\nFF profile folder: " + sqlitepath)
    write_to_infoscreen("\nOutput folder: " + outputpath)
    return(sqlitepath, outputpath)

def exit_programm():
    window_exit = tkinter.messagebox.askokcancel("Exit?", "Exit FFFE ?")
    if window_exit == 1:
        sys.exit()
    else:
        return()

def show_info():
    window_info = tkinter.messagebox.showinfo("Info","Firefox 4+ Examiner (FFFE)\
                                        \n\nFFFE parses Firefox 4 (and later) databases and writes CSV files with the results.\
                                        \n\nUsage:\
                                        \n\n1) Press Button 'Start'\
                                        \n2) Select path to Firefox Profile\
                                        \n3) Select path where the output files shall be written\
                                        \n\nFFFE parses (and therefore needs) the following databases:\
                                        \n\nplaces.sqlite\
                                        \ncookies.sqlite\
                                        \ndownloads.sqlite\
                                        \nformhistory.sqlite\
                                        \nsignons.sqlite")
    return()

def write_to_infoscreen(infotext):
    infotext = infotext + "\n"
    text_info.insert("end", infotext)
    return()

def run_program():
    text_info.delete("1.0", END)
    sqlitepath, outputpath = get_dirs()
    checkpaths(sqlitepath, outputpath)
    write_to_infoscreen("\nWorking...")
    places = get_places(sqlitepath)
    inputhistory = get_inputhistory(sqlitepath, places)
    bookmarks = get_bookmarks(sqlitepath,places)
    historyvisits = get_historyvisits(sqlitepath, places)
    cookies = get_cookies(sqlitepath)
    signonslogin = get_signons(sqlitepath)
    signonsdisabled = get_disabledHosts(sqlitepath)
    formhistory = get_formhistory(sqlitepath)
    downloads = get_downloads(sqlitepath)
    write_to_infoscreen("\nWork done.")

    writefiles(outputpath, places, historyvisits,inputhistory, bookmarks, cookies, signonslogin, signonsdisabled, formhistory, downloads)
    #TODO: And Now? What to do after writing files?
    return()

import sqlite3
import time
import os
import csv
import sys
from tkinter import filedialog
import tkinter
import tkinter.scrolledtext
import tkinter.messagebox

global sqlitepath
global outputpath
global places#, inputhistory, bookmarks,historyvisits, cookies, signonslogin, signonsdisabled, formhistory, downloads
sqlitepath = "Not Entered Yet"
outputpath = "Not Entered Yet"

# GUI
window_main = tkinter.Tk()
window_main.title("Firefox 4+ Examiner")
window_main.geometry("700x450")
window_main.minsize(400, 225)

text_info = tkinter.scrolledtext.ScrolledText(window_main, width=80, height=10)
text_info["borderwidth"] = 5
text_info["relief"] = "ridge"
text_info["bg"] = "#EDEDED"
text_info["fg"] = "#000000"
text_info.pack(expand = 1, fill = "both")


frame_buttons = tkinter.Frame(window_main, width = 80, height = 20)#, relief="sunken", bd=1)
frame_buttons.pack(side="right", anchor = "s", expand=1, fill="x", padx=5, pady=5)

button_exit = tkinter.Button(frame_buttons, text = "Exit", command = exit_programm)
button_exit.pack(side="right", ipadx = 20)

button_info = tkinter.Button(frame_buttons, text = "Info", command = show_info)
button_info.pack(side="right", padx = 10, ipadx = 20)

button_start = tkinter.Button(frame_buttons, text = "Start", command = run_program)
button_start.pack(side="right", ipadx = 20)

write_to_infoscreen("###################################################################")
write_to_infoscreen("#                  Firefox 4+ Examiner Version 1.0                #" )
write_to_infoscreen("#  https://github.com/HexBugsAndRocknRoll/Firefox_4_Plus_Examiner #")
write_to_infoscreen("###################################################################\n")
write_to_infoscreen("Press Start to enter FF profile folder and output folder." )
write_to_infoscreen("\nProfile folder locations:\n")
write_to_infoscreen("Windows 2000, XP:")
write_to_infoscreen("C:\\Documents and Settings\\USERNAME\\Application Data\\Mozilla\\Firefox\\Profiles\\<profile folder>")
write_to_infoscreen("\nWindows Vista, 7:")
write_to_infoscreen("C:\\Users\\USERNAME\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\<profile folder>")
write_to_infoscreen("\nLinux:")
write_to_infoscreen("~/.mozilla/firefox/<profile folder>")
write_to_infoscreen("\nMac OS X:")
write_to_infoscreen("~/Library/Mozilla/Firefox/Profiles/<profile folder>\n or \n\
~/Library/Application Support/Firefox/Profiles/<profile folder>")


# Main Loop
window_main.mainloop()

checkpaths(sqlitepath, outputpath)
sys.exit()

places = get_places(sqlitepath)
inputhistory = get_inputhistory(sqlitepath)
bookmarks = get_bookmarks(sqlitepath)
historyvisits = get_historyvisits(sqlitepath)
cookies = get_cookies(sqlitepath)
signonslogin = get_signons(sqlitepath)
signonsdisabled = get_disabledHosts(sqlitepath)
formhistory = get_formhistory(sqlitepath)
downloads = get_downloads(sqlitepath)
writefiles()


#TODO: Parse Bookmarks Backupfolder, json files, http://jsonformatter.curiousconcept.com/
#TODO: crack passwords, https://github.com/pradeep1288/ffpasscracker
#TODO: Extensions.ini
#TODO: Stay Frosty!