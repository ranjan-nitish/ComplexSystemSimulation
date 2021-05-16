# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 16:16:31 2021

@author: NITISH
"""

import random as rand
from PIL import Image
from random import choice,uniform,randint
import matplotlib
from matplotlib.cbook import get_sample_data
matplotlib.use('TkAgg')
from pylab import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import *
n =300 # number of agents
r = 0.3 # neighborhood radius
 
count=0
class agent:
    pass

def leadership():
    import random as rand
    rn=randint(100)
    if rn>97:
        return 1
    else:
        return 0

def initialize():
    import random as rand
    global agents
    global grp_num
    global grp
    global indv
    count=0
    grp_num=[]
    grp={}
    agents = []
    for i in range(n):
        ag = agent()
        ag.id=i
        ag.grpid='None'
        ag.x =random()
        ag.y =random()
        ag.leader=leadership()
        #ag.leader=0
        agents.append(ag)
    
    global img,fig
    # global image_path
    img=plt.imread("C:/Users/NITISH/Desktop/mars-min.jpg")
    fig=plt.figure()
    
def imscatter(x, y, image, ax=None, zoom=1):
    if ax is None:
        ax = plt.gca()
    try:
        image = plt.imread(image)
    except TypeError:
        # Likely already an array...
        pass
    im = matplotlib.offsetbox.OffsetImage(image, zoom=zoom)
    x, y = np.atleast_1d(x, y)
    artists = []
    for x0, y0 in zip(x, y):
        ab = matplotlib.offsetbox.AnnotationBbox(im, (x0, y0), xycoords='data', frameon=False)
        artists.append(ax.add_artist(ab))
    ax.update_datalim(np.column_stack([x, y]))
    ax.autoscale()
    return artists

def observe():
    global agents
    global indv
    cla()
    
    ax1=fig.add_subplot(111,label='1',frame_on=False)
    ax0=fig.add_subplot(111,label='2',frame_on=False)
    ax1.imshow(img,aspect='auto')
    ax1.set_axis_off()
    #black = [ag for ag in agents if ag.leader == 0]
    global leaders
    leaders = [ag for ag in agents if ag.leader !=0]
    # global image_path
    image_path = get_sample_data("C:/Users/NITISH/Desktop/ast.png")
    imscatter([ag.x for ag in agents], [ag.y for ag in agents], image_path, zoom=0.2,ax=ax0)
    ax0.plot([ag.x for ag in agents], [ag.y for ag in agents],'ko')
    #ax0.plot([ag.x for ag in leaders], [ag.y for ag in leaders],'bo',markersize=8)
    #axis([0,1,0,1])
    plt.show()
    

def likematrix():
    import random as rand
    global like
    like=[]
    for i in range(n):
        temp=[]
        for j in range(n):
            temp.append(randint(-2,3))
        like.append(temp)

            
            

                    
            
def movement(grp):
    import random as rand
    for num in grp_num:
        group=grp['grp'+str(num)]
        for i in range(1,len(group)):
            group[i].x+=rand.choice([0.003,-0.002,0.001,0.005,-0.001,-0.006,])
            group[i].y+=rand.choice([0.001,-0.001,0.002,-0.0025,0.001,-0.001])
    

                    
def grp_wleader(ag,neighbors):
    import random as rand
    if len(neighbors) > 0:
        if ag.grpid=='None':
                ag.grpid=len(grp)+1
                grp_num.append(ag.grpid)
                grp['grp'+str(ag.grpid)]=[ag]
        for nb in neighbors:
            l_an=like[ag.id][nb.id]
            l_na=like[nb.id][ag.id]+ag.leader
            
            if nb.grpid =='None':
                if l_an>=0 and l_na>=0:
                    grp_meb=grp['grp'+str(ag.grpid)]
                    nb.grpid=ag.grpid
                    grp_meb.append(nb)
                    ldr=grp_meb[0]
                    nb.x,nb.y = ag.x+rand.choice([0.03,-0.02,0.01,0.05,-0.01,-0.06,]),ag.y+rand.choice([0.01,-0.01,0.02,-0.025,0.01,-0.1])
                else:
                    nb.x, nb.y = random(),random()
            
                
                    
     
    


def update():
    likematrix()
    global agents
    global like
    global count
    count+=1
    ag = agents[randint(n)]
    neighbors = [nb for nb in agents if (ag.x - nb.x)**2 + (ag.y - nb.y)**2 < r**2 and nb != ag]
    grp_wleader(ag,neighbors)
    
    #movement(grp)
    
    
    
            
import pycxsimulator
pycxsimulator.GUI().start(func=[initialize, observe, update])