#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 16:29:27 2022

@author: joe
"""

import pandas as pd
import numpy as np
from scipy import signal
import math

# peakfinder class; used to process raw data into peak analysis
class peakfinder:
    # filedir can be specified on initialisation or passed to the analyse function
    def __init__(self,filedir=""):
        self.filedir = filedir
        return
    
    def analyse(self,filedir=""):
        if(filedir==""):
            localdir = self.filedir
        else:
            localdir = filedir
        process_inputs(localdir)
        return
        

# Save peak data as a csv
def process_inputs(filedir):
    # Get the raw data
    rawdata = convert_rawdata(filedir)
    # Find and process the peaks of this data
    peaks = find_allpeaks(rawdata)
    # Convert this data to a dataframe
    peaks = peaks_to_df(peaks)
    # Save the new dataframe
    outname = filedir.replace("DATALOG.TXT","PEAKDATA.csv")
    with open(outname,"w") as f:
        peaks.to_csv(f,index=False,sep=",",line_terminator="\n")
    return

# Convert raw data into a dataframe
def convert_rawdata(ddir=""):
    with open(ddir,"r") as f:
        data = f.read()
    datalist = data.split("\n")
    data = []
    for entry in datalist:
        # Ignore lines without the 'Time' keyword i.e. they're not formatted properly
        if("Time" not in entry): continue
        temp = entry.split(",")
        ## Get the timestamp and voltages from this line
        # Uses [6:] so 'Time: ' is removed
        datatime = int(temp[0][6:])
        v1,v2,v3 = float(temp[1]),float(temp[2]),float(temp[3])
        data.append([datatime,v1,v2,v3].copy())
    del datalist
    # Convert dataframe
    data = pd.DataFrame(data=data,columns=["Time (ms)","V1","V2","V3"])
    return data

# Find peaks of a dataframe made from the raw data
def find_allpeaks(df):
    peaks = {}
    # Cycle through V1, V2 and V3
    for i in range(1,4):
        peaks[f"V{i}"] = find_peaks(df["Time (ms)"],df[f"V{i}"])
    return peaks

# Convert an allpeaks dict to a dataframe
def peaks_to_df(peakdict):
    data = []
    for key in peakdict:
        for row in peakdict[key].iterrows():
            newlist = [key] + [list(row)[1][i] for i in range(len(list(row)[1]))]
            data.append(newlist.copy())
    data = pd.DataFrame(data=data,columns=["Channel","Peak Index","Time (ms)",
                                           "Voltage (V)","Width (ms)","Area under peak",
                                           "Ascent Gradient","Ascent Standard Deviation",
                                           "Ascent Minimum","Ascent Maximum",
                                           "Descent Gradient","Descent Standard Deviation",
                                           "Descent Minimum","Descent Maximum"])
    return data
    
    
# Find peaks from a single time series and accompanying voltage series
def find_peaks(ts,vs):
    baseline,dev = find_baseline(vs)
    # Get data peaks
    peaks = signal.find_peaks(vs)
    if(len(peaks)==0): return []
    # Remove peaks within the standard deviation from baseline
    real_peaks = []
    for i in peaks[0]:
        if(vs[i]<baseline+dev and vs[i]>baseline-dev):
            continue
        real_peaks.append([i,ts[i],vs[i]].copy())
    peaks = pd.DataFrame(data=real_peaks,columns=["Index","Time (ms)","Voltage"])
    # Process the peaks to merge peaks appropriately, find their width and find their area
    peaks = process_peaks(ts,vs,peaks)
    return peaks

# Get the baseline of a voltage series
def find_baseline(vs,mode="deviation"):
    # Done by finding an average of points all between the data's standard deviation
    baseline,dev = np.mean(vs),np.std(vs)
    # Alter the deviation based on the mode if appropriate
    if(mode=="root deviation"):
        dev = abs(np.sqrt(dev))
    elif(mode=="half deviation"):
        dev = dev/2
    elif(mode=="square deviation"):
        dev = np.power(dev,2)
    # Loop is repeated 5 times so baseline is approximately right without processing taking too long
    for _ in range(5):
        norms = []
        for v in vs:
            if(v<baseline+dev and v>baseline-dev):
                norms.append(v)
        baseline = np.mean(norms)
    return baseline,dev

# Merge peaks and find their width
def process_peaks(ts,vs,unprocessed_peaks):
    # Convert unprocessed peaks to a list for easier manipulation
    i,t,v = unprocessed_peaks["Index"],unprocessed_peaks["Time (ms)"],unprocessed_peaks["Voltage"]
    peaks = [[i[k],t[k],v[k]].copy() for k in range(len(i))]
    # Start by getting the baseline range
    baseline,dev = find_baseline(vs)
    brange = [baseline-dev,baseline+dev]
    ## First, merge peaks by checking if any data point substantially decreases between points
    # Currently just checks if the data dips into the baseline range
    p = 0
    while(p<len(peaks)-1):
        peak,nextpeak = peaks[p],peaks[p+1]
        # Default to setting these 2 peaks as to-merge, and then start finding reasons to not merge them
        tomerge = True
        # Starting from the time, check if a point goes into baseline-range
        for i in range(peak[0]+1,nextpeak[0]):
            if(vs[i]<brange[1]):
                #print(f"Merging {peak} and {nextpeak} due to voltage {vs[i]} at time {ts[i]} (Index = {i})")
                tomerge = False
                break
        if(tomerge==True):
            # Make the new peak the one with the largest voltage
            if(peak[2]>nextpeak[2]):
                del peaks[p+1]
            else:
                del peaks[p]
        else:
            p += 1
    ## Find the peaks' width, area, and gradients
    for peak in peaks:
        # Find the points this peak exits and then re-enters the baseline range
        mi,ma = peak[0],peak[0]
        while(True):
            if(vs[mi-1]>= brange[1]):
                mi -= 1
            elif(vs[ma+1]>= brange[1]):
                ma += 1
            else:
                break
        # Get the width in time
        mit,mat = ts[mi],ts[ma]
        peak.append(mat-mit)
        # Get the area under the line
        area = 0.0
        for i in range(mi,ma):
            # Trianglular area followed by area between triangle and baseline
            tri = 0.5*abs(vs[i+1]-vs[i])*abs(ts[i+1]-ts[i])
            # Height * width
            sqr = (min(vs[i+1],vs[i])-baseline) * abs(ts[i+1]-ts[i])
            area += tri + sqr
        peak.append(area)
        ## Finding the gradients for ascent and descent
        asgrads,degrads = [],[]
        for i in range(mi,peak[0]):
            grad = (vs[i+1]-vs[i])/(ts[i+1]-ts[i])
            asgrads.append(grad)
        for i in range(peak[0],ma):
            grad = (vs[i+1]-vs[i])/(ts[i+1]-ts[i])
            degrads.append(grad)
        # Add the average gradient, standard deviation, ~min gradient and ~max gradient
        # ~ used as its the average of the bottom/top 5% of gradients
        temp = sorted(asgrads)
        asmin,asmax = np.mean(temp[:math.ceil(len(temp)/20)]),np.mean(temp[int((19*len(temp))/20):])
        temp = sorted(degrads)
        demin,demax = np.mean(temp[:math.ceil(len(temp)/20)]),np.mean(temp[int((19*len(temp))/20):])
        peak += [np.mean(asgrads),np.std(asgrads),asmin,asmax].copy()
        peak += [np.mean(degrads),np.std(degrads),demin,demax].copy()
        
    # Reform the data into a dataframe
    peaks = pd.DataFrame(data=peaks,columns=["Peak Index","Time (ms)","Voltage",\
                                             "Width (ms)","Area under peak",\
                                             "Ascent Gradient","Ascent Standard Deviation",\
                                             "Ascent Minimum","Ascent Maximum",\
                                             "Descent Gradient","Descent Standard Deviation",\
                                             "Descent Minimum","Descent Maximum"])
    return peaks