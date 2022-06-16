from functools import total_ordering

# consts
SIZE = 10

def is_horiz(va, vb):
    return va[0] == vb[0]

def is_vert(va, vb):
    return va[1] == vb[1]

def count_row(coords, row):
    cnt = 0
    for coord in coords[row]:
        if coord:
            cnt += 1
    return cnt

def count_col(coords, col):
    cnt = 0
    for coord in coords:
        if coord[col]:
            cnt += 1
    return cnt

@total_ordering
class Edge:
    def __init__(self, *vertices):
        self.vertices = vertices
    
    @property
    def is_horiz(self):
        return is_horiz(*self.vertices)
    
    @property
    def is_vert(self):
        return is_vert(*self.vertices)
    
    @property
    def length(self):
        va = self.vertices[0]
        vb = self.vertices[1]

        res = (va[0] - vb[0]) ** 2 + (va[1] - vb[1]) ** 2
        res = res ** 0.5

        return res
    
    def __eq__(self, other):
        if not isinstance(other, Edge):
            return NotImplemented
        return self.vertices == other.vertices
    
    def __lt__(self, other):
        if not isinstance(other, Edge):
            return NotImplemented
        return self.length < other.length


# #### MAIN ####
# Receive input
coords = [[int(ch) for ch in input()] for i in range(SIZE)]

# Find longest edge
for r, row in enumerate(coords):
    pass