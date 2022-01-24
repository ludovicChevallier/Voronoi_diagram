import numpy as np
import matplotlib.pyplot as plt
from data_type import Sites,Arc,Segment,Point
import cmath
import copy
import operator

nb_intersection=0
#All the points will already be of class points with events ="sites"
def Voronoi(points):
    #sort the points descending by y coordinates
    segment=[]
    Binary_Tree=Arc()
    def myFunc(e):
        return e.y
    def myFunc2(e):
        return e.x
    list_point=[]
    points.sort(key=operator.attrgetter('y','x'),reverse=True)
    while len(points)!=0:
        list_circle=[]
        point=points.pop(0)
        if(point.event=="site"):
            list_point.append(point)
            while(Binary_Tree.parent!=None):
                Binary_Tree=Binary_Tree.parent
            list_circle=site_events(point,Binary_Tree,segment) 
            while(Binary_Tree.parent!=None):
                Binary_Tree=Binary_Tree.parent
            #print(Binary_Tree.arcright.sleft.x,Binary_Tree.arcright.sright.x)       
            if(list_circle!=None):
                index=0
                for i in range(len(list_circle)):
                    if(len(points)!=0):
                        for j in range(len(points)):
                            if(type(list_circle[i].y)==complex):
                                list_circle[i].y=cmath.sqrt((list_circle[i].y.real)**2+(list_circle[i].y.imag)**2)
                                list_circle[i].y=list_circle[i].y.real
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
            print(point.x,point.y)
            Binary_Tree=circle_events(point,segment,Binary_Tree)
    #We need to close the segments
    list_seg_x=[]
    list_seg_y=[]
    for i in range(len(segment)):
        print("arc")
        print(segment[i].arc.sleft.x,segment[i].arc.sright.x)
        #find 2 points that intersect the segment
        s1,s2=intersection(Point(segment[i].arc.sleft.x,segment[i].arc.sleft.y),Point(segment[i].arc.sright.x,segment[i].arc.sright.y),0)
        if(s2!=None):
            a=(s1.y-s2.y)/(s1.x-s2.x)
            b=s1.y-a*s1.x
        else:
            a=0
            b=s1.x
        if(len(segment)>1 and segment[i].end==None):
            print("segment==2")
            seg=None
            j=1
            #If all the segment doesn't have an end it means that all of them are independent
            for j in range(len(segment)):
                if(j!=i and segment[j].end!=None and segment[i].start.x==segment[j].end.x and segment[i].start.y==segment[j].end.y):
                    seg=segment[j]
            if(seg!=None):
                print("not else")
                y=cmath.sqrt((segment[i].start.x.real)**2+(segment[i].start.x.imag)**2)
                if(a<0  and segment[i].start.y<seg.start.y):
                    print("1")
                    segment[i].end=Point(50,a*50+b)
                elif(a>0  and segment[i].start.y<seg.start.y):
                    print("2")
                    segment[i].end=Point(0,b)
                elif(a>0  and segment[i].start.y>seg.start.y):
                    print("3")
                    segment[i].end=Point(50,a*50+b)
                elif(a<0 and segment[i].start.y<seg.start.y ):
                    print("4")
                    segment[i].end=Point(0,b)
                elif(a==0):
                    if(segment[i].start.y==seg.end.y):
                        print("under")
                        segment[i].end=Point(b,0)
                    else:
                        print("upper")
                        segment[i].end=Point(b,50)
                else:
                    print("5")
                    segment[i].end=Point(0,b)
            else:
                print("else")
                segment[i].start=Point(0,b)
                segment[i].end=Point(50,a*50+b)
        elif(len(segment)==1):
            if(a>0):
                segment[i].start=Point(0,b)
                segment[i].end=Point(50,a*50+b)
            else:
                segment[i].end=Point(0,b)
                segment[i].start=Point(50,a*50+b)
        else:
            if(i<len(segment)-1 and segment[i+1].start!=None and segment[i].end.x==segment[i+1].start.x or i!=0 and segment[i-1].end!=None and segment[i].end.x==segment[i-1].end.x or i<len(segment) and segment[i+1].end!=None and segment[i].end.x==segment[i+1].end.x):
                if(segment[i-1].end!=None and i<len(segment)-1 and segment[i].end.x==segment[i+1].start.x and i!=0 and segment[i].start.x==segment[i-1].end.x or i<len(segment)-1 and segment[i+1].end!=None and i<len(segment)-1 and segment[i].end.x==segment[i+1].end.x and i!=0 and segment[i].start.x==segment[i-1].start.x):
                    print("continue")
                elif(segment[i].end.y-segment[i].start.y>0):
                    if(a>0):
                        print("1j")
                        segment[i].start=Point(0,b)
                    elif(a==0):
                        if(segment[i].end.x==segment[i+1].start.x):
                            print("under2")
                            segment[i].start=Point(b,50)
                        else:
                            print("upper2")
                            segment[i].start=Point(b,0)
                    elif(segment[i-1].end!=None and segment[i].start.x==segment[i-1].start.x):
                        print("ok")
                    else:
                        print("2j")
                        segment[i].start=Point(50,a*50+b)
                else:
                    print("start")
                    if(a>0):
                        print("1x")
                        segment[i].start=Point(50,a*50+b)
                    elif(a==0):
                        if(segment[i].end.x==segment[i+1].start.x):
                            print("under3")
                            segment[i].start=Point(b,50)
                        else:
                            print("upper3")
                            segment[i].start=Point(b,0)
                    elif(segment[i-1].end!=None and segment[i].start.x==segment[i-1].start.x):
                        print("ok")
                    else:
                        print("2x")
                        segment[i].start=Point(0,b)

                    
            else:
                if(a>0):
                    print("3j")
                    segment[i].start=Point(0,b)
                    segment[i].end=Point(50,a*50+b)
                else:
                    print("4j")
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
    print("points")
    print(point.x,point.y)
    if(Binary_Tree.sleft==None and Binary_Tree.sright==None):
        #When we create a node we need also to a child node
        Binary_Tree.sleft=point
        Binary_Tree.arcleft=Arc(None,point)
        Binary_Tree.arcleft.parent=Binary_Tree
        return None
    elif(Binary_Tree.sleft!=None and Binary_Tree.sright==None):
        print("sleft")
        s1,s2=intersection(Binary_Tree.sleft,point,float(point.y-0.001))
        #in case of one intersection
        if(s2==None and s1!=None):
            print("foud one")
            if(Binary_Tree.sleft.x>point.x):
                print("permutation")
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
            Tree=copy.deepcopy(Binary_Tree)
            segment.append(Segment(s1,Tree))
            return detect_circle_event(Binary_Tree,Binary_Tree.sleft)
        elif(s1==None):
            return None
        else:
            #modifier
            if(Binary_Tree.sleft.y==point.y):
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
                Tree=copy.deepcopy(Binary_Tree)
                segment.append(Segment(s1,Tree,end=s2))
                return None
            if(Binary_Tree.sleft.x==point.x):
                Tree=copy.deepcopy(Binary_Tree)
                segment.append(Segment(s1,Tree,end=s2))
                return None
            #In case the new point has 2 intersection with an other point we complete the node and add a new one
            Binary_Tree.sright=point
            Binary_Tree.arcright=Arc(point,Binary_Tree.sleft,parent=Binary_Tree)
            Binary_Tree.arcright.arcleft=Arc(None,point,parent=Binary_Tree.arcright)
            Binary_Tree.arcright.arcright=Arc(Binary_Tree.sleft,None,parent=Binary_Tree.arcright)
            #modifier
            Tree=copy.deepcopy(Binary_Tree)
            segment.append(Segment(s1,Tree))
            segment.append(Segment(s2,Tree.arcright))
            return detect_circle_event(Binary_Tree,Binary_Tree.sleft,Binary_Tree.sleft)
    elif(Binary_Tree.sleft==None and Binary_Tree.sright!=None):
        print("nothing on the left")
        s1,s2=intersection(Binary_Tree.sright,point,float(point.y-0.001))
        if(s2==None and s1!=None):
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
            Tree=copy.deepcopy(Binary_Tree)
            segment.append(Segment(s1,Tree))
            print("detect circle")
            list_c=detect_circle_event(Binary_Tree,None,Binary_Tree.sright)
            return list_c 
        elif(s1==None):
            return None
        else:
             #modifier
            if(Binary_Tree.sright.y==point.y):
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
                Tree=copy.deepcopy(Binary_Tree)
                segment.append(Segment(s1,Tree,end=s2))
                return None
            if(Binary_Tree.sright.x==point.x):
            #modifier
                Tree=copy.deepcopy(Binary_Tree)
                segment.append(Segment(s1,Tree,end=s2))
                return None
            #In case the new point has 2 intersection with an other point we complete the node and add a new one
            Binary_Tree.sleft=point
            Binary_Tree.arcleft=Arc(Binary_Tree.sright,point,parent=Binary_Tree)
            Binary_Tree.arcleft.arcright=Arc(point,None,parent=Binary_Tree.arcleft)
            Binary_Tree.arcleft.arcleft=Arc(None,Binary_Tree.sright,parent=Binary_Tree.arcleft)
            #Will try to find circle event on the left and right side f the point
            #modifier
            Tree=copy.deepcopy(Binary_Tree)
            segment.append(Segment(s1,Tree))
            segment.append(Segment(s2,Tree.arcleft))
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
            print("arcmiddle")
            #peut être réduire l?
            s1,s2=intersection(Binary_Tree.sright,point,float(point.y-0.001))
            s3,s4=intersection(Binary_Tree.sleft,point,float(point.y-0.001))
            s5,s6=intersection(Binary_Tree.sleft,Binary_Tree.sright,float(point.y-0.001))
            global nb_intersection
            nb_intersection-=1
            old_point=None
            #worst case possible : we have a point between 2 other points an need to modify the decision tree
            #if the new point intersect the 2 sites
            #ATTENTION CEUX CAS PEU ETRE FAUX CAR UN NOUVEAU POINT NE PEUX CROISER DEUX DES LE DEBUT
            if(s2==None and s4==None and s1!=None and s3!=None):
                print("s2 and s4 not None")
                #nb_intersection-=1
                #if one of the 2 sites is in the extreme we just have to push it
                if(Binary_Tree.arcright!=None and Binary_Tree.arcright.sright==None):
                    print("cas1")
                    #TODO faire sa pour chaque cas
                    old_point=Binary_Tree.sright
                    Binary_Tree.sright=point
                    Binary_Tree.arcright.sright=old_point
                    Binary_Tree.arcright.sleft=point
                    Binary_Tree.arcright.arcright=Arc(old_point,None,parent=Binary_Tree.arcright)
                    Binary_Tree.arcright.arcleft=Arc(None,point,parent=Binary_Tree.arcright)
                    segment[-1].end=s5
                    #modifier
                    Tree=copy.deepcopy(Binary_Tree)
                    segment.append(Segment(s5,Tree.arcright))
                    segment.append(Segment(s5,Tree))
                    #nb_intersection-=1
                    list_c=detect_circle_event(Binary_Tree,Binary_Tree.sleft,old_point,point)
                    Binary_Tree=Tree
                elif(Binary_Tree.arcleft.sleft==None):
                    print("cas2")
                    old_point=Binary_Tree.sleft
                    Binary_Tree.sleft=point
                    Binary_Tree.arcleft.sleft=old_point
                    Binary_Tree.arcleft.sright=point
                    Binary_Tree.arcleft.arcleft=Arc(None,old_point,parent=Binary_Tree.arcleft)
                    Binary_Tree.arcleft.arcleft=Arc(point,None,parent=Binary_Tree.arcleft)
                    segment[-1].end=s5
                    #modifier
                    Tree=copy.deepcopy(Binary_Tree)
                    segment.append(Segment(s5,Tree))
                    segment.append(Segment(s5,Tree.arcleft))
                    list_c=detect_circle_event(Binary_Tree,old_point,Binary_Tree.sright,point)
                else:
                    print("cas3")
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
            elif(s1!=None and s2!=None):
                print("s1!=s2")
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
                #modifier
                Tree=copy.deepcopy(Binary_Tree)
                segment.append(Segment(s1,Tree.arcleft))
                segment.append(Segment(s2,Tree))
                return detect_circle_event(Binary_Tree,None,Binary_Tree.sright)
            elif(s3!=None and s4!=None):
                print("s3!=s4")
                arcright=Binary_Tree.arcright
                Binary_Tree.sright=point
                Binary_Tree.arcright=Arc(point,Binary_Tree.sleft,parent=Binary_Tree)
                Binary_Tree.arcright.arcleft=Arc(None,point,parent=Binary_Tree.arcright)
                Binary_Tree.arcright.arcright=Arc( Binary_Tree.arcright.sright,arcright.sleft,parent=Binary_Tree.arcright)
                arcright.parent=Binary_Tree.arcright.arcright
                Binary_Tree.arcright.arcright.arcright=arcright
                #<p1,p2>--><p2,p1>
                #modifier
                Tree=copy.deepcopy(Binary_Tree)
                segment.append(Segment(s3,Tree))
                segment.append(Segment(s4,Tree.arcright))
                return detect_circle_event(Binary_Tree,Binary_Tree.sleft)


                    
                


def intersection(p0,p1,l):
    global nb_intersection
    nb_intersection += 1
    x1=complex(0.0)
    x2=0.0
    a0=0.0
    b0=0.0
    c0=0.0
    a1=0.0
    b1=0.0
    c1=0.0
    a=0.0
    b=0.0
    c=0.0
    if(p0.y==p1.y):
        #p0.y-=0.05
        b0=(-2)*p0.x*0.5*1/(p0.y-l)
        c0=((p0.x**2)+(p0.y**2)-(l**2))*0.5*1/(p0.y-l)
        b1=(-2)*p1.x*0.5*1/(p1.y-l)
        c1=((p1.x**2)+(p1.y**2)-(l**2))*0.5*1/(p1.y-l)
        b=b1-b0
        c=c1-c0 
        x1=-c/b
        y1=b1*x1+c1
        #x1=(p0.x+p1.x)/2
        #y1=p0.y
        print("y==y")
        return Point(x1,p0.y), None
    #use quadratic formula
    #https://math.stackexchange.com/questions/2700033/explanation-of-method-for-finding-the-intersection-of-two-parabolas
    #https://math.stackexchange.com/questions/1370231/parabola-equation-in-fortune-algorithm-for-building-voronoi-diagram
    # we just have to compute a b and c which are the value of the parabola ax²+bx+c and use them in the formula
    #a0,b0 and c0 are the parameters of the parabola for the point p0 (look at the lessons)
    while(type(x1)==complex):
        a0=0.5*1/(p0.y-l)
        b0=(-2)*p0.x*0.5*1/(p0.y-l)
        c0=((p0.x**2)+(p0.y**2)-(l**2))*0.5*1/(p0.y-l)
        a1=0.5*1/((p1.y-l))
        b1=(-2)*p1.x*0.5*1/(p1.y-l)
        c1=((p1.x**2)+(p1.y**2)-(l**2))*0.5*1/(p1.y-l)
        a=a1-a0
        b=b1-b0
        c=c1-c0  
        #compute the 2 possibl intersections
        x1=((-1*b)-((b**2)-4*a*c)**0.5)/(2*a)
        x2=((-1*b)+((b**2)-4*a*c)**0.5)/(2*a)
        l=l-1
    #compute the y intersection
    #The thing is that it's not possible for x1 and x2 to be equal but they would be very close for example :29.9797595392213 30.020256460778693
    if(x1-x2>3.0 or x2-x1>3.0):
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
    def myFunc(e):
        return e.x
    list_point=[p1,p2,p3]
    list_point.sort(key=myFunc)
    p1=list_point[0]
    p2=list_point[1]
    p3=list_point[2]
    A=(p1.x*(p2.y-p3.y)-p1.y*(p2.x-p3.x)+p2.x*p3.y-p3.x*p2.y)
    B=((p1.x**2+p1.y**2)*(p3.y-p2.y)+(p2.x**2+p2.y**2)*(p1.y-p3.y)+(p3.x**2+p3.y**2)*(p2.y-p1.y))
    C=((p1.x**2+p1.y**2)*(p2.x-p3.x)+(p2.x**2+p2.y**2)*(p3.x-p1.x)+(p3.x**2+p3.y**2)*(p1.x-p2.x))
    D=((p1.x**2+p1.y**2)*(p3.x*p2.y-p3.y*p2.x)+(p2.x**2+p2.y**2)*(p1.x*p3.y-p1.y*p3.x)+(p3.x**2+p3.y**2)*(p2.x*p1.y-p1.x*p2.y))
    if(A!=0):
        global nb_intersection
        nb_intersection+=1
        print("found something")
        x=-(B/(2*A))
        y=-(C/(2*A))
        #compute the radius of the circle
        r=((B**2+C**2-4*A*D)/(4*A**2))**0.5
        if(type(r)==complex):
            print("CERCLE COMPLEXE")
            #return None
        c1=Sites(x,y-r,"circle",arc,r)
        return [c1]
    else:
        return None
def detect_circle_event(Binary_Tree,pleft=None,pright=None,pmiddle=None):
    # we have an intersection on the right side of the point and we are going to see if there is a risk a disapearing
    if(pleft!=None and pright==None and pmiddle==None):
        print("pleft")
        a=False
        arc1=None
        arc2=None
        #modifier
        Tree=Binary_Tree
        while(a==False):
            #We check the children if there is an intersection
            if(Tree.arcright!=None and Tree.arcright.sright!=None):
                arc1=Tree
                arc2=Tree.arcright
                a=True
            #We check if the parent 
            elif(Tree.parent!=None and Tree.parent.sright==Tree.sleft):
                print("parent")
                arc1=Tree
                arc2=Tree.parent
                a=True
            else:
                a=True
        if(arc1==None):
            print("Nothing found")
            return None
        else:
            print('compute circle')
            #if we found out that there is also an intersection on the left side it means that there is a circle event
            return compute_circle(arc1.sleft,arc1.sright,arc2.sleft,[arc1,arc2])
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
            if(Tree.arcleft!=None and Tree.arcleft.sleft!=None):
                arc1=Tree
                arc2=Tree.arcleft
                a=True
            #We check if the parent 
            elif(Tree.parent!=None and Tree.parent.sleft==Tree.sright):
                print("parent")
                arc1=Tree
                arc2=Tree.parent
                a=True
            #TODO faire la même chose pour pleft
            elif(Tree.parent!=None and Tree.parent.sright==Tree.sleft):
                #pas sur
                print("parent2")
                arc1=Tree.parent
                arc2=Tree
                a=True
            else:
                a=True
        if(arc1==None):
            print("Nothing found")
            return None
        else:
            #if we found out that there is also an intersection on the left side it means that there is a circle event
            return compute_circle(arc1.sleft,arc1.sright,arc2.sright,[arc1,arc2])
    #Not sure if it usefull
    elif(pleft!=None and pright!=None):
        print("pmiddle")
        #In the case where the new point has an intersection with 2 points we need to check for the left and right point
        c1=None
        c2=None
        if(Binary_Tree.arcleft!=None):
            c1=detect_circle_event(Binary_Tree.arcleft,pleft)
        if(Binary_Tree.arcright!=None):
            c2=detect_circle_event(Binary_Tree.arcright,None,pright)
        list_c=[]
        if(c1!=None):
            print("c1")
            list_c.append(c1[0])
        if(c2!=None):
            print("c2")
            list_c.append(c2[0])
        return list_c
def circle_events(point,segments,Binary_Tree):
    print("circle event")
    arcs=point.arc
    #First we finish the segment that are linked to this circle events
    #We have two things to do : delete the arc from the Binary tree and for the segment, add the end point
    i=0
    true_segment=[]
    for arc in point.arc:
            for segment in segments:
                if(segment.arc.sleft.x==arc.sleft.x and segment.arc.sright.x==arc.sright.x):
                    true_segment.append(segment)
    if(true_segment[-1].start.x!=true_segment[-2].start.x and true_segment[-1].start.y!=true_segment[-2].start.y  ):
        for arc in point.arc:
            for segment in segments:
                #TODO ajouter le end seulement si le segment ne vient pas d'être crée
                if(segment.arc.sleft.x==arc.sleft.x and segment.arc.sright.x==arc.sright.x):
                    segment.end=Point(point.x,point.y)
    else:
        position=len(segments)
        for arc in point.arc:
            for segment in segments:
                #TODO ajouter le end seulement si le segment ne vient pas d'être crée
                if(segment.arc.sleft.x==arc.sleft.x and segment.arc.sright.x==arc.sright.x):
                    segment.start=Point(point.x,point.y)
                    if(segments.index(segment)<position):
                        position=segments.index(segment)
        segments[position-1].end=Point(point.x,point.y)
    #for the case of deleting in a binary tree we have 2 cases : first one the point is intersectd by 2 other points or the point is intersect by only one
    if(point.arc[1].parent!=None and point.arc[1].parent.sleft.x==point.arc[0].sleft.x):
        #arc is the parent
        arc= point.arc[0]
        arc2=point.arc[1]
        print("first case")
    else:
        arc= point.arc[1]
        arc2=point.arc[0]
        print("second case")
    a=False
    Tree=copy.deepcopy(Binary_Tree)
    #print(Tree.sleft.x,Tree.sright.x,Tree.arcleft.arcleft.sright.x)
    new_arc=None
    while(a==False):
        #modifier=
        if(Tree!=None and Tree.sleft!=None and arc.sright!=None and  arc.sright.x<=Tree.sleft.x):
            print("sleft")
            Tree=Tree.arcleft
        elif(Tree!=None and Tree.sright!=None and arc.sleft!=None and arc.sleft.x>=Tree.sright.x):
            print("sright")
            Tree=Tree.arcright
        else:
            Tree_parent=Tree.parent
            arcleft=None
            arcright=None
            #modifer sright!=None and ....
            if(Tree.arcright.sright!=None and arc2.sright.x==Tree.arcright.sright.x and arc2.sright.y==Tree.arcright.sright.y):
                print("arcright")
                arcright=Tree.arcright
            elif(Tree.arcleft.sleft!=None and arc2.sleft.x==Tree.arcleft.sleft.x and arc2.sleft.y==Tree.arcleft.sleft.y):
                print("arcleft")
                arcleft=Tree.arcleft 
            else:
                arcleft=Tree.arcleft
            
            # if(Tree.arcleft!=None and Tree.sleft.x==Tree.arcleft.sright.x):
            #     print("cas0")
            #     Tree.sleft=Tree.arcleft.sleft
            #     print(Tree.arcleft.arcleft)
            #     Tree.arcleft=Tree.arcleft.arcleft
            #     if(Tree.arcleft!=None):
            #         Tree.arcleft.parent=Tree
            #     new_arc=Tree
            #     a=True
            if(arcright!=None and Tree.sleft!=arcright.sright):
                # <p1,p2>--><p2,p3>
                print("cas1")
                Tree.sright=arcright.sright
                Tree.arcright=arcright.arcright
                Tree.arcright.parent=Tree
                new_arc=Tree
                a=True
            # elif(arcleft!=None and Tree.sleft==Tree.arcleft.sright):
            #     print("cas1.2")
            #     new_arc=Tree.arcleft
            #     a=True
            elif(arcleft!=None and Tree.sright!=arcleft.sleft):
                print("cas2")
                Tree.sleft=arcleft.sleft
                Tree.arcleft=arcleft.arcleft
                Tree.arcleft.parent=Tree
                new_arc=Tree
                a=True
            else:
                #In the case of the point intersecting an other one we techniqually have two circle event one for each intersection so we have to check if delete the left arc or right arc
                if(Tree.arcright==arc2):
                    print("cas3")
                    #<p1,p2>--><p2,p1>--><p1,p3>--><p3,None>
                    #<p1,p2>--><p2,p3>--><p3,None>
                    Tree.arcright.sright=arcright.arcright.sleft
                    Tree.arcright.arcright=arcright.arcright.arcright
                    Tree.arcright.arcright.arcright.parent=arcright.arcright
                    new_arc=Tree.arcright
                    a=True
                else:
                    print("cas4")
                    #<p4,p1><--<p1,p2>--><p2,p1>
                    #<p4,p2>--><p2,p1>
                    Tree.arcleft.sright=Tree.sright
                    Tree.arcleft.arcright=Tree.arcright
                    Tree.arcright.parent=Tree.arcleft
                    new_arc=Tree.arcleft
                    a=True
    print("modification point")
    for seg in segments:
        #We need to modify the end point for the other segments since they were based on the the circle
        if(seg.start!=None and seg.start.x==point.x and seg.start.y==point.y):
            seg.start.y=point.y+point.r
        if(seg.end!=None and seg.end.x==point.x and seg.end.y==point.y):
            seg.end.y=point.y+point.r
    #TODO check this peu être ne doit on pas toujours ajouter
    while(Tree.parent!=None):
        Tree=Tree.parent 
    Tree2=copy.deepcopy(Binary_Tree)
    while(Tree2.parent!=None):
        Tree2=Tree2.parent
    test=True
    #only add the segment if the number of segment is under the number of nodes inside the tree:
    for seg in segments:
        test=nb_leaf(seg.arc,new_arc,test)
        if(test==False):
            break
    if(test==True):
        print(new_arc.sleft.x,new_arc.sright.x)
        segments.append(Segment(Point(point.x,point.y+point.r),new_arc))
    return Tree

def nb_leaf(segment,new_arc,test):
    if(segment.sleft.x==new_arc.sleft.x and segment.sleft.y==new_arc.sleft.y and  segment.sright.x==new_arc.sright.x and  segment.sright.y==new_arc.sright.y):
        test=False
    return test
#p1=Sites(30.0,45.0,"site")
#p2=Sites(10.0,20.0,"site")
#Need to fix y=y
# p1=Sites(15.0,19.0,"site")
# #p2=Sites(20.0,40.0,"site")
# p3=Sites(30.0,20.0,"site")
# p4=Sites(40.0,39.0,"site")
# p1=Sites(35.0,20.0,"site")
# p2=Sites(20.0,30.0,"site")
# p3=Sites(45.0,20.0,"site")
# p4=Sites(40.0,39.0,"site")
p1=Sites(10.0,20.0,"site")
p2=Sites(20.0,10.0,"site")
p3=Sites(30.0,20.0,"site")
p4=Sites(40.0,39.0,"site")
points=[p1,p2,p3]
Voronoi(points)




                

            
            
        



