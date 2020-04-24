# This version of the HL_line_reader is to try read in text from the csv file and
#display it using the vtk.BilboardTextActor3D class, in addition to drawing the lines
#and the spheres.  as of 10/20/10 at 2220 hrs this works.

### as of 11/1/19 this file is renamed HL_event_reader_V100.py and is designed to read
#just the events and display them.  I will comment out all code dealing with lines
# see Notes > VTK> MyPrograms >Next Gen Event Reader

#as of 11/20/19 this works.   Need shorten the label or put it on two lines.  Also the offsets of the labels are not
#quite right (but that is a problem with the data set.  This program behaves correctly.   Changes to this program:
#1) take he i counter off of the label.  2) add the id below each event label  3) upgraded version to V101

#as of 3/10/19 this works on just events.  Part of line display is in but commented out.  Saved this
#and renamed to hamletdisplayV110 and incremented to V110

# AS OF 3/10/20 AT 1219 THIS WORKS WITH BOTH EVENTS AND LINES!!!!!!!!!!
    #need to really test
    #need to make sure all the events and lines are included
    #need to incorporate the line weight and resolution in the line construction process
    #need to make the background white and the lettering black, so it can be printed
    #need the interactor to start up in trackball mode.



#need a much better user interface.   Look at how the interactor responds to Tkl


#import csv reader
import csv

import vtk
from vtk import *

#name the file the data is in - full path  - each line in the csv file is
# has 13 elements:

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

eventfile = "C:/Users/JRBEC/VTK_Programs/Hamlet_V117.csv"
versionfile = "C:/Users/JRBEC/VTK_Programs/Hamlet_linefile_versions.csv"

#variables
fileversions = []
listoflines = []
coords = []

#read each event into list coords[][].  coords[][] contains all the
#events from eventfile

def read_coords():
    global coords                            
    with open(eventfile, newline = "")as file:                                   
        reader = csv.reader(file)           
        for row in reader:
            #item = ""
            #if item in row:

                #continue
            #else:
            coords.append(row)             
    print("read in coords")
    print("read in coords" + " " +str(len(coords)))
    return coords


#-----------------------------------------------------------------------
#read versionfile to get the latest set of lines from HL_linesV60.py.  Versionfile
#has one entry - the latest version of HamletLinesV1xx.  Then linefile1 is the text string
#that contains the name HamletLinesV1xx.csv  Then read from HamletLinesV1xx into listofline[][]
#will will contain all the lines

def read_line(fileversions, listoflines):
    with open(versionfile, newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            fileversions.append(row)
            #print(fileversions)
            l = len(fileversions)
            print(l)
            linefile = fileversions[l-1]
            linefile1=linefile[0]
            print(linefile)
            print("str", linefile1)
            
    with open(linefile1, newline="")as file1:
        reader = csv.reader(file1)
        for row in reader:
            listoflines.append(row)

        j = 0
    while j < len(listoflines):
        print(j, listoflines[j])
        print
        j +=1

    return listoflines




  
#------------------------------------------------------------------------    

#create the renderer to be used inside the looping function below
# may need to think about local and global variables here since renderer is
#created outside the function but used both inside and outside the function

renderer = vtkRenderer()
renderer.SetBackground(1,1,1)

# Called from main.  First in for loop assign variable name to each event parameter of an 
# individual event from eventfile/coords[][]   indexed by i

def event_create(coords,numbers, colors, name_colors):
    print("event create" + " " + str(len(coords)))
    for i in range(len(coords)):        #i is the index of the events
        #print("index of coords ="+ " " + str(i))
        param_value = coords[i]         #param_value[] is the specific event indexed by the value of i
        eid = int(param_value[0])       #event id
        text = str(param_value[1])      #descriptive text
        labelf= str(param_value[2])      #first half of label
        labels= str(param_value[3])      #second half of label?
        
        xe = float(param_value[4])      #event x coord
        ye = float(param_value[5])      #event y coord
        ze = float(param_value[6])      #event z coord

        etype = str(param_value[7])     #event type (determines shape)
        
        act1 = str(param_value[8])      #actor 1 - principal actor
        act2 = str(param_value[9])      #actor 2 - secondary actor
        act3 = str(param_value[10])      #actor 3 - terceriy actor
        
        xoff = int(param_value[11])     #label offset x coord
        yoff = int(param_value[12])     #label offset y coord
        zoff = int(param_value[13])     #label offset z coord
        
        trans = float(param_value[14])  #Label transparencey (50% default)

        #determine the r,g,b values of the color of the sphere based upon the actor. This is defined
        # in a dictionary name_colors in the def main function.  rgb is from the colors dictionary also
        # in def main function
        
        inter = name_colors[act1]
        rgb = colors[inter]
        r = rgb[0]
        g = rgb[1]
        b = rgb[2]
                  
        #for the line create the incremented line, mapper and actor var names
        #line = "line" + str(i)
        #mapper = "mapper" + str(i)
        #actor = "actor" + str(i)
        
        # for the icon - now defaulted to a sphere -  create the incremented sphere var, mapper and actor
        #for now, every event is a sphere.  Will change that in the future.
        sphere = "sphere" + str(i)
        smapper = "smapper" + str(i)
        sactor = "sactor" + str(i)

        #for the label create the incremented label and the actor var name
        label = labelf + "\n" + labels + "\n" + str(eid) 
        #print(label)
        #lactor = "lactor"+str(i)

        #for the line var define its start, end and resolution, then create line
        #mapper and then the line actor.  In the actor define color and line width
        #line = vtkLineSource()
        #line.SetPoint1(xs, ys, zs)
        #line.SetPoint2(xe, ye, ze)
        #line.SetResolution(res)


        #mapper = vtkPolyDataMapper()
        #mapper.SetInputConnection(line.GetOutputPort())

        #actor = vtkActor()
        #actor.SetMapper(mapper)
        #actor.GetProperty().SetColor(r,g,b)
        #actor.GetProperty().SetLineWidth(wid)

        #now add in the sphere var at each point define its center, radius, the
        #create the sphere smapper and sactor.  In the sactor set the color

        sphere = vtkSphereSource()
        sphere.SetCenter(xe, ye, ze)
        sphere.SetRadius(5)

        smapper = vtkPolyDataMapper()
        smapper.SetInputConnection(sphere.GetOutputPort())

        sactor = vtkActor()
        sactor.SetMapper(smapper)
        sactor.GetProperty().SetColor(r,g,b)
        sactor.GetProperty().SetOpacity(trans)


        #add the text to each point,  it creates an actor directly and then set the
        #actual text and the actual location

        text = vtkBillboardTextActor3D()
        text.SetInput(label)
        text.GetTextProperty().SetFontSize(12)
        text.GetTextProperty().SetJustificationToCentered()
        text.GetTextProperty().SetOpacity(0.50)
        text.GetTextProperty().SetColor(0,0,0)
        text.SetPosition(xe, ye, ze) 
              
        renderer.AddViewProp(sactor)
        #renderer.AddViewProp(actor)
        renderer.AddActor(text)
        
        if i == (len(coords)) - 1:
            break
        #print("ran event_create")
#------------------------------------------------------------------
#called from main()

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

        

def line_create(listoflines, colors, name_colors):
    print ("line create" + " " + str(len(listoflines)))
    for i in range(len(listoflines)):
        line_value = listoflines[i]     #line_value = one line's parameters from listoflines
        lid = int(line_value[0])        #line id number
        lsid = int(line_value[1])       #id of the line start event
        lsx = int(line_value[2])        # x coord of line start event
        lsy = int(line_value[3])        # y coord of line start event
        lsz = int(line_value[4])        # z coord of line start event
        leid = int(line_value[5])       # id of the line end event
        lex = int(line_value[6])        # x coord of line end event
        ley = int(line_value[7])        # y coord of line end event
        lez = int(line_value[8])        # z coord of line end event
        lacn = int(line_value[9])       # Action chain list number (not index)
        lacl = str(line_value[10])      # Action chain label (text)
        lacc = str(line_value[11])      # Action chain color

        #determine the r,g,b values of the color of the line.

     
        rgb = colors[lacc]
        r = rgb[0]
        g = rgb[1]
        b = rgb[2]

        #for the line create the incremented line, mapper and actor var names
        lline = "line" + str(i)
        lmapper = "mapper" + str(i)
        lactor = "actor" + str(i)

        #for the line var define its start, end and resolution, then create line
        #mapper and then the line actor.  In the actor define color and line width
        lline = vtkLineSource()
        lline.SetPoint1(lsx, lsy, lsz)
        lline.SetPoint2(lex, ley, lez)
        lline.SetResolution(10)         #?????? - hard coded

        lmapper = vtkPolyDataMapper()
        lmapper.SetInputConnection(lline.GetOutputPort())

        lactor = vtkActor()
        lactor.SetMapper(lmapper)
        lactor.GetProperty().SetColor(r,g,b)
        lactor.GetProperty().SetLineWidth(2)   #hard coded to 10???  need to all to line parameter
                                                #both resolution and line width

        renderer.AddViewProp(lactor)

        if i == (len(listoflines)-1):
            break
                
        
#-----------------------------------------------------------------------------------
def main():

    #create the dictionary of colors
    colors = {"forestgreen": [0.133, 0.545, 0.133],
              "blue": [0.0, 0.0, 1.0],
              "red": [1.0, 0.0, 0.0],
              "lsalmon":[1.0, 0.627, 0.478],
              "purple": [0.502, 0.0, 0.502],
              "chocolate": [0.824, 0.412, 0.118],
              "darkorange": [1.0, 0.549, 0.00],
              "yellowgreen": [0.604, 0.804, 0.196],
              "gray": [0.502, 0.502, 0.502],
              "deeppink": [1.0, 0.078, 0.576],
              "brown": [0.647, 0.163, 0.165],
              "lime": [0.00, 1.00, 0.00],
              "dodgerblue": [0.118, 0.565, 1.00],
              "lawngreen": [0.486, 0.988, 0.00],
              "darkkhaki": [0.741, 0.718, 0.420],
              "white": [1.0, 1.0, 1.0]}

    #create the names/colors dictionary
    name_colors = {"Hamlet": "forestgreen",
                   "Horatio": "blue",
                   "Claudius": "red",
                   "King":"red",
                   "Gertrude": "lsalmon",
                   "Ghost": "purple",
                   "Polonius": "chocolate",
                   "Laertes": "darkorange",
                   "Ophelia": "yellowgreen",
                   "Voltemand": "gray",
                   "Cornelius": "gray",
                   "Rosencrantz": "deeppink",
                   "Guilderstern": "deeppink",
                   "Fortinbras": "brown",
                   "First_player": "lime",
                   "Marcellus": "dodgerblue",
                   "Barnardo": "dodgerblue",
                   "Elder_Hamlet": "lawngreen",
                   "Elder_Norway": "darkkhaki",
                   "": "white"}



    # Create axes
    linex = vtkLineSource()     # x axis
    linex.SetPoint1(0, 0, 0)
    linex.SetPoint2(5000, 0, 0)
    linex.SetResolution(32)

    liney = vtkLineSource()     #y axis
    liney.SetPoint1(0, 0, 0)
    liney.SetPoint2(0, 1000, 0)
    liney.SetResolution(32)

    linez = vtkLineSource()     #Z axis
    linez.SetPoint1(0, 0, 0)
    linez.SetPoint2(0, 0, 1000)
    linez.SetResolution(32)

    #add mappers for axes
    mapperx = vtkPolyDataMapper()
    mapperx.SetInputConnection(linex.GetOutputPort())

    mappery = vtkPolyDataMapper()
    mappery.SetInputConnection(liney.GetOutputPort())

    mapperz = vtkPolyDataMapper()
    mapperz.SetInputConnection(linez.GetOutputPort())

    #create actors for axes
    actorx = vtkActor()
    actorx.SetMapper(mapperx)
    actorx.GetProperty().SetColor(0., 0., 0.)  #x = white - black
    actorx.GetProperty().SetLineWidth(2.5)

    actory = vtkActor()
    actory.SetMapper(mappery)
    actory.GetProperty().SetColor(0., 0., 1.)  #y = blue
    actory.GetProperty().SetLineWidth(2.5)

    actorz = vtkActor()
    actorz.SetMapper(mapperz)
    actorz.GetProperty().SetColor(1., 0., 0.)  #z = red
    actorz.GetProperty().SetLineWidth(2.5)

    #add axes actors to renderer
    renderer.AddViewProp(actorx)
    renderer.AddViewProp(actory)
    renderer.AddViewProp(actorz) 
     
    
# this function reads all the events into coords[][]
    numbers = read_coords()

#this function reads in all the lines into listoflines[][]
    numbers5 = read_line(fileversions, listoflines)

#this function is main loop that creates and renders all the events
    #print(str(len(coords)))
    event = event_create(coords, numbers, colors, name_colors)       #eliminated numbers ??

#this function is main loop that creates and renders all the lines
    lines5 = line_create(listoflines, colors, name_colors)
    

    window = vtkRenderWindow()
    window.AddRenderer(renderer)
    window.SetSize(1000,700)

    interactor = vtkRenderWindowInteractor()
    interactor.SetRenderWindow(window)

    window.Render()
    interactor.Start()

main()
