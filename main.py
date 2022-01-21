import numpy as np
import matplotlib.pyplot as plt
from data_type import Sites,Arc,Segment,Point
import cmath
import copy
#All the points will already be of class points with events ="sites"
def Voronoi(points):
    #sort the points descending by y coordinates
    segment=[]
    Binary_Tree=Arc()
    def myFunc(e):
        return e.y
    list_point=[]
    points.sort(key=myFunc,reverse=True)
    while len(points)!=0:
        list_circle=[]
        point=points.pop(0)
        if(point.event=="site"):
            list_point.append(point)
            list_circle=site_events(point,Binary_Tree,segment)        
            if(list_circle!=None):
                print(list_circle)
                index=0
                for i in range(len(list_circle)):
                    if(len(points)!=0):
                        for j in range(len(points)):
                            if(list_circle[i].y>points[j].y):
                                index=j
                            if(j!=0):
                                points.insert(j-1,list_circle[i])
                            else:
                                point=points[0]
                                points[0]=list_circle[i]
                                points.insert(0,point)
                    else:
                        for i in range(len(list_circle)):
                            points.append(list_circle[i])
        else:
            print("circle event")
            Binary_Tree=circle_events(point,segment,Binary_Tree)
    #We need to close the segments
    list_seg_x=[]
    list_seg_y=[]
    for i in range(len(segment)):
        print(segment[i].arc.sleft.x,segment[i].arc.sright.x)
        #find 2 points that intersect the segment
        s1,s2=intersection(Point(segment[i].arc.sleft.x,segment[i].arc.sleft.y),Point(segment[i].arc.sright.x,segment[i].arc.sright.y),0)
        #find the constant a and b to compute ax+b
        a=(s1.y-s2.y)/(s1.x-s2.x)
        b=s1.y-a*s1.x
        #segment[i].start=Point(0,b)
        #segment[i].end=Point(50,a*50+b)

        if(len(segment)>1 and segment[i].end==None):
            seg=None
            j=1
            print(i)
            while(segment[i-j].end==None):
                print(segment[i-j].end)
                print(j)
                j+=1
            seg=segment[i-j]
            y=cmath.sqrt((segment[i].start.x.real)**2+(segment[i].start.x.imag)**2)
            if(a<0  and y.real<seg.start.y):
                segment[i].end=Point(50,a*50+b)
            elif(a>0  and y.real<seg.start.y):
                segment[i].end=Point(0,b)
            elif(a>0  and y.real>seg.start.y):
                segment[i].end=Point(50,a*50+b)
            else:
                segment[i].end=Point(0,b)
        elif(len(segment)==1):
            if(a>0):
                segment[i].start=Point(0,b)
                segment[i].end=Point(50,a*50+b)
            else:
                segment[i].end=Point(0,b)
                segment[i].start=Point(50,a*50+b)
        else:
            if(i<len(segment) and segment[i].end.x==segment[i+1].start.x or i!=0 and segment[i].end.x==segment[i-1].end.x or i<len(segment) and segment[i].end.x==segment[i+1].end.x):
                if(a<0):
                    print("1")
                    segment[i].start=Point(0,b)
                else:
                    print("2")
                    segment[i].start=Point(50,a*50+b)
            else:
                if(a>0):
                    print("3")
                    segment[i].start=Point(0,b)
                    segment[i].end=Point(50,a*50+b)
                else:
                    print("4")
                    segment[i].end=Point(0,b)
                    segment[i].start=Point(50,a*50+b)
        list_seg_x.append([segment[i].start.x,segment[i].end.x])
        list_seg_y.append([segment[i].start.y,segment[i].end.y])
    x=[]
    y=[]
    plt.figure() 
    for point in list_point:
        x.append(point.x)
        y.append(point.y)
    #plot the points 
    plt.xlim([0, 50])
    plt.ylim([0, 50])
    for i in range(len(x)):
        plt.plot(x[i],y[i],'o', color='black')
    for i in range(len(list_seg_x)):
        plt.plot(list_seg_x[i],list_seg_y[i])
    plt.show()

        
    


            

#TODO ADD the Circle event and the return of segment
def site_events(point,Binary_Tree,segment):
    if(len(segment)>0):
        print(point.x)
        print(segment[0].arc.sleft.x,segment[0].arc.sright.x)
    if(Binary_Tree.sleft==None and Binary_Tree.sright==None):
        #When we create a node we need also to a child node
        Binary_Tree.sleft=point
        Binary_Tree.arcleft=Arc(None,point)
        Binary_Tree.arcleft.parent=Binary_Tree
        return None
    elif(Binary_Tree.sleft!=None and Binary_Tree.sright==None):
        s1,s2=intersection(Binary_Tree.sleft,point,float(point.y-0.00001))
        if(Binary_Tree.sleft.y==point.y):
            segment.append(Segment(s1,Binary_Tree,s2))
            return None
        if(Binary_Tree.sleft.x==point.x):
            segment.append(Segment(s1,Binary_Tree,s2))
            return None
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
                Binary_Tree.arcright.parent=Binary_Tree
                Binary_Tree.arcleft.parent=Binary_Tree
            else:
                Binary_Tree.sright=point
                Binary_Tree.arcright=Arc(point,None,parent=Binary_Tree)
                Binary_Tree.arcright.parent=Binary_Tree
            segment.append(Segment(s1,Binary_Tree))
            return detect_circle_event(Binary_Tree,Binary_Tree.sleft)
        else:
            #In case the new point has 2 intersection with an other point we complete the node and add a new one
            Binary_Tree.sright=point
            Binary_Tree.arcright=Arc(point,Binary_Tree.sleft,parent=Binary_Tree)
            Binary_Tree.arcright.arcleft=Arc(None,point,parent=Binary_Tree.arcright)
            Binary_Tree.arcright.arcright=Arc(Binary_Tree.sleft,None,parent=Binary_Tree.arcright)
            segment.append(Segment(s1,Binary_Tree))
            segment.append(Segment(s2,Binary_Tree.arcright))
            return detect_circle_event(Binary_Tree,Binary_Tree.sleft,Binary_Tree.sleft)
    elif(Binary_Tree.sleft==None and Binary_Tree.sright!=None):
        print('right')
        s1,s2=intersection(Binary_Tree.sright,point,float(point.y-0.00001))
        if(Binary_Tree.sright.y==point.y):
            segment.append(Segment(s1,Binary_Tree,s2))
            return None
        if(Binary_Tree.sright.x==point.x):
            segment.append(Segment(s1,Binary_Tree,s2))
            return None
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
            segment.append(Segment(s1,Binary_Tree))
            print("detect circle")
            list_c=detect_circle_event(Binary_Tree,None,Binary_Tree.sright)
            print(list_c)
            return list_c 
        else:
            #In case the new point has 2 intersection with an other point we complete the node and add a new one
            Binary_Tree.sleft=point
            Binary_Tree.arcleft=Arc(Binary_Tree.sright,point,parent=Binary_Tree)
            Binary_Tree.arcleft.arcright=Arc(point,None,parent=Binary_Tree.arcleft)
            Binary_Tree.arcleft.arcleft=Arc(None,Binary_Tree.sright,parent=Binary_Tree.arcleft)
            #Will try to find circle event on the left and right side f the point
            segment.append(Segment(s1,Binary_Tree))
            segment.append(Segment(s2,Binary_Tree.arcleft))
            return detect_circle_event(Binary_Tree,Binary_Tree.sright,Binary_Tree.sright)
    elif(Binary_Tree.sleft!=None and Binary_Tree.sright!=None):
        if(Binary_Tree.sleft.x>point.x):
            print("arcleft")
            list_c=site_events(point,Binary_Tree.arcleft,segment)
            return list_c
        elif(Binary_Tree.sright.x<point.x):
            print("arcright")
            list_c=site_events(point,Binary_Tree.arcright,segment)
            return list_c
        else:
            #peut être réduire l?
            s1,s2=intersection(Binary_Tree.sright,point,float(point.y-0.00001))
            s3,s4=intersection(Binary_Tree.sleft,point,float(point.y-0.00001))
            s5,s6=intersection(Binary_Tree.sleft,Binary_Tree.sright,float(point.y-0.00001))
            old_point=None
            #worst case possible : we have a point between 2 other points an need to modify the decision tree
            #if the new point intersect the 2 sites
            #ATTENTION CEUX CAS PEU ETRE FAUX CAR UN NOUVEAU POINT NE PEUX CROISER DEUX DES LE DEBUT
            if(s2==None and s4==None):
                #if one of the 2 sites is in the extreme we just have to push it
                if(Binary_Tree.arcright.sright==None):
                    #TODO faire sa pour chaque cas
                    Tree=copy.deepcopy(Binary_Tree)
                    old_point=Tree.sright
                    Tree.sright=point
                    Tree.arcright.sright=old_point
                    Tree.arcright.sleft=point
                    Tree.arcright.arcright=Arc(old_point,None,parent=Tree.arcright)
                    Tree.arcright.arcleft=Arc(None,point,parent=Tree.arcright)
                    segment[-1].end=s5
                    segment.append(Segment(s5,Tree.arcright))
                    segment.append(Segment(s5,Tree))
                    list_c=detect_circle_event(Binary_Tree,Binary_Tree.sleft,old_point,point)

                    Binary_Tree=Tree
                    print("----")
                    print(Binary_Tree.sright.x)
                elif(Binary_Tree.arcleft.sleft==None):
                    old_point=Binary_Tree.sleft
                    Binary_Tree.sleft=point
                    Binary_Tree.arcleft.sleft=old_point
                    Binary_Tree.arcleft.sright=point
                    Binary_Tree.arcleft.arcleft=Arc(None,old_point,parent=Binary_Tree.arcleft)
                    Binary_Tree.arcleft.arcleft=Arc(point,None,parent=Binary_Tree.arcleft)
                    segment[-1].end=s5
                    segment.append(Segment(s5,Binary_Tree))
                    segment.append(Segment(s5,Binary_Tree.arcleft))
                    list_c=detect_circle_event(Binary_Tree,old_point,Binary_Tree.sright,point)
                else:
                    #most complex cases : the point is in the middle of the three
                    old_point=Binary_Tree.sright
                    Binary_Tree.sright=point
                    arcleft=Binary_Tree
                    a=False
                    RTree=Binary_Tree
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
                    segment[-1].end=s5
                    segment.append(Segment(s5,arcleft.arcright))
                    segment.append(Segment(s5,arcleft))
                    list_c=detect_circle_event(Binary_Tree,Binary_Tree.sleft,old_point,point)
                return list_c
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
                #<p3,p2>--><p2,p3>
                segment.append(Segment(s1,Binary_Tree.arcleft))
                segment.append(Segment(s2,Binary_Tree))
                return detect_circle_event(Binary_Tree,None,Binary_Tree.sright)
            elif(s3!=None):
                arcright=Binary_Tree.arcright
                Binary_Tree.sright=point
                Binary_Tree.arcright=Arc(point,Binary_Tree.sleft,parent=Binary_Tree)
                Binary_Tree.arcright.arcleft=Arc(None,point,parent=Binary_Tree.arcright)
                Binary_Tree.arcright.arcright=Arc( Binary_Tree.arcright.sright,arcright.sleft,parent=Binary_Tree.arcright)
                arcright.parent=Binary_Tree.arcright.arcright
                Binary_Tree.arcright.arcright.arcright=arcright
                #<p1,p2>--><p2,p1>
                segment.append(Segment(s3,Binary_Tree))
                segment.append(Segment(s4,Binary_Tree.arcright))
                return detect_circle_event(Binary_Tree,Binary_Tree.sleft)


                    
                


def intersection(p0,p1,l):
    if(p0.x==p1.x):
        dist=(((p0.y-p1.y)/2.0)**2)**0.5
        if(p0.y<p1.y):
            return Point(0,p0.y+dist),Point(50,p0.y+dist)
        else:
            return Point(0,p1.y+dist),Point(50,p1.y+dist)
    elif(p0.y==p1.y):
        dist=(((p0.x-p1.x)/2)**2)**0.5
        if(p0.x<p1.x):
            return Point(p0.x+dist,0),Point(p0.x+dist,50)
        else:
            return Point(p1.x+dist,0),Point(p1.x+dist,50)  
    else:
        #use quadratic formula
        #https://math.stackexchange.com/questions/2700033/explanation-of-method-for-finding-the-intersection-of-two-parabolas
        #https://math.stackexchange.com/questions/1370231/parabola-equation-in-fortune-algorithm-for-building-voronoi-diagram
        # we just have to compute a b and c which are the value of the parabola ax²+bx+c and use them in the formula
        #a0,b0 and c0 are the parameters of the parabola for the point p0 (look at the lessons)
        a0=0.5*1/(p0.y-l)
        b0=(-2)*p0.x*0.5*1/(p0.y-l)
        c0=((p0.x**2)+(p0.y**2)-(l**2))*0.5*1/(p0.y-l)
        a1=1/(2*(p1.y-l))
        b1=(-2)*p1.x*0.5*1/(p1.y-l)
        c1=((p1.x**2)+(p1.y**2)-(l**2))*0.5*1/(p1.y-l)
        a=a1-a0
        b=b1-b0
        c=c1-c0
        #compute the 2 possibl intersections
        x1=((-1*b)-((b**2)-4*a*c)**0.5)/(2*a)
        x2=((-1*b)+((b**2)-4*a*c)**0.5)/(2*a)
        #compute the y intersection
        #The thing is that it's not possible for x1 and x2 to be equal but they would be very close for example :29.9797595392213 30.020256460778693
        if(x1-x2>1.0 or x2-x1>1.0):
            y1=a1*x1**2+b1*x1+c1
            y2=a1*x2**2+b1*x2+c1
            
            # if i have 2 intersection between 2 points it means that i have a circle event
            return Point(x1,y1),Point(x2,y2)
        else:
            y1=a1*x1**2+b1*x1+c1
            return Point(x1,y1), None



def compute_circle(p1,p2,p3,arc):
    #the formula:http://www.ambrsoft.com/trigocalc/circle3d.htm
    #compute the center of the circle
    A=(2*(p1.x*(p2.y-p3.y)-p1.y*(p2.x-p3.x)+p2.x*p3.y-p3.x*p2.y))
    B=((p1.x**2+p1.y**2)*(p3.y-p2.y)+(p2.x**2+p2.y**2)*(p1.y-p3.y)+(p3.x**2+p3.y**2)*(p2.y-p1.y))
    C=((p1.x**2+p1.y**2)*(p2.x-p3.x)+(p2.x**2+p2.y**2)*(p3.x-p1.x)+(p3.x**2+p3.y**2)*(p1.x-p2.x))
    D=((p1.x**2+p1.y**2)*(p3.x*p2.y-p3.y*p2.x)+(p2.x**2+p2.y**2)*(p1.x*p3.y-p1.y*p3.x)+(p3.x**2+p3.y**2)*(p2.x*p1.y-p1.x*p2.y))
    x=-(B/A)
    y=-(C/A)
    #compute the radius of the circle
    r=((B**2+C**2-4*A*D)/(2*A**2))**0.5
    c1=Sites(x,y-r,"circle",arc)
    return [c1]
def detect_circle_event(Binary_Tree,pleft=None,pright=None,pmiddle=None):
    # we have an intersection on the right side of the point and we are going to see if there is a risk a disapearing
    if(pleft!=None and pright==None and pmiddle==None):
        a=False
        arc1=None
        arc2=None
        #modifier
        Tree=Binary_Tree
        while(a==False):
            #We check the children if there is an intersection
            if(Tree.arcleft!=None and Tree.arcleft.sleft!=None):
                arc1=Tree
                arc2=Tree.arcright
                a=True
            #We check if the parent 
            elif(Tree.parent!=None and Tree.parent.sright==Tree.sleft):
                arc1=Tree
                arc2=Tree.parent
                a=True
            else:
                a=True
        if(arc1==None):
            return None
        else:
            #if we found out that there is also an intersection on the left side it means that there is a circle event
            return compute_circle(arc1.sleft,arc1.sright,arc2.sright,[arc1,arc2])
    elif(pleft==None and pright!=None and pmiddle==None):
        print('pright')
        #If we find an intersection on the left side of the point
        a=False
        #modifier
        Tree=Binary_Tree
        arc1=None
        arc2=None
        while(a==False):
            #We check the children if there is an intersection
            if(Tree.arcright!=None and Tree.arcright.sright!=None):
                arc1=Tree
                arc2=Tree.arcright
                a=True
            #We check if the parent 
            elif(Tree.parent!=None and Tree.parent.sleft==Tree.sright):
                arc1=Tree
                arc2=Tree.parent
                a=True
            else:
                a=True
        if(arc1==None):
            return None
        else:
            print('compute circle')
            #if we found out that there is also an intersection on the left side it means that there is a circle event
            return compute_circle(arc1.sleft,arc1.sright,arc2.sright,[arc1,arc2])
    #Not sure if it usefull
    elif(pleft!=None and pright!=None):
        
        #In the case where the new point has an intersection with 2 points we need to check for the left and right point
        c1=detect_circle_event(Binary_Tree.arcleft,pleft)
        c2=detect_circle_event(Binary_Tree.arcright,None,pright)
        list_c=[]
        if(c1!=None):
            print("c1")
            list_c.append(c1[0])
        if(c2!=None):
            print("c2")
            list_c.append(c2[0])
        print(list_c)
        return list_c
def circle_events(point,segments,Binary_Tree):
    arcs=point.arc
    #First we finish the segment that are linked to this circle events
    #We have two things to do : delete the arc from the Binary tree and for the segment, add the end point
    for arc in point.arc:
        for segment in segments:
            if(segment.arc.sleft==arc.sleft and segment.arc.sright==arc.sright):
                print("end")
                segment.end=Point(point.x,point.y)
    #for the case of deleting in a binary tree we have 2 cases : first one the point is intersectd by 2 other points or the point is intersect by only one
    if(point.arc[1].parent==point.arc[0]):
        arc= point.arc[0]
        arc2=point.arc[1]
        print("first case")
    else:
        arc= point.arc[1]
        arc2=point.arc[0]
        print("second case")
    a=False
    Tree=copy.deepcopy(Binary_Tree)
    new_arc=None
    while(a==False):
        if(arc.sright.x<Tree.sleft.x):
            print("sleft")
            Tree=Tree.sleft
        elif(arc.sleft.x>Tree.sright.x):
            print("sright")
            Tree=Tree.sright
        else:
            Tree_parent=Tree.parent
            arcleft=None
            arcright=None
            if(Tree.arcright.sright!=None):
                arcright=Tree.arcright
            else:
                arcleft=Tree.arcleft 
            #<p1,p2>--><p2,p3>
            if(arcright!=None and Tree.slfet!=arcright.sright):
                Tree.sright=arcright.sright
                Tree.arcright=arcright.arcright
                Tree.arcright.parent=Tree
                new_arc=Tree
                a=True
            elif(arcleft!=None and Tree.sright!=arcleft.sleft):
                Tree.sleft=arcleft.sleft
                Tree.arcleft=arcleft.arcleft
                Tree.arcleft.parent=Tree
                new_arc=Tree
                a=True
            else:
                #In the case of the point intersecting an other one we techniqually have two circle event one for each intersection so we have to check if delete the left arc or right arc
                if(Tree.arcright==arc2):
                    #<p1,p2>--><p2,p1>--><p1,p3>--><p3,None>
                    #<p1,p2>--><p2,p3>--><p3,None>
                    Tree.arcright.sright=arcright.arcright.sleft
                    Tree.arcright.arcright=arcright.arcright.arcright
                    Tree.arcright.arcright.arcright.parent=arcright.arcright
                    new_arc=Tree.arcright
                    a=True
                else:
                    #<p4,p1><--<p1,p2>--><p2,p1>
                    #<p4,p2>--><p2,p1>
                    Tree.arcleft.sright=Tree.sright
                    Tree.arcleft.arcright=Tree.arcright
                    Tree.arcright.parent=Tree.arcleft
                    new_arc=Tree.arcleft
                    a=True
    segments.append(Segment(Point(point.x,point.y),new_arc))
    while(Tree.parent!=None):
        Tree=Tree.parent
    return Tree


#p1=Sites(30.0,45.0,"site")
#p2=Sites(10.0,20.0,"site")
#Need to fix y=y
p1=Sites(10.0,19.0,"site")
p2=Sites(20.0,10.0,"site")
p3=Sites(30.0,20.0,"site")
points=[p1,p2,p3]
Voronoi(points)




                

            
            
        



