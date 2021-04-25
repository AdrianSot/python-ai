import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for var in self.crossword.variables:
            current_set = self.domains[var].copy()
            for val in current_set:
                if(len(val) != var.length): 
                    self.domains[var].remove(val)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        didRevision = False
        if self.crossword.overlaps[x,y] is None:
            return False
        i, j = self.crossword.overlaps[x,y]
        xdomain = self.domains[x].copy()
        for xval in xdomain:
            is_consistent_val = False 
            for yval in self.domains[y]:
                if xval[i] == yval[j]:
                    is_consistent_val = True
                    break
            if not is_consistent_val:
                self.domains[x].remove(xval)
                didRevision = True

        return didRevision

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        inQueue = {}
        if arcs is None:
            arcs = [] 
            for var in self.crossword.overlaps:
                if var:
                    x, y = var
                    inQueue[x,y] = True
                    arcs.append((x,y))
        while len(arcs) > 0:
            x, y = arcs.pop()
            inQueue[x,y] = False
            if self.revise(x,y):
                if len(self.domains[x]) == 0:
                    return False
                for var in self.crossword.neighbors(x):
                    if not inQueue[x,var]:
                        arcs.append((x,var))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for var in self.crossword.variables:
            if var not in assignment:
                return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        seen_values = set()
        for x in assignment:
            if assignment[x] in seen_values:
                return False
            if x.length != len(assignment[x]):
                return False
            seen_values.add(assignment[x])
            for y in self.crossword.neighbors(x):
                if y not in assignment:
                    continue
                indexes = self.crossword.overlaps[x,y]
                if indexes:
                    i, j = indexes
                if assignment[x][i] != assignment[y][j]:
                    return False
        return True
                

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        values = []
        for value in self.domains[var]:
            ruled_out = 0
            for y in self.crossword.neighbors(var):
                if y in assignment:
                    continue
                for val in self.domains[y]:
                    if val == value:
                        ruled_out += 1
                    else:
                        indexes = self.crossword.overlap(var,y)
                        if indexes:
                            i, j = indexes
                        if value[i] != val[j]:
                            ruled_out += 1
            values.append((value,ruled_out))
        return values.sort(key=lambda x: x[1])

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        min_var = None
        min_val = None
        if len(assignment) == 0:
            return list(self.crossword.variables)[0]
        for var in self.crossword.variables:
            if var not in assignment:
                min_var = var
                min_val = len(self.domains[min_var])
                break
        for var in self.crossword.variables:
            if var not in assignment:
                if len(self.domains[var]) < min_val:
                    min_var = var
                    min_val = len(self.domains[min_var])
                elif len(self.domains[var]) == min_val:
                    if(self.crossword.neighbors(var) > self.crossword.neighbors(min_var)):
                        min_var = var
                        min_val = len(self.domains[min_var])
        return min_var

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        for val in self.domains[var]:
            assignment[var] = val
            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if result is not None:
                    return result
                assignment.pop(var)
            else:
                assignment.pop(var)
        return None

def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
