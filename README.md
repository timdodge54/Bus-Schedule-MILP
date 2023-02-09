# Bus Scheduling Mixed Integer Programming 

This paper describes a mixed integer linear programming optimization problem that solves a task assignment problem. This task assignment problem is housed within a larger optimization problem that is attempting to minimize the total cost to charge a fleet of electric vehicles. The optimization is constantly updating and has the potential to reassign buses at given intervals and the goal of this individual problem is to minimize the amount of charger reassignment that occurs. The results show that it is possible to find a feasible solution by comparing the overlap of previous plans.
## Previous and Current Plan
![sched](https://user-images.githubusercontent.com/93363769/214746592-c7352b93-dea3-4e9e-96d2-b59dd1722653.jpg)
# Desired result
![desired_result](https://user-images.githubusercontent.com/93363769/214746783-c0156566-4fda-4f6b-afce-8a2fd8ee16b3.jpg)

# Problem Description

The Utah State Robotics lab is working on an optimal scheduling program allowing multiple electric buses to charge while minimizing the load on the electrical grid at peak times to reduce the total cost of charging. The greater program utilizes a receding horizon optimization planner. For this project an initial plan is made for the entire day then the planner looks over some horizon time period and plans for that horizon time. The planner decides on when a certain bus should charge at a certain station with a certain type of charger (fast, medium, or slow). A given station has a set number of fast, medium, and slow chargers. This optimization problem takes the information provided by the receding horizon planner and plans which specific charger within the given charger type should be chosen at a given station.

The overall goal of this nested optimization problem is to take the information of the long term and short-term plan and minimizes charger reassignment. Meaning if the planner originally had a charging task scheduled at some time to be assigned to a given charger. When a new plan is made by the receding horizon planner it will disincentivize assigning a charging task occurring at the same time to assign said task to another charger.  

The decision of this optimization is whether to assign a given charging task to a specific charger. There are two major constraints to this optimization problem. The first is that at a given time one charger cannot be assigned to more that one task. The second constraint is that no single tasks can be assigned to more that one charger at a time. An example of a current plan overlapped with a previous plan is shown in Figure 1. The desired result from an optimization of charging assignments is shown in Figure 2.

# Mathmatically Formulated Problem
For the purpose of the mathematical formulation of the optimization problem variable
notation must be defined. For this problem the decision variables are the
choice of whether to assign charging task j to a charger i. These decision
variables will be referred to as $x_{ij}$. The number of tasks is
defined as $n_j$ and the number of chargers
is $n_i$. For a given task i the start time is $t_{s,i} and the end time is $t_{e,i}$. The utility score which is the percent overlap with a previous plan for a given task i assigned to a
charger i is defined as $u_{i,j}$.

The objective function is maximizing the product $x_{i,j}$ of $u_{i,j}$ and . This incentivizes not
reassigning charging tasks to different chargers but does not strictly enforce
not reassigning charging tasks. The constraint of not having one charging task
assigned to multiple chargers is by summing all $x_{i,j} for all j and setting a less than or equal to
constraint at 1.

The constraint for guaranteeing that one charger is only assigned to one task at a
time all overlapping pairs are summed and an inequality constraint less than or
equal to one is set for all overlapping pairs. Tasks are defined as overlapping
if the $t_{s,j}$ or $t_{e,j} is in between the times for task j + 1. In
mathematical terms $(t_{s,j + 1} \leq t_{s,j} \leq t_{e,j +1}) \lor t_{s,j + 1} \leq t_{e,j} \leq t_{e,j+1}$ .

The overall optimization problem can then be formulated as the following

![opt_form](https://user-images.githubusercontent.com/93363769/214747838-501b054a-7293-4bec-8bae-4980448c4e34.jpg)

# Results 
The program optimized the given schedules the following show valid resulting scheduels.
## Previous Plan for Example Optimization Problem
![prev_1](https://user-images.githubusercontent.com/93363769/214748259-f28863d7-3c1c-432c-ae27-398e04604451.jpg)


![prev_2](https://user-images.githubusercontent.com/93363769/214748355-a4018d88-7837-4bdc-b970-5c9ea3e03bdf.jpg)

## Optimized Result

![res_1](https://user-images.githubusercontent.com/93363769/214748442-3b60089a-db29-403f-b794-eb28c1461864.jpg)

![res_2](https://user-images.githubusercontent.com/93363769/214748457-4b7dd8ff-934d-4259-99c7-2d9f8e9fc8c9.jpg)

