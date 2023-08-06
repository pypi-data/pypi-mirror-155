# observations.py
#
# A simple interface that reads and writes mom-files and stores
# them into a Python class 'observations'.
#
# This file is part of HectorP 0.0.5.
#
# HectorP is free software: you can redistribute it and/or modify it under the 
# terms of the GNU General Public License as published by the Free Software 
# Foundation, either version 3 of the License, or (at your option) any later 
# version.
#
# HectorP is distributed in the hope that it will be useful, but WITHOUT ANY 
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with 
# HectorP. If not, see <https://www.gnu.org/licenses/>.
#
#  31/1/2019  Machiel Bos, Santa Clara
#   1/5/2020  David Bugalho
# 29/12/2021  Machiel Bos, Santa Clara
#  7/ 2/2022  Machiel Bos, Santa Clara
#==============================================================================

import pandas as pd
import numpy as np
import os
import sys
import math
from hectorp.control import Control
from hectorp.control import SingletonMeta
from pathlib import Path

#==============================================================================
# Class definition
#==============================================================================

class Observations(metaclass=SingletonMeta):
    """Class to store my time series together with some metadata
    
    Methods
    -------
    momread(fname)
        read mom-file fname and store the data into the mom class
    momwrite(fname)
        write the momdata to a file called fname
    make_continuous()
        make index regularly spaced + fill gaps with NaN's
    """
    
    def __init__(self):
        """This is my time series class
        
        This constructor defines the time series in pandas DataFrame data,
        list of offsets and the sampling period (unit days)
        
        """

        #--- Get control parameters (singleton)
        control = Control()
        try:
            self.verbose = control.params['Verbose']
        except:
            self.verbose = True

        #--- class variables
        self.data = pd.DataFrame()
        self.offsets = []
        self.sampling_period = 0.0
        self.F = None
        self.percentage_gaps = None
        self.m = 0

        #--- Read file with observations
        try:
            datafile = control.params['DataFile']
            directory = Path(control.params['DataDirectory'])
        except Exception as e:
            print(e)
            sys.exit()

        fname = str(directory / datafile)
        self.momread(fname)

        #--- Inform the user
        if self.verbose==True:
            print("\nFilename                   : {0:s}".format(fname))
            print("Number of observations+gaps: {0:d}".format(self.m))
            print("Percentage of gaps         : {0:5.1f}".\
					          format(self.percentage_gaps))

    
    def momread(self,fname):
        """Read mom-file fname and store the data into the mom class
        
        Args:
            fname (string) : name of file that will be read
        """
        #--- Check if file exists
        if os.path.isfile(fname)==False:
            print('File {0:s} does not exist'.format(fname))
            sys.exit()
        
        #--- Read the file (header + time series)
        mjd = []
        obs = []
        mod = []
        with open(fname,'r') as fp:
            for line in fp:
                cols = line.split()
                if line.startswith('#')==True:
                    if cols[1]=='sampling' and cols[2]=='period':
                        self.sampling_period = float(cols[3])
                    elif cols[0]=='#' and cols[1]=='offset':
                        self.offsets.append(float(cols[2]))
                else:
                    if len(cols)<2 or len(cols)>3:
                        print('Found illegal row: {0:s}'.format(line))
                        sys.exit()
                    
                    mjd.append(float(cols[0]))
                    obs.append(float(cols[1]))
                    if len(cols)==3:
                        mod.append(float(cols[2]))
                    
        #---- Create pandas DataFrame
        self.data = pd.DataFrame({'obs':np.asarray(obs)}, \
                                              index=np.asarray(mjd))
        if len(mod)>0:
            self.data['mod']=np.asarray(mod)
            
        #--- Ensure that the observations are regularly spaced
        self.make_continuous()
        
        #--- Create special missing data matrix F
        self.m = len(self.data.index)
        n = self.data['obs'].isna().sum()
        self.F = np.zeros((self.m,n))
        j=0
        for i in range(0,self.m):
            if np.isnan(self.data.iloc[i,0])==True:
                self.F[i,j]=1.0
                j += 1

        #--- Compute percentage of gaps
        self.percentage_gaps = 100.0 * float(n) /float(self.m)
        
        
        
    def momwrite(self,fname):
        """Write the momdata to a file called fname
        
        Args:
            fname (string) : name of file that will be written
        """
        #--- Try to open the file for writing
        try:
            fp = open(fname,'w') 
        except IOError: 
           print('Error: File {0:s} cannot be opened for written.'. \
                                                         format(fname))
           sys.exit()
        if self.verbose==True:
            print('--> {0:s}'.format(fname))
        
        #--- Write header
        fp.write('# sampling period {0:f}\n'.format(self.sampling_period))
                
        #--- Write header offsets
        for i in range(0,len(self.offsets)):
            fp.write('# offset {0:10.4f}\n'.format(self.offsets[i]))
 
        #--- Write time series
        for i in range(0,len(self.data.index)):
            if not math.isnan(self.data.iloc[i,0])==True:
                fp.write('{0:12.6f} {1:13.6f}'.format(self.data.index[i],\
                                                  self.data.iloc[i,0]))
                if len(self.data.columns)==2:
                    fp.write(' {0:13.6f}\n'.format(self.data.iloc[i,1]))
                else:
                    fp.write('\n')
            
        fp.close()
        
        
    
    def make_continuous(self):
        """Make index regularly spaced + fill gaps with NaN's
        """
        #--- Small number
        EPS = 1.0e-8
        
        #--- Number of observations currently
        mm = len(self.data.index)
        
        mjd0  = self.data.index[0]
        mjd1  = self.data.index[mm-1]
        m_new = int((mjd1-mjd0)/self.sampling_period + EPS) + 1
        new_index = np.linspace(mjd0,mjd1,m_new)
        self.data = self.data.reindex(new_index)



    def show_results(self,output):
        """ add info to json-ouput dict
        """
        
        output['N'] = self.m
        output['gap_percentage'] = self.percentage_gaps 



    def add_offset(self,mjd):
        """ Add mjd to list of offsets
        
        Args:
            mjd (float): modified julian date of offset
        """

        EPS   = 1.0e-6
        found = False
        i     = 0
        while i<len(self.offsets) and found==False:
            if abs(self.offsets[i]-mjd)<EPS:
                found = True
            i += 1
        if found==False:
            self.offsets.append(mjd)



    def set_NaN(self,index):
        """ Set observation at index to NaN and update matrix F

        Args:
            index (int): index of array which needs to be set to NaN
        """

        self.data.iloc[index,0] = np.nan 
        dummy = np.zeros(self.m)
        dummy[index] = 1.0
        self.F = np.c_[ self.F, dummy ] # add another column to F



    def add_mod(self,xhat):
        """ Add estimated model as column in DataFrame

        Args:
            xhat (array float) : estimated model
        """

        self.data['mod']=np.asarray(xhat)
