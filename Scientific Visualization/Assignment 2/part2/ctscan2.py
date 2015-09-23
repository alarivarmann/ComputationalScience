# File:        ctscan.py
# Description: MPR rendering

import vtk

class KeyboardInterface(object):
    """Keyboard interface.

    Provides a simple keyboard interface for interaction. You should
    extend this interface with keyboard shortcuts for changing the
    isovalue interactively.

    """

    def __init__(self):
        self.screenshot_counter = 0
        self.render_window = None
        self.window2image_filter = None
        self.png_writer = None
        self.renderer = None
        self.X = 256/2
        self.Xswitch = 1
        self.Yswitch = 1
        self.Zswitch = 1
        self.Y = 256/2
        self.Z = 169/2
        self.liver = 1

    def keypress(self, obj, event):
        """This function captures keypress events and defines actions for
        keyboard shortcuts."""
        key = obj.GetKeySym()
        if key == "9":
            self.render_window.Render()
            self.window2image_filter.Modified()
            screenshot_filename = ("screenshot%02d.png" %
                                   (self.screenshot_counter))
            self.png_writer.SetFileName(screenshot_filename)
            self.png_writer.Write()
            print("Saved %s" % (screenshot_filename))
            self.screenshot_counter += 1
        elif key == "g":
            if self.X < 246.0:
                self.X=self.X+10
                ipwx.SetSliceIndex(self.X)
                self.render_window.Render()
            else:
                print "Max. X value reached!"
        elif key == "b":
            if self.X > 10.0:
                self.X=self.X-10
                ipwx.SetSliceIndex(self.X)
                self.render_window.Render()
            else:
                print "Min. X value reached!"
        elif key == "h":
            if self.Y < 246.0:
                self.Y=self.Y+10
                ipwy.SetSliceIndex(self.Y)
                self.render_window.Render()
            else:
                print "Max. Y value reached!"
        elif key == "n":
            if self.Y > 10.0:
                self.Y=self.Y-10
                ipwy.SetSliceIndex(self.Y)
                self.render_window.Render()
            else:
                print "Min. Y value reached!"
        elif key == "j":
            if self.Z < 159.0:
                self.Z=self.Z+10
                ipwz.SetSliceIndex(self.Z)
                self.render_window.Render()
            else:
                print "Max. Z value reached!"
        elif key == "m":
            if self.Z > 5.0:
                self.Z=self.Z-5
                ipwz.SetSliceIndex(self.Z)
                self.render_window.Render()
            else:
                print "Min. Z value reached!"
        elif key == "6":
            if self.Xswitch == 1:
                ipwx.EnabledOff()
                self.Xswitch = 0
            else:
                ipwx.EnabledOn()
                self.Xswitch = 1
        elif key == "7":
            if self.Yswitch == 1:
                ipwy.EnabledOff()
                self.Yswitch = 0
            else:
                ipwy.EnabledOn()
                self.Yswitch = 1
        elif key == "8":
            if self.Zswitch == 1:
                ipwz.EnabledOff()
                self.Zswitch = 0
            else:
                ipwz.EnabledOn()
                self.Zswitch = 1
        elif key == "k":
            if self.Xswitch == 1 or self.Yswitch == 1 or self.Zswitch == 1:
                ipwx.EnabledOff()
                ipwy.EnabledOff()
                ipwz.EnabledOff()
                self.Xswitch = 0
                self.Yswitch = 0
                self.Zswitch = 0
            else:
                ipwx.EnabledOn()
                ipwy.EnabledOn()
                ipwz.EnabledOn()
                self.Xswitch = 1
                self.Yswitch = 1
                self.Zswitch = 1
        elif key == "l":
            if self.liver == 1:
                renderer.RemoveActor(liverActor)
                self.liver = 0
                self.render_window.Render()
            else:
                renderer.AddActor(liverActor)
                self.liver = 1
                self.render_window.Render()
# image reader
filename1 = "ctscan_ez.vtk"
reader1 = vtk.vtkStructuredPointsReader()
reader1.SetFileName( filename1 )
reader1.Update()

W,H,D = reader1.GetOutput().GetDimensions()
a1,b1 = reader1.GetOutput().GetScalarRange()
print "Range of image: %d--%d" %(a1,b1)


filename2 = "ctscan_ez_bin.vtk"
reader2 = vtk.vtkStructuredPointsReader()
reader2.SetFileName( filename2 )
reader2.Update()

a2,b2 = reader2.GetOutput().GetScalarRange()
print "Range of segmented image: %d--%d" %(a2,b2)

#Liver
liverFilter = vtk.vtkContourFilter()
liverFilter.SetInputConnection(reader2.GetOutputPort())
liverFilter.SetValue(0, 255.0)

liverMapper = vtk.vtkPolyDataMapper()
liverMapper.SetInputConnection(liverFilter.GetOutputPort())
liverMapper.SetScalarRange(0.0, 255.0)

lut = vtk.vtkLookupTable()
liverMapper.SetLookupTable(lut)
lut.SetHueRange(0.10,0.10)
lut.Build()

liverActor = vtk.vtkActor()
liverActor.SetMapper(liverMapper)

#Info Text 1
showInfoText = vtk.vtkTextMapper()
showInfoText.SetInput("Press the following keys to move the planes\nNormal to X: G ; B \nNormal to Y: H ; N\nNormal to Z: J ; M")
tprop = showInfoText.GetTextProperty()
tprop.SetFontSize(14)
tprop.SetJustificationToCentered()
tprop.SetVerticalJustificationToBottom()
tprop.SetColor(1, 1, 1)

showInfoTextActor = vtk.vtkActor2D()
showInfoTextActor.SetMapper(showInfoText)
showInfoTextActor.GetPositionCoordinate().SetCoordinateSystemToNormalizedDisplay()
showInfoTextActor.GetPositionCoordinate().SetValue(0.5, 0.01)

#Info Text 2
showInfoText2 = vtk.vtkTextMapper()
showInfoText2.SetInput("Toggle MPR: K\nToggle Individual Planes: 6 ; 7 ; 8\nToggle Segmentation: L")
tprop2 = showInfoText.GetTextProperty()
tprop2.SetFontSize(14)
#tprop2.SetJustificationToLeft()
#tprop2.SetVerticalJustificationToTop()
tprop2.SetColor(1, 1, 1)

showInfoTextActor2 = vtk.vtkActor2D()
showInfoTextActor2.SetMapper(showInfoText2)
showInfoTextActor2.GetPositionCoordinate().SetCoordinateSystemToNormalizedDisplay()
showInfoTextActor2.GetPositionCoordinate().SetValue(0.01, 0.90)


# Create a renderer
renderer = vtk.vtkRenderer()
renderer.SetBackground(0.2, 0.2, 0.2)

# Create a render window
render_window = vtk.vtkRenderWindow()
render_window.SetWindowName("CT Scan")
render_window.SetSize(512, 512)
render_window.AddRenderer(renderer)

# Create an interactor
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

#
# add your code here for MPR and the liver surface
#
# Help to get started...
# 
picker=vtk.vtkCellPicker() # use same picker for all 
picker.SetTolerance(0.005)
#X-CutPlane
ipwx = vtk.vtkImagePlaneWidget()
ipwx.SetPicker(picker) 
ipwx.SetInput(reader1.GetOutput())
ipwx.SetCurrentRenderer(renderer)
ipwx.SetInteractor(interactor)
ipwx.PlaceWidget()
ipwx.SetPlaneOrientationToXAxes()
ipwx.SetSliceIndex(W/2)
ipwx.DisplayTextOn()
ipwx.EnabledOn()
#Y-CutPlane
ipwy = vtk.vtkImagePlaneWidget()
ipwy.SetPicker(picker) 
ipwy.SetInput(reader1.GetOutput())
ipwy.SetCurrentRenderer(renderer)
ipwy.SetInteractor(interactor)
ipwy.PlaceWidget()
ipwy.SetPlaneOrientationToYAxes()
ipwy.SetSliceIndex(H/2)
ipwy.DisplayTextOn()
ipwy.EnabledOn()
#Z-CutPlane
ipwz = vtk.vtkImagePlaneWidget()
ipwz.SetPicker(picker) 
ipwz.SetInput(reader1.GetOutput())
ipwz.SetCurrentRenderer(renderer)
ipwz.SetInteractor(interactor)
ipwz.PlaceWidget()
ipwz.SetPlaneOrientationToZAxes()
ipwz.SetSliceIndex(D/2)
ipwz.DisplayTextOn()
ipwz.EnabledOn()  

# create an outline of the dataset
outline = vtk.vtkOutlineFilter()
outline.SetInput( reader1.GetOutput() )
outlineMapper = vtk.vtkPolyDataMapper()
outlineMapper.SetInput(outline.GetOutput())
outlineActor = vtk.vtkActor()
outlineActor.SetMapper(outlineMapper)

# the actors property defines color, shading, line width,...
outlineActor.GetProperty().SetColor(0.8,0.8,0.8)
outlineActor.GetProperty().SetLineWidth(2.0)

# add the actors
renderer.AddActor(outlineActor)
renderer.AddActor(liverActor)
renderer.AddActor(showInfoTextActor)
renderer.AddActor(showInfoTextActor2)
render_window.Render()

# Create a window-to-image filter and a PNG writer that can be used
# for taking screenshots
window2image_filter = vtk.vtkWindowToImageFilter()
window2image_filter.SetInput(render_window)
png_writer = vtk.vtkPNGWriter()
png_writer.SetInput(window2image_filter.GetOutput())

# Set up the keyboard interface
keyboard_interface = KeyboardInterface()
keyboard_interface.render_window = render_window
keyboard_interface.window2image_filter = window2image_filter
keyboard_interface.png_writer = png_writer
keyboard_interface.renderer = renderer

# Connect the keyboard interface to the interactor
interactor.AddObserver("KeyPressEvent", keyboard_interface.keypress)

# Initialize the interactor and start the rendering loop
interactor.Initialize()
render_window.Render()
interactor.Start()
