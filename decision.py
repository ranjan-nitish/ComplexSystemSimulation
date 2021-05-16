# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 16:34:00 2021

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
r = 0.5 # neighborhood radius
 
count=0

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
        return rand.uniform(0,10)
    else:
        return 0

def initialize():
    import random as rand
    global agents
    global grp_num
    global grp
    global indv
    global ldr
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
        ag.religion=randint(10)
        ag.eco=randint(10)
        #ag.leader=0
        agents.append(ag)
    indv=agents.copy()
    ldr=[ag for ag in agents if ag.leader != 0]
    global fig,ax0,ax1
    fig, (ax0) = plt.subplots(1,gridspec_kw={'width_ratios': [1]})
    ax0.set_xlim([-1, len(ldr)])
    ax0.set_ylim([0, n])
    
    
def observe():
    import random as rand
    global agents
    global indv
    cla()
    black = [ag for ag in indv if ag.leader == 0]
    
    leaders = [ag for ag in indv if ag.leader !=0]
    plt.scatter([ag.x for ag in black], [ag.y for ag in black],c='k',s=60)
    plt.scatter([ag.x for ag in leaders], [ag.y for ag in leaders],c='b',s=100)
    plt.show()

    for num in grp_num:
        global count
        group=grp['grp'+str(num)]
        plt.scatter(group[1].x,group[1].y,c=group[0],s=(100+20*len(group)))
        plt.show()
   
    if count==15:
        draw_bar(grp,ax0)
        
        
        
    
        
    
#gennerating like matrix for each agent
def likematrix():
    import random as rand
    global like
    like=[]
    for i in range(n):
        temp=[]
        for j in range(n):
            temp.append(rand.uniform(0,10))
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
def find_element(grp,nb):
    for i in range(1,len(grp)):
        if grp[i].id == nb.id:
            del grp[i]
        
def draw_bar(grp,ax0):
    x=[]
    y=[]
    for i in range(len(grp)):
        name='Leader'+str(i+1)
        x.append(name)
        y.append(len(grp['grp'+str(i+1)]))
    ax0.bar(x,y)
    ax0.ylabel("Supporting Voters")
                    
            
def grp_leader(ag,neighbors):
    import random as rand
    #only leader or agent belonging to any grp can make group initiation
    if ag.leader!= 0  :
        if len(neighbors)>0 :
            global indv
            #assigning group id to leader for the first time
            if ag.grpid=='None':
                ag.grpid=len(grp)+1
                grp_num.append(ag.grpid)
                col=color[ag.grpid]
                grp['grp'+str(ag.grpid)]=[col,ag]
            
                
                indv.remove(ag)
                
            for nb in neighbors:
                if nb.leader==0:
                    l_grp=like_for_grp(nb)# like of neighbour for the group of interacting agent
                
                    l_na=like[nb.id][ag.id]+ag.leader#like of neighbour towards agent
                    if nb.religion>=ag.religion:
                        relg=nb.religion
                    else:
                        relg=0
                    if ag.eco>nb.eco:
                        ecostatus=nb.eco
                    else:
                        ecostatus=0
                    th=(0.1*l_grp)+(0.2*l_na)+(0.2*relg)+(0.5*ecostatus)
                    print(th)
                    
                    if th>=4:
                        if nb.grpid=='None':
                            nb.grpid=ag.grpid
                        else:
                            old_grp=grp['grp'+str(nb.grpid)]
                            old_grp.remove(nb)
                            nb.grpid=ag.grpid
                            
                        grp['grp'+str(ag.grpid)].append(nb)
                        if nb in indv:    
                            indv.remove(nb)
                        ldr=grp['grp'+str(ag.grpid)][1]
                        #considering boundary condition so that agent doesn't go beyond frame
                        if nb.x>1 and nb.x<5 and nb.y>1 and nb.y<5:
                            nb.x,nb.y = ldr.x+rand.choice([0.3,-0.2,0.1,0.5,-0.1,-0.6,]),ldr.y+rand.choice([0.1,-0.1,0.2,-0.25,0.4,-0.032])
                        else:
                            nb.x,nb.y = ldr.x+rand.choice([0.3,0.1,0.5,-0.1]),ldr.y+rand.choice([0.1,0.2,0.4,-0.032])
                    else:
                        nb.x, nb.y = rand.uniform(0.0,6.0), rand.uniform(0.0,6.0)
                
    
        else:
            ag.x , ag.y =rand.uniform(0.0,6.0), rand.uniform(0.0,6.0)
        
            
            
            
    elif ag.leader==0:
        ag.x , ag.y =rand.uniform(0.0,6.0), rand.uniform(0.0,6.0)
            
                    
            
def movement(grp):
    import random as rand
    global count
    for num in grp_num:
        group=grp['grp'+str(num)]
        global count
        if len(group) >1:
            group[1].x+=rand.uniform(-0.2,0.2)
            group[1].y+=rand.uniform(-0.2,0.2)
            if group[1].x<0:
                group[1].x+=1
                if group[1].y<0:
                    group[1].y+=1
                elif group[1].y>6:
                    group[1].y-=1
            elif group[1].x>6:
                group[1].x-=1
                if group[1].y<0:
                    group[1].y+=1
                elif group[1].y>6:
                    group[1].y-=1
            if group[1].y<0:
                group[1].y+=1
                if group[1].x<0:
                    group[1].x+=1
                elif group[1].x>6:
                    group[1].x-=1
            elif group[1].y>6:
                group[1].y-=1
                if group[1].x<0:
                    group[1].x+=1
                elif group[1].x>6:
                    group[1].x-=1
                
                
    

                    



def update():
    likematrix()
    global agents
    global like
    global count;global indv;
    global grp;global ldr
    count+=1
    ag = ldr[randint(len(ldr)-1)]
    neighbors = [nb for nb in agents if (ag.x - nb.x)**2 + (ag.y - nb.y)**2 < r**2 and nb != ag]
    grp_leader(ag,neighbors)
    if count <2000:
        movement(grp)
    if count==1000:
        for id in grp_num:
            ledr=grp['grp'+str(id)][1]
            print(ledr.leader)
        print(len(indv))
    
        
    
        
    
    
    
            
import pycxsimulator
pycxsimulator.GUI().start(func=[initialize, observe, update])