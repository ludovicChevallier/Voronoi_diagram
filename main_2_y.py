import random
import math
import matplotlib.pyplot as plt
from data_type_y import Point, Event, Arc, Segment, PriorityQueue

# Source: (C++) http://www.cs.hmc.edu/~mbrubeck/voronoi.html

class Voronoi:
    def __init__(self, points):
        self.output = [] # list of line segment
        self.arc = None  # binary tree for parabola arcs

        self.points = PriorityQueue() # site events
        self.event = PriorityQueue() # circle events

        # bounding box
        self.x0 = -50.0
        self.x1 = -50.0
        self.y0 = 550.0
        self.y1 = 550.0

        # insert points to site event
        for pts in points:
            point = Point(pts[0], pts[1])
            self.points.push(point)
            # keep track of bounding box size
            if point.x < self.x0: self.x0 = point.x
            if point.y < self.y0: self.y0 = point.y
            if point.x > self.x1: self.x1 = point.x
            if point.y > self.y1: self.y1 = point.y

        # add margins to the bounding box
        dx = (self.x1 - self.x0 + 1) / 5.0
        dy = (self.y1 - self.y0 + 1) / 5.0
        self.x0 = self.x0 - dx
        self.x1 = self.x1 + dx
        self.y0 = self.y0 - dy
        self.y1 = self.y1 + dy

    def process(self):
        while not self.points.empty():
            if not self.event.empty() and (self.event.top().y <= self.points.top().y):
                self.process_event() # handle circle event
            else:
                self.process_point() # handle site event

        # after all points, process remaining circle events
        while not self.event.empty():
            self.process_event()

        self.finish_edges()

    def process_point(self):
        # get next event from site pq
        p = self.points.pop()
        # add new arc (parabola)
        self.arc_insert(p)

    def process_event(self):
        print("update segment")
        # get next event from circle pq
        e = self.event.pop()

        if e.valid:
            # start new edge with as a point of start the circle center
            s = Segment(e.p)
            self.output.append(s)

            # remove associated arc (parabola)
            a = e.a
            #What this do is that in each arc (pprev and pnext) we have the intersection p1,p2 and p2,p3 and we create p1,p3 and p3,p1
            # And for this new intersection we say that their point of start is the center of the circle 
            if a.pprev is not None:
                a.pprev.pnext = a.pnext
                a.pprev.s1 = s
            if a.pnext is not None:
                a.pnext.pprev = a.pprev
                a.pnext.s0 = s
            # finish the edges before and after a
            if a.s0 is not None: a.s0.finish(e.p)
            if a.s1 is not None: a.s1.finish(e.p)
            print("finish segment")
            print(a.p.x)
            print(a.s0.end.x,a.s1.end.x)
            print(a.s0.start.x,a.s1.start.x)

            # recheck circle events on either side of p
            if a.pprev is not None: self.check_circle_event(a.pprev, e.y)
            if a.pnext is not None: self.check_circle_event(a.pnext, e.y)

    def arc_insert(self, p):
        if self.arc is None:
            self.arc = Arc(p)
        else:
            # find the current arcs at p.y
            i = self.arc
            while i is not None:
                flag, z = self.intersect(p, i)
                if flag:
                    print("-------")
                    print("found intersection")
                    print(p.x,i.p.x)
                    # new parabola intersects arc i
                    flag, zz = self.intersect(p, i.pnext)
                    if (i.pnext is not None) and (not flag):
                        #The idea behind this is to create a circle for example : p2 has prec and pnext=p1 which means our pnext is equal (p2,p2,p1). so when we do Arc(p,i,i.next) When we are going to compute the circle event for i.pnext i.prev is going to be p3, and i.pnext=10
                        #So in the end we would have p1-->p2-->p3-->p2-->p1
                        i.pnext.pprev = Arc(i.p, i, i.pnext)
                        i.pnext = i.pnext.pprev
                    else:
                        #If there is no pnext we add one with the same i but telling that the previous is i
                        i.pnext = Arc(i.p, i)
                    #We link them so that when we will add the point p and affect to i.s1 the segment it will also do it for p since p will be i.pnext
                    i.pnext.s1 = i.s1
                    # add p between i and i.pnext
                    #TODO we do this because we will pi, pj,pk and pi ,pk,pj  thanks to the two next line
                    #He does this because thanks to this if we want to compute the circle event for i and point p it's possible because we will have i.pprev and i.ppnext
                    i.pnext.pprev = Arc(p, i, i.pnext)
                    #It also modify i.pnext.pprev because it become i due to Arc(p, i, i.pnext)
                    i.pnext = i.pnext.pprev
                    print("ADD p")
                    print(i.p.x)
                    if(i.pprev!=None):
                        print(i.pprev.p.x)
                    print(i.pnext.p.x)
                    print(i.pnext.pprev.p.x)
                    print(i.pnext.pnext.p.x)


                    i = i.pnext # now i points to the new arc
                    print("assign seg")
                    # add new half-edges connected to i's endpoints
                    #On lie les segment s0 et s1 de chaque côté du nouveau point
                    seg = Segment(z)
                    print(z.x)
                    self.output.append(seg)
                    i.pprev.s1 = i.s0 = seg
                    seg = Segment(z)
                    self.output.append(seg)
                    i.pnext.s0 = i.s1 = seg

                    # check for new circle events around the new arc
                    print("MID")
                    self.check_circle_event(i, p.y)
                    print("LEFT")
                    self.check_circle_event(i.pprev, p.y)
                    print("RIGHT")
                    self.check_circle_event(i.pnext, p.y)

                    return
                        
                i = i.pnext

            # if p never intersects an arc, append it to the list
            i = self.arc
            while i.pnext is not None:
                i = i.pnext
            i.pnext = Arc(p, i)
            
            # insert new segment between p and i
            x = self.x0
            y = (i.pnext.p.y + i.p.y) / 2.0
            start = Point(x, y)

            seg = Segment(start)
            i.s1 = i.pnext.s0 = seg
            self.output.append(seg)

    def check_circle_event(self, i, y0):
        if(i.pprev!=None):
            print("prev: "+ str(i.pprev.p.x))
        print( i.p.x)
        if(i.pnext!=None):
             print("next: "+str(i.pnext.p.x))
        # look for a new circle event for arc i
        if (i.e is not None) and (i.e.y  != self.y0):
            #If the arc is already assign to a circle event and that this circle event is not on the same x level of l (x0) it's a false alarm
            i.e.valid = False
        i.e = None

        if (i.pprev is None) or (i.pnext is None): return

        flag, y, o = self.circle(i.pprev.p, i.p, i.pnext.p)
        if flag and (y > self.y0):
            print("detect circle event")
            print(i.pprev.p.x, i.p.x, i.pnext.p.x)
            i.e = Event(y, o, i)
            self.event.push(i.e)

    def circle(self, a, b, c):
        # check if bc is a "right turn" from ab
        #abc  must be in clock wise order to compute correctly the center of the circle
        if ((b.x - a.x)*(c.y - a.y) - (c.x - a.x)*(b.y - a.y)) > 0:
            print("false circle")
            print(a.x,b.x,c.x) 
            return False, None, None
        #https://books.google.it/books?id=gsv7HALW2jYC&pg=PA219&lpg=PA219&dq=computer+circle+with+3+points+Joseph+O%27Rourke&source=bl&ots=r4Qs-iabac&sig=ACfU3U3b59Cwtlvc2KJNMPINtNan3kXtiQ&hl=fr&sa=X&ved=2ahUKEwiI-Oy21uD1AhUPQ_EDHUcTDdEQ6AF6BAgoEAM#v=onepage&q=computer%20circle%20with%203%20points%20Joseph%20O'Rourke&f=false
        # Joseph O'Rourke, Computational Geometry in C (2nd ed.) p.189
        A = b.x - a.x
        B = b.y - a.y
        C = c.x - a.x
        D = c.y - a.y
        E = A*(a.x + b.x) + B*(a.y + b.y)
        F = C*(a.x + c.x) + D*(a.y + c.y)
        G = 2*(A*(c.y - b.y) - B*(c.x - b.x))

        #Which means that points are all on the same segment which makes the computation impossible
        if (G == 0): return False, None, None # Points are co-linear

        # point o is the center of the circle
        ox = 1.0 * (D*E - B*F) / G
        oy = 1.0 * (A*F - C*E) / G

        # o.x plus radius equals max x coord
        y = oy + math.sqrt((a.x-ox)**2 + (a.y-oy)**2)
        o = Point(ox, oy)
           
        return True, y, o
        
    def intersect(self, p, i):
        # check whether a new parabola at point p intersect with arc i
        if (i is None): return False, None
        if (i.p.x == p.x): return False, None

        a = 0.0
        b = 0.0

        if i.pprev is not None:
            a = (self.intersection(i.pprev.p, i.p, 1.0*p.x)).x
        if i.pnext is not None:
            b = (self.intersection(i.p, i.pnext.p, 1.0*p.x)).x
        if(a!=0.0 and b!=0.0):
            print("intersection_prev")
            print(i.pprev.p.x, i.p.x,i.pnext.p.x)
            print(a,b)
        if (((i.pprev is None) or (a >= p.x)) and ((i.pnext is None) or (p.x >= b))):
            print("intersection")
            if(a!=0.0 and b!=0.0):
                print(i.pprev.p.x, i.p.x,i.pnext.p.x)
            print(p.y)
            print(a,b)
            px = p.x
            py = 1.0 * ((i.p.y)**2 + (i.p.x-px)**2 - p.y**2) / (2*i.p.y - 2*p.y)
            print(py,px)
            res = Point(px, py)
            return True, res
        return False, None

    def intersection(self, p0, p1, l):
        # get the intersection of two parabolas
        p = p0
        if (p0.x == p1.x):
            py = (p0.y + p1.y) / 2.0
        elif (p1.x == l):
            py = p1.y
        elif (p0.x == l):
            py = p0.y
            p = p1
        else:
            # use quadratic formula
            z0 = 2.0 * (p0.x - l)
            z1 = 2.0 * (p1.x - l)

            a = 1.0/z0 - 1.0/z1
            b = -2.0 * (p0.y/z0 - p1.y/z1)
            c = 1.0 * (p0.y**2 + p0.x**2 - l**2) / z0 - 1.0 * (p1.y**2 + p1.x**2 - l**2) / z1

            py = 1.0 * (-b-math.sqrt(b*b - 4*a*c)) / (2*a)
            
        px = 1.0 * (p.x**2 + (p.y-py)**2 - l**2) / (2*p.x-2*l)
        res = Point(px, py)
        return res

    def finish_edges(self):
        l = self.x1 + (self.x1 - self.x0) + (self.y1 - self.y0)
        i = self.arc
        while i.pnext is not None:
            if i.s1 is not None:
                #l'idée est de "tirer" le segment des deux côtes en faisant l'intersection entre p1 p2 puis p2,p1
                p = self.intersection(i.p, i.pnext.p, l*2.0)
                i.s1.finish(p)
            i = i.pnext

    def print_output(self):
        it = 0
        for o in self.output:
            it = it + 1
            p0 = o.start
            p1 = o.end
            print (p0.x, p0.y, p1.x, p1.y)

    def get_output(self):
        res = []
        for o in self.output:
            p0 = o.start
            p1 = o.end
            res.append((p0.x, p0.y, p1.x, p1.y))
        return res

p1=(10.0,40.0)
p2=(45.0,21.0)
p3=(20.0,10.0)
p4=(30.0,20.0)
p5=(50.0,60.0)
points=[p1,p2,p3,p5]
vp = Voronoi(points)
vp.process()
lines = vp.get_output()

x=[]
y=[]
list_seg_x=[]
list_seg_y=[]
plt.figure() 
for point in points:
    x.append(point[0])
    y.append(point[1])
for line in lines:
    list_seg_x.append([line[0],line[2]])
    list_seg_y.append([line[1],line[3]])
#plot the points 
plt.xlim([-50, 100])
plt.ylim([-50, 100])
for i in range(len(x)):
    plt.plot(x[i],y[i],'o', color='black')
for i in range(len(list_seg_x)):
    plt.plot(list_seg_x[i],list_seg_y[i])
plt.show()