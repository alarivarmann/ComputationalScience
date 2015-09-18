


"""Isosurface extraction.

This script should extract and display isosurfaces of the probability
density of a hydrogen atom in a volume dataset.

You can run the script from the command line by typing
python isosurface.py

"""

import vtk
from vtk import *


# Define a class for the keyboard interface
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
        self.filter = None
        # Add the extra attributes you need here...

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
        elif key == "Up":
            value = self.filter.GetValue(0)
            self.filter.SetValue(0, value + 0.05)
            self.render_window.Render()
        elif key == "Down":
                value = self.filter.GetValue(0)
                self.filter.SetValue(0, value - 0.05)
                self.render_window.Render()
        # Add your keyboard shortcuts here. You can use, e.g., the
        # "Up" key to increase the isovalue and the "Down" key to
        # decrease it. Don't forget to call the render window's
        # Render() function to update the rendering after you have
        # changed the isovalue.
        # elif key == ...


# Read the volume dataset
filename = "hydrogen.vtk"
reader = vtk.vtkStructuredPointsReader()
reader.SetFileName(filename)
print("Reading volume dataset from " + filename + " ...")
reader.Update()  # executes the reader
print("Done!")

# Just for illustration, extract and print the dimensions of the
# volume. The string formatting used here is similar to the sprintf
# style in C.
width, height, depth = reader.GetOutput().GetDimensions()
print("Dimensions: %i %i %i" % (width, height, depth))

# Create an outline of the volume
outline = vtk.vtkOutlineFilter()
outline.SetInput(reader.GetOutput())
outline_mapper = vtk.vtkPolyDataMapper()
outline_mapper.SetInput(outline.GetOutput())


outline_actor = vtk.vtkActor()
outline_actor.SetMapper(outline_mapper)

# Define actor properties (color, shading, line width, etc)
outline_actor.GetProperty().SetColor(0.8, 0.8, 0.8)
outline_actor.GetProperty().SetLineWidth(2.0)


#create the lookuptable for colors
lookupTable = vtk.vtkLookupTable()
lookupTable.SetNumberOfTableValues(100)
lookupTable.SetTableRange (0, 100)
lookupTable.Build()

lookupTable.SetTableValue(0, 1.0, 0.0, 0.0) # red
lookupTable.SetTableValue(0.5, 1.0, 1.0, 1.0) # white
lookupTable.SetTableValue(1, 0.0, 1.0, 0.0) # green

#create a colorbar using the lookuptable to see if it's correct
colorbar = vtk.vtkScalarBarActor() # scalarbaractor creates the visual representation of the data, it's not interacting with objects itself
colorbar.SetLookupTable(lookupTable)
colorbar.SetWidth(0.1)
colorbar.SetPosition(0.80, 0.1)
# colorbar.SetLabelFormat("%.3g")
colorbar.VisibilityOn()




isoSurface = vtk.vtkContourFilter()
isoSurface.SetInputConnection(reader.GetOutputPort())
isoSurface.SetValue(0, 0.5)


# Create a renderer and add the actors to it

#ctfun = vtk.vtkColorTransferFunction()
#ctfun.AddRGBPoint(0.0, 0.5, 0.0, 0.0)
#ctfun.AddRGBPoint(0.3, 1.0, 0.5, 0.5)
# ctfun.AddRGBPoint(0.6, 0.9, 0.2, 0.3)



isoSurface_mapper = vtk.vtkPolyDataMapper()
isoSurface_mapper.SetInput(isoSurface.GetOutput())

isoSurface_mapper.SetLookupTable(lookupTable)


# create the actor and set its properties

isoSurface_actor = vtk.vtkActor()
isoSurface_actor.SetMapper(isoSurface_mapper)




renderer = vtk.vtkRenderer()
renderer.SetBackground(0.2, 0.2, 0.2)
renderer.AddActor(outline_actor)

# renderer.AddActor(...)

renderer.AddActor(isoSurface_actor)
renderer.AddActor(colorbar)

# Create a render window
render_window = vtk.vtkRenderWindow()
render_window.SetWindowName("Isosurface extraction")
render_window.SetSize(500, 500)
render_window.AddRenderer(renderer)

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

keyboard_interface.filter = isoSurface

# Connect the keyboard interface to the interactor
interactor.AddObserver("KeyPressEvent", keyboard_interface.keypress)

# Initialize the interactor and start the rendering loop
interactor.Initialize()
render_window.Render()
interactor.Start()
