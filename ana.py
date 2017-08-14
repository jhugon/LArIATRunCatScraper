#!/usr/bin/env python

import os.path
import re
import numpy
from matplotlib import pyplot as mpl
import matplotlib.colors

binning = [-5,-1,1.,9,11,19,21,39,41,59,61,79,81,99,101,105]

runSummaryDict = {}
runs = []
currents = []
with open("RunII_info.txt") as infile:
  for line in infile:
    line = line.split(" ")
    runs.append(int(line[0]))
    currents.append(float(line[2]))
    runSummaryDict[int(line[0])] = float(line[2])

fig, ax = mpl.subplots()
ax.hist(currents,bins=binning,histtype="step")
ax.set_xlabel("Current")
ax.set_ylabel("Runs / bin")
ax.set_xlim(-5,105)
fig.suptitle("Run II Magnet Current from RunSummary")
fig.savefig("runSummary_currentHist.png")
fig.savefig("runSummary_currentHist.pdf")

################

def getSamInfo(filename,current):
    result = []
    with open(filename) as infile:
      for line in infile:
        fn = os.path.basename(line)
        # lariat_digit_r008409_sr0002_20160526T053201.root
        match = re.match(r"lariat_digit_r(\d+)_sr(\d+)_([0-9T]+)\.root",fn)
        if not match:
            errormsg = '"{}" doesn\'t match format string'.format(fn)
            raise Exception(errormsg)
        run = int(match.group(1))
        subrun = int(match.group(2))
        timestamp = match.group(3)
        runSummaryCurrent = runSummaryDict[run]
        result.append([run,subrun,current,runSummaryCurrent])
    result.sort(key=lambda x: x[0]*10000+x[1])
    result = numpy.array(result)
    print "SAM: {} runs at {} A".format(result.shape[0],current)
    return result

sam0A = getSamInfo("Lovely1_Pos_RunII_jhugon_current0_secondary64_v1.files",0)
sam60A = getSamInfo("Lovely1_Pos_RunII_jhugon_current60_secondary64_v1.files",60)
sam100A = getSamInfo("Lovely1_Pos_RunII_jhugon_current100_secondary64_v1.files",100)

allData = numpy.concatenate((sam0A,sam60A,sam100A),0)

################

fig, ax = mpl.subplots()
ax.hist(allData[:,3],binning,histtype='step',label="Run Summary")
ax.hist(allData[:,2],binning,histtype='step',label="SAM")
ax.set_xlabel("Magnet Current [A]")
ax.set_ylabel("Files (subruns) per bin")
ax.set_xlim(-5,105)
ax.set_yscale('log')
ax.legend(loc="upper center")
fig.suptitle("Lovely Run II+ Magnet Current")
fig.savefig("currentHist.png")
fig.savefig("currentHist.pdf")

fig = mpl.figure()
ax = fig.add_subplot(111,aspect="equal")
hist2d, xedges, yedges = numpy.histogram2d(allData[:,2],allData[:,3],bins=(50,50),range=((-10,110),(-10,110)))
x,y = numpy.meshgrid(xedges,yedges)
meshcolors = ax.pcolormesh(x,y,hist2d,cmap="Blues",norm=matplotlib.colors.LogNorm())
ax.set_xlabel("SAM Magnet Current [A]")
ax.set_ylabel("Run Summary Magnet Current [A]")
ax.set_xlim(-10,110)
ax.set_ylim(-10,110)
fig.colorbar(meshcolors)
fig.suptitle("Lovely Run II+ Magnet Current")
fig.savefig("currentHist2D.png")
fig.savefig("currentHist2D.pdf")

####################################

for i in reversed(range(len(runs))):
  if currents[i] < 10.:
    currents.pop(i)
    runs.pop(i)

fig, ax = mpl.subplots()
ax.plot(runs,currents,'.b',label="Run II Run Summary")
ax.plot(allData[:,0],allData[:,2],'.g',label="Lovely Run II+ SAM")
ax.set_xlabel("Run Number")
ax.set_ylabel("Magnet Current [A]")
ax.set_ylim(-5,105)
ax.legend(loc="center right")
fig.suptitle("Run II Magnet Current v. Run Number")
fig.savefig("currentVrun.png")
fig.savefig("currentVrun.pdf")

