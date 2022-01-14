# -*- coding: utf-8 -*-
"""
Created on Fri Jan 14 14:06:19 2022

@author: charl
"""




class Master:
    def __init__(self):
        self.WTs = []
        





class WT:
    def __init__(self,eastings,northings,altitude,hub_height,gnd_attn,mode_attn, wt_type):
        self.eastings = eastings
        self.northings = northings
        self.altitude =altitude
        self.hub_height =hub_height
        self.gnd_attn =gnd_attn
        self.mode_attn =mode_attn
        self.wt_type =wt_type
        