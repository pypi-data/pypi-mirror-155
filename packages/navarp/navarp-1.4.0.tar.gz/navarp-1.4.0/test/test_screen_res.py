# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 10:35:38 2019

@author: fbisti
"""

import sys
from PyQt5 import QtWidgets

app = QtWidgets.QApplication(sys.argv)

screen = app.primaryScreen()
print('Screen: %s' % screen.name())
size = screen.size()
print('Size: %d x %d' % (size.width(), size.height()))
rect = screen.availableGeometry()
print('Available: %d x %d' % (rect.width(), rect.height()))