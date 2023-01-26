# Bus Scheduling Mixed Integer Programming 

This paper describes a mixed integer linear programming optimization problem that solves a task assignment problem. This task assignment problem is housed within a larger optimization problem that is attempting to minimize the total cost to charge a fleet of electric vehicles. The optimization is constantly updating and has the potential to reassign buses at given intervals and the goal of this individual problem is to minimize the amount of charger reassignment that occurs. The results show that it is possible to find a feasible solution by comparing the overlap of previous plans.

# Problem Description

The Utah State Robotics lab is working on an optimal scheduling program allowing multiple electric buses to charge while minimizing the load on the electrical grid at peak times to reduce the total cost of charging. The greater program utilizes a receding horizon optimization planner. For this project an initial plan is made for the entire day then the planner looks over some horizon time period and plans for that horizon time. The planner decides on when a certain bus should charge at a certain station with a certain type of charger (fast, medium, or slow). A given station has a set number of fast, medium, and slow chargers. This optimization problem takes the information provided by the receding horizon planner and plans which specific charger within the given charger type should be chosen at a given station.

The overall goal of this nested optimization problem is to take the information of the long term and short-term plan and minimizes charger reassignment. Meaning if the planner originally had a charging task scheduled at some time to be assigned to a given charger. When a new plan is made by the receding horizon planner it will disincentivize assigning a charging task occurring at the same time to assign said task to another charger.  

The decision of this optimization is whether to assign a given charging task to a specific charger. There are two major constraints to this optimization problem. The first is that at a given time one charger cannot be assigned to more that one task. The second constraint is that no single tasks can be assigned to more that one charger at a time. An example of a current plan overlapped with a previous plan is shown in Figure 1. The desired result from an optimization of charging assignments is shown in Figure 2.

# Mathmatically Formulated Problem

# Results 
The program optimized the given schedules the following show valid resulting scheduels.

