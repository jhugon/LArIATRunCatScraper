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

# Some reduntant import. 
# We probably use only requests, collections, ROOT and array
# But, you know, just in case
import re, requests, json, csv, argparse
from collections import defaultdict
import ROOT
from ROOT import TFile, TTree
from array import array
 


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
            print runNumber
            try:
                energyIn = float(w[2].replace("<TD>", ""))
            except ValueError:
                energyIn   = 0
                polarityIn = 0
                currentIn  = 0
    # Return your the run conditions
    # In case run not found, the values will be 0, 0, 0
    return  (polarityIn, currentIn, energyIn)




# This code takes as an argument 
# the name of the input csv file
parser = argparse.ArgumentParser()
parser.add_argument("fname"   , nargs='?', default = 'test.csv', type = str, help="insert fileName")
parser.add_argument("outName" , nargs='?', default = 'beamConditions.root'   , type = str, help="insert fileName")
args    = parser.parse_args()
fname   = args.fname
outName = args.outName



# First things first:
# read the input file
my_dict = defaultdict(int)
if (fname.find(".root") != -1):
    print "Ok, you gave me a root file! "
    rFile = ROOT.TFile(fname)
    rTree = rFile.Get('anatree/anatree')

    for entry in range(rTree.GetEntries()):
        rTree.GetEntry(entry)
        runIn    = int(rTree.run)
        my_dict[runIn] += 1

else:
    print "Ok, you didn't give me a root file, hopefully this is a csv "
    with open(fname) as f:
        for fLine in f.readlines():
            w = fLine.split(",")
            runIn    = int(w[0])
            my_dict[runIn] += 1


# Store this info in a csv and in a ROOT TTree
# Define TFile and TTree
# The TTree has 1 enrty per run
f = TFile( outName+".root", 'recreate' )
t = TTree( 'RunConditionsTTree', 'tree' )

# Define TTree Branches
run      = array( 'i', [ 0 ] )  # Run Number 
nevents  = array( 'i', [ 0 ] )  # Number of events in that run
polarity = array( 'f', [ 0 ] )  # Magnet polarity fo that run
current  = array( 'f', [ 0 ] )  # Magnet current for that run
energy   = array( 'f', [ 0 ] )  # Secondary beam energy for that run
t.Branch( 'run'     ,run     , 'run/I'     )
t.Branch( 'nevents' ,nevents , 'nevents/I' )
t.Branch( 'polarity',polarity, 'polarity/F')
t.Branch( 'current' ,current , 'current/F' )
t.Branch( 'energy'  ,energy  , 'energy/F'  )

# Open your out csv file and loop on the dictionary
stupidCounter = 0
with open(outName+".csv","w") as target:
    for k,v in my_dict.items():
        stupidCounter+=1
        if not stupidCounter % 10000.:
            print "Run count: ", stupidCounter 
        # This is where the magic happens 
        # (call the consultRunCat function and store results)
        tupla = consultRunCat(k)
        outline =  str(k)+","+str(v)+","+str(tupla[0])+","+str(tupla[1])+","+str(tupla[2])+"\n"
        # write output
        target.write(outline)
        # Fill TTree branches
        run[0]      =  k      
        nevents[0]  =  v
        polarity[0] =  tupla[0]
        current[0]  =  tupla[1]
        energy[0]   =  tupla[2]
        t.Fill()
 
f.Write()
f.Close()
