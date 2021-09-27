# Demo
To run a demo, install package dependencies from the Pipfile and run "new_webtree.py" with one .csv file from the data folder as a command line arguement.


# Redesigning WebTree

By Michael Robertson and George Baldini for Davidson College's Machine Reasoning HW4


### Table of Contents:
- [Abstract](#abstract)
- [Introduction](#introduction)
- [Background](#background)
- [Experiments](#experiments)
- [Results](#results)
- [Conclusions](#conclusions)
- [Contributions](#contributions)
- [Acknowledgements](#acknowledgements)
- [References](#references)


---
## Abstract

We model Davidson College’s problem of class assignment as
an integer programming constraint satisfaction problem using
anonymized data collected from 2013-2015 student WebTree
submissions. Our results provide a legitimate argument for
replacing WebTree. Our best algorithm outperforms WebTree
more often in our tests and also incorporates more factors into
its decision-making. Our solution improves the percentage of
students receiving classes in their major but violates WebTree
logic, ignoring class dependencies (i.e. “I want this class only
if I don’t get that class”). We conclude with ideas to further
improve our algorithm.

## Introduction

The Davidson College Registrar manages course assignments from over 400 courses to each of Davidson’s≈ 2 , 000
students each semester. To handle this problem, the Registrar uses a front-end application called “WebTree” to record
student preferences and back-end COBOL code, written by
a retired professor, to distribute classes based on preferences.
Davidson students, particularly upperclassmen, frequently criticize WebTree because it often leaves them 
without classes they need to graduate. In this paper, we offer an
alternative course selection algorithm that models this problem as a linear programming constraint 
optimization problem. We constructed our model with WebTree input data
from the fall and spring semesters of the 2013 and 2014 academic years. Each file contained the following columns:

- ID: student ID number
- CLASS: class standing of student
- CRN: unique identifier for a specific section of a course
    (what students select on WebTree)
- TREE: the tree number in which the current CRN was
    listed (1, 2, 3, or 4)
- BRANCH: the node in the tree where the CRN was listed.
    Nodes are numbered in level order, left-to-right, starting
    at 1
- COURSE_CEILING: enrollment limit for this CRN
- MAJOR: student’s major
- MAJOR2: student’s second major
- SUBJ: course subject code
- NUMB: course catalog number
- SEQ: course section number
       
 In section 2 we describe the process WebTree currently
    goes through in order to assign classes, and in section 3 we
    describe our own approach to modeling the problem. We
    present our results in section 4 and offer suggestions for improvements to our own model in 5.

## Background

The WebTree front-end web application allows students to
imput their preferences to 25 nodes on 4 trees. Each node
represents a course preference logically dependent on other
potential assignments. The pdf file "web_tree_worksheet" in the `/fig` folder illustrates the logical 
dependency of these nodes.
We modeled the WebTree input data as a ranked list of 48
choices, where each choice is a set of four classes. 
For example, a student’s first choice for a set of four classes would
be their 1 node class, their 1A node class, their 1AA node
class, and their 4A node class. Their 48th choice for a set
of four classes would be their 3 node class, their 3B class,
their 3BB class, and their 4D class. WebTree also includes
a “second pass” that executes if a student has less than four
classes after exhausting all 48 choices (as referenced in the
4D node in the worksheet in `/fig`). However, since satisfactory 
explanation has been provided by relevant parties, we have excluded
it from our interpretation of WebTree’s functioning.
The WebTree back-end algorithm first groups students
based on seniority, and then randomly ranks them within
each class, assigning them a lottery number. Moving
through the lottery numbers sequentially, it assigns a student
their top class choice if the assignment meets the following
requirements:
- The class has not exceeded its capacity.
- The student has not already been assigned this class.
- The student has not already been assigned four classes.


In the case that a student’s top choice violates one of these
conditions, WebTree looks to their next choice, and continues on until it either assigns a student a course or exhausts
their preferences.




## Experiments


In our solution of the problem, we modeled the final assignments in a student-class matrix with Boolean entries, which
lent itself to a mathematical description of the relevant constraints and quality of a solution.
For the variables of our CSP, we used a matrix of size S
by C, where S is the total number of students who submitted
WebTree preferences, andCis the total number of classes
offered. Each entry in the matrix P<sub>ij</sub> therefore corresponded
to a specific student-class combination. Each entry took a
Boolean value, where of 0 corresponded to that student not
taking the class, and 1 corresponded to the student taking the
class.
Our constraints were:

1. Every student must have between 2 and 4 classes, so the equation:
<p align="center">
<img src="https://render.githubusercontent.com/render/math?math=2\leq \sum  P_{ij}\leq 4">
</p>
where j ranges from 1 to C, must be true for every value of i from 1 to the number of students.

    

2. Every class must have a number of students in it between
    0 and its capacity:
<p align="center">
<img src="https://render.githubusercontent.com/render/math?math=0 \leq \sum P_{ij} \leq cp(C_j) \quad \forall \text{ columns } j"
</p>
   where cp(C<sub>j</sub>) is the capacity of the class corresponding to column j


3. No student can be in a class more than once. (Implicitly
    enforced through the modeling of the problem)
    
   
Solving the CSP requires an optimization function to describe quantitatively how well-suited a class assignment is
to a student’s choices. In our experiments, we varied this
function considerably to improve our results, but consider
as an example our original choice:

   
<p align="center">
<img src="https://render.githubusercontent.com/render/math?math=f_1(S_i, CRN) = g_i(CRN)\cdot h(CRN, g_i(CRN)) \cdot y_1(S_i) \cdot m_1(S_i, CRN)"
</p>

where

   - The function g<sub>i</sub>(CRN) is 48 minus number of theith student’s choice in which the CRN is found. For example, if
    course CRN 25143 is first found in a student’s 36th ranked
   WebTree choice of four classes,g<sub>i</sub>(25143)= 48 − 36 =12.
   - The function h(CRN,g<sub>i</sub>(CRN)) is the location of a class
    CRN within theith student’s ranked choice g(CRN).
    For example, if course CRN 25143 is found in a student’s 36th ranked WebTree choice of four classes, and
    it is the 3rd choice class in that choice of four classes,
    h(CRN,g(CRN))=3.
   - The function y<sub>1</sub> (S<sub>i</sub>) is the student’s class year (senior=4,... etc).
   - The functionm 1 (S<sub>i</sub>,CRN) returns 2 if the CRN references
   a class in student’s S<sub>i</sub>’s major, and 1 otherwise.
    By supplying Google’s “Glop” integer programming
solver with different versions offas our optimization function, we used them to find the optimal constrained assignment of students to classes (Perron 2011).


We created several different metrics of success to measure our solution against the original WebTree algorithm and
modified our optimization function f in order to improve our results.
   We first ran Glop using the example optimization function f<sub>1</sub> , and then modified f<sub>1</sub> after our solution did not 
outperform WebTree on our metrics. We remapped the output
   to change the relative weights between choices. Because g<sub>i</sub>
   and h<sub>i</sub>in f<sub>1</sub> are both linear functions of the class-student
pairing’s position in a list, a change by k positions in either
of these lists corresponds directly to a k change in the output
of that function.
This change doesn’t reflect all of the students’ actual 
preferences however. Students generally care much more about
moving from their fifth WebTree choice of four classes to
their sixth choice than about moving from their twenty-seventh choice to their twenty-eighth. To reflect this, we
mapped the output of g and h using two functions, a polynomial and a sigmoid, which preserved the ranges on the
domains, but altered the rates of change of the optimization value at different points, corresponding to students actual preferences. We also decreased the value of giving upperclass students their first choice, as well as giving majors their major choices. 
   We wrote y<sub>2</sub> (S<sub>i</sub>) to be such that
   y<sub>2</sub>(1) = 1.2, y<sub>2</sub>(2) = 1.5, y<sub>2</sub>(3) = 1.8 ,and y<sub>2</sub>(4) = 2
(where 1 corresponds to a first year student... etc), and
   wrote m<sub2>sug (S<sub>i</sub>,CRN) to return 1.3 if the class matched the 
students major, rather than 2 asm 1 did. Both return 1 if the
class and major do not match.




We first used a polynomial generated from interpolation
through the points (48,48), (1,1), and (20,10) to map the output. The first two points specified that the range doesn’t
change, and the third point seems like a reasonable 
assumption: the 20th choice should be worth approximately a fifth
as much as the first choice. Lagrange polynomial 
interpolation through these points produced the mapping function

   
<p align="center">
<img src="https://render.githubusercontent.com/render/math?math=P(x) = \frac{5}{266}x^2 - \frac{3}{38}x %2B+ \frac{20}{10}"
</p>


   Using this remap to modify the outputs of g<sub>i</sub> and h, we
create
   
      
<p align="center">
<img src="https://render.githubusercontent.com/render/math?math=f_2(S_i, CRN) = P(g_i(CRN))\cdot P(h(CRN, g_i(CRN))) \cdot y_2(S_i) \cdot m_2(S_i, CRN)"
</p>
   
   
We intended this mapping function to model the fast drop-off in valuation of choices. 
It attempts to account for the
fact that students care much more about changing from their
first choice to their third choice than from changing from
their twentieth choice to their twenty-first choice. However,
because of the drastically poor performance of the 
optimization on measures of success described in our results, we reworked our mapping function.
   We created f<sub>3</sub> by changing our modeling function from an
interpolating polynomial to a sigmoid. This function models
the high valuation by students of their top choices, and the
sharp drop-off in valuation around their sixth choice. Using
a new sigmoid mapping function
   

<p align="center">
<img src="https://render.githubusercontent.com/render/math?math=S(x) = \frac{48}{1 %2B+ e^{-0.5(x-37)}}"
</p>
 
 we again modified the outputs of g<sub>i</sub> and h to create
   
<p align="center">
<img src="https://render.githubusercontent.com/render/math?math=f_3(S_i, CRN) \cdot S(h(CRN,g_i(CRN))) \cdot y_2(S_i) \cdot m_2(S_i, CRN)."
</p>
 
We compare the results of these different optimization
functions in the next sections.

&nbsp;
   
<p align="center">
    
  <img src="https://raw.githubusercontent.com/robertson809/redesigning-webtree/master/fig/desmos_functions.png" alt="drawing" width="400"/>
</p>
   
   
 <p align = "center">
   Figure 1:f<sub>1</sub> (Blue),f<sub>2</sub> (Green), and f<sub>3</sub> (Red). Each function
attempts to model student valuation of relative parts of their
WebTree rankings. Image courtesy of Desmos Grapher.
   </p>

   


## Results

As shown in Figure 2, each algorithm had varying results.
Ourf 3 gave a higher percentage of students their first and
second choices for most semesters, while WebTree (f 0 ) 
performed better for students’ third and fourth choices. We do
not know whyf 2 performed so miserably, but we can 
conclude that a polynomial mapping function does not correctly
model students’ interests.
Our integer programming solver with f 1 and f 3 beat
WebTree in assigning more major classes to students who
asked for them. We expected this outcome, because we
added a positive factor in our optimization function based
on whether class-student pairing matched a student with a
class in their major.
We have bolded the highest percentage in each row for
each year. In totalf 3 has 19 bolded entries,f 2 has 0,f 1 has
8, andf 0 has 14. This suggests that our linear programming
model better solved the WebTree model than the baseline
current application of WebTree, but only when using thef 3
optimization function.

## Conclusions


In this paper, we sought to improve Davidson’s WebTree 
algorithm by modeling it as constraint satisfaction problem.

<p align="center">
    
  <img src="https://raw.githubusercontent.com/robertson809/redesigning-webtree/master/fig/results_table.png " alt="drawing" width="700"/>
</p>
   
   <p align="center">
      Figure 2: Comparison of our algorithms (f<sub>1</sub> - linear, f<sub>2</sub> - polynomial, f<sub>3</sub> - sigmoid) to the traditional WebTree, f<sub>0</sub>. An entry in
“x” Choices for functionfiindicates the percentage of students who received theirxth choice, where their first choice is their 1
node class on WebTree, their second is their 1A class, third is their 1AA class, and fourth is their 4A class. Major First Choice
and Second Choice refer to the percentage of students whose first and second choice, respectively, were classes in their major,
and who got that class. First choice percentages are also broken down by year in the bottom four columns.
   </p>

Our results offer an argument to replace WebTree with a 
linear programming solver using thef 3 optimization function,
as our algorithm produces the highest percentages most 
often in Figure 2. Additionally, our algorithm also 
considers an additional factor in this problem: students’ majors.
Due to the common dissatisfaction of students not receiving 
classes in their majors, we provide the functionality to
remedy that inconsistency.
   
   
In order for our algorithm to maximize its payoff, it would
require replacing the data input portion of the current 
WebTree program. Our approach can offer students a set of
classes that they didn’t request together, so we suggest 
modifying the front-end data input part of WebTree. We would
solicit a one “must-have” course, two sets of three courses
of which the student would highly value getting one of, and
a remaining set of six courses the student would like one
of, but prioritizes least. The current WebTree data intake
focuses heavily on the logical dependency of often 
redundant class dependencies, forcing the student to describe their
preferences in repetitive detail. Because students generally
want one to two courses for their major, one or two for a 
minor or distribution requirement, and one for general interest,
students’ choices generally don’t have complex 
dependencies, making much of the logical structure of WebTree 
useless and students’ entries in it redundant. For example, while
a student may only want to take one 300-level anthropology
class out of a ranked list of three, the course assignment they
receive from that group is unlikely to effect their their ranked
list of three language courses they’d like to use to fulfill their
language requirement.
   
   
While our approach rarely makes gains of more than 10%
on our metrics over the baseline WebTree, our model does
allow for easy adjustment of class year weighting. If, for
example, seniors successfully convinced the administration
through student government that their preferences should
be weighed more heavily over first-years than our model
currently does, we could easily accommodate this request
by simply changing a weight in our optimization function,
while the baseline WebTree has no similar easily 
implementable fix. Similarly, if large numbers of students do
not receive the classes in their major they need to 
graduate, our WebTree algorithm could simply be rerun with a
larger output on ourmfunction in the case of a match, and
the new student-class assignment solution produced by 
rerunning Glop would accommodate the desired change.

## Contributions
   
Baldini and Robertson both contributed to each function of
the code. Robertson focused more on creating our model,
while Baldini spent more time working on the data intake
and testing cases. Both authors co-authored each section of
the paper and proof-read the entire document.

## Acknowledgements

Thank you Dr. Ramanujan for guidance throughout the 
process of implementing our algorithm.

## References

Davidson College. WebTree Worksheet. https:
//www.davidson.edu/Documents/Administrative%20Department/Registrar/WebTreeWorksheet.pdf.
Retrieved on Mar. 25, 2019.
   
   
Perron, L. 2011. Operations Research and Constraint 
Programming at Google. In Lee, J., ed.,Principles and Practice
of Constraint Programming – CP 2011, 2–2. Berlin, 
Heidelberg: Springer Berlin Heidelberg.
