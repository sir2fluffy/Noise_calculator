# -*- coding: utf-8 -*-
"""
Created on Fri Jan 14 14:06:19 2022

@author: charl
"""

import numpy as np
import matplotlib.pyplot as pl


class Master:
    def __init__(self):
        self.WTs = []
        self.RECs = []
        self.mpp = 1#meters per pixel
        self.next_index_wt = 0
        self.next_index_rec = 0
        
        #self.map_padding = 100
        self.mete_dict = {0: (0,0,0,0,0,0,0,0),  1:(0.1, 0.4, 1.0, 1.9, 3.7, 9.7, 32.8, 117.0) ,    2:(0.1, 0.3, 1.1, 2.8, 5.0, 9.0, 22.9, 76.6) , 3:      (0.1, 0.3, 1.0, 3.1, 7.4, 12.7, 23.1, 59.3)  ,4:    (0.3, 0.6, 1.2, 2.7, 8.2, 28.2, 88.8, 202.0) ,5:    (0.1, 0.5, 1.2, 2.2, 4.2, 10.8, 36.2, 129.0)   ,6:  (0.1, 0.3, 1.1, 2.4, 4.1, 8.3, 23.7, 82.8)}
        self.mete_conditions = 0 #number 0 to 6 indicating which list to use of the above mete conds
        
        self.noise_array = None# total nosie array of all turbines
        
        
        
        
    def __len__(self):
        return len(self.WTs)

    def __iter__(self):
        return self.WTs
    
    def get_(self,parameter):
        temp = []
        for WT in self.WTs:
            exec(f"temp.append(WT.{parameter})")
        return temp
            
    
        
        
        
    def gen_maps(self,padding=100,scale=.10):
    
       # determine map size
       
        if len(self) == 0:
            raise Exception("No turbines to generate map")
        elif len(self) == 1:# add x pixels around turbine# 
            self.map_size = (2, 2*padding, 2*padding)     
            map_x = (2*padding) + 1
            map_y = (2*padding) + 1
            
            
            
            map_x_min = (self.WTs[0]).eastings - padding*self.mpp
            map_y_min = (self.WTs[0]).northings - padding*self.mpp
            
        else:# generate map as max turbine range + x%     
        
            eastings = self.get_("eastings")           
            map_x = int(((max(eastings) - min(eastings))/self.mpp)*(1+(2*scale))) + 1
            map_x_min = min(eastings)-(map_x*self.mpp*scale)
            
            northings = self.get_("northings")           
            map_y = int(((max(northings) - min(northings))/self.mpp)*(1+(2*scale))) + 1
            map_y_min = min(northings)-(map_y*self.mpp*scale)
            
            self.map_size = (2, map_x, map_y)
    #generate blank 3d array 
           
           
           
           
        coord_array = np.zeros(self.map_size)
        
        for x in range(0,self.map_size[1]):#fill array with meter coordiantes of each pixel
            coord_array[0,x,:] = (x*self.mpp) + map_x_min
            
        for y in range(0,self.map_size[2]):
            coord_array[1,:,y] = (y*self.mpp) + map_y_min
        # determine noises
        
        def noise(self, coord_array):
            def get_distance(coord_array,WT):
                WT_x = WT.eastings
                WT_y = WT.northings
                return np.sqrt(np.square( coord_array[0,:,:]-WT_x)+ np.square(coord_array[1,:,:]-WT_y)) #return distance array
            
            def attenuation(self, distance, WT, index):# attenuation calculations
                
            #A_div
                d_0 = 1 # refernce distance = 1m
                
                
                    
                A_div = (20*np.log((distance+1)/d_0)+ 11)
                
                #A_atm
                alpha = self.mete_dict[self.mete_conditions][index]# atomospheric attenuation coefficent fromt able 2 todo: add this table
                
                A_atm = (alpha*distance)/1000
                #A_gr
                
                A_gr = WT.gnd_attn
                
                return A_div + A_atm + A_gr
            
            for WT in self.WTs:
                WT.noisemap = np.zeros((8,*self.map_size[1:]))
                distance = get_distance(coord_array, WT)
                self.distance_array = distance
                self.coord_array = coord_array
                
                
                
                # pl.imshow(distance/np.max(distance),interpolation='nearest')
                # pl.show()
                for index, frequency in enumerate((63,125,250,500,1000 ,2000 ,4000 ,8000)):
                    
                    
                    A = attenuation(self, distance, WT, index)
                    
                    L_W = WT.wt_type[index] 
                    D_c = 0
                    loudness = L_W + D_c - A
                    
                    WT.noisemap[index,:,:] = loudness
        
        noise(self,coord_array)
                
                    
                    

        total_map = np.zeros(self.map_size[1:])  
        for WT in self.WTs:
            for index in range(0,8):
                total_map = 10*np.log10(10**(WT.noisemap[index,:,:]/10)+10**(total_map/10))
                
        self.noise_array = total_map
            
        
        
        pl.imshow(self.noise_array,interpolation='nearest')
        pl.gca().invert_yaxis()
        pl.show()
        
        pl.contour(self.noise_array)
        pl.show()
                    
                    
        
        
        
        
        
            
            
            
            
        
        


class WT:
    def __init__(self,eastings,northings,altitude,hub_height,gnd_attn,mode_attn, wt_type):
        self.eastings = eastings
        self.northings = northings
        self.altitude = altitude
        self.hub_height = hub_height
        self.gnd_attn = gnd_attn
        self.mode_attn = mode_attn
        self.wt_type = wt_type
        self.index =  Master.next_index_wt
        self.noisemap = None # will become a 8,x,y array of the different noise maps
        Master.next_index_wt += 1
        Master.WTs.append(self)

class REC:
    def __init__(self,eastings,northings,altitude,name,attn):
        self.eastings = eastings
        self.northings = northings
        self.altitude = altitude
        self.attn = attn
        self.index =  Master.next_index_rec
        self.name = name        
        Master.next_index += 1
        Master.RECs.append(self)        
        
Master=Master()




for paras in ((100,100,12,12,1,1,[100,100,100,100,100,100,100,100]),(300,300,12,12,1,1,[100,100,100,100,100,100,100,100])):
    WT(*paras)
    
Master.gen_maps()

