
import numpy as np
import matplotlib.pyplot as plt
from data_type import Sites,Arc,Segment
#All the points will already be of class points with events ="sites"
def Voronoi(points):
    #sort the points descending by y coordinates
    Binary_Tree=Arc()
    def myFunc(e):
        return e.y
    points.sort(key=myFunc,reverse=True)

    while len(points)!=0:
        point=points.pop(0)
        if(point.event=="site"):
            site_events(point,Binary_Tree)
        else:
            circle_events(point)

def site_events(point,Binary_Tree):
    if(Binary_Tree.sleft==None):
        Binary_Tree.sleft=point
    elif(Binary_Tree.sleft!=None and Binary_Tree.sright==None):
        if(Binary_Tree.sleft.x>point.x):
            Binary_Tree.sright=Binary_Tree.sleft
            Binary_Tree.sleft=point
def intersection(p0,p1,l):
    if(p0.x==p1.x):
        py=(p0.y +p1.y)/2.0
    else:
        #use quadratic formula
        # we just have to compute a b and c which are the value of the parabola ax²+bx+c and use them in the formula
        a0=0.5*1/(p0.x-l)
        b0=0.5*1/(p0.x-l)*(-2)*p0.x
        c0=(p0.x**2)*(p0.y**2)*(l**2)
        a1=0.5*1/(p1.x-l)
        b1=0.5*1/(p1.x-l)*(-2)*p1.x
        c1=(p1.x**2)*(p1.y**2)*(l**2)
        a=a1-a0
        b=b1-b0
        c=c1-c0
        #compute the 2 possibl intersections
        x1=(-b-((b**2)-4*a*c)**0.5)/2*a
        x2=(-b+((b**2)-4*a*c)**0.5)/2*a



def circle_events(point):
    print("circle")
