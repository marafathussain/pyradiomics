from __future__ import print_function
import six
import os  # needed navigate the system to get the input data

import radiomics
from radiomics import featureextractor  # This module is used for interaction with pyradiomics
import numpy as np
import csv


# Instantiate the extractor
extractor = featureextractor.RadiomicsFeatureExtractor()

print('Extraction parameters:\n\t', extractor.settings)
print('Enabled filters:\n\t', extractor.enabledImagetypes)
print('Enabled features:\n\t', extractor.enabledFeatures)


filename = "/home/marafath/scratch/Age_sex.csv"
rows = [] 

with open(filename, 'r') as csvfile: 
    # creating a csv reader object 
    csvreader = csv.reader(csvfile) 
  
    # extracting each data row one by one 
    for row in csvreader: 
        rows.append(row) 
  
    # get total number of rows 
    print("Total no. of rows: %d"%(csvreader.line_num))
    

data_dir = '/home/marafath/scratch/iran_organized_data2'
import copy

c = 0
for patient in os.listdir(data_dir):
    rad = []
    f = 0
    for pat in range(0,len(rows)):
        if rows[pat][0] == patient:
            if rows[pat][1] == '0':
                age = 50
            else:
                age = rows[pat][1]
                age = age[1:3]
                age = int(age)
            rad.append(age/100)
            
            if rows[pat][2] == ' ':
                rad.append(1)
                rad.append(0)
            elif rows[pat][2] == 'M':
                rad.append(1)
                rad.append(0)
            else:    
                rad.append(0)
                rad.append(1)
    rad = np.asarray(rad,np.float64)
    for series in os.listdir(os.path.join(data_dir,patient)):
        if f == 0:
            c += 1
            f = 1
        rad_ = copy.deepcopy(rad)   
        imagePath = os.path.join(data_dir,patient,series,'image.nii.gz')
        maskPath = os.path.join(data_dir,patient,series,'infection.nii.gz')
        result = extractor.execute(imagePath, maskPath)
        print(patient+'_'+series)
        
        counter = 0
        for key, value in six.iteritems(result):
            counter += 1
            if counter < 23:
                continue
            rad_ = np.append(rad_, value)  

        print(len(rad_))    
        np.save(os.path.join(data_dir,patient,series,'radiomics'), rad_) 
    
print(c)   