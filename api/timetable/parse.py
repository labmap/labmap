from bs4 import BeautifulSoup

from cell import Cell
from event import Event


def flatten(l):
    return sum(l, [])


def unmerge_cells_horizontally(cells):
    cells = [[cell] + [cell.empty_copy()] * (cell.colspan - 1) for cell in cells]
    cells = flatten(cells)
    return cells


def unmerge_cells_vertically(cells, rowspans):
    cells = cells[:]
    for i, rowspan in enumerate(rowspans):
        if rowspan > 0:
            cells.insert(i, Cell(None))
    return cells


def extract_headers(table):
    headers = [Cell(th) for th in table.contents[0]]
    width = sum([header.colspan for header in headers])
    rows = table.contents[1:]
    return headers, rows, width


def normalize_table(table):
    headers, rows, width = extract_headers(table)
    normalized_table = []
    rowspans = [0] * width
    for row in rows:
        cells = [Cell(td) for td in row.children]
        cells = unmerge_cells_horizontally(cells)
        cells = unmerge_cells_vertically(cells, rowspans)
        assert len(cells) == len(rowspans)
        rowspans = [rowspan + cell.rowspan - 1 for rowspan, cell in zip(rowspans, cells)]
        normalized_table.append(cells)
    return headers, normalized_table


def extract_start_time(table):
    start_time_string = table[0][0].td.span.text
    hours, minutes = [int(x) for x in start_time_string.split(":")]
    start_time = hours * 60 + minutes
    return start_time


def parse_table(headers, table):
    result = {}
    start_time = extract_start_time(table)
    for i, row in enumerate(table):
        time = start_time + i * 5
        range_start = 0
        for header in headers:
            if header.td.contents:
                header_name = header.td.contents[0]
                events = [
                    Event(cell, time)
                    for cell in row[range_start: range_start + header.colspan]
                    if cell.td and cell.td.contents
                ]
                try:
                    result[header_name] += events
                except KeyError:
                    result[header_name] = events
            range_start += header.colspan
    return result


def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.findAll('table')[-1]
    headers, table = normalize_table(table)
    return parse_table(headers, table)
