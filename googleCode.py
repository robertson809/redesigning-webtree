from __future__ import print_function
from ortools.linear_solver import pywraplp
from baseline_webtree import read_file
from array import *

def main():
  solver = pywraplp.Solver('SolveIntegerProblem', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
  
  student_requests, students_by_class, courses = read_file('testWB2.csv')
  num_students = len(student_requests)
  num_classes = len(courses)
  print(courses)
  
  #mat is a list of lists (2d matrix) of all the possible student class pairings
  mat = []
  #we want a variable for each possible student class pairing
  for i in range(0, num_students):
      mat.append([])
      for j in range(0,num_classes):
          mat[i].append(solver.IntVar(0.0, 1.0, str(i)+str(j)))
  
  #constrain that each student must have between 0 and 4 classes
  constraints = []
  for row in range(len(mat)):
      constraints.append(solver.Constraint(0.0, 4.0))
      for col in range(len(mat[0])):
          constraints[row].SetCoefficient(mat[row][col], 1.0)
  
  #get a ordered lists of course capacities
  course_capacities = []
  for course in courses:
      course_capacities.append(courses[course])
  
  #constrain that each course must not overflow its capacity
  for col in range(len(mat[0])):
      constraints.append(solver.Constraint(0.0, course_capacities[col]))
      for row in range(len(mat)):
          constraints[col].SetCoefficient(mat[row][col], 1.0)
          
      

  # Maximize x + 10 * y.
  objective = solver.Objective()
  objective.SetCoefficient(x, 1)
  objective.SetCoefficient(y, 10)
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
  variable_list = [x, y]

  for variable in variable_list:
    print('%s = %d' % (variable.name(), variable.solution_value()))

if __name__ == '__main__':
  main()