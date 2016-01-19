# -*- coding: utf-8 -*-
"""
/***************************************************************************
 gaeta
                                 A QGIS plugin
 Gaeta - Geo Analysis & Terrain Animation - Cesium Viewer
                              -------------------
        begin                : 2015-10-31
        git sha              : $Format:%H$
        copyright            : (C) 2015 by GeoDrinX
        email                : geodrinx@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from gaeta_dialog import gaetaDialog
import os.path

import qgis
import codecs

import datetime
import time


import webbrowser


# GDX_Publisher --------------------------------------

def GDX_Publisher(self):


				mapCanvas = self.iface.mapCanvas()

#    dataSource.loadUrl('h ttp://localhost:8000/cesium/Apps/cesiumViewer/temp/gaetaDoc.kml');				

				tempdir = unicode(QFileInfo(QgsApplication.qgisUserDbFilePath()).path()) + "/python/plugins/gaeta/_WebServer/cesium/Apps/cesiumViewer/"
        
				adesso = str(datetime.datetime.now())
				adesso = adesso.replace(" ","_")
				adesso = adesso.replace(":","_")
				adesso = adesso.replace(".","_")        				

#				print "adesso: <%s>\n" %(adesso)

# Prendo le coordinate della finestra attuale---------------------------------------
# 13.5702225179249876,41.2134192420407501 : 13.5768356834183166,41.2182110366311107
				text = mapCanvas.extent().toString()
				text1 = text.replace("," , " ")
				text2 = text1.replace(" : ", ",")
#				the_filter = "bbox($geometry, geomFromWKT ( 'LINESTRING(" + text2 + ")'))"
#				self.doPaste(the_filter) 				

# HERE IT DELETES THE OLD IMAGE ------------------------------------
# (if you comment these, images still remain ...  :)
#				for filename in glob.glob(str(tempdir + '/*.png')) :
#				   os.remove( str(filename) )
#				for filename in glob.glob(str(tempdir + '/*.pngw')) :
#				   os.remove( str(filename) )            
# ------------------------------------------------------------------				

    
				tname = 'ZIPPA'

				out_folder = tempdir
				
				kml = codecs.open(out_folder + '/gaetaDoc.kml', 'w', encoding='utf-8')
#				kml=open(out_folder + '/doc.kml', 'w')
				#

				iface = qgis.utils.iface

				if QGis.QGIS_VERSION_INT <= 120200: 

				   mapRenderer = mapCanvas.mapRenderer()
				   mapRect = mapRenderer.extent()
				   width = mapRenderer.width()
				   height = mapRenderer.height()
				   srs = mapRenderer.destinationCrs()

				   # create output image and initialize it
				   image = QImage(QSize(width, height), QImage.Format_ARGB32)

				   image.fill(0)
				
				   #adjust map canvas (renderer) to the image size and render
				   imagePainter = QPainter(image)
				
				   zoom = 1
				   target_dpi = int(round(zoom * mapRenderer.outputDpi()))				
				
				   mapRenderer.setOutputSize(QSize(width, height), target_dpi)
			
				   mapRenderer.render(imagePainter)
				   imagePainter.end()

				   xN = mapRect.xMinimum()
				   yN = mapRect.yMinimum()

				   nomePNG = ("QGisView_%lf_%lf_%s") % (xN, yN, adesso)
				
				   input_file = out_folder + "/" + nomePNG + ".png"
				
				   #Save the image
				   image.save(input_file, "png")

				else:   # ovvero  QGis.QGIS_VERSION_INT > 120200


           
				   mapRenderer = mapCanvas.mapRenderer()
				   mapRect = mapRenderer.extent()
				   width = mapRenderer.width()
				   height = mapRenderer.height()
				   srs = mapRenderer.destinationCrs()

				   xN = mapRect.xMinimum()
				   yN = mapRect.yMinimum()

				   mapSettings = QgsMapSettings()
				   mapSettings.setMapUnits(0)
				   mapSettings.setExtent(mapRect)
				   DPI = 300
				   mapSettings.setOutputDpi(DPI)

				   mapSettings.setOutputSize(QSize(width, height))

				   lst = []
				   layerTreeRoot = QgsProject.instance().layerTreeRoot()
				   for id in layerTreeRoot.findLayerIds():
				       node = layerTreeRoot.findLayer(id)
				       lst.append(id)
           
				   mapSettings.setLayers(lst)
           
				   mapSettings.setFlags(QgsMapSettings.Antialiasing | QgsMapSettings.UseAdvancedEffects | QgsMapSettings.ForceVectorOutput | QgsMapSettings.DrawLabeling)
				   image = QImage(QSize(width, height), QImage.Format_RGB32)

				   image.fill(0)

				   image.setDotsPerMeterX(DPI / 25.4 * 1000)
				   image.setDotsPerMeterY(DPI / 25.4 * 1000)
				   p = QPainter()
				   p.begin(image)
				   mapRenderer = QgsMapRendererCustomPainterJob(mapSettings, p)
				   mapRenderer.start()
				   mapRenderer.waitForFinished()
				   p.end()

				   nomePNG = ("QGisView_%lf_%lf_%s") % (xN, yN, adesso)
				   input_file = out_folder + "/" + nomePNG + ".png"
				
				   #Save the image
				   image.save(input_file, "png")


				# EndIf     # QGis.QGIS_VERSION_INT > 120200

				layer = mapCanvas.currentLayer()
				crsSrc = srs  # QgsCoordinateReferenceSystem(layer.crs())   # prendere quello attuale
				crsDest = QgsCoordinateReferenceSystem(4326)  # Wgs84LLH
				xform = QgsCoordinateTransform(crsSrc, crsDest)

				x1 = mapRect.xMinimum()
				y1 = mapRect.yMinimum()
				
				x2 = mapRect.xMaximum()
				y2 = mapRect.yMinimum()

				x3 = mapRect.xMaximum()
				y3 = mapRect.yMaximum()

				x4 = mapRect.xMinimum()
				y4 = mapRect.yMaximum()

				xc = (x1 + x3) / 2.
				yc = (y1 + y3) / 2.	

				pt1 = xform.transform(QgsPoint(x1, y1))				
				pt2 = xform.transform(QgsPoint(x2, y2))
				pt3 = xform.transform(QgsPoint(x3, y3))
				pt4 = xform.transform(QgsPoint(x4, y4))                				

				pt5 = xform.transform(QgsPoint(xc, yc))

				xc = pt5.x()
				yc = pt5.y()

				x1 = pt1.x()
				y1 = pt1.y()
				
				x2 = pt2.x()
				y2 = pt2.y()
				
				x3 = pt3.x()
				y3 = pt3.y()
				
				x4 = pt4.x()
				y4 = pt4.y()
				

				
				#Write kml header
				kml.write('<?xml version="1.0" encoding="UTF-8"?>\n')
				kml.write('<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">\n')				
				kml.write('    <Document>\n')
				kml.write('    	 <name>QGisView</name>\n')
				kml.write('    	 <Snippet maxLines="0"></Snippet>\n') 
				loc = ("    	 <description><![CDATA[http://map.project-osrm.org/?loc=%.9lf,%.9lf&ly=1784084387]]></description>\n") %(yc, xc)

				kml.write(loc)
#
				
				
#				kml.write('    	 <description>http://map.project-osrm.org/?hl=it&loc=45.989486,12.778154&loc=45.985624,12.781076&z=16&center=45.984058,12.774417&alt=0&df=0&re=0&ly=-940622518</description>\n')
				
				kml.write('	     <open>1</open>\n')

				kml.write('	     <Style id="sh_ylw-pushpin">\n')
				kml.write('	     	<IconStyle>\n')
				kml.write('	     		<scale>1.2</scale>\n')
				kml.write('	     	</IconStyle>\n')
				kml.write('	     	<PolyStyle>\n')
				kml.write('	     		<fill>0</fill>\n')
				kml.write('	     	</PolyStyle>\n')
				kml.write('	     </Style>\n')
				kml.write('	     <Style id="sn_ylw-pushpin">\n')
				kml.write('	     	<PolyStyle>\n')
				kml.write('	     		<fill>0</fill>\n')
				kml.write('	     	</PolyStyle>\n')
				kml.write('	     </Style>\n')
				kml.write('	     <StyleMap id="msn_ylw-pushpin">\n')
				kml.write('	     	<Pair>\n')
				kml.write('	     		<key>normal</key>\n')
				kml.write('	     		<styleUrl>#sn_ylw-pushpin</styleUrl>\n')
				kml.write('	     	</Pair>\n')
				kml.write('	     	<Pair>\n')
				kml.write('	     		<key>highlight</key>\n')
				kml.write('	     		<styleUrl>#sh_ylw-pushpin</styleUrl>\n')
				kml.write('	     	</Pair>\n')
				kml.write('	     </StyleMap>\n')				
				
				kml.write('	     	<Style id="hl">\n')
				kml.write('	     		<IconStyle>\n')
				kml.write('	     			<scale>0.7</scale>\n')
				kml.write('	     			<Icon>\n')
				kml.write('	     				<href>http://maps.google.com/mapfiles/kml/shapes/placemark_circle_highlight.png</href>\n')
				kml.write('	     			</Icon>\n')
				kml.write('	     		</IconStyle>\n')
				kml.write('	     		<LabelStyle>\n')
				kml.write('	     			<scale>0.7</scale>\n')
				kml.write('	     		</LabelStyle>\n')							
				kml.write('	     		<ListStyle>\n')
				kml.write('	     		</ListStyle>\n')
				kml.write('	     	</Style>\n')
				kml.write('	     	<Style id="default">\n')
				kml.write('	     		<IconStyle>\n')
				kml.write('	     			<scale>0.7</scale>\n')
				kml.write('	     			<Icon>\n')
				kml.write('	     				<href>http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png</href>\n')
				kml.write('	     			</Icon>\n')
				kml.write('	     		</IconStyle>\n')
				kml.write('	     		<LabelStyle>\n')
				kml.write('	     			<scale>0.7</scale>\n')
				kml.write('	     		</LabelStyle>\n')			
				kml.write('	     		<ListStyle>\n')
				kml.write('	     		</ListStyle>\n')
				kml.write('	     	</Style>\n')
				kml.write('	     	<StyleMap id="default0">\n')
				kml.write('	     		<Pair>\n')
				kml.write('	     			<key>normal</key>\n')
				kml.write('	     			<styleUrl>#default</styleUrl>\n')
				kml.write('	     		</Pair>\n')
				kml.write('	     		<Pair>\n')
				kml.write('	     			<key>highlight</key>\n')
				kml.write('	     			<styleUrl>#hl</styleUrl>\n')
				kml.write('	     		</Pair>\n')
				kml.write('	     	</StyleMap>\n')
				
				
				rotazio = 0.0
				if QGis.QGIS_VERSION_INT >= 20801:                
				   rotazio = -(mapCanvas.rotation())
				
				
				kml.write('      <Folder>\n')
				
				xc = (x1 + x3) / 2.
				yc = (y1 + y3) / 2.
				dx = (x3 - x1) * 75000. #100000.


#				kml.write('    		<open>1</open>\n')    
#				kml.write('    		<NetworkLink>\n')
#				kml.write('    		   <name>QGIS_link</name>\n')
#				kml.write('    		   <visibility>1</visibility>\n')
#				kml.write('    		   <open>1</open>\n')
#				kml.write('    		   <Link>\n')
#				kml.write('    		      <href>../_WebServer/QGIS_link.kmz</href>\n')
#				kml.write('    		   </Link>\n')
#				kml.write('    		</NetworkLink>\n')        

        				
				kml.write('    		<LookAt>\n')
				stringazza = ("    		   <longitude>%lf</longitude>\n") %(xc)
				kml.write(stringazza)				
				stringazza = ("    		   <latitude>%lf</latitude>\n") %(yc)
				kml.write(stringazza)				
				kml.write('    		   <altitude>0</altitude>\n')

				stringazza = ("    		   <heading>%lf</heading>\n") %(rotazio)
				kml.write(stringazza)
        
				kml.write('    		   <tilt>0</tilt>\n')
				stringazza = ("    		   <range>%lf</range>\n") %(dx)
				kml.write(stringazza)				
				kml.write('    		   <gx:altitudeMode>relativeToGround</gx:altitudeMode>\n')
				kml.write('    		</LookAt>\n')

				kml.write('      <GroundOverlay>\n')
				kml.write('    	 <name>QGisView</name>\n')
        				
				kml.write('    	<Icon>\n')

#				nomePNG = ("QGisView_%lf_%lf_%s") % (xN, yN, adesso)
				stringazza = ("    	<href>%s.png</href>\n") % (nomePNG)
				kml.write(stringazza)
				kml.write('    		<viewBoundScale>1.0</viewBoundScale>\n')
				kml.write('    	</Icon>\n')
				kml.write('    	<gx:LatLonQuad>\n')
				kml.write('    		<coordinates>\n')

				stringazza =    ("%.9lf,%.9lf,0 %.9lf,%.9lf,0 %.9lf,%.9lf,0 %.9lf,%.9lf,0\n") % (x1, y1, x2, y2, x3, y3, x4, y4)        		
				kml.write(stringazza)				

				kml.write('    		</coordinates>\n')
				kml.write('    	</gx:LatLonQuad>\n')
				kml.write('    </GroundOverlay>\n')

#				#Write kml footer
#				kml.write('</kml>\n')
#				#Close kml file
#				kml.close()



				#Export tfw-file
				xScale = (mapRect.xMaximum() - mapRect.xMinimum()) /  image.width()
				yScale = (mapRect.yMaximum() - mapRect.yMinimum()) /  image.height()

							
				f = open(out_folder + "/" + nomePNG	+ ".pngw", 'w')				
				f.write(str(xScale) + '\n')
				f.write(str(0) + '\n')
				f.write(str(0) + '\n')
				f.write('-' + str(yScale) + '\n')
				f.write(str(mapRect.xMinimum()) + '\n')
				f.write(str(mapRect.yMaximum()) + '\n')
				f.write(str(mapRect.xMaximum()) + '\n')
				f.write(str(mapRect.yMinimum()))				
				f.close()
			

				nomeLay = "gearthview" 	 # foo default name		


#  Adesso scrivo il vettoriale
#  Prendo il sistema di riferimento del Layer selezionato ------------------
        
        
				layer = mapCanvas.currentLayer()
				if layer:
				  if layer.type() == layer.VectorLayer:				

#				    nele = -1
				    name = layer.source();
				    nomeLayer = layer.name()
				    nomeLay   = nomeLayer.replace(" ","_")

				    kml.write('    <Folder>\n')
				    stringazza =   ('			<name>%s</name>\n') % (nomeLay)
				    kml.write (stringazza)     				          
      				    
				    crsSrc = layer.crs();

				    crsDest = QgsCoordinateReferenceSystem(4326)  # Wgs84LLH
				    xform = QgsCoordinateTransform(crsSrc, crsDest)

#----------------------------------------------------------------------------
#  Trasformo la finestra video in coordinate layer, 
#     per estrarre solo gli elementi visibili
#----------------------------------------------------------------------------
#				    mapCanvas = iface.mapCanvas()
				    boundBox = mapCanvas.extent() 
                
				    xMin = float(boundBox.xMinimum())
				    yMin = float(boundBox.yMinimum())

				    xMax = float(boundBox.xMaximum())                
				    yMax = float(boundBox.yMaximum())
				    
				    
				    crs2 = mapCanvas.mapRenderer().destinationCrs()
				    crsSrc2  = QgsCoordinateReferenceSystem(crs2.authid())   
				    crsDest2 = QgsCoordinateReferenceSystem(layer.crs())   
				    xform2   = QgsCoordinateTransform(crsSrc2, crsDest2)
                              
				    pt0 = xform2.transform(QgsPoint(xMin, yMin))
				    pt1 = xform2.transform(QgsPoint(xMax, yMax))
				    
				    rect = QgsRectangle(pt0, pt1)
				    
#----------------------------------------------------------------------------


				    rq = QgsFeatureRequest(rect)

				    iter = layer.getFeatures(rq)				    
				    for feat in iter:
				    
#				      nele = nele + 1
				      nele = feat.id()

# Prendo il contenuto dei campi -------------
#				      fff = feat.fields()
#				      num = fff.count()
#				      for iii in range(num):
#				         print "%s " %(feat[iii])
# -------------------------------------------

# NathanW example code-----------------------------
#				      for feature in layer.getFeatures():
#				         for attr in feature:
#				            print attr
#
#				      for f in layer.pendingFields():
#				         print f.name()
#-------------------------------------------------
              				      
				      # fetch geometry
				      geom = feat.geometry()
				       # show some information about the feature

#				      print ("GeomType: %d") %(geom.type())
				      
				      if geom.type() == QGis.Point:
				        elem = geom.asPoint()
				        x1 = elem.x()
				        y1 = elem.y()

				        pt1 = xform.transform(QgsPoint(x1, y1))

				        kml.write ('	<Placemark>\n')
				        
				        stringazza =   ('		<name>%s</name>\n') % (nele)
				        kml.write (stringazza)	
                			        
				        kml.write ('	<styleUrl>#default0</styleUrl>\n')

# DESCRIPTION DATA-----------
				        kml.write ('	<Snippet maxLines="0"></Snippet>\n')
				        kml.write ('	<description><![CDATA[\n')				        
				        kml.write ('<html><body><table border="1">\n')
				        kml.write ('<tr><th>Field Name</th><th>Field Value</th></tr>\n')
 
 # Prendo il contenuto dei campi -------------
				        fff = feat.fields()
				        num = fff.count()                
				        iii = -1
				        for f in layer.pendingFields(): 				        
				           iii = iii + 1
				           
				           stringazza = ('<tr><td>%s</td><td>%s</td></tr>\n') %(f.name(),feat[iii])

				           kml.write (stringazza)					           
               	
				        kml.write ('</table></body></html>\n')
				        kml.write (']]></description>\n')
				        
# DESCRIPTION DATA-----------

# EXTENDED DATA -------------			
#				        stringazza =   ('		<ExtendedData><SchemaData schemaUrl="#%s">\n') % (nomeLay)
#				        kml.write (stringazza)                 	        
#
##				        stringazza = ('				<SimpleData name="id">%d</SimpleData>\n') %(nele)
##				        kml.write (stringazza)
#
## Prendo il contenuto dei campi -------------
#				        fff = feat.fields()
#				        num = fff.count()                
#				        iii = -1
#				        for f in layer.pendingFields(): 				        
#				           iii = iii + 1
#				           
#				           stringazza = ('				<SimpleData name="%s">%s</SimpleData>\n') %(f.name(),feat[iii])
#
#				           kml.write (stringazza)					           
#                				        
#				        kml.write ('		</SchemaData></ExtendedData>\n')				        
# EXTENDED DATA -------------
				        
				        kml.write ('		<Point>\n')
				        kml.write ('			<gx:drawOrder>1</gx:drawOrder>\n')
				        stringazza =   ('			<coordinates>%.9lf,%.9lf</coordinates>\n') % (pt1.x(), pt1.y())
				        kml.write (stringazza)                                  
				        kml.write ('		</Point>\n')
				        kml.write ('	</Placemark>\n')


				      elif geom.type() == QGis.Line:

				        kml.write ('	<Placemark>\n')
                	
				        stringazza =   ('		<name>%s</name>\n') % (nele)
				        kml.write (stringazza)

# DESCRIPTION DATA-----------
				        kml.write ('	<Snippet maxLines="0"></Snippet>\n')
				        kml.write ('	<description><![CDATA[\n')				        
				        kml.write ('<html><body><table border="1">\n')
				        kml.write ('<tr><th>Field Name</th><th>Field Value</th></tr>\n')
 
 # Prendo il contenuto dei campi -------------
				        fff = feat.fields()
				        num = fff.count()                
				        iii = -1
				        for f in layer.pendingFields(): 				        
				           iii = iii + 1
				           
				           stringazza = ('<tr><td>%s</td><td>%s</td></tr>\n') %(f.name(),feat[iii])

				           kml.write (stringazza)					           
               	
				        kml.write ('</table></body></html>\n')
				        kml.write (']]></description>\n')
				        
# DESCRIPTION DATA-----------
				        
# EXTENDED DATA -------------			
#				        stringazza =   ('		<ExtendedData><SchemaData schemaUrl="#%s">\n') % (nomeLay)
#				        kml.write (stringazza)                 	        
#
##				        stringazza = ('				<SimpleData name="id">%d</SimpleData>\n') %(nele)
##				        kml.write (stringazza)
#
## Prendo il contenuto dei campi -------------
#				        fff = feat.fields()
#				        num = fff.count()                
#				        iii = -1
#				        for f in layer.pendingFields(): 				        
#				           iii = iii + 1
#				           
#				           stringazza = ('				<SimpleData name="%s">%s</SimpleData>\n') %(f.name(),feat[iii])
#
#				           kml.write (stringazza)					           
#                				        
#				        kml.write ('		</SchemaData></ExtendedData>\n')				        
# EXTENDED DATA -------------
                			        
				        kml.write ('		<LineString>\n')
				        kml.write ('			<tessellate>1</tessellate>\n')
				        kml.write ('			<coordinates>\n')
				        
				        elem = geom.asPolyline()
				         
				        for p1 in elem:
				          x1,y1 = p1.x(),p1.y()

				          pt1 = xform.transform(QgsPoint(x1, y1))
                                               
				          stringazza =   ('%.9lf,%.9lf \n') % (pt1.x(), pt1.y())
				          kml.write (stringazza)
				          
				        kml.write ('			</coordinates>\n')                   
				        kml.write ('		</LineString>\n')
				        kml.write ('	</Placemark>\n')


				      elif geom.type() == QGis.Polygon:

				        kml.write ('	<Placemark>\n')
				        stringazza =   ('		<name>%s</name>\n') % (nele)
				        kml.write (stringazza)				        
				        kml.write ('		<styleUrl>#msn_ylw-pushpin</styleUrl>\n')
				        
# DESCRIPTION DATA-----------
				        kml.write ('	<Snippet maxLines="0"></Snippet>\n')
				        kml.write ('	<description><![CDATA[\n')				        
				        kml.write ('<html><body><table border="1">\n')
				        kml.write ('<tr><th>Field Name</th><th>Field Value</th></tr>\n')
 
 # Prendo il contenuto dei campi -------------
				        fff = feat.fields()
				        num = fff.count()                
				        iii = -1
				        for f in layer.pendingFields(): 				        
				           iii = iii + 1
				           
				           stringazza = ('<tr><td>%s</td><td>%s</td></tr>\n') %(f.name(),feat[iii])

				           kml.write (stringazza)					           
               	
				        kml.write ('</table></body></html>\n')
				        kml.write (']]></description>\n')
				        
# DESCRIPTION DATA-----------				        
				        
# EXTENDED DATA -------------			
#				        stringazza =   ('		<ExtendedData><SchemaData schemaUrl="#%s">\n') % (nomeLay)
#				        kml.write (stringazza)                 	        
#
##				        stringazza = ('				<SimpleData name="id">%d</SimpleData>\n') %(nele)
##				        kml.write (stringazza)
#
## Prendo il contenuto dei campi -------------
#				        fff = feat.fields()
#				        num = fff.count()                
#				        iii = -1
#				        for f in layer.pendingFields(): 				        
#				           iii = iii + 1
#				           
#				           stringazza = ('				<SimpleData name="%s">%s</SimpleData>\n') %(f.name(),feat[iii])
#
#				           kml.write (stringazza)					           
#                				        
#				        kml.write ('		</SchemaData></ExtendedData>\n')				        
# EXTENDED DATA -------------
                				        
				        kml.write ('		<Polygon>\n')
				        kml.write ('			<tessellate>1</tessellate>\n')
				        kml.write ('     <outerBoundaryIs>\n')
				        kml.write ('        <LinearRing>\n')
				        kml.write ('         <coordinates>\n')
              
				        elem = geom.asPolygon()

# h ttp://qgis.spatialthoughts.com/2012/11/tip-count-number-of-vertices-in-layer.html				        
				        if geom.isMultipart():
				          print "MULTIPART !!!"
				          elem = geom.asMultiPolygon()

#				          for polygon in elem:
#				             for ring in polygon:
# 				                print ("Pezzo con %d vertici") %(len(ring))

                     
                            			        			        
				        for iii in range (len(elem)):

				          if (iii == 1):				          
				            kml.write ('         </coordinates>\n')
				            kml.write ('         </LinearRing>\n')
				            kml.write ('         </outerBoundaryIs>\n')
				            kml.write ('         <innerBoundaryIs>\n')
				            kml.write ('         <LinearRing>\n')
				            kml.write ('         <coordinates>\n')

				          if (iii > 1):				          
				            kml.write ('         </coordinates>\n')
				            kml.write ('         </LinearRing>\n')
				            kml.write ('         </innerBoundaryIs>\n')
				            kml.write ('         <innerBoundaryIs>\n')
				            kml.write ('         <LinearRing>\n')
				            kml.write ('         <coordinates>\n')	
				        
				          for jjj in range (len(elem[iii])):
				                         
				            x1,y1 = elem[iii][jjj][0], elem[iii][jjj][1]

				            if geom.isMultipart():
				               pt1 = xform.transform(x1)
				            else:				            
				               pt1 = xform.transform(QgsPoint(x1, y1))
                          
				            stringazza =   ('%.9lf,%.9lf,0 \n') % (pt1.x(), pt1.y())
				            kml.write (stringazza)

				        if (iii == 0):
				           kml.write ('         </coordinates>\n')
				           kml.write ('        </LinearRing>\n')
				           kml.write ('     </outerBoundaryIs>\n')
				           kml.write ('   </Polygon>\n')

				        if (iii > 0):
				           kml.write ('         </coordinates>\n')
				           kml.write ('        </LinearRing>\n')
				           kml.write ('     </innerBoundaryIs>\n')
				           kml.write ('   </Polygon>\n')	
                  				        
				        kml.write ('	</Placemark>\n')
				        
				    kml.write ('  </Folder>\n')
					    
				    
				kml.write ('</Folder>\n')

				stringazza = ('<Schema name="%s" id="%s">\n') % (nomeLay, nomeLay)
				kml.write (stringazza)				
				kml.write ('	<SimpleField name="id" type="string"></SimpleField>\n')
				kml.write ('</Schema>\n')		
				
				kml.write ('</Document>\n')        
				kml.write ('</kml>\n')
				kml.close()

# GDX_Publisher2 --------------------------------------

def GDX_Publisher2(self, kml):


				mapCanvas = self.iface.mapCanvas()
				
#				tempdir = unicode(QFileInfo(QgsApplication.qgisUserDbFilePath()).path()) + "/python/plugins/gearthview/temp"
				tempdir = unicode(QFileInfo(QgsApplication.qgisUserDbFilePath()).path()) + "/python/plugins/gaeta/_WebServer/cesium/Apps/cesiumViewer/"

				adesso = str(datetime.datetime.now())
				adesso = adesso.replace(" ","_")
				adesso = adesso.replace(":","_")
				adesso = adesso.replace(".","_")        				


				text = mapCanvas.extent().toString()
				text1 = text.replace("," , " ")
				text2 = text1.replace(" : ", ",")
			

# HERE IT DELETES THE OLD IMAGE ------------------------------------
# (if you comment these, images still remain ...  :)
#				for filename in glob.glob(str(tempdir + '/*.png')) :
#				   os.remove( str(filename) )
#				for filename in glob.glob(str(tempdir + '/*.pngw')) :
#				   os.remove( str(filename) )            
# ------------------------------------------------------------------				

    
				tname = 'ZIPPA'

				out_folder = tempdir
				

				iface = qgis.utils.iface

				mapRenderer = mapCanvas.mapRenderer()
				mapRect = mapRenderer.extent()
				width = mapRenderer.width()
				height = mapRenderer.height()
				srs = mapRenderer.destinationCrs()

				# create output image and initialize it
				image = QImage(QSize(width, height), QImage.Format_ARGB32)
				image.fill(0)
				
				#adjust map canvas (renderer) to the image size and render
				imagePainter = QPainter(image)
				
				zoom = 1
				target_dpi = int(round(zoom * mapRenderer.outputDpi()))				
				
				mapRenderer.setOutputSize(QSize(width, height), target_dpi)
			
				mapRenderer.render(imagePainter)
				imagePainter.end()

				xN = mapRect.xMinimum()
				yN = mapRect.yMinimum()

				nomePNG = ("QGisView_%lf_%lf_%s") % (xN, yN, adesso)
				
				input_file = out_folder + "/" + nomePNG + ".png"
				
				#Save the image
				image.save(input_file, "png")

				layer = mapCanvas.currentLayer()
				crsSrc = srs  # QgsCoordinateReferenceSystem(layer.crs())   # prendere quello attuale
				crsDest = QgsCoordinateReferenceSystem(4326)  # Wgs84LLH
				xform = QgsCoordinateTransform(crsSrc, crsDest)


				x1 = mapRect.xMinimum()
				y1 = mapRect.yMinimum()
				
				x2 = mapRect.xMaximum()
				y2 = mapRect.yMinimum()

				x3 = mapRect.xMaximum()
				y3 = mapRect.yMaximum()

				x4 = mapRect.xMinimum()
				y4 = mapRect.yMaximum()

				xc = (x1 + x3) / 2.
				yc = (y1 + y3) / 2.	

				pt1 = xform.transform(QgsPoint(x1, y1))				
				pt2 = xform.transform(QgsPoint(x2, y2))
				pt3 = xform.transform(QgsPoint(x3, y3))
				pt4 = xform.transform(QgsPoint(x4, y4))                				

				pt5 = xform.transform(QgsPoint(xc, yc))

				xc = pt5.x()
				yc = pt5.y()

				x1 = pt1.x()
				y1 = pt1.y()
				
				x2 = pt2.x()
				y2 = pt2.y()
				
				x3 = pt3.x()
				y3 = pt3.y()
				
				x4 = pt4.x()
				y4 = pt4.y()
				
				kml = ""
				
				#Write kml header
				
#				kml = kml + ('<?xml version="1.0" encoding="UTF-8"?>\n')
#				kml = kml + ('<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">\n')				
#				kml = kml + ('    <Document>\n')
#				kml = kml + ('    	 <name>QGisView</name>\n')
#				kml = kml + ('    	 <Snippet maxLines="0"></Snippet>\n') 
#				loc = ("    	 <description><![CDATA[http://map.project-osrm.org/?loc=%.9lf,%.9lf&ly=1784084387]]></description>\n") %(yc, xc)
#				kml = kml + (loc)
#				kml = kml + ('	     <open>0</open>\n')

#				kml = kml + ('	     <Style id="sh_ylw-pushpin">\n')
#				kml = kml + ('	     	<IconStyle>\n')
#				kml = kml + ('	     		<scale>1.2</scale>\n')
#				kml = kml + ('	     	</IconStyle>\n')
#				kml = kml + ('	     	<PolyStyle>\n')
#				kml = kml + ('	     		<fill>0</fill>\n')
#				kml = kml + ('	     	</PolyStyle>\n')
#				kml = kml + ('	     </Style>\n')
#				kml = kml + ('	     <Style id="sn_ylw-pushpin">\n')
#				kml = kml + ('	     	<PolyStyle>\n')
#				kml = kml + ('	     		<fill>0</fill>\n')
#				kml = kml + ('	     	</PolyStyle>\n')
#				kml = kml + ('	     </Style>\n')
#				kml = kml + ('	     <StyleMap id="msn_ylw-pushpin">\n')
#				kml = kml + ('	     	<Pair>\n')
#				kml = kml + ('	     		<key>normal</key>\n')
#				kml = kml + ('	     		<styleUrl>#sn_ylw-pushpin</styleUrl>\n')
#				kml = kml + ('	     	</Pair>\n')
#				kml = kml + ('	     	<Pair>\n')
#				kml = kml + ('	     		<key>highlight</key>\n')
#				kml = kml + ('	     		<styleUrl>#sh_ylw-pushpin</styleUrl>\n')
#				kml = kml + ('	     	</Pair>\n')
#				kml = kml + ('	     </StyleMap>\n')				
#				
#				kml = kml + ('	     	<Style id="hl">\n')
#				kml = kml + ('	     		<IconStyle>\n')
#				kml = kml + ('	     			<scale>0.7</scale>\n')
#				kml = kml + ('	     			<Icon>\n')
#				kml = kml + ('	     				<href>http://maps.google.com/mapfiles/kml/shapes/placemark_circle_highlight.png</href>\n')
#				kml = kml + ('	     			</Icon>\n')
#				kml = kml + ('	     		</IconStyle>\n')
#				kml = kml + ('	     		<LabelStyle>\n')
#				kml = kml + ('	     			<scale>0.7</scale>\n')
#				kml = kml + ('	     		</LabelStyle>\n')							
#				kml = kml + ('	     		<ListStyle>\n')
#				kml = kml + ('	     		</ListStyle>\n')
#				kml = kml + ('	     	</Style>\n')
#				kml = kml + ('	     	<Style id="default">\n')
#				kml = kml + ('	     		<IconStyle>\n')
#				kml = kml + ('	     			<scale>0.7</scale>\n')
#				kml = kml + ('	     			<Icon>\n')
#				kml = kml + ('	     				<href>http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png</href>\n')
#				kml = kml + ('	     			</Icon>\n')
#				kml = kml + ('	     		</IconStyle>\n')
#				kml = kml + ('	     		<LabelStyle>\n')
#				kml = kml + ('	     			<scale>0.7</scale>\n')
#				kml = kml + ('	     		</LabelStyle>\n')			
#				kml = kml + ('	     		<ListStyle>\n')
#				kml = kml + ('	     		</ListStyle>\n')
#				kml = kml + ('	     	</Style>\n')
#				kml = kml + ('	     	<StyleMap id="default0">\n')
#				kml = kml + ('	     		<Pair>\n')
#				kml = kml + ('	     			<key>normal</key>\n')
#				kml = kml + ('	     			<styleUrl>#default</styleUrl>\n')
#				kml = kml + ('	     		</Pair>\n')
#				kml = kml + ('	     		<Pair>\n')
#				kml = kml + ('	     			<key>highlight</key>\n')
#				kml = kml + ('	     			<styleUrl>#hl</styleUrl>\n')
#				kml = kml + ('	     		</Pair>\n')
#				kml = kml + ('	     	</StyleMap>\n')
				
				
#				kml = kml + ('      <Folder>\n')
				
				xc = (x1 + x3) / 2.
				yc = (y1 + y3) / 2.
				dx = (x3 - x1) * 75000. #100000.
        				
#				kml = kml + ('    		<LookAt>\n')
#				stringazza = ("    		   <longitude>%lf</longitude>\n") %(xc)
#				kml = kml + (stringazza)				
#				stringazza = ("    		   <latitude>%lf</latitude>\n") %(yc)
#				kml = kml + (stringazza)				
#				kml = kml + ('    		   <altitude>0</altitude>\n')
#				kml = kml + ('    		   <heading>0.00</heading>\n')
#				kml = kml + ('    		   <tilt>0</tilt>\n')
#				stringazza = ("    		   <range>%lf</range>\n") %(dx)
#				kml = kml + (stringazza)				
#				kml = kml + ('    		   <gx:altitudeMode>relativeToGround</gx:altitudeMode>\n')
#				kml = kml + ('    		</LookAt>\n')

#				kml = kml + ('      <GroundOverlay>\n')
#				kml = kml + ('    	 <name>QGisView</name>\n')
        				
#				kml = kml + ('    	<Icon>\n')

#				stringazza = ("    	<href>%s.png</href>\n") % (nomePNG)
#				kml = kml + (stringazza)
#				kml = kml + ('    		<viewBoundScale>1.0</viewBoundScale>\n')
#				kml = kml + ('    	</Icon>\n')
#				kml = kml + ('    	<gx:LatLonQuad>\n')
#				kml = kml + ('    		<coordinates>\n')

#				stringazza =    ("%.9lf,%.9lf,0 %.9lf,%.9lf,0 %.9lf,%.9lf,0 %.9lf,%.9lf,0\n") % (x1, y1, x2, y2, x3, y3, x4, y4)        		
#				kml = kml + (stringazza)				

#				kml = kml + ('    		</coordinates>\n')
#				kml = kml + ('    	</gx:LatLonQuad>\n')
#				kml = kml + ('    </GroundOverlay>\n')

#				#Write kml footer
#				kml = kml + ('</kml>\n')
#				#Close kml file
#				kml.close()



				#Export tfw-file
#				xScale = (mapRect.xMaximum() - mapRect.xMinimum()) /  image.width()
#				yScale = (mapRect.yMaximum() - mapRect.yMinimum()) /  image.height()

							
#				f = open(out_folder + "/" + nomePNG	+ ".pngw", 'w')				
#				f.write(str(xScale) + '\n')
#				f.write(str(0) + '\n')
#				f.write(str(0) + '\n')
#				f.write('-' + str(yScale) + '\n')
#				f.write(str(mapRect.xMinimum()) + '\n')
#				f.write(str(mapRect.yMaximum()) + '\n')
#				f.write(str(mapRect.xMaximum()) + '\n')
#				f.write(str(mapRect.yMinimum()))				
#				f.close()
			

				nomeLay = "gearthview" 	 # foo default name		


#  Adesso scrivo il vettoriale
#  Prendo il sistema di riferimento del Layer selezionato ------------------
        
        
				layer = mapCanvas.currentLayer()
				if layer:
				  if layer.type() == layer.VectorLayer:				

				    name = layer.source();
				    nomeLayer = layer.name()
				    nomeLay   = nomeLayer.replace(" ","_")

				    kml = kml + ('    <Folder>\n')
				    stringazza =   ('			<name>%s</name>\n') % (nomeLay)
				    kml = kml +  (stringazza)     				          
      				    
				    crsSrc = layer.crs();

				    crsDest = QgsCoordinateReferenceSystem(4326)  # Wgs84LLH
				    xform = QgsCoordinateTransform(crsSrc, crsDest)


				    boundBox = mapCanvas.extent() 
                
				    xMin = float(boundBox.xMinimum())
				    yMin = float(boundBox.yMinimum())

				    xMax = float(boundBox.xMaximum())                
				    yMax = float(boundBox.yMaximum())
				    
				    
				    crs2 = mapCanvas.mapRenderer().destinationCrs()
				    crsSrc2  = QgsCoordinateReferenceSystem(crs2.authid())   
				    crsDest2 = QgsCoordinateReferenceSystem(layer.crs())   
				    xform2   = QgsCoordinateTransform(crsSrc2, crsDest2)
                              
				    pt0 = xform2.transform(QgsPoint(xMin, yMin))
				    pt1 = xform2.transform(QgsPoint(xMax, yMax))
				    
				    rect = QgsRectangle(pt0, pt1)
				    


				    rq = QgsFeatureRequest(rect)

				    iter = layer.getFeatures(rq)				    
				    for feat in iter:
				    
				      nele = feat.id()

              				      
				      # fetch geometry
				      geom = feat.geometry()
				       # show some information about the feature

#				      print ("GeomType: %d") %(geom.type())
				      
				      if geom.type() == QGis.Point:
				        elem = geom.asPoint()
				        x1 = elem.x()
				        y1 = elem.y()

				        pt1 = xform.transform(QgsPoint(x1, y1))

				        kml = kml +  ('	<Placemark>\n')
				        
				        stringazza =   ('		<name>%s</name>\n') % (nele)
				        kml = kml +  (stringazza)	
                			        
				        kml = kml +  ('	<styleUrl>#default0</styleUrl>\n')

# DESCRIPTION DATA-----------
				        kml = kml +  ('	<Snippet maxLines="0"></Snippet>\n')
				        kml = kml +  ('	<description><![CDATA[\n')				        
				        kml = kml +  ('<html><body><table border="1">\n')
				        kml = kml +  ('<tr><th>Field Name</th><th>Field Value</th></tr>\n')
 
 # Prendo il contenuto dei campi -------------
				        fff = feat.fields()
				        num = fff.count()                
				        iii = -1
				        for f in layer.pendingFields(): 				        
				           iii = iii + 1
				           
				           stringazza = ('<tr><td>%s</td><td>%s</td></tr>\n') %(f.name(),feat[iii])

				           kml = kml +  (stringazza)					           
               	
				        kml = kml +  ('</table></body></html>\n')
				        kml = kml +  (']]></description>\n')
				        
# DESCRIPTION DATA-----------

				        
				        kml = kml +  ('		<Point>\n')
				        kml = kml +  ('			<gx:drawOrder>1</gx:drawOrder>\n')
				        stringazza =   ('			<coordinates>%.9lf,%.9lf</coordinates>\n') % (pt1.x(), pt1.y())
				        kml = kml +  (stringazza)                                  
				        kml = kml +  ('		</Point>\n')
				        kml = kml +  ('	</Placemark>\n')


				      elif geom.type() == QGis.Line:

				        kml = kml +  ('	<Placemark>\n')
                	
				        stringazza =   ('		<name>%s</name>\n') % (nele)
				        kml = kml +  (stringazza)

# DESCRIPTION DATA-----------
				        kml = kml +  ('	<Snippet maxLines="0"></Snippet>\n')
				        kml = kml +  ('	<description><![CDATA[\n')				        
				        kml = kml +  ('<html><body><table border="1">\n')
				        kml = kml +  ('<tr><th>Field Name</th><th>Field Value</th></tr>\n')
 
 # Prendo il contenuto dei campi -------------
				        fff = feat.fields()
				        num = fff.count()                
				        iii = -1
				        for f in layer.pendingFields(): 				        
				           iii = iii + 1
				           
				           stringazza = ('<tr><td>%s</td><td>%s</td></tr>\n') %(f.name(),feat[iii])

				           kml = kml +  (stringazza)					           
               	
				        kml = kml +  ('</table></body></html>\n')
				        kml = kml +  (']]></description>\n')
				        
				                        			        
				        kml = kml +  ('		<LineString>\n')
				        kml = kml +  ('			<tessellate>1</tessellate>\n')
				        kml = kml +  ('			<coordinates>\n')
				        
				        elem = geom.asPolyline()
				         
				        for p1 in elem:
				          x1,y1 = p1.x(),p1.y()

				          pt1 = xform.transform(QgsPoint(x1, y1))
                                               
				          stringazza =   ('%.9lf,%.9lf \n') % (pt1.x(), pt1.y())
				          kml = kml +  (stringazza)
				          
				        kml = kml +  ('			</coordinates>\n')                   
				        kml = kml +  ('		</LineString>\n')
				        kml = kml +  ('	</Placemark>\n')


				      elif geom.type() == QGis.Polygon:

				        kml = kml +  ('	<Placemark>\n')
				        stringazza =   ('		<name>%s</name>\n') % (nele)
				        kml = kml +  (stringazza)				        
				        kml = kml +  ('		<styleUrl>#msn_ylw-pushpin</styleUrl>\n')
				        
# DESCRIPTION DATA-----------
				        kml = kml +  ('	<Snippet maxLines="0"></Snippet>\n')
				        kml = kml +  ('	<description><![CDATA[\n')				        
				        kml = kml +  ('<html><body><table border="1">\n')
				        kml = kml +  ('<tr><th>Field Name</th><th>Field Value</th></tr>\n')
 
 # Prendo il contenuto dei campi -------------
				        fff = feat.fields()
				        num = fff.count()                
				        iii = -1
				        for f in layer.pendingFields(): 				        
				           iii = iii + 1
				           
				           stringazza = ('<tr><td>%s</td><td>%s</td></tr>\n') %(f.name(),feat[iii])

				           kml = kml +  (stringazza)					           
               	
				        kml = kml +  ('</table></body></html>\n')
				        kml = kml +  (']]></description>\n')
				        
# DESCRIPTION DATA-----------				        
				        
                				        
				        kml = kml +  ('		<Polygon>\n')
				        kml = kml +  ('			<tessellate>1</tessellate>\n')
				        kml = kml +  ('     <outerBoundaryIs>\n')
				        kml = kml +  ('        <LinearRing>\n')
				        kml = kml +  ('         <coordinates>\n')
              
				        elem = geom.asPolygon()

# h ttp://qgis.spatialthoughts.com/2012/11/tip-count-number-of-vertices-in-layer.html				        
				        if geom.isMultipart():
				          print "MULTIPART !!!"
				          elem = geom.asMultiPolygon()

				          for polygon in elem:
				             for ring in polygon:
				                print ("Pezzo con %d vertici") %(len(ring))

                     
                            			        			        
				        for iii in range (len(elem)):

				          if (iii == 1):				          
				            kml = kml +  ('         </coordinates>\n')
				            kml = kml +  ('         </LinearRing>\n')
				            kml = kml +  ('         </outerBoundaryIs>\n')
				            kml = kml +  ('         <innerBoundaryIs>\n')
				            kml = kml +  ('         <LinearRing>\n')
				            kml = kml +  ('         <coordinates>\n')

				          if (iii > 1):				          
				            kml = kml +  ('         </coordinates>\n')
				            kml = kml +  ('         </LinearRing>\n')
				            kml = kml +  ('         </innerBoundaryIs>\n')
				            kml = kml +  ('         <innerBoundaryIs>\n')
				            kml = kml +  ('         <LinearRing>\n')
				            kml = kml +  ('         <coordinates>\n')	
				        
				          for jjj in range (len(elem[iii])):
				                         
				            x1,y1 = elem[iii][jjj][0], elem[iii][jjj][1]

				            if geom.isMultipart():
				               pt1 = xform.transform(x1)
				            else:				            
				               pt1 = xform.transform(QgsPoint(x1, y1))
                          
				            stringazza =   ('%.9lf,%.9lf,0 \n') % (pt1.x(), pt1.y())
				            kml = kml +  (stringazza)

				        if (iii == 0):
				           kml = kml +  ('         </coordinates>\n')
				           kml = kml +  ('        </LinearRing>\n')
				           kml = kml +  ('     </outerBoundaryIs>\n')
				           kml = kml +  ('   </Polygon>\n')

				        if (iii > 0):
				           kml = kml +  ('         </coordinates>\n')
				           kml = kml +  ('        </LinearRing>\n')
				           kml = kml +  ('     </innerBoundaryIs>\n')
				           kml = kml +  ('   </Polygon>\n')	
                  				        
				        kml = kml +  ('	</Placemark>\n')
				        
				    kml = kml +  ('  </Folder>\n')
					    
				    
#				kml = kml +  ('</Folder>\n')

#				stringazza = ('<Schema name="%s" id="%s">\n') % (nomeLay, nomeLay)
#				kml = kml +  (stringazza)				
#				kml = kml +  ('	<SimpleField name="id" type="string"></SimpleField>\n')
#				kml = kml +  ('</Schema>\n')		
				
#				kml = kml +  ('</Document>\n')        
#				kml = kml +  ('</kml>\n')
				
				
#				kmlFile = codecs.open(out_folder + '/doc.kml', 'w', encoding='utf-8')
#				kmlFile.write(kml)			
#				kmlFile.close()

#				print  'Content-Type: application/vnd.google-earth.kml+xml\n'
				return				

class gaeta:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value("locale/userLocale")[0:2]
        localePath = os.path.join(self.plugin_dir, 'i18n', 'gaeta_{}.qm'.format(locale))

        if os.path.exists(localePath):
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = gaetaDialog()

    def initGui(self):
        # Create action that will start plugin configuration
        self.action = QAction(
            QIcon(":/plugins/gaeta/icon.png"),
            u"gaeta", self.iface.mainWindow())
        # connect the action to the run method
        self.action.triggered.connect(self.run)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu(u"&gaeta", self.action)

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(u"&gaeta", self.action)
        self.iface.removeToolBarIcon(self.action)

    # run method that performs all the real work
    def run(self):

				tempdir = unicode(QFileInfo(QgsApplication.qgisUserDbFilePath()).path()) + "/python/plugins/gaeta/_WebServer/cesium/Apps/cesiumViewer/"
				

#  Adesso scrivo il vettoriale
#  Prendo il sistema di riferimento del Layer selezionato ------------------
        
        
				layer = self.iface.mapCanvas().currentLayer()
				if layer:
				  if layer.type() == layer.VectorLayer:				

				    name = layer.source();
				    nomeLayer = layer.name()
				    nomeLay   = nomeLayer.replace(" ","_")

				    numFeatures = layer.featureCount()
				    print ("numFeatures %d") %(numFeatures)
    				          
      				    
				    crsSrc = layer.crs();

				    crsDest = QgsCoordinateReferenceSystem(4326)  # Wgs84LLH
				    xform = QgsCoordinateTransform(crsSrc, crsDest)

#----------------------------------------------------------------------------
#  Trasformo la finestra video in coordinate layer, 
#     per estrarre solo gli elementi visibili
#----------------------------------------------------------------------------
				    iface = qgis.utils.iface
				    
				    boundBox = iface.mapCanvas().extent() 
                
				    xMin = float(boundBox.xMinimum())
				    yMin = float(boundBox.yMinimum())

				    xMax = float(boundBox.xMaximum())                
				    yMax = float(boundBox.yMaximum())
				    
				    
				    crs2 = self.iface.mapCanvas().mapRenderer().destinationCrs()
				    crsSrc2  = QgsCoordinateReferenceSystem(crs2.authid())   
				    crsDest2 = QgsCoordinateReferenceSystem(layer.crs())   
				    xform2   = QgsCoordinateTransform(crsSrc2, crsDest2)
                              
				    pt0 = xform2.transform(QgsPoint(xMin, yMin))
				    pt1 = xform2.transform(QgsPoint(xMax, yMax))
				    
				    rect = QgsRectangle(pt0, pt1)
				    
#----------------------------------------------------------------------------

				    rq = QgsFeatureRequest(rect)

				    iter = layer.getFeatures(rq)
            
#  CONTEGGIO gli elementi da esportare -----------------------

				    nele = 0
				    for feat in iter:
				        nele = nele + 1

#  RICARICO la geometria ---------------------------------------		    
				    iter = layer.getFeatures(rq)

# ---------------------------------------------------------------------------				
#    INIZIO scrittura  KML 
# ---------------------------------------------------------------------------

				    out_folder = tempdir
				
#				    kml = codecs.open(out_folder + '/gaetaDoc.kml', 'w', encoding='utf-8')

				    #Write the KML
            
#				    kmlString = ""
            
				    GDX_Publisher(self)

#				    kml.write(kmlString)

#				    kml.close()


# ---------------------------------------------------------------------------				
#    FINE scrittura    KML 
# ---------------------------------------------------------------------------



# ---------------------------------------------------------------------------
#    INIZIO scrittura  geoJSON 
# ---------------------------------------------------------------------------

#				    out_folder = tempdir
#				
#				    kml = codecs.open(out_folder + '/gaetaDoc.geojson', 'w', encoding='utf-8')
#
				    ##Write the geoJson header
#
				    #kml.write('{\n')
				    #kml.write('"type": "FeatureCollection",\n')
				    #kml.write('"crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } },\n') 
				    #kml.write('\n')
#
				    #kml.write('"features": [')
#				    
#				    numE = 0
#				    for feat in iter:
#
				        #numE = numE + 1
#                				        		      
				        ## Leggo la geometria dell'elemento
#				      
#				        geom = feat.geometry()
#				      
#				        kml.write ('\n{ "type": "Feature", ')
#                 
## DESCRIPTION DATA-----------
				        			        #
				        #kml.write ('"properties": {')
#
# 
# # Prendo il contenuto dei campi -------------
				        #fff = feat.fields()
				        #num = fff.count()
				        #print num
				        #iii = -1
				        #for f in layer.pendingFields(): 				        
#				           iii = iii + 1			           
#				           stringazza = (' "%s": "%s"') %(f.name(),feat[iii]) # QUA c'è una virgola di troppo
#				           kml.write (stringazza)
#				           if(iii < num-1):
#				              kml.write (',')
#				        kml.write (' }, ')
#
##  Scrivo la geometria dell'elemento corrente ------------
				        #kml.write ('"geometry": ')		        
				        #stringazza =  geom.exportToGeoJSON()
				        #kml.write (stringazza)
#				        
#				        kml.write (' } ')
#
				        #if (numE < nele):
#				              kml.write (',')
#
				        #
				    ##----- Fine Ciclo Elementi da esportare
#				    
#
				    #kml.write (']\n')
				    #kml.write ('}\n')
#
				    #kml.close()
## ---------------------------------------------------------------------------				
##    FINE scrittura  geoJSON 
## ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------				
#    INIZIO scrittura  czml 
# ---------------------------------------------------------------------------


#  Adesso scrivo il vettoriale
#  Prendo il sistema di riferimento del Layer selezionato ------------------
        
        
#				layer = self.iface.mapCanvas().currentLayer()
#				if layer:
#				  if layer.type() == layer.VectorLayer:				
#
#				    out_folder = tempdir
#				
#				    kml = codecs.open(out_folder + '/gaetaDoc.czml', 'w', encoding='utf-8')
#
#				    #Write the czml header

#				    kml.write('[{\n')
#				    kml.write('        "id" : "document",\n')
#				    kml.write('        "version" : "1.0"\n')
#				    kml.write('    }, {\n\n')

#				    rq = QgsFeatureRequest(rect)

#				    iter = layer.getFeatures(rq)
            
#  CICLO per ogni elemento da esportare -----------------------
				    
#				    for feat in iter:
				    
#				      nele = feat.id()
              				      
#				      # fetch geometry
#				      geom = feat.geometry()
#				       # show some information about the feature
#				      
#				      if geom.type() == QGis.Point:
#
				        #kml.write ('    "point":{	\n')			        
#
#
				      #elif geom.type() == QGis.Line:
#
				        #kml.write ('    "line":{\n')
#
#
#
				      #elif geom.type() == QGis.Polygon:
#
				        #kml.write ('    "polygon":{\n')
				        #kml.write ('      "positions":{\n')
				        #kml.write ('        "cartographicDegrees":[\n          ')
#				        
#				        elem = geom.asPolygon()
#
				        #for iii in range (len(elem)):
#
##				          if (iii == 1):				          
##				            kml.write ('         </coordinates>\n')
##				            kml.write ('         </LinearRing>\n')
##				            kml.write ('         </outerBoundaryIs>\n')
##				            kml.write ('         <innerBoundaryIs>\n')
##				            kml.write ('         <LinearRing>\n')
##				            kml.write ('         <coordinates>\n')
##
##				          if (iii > 1):				          
##				            kml.write ('         </coordinates>\n')
##				            kml.write ('         </LinearRing>\n')
##				            kml.write ('         </innerBoundaryIs>\n')
##				            kml.write ('         <innerBoundaryIs>\n')
##				            kml.write ('         <LinearRing>\n')
##				            kml.write ('         <coordinates>\n')
	#
#				          npunti = len(elem[iii])
#
				          #np = -1
#				          
#				          for jjj in range (len(elem[iii])):
#				                         
#				            x1,y1 = elem[iii][jjj][0], elem[iii][jjj][1]
#				            
#				            pt1 = xform.transform(QgsPoint(x1, y1))
#                           
				            #stringazza =   ('%.9lf,%.9lf,0') % (pt1.x(), pt1.y())
				            #kml.write (stringazza)
#				            
#				            np = np + 1
#				            
#				            if (np < npunti-1):
#				              kml.write (',')				            
#
##				        if (iii == 0):
##				           kml.write ('         </coordinates>\n')
##				           kml.write ('        </LinearRing>\n')
##				           kml.write ('     </outerBoundaryIs>\n')
##				           kml.write ('   </Polygon>\n')
##
##				        if (iii > 0):
##				           kml.write ('         </coordinates>\n')
##				           kml.write ('        </LinearRing>\n')
##				           kml.write ('     </innerBoundaryIs>\n')
##				           kml.write ('   </Polygon>\n')
	#
#				        kml.write ('\n        ]\n')
#
				        #kml.write ('      },\n')
				        #kml.write ('      "material":{\n')
				        #kml.write ('        "solidColor":{\n')
				        #kml.write ('          "color":{\n')
				        #kml.write ('            "rgba":[\n')
				        #kml.write ('              255,0,0,77\n')
				        #kml.write ('            ]\n')
				        #kml.write ('          }\n')
				        #kml.write ('        }\n')
				        #kml.write ('      },\n')
				        #kml.write ('      "fill":true,\n')
				        #kml.write ('      "outline":true,\n')
				        #kml.write ('      "outlineColor":{\n')
				        #kml.write ('        "rgba":[\n')
				        #kml.write ('          255,0,0,255\n')
				        #kml.write ('        ]\n')
				        #kml.write ('      }\n')
				        #kml.write ('    }\n')
#				        
#				    #----- Fine Ciclo Elementi da esportare
#				    
#
				    #kml.write ('  }]\n')
#
				    #kml.close()



#				webbrowser.open_new("http://localhost:8000/cesium/Apps/cesiumViewer/index.html")
				webbrowser.open("http://localhost:8000/cesium/Apps/cesiumViewer/index.html", new=0, autoraise=True)        

#				if sys.platform[:3] == "win":
#				    class WindowsDefault(BaseBrowser):
#				        def open(self, url, new=0, autoraise=True):
#				            try:
#				                os.startfile(url)
