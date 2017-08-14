#!/usr/bin/env python
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
#
# To Do
# [ x ] read input file
# [   ] read input as ttree file
# [   ] from input file figure how many events per run
# [ x ] consultRunCat: 
#       take as a input the runNumber, output the polarity, current and energy 
# [ x ] write csv output

"""@Package docstring
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

import re, requests, json, csv, argparse
from collections import defaultdict

# Then consult the runCatalog
def consultRunCat( runNumber ):
    #These are the important tags on the web page that we need to find
    currentIn_tag   = "mid_f_mc7an"
    energyIn_tag    = "mid_f_mcenrg"
    polarityIn_tag  = "mid_f_mc7anb"
    # The url is tied to the run number: 1 url = 1 run number
    url ='http://lariat-wbm.fnal.gov/wbm/servlet/LariatRunSummary?RUN='+str(runNumber)
    # Get the content of the url
    r = requests.get(url)
    # Make it into text and split by line (text is now an iterable object)
    text = (r.text).split()
    polarityIn = 0.
    currentIn  = 0.
    energyIn   = 0.
    # Check if tags are contained in each line
    # the tag "mid_f_mc7an" is contained in "mid_f_mc7anb" 
    for line in text:
        if line.find(currentIn_tag) != -1:
            if line.find(polarityIn_tag) != -1:
                w = line.split("</TD>")
                try:    
                    polarityIn = float(w[2].replace("<TD>", ""))
                    if polarityIn > 0:
                        polarityIn = 1.
                    else: 
                        polarityIn = -1.                
                except ValueError:
                    energyIn   = 0
                    polarityIn = 0
                    currentIn  = 0
            else:
                w = line.split("</TD>")
                try:
                    currentIn = float(w[2].replace("<TD>", ""))
                except ValueError:
                    energyIn   = 0
                    polarityIn = 0
                    currentIn  = 0
        if line.find(energyIn_tag) != -1:
            w = line.split("</TD>")
            #print runNumber
            try:
                energyIn = float(w[3].replace("<TD>", ""))
            except ValueError:
                energyIn   = 0
                polarityIn = 0
                currentIn  = 0
    # Return your the run conditions
    # In case run not found, the values will be 0, 0, 0
    return  (runNumber,polarityIn, currentIn, energyIn)

with open("RunII_info.txt",'w') as outfile:
  for run in range(8000,10227):
  #for run in [8000,10227]:
    outfile.write("{} {} {} {}\n".format(*consultRunCat(run)))
