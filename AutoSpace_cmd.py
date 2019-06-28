import rhinoscript.userinterface
import rhinoscript.geometry
import rhinoscriptsyntax as rs
import math

__commandname__ = "AutoSpace"

# RunCommand is the called when the user enters the command name in Rhino.
# The command name is defined by the filname minus "_cmd.py"
def RunCommand( is_interactive ):


    #returns beginSurf,endSurf
    def getSurface ():
    
        surface = rs.GetObject("Please Select The Surface Object",rs.filter.curve, True, True)
        #if( surface==None ): return
        #rs.UnselectObject(surface)
        beginSurf = rs.CurveStartPoint(surface)[0]
        surfLen = getLength(surface)
        endSurf = beginSurf + surfLen
    
        return beginSurf,endSurf, surfLen 
    
    #returns lengths of an object
    def getLength(object):
        rs.EnableObjectGrips(object)
        list = rs.ObjectGripLocations(object)
        
        surfX = []
        for pt in list:
            surfX.append(pt[0])
        first = surfX[0]
        secon = surfX[1]
        
        surfLen = secon - first
        return surfLen
    
    #returns list of object ids (list), amount of objects (amntObj) and the length of the array object (lenObj)
    def arrayObjs():
        arrObjects = rs.GetObjects( "Select Array Objects", rs.filter.curve, True, True)
    
        if( arrObjects==None ): return
        rs.UnselectObjects(arrObjects)
    
        list = []
        amntObj  = 0
        lenObj = getLength(arrObjects[0])
        
        for object in arrObjects:
            if rs.IsCurve(object):
                #Get the curve length
        
                amntObj  += 1
                list.append(str(object))
        return list,amntObj, lenObj
    
    #give space btwn centers of objects
    def calc_space(num_items,surf_len, width): 
        assert num_items > 2,"Number of items has to be bigger then 1"
        assert num_items * width  < surf_len, "Combined width of objects should be smaller then surface length"
        space = (surf_len-width)/(num_items -1)
        print("space = ",space)
        return space
    
    
    #for some reason, it has to be array objs THEN surface. I have no idea why, but the calculations get messed up if you switch it
    
    #GET ARRAY INFO
    list,amntObj, lenObj = arrayObjs()
    print("amntObj,lenObj, " ,amntObj,lenObj)
    #GET SURFACE LENGTHS
    beginSurf,endSurf, surfLen = getSurface()
    print("beginSurf",beginSurf)
    #this is only a functions bc it helps clean things up until i have time to deal
    
    
    #OBJECTS MUST BE SELECTED RIGHT TO LEFT
    for index, object in enumerate(list):
        if (index == 0): #1st object in the list
      
            xCordObj = rs.CurveStartPoint(object)[0]
    
            start = beginSurf  - xCordObj
            rs.MoveObject(object, [start, 0, 0])
    
        elif (index == len(list)-1): #last object in the list
            # SUBTRACT THE LEN OF SURF FROM THE BEGING OF THE SURF TO THE BEGIN OF THE 1ST OB
            xCordObj = rs.CurveStartPoint(object)[0] #[0]gets the x cord
            endPnt = endSurf - lenObj - xCordObj
            rs.MoveObject(object, [endPnt, 0, 0])
            
    #beginSurf = fisrt coridante, endSurf = last
        else:
            currentXCoordObj = rs.CurveStartPoint(object)[0]
            print("beginSurf ", beginSurf, " surf_len ", surfLen)
            newXCoord=beginSurf + index * calc_space(num_items=amntObj,surf_len=surfLen,width=lenObj)
            dist=newXCoord - currentXCoordObj
            print ( "current " , currentXCoordObj, " newCoord ", newXCoord, " index ", index , " dist ", dist) 
            rs.MoveObject( object,  [ dist ,0,0   ])
    
    print("Program Complete")
    return 0
RunCommand(True)
