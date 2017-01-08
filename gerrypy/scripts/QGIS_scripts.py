"""PyQGIS scripts for manipulting spatial data."""

# from qgis.core import QgsProject
from PyQt4.QtCore import QFileInfo

project = QgsProject.instance()

print(project.fileName)

project.write(QFileInfo('../models/GIS_data/gerrypy.qgs'))

print(project.fileName)
