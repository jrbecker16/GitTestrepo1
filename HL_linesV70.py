
# Status as of 4/7/20    -- V70 - added Mimi's 11 Action Chains with colors - colors consistent with the
#                           colormap in hamletdisplayV110.py
# Status as of 3/9/2020   -- V60--THIS VERSION FROZEN.  DO NOT WORK ON OR CHANGE IN ANYWAY.

#this is a line to change this file.  To test git adn github and PyCharm
#delete after it all works

# The program seems to work completely.  It can:
#   1. Build the interface in tkinter
#   2. Read in the eventfile and fill the two list boxes with scrollable
#      selectable lists to indicate the event that starts the line and the event that
#      ends the line.
#   3. Create a listbox of Action Chains from an internal list - NOTE: this eventually
#      needs to be changed to build the AClist from an external file
#   4. Open the versionfile and get the last saved HamletLinesV1xx file and read in the
#      lines into the Current Line Box.   At that point it also creates the incremented
#      HamletLinesV1xx file for eventual output and puts its name the Output File text box
#      and puts the just opened file name in the Input File text box
#   5. Allows you to build a line by selecting a start event, end event and an Action Chain
#      Then you click on the Create Line button box and the new line will be added to the
#      Current Lines listbox and written to listoflines[][] and parts to displayline[][].
#   6. You can also delete a line by selecting the line in the Current Lines listbox and
#      clicking on the DeleteLine button box.  This will remove the line data from both
#      listoflines[][] and displayline[][] and update the Current Lines listbox
#   7. If necessary you can edit the output file name in the Output File textbox.
#   8. When you click on the Write Lines to File button box,  the current listoflines[][] is
#      written to the file named in the Output File text box and versionfile is updated with that
#      file name
#
# Some cautions:
#   1. Only click on Read In File and the Write Lines to File button boxs once in each session
#      of program operation.  If you click either more than once, you will get duplicate lines
#      in the listofline[][] and displaylines[][].   This could be solved by somehow clearing
#      the CurrentLines listbox and listoflines[][] ect.    OR by checking to make sure that any
#      lines already in Current Lines box and listoflines[][] are not reloaded.   I.E. you only
#      incremental lines.   Add later.
#   2. So now you have to shutdown and restart the app after you click on Write Lines to File to
#      make it work correctly.
#   3. This still has the problem with the 2nd and third listbox is selected tkinter runs the
#      previous selection and throws and error.   Doesn't seem to cause any harm.  Need to
#      create a simple example and submit to GitHob  or Stack.
#
#
#Ideas:
#   1. Perhaps the linefile and eventually listoflines[][] and then HamletLinesV1xx should only
#      contain the id number of the start and end events and then when VTK is run, the coordinates
#      of the start and end will be read from the eventfile. This would be useful when we start to
#      drag and drop the events and want the lines to follow.  Just have to update eventfile and
#      not redo the listoflines[][] etc.
#---------------------------------------------------------------------

import csv
from tkinter import *
from tkinter import ttk

#declares the root and adds title
root = Tk()         
root.title("Action Chain Layout") 

# this program operates off of two csv file:  eventfile and and versionfile. Should not
# touch eventfile. There is actually a third list of lists for the ActonChain identification but
#right now that is handled in the program - see ACList below

eventfile = "C:/Users/JRBEC/VTK_Programs/Hamlet_V117.csv"
versionfile = "C:/Users/JRBEC/VTK_Programs/Hamlet_linefile_versions.csv"



#eventfile = a list of lists. Each inner list contains
#the elements of an event in an action chain - the elements are listed below
#this file is used to create the events in VTK

    # 0 = event id - kept unique
    # 1 = event full description
    # 2 = event short description - Label
    # 3 = event short description - label 2nd half
    # 4 = event x coord
    # 5 = event y coord
    # 6 = event z coord
    # 7 = event type (to be used to select icon)
    # 8 = Actor 1
    # 9 = Actor 2
    # 10 = Actor 3
    # 11 = label displacement in x axis
    # 12 = Label displacement in y axis
    # 13 = label displacement in z axis
    # 14 = transparency of icon
    
# linefile = A list of lists.  Each inner list contains the
#the elements of a line that connects two events.  These lines and events
#create action chains - elements of each line are below.  Eventually this list get
#read into listoflines[][] which is eventually written to HamletLinesV1xx and is use
#in the VTK program to draw the line.

    # 0 =  line id  - needs to be unique
    # 1 = start event id from eventlist  (note: not eventfile index)
    # 2 = start event x coord (index 3 of eventfile)
    # 3 = start event y coord (index 4 of eventfile)
    # 4 = start event z coord (index 5 of eventfile)
    # 5 = end event id from eventlistb (note:  not event file index)
    # 6 = end event x coord
    # 7 = enc event y coord
    # 8 = end event z coord
    # 9 = Action chain list number (note:  not index)
    # 10 = Action chain label - text
    # 11 = Action chain color - text
    
    


#creates the lists variables outside of the function so they
#can be used again.   Is this a global?
#event is the list of the item[1] in the file
#eventlist is just the whole file arranged as a set of
#lists within lists.  Each inner list = data on one event
#ACnames[] is the name of each action chain
#ACList[] is list of lists of action chain, color and AC id number
#added eventb and eventlistb for the End list to decouple

event = []              #is list of the event descriptions for Start Event listbox.
                        # this is eventfile[2]
                        
eventlist = []          #is list of lists of all Start events with event elements in
                        # the inner list.  It is the CSV file eventfile read into eventlist
                        
eventb = []             #is list of event descriptions for End event listbox.
                        # this is eventfile[2]
                        
eventlistb = []         #is list of lists of all End events with event elements in
                        # the inner list. It is the CSV file eventfile read into eventlistb
                        
linelist = []           #is list of line elements.  One for each line

ACnames = []            #is list of Action Chain names for AC listbox

AClist = []             #is list of list of all Action Chains with AC description elements in
                        # the inner lists
                        
listoflines = []        #is list of list all lines.  Initally it is built from the linefile.
                        #linelist[] are added to it and can be deleted from it.  Then it writes
                        #everything back to the linefile(cvs)

displayline = []        #is list of of "line id"+"Start Event"+End Event" concanatted together
                        #and displayed in the Current Lines list box. User can choose a entry
                        #this list to delete. NOTE:  THIS LIST AND LISTOFLINES HAVE TO STAY
                        #SYNCRONIZED

fileversions = []       # the list that hold the names (with version numbers) of the various
                        #linefiles

namelist = []


#create a list of lists of action chains along with their colors and AC id number.  These can
#be added to if necessary. This eventually needs to be changed to read in a csv file
#just like the other lists.

AClist = [["Hamlet", "forestgreen", 1], ["Ghost", "purple", 2], ["King", "red", 3],
          ["Queen", "lsalmon", 4], ["Polonius", "chocolate", 5], ["Laertes", "darkorange", 6],
          ["Ophelia", "yellowgreen", 7], ["Horatio", "blue", 8], ["Fortinbras", "brown", 9],
          ["Ros/Gilder", "deeppink", 10], ["Marcell/Bern", "dodgerblue", 11]]

#reads in the first item of each sublist in AClist into ACNames[]
#ACNames[] is used to fill the AC listbox
i=0
while i < len(AClist):
    ACnames.append(AClist[i][0])
    i += 1


#function with loop to read in eventfile.csv
#reads the whole file into two lists eventlist[] and eventlistb[]
#also reads the second item (index=1) of each event into event[] and
#eventb[].  These lists are used as input to the Start and End listboxes
#??the function is called by the line below it.  Why do
#it as a function, with scope as opposed to straight line
#code???

def read_event(event, eventlist, eventb, eventlistb):
    with open(eventfile, newline= "")as file:
        reader = csv.reader(file)
        for row in reader:
            event.append(row[1])
            eventb.append(row[1])
            eventlist.append(row)
            eventlistb.append(row)
        return event
        return eventlist
        return eventb
        return eventlistb

read_event(event, eventlist, eventb, eventlistb)


#-------------------------------
# CREATE ALL THE ACTIONS THAT HAPPEN WHEN SELECTIONS ARE MADE



#versionfile = Hamlet_linefile_version.csv and contains, in csv format, the list of the latest
#HLV1xx file, i.e. HamletLinesV101.csv etc.   Each HamletLinesV1xx
#contains all the elements of a line that VTK will eventually use.
#The read_line function opens versionfile and reads it into fileversions[][].  It then finds
#the length of fileversions[][] and then reads in the last entry of fileversions[][] into
#linefile[].  Then the first (index 0) and only entry in linefile[] is assigned to the variable
#linefile1 which is a text string with the name of the latest HLV1xx file.  It then replaces whatever
#is in the Input File box with linefile[]  (??? should I use linefile1 instead ??)

#Note:  currently when the name of the Output File is written to versionfile, only the last
#file name is stored.  It does not append, it overwrites.  

#then the 2nd reading function opens linefile1 (ie. some HLV1xx) and in a for loop, for each
# row read in, extracts the items of that row of linefile1 necessary to build an entry in
#displayline[].  It then inserts that entry to the end of the list Current Lines box (lbox5) and
#appends the whole row to listoflines[][].  So now have two lists:  listoflines[][] and displayline[][]
#whose indexes must be kept consistent.  listoflines[][] will eventually be read into the next HLV1xx so
#that VTK can use it to build all the action chains.

#the last part of this function, finds the version number of HLV1xx and increments by 1 creates the
#Output file name that listoflines[][] will eventually get written to.  It then replaces what ever is in the
#Output File box with that file name.  Note:  the output file name can be edited in that box before "Write Lines
#to File" box is clicked. 

def read_line(fileversions, listoflines, displayline):
    with open(versionfile, newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            fileversions.append(row)
            #print(fileversions)
            l = len(fileversions)
            #print(l)
            linefile = fileversions[l-1]
            linefile1=linefile[0]
            #print(linefile)
            #print("str", linefile1)
            InputFileBox.replace('1.0','2.0', linefile)
            namelist.append(linefile)

            
    with open(linefile1, newline="")as file1:
        reader = csv.reader(file1)
        for row in reader:
            lineid = (row[0])
            startdes = event[int(row[1])]
            enddes = eventb[int(row[5])]
            linedisplay = "Line ID="+"  "+str(lineid)+"  _  "+str(startdes)+"  >>  "+str(enddes)
            displayline.append(linedisplay)
            lbox5.insert(END,linedisplay)
            listoflines.append(row)
    
            
        #print(linefile1)
        dot_index = linefile1.find(".")
        #print(dot_index)
        dot_itgr = int(dot_index)
        q = dot_itgr-3
        r = dot_itgr
        version = linefile1[q:r]
        #print(version)
        nversion = int(version) + 1
        #print(nversion)
        subname = linefile1[0:q]
        #print(subname)
        writefile = subname+str(nversion)+".csv"
        #print(writefile)
        OutputFileBox.replace('1.0', '2.0', writefile)

            
        return listoflines
        return displayline
        return writefile

#read_line(listoflines,displayline)

#turns the lists that will be used in the listboxes into a StringVar.  ???Why is necessary???
#actually these lines set the text used for the listvariables
#as StringVAR.  It appears that the entrants to the listboxes have to be
#StringVARs


event3 = StringVar(value=eventb)        #eventb list used in End Event
event4 = StringVar(value=ACnames)       #event4 list used in Action Chain
event5 = StringVar(value=listoflines)   #event5 list used for list of lines - not sure if used
event6 = StringVar (value=displayline)  #event6 list used for display line list box



#Global variables.  They will be used outside of the functions that assign them.

ids = 0
ide = 0
idac = 0

#Selection of Start Event

def startevent(*args):
    global ids
    idxs = lbox.curselection()      #single entry list(tuple??) of index of event[] that was selected-
                                    #matches index of eventlist[]
    #print("Start Picked", idxs)
    #print()
    ids = int(idxs[0])              #integer representation of index of selected Start Event
    message.set(event[ids])         #populates the Start Event Selected box
    #lbox.insert(0, "This is a test")
    return ids

#Selection of End Event

def endevent(*args):
    global ide
    idxe = lbox2.curselection()     #single entry list (tuple??) of index of eventb[] that was selected -
                                    #matches index of eventlistb[]
    #print("End Picked", idxe)
    #print()
    ide = int(idxe[0])              #interger representation of index of selected End Event
    message2.set(eventb[ide])       #populates the End Event Selected box
    return ide

#Selection of Action Chain

def acsel(*args):
    global idac
    idxac = AClis.curselection()    #single entry list(tuple??) of index of AClis[] that was selected
                                    #matches index of AClist
    #print("AC Picked", idxac)
    idac = int(idxac[0])            #integer representationof index of selected Action Chain
    print()
    message3.set(ACnames[idac])     # populates the Action Chain Selected box
    return idac

#Selection of Build Line button box

#once the StartEvent and EndEvent and Action Chain has been selected, user hits "Build Line"
#button box and this function then:
#   - builds a linelist by
#       - creating a line number by adding 1 to the length of current listoflines[] appends to
#         linelist[0]
#       - takes the event id of StartEvent eventlist - appends to linelist[1]
#       - takes x,y,z of StartEvent eventlist append to linelist[2,3,4]
#       - takes event id of EndEvent eventlistb  - appends to linelist[5]
#       - takes x,y,z of EndEvent eventlistb - appends to linelist[6,7,8]

def createline(*args):
    global ids
    global ide
    global idac
    global listoflines
    global linelist
    global eventlist
    global eventlistb
    global AClist
    global displayline
    global event6
    ln = len(listoflines)-1
    lni = int(ln)
    print(ln)
    lid = listoflines[lni][0]               #find the line id of last line in listoflines
    tem = int(lid) + 1
    linelist.append(tem)                    #linelist[0]  - line id
    linelist.append(eventlist[ids][0])      #linelist[1]  - StartEvent id
    linelist.append(eventlist[ids][4])      #linelist[2]  - StartEvent x
    linelist.append(eventlist[ids][5])      #linelist[3]  - StartEvent y
    linelist.append(eventlist[ids][6])      #linelist[4]  - StartEvent z
    linelist.append(eventlistb[ide][0])     #linelist[5]  - EndEvent id
    linelist.append(eventlistb[ide][4])     #linelist[6]  - EndEvent x
    linelist.append(eventlistb[ide][5])     #linelist[7]  - EndEvent y
    linelist.append(eventlistb[ide][6])     #linelist[8]  - EndEvent z
    linelist.append(AClist[idac][2])        #linelist[9]  - AClist id
    linelist.append(AClist[idac][0])        #linelist[10] - AClist label
    linelist.append(AClist[idac][1])        #linelist[11] - AClist color
    listoflines.append(linelist)            #appends the linelist[] just built to listoflines[][]
    # next four lines buld the displayline[] for use in the Current Lines box
    ln2 = ln
    startdes2 = str(eventlist[ids][1]) 
    enddes2 = str(eventlistb[ide][1]) 
    linedisplay = "Line ID="+"  "+str(tem)+"  _  "+str(startdes2)+"  >>  "+str(enddes2)
    displayline.append(linedisplay)
    lbox5.insert(END,linedisplay)
    linelist=[]

##    j = 0
##    while j < len(listoflines):
##        #print(j, listoflines[j])
##        #print
##        j +=1
##
##    j=0
##    while j < len(listoflines):
##        #print(j, displayline[j])
##        j += 1
    
#selection of deleteline button box.
#Note this must keep displayline[][] and listofline[][] consistent

def deleteline(*args):
    #print("delete line selected")
    iddl = lbox5.curselection()
    idd = int(iddl[0])
    print(idd)
    displayline.pop(idd)
    listoflines.pop(idd)
    lbox5.delete(idd)

##    j = 0
##    while j < len(listoflines):
##        print(j, listoflines[j])
##        print
##        j +=1
##
##    j=0
##    while j < len(listoflines):
##        print(j, displayline[j])
##        j += 1

#selection of writefile button box

#This function first gets the name of the output file that is in the Output File text box and assigns that
#to the variable writefilename.

def writefile(*args):
    namelist = []
    global listoflines
    global versionfile
    print("write file selected")
    writefilename = OutputFileBox.get('1.0', 'end-1 chars')
    #print(writefilename)
    namelist.append(writefilename)
    #print(namelist)

    with open(writefilename, "w", newline="")as file9:
        writer = csv.writer(file9)
        writer.writerows(listoflines)

    with open(versionfile, "w", newline="")as file1:
        writer = csv.writer(file1)
        writer.writerow(namelist)
    

#selection of openfile button box
    #this calls the function that reads in linefile and creates
    #the displaylines.  It also populates the Current Lines box

def readinfile(*args):
    print("open file selected")
    read_line(fileversions, listoflines,displayline) 



#---------------------------------------------
#BUILD AND GRID ALL THE ELEMENTS OF THE UI

# LFrame
#builds LFrame inside of root and grids it
#and allows resizing
Lframe = ttk.Frame(root, padding=(10,10,10,10))     
Lframe.grid(column=0, row=0, sticky=(N,W,E,S))     
root.grid_columnconfigure(0, weight=1)              
root.grid_rowconfigure(0, weight=1)

#------------------------------------------

#Starting Event listbox

#varibles
message = StringVar()
event2 = StringVar(value=event)         #event list used in Starting Event
            
#creates first Listbox with the listvariable event2 (which is
#a StringVar ?? this seems to work.
lbox = Listbox(Lframe, listvariable=event2, width= 70, height = 20)
lbox.grid(column=0, row=1, sticky=(N,E,S,W))
lbox.grid_columnconfigure(0,weight=1)
lbox.grid_rowconfigure(0,weight=1)

#adds a scroll bar.  Note the way the " 'yscrollcommand' " is formatted
sbar=ttk.Scrollbar(Lframe, orient= VERTICAL, command=lbox.yview)
sbar.grid(column=1, row=1, sticky = (N,S,W))
lbox['yscrollcommand'] =sbar.set

#creates the label on the first list box
label= ttk.Label(Lframe, text="Starting Event")
label.grid(column=0, row=0)

#Start Event Selection Box
# a box that displays the selected Start event.
#note that I had to set the value of message in the function
#to get this to display properly. Note that when the Start Event is selected I have to
#set variable message = to the proper value...tricky
descript = ttk.Entry(Lframe, width = 70, textvariable = message, state="readonly")
descript.grid(column=0, row=2)

#------------------------------------------

#End Event list box

#variables
message2 = StringVar()


#creates the End event listbox and grids it.  Why column 3??
lbox2 = Listbox(Lframe, listvariable=event3, width= 70, height = 20)
lbox2.grid(column=3, row=1, sticky=(N,E,S,W))
lbox2.grid_columnconfigure(0,weight=1)
lbox2.grid_rowconfigure(0,weight=1)

#creates scrollbar for second listbox.  
sbar2=ttk.Scrollbar(Lframe, orient= VERTICAL, command=lbox2.yview)
sbar2.grid(column=4, row=1, sticky = (N,S,W))
lbox2['yscrollcommand'] =sbar2.set

#label for 2nd listbox
label2= ttk.Label(Lframe, text="End Event", width= 20, borderwidth=5, relief="solid" )
label2.grid(column=3, row=0)

#End Event Selection box
## creates the box that displays the selection from the End Event listbox
## grids it.  Note that when the End Event is selected I have to set variable message2
# correctly
descript2 = ttk.Entry(Lframe, width = 70, textvariable = message2, state="readonly")
descript2.grid(column=3, row=2)

#----------------------------------------

#ACList box

#variables
message3 = StringVar()
             
#creates listbox of Action Chain names
AClis = Listbox(Lframe, listvariable = event4, width = 20, height = 12)
AClis.grid(column = 5, row = 1, sticky = (N,E,W))

#label for Action Chain listbox - grids it
label3= ttk.Label(Lframe, text="Action Chain")
label3.grid(column=5, row=0)


#ACName Selection Box.  Creates the box that displays the selection from Action Chain Box
#and grids it.  Note that when the selection is made have to be variable message3 correct
descript3 = ttk.Entry(Lframe, width = 20, textvariable = message3, state="readonly")
descript3.grid(column = 5, row = 2, sticky = (N,E,W))

#--------------------------------------------------------------

#Current Lines listbox

#creates Listbox with the listvariable event6 - listoflines[] as StringVar
# Why StringVar other than this seems to work.??? 
lbox5 = Listbox(Lframe, listvariable=event6, width= 140, height = 10)
lbox5.grid(column=0, row=4, sticky=(N,E,S,W), columnspan= 4)
lbox5.grid_columnconfigure(0,weight=1)
lbox5.grid_rowconfigure(0,weight=1)

#adds a scroll bar.  Note the way the " 'yscrollcommand' " is formatted
sbar5=ttk.Scrollbar(Lframe, orient= VERTICAL, command=lbox5.yview)
sbar5.grid(column= 4, row=4, sticky = (N,S,W))
lbox5['yscrollcommand'] =sbar5.set

#creates the label on the Linelist list box
label= ttk.Label(Lframe, text="Current Lines")
label.grid(column=0, row=3)

#----------------------------------------------------------

# Create Line Button Box

createline = ttk.Button(Lframe, text = 'Create Line', command = createline, default='active')
createline.grid(column=6, row=2, sticky= (N,W))

#-----------------------------------------------------

#Delete Line Button Box

deleteb = ttk.Button(Lframe, text = 'Delete Line', command = deleteline, default='active')
deleteb.grid(column=5, row=4, sticky= (N,W))

#----------------------------------------------------

#input File Box

InputFileBox = Text(Lframe, width = 70, height = 2)
InputFileBox.grid(column=0, row=6,sticky=(E,W), columnspan = 3)
InputFileBox.grid_columnconfigure(0, weight=1)
InputFileBox.grid_rowconfigure(0, weight=1)

#InputFileBox.insert('1.0', 'This is the input file')

#creates the label on the Input File box
label= ttk.Label(Lframe, text="Input File")
label.grid(column=0, row=5)

#__________________________________________________________

#Output File Box

OutputFileBox = Text(Lframe, width = 70, height = 2)
OutputFileBox.grid(column=0, row=8,sticky=(E,W), columnspan = 3)
OutputFileBox.grid_columnconfigure(0, weight=1)
OutputFileBox.grid_rowconfigure(0, weight=1)

#OutputFileBox.insert('1.0', 'This is the output file')


#creates the label on the Output File box
label= ttk.Label(Lframe, text="Output File")
label.grid(column=0, row=7)

#---------------------------------------------------------

#Build Write to File Box
# create the Build Line button box

writefile = ttk.Button(Lframe, text='Write Lines to File', command=writefile, default='active')
writefile.grid(column=3, row= 8, sticky=(W,S))

#---------------------------------------------------------

#Build Open File Box
# create the Build Line button box

readinfile = ttk.Button(Lframe, text='Read In File', command=readinfile, default='active')
readinfile.grid(column=3, row= 6, sticky=(W,S))




# CREATE THE BINDINGS

#binding to Starting Event list    
lbox.bind('<<ListboxSelect>>', startevent)

#binding to End Event list
lbox2.bind('<<ListboxSelect>>', endevent)

#binding to AC list
AClis.bind('<<ListboxSelect>>', acsel)

#binding to Button Box
createline.bind('<<Button-1>>', createline)

#binding to Delete Button Box
deleteb.bind('<<Button-1>>', deleteline)

#binding to Write File button box
writefile.bind('<<Button-1>>', writefile)

#binding to Open File button box
readinfile.bind('<<Button-1>>', readinfile)








#-------------------------
# start the process

#first add padding
for child in Lframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

root.mainloop()       #starts the entry loop.
