# -*- coding: utf-8 -*-
"""
/***************************************************************************
 gaeta
                                 A QGIS plugin
 Gaeta - Geo Analysis & Terrain Animation - Cesium Viewer
                             -------------------
        begin                : 2015-10-31
        copyright            : (C) 2015 by GeoDrinX
        email                : geodrinx@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load gaeta class from file gaeta.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .gaeta import gaeta
    return gaeta(iface)
