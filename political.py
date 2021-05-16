# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 16:34:00 2021

@author: NITISH
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 18:11:05 2021

@author: NITISH
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 16:16:31 2021

@author: NITISH
"""

import random as rand
from random import choice,uniform,randint
import matplotlib
matplotlib.use('TkAgg')
from pylab import *
import numpy
import matplotlib.pyplot as plt
n =250 # number of agents
r = 0.45 # neighborhood radius
 
count=0
growth={}
time={}
number_of_colors = 20
import random
color=[]
#color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
             #for i in range(number_of_colors)]
#color=['go','ro','co','mo','yo','bo']
color=[]
for i in range(number_of_colors):
    col="#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
    if col not in color:
        color.append(col)
class agent:
    pass

def leadership():
    import random as rand
    rn=randint(100)
    if rn>96:
        return rand.uniform(1.0,4.0)
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
        ag.x =rand.uniform(0.2,5.8)
        ag.y =rand.uniform(0.2,5.8)
        ag.leader=leadership()
        #ag.leader=0
        agents.append(ag)
    indv=agents.copy()
    global fig
    global ax3
    fig, (ax3) = plt.subplots(1,gridspec_kw={'width_ratios': [1]})
    
def observe():
    import random as rand
    global agents
    global indv;global fig,ax0,ax1
    cla()
    '''ax1=fig.add_subplot(111,label='1')
    ax0=fig.add_subplot(121,label='2')'''
    black = [ag for ag in indv if ag.leader == 0]
    global leaders
    leaders = [ag for ag in indv if ag.leader !=0]
    plt.scatter([ag.x for ag in black], [ag.y for ag in black],c='k',s=60)
    plt.scatter([ag.x for ag in leaders], [ag.y for ag in leaders],c='b',s=100)
    plt.show()
    for num in grp_num:
        global count
        group=grp['grp'+str(num)]
        plt.scatter(group[1].x,group[1].y,c=group[0],s=(100+20*len(group)))
        plt.show()
        
        
    
    if len(growth)!=0 and len(time)!=0 and count==1500:
        for i in range(1,len(growth)+1):
            ax3.plot(time['grp'+str(i)],growth['grp'+str(i)])
            plt.show()
        
        
    
#gennerating like matrix for each agent
def likematrix():
    import random as rand
    global like
    like=[]
    for i in range(n):
        temp=[]
        for j in range(n):
            temp.append(rand.uniform(-3.0,4.0))
        like.append(temp)
        
def like_for_grp(ag):
    if ag.grpid=='None':
        return 0
    else:
        glike=0
        temp=grp['grp'+str(ag.grpid)]
        for i in range(1,len(temp)):
            glike+=like[ag.id][temp[i].id]
        return glike/len(temp)
            
            
def grp_pol_leader(ag,neighbors):
    import random as rand
    #only leader or agent belonging to any grp can make group initiation
    if ag.leader!= 0 or ag.grpid != 'None':
        if len(neighbors)>0:
            global indv
            #assigning group id to leader for the first time
            if ag.grpid=='None':
                ag.grpid=len(grp)+1
                grp_num.append(ag.grpid)
                col=color[ag.grpid]
                grp['grp'+str(ag.grpid)]=[col,ag]
                growth['grp'+str(ag.grpid)]=[1]
                time['grp'+str(ag.grpid)]=[count]
                indv.remove(ag)
                            
            
            
            for nb in neighbors:
                l_grp=like_for_grp(nb)# like of neighbour for the group of interacting agent
                l_an=like[ag.id][nb.id]+ag.leader#like of agent towards neighbour
                l_na=like[nb.id][ag.id]+ag.leader#like of neighbour towards agent
                
                            
                if nb.grpid=='None':
                    if min(l_an,l_na,l_grp)>=0:
                        nb.grpid=ag.grpid
                        grp['grp'+str(ag.grpid)].append(nb)
                        
                        indv.remove(nb)
                        ldr=grp['grp'+str(ag.grpid)][1]
                        #considering boundary condition so that agent doesn't go beyond frame
                        if nb.x>1 and nb.x<5 and nb.y>1 and nb.y<5:
                            nb.x,nb.y = ldr.x+rand.choice([0.3,-0.2,0.1,0.5,-0.1,-0.6,]),ldr.y+rand.choice([0.1,-0.1,0.2,-0.25,0.4,-0.032])
                        else:
                            nb.x,nb.y = ldr.x+rand.choice([0.3,0.1,0.5,-0.1]),ldr.y+rand.choice([0.1,0.2,0.4,-0.032])
                            
                    else:
                        nb.x, nb.y = rand.uniform(0.0,6.0), rand.uniform(0.0,6.0)
                elif nb.leader==0:
                    #consideing depriciation or increase in like of agent for thier own grp
                    l_own_grp=like_for_grp(nb)+rand.choice([0.3,-0.2,0.,0.5,-0.1,-0.6,])
                    ldr_n=grp['grp'+str(nb.grpid)][1]
                    l_own_leader=like[nb.id][ldr_n.id]+ldr_n.leader+rand.choice([0.3,-0.2,0.,0.5,-0.1,-0.6,])
                    if l_grp>l_own_grp and l_na>l_own_leader:
                        grp['grp'+str(nb.grpid)].remove(nb)
                        nb.grpid=ag.grpid
                        grp['grp'+str(ag.grpid)].append(nb)
                        ldr=grp['grp'+str(ag.grpid)][1]
                        nb.x,nb.y = ldr.x+rand.choice([0.3,0.2,0.1,0.5,-0.1,0.6,]),ldr.y+rand.choice([0.1,-0.1,0.2,-0.25,0.4,-0.3])
                        
    elif ag.leader==0:
        ag.x , ag.y =rand.uniform(0.0,6.0), rand.uniform(0.0,6.0)
                    
            
def movement(grp):
    import random as rand
    global count
    for num in grp_num:
        group=grp['grp'+str(num)]
        for i in range(1,len(group)):
            if i!=1: 
                group[i].x+=rand.choice([0.03,-0.02,0.01,0.05,-0.01,-0.06,])
                group[i].y+=rand.choice([0.01,-0.01,0.02,-0.025,0.01,-0.01])
            elif count/10 ==0:
                group[i].x+=rand.choice([0.003,-0.02,0.01,0.05,-0.01,-0.006,])
                group[i].y+=rand.choice([0.001,-0.01,0.02,-0.025,0.01,-0.01])
                
                
    
def coalition(leaders,neighbors):
    pass
                    



def update():
    likematrix()
    global agents
    global like
    global count;global indv;
    global grp;global time
    count+=1
    ag = agents[randint(n)]
    neighbors = [nb for nb in agents if (ag.x - nb.x)**2 + (ag.y - nb.y)**2 < r**2 and nb != ag]
    grp_pol_leader(ag,neighbors)
    movement(grp)
    if count==1000:
        for id in grp_num:
            ldr=grp['grp'+str(id)][1]
            print(ldr.leader)
        print(len(indv))
    if len(grp) != 0 :
        for k in grp_num:
            size=growth['grp'+str(k)]
            size.append(len(grp['grp'+str(k)]))
            time['grp'+str(k)].append(count)
        
    
    
    
            
import pycxsimulator
pycxsimulator.GUI().start(func=[initialize, observe, update])