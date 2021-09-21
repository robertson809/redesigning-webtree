# Redesigning WebTree

## George Baldini and Michael Robertson

```
{gebaldini,mirobertson}@davidson.edu
Davidson College
Davidson, NC 28035
U.S.A.
```
```
Abstract
```
```
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
```
## 1 Introduction

The Davidson College Registrar manages course assign-
ments from over 400 courses to each of Davidson’s≈ 2 , 000
students each semester. To handle this problem, the Regis-
trar uses a front-end application called “WebTree” to record
student preferences and back-end COBOL code, written by
a retired professor, to distribute classes based on prefer-
ences.
Davidson students, particularly upperclassmen, fre-
quently criticize WebTree because it often leaves them with-
out classes they need to graduate. In this paper, we offer an
alternative course selection algorithm that models this prob-
lem as a linear programming constraint optimization prob-
lem. We constructed our model with WebTree input data
from the fall and spring semesters of the 2013 and 2014 aca-
demic years. Each file contained the following columns:

- ID: student ID number
- CLASS: class standing of student
- CRN: unique identifier for a specific section of a course
    (what students select on WebTree)
- TREE: the tree number in which the current CRN was
    listed (1, 2, 3, or 4)
- BRANCH: the node in the tree where the CRN was listed.
    Nodes are numbered in level order, left-to-right, starting
    at 1
- COURSECEILING: enrollment limit for this CRN
- MAJOR: student’s major
- MAJOR2: student’s second major
    - SUBJ: course subject code
    - NUMB: course catalog number
    - SEQ: course section number
       In section 2 we describe the process WebTree currently
    goes through in order to assign classes, and in section 3 we
    describe our own approach to modeling the problem. We
    present our results in section 4 and offer suggestions for im-
    provements to our own model in 5.

## 2 Background

```
The WebTree front-end web application allows students to
imput their preferences to 25 nodes on 4 trees. Each node
represents a course preference logically dependent on other
potential assignments. Figure 1 describes the logical depen-
dency of these nodes.
We modeled the WebTree input data as a ranked list of 48
choices, where each choice is a set of four classes. For ex-
ample, a student’s first choice for a set of four classes would
be their 1 node class, their 1A node class, their 1AA node
class, and their 4A node class. Their 48th choice for a set
of four classes would be their 3 node class, their 3B class,
their 3BB class, and their 4D class. WebTree also includes
a “second pass” that executes if a student has less than four
classes after exhausting all 48 choices (as referenced in the
4D node in Figure 1). However, since satisfactory explana-
tion has been provided by relevant parties, we have excluded
it from our interpretation of WebTree’s functioning.
The WebTree back-end algorithm first groups students
based on seniority, and then randomly ranks them within
each class, assigning them a lottery number. Moving
through the lottery numbers sequentially, it assigns a student
their top class choice if the assignment meets the following
requirements:
```
- The class has not exceeded its capacity.
- The student has not already been assigned this class.
- The student has not already been assigned four classes.
In the case that a student’s top choice violates one of these
conditions, WebTree looks to their next choice, and contin-
ues on until it either assigns a student a course or exhausts
their preferences.


(^)
**WARNING: Your preferences must be entered into WebTree before 5:00 p.m. on the last day.**^
**Anything entered will be processed, even if you have not clicked “Submit.”**
________ Course________ CRN
(If full, program goes to Tree 2)________ Time
________ Course________ CRN
(If full, program goes to 1B)________ Time
________ Course________ CRN
(If full, program goes to 1AB)________ Time
________ Course________ CRN
(Program goes to Tree 4)________ Time
________ Course________ CRN
(If full, program goes to 1BA)________ Time
________ Course________ CRN
(If full, program goes to 1BB)________ Time
________ Course________ CRN
(Program goes to Tree 4)________ Time
________ Course________ CRN
(If full, program goes to Tree 3)________ Time
________ Course________ CRN
(If full, program goes to 2B)________ Time
________ Course________ CRN
(If full, program goes to 2AB)________ Time
________ Course________ CRN
(Program goes to Tree 4)________ Time
________ Course________ CRN
(If full, program goes to 2BA)________ Time
________ Course________ CRN
(If full, program goes to 2BB)________ Time
________ Course________ CRN
(Program goes to Tree 4)________ Time
________ Course________ CRN
(If full, program goes to Tree 4)________ Time
________ Course________ CRN
(If full, program goes to 3B)________ Time
________ Course________ CRN
(If full, program goes to 3AB)________ Time
________ Course________ CRN
(Program goes to Tree 4)________ Time
________ Course________ CRN
(If full, program goes to 3BA)________ Time
________ Course________ CRN
(If full, program goes to 3BB)________ Time
________ Course________ CRN
(Program goes to Tree 4)________ Time
________ Course________ CRN
(If full, program goes to 4B)________ Time
________ Course________ CRN
(If full, program goes to 4C)________ Time
________ Course________ CRN
(If full, program goes to 4D)________ Time
________ Course________ CRN
(If full, and less than 4 classes, ________ Time
program goes to Tree 1)
**1
1 A 1 B
1 AA 1 AB 1 BA 1 BB
2
2 A 2 B
2 AA 2 AB 2 BA 2 BB
3
3 A 3 B
3 AA 3 AB 3 BA**^3 **BB**^
**4 A 4 B 4C 4D**
_Nrequires permissionote any course that.
WebTree will ask you if you have it.
“34Be alert to notes in the schedule: ,” for instance, means “juniors
Firstand seniors only-years and sophomores only.”; “12” means_^ _”_
Figure 1: WebTree Logic. Image courtesy of the Davidson
College Registrar (Davidson College).

## 3 Experiments

```
In our solution of the problem, we modeled the final assign-
ments in a student-class matrix with Boolean entries, which
lent itself to a mathematical description of the relevant con-
straints and quality of a solution.
For the variables of our CSP, we used a matrix of sizeS
byC, whereSis the total number of students who submitted
WebTree preferences, andCis the total number of classes
offered. Each entry in the matrixPi jtherefore corresponded
to a specific student-class combination. Each entry took a
Boolean value, where of 0 corresponded to that student not
taking the class, and 1 corresponded to the student taking the
class.
Our constraints were:
```
1. Every student must have between 2 and 4 classes:

### 2 ≤

### ∑C

```
j= 1
```
```
Pi j≤ 2 ∀rowsi
```
2. Every class must have a number of students in it between
    0 and its capacity:

### 0 ≤

### ∑S

```
i= 1
```
```
Pi j≤cp(Cj) ∀columnsj,
```
```
wherecp(Cj) is the capacity of the class corresponding to
columnj.
```
3. No student can be in a class more than once. (Implicitly
    enforced through the modeling of the problem)
    Solving the CSP requires an optimization function to de-
scribe quantitatively how well-suited a class assignment is
to a student’s choices. In our experiments, we varied this
function considerably to improve our results, but consider
as an example our original choice:

```
f 1 (Si,CRN)=gi(CRN)·h(CRN,gi(CRN))·y 1 (Si)·m 1 (Si,CRN)
```
```
where
```
- The functiongi(CRN) is 48 minus number of theith stu-
    dent’s choice in which the CRN is found. For example, if
    course CRN 25143 is first found in a student’s 36th ranked
    WebTree choice of four classes,gi(25143)= 48 − 36 =12.
- The functionh(CRN,gi(CRN)) is the location of a class
    CRN within theith student’s ranked choiceg(CRN).
    For example, if course CRN 25143 is found in a stu-
    dent’s 36th ranked WebTree choice of four classes, and
    it is the 3rd choice class in that choice of four classes,
    h(CRN,g(CRN))=3.
- The functiony 1 (Si) is the student’s class year (senior=4,
   ... etc).
- The functionm 1 (Si,CRN) returns 2 if the CRN references
    a class in student’sSi’s major, and 1 otherwise.
    By supplying Google’s “Glop” integer programming
solver with different versions offas our optimization func-
tion, we used them to find the optimal constrained assign-
ment of students to classes (Perron 2011).


We created several different metrics of success to mea-
sure our solution against the original WebTree algorithm and
modified our optimization functionfin order to improve our
results.
We first ran Glop using the example optimization func-
tionf 1 , and then modifiedf 1 after our solution did not out-
perform WebTree on our metrics. We remapped the output
to change the relative weights between choices. Becausegi
andhiinf 1 are both linear functions of the class-student
pairing’s position in a list, a change bykpositions in either
of these lists corresponds directly to akchange in the output
of that function.
This change doesn’t reflect all of the students’ actual pref-
erences however. Students generally care much more about
moving from their fifth WebTree choice of four classes to
their sixth choice than about moving from their twenty-
seventh choice to their twenty-eighth. To reflect this, we
mapped the output ofgandhusing two functions, a poly-
nomial and a sigmoid, which preserved the ranges on the
domains, but altered the rates of change of the optimiza-
tion value at different points, corresponding to students ac-
tual preferences. We also decreased the value of giving up-
perclass students their first choice, as well as giving ma-
jors their major choices. We wrotey 2 (Si) to be such that
y 2 (1) = 1. 2 ,y 2 (2) = 1. 5 ,y 2 (3) = 1. 8 ,andy 2 (4) = 2
(where 1 corresponds to a first year student... etc), and
wrotem 2 (Si,CRN) to return 1.3 if the class matched the stu-
dents major, rather than 2 asm 1 did. Both return 1 if the
class and major do not match.
We first used a polynomial generated from interpolation
through the points (48,48) (1,1) (20,10) to map the out-
put. The first two points specified that the range doesn’t
change, and the third point seems like a reasonable assump-
tion: the 20th choice should be worth approximately a fifth
as much as the first choice. Lagrange polynomial interpola-
tion through these points produced the mapping function

```
P(x)=
```
### 5

### 266

```
x^2 −
```
### 3

### 38

```
x+
```
### 20

### 10

Using this remap to modify the outputs ofgiandh, we
create
f 2 (Si,CRN)=P(gi(CRN))·P(h(CRN,gi(CRN)))
·y 2 (Si)·m 2 (Si,CRN)
We intended this mapping function to model the fast drop-
poffin valuation of choices. It attempts to account for the
fact that students care much more about changing from their
first choice to their third choice than from changing from
their twentieth choice to their twenty-first choice. However,
because of the drastically poor performance of the optimiza-
tion on measures of success described in our results, we re-
worked our mapping function.
We createdf 3 by changing our modeling function from an
interpolating polynomial to a sigmoid. This function models
the high valuation by students of their top choices, and the
sharp drop-offin valuation around their sixth choice. Using
a new sigmoid mapping function

```
S(x)=
```
### 48

```
1 +e−^0 .5(x−37)
```
```
Figure 2:f 1 (Blue),f 2 (Green), andf 3 (Red). Each function
attempts to model student valuation of relative parts of their
WebTree rankings. Image courtesy of Desmos Grapher.
```
```
we again modified the outputs ofgiandhto create
f 3 (Si,CRN)=S(gi(CRN))·S(h(CRN,gi(CRN)))
·y 2 (Si)·m 2 (Si,CRN)
```
```
We compare the results of these different optimization
functions in the next sections.
```
## 4 Results

```
As shown in Figure 3, each algorithm had varying results.
Ourf 3 gave a higher percentage of students their first and
second choices for most semesters, while WebTree (f 0 ) per-
formed better for students’ third and fourth choices. We do
not know whyf 2 performed so miserably, but we can con-
clude that a polynomial mapping function does not correctly
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
```
## 5 Conclusions

```
In this paper, we sought to improve Davidson’s WebTree al-
gorithm by modeling it as constraint satisfaction problem.
```

```
Category
```
```
Fall 2013 Spring 2014 Fall 2014 Spring 2015
f 0 f 1 f 2 f 3 f 0 f 1 f 2 f 3 f 0 f 1 f 2 f 3 f 0 f 1 f 2 f 3
1st Choices 88 82 22 90 90 81 25 92 91 83 21 93 91 84 25 92
2nd Choices 75 76 22 81 67 69 23 71 74 75 23 79 73 73 22 77
3rd Choices 58 59 22 54 50 54 23 49 56 53 21 47 58 57 21 51
4th Choices 58 36 23 29 55 38 22 30 58 34 23 25 62 38 22 30
```
```
Major 1st Choice 88 94 24 94 91 94 26 96 94 97 21 97 90 94 27 95
Major 2nd Choice 77 90 24 85 69 84 24 76 76 91 25 84 75 85 24 81
```
```
1st Choices Seniors 94 85 25 91 96 89 31 94 95 89 26 95 98 95 31 98
1st Choices Juniors 87 86 25 92 92 85 24 94 97 89 22 97 94 88 25 95
1st Choices Sophomores 81 72 20 83 85 77 22 86 88 75 20 89 87 77 22 87
1st Choices Freshmen 74 70 15 77 83 70 21 87 87 81 16 90 86 76 20 89
```
Figure 3: Comparison of our algorithms (f 1 - linear,f 2 - polynomial,f 3 - sigmoid) to the traditional WebTree,f 0. An entry in
“x” Choices for functionfiindicates the percentage of students who received theirxth choice, where their first choice is their 1
node class on WebTree, their second is their 1A class, third is their 1AA class, and fourth is their 4A class. Major First Choice
and Second Choice refer to the percentage of students whose first and second choice, respectively, were classes in their major,
and who got that class. First choice percentages are also broken down by year in the bottom four columns.

Our results offer an argument to replace WebTree with a lin-
ear programming solver using thef 3 optimization function,
as our algorithm produces the highest percentages most of-
ten in Figure 3. Additionally, our algorithm also consid-
ers an additional factor in this problem: students’ majors.
Due to the common dissatisfaction of students not receiv-
ing classes in their majors, we provide the functionality to
remedy that inconsistency.
In order for our algorithm to maximize its payoff, it would
require replacing the data input portion of the current Web-
Tree program. Our approach can offer students a set of
classes that they didn’t request together, so we suggest mod-
ifying the front-end data input part of WebTree. We would
solicit a one “must-have” course, two sets of three courses
of which the student would highly value getting one of, and
a remaining set of six courses the student would like one
of, but prioritizes least. The current WebTree data intake
focuses heavily on the logical dependency of often redun-
dant class dependencies, forcing the student to describe their
preferences in repetitive detail. Because students generally
want one to two courses for their major, one or two for a mi-
nor or distribution requirement, and one for general interest,
students’ choices generally don’t have complex dependen-
cies, making much of the logical structure of WebTree use-
less and students’ entries in it redundant. For example, while
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

```
by simply changing a weight in our optimization function,
while the baseline WebTree has no similar easily imple-
mentable fix. Similarly, if large numbers of students do
not receive the classes in their major they need to gradu-
ate, our WebTree algorithm could simply be rerun with a
larger output on ourmfunction in the case of a match, and
the new student-class assignment solution produced by re-
running Glop would accommodate the desired change.
```
## 6 Contributions

```
Baldini and Robertson both contributed to each function of
the code. Robertson focused more on creating our model,
while Baldini spent more time working on the data intake
and testing cases. Both authors co-authored each section of
the paper and proof-read the entire document.
```
## 7 Acknowledgements

```
Thank you Dr. Ramanujan for guidance throughout the pro-
cess of implementing our algorithm.
```
## References

```
Davidson College. WebTree Worksheet. https:
//www.davidson.edu/Documents/Administrative%
20Department/Registrar/WebTreeWorksheet.pdf.
Retrieved on Mar. 25, 2019.
Perron, L. 2011. Operations Research and Constraint Pro-
gramming at Google. In Lee, J., ed.,Principles and Practice
of Constraint Programming – CP 2011, 2–2. Berlin, Heidel-
berg: Springer Berlin Heidelberg.
```

