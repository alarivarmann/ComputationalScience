import vtk


reader = vtk.vtkStructuredPointsReader()
reader.SetFileName("foot.vtk")

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
        self.opacityTransferFunction = None
        self.skinopacity = 0.05
        self.muscleopacity = 0.5
        self.boneopacity = 0.9
        self.skincol = 1.0
        self.musclecol = 1.0
        self.bonecol = 1.0

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
            self.skinopacity = self.skinopacity + 0.05
            if self.skinopacity < 0.96:
                opacityTransferFunction.RemovePoint(60.0)
                opacityTransferFunction.AddPoint(60.0,self.skinopacity)
                print "Skin Opacity: %f" %(self.skinopacity)
                self.render_window.Render()
            else:
				print "Max. opacity value reached!"
        elif key == "b":
            self.skinopacity = self.skinopacity - 0.05
            if self.skinopacity > 0.05:
                opacityTransferFunction.RemovePoint(60.0)
                opacityTransferFunction.AddPoint(60.0,self.skinopacity)
                print "Skin Opacity: %f" %(self.skinopacity)
                self.render_window.Render()
            else:
				print "Min. opacity value reached!"
        elif key == "h":
            self.muscleopacity = self.muscleopacity + 0.1
            if self.muscleopacity < 0.91:
                opacityTransferFunction.RemovePoint(120.0)
                opacityTransferFunction.AddPoint(120.0,self.muscleopacity)
                print "Muscle Opacity: %f" %(self.muscleopacity)
                self.render_window.Render()
            else:
				print "Min. opacity value reached!"
        elif key == "n":
            self.muscleopacity = self.muscleopacity - 0.1
            if self.muscleopacity > 0.09:
                opacityTransferFunction.RemovePoint(120.0)
                opacityTransferFunction.AddPoint(120.0,self.muscleopacity)
                print "Muscle Opacity: %f" %(self.muscleopacity)
                self.render_window.Render()
            else:
				print "Min. opacity value reached!"
        elif key == "j":
            self.boneopacity = self.boneopacity + 0.05
            if self.boneopacity < 0.96:
                opacityTransferFunction.RemovePoint(200.0)
                opacityTransferFunction.AddPoint(200.0,self.boneopacity)
                print "Bone Opacity: %f" %(self.boneopacity)
                self.render_window.Render()
            else:
				print "Min. opacity value reached!"
        elif key == "m":
            self.boneopacity = self.boneopacity - 0.05
            if self.boneopacity > 0.04:
                opacityTransferFunction.RemovePoint(200.0)
                opacityTransferFunction.AddPoint(200.0,self.boneopacity)
                print "Bone Opacity: %f" %(self.boneopacity)
                self.render_window.Render()
            else:
				print "Min. opacity value reached!"
        elif key == "7":
            if self.bonecol == 1:
                colorTransferFunction.RemovePoint(150.0)
                colorTransferFunction.AddRGBPoint(150.0,0.0,1.0,0.0)
                self.bonecol = 0
                self.render_window.Render()
            else:
                colorTransferFunction.RemovePoint(150.0)
                colorTransferFunction.AddRGBPoint(150.0,1.0,1.0,1.0)
                self.bonecol = 1
                self.render_window.Render()
        elif key == "6":
            if self.skincol == 1:
                colorTransferFunction.RemovePoint(0.0)
                colorTransferFunction.AddRGBPoint(0.0,0.5,0.0,0.5)
                self.skincol = 0
                self.render_window.Render()
            else:
                colorTransferFunction.RemovePoint(0.0)
                colorTransferFunction.AddRGBPoint(0.0,1.0,0.6274,0.4784)
                self.skincol = 1
                self.render_window.Render()
        elif key == "8":
            if self.musclecol == 1:
                colorTransferFunction.RemovePoint(120.0)
                colorTransferFunction.AddRGBPoint(120.0,1.0,1.0,0.0)
                self.musclecol = 0
                self.render_window.Render()
            else:
                colorTransferFunction.RemovePoint(120.0)
                colorTransferFunction.AddRGBPoint(120.0,1.0,0.0,0.0)
                self.musclecol = 1
                self.render_window.Render()
# create an outline of the dataset
outline = vtk.vtkOutlineFilter()
outline.SetInput(reader.GetOutput())
outlineMapper = vtk.vtkPolyDataMapper()
outlineMapper.SetInput(outline.GetOutput())
outlineActor = vtk.vtkActor()
outlineActor.SetMapper(outlineMapper)
outlineActor.GetProperty().SetColor(0.8,0.8,0.8)
outlineActor.GetProperty().SetLineWidth(2.0)


opacityTransferFunction = vtk.vtkPiecewiseFunction()
opacityTransferFunction.AddPoint(20.0,0.0)
opacityTransferFunction.AddPoint(60.0,0.05)
opacityTransferFunction.AddPoint(120.0,0.5)
opacityTransferFunction.AddPoint(150.0,0.9)

colorTransferFunction = vtk.vtkColorTransferFunction()
colorTransferFunction.AddRGBPoint(0.0,1.0,0.6274,0.4784)
colorTransferFunction.AddRGBPoint(60.0,0.698,0.133,0.133)
colorTransferFunction.AddRGBPoint(120.0,1.0,0.0,0.0)
colorTransferFunction.AddRGBPoint(150.0,1.0,1.0,1.0)


volumeProperty = vtk.vtkVolumeProperty()
volumeProperty.SetColor(colorTransferFunction)
volumeProperty.SetScalarOpacity(opacityTransferFunction)

compositeFunction = vtk.vtkVolumeRayCastCompositeFunction()
volumeMapper = vtk.vtkVolumeRayCastMapper()
volumeMapper.SetVolumeRayCastFunction(compositeFunction )
volumeMapper.SetInputConnection(reader.GetOutputPort() )

volumeMapper.SetSampleDistance(.5)

volume = vtk.vtkVolume()
volume.SetMapper(volumeMapper)
volume.SetProperty(volumeProperty)

# Create a renderer and add the actors to it
renderer = vtk.vtkRenderer()
renderer.AddVolume(volume)
renderer.SetBackground(0.2, 0.2, 0.2)
renderer.AddActor(outlineActor)

# Create a render window
render_window = vtk.vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("Volume rendering of Foot data");
render_window.SetSize(500, 500)

# Create an interactor
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

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
keyboard_interface.opacityTransferFunction = opacityTransferFunction

# Connect the keyboard interface to the interactor
interactor.AddObserver("KeyPressEvent", keyboard_interface.keypress)

# Initialize the interactor and start the rendering loop
interactor.Initialize()
render_window.Render()
interactor.Start()
