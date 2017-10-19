# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 00:08:17 2017

@author: song-isong-i
"""

def read_asf(asf_filename):
    with open(asf_filename, 'r') as asff:
        asf = asff.read().split('\n')    
    dof = {}      
    for i,c in enumerate(asf):
        asf[i] = c.lstrip(' ').rstrip(' ')    
    for i in range(30):
        find = 'id '+str(i+1)
        index = asf.index(find)
        name = asf[index+1][5:]
        dofline = asf[index+5]
        if dofline == 'end':
            continue
        else:
            v = dofline[4:]
            ax = [0,0,0]
            if 'rx' in v:
                ax[0] = 1
            if 'ry' in v:
                ax[1] = 1
            if 'rz' in v:
                ax[2] = 1
            dof[name] = ax
    return dof
    
def amc2vector(amc_filename,dof):
    amcf = open(amc_filename, 'r')
    amc = amcf.readlines()
    amcf.close()
    count = 1
    rdata = []
    frame = []
    for i, line in enumerate(amc):
        if line.startswith(':') or line.startswith('#'):
            continue
        if str(count) == line.rstrip('\n'):
            if count != 1:
                rdata.append(frame)
            frame = []
            count += 1
            continue
        
        values = line.rstrip('\n').split(' ')
        name = values.pop(0)
        if name == 'root':
            frame.extend([float(v) for v in values])
        else:
            ax = dof[name][:]
            for j, r in enumerate(ax):
                if r == 1:
                    ax[j] = float(values.pop(0)) 
            if len(values) > 0:
                print(values)
                print(ax)
                raise ValueError('ERROR')
                break
            frame.extend(ax)  
        if i == len(amc)-1:
            rdata.append(frame)
    return rdata
            
#def convert_all(amc_folder, dof)
import numpy as np
if __name__ == '__main__':
    asf_filename = '01.asf'
    amc_filename = '05_04.amc'
    dof = read_asf(asf_filename)
    rdata = amc2vector(amc_filename,dof)
    print(np.array(rdata).shape)
    