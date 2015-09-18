import vtk

square = vtk.vtkCubeSource()
mapper = vtk.vtkPolyDataMapper()
mapper.SetInput(square.GetOutput())

legendBox = vtk.vtkLegendBoxActor()
legendBox.SetNumberOfEntries(1)


legendBox.SetEntry(0, square.GetOutput(), "Test", [1,1,0])
ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
ren.AddActor(legendBox)

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin);

renWin.Render()
iren.Start()
