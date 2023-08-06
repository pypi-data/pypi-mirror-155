# -*- coding: utf-8 -*-
#
# This program removes outliers from the observations.
#
#  This script is part of HectorP 0.0.5
#
#  HectorP is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  any later version.
#
#  HectorP is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with HectorP. If not, see <http://www.gnu.org/licenses/>
#
# 6/2/2022 Machiel Bos, Santa Clara
#===============================================================================

import os
import math
import time
import json
import numpy as np
import argparse
from hectorp.datasnooping import DataSnooping
from hectorp.control import Control
from hectorp.observations import Observations

#===============================================================================
# Main program
#===============================================================================

def main():

    #--- Parse command line arguments in a bit more professional way
    parser = argparse.ArgumentParser(description= 'Estimate trend')

    #--- List arguments that can be given
    parser.add_argument('-i', required=False, default='removeoutliers.ctl', \
                                      dest='fname', help='Name of control file')

    args = parser.parse_args()

    #--- parse command-line arguments
    fname = args.fname

    #--- Read control parameters into dictionary (singleton class)
    control = Control(fname)
    try:
        verbose = control.params['Verbose']
    except:
        verbose = True

    if verbose==True:
        print("\n***************************************")
        print("    removeoutliers, version 0.0.5")
        print("***************************************")

    #--- Get Classes
    datasnooping = DataSnooping()
    observations = Observations()

    #--- Start the clock!
    start_time = time.time()

    #--- Define 'output' dictionary to create json file with results
    output = {}
    datasnooping.run(output)

    #--- save cleaned time series to file
    fname_out = control.params['OutputFile']
    observations.momwrite(fname_out)

    #--- Save dictionary 'output' as json file
    with open('removeoutliers.json','w') as fp:
        json.dump(output, fp, indent=4)

    #--- Show time lapsed
    if verbose==True:
        print("--- {0:8.3f} s ---\n".format(float(time.time() - start_time)))
