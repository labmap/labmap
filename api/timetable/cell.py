class Cell:
    def __init__(self, td):
        if td is None:
            self.td = None
            self.rowspan = 0
            self.colspan = 1
        else:
            self.td = td
            if td.has_attr('rowspan') and td['rowspan']:
                self.rowspan = int(td['rowspan'])
            else:
                self.rowspan = 1
            if td.has_attr('colspan') and td['colspan']:
                self.colspan = int(td['colspan'])
            else:
                self.colspan = 1

    def empty_copy(self):
        copy = Cell(self.td)
        copy.td = None
        return copy
