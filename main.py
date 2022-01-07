
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
#TODO ADD the Circle event and the return of segment
def site_events(point,Binary_Tree):
    if(Binary_Tree.sleft==None and Binary_Tree.sright==None):
        #When we create a node we need also to a child node
        Binary_Tree.sleft=point
        Binary_Tree.arcleft=Arc(None,point)
    elif(Binary_Tree.sleft!=None and Binary_Tree.sright==None):
        s1,s2=intersection(Binary_Tree.sleft,point)
        #in case of one intersection
        if(s2==None):
            if(Binary_Tree.sleft.x>point.x):
                #We need to switch points 
                Binary_Tree.sright=Binary_Tree.sleft
                Binary_Tree.sleft=point
                #We need to also permute the arc and also permute the value inside the arc because <None,p1>--<p1,None> =><None,p2>--<p2,p1>--<p1,None>
                Binary_Tree.arcright=Binary_Tree.arcleft
                Binary_Tree.arcright.sleft=Binary_Tree.arcright.sright
                Binary_Tree.arcright.sright=None
                Binary_Tree.arcleft=Arc(None,point,parent=Binary_Tree)
            else:
                Binary_Tree.sright=point
                Binary_Tree.arcright=Arc(point,None,parent=Binary_Tree)
        else:
            #In case the new point has 2 intersection with an other point we complete the node and add a new one
            Binary_Tree.sright=point
            Binary_Tree.arcright=Arc(point,Binary_Tree.sleft,parent=Binary_Tree)
            Binary_Tree.arcright.arcleft=Arc(None,point,parent=Binary_Tree.arcright)
            Binary_Tree.arcright.arcright=Arc(Binary_Tree.sleft,None,parent=Binary_Tree.arcright)
    elif(Binary_Tree.sleft==None and Binary_Tree.sright!=None):
        s1,s2=intersection(Binary_Tree.sright,point)
        if(s2==None):
            if(Binary_Tree.sright.x<point.x):
                Binary_Tree.sleft=Binary_Tree.sright
                Binary_Tree.sright=point
                #We need to also permute the arc and also permute the value inside the arc because <None,p1>--<p1,None> =><None,p2>--<p2,p1>--<p1,None>
                Binary_Tree.arcleft=Binary_Tree.arcright
                Binary_Tree.arcleft.sright=Binary_Tree.arcleft.sleft
                Binary_Tree.arcleft.sleft=None
                Binary_Tree.arcright=Arc(None,point,parent=Binary_Tree)
            else:
                Binary_Tree.sleft=point
                Binary_Tree.arcleft=Arc(None,point,parent=Binary_Tree)
        else:
            #In case the new point has 2 intersection with an other point we complete the node and add a new one
            Binary_Tree.sleft=point
            Binary_Tree.arcleft=Arc(Binary_Tree.sright,point,parent=Binary_Tree)
            Binary_Tree.arcleft.arcright=Arc(point,None,parent=Binary_Tree.arcleft)
            Binary_Tree.arcleft.arcleft=Arc(None,Binary_Tree.sright,parent=Binary_Tree.arcleft)
    elif(Binary_Tree.sleft!=None and Binary_Tree.sright!=None):
        if(Binary_Tree.sleft.x>point.x):
            site_events(point,Binary_Tree.arcleft)
        elif(Binary_Tree.sright.x<point.x):
            site_events(point,Binary_Tree.arcright)
        else:
            s1,s2=intersection(Binary_Tree.sright,point)
            s3,s4=intersection(Binary_Tree.sleft,point)
            #worst case possible : we have a point between 2 other points an need to modify the decision tree
            #if the new point intersect the 2 sites 
            if(s2==None and s4==None):
                #if one of the 2 sites is in the extreme we just have to push it
                if(Binary_Tree.arcright.sright==None):
                    old_point=Binary_Tree.sright
                    Binary_Tree.sright=point
                    Binary_Tree.arcright.sright=old_point
                    Binary_Tree.arcright.sleft=point
                    Binary_Tree.arcright.arcright=Arc(old_point,None,parent=Binary_Tree.arcright)
                    Binary_Tree.arcright.arcleft=Arc(None,point,parent=Binary_Tree.arcright)
                elif(Binary_Tree.arcleft.sleft==None):
                    old_point=Binary_Tree.sleft
                    Binary_Tree.sleft=point
                    Binary_Tree.arcleft.sleft=old_point
                    Binary_Tree.arcleft.sright=point
                    Binary_Tree.arcleft.arcleft=Arc(None,old_point,parent=Binary_Tree.arcleft)
                    Binary_Tree.arcleft.arcleft=Arc(point,None,parent=Binary_Tree.arcleft)
                else:
                    #most complex cases : the point is in the middle of the three
                    old_point=Binary_Tree.sright
                    Binary_Tree.sright=point
                    a=False
                    RTree=Binary_Tree
                    LTree=Binary_Tree
                    while(a==False):
                        if(RTree.arcright!=None):    
                            RTree=RTree.arcright
                            RTree.arcleft.sright=point
                            RTree.sleft=point
                            point=old_point
                            old_point=RTree.sright
                            RTree.sright=point
                        else:
                            RTree.arcright=Arc(point,None,parent=RTree)
                            a=True
                    while(RTree.parent!=None):
                        RTree=RTree.parent
                    Binary_Tree=RTree
            elif(s2!=None and s1!=None):
                arcleft=Binary_Tree.arcleft
                Binary_Tree.sleft=point
                Binary_Tree.arcleft=Arc(Binary_Tree.sright,point,parent=Binary_Tree)
                Binary_Tree.arcleft.arcright=Arc(point,None,parent=Binary_Tree.arcleft)
                Binary_Tree.arcleft.arcleft=Arc(arcleft.sright, Binary_Tree.arcleft.sleft,parent=Binary_Tree.arcleft)
                arcleft.parent=Binary_Tree.arcleft.arcleft
                Binary_Tree.arcleft.arcleft.arcleft=arcleft
                Binary_Tree.arcleft.arcleft.arcright=Arc(Binary_Tree.arcleft.arcleft.sright,None,parent=Binary_Tree.arcleft.arcleft)
            elif(s3!=None and s4!=None):
                arcleft=Binary_Tree.arcleft
                Binary_Tree.arcleft=Arc(point,Binary_Tree.sleft,parent=Binary_Tree)
                Binary_Tree.arcleft.arcright=Arc(Binary_Tree.sleft,None,parent=Binary_Tree.arcleft)
                Binary_Tree.arcleft.arcleft=Arc(arcleft.sright, Binary_Tree.arcleft.sleft,parent=Binary_Tree.arcleft)
                arcleft.parent=Binary_Tree.arcleft.arcleft
                Binary_Tree.arcleft.arcleft.arcleft=arcleft


                    
                


def intersection(p0,p1,l):
    if(p0.x==p1.x):
        py=(p0.y +p1.y)/2.0
    else:
        #use quadratic formula
        # we just have to compute a b and c which are the value of the parabola ax²+bx+c and use them in the formula
        #a0,b0 and c0 are the parameters of the parabola for the point p0 (look at the lessons)
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
        #compute the y intersection
        if(x1!=x2):
            y1=a*x1**2+b*x1+c
            y2=a*x2**2+b*x1+c
            # if i have 2 intersection between 2 points it means that i have a circle event
            return Segment(Sites(x1,y1)),Segment(Sites(x2,y2))
        else:
            y1=a*x1**2+b*x1+c
            return Segment(Sites(x1,y1)), None



def circle_events(point):
    print("circle")
