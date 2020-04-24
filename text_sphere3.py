

#this program is to create a sphere at some location and then to add a text
#label to it using vtkBillboardTextActor3D.  Purpose is learn how to use
#vtkBillboardTextActor3D

from vtk import *     #imports all of vtk

renderer = vtkRenderer()

def sphere_create():

    sphere = vtkSphereSource()
    sphere.SetCenter(5, 5, 5)   #centers it at 5,5,5
    sphere.SetRadius(2)
    sphere.SetThetaResolution(20)
    sphere.SetPhiResolution(20)

    smapper = vtkPolyDataMapper()
    smapper.SetInputConnection(sphere.GetOutputPort())  

    sactor = vtkActor()
    sactor.SetMapper(smapper)
    sactor.GetProperty().SetColor(0, 0, 1)
    sactor.GetProperty().SetOpacity(0.5)

    renderer.AddViewProp(sactor)

def text_create():
    text = vtkBillboardTextActor3D()
    text.SetInput("This is a Sphere \n 2nd Line")
    text.SetPosition(5, 8, 5)
    text.VisibilityOn()
    text.GetTextProperty().SetColor(1, 0, 0)
    text.GetTextProperty().SetFontSize(24)
    text.GetTextProperty().SetFontFamilyToArial()
    text.GetTextProperty().SetBold(1)
    text.GetTextProperty().FrameOn()
    text.GetTextProperty().SetJustificationToCentered()
    #text.GetTextProperty().SetLineOffset(-30)
    text.GetTextProperty().SetOpacity(1.0)
    text.GetTextProperty().SetOrientation(45)
    text.GetTextProperty().ShadowOn()

    renderer.AddActor(text)

def main():

        # Create axes
    linex = vtkLineSource()     # x axis
    linex.SetPoint1(0, 0, 0)
    linex.SetPoint2(10, 0, 0)  #needed to stretch the x axis by 6
    linex.SetResolution(32)

    liney = vtkLineSource()     #y axis
    liney.SetPoint1(0, 0, 0)
    liney.SetPoint2(0, 10, 0)  # need to strech the y axis by 5
    liney.SetResolution(32)

    linez = vtkLineSource()     #Z axis
    linez.SetPoint1(0, 0, 0)
    linez.SetPoint2(0, 0, 10)  # need to stretch z axis by 5
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
    actorx.GetProperty().SetColor(1., 1., 1.)
    actorx.GetProperty().SetLineWidth(2.5)

    actory = vtkActor()
    actory.SetMapper(mappery)
    actory.GetProperty().SetColor(0., 0., 1.)
    actory.GetProperty().SetLineWidth(2.5)

    actorz = vtkActor()
    actorz.SetMapper(mapperz)
    actorz.GetProperty().SetColor(1., 0., 0.)
    actorz.GetProperty().SetLineWidth(2.5)

    #add axes actors to renderer
    renderer.AddViewProp(actorx)
    renderer.AddViewProp(actory)
    renderer.AddViewProp(actorz) 
     

    spheres = sphere_create()
    texts = text_create()

    window = vtkRenderWindow()
    window.AddRenderer(renderer)
    window.SetSize(500,500)

    interactor = vtkRenderWindowInteractor()
    interactor.SetRenderWindow(window)

    window.Render()
    interactor.Start()

main()
    
