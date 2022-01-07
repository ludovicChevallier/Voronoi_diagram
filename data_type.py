class Sites:
    x=0.0
    y=0.0
    event=""
    def __init__(self,x,y,event) :
        self.x=x
        self.y=y
        self.event=event
#this is our Binary tree containing the 2 arcs that intersect 
class Arc:
    sleft=None
    sright=None
    arcleft=None
    arcright=None
    parent=None
    def __init__(self,sleft=None,sright=None,arcleft=None,arcright=None,parent=None):
        self.sleft=sleft
        self.sright=sright
        self.arcleft=arcleft
        self.arcright=arcright
        self.parent=parent

class Segment:
    start=None
    end=None
    def __init__(self,s):
        self.start=s
        self.end=None
