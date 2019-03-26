from __future__ import print_function
from ortools.linear_solver import pywraplp
from baseline_webtree import read_file, student_choices, assign_random_numbers, run_webtree
import time, sys
WT_CHOICE_LEN = 48



student_requests, students_by_class, courses, course_major, student_major = read_file(sys.argv[1])
num_students = len(student_requests)
num_classes = len(courses)

                              
#a dictionary from student ID to a list of their ranked 48 choices
ranked = student_choices(student_requests)

# student IDs
student_ids = list(student_requests.keys())
# course CRNs
course_crns = list(courses.keys())

def main():
    start = time.time()
    assignments = optimize()
    finish = time.time()
    print('running time is ',  finish - start)
    
    first_choices = 0
    for s in ranked:
        if ranked[s][0][0] in list(assignments[s]):
            first_choices += 1
    second_choices = 0
    for s in ranked:
        if ranked[s][0][1] in list(assignments[s]):
            second_choices += 1
            
    
            
    print("Improved First Choices")
    print(first_choices, num_students, float(first_choices)/num_students)
    
    print("Second Choices")
    print(second_choices, num_students, float(second_choices)/num_students)
def optimize():
    print(ranked)
    #import glop, the integer programming solver
    solver = pywraplp.Solver('SolveIntegerProblem', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

    #mat is a list of lists (3d matrix) of all the possible student class pairings
    #the students are ordered by their IDs and the CRNs are ordered by their order from
    #courses
    mat = []
    #we want a variable for each possible student class pairing
    for std in range(0, num_students):
        mat.append([])
        for class_num in range(0, num_classes):
            mat[std].append([])
            #if(variable is in the right ranked choice for the student, let it take on a 1 value)
            choice_num = 0
            for four_classes in ranked[std+1]:
                choice_num += 1
                if course_crns[class_num] in four_classes: 
                    mat[std][class_num].append(solver.IntVar(0.0, 1.0, str(std)+" "+str(class_num) +" "+ str(choice_num)))
                else:
                    mat[std][class_num].append(None)
       
    

    #####################CONSTRAINT 1, STUDENT CLASSES FROM 2 to 4 ###########################
    #constrain that each student must have between 2 and 4 classes
    #\sum_j=0^{num_classes}, k=0^{48} < 4
    stud_constraint = []
    for row in range(num_students):
        stud_constraint.append(solver.Constraint(2.0, 4.0))
        #add the weights to the linear terms of constraint student [row]
        for col in range(num_classes):
            for dep in range(WT_CHOICE_LEN):
                #sum of all the classes and position binary numbers is less than 4, weighted with 1
                #mat[row][col][depth] is the corresponding variable
                if mat[row][col][dep] is not None:
                    stud_constraint[row].SetCoefficient(mat[row][col][dep], 1.0)
  

    #####################CONSTRAINT 2, CLASS OCCUPANCY FROM 0 to CAPACITY ###########################
    #constraint that each course must not overflow its capacity
    #get a ordered lists of course capacities using the CRN to capacity dictionary
    course_capacities = []
    for course in courses:
        course_capacities.append(courses[course])

    cor_constraint = []
    #don't need to actually save the constraints beyond adding weighted coefficients to them
    #for all classes j /sum_i = 0 ^{num_students}, k=0^{48} C_ijk < capacity
    for col in range(num_classes):
        cor_constraint.append(solver.Constraint(0.0, course_capacities[col]))
        for row in range(num_students):
            for dep in range(WT_CHOICE_LEN):
                #sum of binary number for a corse over all students and lists cannot get over
                #course capacity = course_capacities[col], mat[row][col][dep] is binary variable
                if mat[row][col][dep] is not None:
                    cor_constraint[col].SetCoefficient(mat[row][col][dep], 1.0)
    

    #####################CONSTRAINT 3, COURSES MUST COME FROM SAME WT 'CHOICE' ####################
    #constraint that the four courses must come from the same webtree "selection"
    sel_constraint = []
    #for all lists k /sum_{i = 0} ^{num_students}, _j=0^{num_classes}
    for std in range(num_students):
        sel_constraint.append(solver.Constraint(4,4))
        for choice in range(WT_CHOICE_LEN):
            if mat[std][class_num][choice] is not None:
                sel_constraint[dep].SetCoefficient(mat[row][col][dep], 1.0)
        
    
    # Make objective function
    objective = solver.Objective()
    for row in range(num_students):
        for col in range(num_classes):
            for dep in range(WT_CHOICE_LEN):
            #we need to access all of this information
            #we have the position of the student in the matrix, and the position of the class in the matrix
            #we need to find the year and the major
                if mat[row][col][dep] is not None:
                    objective.SetCoefficient(mat[row][col][dep], weight(student_ids[row], course_crns[col]))
    objective.SetMaximization()
    
    
    """Solve the problem and print the solution."""
    result_status = solver.Solve()
    print ('henlo')  
    # The problem has an optimal solution.
    #assert result_status == pywraplp.Solver.OPTIMAL

    # The solution looks legit (when using solvers other than
    # GLOP_LINEAR_PROGRAMMING, verifying the solution is highly recommended!).
    #assert solver.VerifySolution(1e-7, True)

    print('Number of variables =', solver.NumVariables())
    print('Number of constraints =', solver.NumConstraints())

    # The objective value of the solution.
    print('Optimal objective value = %d' % solver.Objective().Value())
    print()
    
    

    #dictionary from student id to four courses they're assigned
    assignments = {}
    for row in range(len(mat)):
        for col in range(len(mat[0])):
            for dep in range(WT_CHOICE_LEN):
                variable = mat[row][col][dep]
                split = variable.name().split()
                name = int(split[0])+1
                course_index = int(split[1])
                val = variable.solution_value()
                if val:
                    if name in assignments:
                        assignments[name].add(course_crns[course_index])
                    else:
                        assignments[name] = set([course_crns[course_index]])
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
            score += (len(ranked[student]) - ranked[student].index(four_classes)) * ( - four_classes.index(class_crn))
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

    return score

if __name__ == '__main__':
    main()
