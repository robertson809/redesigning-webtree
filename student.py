
class Student:
    """Type for representing a student record.

    Attributes:
        id - an integer representing the student's ID number.
        class_year - a string representing the student's class year.
        _next_course - a tuple representing the WebTree node that
                       should be considered next for scheduling.
        requests - a list of 3-tuples representing the student's
                   WebTree requests.
    """
    def __init__(self, id, class_year):
        """Constructs a new student record with specified attributes.

        Parameters:
            id - this student's ID number (an integer).
            class - this student's class (a string).
        """
        self.id = id
        self.class_year = class_year
        self._next_course = (1, 1)
        self.requests = {}

    def __str__(self):
        """Returns a printable representation of this student record.

        Returns:
            A string in the format:
            '{id, class_year, (request_1), (request_2), ...}'.
        """
        str_rep = "{" + str(self.id) + ", " + self.class_year
        str_rep += ", " + str(self.requests)
        str_rep += "}"
        return str_rep

    def add_request(self, crn, tree, branch):
        """Adds the supplied WebTree request to this student's record.

        Parameters:
            crn - the CRN of the requested course (integer).
            tree - the tree number where CRN was placed (integer).
            branch - the node in the tree where CRN was placed (integer).

        Returns:
            None.
        """
        self.requests[(tree, branch)] = crn

    def get_next_course(self):
        """Returns the next CRN according to this student's preference.

        Returns:
            An integer representing the next CRN in this student's completed
            preference form.
        """
        return self.requests[self._next_course]

    def can_advance_preference(self):
        """Returns True iff this student's WebTree has not been exhausted.

        Returns:
            True iff we've not already advanced beyond tree #4, branch #4 in
            this student's preferences (which resets the counters to (0, 0)).
        """
        return (self._next_course != (0, 0))

    def advance_preference(self, got_last_class):
        """Progresses along this student's WebTree preferences.

        Parameters:
            got_last_class - a Boolean indicating whether the student received
                             the last requested class.

        Returns:
            None
        """
        tree = self._next_course[0]
        branch = self._next_course[1]

        if (tree == 0) or (branch == 0):
            raise Exception("This should never happen!")
        
        if got_last_class: # stay along same path if possible
            if (tree <= 3) and (branch <= 3):
                self._next_course = (tree, branch*2)
            elif (tree <= 3): # time to move to fill-in tree (#4)
                self._next_course = (4, 1)
            elif (branch <= 3): # already in tree #4
                self._next_course = (4, branch + 1)
            else: # already at 4-4, nowhere left to go, tough luck kid.
                self._next_course = (0, 0)
        else: # need to make a parallel move, or jump to a different tree
            if (tree <= 3) and (branch == 1):
                self._next_course = (tree + 1, 1)
            elif (tree <= 3) and (branch % 2 == 0): # rightwards move if possible
                self._next_course = (tree, branch + 1)
            elif (tree <= 3) and (branch == 3): # special case, goes to next row
                self._next_course = (tree, branch + 1)
            elif (tree <= 3): # 5 or 7, move to fill-in tree (#4)
                self._next_course = (4, 1)
            elif (branch <= 3): # already in tree #4
                self._next_course = (4, branch + 1)
            else: # tough luck kid
                self._next_course = (0, 0)

    def reset_preferences(self):
        """Resets this student's WebTree iterator to tree #1, branch #1.

        Returns:
            None.
        """
        self._next_course = (1, 1)

    def traverse_tree(self):
        """Performs a level-order traversal of every tree in the student's
        preferences.

        Returns:
            None.
        """
        tree = self._next_course[0]
        branch = self._next_course[1]
        
        if (tree == 0) or (branch == 0):
            raise Exception("This should never happen!")

        if (tree == 4) and (branch == 4): # we're done
            self._next_course = (0, 0)
        elif (tree == 4): # rightwards on tree #4
            self._next_course = (4, branch + 1)
        elif (branch == 7): # jump to top of next tree
            self._next_course = (tree + 1, 1)
        else: # next node in current tree in level order
            self._next_course = (tree, branch + 1)
                
                
            
                
            
    
