"""PyQGIS scripts for manipulting spatial data."""

from qgis.core import QgsProject, QgsDataSourceURI, QgsVectorLayer, QgsMapLayerRegistry
from PyQt4.QtCore import QFileInfo

project = QgsProject.instance()

print(project.fileName())

project.write(QFileInfo('../models/GIS_data/gerrypy.qgs'))

print(project.fileName())

#Add vector data

uri = QgsDataSourceURI()

uri.setConnection("localhost", "5432", "gisdb", "julienawilson", "postword!!")
uri.setDataSource("public", "colorado_tracts", "geom") #This can take an option filter argument

CO_tracts = QgsVectorLayer(uri.uri(False), "CO_tracts", "postgres")

if not CO_tracts:
    print("Layer failed to load!")
else:
    print("it worked!")

print(CO_tracts.fields())
for field in CO_tracts.fields():
    print(field.name())

QgsMapLayerRegistry.instance().addMapLayer(CO_tracts)
print(QgsMapLayerRegistry.instance().mapLayers())
