
import numpy as np
import matplotlib.pyplot as plt
from data_type import Sites,Arc,Segment
#All the points will already be of class points with events ="sites"
def Voronoi(points):
    #sort the points descending by y coordinates
    segment=[]
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
            detect_circle_event(Binary_Tree,Binary_Tree.sleft)
        else:
            #In case the new point has 2 intersection with an other point we complete the node and add a new one
            Binary_Tree.sright=point
            Binary_Tree.arcright=Arc(point,Binary_Tree.sleft,parent=Binary_Tree)
            Binary_Tree.arcright.arcleft=Arc(None,point,parent=Binary_Tree.arcright)
            Binary_Tree.arcright.arcright=Arc(Binary_Tree.sleft,None,parent=Binary_Tree.arcright)
            detect_circle_event(Binary_Tree,Binary_Tree.sleft,Binary_Tree.sleft)
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
            detect_circle_event(Binary_Tree,None,Binary_Tree.sright)
        else:
            #In case the new point has 2 intersection with an other point we complete the node and add a new one
            Binary_Tree.sleft=point
            Binary_Tree.arcleft=Arc(Binary_Tree.sright,point,parent=Binary_Tree)
            Binary_Tree.arcleft.arcright=Arc(point,None,parent=Binary_Tree.arcleft)
            Binary_Tree.arcleft.arcleft=Arc(None,Binary_Tree.sright,parent=Binary_Tree.arcleft)
            #Will try to find circle event on the left and right side f the point
            detect_circle_event(Binary_Tree,Binary_Tree.sright,Binary_Tree.sright)
    elif(Binary_Tree.sleft!=None and Binary_Tree.sright!=None):
        if(Binary_Tree.sleft.x>point.x):
            site_events(point,Binary_Tree.arcleft)
        elif(Binary_Tree.sright.x<point.x):
            site_events(point,Binary_Tree.arcright)
        else:
            #peut être réduire l?
            s1,s2=intersection(Binary_Tree.sright,point,point.y-1)
            s3,s4=intersection(Binary_Tree.sleft,point,point.y-1)
            #worst case possible : we have a point between 2 other points an need to modify the decision tree
            #if the new point intersect the 2 sites
            #ATTENTION CEUX CAS PEU ETRE FAUX CAR UN NOUVEAU POINT NE PEUX CROISER DEUX DES LE DEBUT
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
                c1,c2=detect_circle_event(Binary_Tree,Binary_Tree.sleft,Binary_Tree.sright,point)
                return compute_circle(Binary_Tree.sleft,Binary_Tree.sright,point),c1,c2
            elif(s1!=None):
                #if the point intersect only one site
                arcleft=Binary_Tree.arcleft
                Binary_Tree.sleft=point
                Binary_Tree.arcleft=Arc(Binary_Tree.sright,point,parent=Binary_Tree)
                Binary_Tree.arcleft.arcright=Arc(point,None,parent=Binary_Tree.arcleft)
                Binary_Tree.arcleft.arcleft=Arc(arcleft.sright, Binary_Tree.arcleft.sleft,parent=Binary_Tree.arcleft)
                arcleft.parent=Binary_Tree.arcleft.arcleft
                Binary_Tree.arcleft.arcleft.arcleft=arcleft
                Binary_Tree.arcleft.arcleft.arcright=Arc(Binary_Tree.arcleft.arcleft.sright,None,parent=Binary_Tree.arcleft.arcleft)
                detect_circle_event(Binary_Tree,None,Binary_Tree.sright)
            elif(s3!=None):
                arcleft=Binary_Tree.arcleft
                Binary_Tree.arcleft=Arc(point,Binary_Tree.sleft,parent=Binary_Tree)
                Binary_Tree.arcleft.arcright=Arc(Binary_Tree.sleft,None,parent=Binary_Tree.arcleft)
                Binary_Tree.arcleft.arcleft=Arc(arcleft.sright, Binary_Tree.arcleft.sleft,parent=Binary_Tree.arcleft)
                Binary_Tree.arcleft.arcright=Arc(point,None,parent=Binary_Tree.arcleft)
                arcleft.parent=Binary_Tree.arcleft.arcleft
                Binary_Tree.arcleft.arcleft.arcleft=arcleft
                detect_circle_event(Binary_Tree,Binary_Tree.sleft)


                    
                


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



def compute_circle(p1,p2,p3,arc):
    #the formula:http://www.ambrsoft.com/trigocalc/circle3d.htm
    #compute the center of the circle
    A=(2*(p1.x(p2.y-p3.y)-p1.y(p2.x-p3.x)+p2.x*p3.y-p3.x*p2.y))
    B=((p1.x**2+p1.y**2)(p3.y-p2.y)+(p2.x**2+p2.y**2)(p1.y-p3.y)+(p3.x**2+p3.y**2)(p2.y-p1.y))
    C=((p1.x**2+p1.y**2)(p2.x-p3.x)+(p2.x**2+p2.y**2)(p3.x-p1.x)+(p3.x**2+p3.y**2)(p1.x-p2.x))
    D=((p1.x**2+p1.y**2)(p3.x*p2.y-p3.y*p2.x)+(p2.x**2+p2.y**2)(p1.x*p3.y-p1.y*p3.x)+(p3.x**2+p3.y**2)(p2.x*p1.y-p1.xp2.y))
    x=-(B/A)
    y=-(C/A)
    #compute the radius of the circle
    r=((B**2+C**2-4*A*D)/(2*A**2))**0.5
    c1=Sites(x,y-r,"circle",arc)
    return c1
def detect_circle_event(Binary_Tree,pleft=None,pright=None,pmiddle=None):
    # we have an intersection on the right side of the point and we are going to see if there is a risk a disapearing
    if(pleft!=None and pright==None and pmiddle==None):
        a=False
        Tree=Binary_Tree
        arc1=None
        arc2=None
        while(a==False):
            if(Tree.sleft.x>pleft.x):
                Tree=Tree.arcleft
            elif(Tree.sright.x<pleft.x):
                Tree=Tree.arcright
            elif(Tree.sright.x==pleft.x):
                a==True
                arc1=Tree
                if(Tree.arcright.sleft.x==pleft.x):
                    arc2=Tree.arcright
                else:
                    arc2=Tree.parent
            else:
                a==True
        if(arc1==None):
            return None
        else:
            #if we found out that there is also an intersection on the left side it means that there is a circle event
            return compute_circle(arc1.sleft,arc1.sright,arc2.sright,[arc1,arc2])
    elif(pleft==None and pright!=None and pmiddle==None):
        #If we find an intersection on the left side of the point
        a=False
        Tree=Binary_Tree
        arc1=None
        arc2=None
        while(a==False):
            if(Tree.sleft.x>pright.x):
                Tree=Tree.arcleft
            elif(Tree.sright.x<pright.x):
                Tree=Tree.arcright
            elif(Tree.sleft.x==pright.x):
                a==True
                arc1=Tree
                if(Tree.arcleft.sright.x==pright.x):
                    arc2=Tree.arcleft
                else:
                    arc2=Tree.parent
            else:
                a==True
        if(arc1==None):
            return None
        else:
            #if we found out that there is also an intersection on the left side it means that there is a circle event
            return compute_circle(arc1.sleft,arc1.sright,arc2.sleft,[arc1,arc2])
    #Not sure if it usefull
    elif(pleft!=None and pright!=None):
        #In the case where the new point has an intersection with 2 points we need to check for the left and right point
        c1=detect_circle_event(Binary_Tree,pleft)
        c2=detect_circle_event(Binary_Tree,None,pright)
        return c1,c2
