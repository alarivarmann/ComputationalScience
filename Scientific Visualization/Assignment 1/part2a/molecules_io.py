"""This module provides functions for reading molecule positions,
radii, and connections from ASCII files.

Written by: Filip Malmberg
Modified by: Erik Vidholm and Johan Nysjo

"""

import os
import string
import vtk


def read_points(filename):
    """Reads molecule coordinates from an ASCII file."""
    points = vtk.vtkPoints()
    text_file = open(filename)
    line = text_file.readline()
    while line:
        data = string.split(line)
        if data and data[0] != '#':
            x, y, z = float(data[0]), float(data[1]), float(data[2])
            points.InsertNextPoint(x, y, z)
        line = text_file.readline()
    text_file.close()
    return points


def read_scalars(filename):
    """Reads molecule radii (scalars) from an ASCII file."""
    scalars = vtk.vtkFloatArray()
    text_file = open(filename)
    line = text_file.readline()
    while line:
        data = string.split(line)
        if data and data[0] != '#':
            x = float(data[0])
            scalars.InsertNextValue(x)
        line = text_file.readline()
    text_file.close()
    return scalars


def read_connections(filename):
    """Reads molecule connections from an ASCII file."""
    connections = vtk.vtkCellArray()
    text_file = open(filename)
    line = text_file.readline()
    while line:
        data = string.split(line)
        if data and data[0] != '#':
            a, b = int(data[0]), int(data[1])
            connections.InsertNextCell(2)
            connections.InsertCellPoint(a)
            connections.InsertCellPoint(b)
        line = text_file.readline()
    text_file.close()
    return connections
