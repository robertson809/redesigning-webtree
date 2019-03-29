from __future__ import print_function
from ortools.linear_solver import pywraplp
from baseline_webtree import read_file, student_choices
import math

student_requests, students_by_class, courses, course_major, student_major = read_file(sys.argv[1])
num_students = len(student_requests)
num_classes = len(courses)

#get a list of choices
ranked = student_choices(student_requests)
# student IDs
student_ids = list(student_requests.keys())
# course CRNs
course_crns = list(courses.keys())

def main():
    solver = pywraplp.Solver('SolveIntegerProblem', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

    #mat is a list of lists (2d matrix) of all the possible student class pairings
    mat = []
    #we want a variable for each possible student class pairing
    for i in range(0, num_students):
        mat.append([])
        for j in range(0, num_classes):
            mat[i].append(solver.IntVar(0.0, 1.0, str(i)+" "+str(j)))

    #constrain that each student must have between 0 and 4 classes
    constraints = []
    for row in range(len(mat)):
        constraints.append(solver.Constraint(2.0, 4.0))
        for col in range(len(mat[0])):
            constraints[row].SetCoefficient(mat[row][col], 1.0)

    #get a ordered lists of course capacities
    course_capacities = []
    for course in courses:
        course_capacities.append(courses[course])

    #constrain that each course must not overflow its capacity
    shift = len(constraints)
    for col in range(len(mat[0])):
        constraints.append(solver.Constraint(0.0, course_capacities[col]))
        for row in range(len(mat)):
            constraints[shift+col].SetCoefficient(mat[row][col], 1.0)

    # Make objective function
    objective = solver.Objective()
    for row in range(len(mat)):
        for col in range(len(mat[0])):
            #we need to access all of this information
            #we have the position of the student in the matrix, and the position of the class in the matrix
            #we need to find the year and the major
            objective.SetCoefficient(mat[row][col], weight(student_ids[row], course_crns[col]))
    objective.SetMaximization()


    # Solve the problem and print the solution.
    result_status = solver.Solve()
    # The problem has an optimal solution.
    assert result_status == pywraplp.Solver.OPTIMAL

    # The solution looks legit (when using solvers other than
    # GLOP_LINEAR_PROGRAMMING, verifying the solution is highly recommended!).
    assert solver.VerifySolution(1e-7, True)

    print('Number of variables =', solver.NumVariables())
    print('Number of constraints =', solver.NumConstraints())

    # The objective value of the solution.
    print('Optimal objective value = %d' % solver.Objective().Value())
    print()
    # The value of each variable in the solution.
    # variable_list = [x, y]
    #
    # for variable in variable_list:
    #     print('%s = %d' % (variable.name(), variable.solution_value()))

    assignments = {}
    for row in range(len(mat)):
        for col in range(len(mat[0])):
            variable = mat[row][col]
            split = variable.name().split()
            name = int(split[0])+1
            course_index = int(split[1])
            val = variable.solution_value()
            if val:
                if name in assignments:
                    assignments[name].add(course_crns[course_index])
                else:
                    assignments[name] = set([course_crns[course_index]])

    # Print course assignments
    # for s in assignments:
    #     print(s, list(assignments[s]))

    first_choices = 0
    
    pop = 0
    for s in ranked:
        if ranked[s][0][0] in list(assignments[s]):
            first_choices += 1
        if ranked[s][0][0] != None:
            pop += 1
    print("First Choices")
    print(first_choices, pop, float(first_choices)/pop)

    second_choices = 0
    pop = 0
    for s in ranked:
        if ranked[s][0][1] in list(assignments[s]):
            second_choices += 1
        if ranked[s][0][0] != None:
            pop += 1
    print("Second Choices")
    print(second_choices, pop, float(second_choices)/pop)

    third_choices = 0
    pop = 0
    for s in ranked:
        if ranked[s][0][2] in list(assignments[s]):
            third_choices += 1
        if ranked[s][0][0] != None:
            pop += 1
    print("Third Choices")
    print(third_choices, pop, float(third_choices)/pop)

    fourth_choices = 0
    pop = 0
    for s in ranked:
        if ranked[s][0][3] in list(assignments[s]):
            fourth_choices += 1
        if ranked[s][0][0] != None:
            pop += 1
    print("Fourth Choices")
    print(fourth_choices, pop, float(fourth_choices)/pop)

    # First choice was a class in student's major
    major_choices = 0
    pop = 0
    for s in ranked:
        first_choice = ranked[s][0][0]
        major = student_major[s]
        if 'X' in major[0]:
            major[0] = major[0][1:]
        if "UND" in major or "XUND" in major:
            continue
        if first_choice != None and course_major[first_choice] in major:
            pop += 1
            if first_choice in list(assignments[s]):
                major_choices += 1

    print("Major First Choice")
    print(major_choices, pop, float(major_choices)/pop)
    
    print("1r, 2r, 3r, 4r, Mr", sys.argv[1])
    print(float(first_choices)/pop)
    print(float(second_choices)/pop)
    print(float(third_choices)/pop)
    print(float(fourth_choices)/pop)
    print(float(major_choices)/pop)
    

    # Second choice was a class in student's major
    major_choices = 0
    pop = 0
    for s in ranked:
        second_choice = ranked[s][0][1]
        major = student_major[s]
        if 'X' in major[0]:
            major[0] = major[0][1:]
        if "UND" in major or "XUND" in major:
            continue
        if second_choice != None and course_major[second_choice] in major:
            pop += 1
            if second_choice in list(assignments[s]):
                major_choices += 1

    print("Major Second Choice")
    print(major_choices, pop, float(major_choices)/pop)

    first_choices_seniors = 0
    seniors = 0
    for s in ranked:
        if s in students_by_class["SENI"]:
            seniors += 1
            if ranked[s][0][0] in list(assignments[s]):
                first_choices_seniors += 1
    print("First Choices Seniors")
    print(first_choices_seniors, seniors, float(first_choices_seniors)/seniors)

    first_choices_juniors = 0
    juniors = 0
    for s in ranked:
        if s in students_by_class["JUNI"]:
            juniors += 1
            if ranked[s][0][0] in list(assignments[s]):
                first_choices_juniors += 1
    print("First Choices Juniors")
    print(first_choices_juniors, juniors, float(first_choices_juniors)/juniors)

    first_choices_sophs = 0
    sophs = 0
    for s in ranked:
        if s in students_by_class["SOPH"]:
            sophs += 1
            if ranked[s][0][0] in list(assignments[s]):
                first_choices_sophs += 1
    print("First Choices Sophomores")
    print(first_choices_sophs, sophs, float(first_choices_sophs)/sophs)

    first_choices_fresh = 0
    fresh = 0
    for s in ranked:
        if s in students_by_class["FRST"]:
            fresh += 1
            if ranked[s][0][0] in list(assignments[s]):
                first_choices_fresh += 1
    print("First Choices Freshmen")
    print(first_choices_fresh, fresh, float(first_choices_fresh)/fresh)

# get the weight of how "good" it is to give a student a class, based on its
# position in the webtree ranking, the class year of the student, and their major
def weight(student, class_crn):
    score = 0

    found = False
    best = 0
    for four_classes in ranked[student]:
        if class_crn in four_classes:
            found = True
            i = (4-four_classes.index(class_crn)) * 12
            score += log_48(len(ranked[student] - ranked[student].index(four_classes)) * log_48(i)   
            break
    if not found:
        score -= 10000

    for year in students_by_class:
        if student in students_by_class[year]:
            # OTHER year multiplied by 1
            if year == "FRST":
                score *= 1.2
            elif year == "SOPH":
                score *= 1.5
            elif year == "JUNI":
                score *= 1.8
            else:
                score *= 2
            break

    major = student_major[student]
    if 'X' in major[0]:
        major[0] = major[0][1:]
    if course_major[class_crn] in major:
        score *= 1.3
    return score
    
    #interpolating f(192) = 192, 
def poly_map(x):
    return (13.0/2478.0) * (x ** 2) - (31.0/2478.0)*x + (416.0/413.0)
    #using a logistic function
    #https://www.desmos.com/calculator/5kggnehdh1
def log_48(x):
    return 48.0/(1 + math.exp(-0.5*(x-37.0)))
if __name__ == '__main__':
    main()
