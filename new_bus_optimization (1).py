import random
import typing
from typing import List as lst
from typing import Tuple as tpl

import gurobipy as grb
import matplotlib.pyplot as plt
from gurobipy import *
from matplotlib.patches import Rectangle


def schedule_buses(
    n_tasks: int,
    charger_ids: lst[str],
    task_pairs: lst[tpl[int, int]],
    weights,
) -> lst[str]:
    """Optimize the bus charger assignment problem.

    Args:
        n_tasks: number of total tasks
        charger_ids: list of charger ids
        task_v_time: 2d array where each sub array correspond to a time step in
            chronological order

    Returns:
        The array of all variables in the form
        [(task0, charger0), (task0, charger1), ... (taskN, chargerN))]
        each index is 1 if chosen and 0 if not.
    """
    # Create a new model
    model = grb.Model()
    # Add variables which correspond to 2d array where first index is task 
    # number and second index is charger id
    task_to_chargers = model.addVars(
        n_tasks, charger_ids, vtype=grb.GRB.BINARY, name="task_charger"
    )
    # coef houses the weights for each task with the same dimensionality as
        # constraints
    coeff = []
    # multiply 1 + weight to decision variables
    for key in weights.keys():
        charger_id = weights[key][0]
        added_weight = weights[key][1]
        counter = 0
        task_weights = []
        while counter < len(charger_ids):
            print(counter)
            loop_charger_id = charger_ids[counter]
            if loop_charger_id == charger_id:
                task_weights.append(1 + added_weight)
            else:
                task_weights.append(1)
            counter += 1
        print(task_weights)
        coeff.append(task_weights)
    

    # create objective function
    objective = LinExpr([c for c1 in coeff for c in c1], task_to_chargers.select("*"))
    # coef_flat = [coeff[i][j] * task_to_chargers[i, charger_ids[j]]
        # for i in range(len(coeff)) for j in range(len(coeff[i]))] 
    # objective = grb.quicksum(coef_flat)

    model.setObjective(objective, grb.GRB.MAXIMIZE)
    # add constraints that each task can only be assigned to one charger
    for task_charg in range(n_tasks):
        element = [task_to_chargers[task_charg, id_] for id_ in charger_ids]
        model.addConstr(grb.quicksum(element) == 1)
    # Loop through all tasks that overlap
    for pair in task_pairs:
        for charger_id in charger_ids:
            # add constraint that if two tasks overlap, they cannot 
                # be assigned to the same charger
            model.addConstr(
                task_to_chargers[pair[0], charger_id]
                + task_to_chargers[pair[1], charger_id]
                <= 1
            )

    # Optimise the model
    model.write("model.lp")
    model.optimize()
    model.printAttr("X")
    # X array is in the form 
        # [(task0, charger0), (task0, charger1), ... (taskN, chargerN))]
    # each index there is a zero if that assignment was not chosen and a 
        # 1 if it was
    return unpack_X(model.X, charger_ids)


def unpack_tasks(
    task_list: typing.List[typing.Tuple[float, float, int, int]]
) -> typing.List[typing.Tuple[int, int]]:
    """Take task list and create lists of overlapping times.

    Task list is of the form (start_time, end_time, bus_id,
        task_number.

    Args:
        task_list: list of all charging_tasks

    Returns:
        List of overlapping tasks of the form
        [(task #1, task #2), (task #1, task #3).....]

    """
    all_overlapping_tasks = []
    for i in range(len(task_list)):
        for j in range(i + 1, len(task_list)):
            if (helper_check_overlap(
                task_list[i][0], task_list[i][1], task_list[j][0], task_list[j][1]
                )):
                all_overlapping_tasks.append((task_list[i][3], task_list[j][3]))
    return all_overlapping_tasks


def check_overlap(time_to_check, start_time, end_time) -> bool:
    """Check if time is between start and end time."""
    if end_time > time_to_check > start_time or end_time < time_to_check < end_time:
        return True
    return False


def unpack_X(X: lst[int], charger_ids: lst[str]) -> lst[str]:
    """Unpack the solution X array into a more readable format.

    Args:
        X: array of all optimization variables in the set {1, 0}
        charger_ids: all charger ids

    Returns:
        returns an array 1d array where each index is the charger id 
        corresponding to the task that of the same number 
        (i.e task_1 = chosen_charger[1])
    """
    count = 0
    # create an array were each index in the array corresponds to a task in order
    chosen_slots = []
    for element in X:
        count += 1
        # if the element is 1 then the charger was chosen
        if element == 1:
            # use the count to display the given charger id
            chosen_slots.append(charger_ids[count - 1])
        # if the count has reached the number of chargers then reset it
        if count == len(charger_ids):
            count = 0
    return chosen_slots


def graph_tasks(sol_to_task: typing.Dict[tpl[float, float, int, int], str]):
    """Create a graph of the tasks and their corresponding charger."""
    fig, ax = plt.subplots()
    plt.xlabel("Time (s)")
    plt.ylabel("Bus ID")
    for task in sol_to_task.keys():
        color = "#" + "".join([random.choice("0123456789ABCDEF") for j in range(6)])
        rec = Rectangle(
            (task[0], task[2]),
            task[1] - task[0],
            1,
            label=f"Task id: {task[3]}, Charger id: {sol_to_task[task]}",
            color=color,
        )
        ax.add_patch(rec)
    ax.legend()
    ax.plot()
    plt.show()


def helper_check_overlap(
    first_start: float, first_end: float, second_start: float, second_end: float
) -> bool:
    """Call check overlap with all possible permutations."""
    if (
        check_overlap(first_start, second_start, second_end)
        or check_overlap(first_end, second_start, second_end)
        or check_overlap(second_start, first_start, first_end)
        or check_overlap(second_end, first_start, first_end)
    ):
        return True
    return False


def compare_overlap(
    prev_plan: lst[tpl[float, float, int, int, str]],
    curr_plan: lst[tpl[float, float, int, int]],
) -> typing.Dict[int, tpl[str, float]]:
    """Compare the previous plan to the current plan."""
    # new tuple that will house curr_plan but adding two other elements one for charger
    # id and the other for overlap percentage
    curr_plan_with_weights = {}

    for task in curr_plan:
        # create iterator that only has tasks with same bus id
        filtered = filter(lambda prev_task_: prev_task_[2] == task[2], prev_plan)
        print(task)
        overlap = 0.0
        charger_id = "ZZZZZZ"
        for prev_task in list(filtered):
            # if the previous task has overlap with current task
            if helper_check_overlap(prev_task[0], prev_task[1], task[0], task[1]):
                # check which task starts later that is the beginning of overlap
                begin_overlap = 0.0
                if prev_task[0] < task[0]:
                    begin_overlap = task[0]
                else:
                    begin_overlap = prev_task[0]
                # check which task ends first that is the end of the overlap
                end_overlap = 0.0
                if prev_task[1] < task[1]:
                    end_overlap = prev_task[1]
                else:
                    end_overlap = task[1]
                # total overlap
                total_overlap = end_overlap - begin_overlap
                # total time of the current_task
                curr_total_seconds = task[1] - task[0]
                # get the percentage of overlap with the current window
                percent_overlap = total_overlap / curr_total_seconds
                # if there is are multiple charging session that overlap with
                    # current task take the one that is the the largest
                if percent_overlap > overlap:
                    overlap = percent_overlap
                    charger_id = prev_task[4]
        curr_plan_with_weights[task[3]] = (charger_id, overlap)
    return curr_plan_with_weights


def _main(args=None):
    task_v_time = [
        (200.24, 350.34, 1, 0),
        (230.6, 600, 2, 1),
        (400.1, 500.2, 1, 2),
        (550.2, 700.3, 1, 3),
    ]
    prev_plan = [
        (180.2, 220.3, 1, 0, "A"),
        (200.0, 400.0, 2, 1, "C"),
        (560.0, 580.0, 2, 2, "B"),
        (560.0, 580.0, 1, 3, "B"),
    ]
    task_pairs = unpack_tasks(task_v_time)
    tasks_weighted = compare_overlap(prev_plan, task_v_time)
    for task in tasks_weighted.keys():
        print(
            f"Task {task} has charger {tasks_weighted[task][0]}" 
            f"and overlap {tasks_weighted[task][1]}"
        )
    n_tasks = 4
    charger_ids = ["A", "B", "C"]
    X = schedule_buses(n_tasks, charger_ids, task_pairs, tasks_weighted)
    sol_to_task = {}
    for i in range(len(X)):
        for task in task_v_time:
            if task[3] == i:
                sol_to_task[task] = X[i]
    for key in sol_to_task.keys():
        print(f"charger {key} = {sol_to_task[key]}")
    graph_tasks(sol_to_task)


if __name__ == "__main__":
    _main()
