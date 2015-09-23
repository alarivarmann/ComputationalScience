# File:        volren.py
# Description: Volume rendering of a medical image

import vtk

# image reader
filename = input("Enter filename ( 'myfile.vtk' ): ")
reader = vtk.vtkStructuredPointsReader()
reader.SetFileName( filename )
reader.Update()

data = reader.GetOutput()
a,b = data.GetScalarRange()
print "Range of image: %d--%d" %(a,b)

# OBS! VTK's ray caster can only handle datasets of type
# unsigned char and unsigned short so if you want to render a signed
# dataset you need to copy it and transform it. This is easy to do with
# the vtkImageShiftScale function. Below is an example on how a
# dataset with range [a, b] is converted and stretched to a 8 bit
# unsigned dataset with range [0,255]
#
# iss = vtk.vtkImageShiftScale()
# iss.SetInput( data )
# iss.SetOutputScalarTypeToUnsignedChar()
# iss.SetShift(-a)
# iss.SetScale(255.0/(b-a))
#
# Now you use iss.GetOutput() instead

# create an outline of the dataset
outline = vtk.vtkOutlineFilter()
outline.SetInput( data )
outlineMapper = vtk.vtkPolyDataMapper()
outlineMapper.SetInput( outline.GetOutput() )
outlineActor = vtk.vtkActor()
outlineActor.SetMapper( outlineMapper )

# the actors property defines color, shading, line width,...
outlineActor.GetProperty().SetColor(0.0,0.0,1.0)
outlineActor.GetProperty().SetLineWidth(2.0)






#
# add your code here...
#
# transfer functions,
# vtkVolumeProperty,
# vtkVolumeRayCastMapper,
# vtkVolumeRayCastFunction,
# vtkVolume, ...
#






# a text actor
textActor = vtk.vtkTextActor()
tp = vtk.vtkTextProperty()
tp.BoldOn()
tp.ShadowOn()
tp.ItalicOn()
tp.SetColor(0,0,0)
tp.SetFontFamilyToArial()
tp.SetFontSize(30)
textActor.SetTextProperty(tp)
tpc = textActor.GetPositionCoordinate()
tpc.SetCoordinateSystemToNormalizedViewport()
tpc.SetValue(0.1,0.9)
textActor.SetWidth(.2)
textActor.SetHeight(.2)
textActor.SetInput( "File: " + filename )

# renderer and render window 
ren = vtk.vtkRenderer()
ren.SetBackground(1, 1, 1)
renWin = vtk.vtkRenderWindow()
renWin.SetSize( 512, 512 )
renWin.AddRenderer( ren )

# render window interactor
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow( renWin )

# add the actors
ren.AddActor( outlineActor )
ren.AddActor( textActor )
#ren.AddVolume( myvolume )
renWin.Render()

# create window to image filter to get the window to an image
w2if = vtk.vtkWindowToImageFilter()
w2if.SetInput(renWin)

# create png writer
wr = vtk.vtkPNGWriter()
wr.SetInput(w2if.GetOutput())

# Python function for the keyboard interface
# count is a screenshot counter
count = 0
def Keypress(obj, event):
    global count, iv
    key = obj.GetKeySym()
    if key == "s":
        renWin.Render()     
        w2if.Modified() # tell the w2if that it should update
        fnm = "screenshot%02d.png" %(count)
        wr.SetFileName(fnm)
        wr.Write()
        print "Saved '%s'" %(fnm)
        count = count+1
    # add your keyboard interface here
    # elif key == ...

# add keyboard interface, initialize, and start the interactor
iren.AddObserver("KeyPressEvent", Keypress)
iren.Initialize()
iren.Start()
