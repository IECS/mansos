# -*- coding: utf-8 -*-
#
# Copyright (c) 2008-2012 the MansOS team. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#  * Redistributions of source code must retain the above copyright notice,
#    this list of  conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

import wx
import wx.lib.scrolledpanel as scrolled
import Editor
import os
import globals as g

class EditorManager(scrolled.ScrolledPanel):
    def __init__(self, parent, API, emmbeddedMode = False):
        scrolled.ScrolledPanel.__init__(self, parent)
        
        self.API = API;
        # Just a shorter name
        self.tr = self.API.translater.translate
        self.initUI(emmbeddedMode)
        ### Editor visible variables
        if not emmbeddedMode:
            # @ creation we assume document is saved.
            self.saveState = True
            # Filename or untitled document
            self.fileName = self.tr('Untitled document') + ' ' + str(self.GetParent().nextPageNr)
            # Filename and full path(relative or absolute)
            self.filePath = self.tr('Untitled document') + ' ' + str(self.GetParent().nextPageNr)
            # This marks if document already have a file attached to it
            self.hasAFile = False
        # Define project type
        self.projectType = 0
        
    def update (self, initFilePath = ''):
        if initFilePath == '':
            initFilePath = self.filePath
        if os.path.exists(initFilePath) and os.path.isfile(initFilePath):
            # Load file into editor
            self.code.LoadFile(initFilePath)
            # Draw margins
            self.changeCode('', False)
            # Update editor info
            self.updateInfo(initFilePath, saveState = True, hasAFile = True)
            self.GetParent().titleChange(self.fileName)
            self.detectSEAL()
        else:
            self.changeCode()
            
    def initUI(self, emmbeddedMode):
        self.main = wx.BoxSizer(wx.HORIZONTAL)

        self.code = Editor.CodeEditor(self, self.API, emmbeddedMode)
        self.main.Add(self.code, 
                      1,            # make vertically stretchable
                      wx.EXPAND |    # make horizontally stretchable
                      wx.ALL,        # and make border all around
                      10 );         # set border width to 10)
                      
    def redrawAll(self):
        #Layout sizers
        self.SetSizer(self.main)
        self.SetAutoLayout(1)
        self.main.Fit(self)
        self.SetupScrolling()
        self.Show()
        
    def changeCode(self, newCode = '', overwrite = True):
        if overwrite == True:
            self.code.AddText(newCode)
        self.code.setLineNumbers()
        self.redrawAll()
    
    def save(self):
        self.code.SaveFile(self.filePath)
        self.saveState = True
        self.GetParent().markAsSaved()
    
    def updateInfo(self, path = '', fileName = '', saveState = '', 
                   hasAFile = '', projectType = None):
        if path != '':
            self.filePath = path
            self.fileName = path.split("/")[-1]
        if fileName != '':
            self.fileName = fileName
        if saveState != '':
            self.saveState = saveState
        if hasAFile != '':
            self.hasAFile = hasAFile
        if projectType != None:
            self.projectType = projectType
    
    def detectSEAL(self):
        if self.fileName[-2:] == "sl":
            self.projectType = g.SEAL_PROJECT
        else:
            self.projectType = g.MANSOS_PROJECT
            