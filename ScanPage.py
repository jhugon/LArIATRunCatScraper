# Copyright (C) 2017-2017 Elena Gramellini <elena.gramellini@yale.edu>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You can read copy of the GNU General Public License here:
# <http://www.gnu.org/licenses/>.

"""@package docstring
Scope of this python script: 
Given a list of run, subrun, event
read from the lariat run catalogue and assess the beam conditions 

Author: Elena Gramellini

Creation Date: 2016-26-06 

Version 0 
-----------------------------------------------------------------------
Input:  csv file whose column are run, subrun, event  
Output: csv file whose column are run, N event for that run, magnet polarity, magnet current, secondary beam energy  
"""   


import re, requests, json,csv

# Then consult the runCatalog
def consultRunCat( runNumber ):
    #These are the important tags on the web page that we need to find
    current_tag   = "mid_f_mc7an"
    energy_tag    = "mid_f_mcenrg"
    polarity_tag  = "mid_f_mc7anb"
    url2 ='http://lariat-wbm.fnal.gov/wbm/servlet/LariatRunSummary?RUN='+str(runNumber)
    r = requests.get(url2)
    text = (r.text).split()
    polarity = 0.
    current  = 0.
    energy   = 0.
    for line in text:
        if line.find(current_tag) != -1:
            if line.find(polarity_tag) != -1:
                w = line.split("</TD>")
                polarity = float(w[2].replace("<TD>", ""))
                if polarity > 0:
                    polarity = 1.
                else: 
                    polarity = -1.
            else:
                w = line.split("</TD>")
                current =  float(w[2].replace("<TD>", ""))
                
        if line.find(energy_tag) != -1:
            w = line.split("</TD>")
            energy = float(w[2].replace("<TD>", ""))

    if (polarity and current and energy):
        print runNumber, numberOfEvents, polarity, current, energy
    return  (polarity, current, energy)

# First things first:
# read the input file
runNumber      = 9004
numberOfEvents = 0

#l = consultRunCat( runNumber )


fname = "test.csv"
with open(fname) as f:
    for fLine in f.readlines():
        w = fLine.split(",")
        run = int(w[0])
        evt = int(w[2])
        print run, evt

