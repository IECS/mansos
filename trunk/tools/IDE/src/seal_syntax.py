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

from globals import * #@UnusedWildImport

import component_hierarchy

class SealSyntax():
    def __init__(self, API):
        self.API = API

        self.predefinedConditions = [
            "True",
            "False",
            "isDayTime",
            "time < 5s",
            "Cat's eat apples"
            ]

        platform = self.API.getSetting("platform")
        assert platform in self.API.platforms, \
            "Unknown platform defined: {0}".format(platform)

        __import__(platform)

        self.syntax = [
            ["use", "read", "output"],
            [[]], # use
            [[]], # read
            [[]]  # output
        ]

        for x in component_hierarchy.components:
            if x.name not in self.syntax[x.typeCode][0]:
                # Create a new object entry
                self.syntax[x.typeCode][0].append(x.name)
                self.syntax[x.typeCode].append(list())
            for p in dir(x):
                # Fill object entry with keywords
                if type(x.__getattribute__(p)) is component_hierarchy.SealParameter:
                    # Temp fix
                    if p in ['filter', 'average', 'stdev']:
                        self.syntax[x.typeCode][-1].append((p, x.__getattribute__(p).valueList))
                    else:
                        self.syntax[x.typeCode][-1].insert(0, (p, x.__getattribute__(p).valueList))
                    # Bad thing to do...
                    if p not in SEAL_PARAMETERS:
                        SEAL_PARAMETERS.append(p)

        #self.printAllSyntax()

    def printAllSyntax(self):
        # Just for pure understanding of used structure
        for x in range(len(self.syntax[0])):
            print self.syntax[0][x]
            for y in range(len(self.syntax[x + 1][0])):
                print " "*4, self.syntax[x + 1][0][y]
                for z in self.syntax[x + 1][y + 1]:
                    print " "*8, z[0], ":", z[1]

    def getKeywords(self, target1 = None, target2 = None):
        if target1 == None:
            return self.syntax[0]
        target1Nr = self.findRealIndex(self.syntax[0], target1)

        if target1Nr == 0 or target2 == '':
            return []

        assert target1 in self.syntax[0], "'{}' not found".format(target1)

        if target2 == None:
            return self.syntax[target1Nr][0]

        target2Nr = self.findRealIndex(self.syntax[target1Nr][0], target2)

        if target2Nr == 0:
            return []

        #assert target2 in self.syntax[target1Nr][0], \
        #    "'{}' not found in {}".format(target2, self.syntax[target1Nr][0])

        return self.syntax[target1Nr]\
            [target2Nr]

    def findRealIndex(self, myList, entry):
        #assert entry in myList, "{} not found in {}".format(entry, myList)
        for x in range(len(myList)):
            if myList[x].lower() == entry.lower():
                return x + 1
        return 0