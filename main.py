
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
            site_events(point)
        else:
            circle_events(point)

def site_events(point):
    print("site")

def circle_events(point):
    print("circle")
