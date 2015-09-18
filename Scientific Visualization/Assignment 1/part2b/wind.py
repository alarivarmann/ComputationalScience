"""Air currents.

This script should display a visualization of a vtkStructuredPoints
dataset containing the direction and speed of air currents over North
America.

You can run the script from the command line by typing
python wind.py

"""

import vtk
import math


# Define a class for the keyboard interface
class KeyboardInterface(object):
    """Keyboard interface.
    Provides a simple keyboard interface for interaction. You may
    extend this interface with keyboard shortcuts for, e.g., moving
    the slice plane(s) or manipulating the streamline seedpoints.

    """

    def __init__(self):
        self.screenshot_counter = 0
        self.render_window = None
        self.window2image_filter = None
        self.png_writer = None
        self.cut_plane = None
        self.Z = 7.5
        # Add the extra attributes you need here...

    def keypress(self, obj, event):
        """This function captures keypress events and defines actions for
        keyboard shortcuts."""
        global D, render_window
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
        elif key == "Up":
            if self.Z < 15.0:
                self.Z=self.Z+0.5
                self.cut_plane.SetExtent(0,W,0,H,self.Z,self.Z)
                self.render_window.Render()
            else:
                print "Max. Z value reached!"
        elif key == "Down":
            if self.Z > 0:
                self.Z=self.Z-0.5
                self.cut_plane.SetExtent(0,W,0,H,self.Z,self.Z)
                self.render_window.Render()
            else:
                print "Min. Z value reached!"
		#print 'Prob = %f' %(self.contour_filter.GetValue(0))
        # Add your keyboard shortcuts here. If you modify any of the
        # actors or change some other parts or properties of the
        # scene, don't forget to call the render window's Render()
        # function to update the rendering.
        # elif key == ...


# Read the dataset
filename = "wind.vtk"
reader = vtk.vtkStructuredPointsReader()
reader.SetFileName("wind.vtk")
print("Reading North American windcurrents dataset from " + filename + " ...")
print("Done!")
reader.Update()

#numpy_data = numpy_support.vtk_to_numpy(reader.GetOutput())
# print(numpy_data[:,:,7])

# Just for illustration, extract and print the dimensions of the volume.
width, height, depth = reader.GetOutput().GetDimensions()
print("Dimensions: %i %i %i" % (width, height, depth))

#Outline
outline = vtk.vtkOutlineFilter()
outline.SetInput(reader.GetOutput())
outline_mapper = vtk.vtkPolyDataMapper()
outline_mapper.SetInput(outline.GetOutput())
outline_actor = vtk.vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(0.8, 0.8, 0.8)
outline_actor.GetProperty().SetLineWidth(2.0)

# The range and bounds of the data
a,b = reader.GetOutput().GetScalarRange()
W,H,D = reader.GetOutput().GetDimensions()
xmi, xma, ymi, yma, zmi, zma = reader.GetOutput().GetBounds()

# Color Transfer Function
ctf = vtk.vtkLookupTable()
ctf.SetHueRange(0.667, 0.0)
ctf.SetValueRange(1.0, 1.0)
ctf.SetSaturationRange(1.0, 1.0)
ctf.SetTableRange(a,b)

# A plane for the seeds
plane = vtk.vtkPlaneSource()
plane.SetOrigin(xmi,math.ceil(ymi),zmi)
plane.SetPoint1(xma,math.ceil(ymi),zmi)
plane.SetPoint2(xmi,math.ceil(ymi),zma)
plane.SetXResolution(6)
plane.SetYResolution(6)

# Streamlines
stream = vtk.vtkStreamLine()
stream.SetSource(plane.GetOutput())
stream.SetInput(reader.GetOutput())
stream.SetIntegrationDirectionToForward()
stream.SetIntegrator(vtk.vtkRungeKutta4())
stream.SetStepLength(0.1)

streamMapper = vtk.vtkPolyDataMapper()
streamMapper.SetLookupTable(ctf)
streamMapper.SetInput(stream.GetOutput())
streamMapper.SetScalarRange(a,b)
streamActor = vtk.vtkActor()
streamActor.SetMapper(streamMapper)
streamActor.GetProperty().SetLineWidth(3.0)

#Colour Bar
cbar = vtk.vtkScalarBarActor()
cbar.SetLookupTable(ctf)
cbar.SetOrientationToHorizontal()
cbar.SetPosition(0.1,0.03)
cbar.SetHeight(0.1)
cbar.SetWidth(0.8)
cbar.SetTitle("Wind speed")


#Sliceplane
sliceplane = vtk.vtkImageDataGeometryFilter()
sliceplane.SetInput(reader.GetOutput())
sliceplane.SetExtent(0,W,0,H,D/2,D/2)

sliceplaneMapper = vtk.vtkPolyDataMapper()
sliceplaneMapper.SetLookupTable(ctf)
sliceplaneMapper.SetInput(sliceplane.GetOutput())
sliceplaneMapper.SetScalarRange(a,b)

sliceplaneActor = vtk.vtkActor()
sliceplaneActor.SetMapper(sliceplaneMapper)

#Glyphs
arrow = vtk.vtkArrowSource()
arrow.SetTipRadius(0.03)
arrow.SetShaftRadius(0.01)

arrowGlyph = vtk.vtkGlyph3D()
arrowGlyph.SetInput(sliceplane.GetOutput())
arrowGlyph.SetSourceConnection(arrow.GetOutputPort())

arrowGlyph.SetScaleFactor(0.05)

arrowMapper = vtk.vtkPolyDataMapper()
arrowMapper.SetInputConnection(arrowGlyph.GetOutputPort())


lut = vtk.vtkLookupTable()
arrowMapper.SetLookupTable(lut)
lut.SetHueRange(0.0,0.0)
lut.Build()

arrowActor = vtk.vtkActor()
arrowActor.SetMapper(arrowMapper)

# Create a renderer and add the actors to it
renderer = vtk.vtkRenderer()
renderer.SetBackground(0, 0, 0)
# renderer.AddActor(...)
renderer.AddActor(outline_actor)
renderer.AddActor(streamActor)
renderer.AddActor(arrowActor)
renderer.AddActor(sliceplaneActor)
renderer.AddActor(cbar)

# Create a render window
render_window = vtk.vtkRenderWindow()
render_window.SetWindowName("Air currents")
render_window.SetSize(800, 600)
render_window.AddRenderer(renderer)

# Create an interactor
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

#Plane
"""plane2=vtk.vtkImagePlaneWidget()
plane2.SetInput(reader.GetOutput())
plane2.SetSliceIndex(20)
plane2.SetInteractor(interactor)
plane2.EnabledOn()
plane2.SetPlaneOrientationToZAxes()"""

# Create a window-to-image filter and a PNG writer that can be used
# to take screenshots
window2image_filter = vtk.vtkWindowToImageFilter()
window2image_filter.SetInput(render_window)
png_writer = vtk.vtkPNGWriter()
png_writer.SetInput(window2image_filter.GetOutput())

# Set up the keyboard interface
keyboard_interface = KeyboardInterface()
keyboard_interface.render_window = render_window
keyboard_interface.window2image_filter = window2image_filter
keyboard_interface.png_writer = png_writer
keyboard_interface.cut_plane = sliceplane

# Connect the keyboard interface to the interactor
interactor.AddObserver("KeyPressEvent", keyboard_interface.keypress)

# Initialize the interactor and start the rendering loop
interactor.Initialize()
render_window.Render()
interactor.Start()
