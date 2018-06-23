# **Problem Description:**

Program to find how long it is until the next bus on “BUS ROUTE” leaving from “BUS STOP NAME”
going “DIRECTION” using the api defined at http://svc.metrotransit.org/ .

-“BUS ROUTE” will be a substring of the bus route name which is only in one bus route.  
-“BUS STOP NAME” will be a substring of the bus stop name which is only in one bus stop on that route.  
-“DIRECTION” will be “north” “east” “west” or “south”.  

 Usage: get_next_bus.py bus_route stop_name direction
 
 ex: get_next_bus.py "METRO Blue Line" "Target Field Station Platform 1" south
 
 ### **Sample Outputs:**
``` 
 $python get_next_bus.py "METRO Blue Line" "Target Field Station Platform 1" south
25 Minutes

$python get_next_bus.py "METRO Blue Line" "Target Field Station Platform 1" southe
Unable to find the direction (southe) for the Route name (METRO Blue Line) entered!!!. 
```
