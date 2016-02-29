
from __future__ import print_function
import math
import time
from vtk import *
from array import *
import vtk.util.numpy_support as VN
import numpy as np



# ANIMATION IDEAS --------------------------




# ------------------------------------------------

def main():
    #global location
    #global magnitude
    # global data
    # global time_seconds

	#  renderWindow, min_time, max_time, threshold_filter
    try:
        location
        render_3D_points(4,7)
    except:
        path_to_data_file = 'events3.csv'
        data = parse_csv(path_to_data_file)
        location, magnitude, time_seconds = generate_3D_map_data(data)
        convert_to_vtk(location, magnitude, time_seconds)
        render_3D_points(4,7)
        #render_3D_points(2,4)
	# KEYBOARD

class KeyboardInterface(object):
	def __init__(self):
		self.screenshot_counter = 0
		self.render_window = None
		self.window2image_filter = None
		self.png_writer = None
		self.threshold_filter = None
		self.time_seconds = None
		self.min_time = 0.0
		self.max_time = None
		self.current_time = 0.0
	def keypress(self, obj, event):
		key = obj.GetKeySym()
		if key == "0":
			self.current_time = self.min_time
            	while self.current_time < self.max_time:
               		self.threshold_filter.ThresholdBetween(self.min_time, self.current_time)
                	self.current_time += 400
			if self.current_time > self.max_time:
				break
			self.render_window.Render()


		#window2image_filter.Update()


               #writer = vtk.vtkAVIWriter()
               #writer.SetInputConnection(window2image_filter.GetOutputPort())
               #writer.SetFileName("test.avi")
               #writer.Start()

def parse_csv(path):
    """
    Returns a list of lists containing row values:
    [time_stamp, longitude, depth, magnitude, source].
    """
    data = list()

    f = open(path)

    for line in f:
        if line[0] == '#':
            continue
        line = line.strip()[0:-1].split(';')

        time_stamp = int(time.mktime(time.strptime(line[0], '%Y-%m-%d %H:%M:%S.%f')))
        latitude, longitude, depth = ([float(x) for x in line[1:4]])
        magnitude = float(line[4].split('--')[0])
        source = line[5]

        data.append([time_stamp, latitude, longitude, depth, magnitude, source])

    f.close()

    return data


def distance(lat1, lon1, lat2, lon2):
    """
    Returns distance in kilometres based on latitude and longitude of 2 coordinates.
    """
    R = 6371
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)

    a = math.sin(dLat / 2.0) * math.sin(dLat / 2.0) + math.sin(dLon / 2.0) * math.sin(dLon / 2.0) * math.cos(lat1) * math.cos(lat2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = R * c
    return d


def generate_3D_map_data(data):

    """
    Uses the data to create VTK objects for rendering.
    """
    # Create an array of Points
    location = vtk.vtkPoints()

    # Create arrays of Scalars
    magnitude = vtk.vtkFloatArray()
    time_seconds = vtk.vtkFloatArray()

    LatMax = 0
    LatMin = 360
    LonMax = 0
    LonMin = 360

    for data_point in data:
        t, x, y, z, r = (data_point[:-1]) # x- latitude; y - longitude, z - depth

        # Compute the extremity of the locations
        if x > LatMax:
            LatMax = x
        if x < LatMin:
            LatMin = x
        if y > LonMax:
            LonMax = y
        if y < LonMin:
            LonMin = y

        # Insert floats into the point array
        min_filtered_strength = 2.5

        if r > min_filtered_strength:
            location.InsertNextPoint(x, y, z)
            magnitude.InsertNextValue(r)
            time_seconds.InsertNextValue(t / 1000.) # I added divide by 1000 to convert to seconds

    # Compute the range of the data using the distance function
    x1 = distance(LatMin,LonMin,LatMax,LonMin)
    x2 = distance(LatMin,LonMax,LatMax,LonMax)
    y1 = distance(LatMin,LonMin,LatMin,LonMax)
    y2 = distance(LatMax,LonMin,LatMax,LonMax)

    # Adjust the location to kilometers relative to the origin (LatMin, LonMin) instead of latitude and longitude
    xx = x1
    l = location.GetNumberOfPoints()
    i = 0
    while i < l:
        x,y,z = location.GetPoint(i)
        u = (x - LatMin) / (LatMax - LatMin) # Normalized latitude
        x = (x - LatMin) / (LatMax - LatMin) * xx   # Normalized relative latitude x distance

        yy = (1 - u) * y1 + u * y2    # yy is linear in latitude -- lin interpolation
        y = (y - LonMin) / (LonMax - LonMin) * yy

        location.SetPoint(i, x, y, z)
        i = i + 1


    return location, magnitude, time_seconds

def convert_to_vtk(location, magnitude,time_seconds):
    global min_time
    global max_time
    global points
    global strength
    global time_
    points, strength, time_ = location, magnitude, time_seconds
    min_strength, max_strength = strength.GetRange()

    min_time, max_time = time_.GetRange()  # in seconds

    # Assign unique names to the scalar arrays
    strength.SetName("strength")
    time_.SetName("time")

    # Create a vtkPolyData object from the earthquake data and specify
    # that "strength" should be the active scalar array


    # Threshold the earthquake points to extract all points within a
    # specified time interval.
    #
    # If you do not specify which input array to process, i.e., if you
    # comment out the SetInputArrayToProcess() call, the thresholding will
    # be performed on the active scalar array ("strength", in this case).

    unstructuredgrid_data=vtk.vtkUnstructuredGrid()

    # Read arguments
    unstructuredgrid_data.SetPoints(points)
    unstructuredgrid_data.GetPointData().AddArray(strength)
    unstructuredgrid_data.GetPointData().AddArray(time_)
    unstructuredgrid_data.GetPointData().SetActiveScalars("strength")

    filename = "earthquake_vtk_r.vtk"
    output_at_unstructured=vtk.vtkUnstructuredGridWriter()
    output_at_unstructured.SetInput(unstructuredgrid_data)
    output_at_unstructured.SetFileName(filename)
    output_at_unstructured.Write()

    #return unstructuredgrid_data


def render_3D_points(min_filtered_strength, max_filtered_strength):
    # if I define a dosctring for a class A, then if I run help(A) , then I get the docstring output

    unstructured_reader = vtkUnstructuredGridReader()
    unstructured_reader.SetFileName("earthquake_vtk_r.vtk")
    unstructured_reader.Update()


    threshold_filter = vtk.vtkThresholdPoints() # creates the filter for magnitude filtering
    threshold_filter.SetInput(unstructured_reader.GetOutput())


    #threshold_filter.SetInputArrayToProcess(0, 0, 0, "strength")
    threshold_filter.ThresholdBetween(min_filtered_strength,max_filtered_strength)
    threshold_filter.Update()

    spheresource = vtk.vtkSphereSource()
    spheresource.SetThetaResolution(6)

    myGlyph = vtk.vtkGlyph3D() # filtered data goes to 3D glyph FILTER
    myGlyph.SetInput(threshold_filter.GetOutput())
    myGlyph.SetSource(spheresource.GetOutput())
    myGlyph.ScalingOn()
    myGlyph.SetScaleFactor(7.0)

    myGlyph.SetScaleModeToScaleByScalar()
    myGlyph.SetColorModeToColorByScalar()

    # Heated iron ------------------------------------------------------------------

    glyphMapper = vtk.vtkPolyDataMapper() # data goes thru GLYPH LINE
    glyphMapper.SetInputConnection(myGlyph.GetOutputPort())

    scalarBar = vtk.vtkScalarBarActor()
    scalarBar.SetWidth(0.05)




    colorTransferFunction = vtkColorTransferFunction()
    colorTransferFunction.AddRGBPoint(min_filtered_strength, 1.0, 1.0, 0)
    colorTransferFunction.AddRGBPoint(min_filtered_strength + 0.5, 255.0/255.0, 153.0/255.0, 51.0/255.0)
    colorTransferFunction.AddRGBPoint(min_filtered_strength + 1.5, 255.0/255.0, 0, 0)

    colorTransferFunction.AddRGBPoint(max_filtered_strength, 120.0/255.0, 0, 120.0/255.0)







    glyphMapper.SetLookupTable(colorTransferFunction)
    scalarBar.SetLookupTable(colorTransferFunction)





    pngReader = vtk.vtkPNGReader()
    pngReader.SetFileName( "staticmap.png")

    tekstuur = vtk.vtkTexture() # READER gets the texture as input,
    tekstuur.SetInputConnection(pngReader.GetOutputPort()) # map goes into the texture


    # Create a plane source and actor. The vtkPlanesSource generates
    # texture coordinates.
     # SET PLANE SIZE --- NORMAL DIRECTION, CENTROID
    plane = vtk.vtkPlaneSource() # TEXTURE COORDINATES CREATED BY PLANESOURCE, POLYGON HAS BOTH 3d COORD'S + ASSOCIATED TEXTURE COORDINATES

    plane = vtkPlaneSource()
    min_x,max_x,min_y,max_y,min_z,max_z = unstructured_reader.GetOutput().GetBounds()
    plane.SetOrigin(min_x,min_y,0)
    plane.SetPoint1(min_x,max_y,0)
    plane.SetPoint2(max_x,min_y,0)
    plane.SetXResolution(10)
    plane.SetYResolution(20)


    # -----------------------------------------------

    planeMapper = vtk.vtkPolyDataMapper()
    planeMapper.SetInputConnection(plane.GetOutputPort()) # polydatamapper divides plane data into points, lines or triangles
    planeActor = vtk.vtkActor()
    #planeActor.GetProperty().SetScalarOpacity()


    planeActor.SetMapper(planeMapper)
    planeActor.SetTexture(tekstuur)
    planeActor.SetPosition(1,1,-30)
    planeActor.GetProperty().SetOpacity(0.7)

    # ----------------------------------------------------------------------



    # coordinate axis visualiser
    transform = vtk.vtkTransform()
    transform.Translate(1200, 1300.0, 0.0)
    axes = vtk.vtkAxesActor()

    axes.SetUserTransform(transform)


    axes.GetXAxisCaptionActor2D().GetCaptionTextProperty().SetColor(0.9, 0.3, 0.0)
    axes.GetXAxisShaftProperty().SetColor(0.9, 0.3, 0.0)
    axes.GetXAxisTipProperty().SetColor(0.9, 0.3, 0.0)

    axes.GetYAxisCaptionActor2D().GetCaptionTextProperty().SetColor(0.2, 0.8, 0.0);
    axes.GetYAxisShaftProperty().SetColor(0.2, 0.8, 0.0)
    axes.GetXAxisTipProperty().SetColor(0.2, 0.8, 0.0)

    axes.GetZAxisCaptionActor2D().GetCaptionTextProperty().SetColor(0.0, 0.5, 0.7);
    axes.GetZAxisShaftProperty().SetColor(0.0, 0.5, 0.7)
    axes.GetXAxisTipProperty().SetColor(0.0, 0.5, 0.7)


    axes.SetXAxisLabelText("latitude")
    axes.GetXAxisCaptionActor2D().GetTextActor().SetTextScaleMode(0.95)
    axes.GetXAxisCaptionActor2D().GetCaptionTextProperty().SetFontSize(20)

    axes.SetYAxisLabelText("longitude")
    axes.GetYAxisCaptionActor2D().GetTextActor().SetTextScaleMode(0.95)
    axes.GetYAxisCaptionActor2D().GetCaptionTextProperty().SetFontSize(20)
    axes.SetZAxisLabelText("depth")
    axes.GetZAxisCaptionActor2D().GetTextActor().SetTextScaleMode(0.95)
    axes.GetZAxisCaptionActor2D().GetCaptionTextProperty().SetFontSize(20)

    axes.SetNormalizedShaftLength(100.0, 100.0, 100.0)

    showInfoText = vtk.vtkTextMapper()
    showInfoText.SetInput("Rotate the map to the position of your interest. \n Use mouse to zoom in \n Press 0 to relax and see the earthquake animation in real time  "  )
    tprop = showInfoText.GetTextProperty()
    tprop.SetFontSize(20)
    tprop.SetJustificationToCentered()

    tprop.SetColor(1, 1, 1)

    Infomessage = vtk.vtkActor2D()
    Infomessage.SetMapper(showInfoText)
    Infomessage.GetPositionCoordinate().SetCoordinateSystemToNormalizedDisplay()
    Infomessage.GetPositionCoordinate().SetValue(0.5, 0.01)

    magnitudetext = vtk.vtkTextMapper()
    magnitudetext.SetInput("Earthquake Magnitude (Richter)  "  )
    tprop2 = magnitudetext.GetTextProperty()
    tprop2.SetFontSize(20)


    magnitudeactor = vtk.vtkActor2D()
    magnitudeactor.SetMapper(magnitudetext)
    magnitudeactor.GetPositionCoordinate().SetCoordinateSystemToNormalizedDisplay()
    magnitudeactor.GetPositionCoordinate().SetValue(0, 0.9)

        # ----------------------- AXES END








    scalarBar = vtk.vtkScalarBarActor()
    scalarBar.SetWidth(0.05)
    scalarBar.SetLookupTable( colorTransferFunction )
    scalarBar.SetPosition(0.05,0.1)
    # RENDERER START

    renderer = vtk.vtkRenderer()
    renderer.SetBackground(0.0, 0.0, 0.0)
    renderer.AddActor(axes)
    renderer.AddActor(planeActor)
    renderer.AddActor(scalarBar)
    renderer.AddActor(Infomessage)
    renderer.AddActor(magnitudeactor)

    renderWindow = vtk.vtkRenderWindow()
    renderWindow.SetSize(1500,1200)
    renderWindow.AddRenderer(renderer)



    #style = vtk.vtkInteractorStyleTrackballCamera()
#   def render_3D_points(min_filtered_strength, max_filtered_strength):
    # if I define a dosctring for a class A, then if I run help(A) , then I get the docstring output

    unstructured_reader = vtkUnstructuredGridReader()
    unstructured_reader.SetFileName("earthquake_vtk_r.vtk")
    unstructured_reader.Update()


    threshold_filter = vtk.vtkThresholdPoints() # creates the filter for magnitude filtering
    threshold_filter.SetInput(unstructured_reader.GetOutput())


    #threshold_filter.SetInputArrayToProcess(0, 0, 0, "strength")
    threshold_filter.ThresholdBetween(min_filtered_strength,max_filtered_strength)
    threshold_filter.Update()


    camera =vtkCamera ()


    camera.SetFocalPoint((max_x-min_x)/2,(max_y-min_y)/2,min_z)
    camera.SetPosition((max_x-min_x)/2,(max_y-min_y)/2,-1000)
    camera.Zoom(30)




    spheresource = vtk.vtkSphereSource()
    myGlyph = vtk.vtkGlyph3D() # filtered data goes to 3D glyph FILTER


    myGlyph.SetInput(threshold_filter.GetOutput())


    myGlyph.SetSource(spheresource.GetOutput())
    myGlyph.ScalingOn()
    myGlyph.SetScaleFactor(6.0)



    myGlyph.SetScaleModeToScaleByScalar()
    myGlyph.SetColorModeToColorByScalar()


    glyphMapper = vtk.vtkPolyDataMapper() # data goes thru GLYPH LINE
    glyphMapper.SetInputConnection(myGlyph.GetOutputPort())
    glyphMapper.SetLookupTable(colorTransferFunction)

    # setup display stuff
    glyphActor = vtk.vtkActor()

    #planeActor.RotateZ(-90)
    #glyphActor.RotateZ(-90)
    #axes.RotateZ(-90)
    #planeActor.RotateY(150)
    #glyphActor.RotateY(150)
    #axes.RotateY(130)



    glyphActor.SetMapper(glyphMapper)
    renderer.AddActor(glyphActor)
    #renderer.SetActiveCamera(camera)



    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer)

    window2image_filter = vtk.vtkWindowToImageFilter()
    window2image_filter.SetInput(render_window)
    png_writer = vtk.vtkPNGWriter()
    png_writer.SetInput(window2image_filter.GetOutput())

    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(render_window)

	    # Set up the keyboard interface
    keyboard_interface = KeyboardInterface()
    keyboard_interface.render_window = render_window
    keyboard_interface.window2image_filter = window2image_filter
    keyboard_interface.png_writer = png_writer

    threshold_filter.SetInputArrayToProcess(0, 0, 0, 0, "time")

    keyboard_interface.threshold_filter = threshold_filter
    keyboard_interface.min_time = min_time
    keyboard_interface.max_time = max_time

    # Connect the keyboard interface to the interactor
    interactor.AddObserver("KeyPressEvent", keyboard_interface.keypress)

    interactor.Initialize()
    render_window.Render()
    interactor.Start()


if __name__ == '__main__':
    main()
