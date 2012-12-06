# vim: fileencoding=utf8 tw=120 expandtab ts=4 sw=4 :

# Floory
# A simple floor planner intended for CSS sprites generators. Disclaimer: this algorithm is very simple and thus will
# probably never produce an optimal result. Moreover, it is quite complex (somewhat O(n³) I guess), so don't use it if
# you need to handle a lot of items.
#
# Copyright (c) 2012 Rémy Sanchez <remy.sanchez@hyperthese.net>
# Under the terms of the WTFPL

class Item(object):
    """
    Represents an item, with its size and position.
    """

    def __init__(self, name, w, h):
        self.name = name
        self.w = w
        self.h = h
        self.x = None
        self.y = None

    def __str__(self):
        return str(self.__repr__())

    def __repr__(self):
        return self.name

class Grid(object):
    """
    Holds the grid with the placed items, and manipulates it.
    """

    def __init__(self):
        self.w = 1
        self.h = 1
        self.grid = [[None]]

        self.full_col = [False]
        self.full_row = [False]

    def fits_in(self, item, x, y):
        # Warning: there is no boundary check here, so be careful when calling the function

        for i in range(x, x + item.w):
            for j in range(y, y + item.h):
                if self.grid[i][j] is not None:
                    return False

        return True

    def find_fit(self, item):
        if item.w > self.w or item.h > self.h:
            return None

        for j in range(0, self.h - item.h + 1):
            for i in range(0, self.w - item.w + 1):
                if self.fits_in(item, i, j):
                    return (i, j)

        return None

    def book(self, item):
        for i in range(0, item.w):
            for j in range(0, item.h):
                self.grid[item.x + i][item.y + j] = item

    def enlarge(self, w, h):
        if w > self.w:
            self.grid += [[None for y in range(0, self.h)] for x in range(0, w - self.w)]
            self.w = w

        if h > self.h:
            for x in range(0, self.w):
                self.grid[x] += [None for y in range(0, h - self.h)]
            self.h = h

    def crop(self):
        max_x = 0
        max_y = 0

        for x in range(0, self.w):
            for y in range(0, self.h):
                if self.grid[x][y] is not None:
                    if x > max_x:
                        max_x = x
                    if y > max_y:
                        max_y = y

        max_x += 1
        max_y += 1

        newgrid = [[self.grid[x][y] for y in range(0, max_y)] for x in range(0, max_x)]
        self.grid = newgrid
        self.w = max_x
        self.h = max_y

def plan(items, width=10):
    """
    Will calculate an optimized planning for the items and set the appropriate coordinates in the objects.
    """

    def cmp_item(a, b):
        if a.w == b.w:
            return a.h - b.h
        return a.w - b.w

    items = sorted(items, cmp=cmp_item, reverse=True)

    grid = Grid()
    grid.enlarge(width, 0)

    for item in items:
        fit = grid.find_fit(item)

        if fit is None:
            grid.enlarge(item.w, grid.h + item.h)
            fit = grid.find_fit(item)

        if fit is None:
            raise Exception('Something went terribly wrong in the head of the guy that created this code.')

        item.x, item.y = fit
        grid.book(item)

    grid.crop()

    return grid

def _disp_grid(grid):
    import sys

    for y in range(0, grid.h):
        for x in range(0, grid.w):
            sys.stdout.write("%5s" % grid.grid[x][y])
        sys.stdout.write("\n")

if __name__ == '__main__':
    items = [
        Item("a", 2, 8),
        Item("t", 12, 21),
        Item("z", 4, 4),
        Item("B", 6, 2),
        Item("T", 1, 7),
    ] + [Item(str(x), 1, 1) for x in range(0, 100)]

    out = plan(items)
    _disp_grid(out)
