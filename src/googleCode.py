from __future__ import print_function
from ortools.linear_solver import pywraplp
from baseline_webtree import read_file, student_choices

student_requests, students_by_class, courses, course_major, student_major = read_file('../data/fall-2013.csv')
num_students = len(student_requests)
num_classes = len(courses)

#get a list of choices
ranked = student_choices(student_requests)
# student IDs
student_ids = list(student_requests.keys())
# course CRNs
course_crns = list(courses.keys())

def main():
    optimize()
def optimize():
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
        constraints.append(solver.Constraint(0.0, 4.0))
        for col in range(len(mat[0])):
            constraints[row].SetCoefficient(mat[row][col], 1.0)

    #get a ordered lists of course capacities using the CRN to capacity dictionary
    course_capacities = []
    for course in courses:
        course_capacities.append(courses[course])

    #constraint that each course must not overflow its capacity
    #make sure we pick up where we left off with shift
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

    """Solve the problem and print the solution."""
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

    #dictionary from student id to four courses they're assigned
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
    for s in assignments.keys():
        if ranked[s][0][0] in list(assignments[s]):
            first_choices += 1
    print("First Choices")
    print(first_choices, num_students, float(first_choices)/num_students)
    
    #a dictionary from student ids to four courses they're assigned
    return assignments

    

# get the weight of how "good" it is to give a student a class, based on its
# position in the webtree ranking, the class year of the student, and their major
def weight(student, class_crn):
    score = 0

    found = False
    for four_classes in ranked[student]:
        if class_crn in four_classes:
            found = True
            score += (len(ranked[student]) - ranked[student].index(four_classes)) * (4-four_classes.index(class_crn))
            break
    if not found:
        score -= 10000

    for year in students_by_class:
        if student in students_by_class[year]:
            # OTHER year multiplied by 1
            if year == "FRST":
                score *= 2
            elif year == "SOPH":
                score *= 3
            elif year == "JUNI":
                score *= 4
            else:
                score *= 5
            break

    if course_major[class_crn] in student_major[student]:
        score *= 2

    return score

if __name__ == '__main__':
    main()
