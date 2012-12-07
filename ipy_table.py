#!/usr/bin/python
from IPython.core.display import HTML
# from prettytable import *
from numpy import float64
import csv

_VERSION = 1.5
_TABLE = None

def read_csv_file(filename, skip_first_row=False):
    '''Reads a CSV file and returns the data as a two dimensional list'''
    data = []
    with open(filename, 'rU') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            data.append(row)
    if skip_first_row:
        if len(data):
            # Delete the first row
            del data[0]
    return data


def _formatter(item, float_format):
    """
    Applies _float_format if the item is a float or float64, otherwise
    returns item unmodified.
    This function is written such that it won't error if numpy isn't imported.
    """

    if str(type(item)) in ["<type 'float'>", "<type 'numpy.float64'>"]:
        return float_format % item
    return item

def _convert_to_list(data):
    """
    Accepts a list or a numpy.ndarray and returns a list.
    This function is written such that it won't error if numpy isn't imported.
    """
    if str(type(data)) == "<type 'numpy.ndarray'>":
        return data.tolist()
    return data

def valid_key(dict, key):
    """Test that a disctionary key exists and that it's value is not blank"""
    if key in dict:
        if dict[key]:
            return True
    return False

def tabulate(data_list, columns, float_format="%0.4f"):
    '''
    Renders a list (not array) of items into an HTML table
    with a specified number of columns.
    '''
    total_items = len(data_list)
    rows = total_items / columns
    if total_items % columns:
        rows += 1
    num_blank_cells = rows * columns - total_items
    if num_blank_cells:
        rows += 1

    # Create an array and pad the ending cells with null strings
    array = copy.copy(_convert_to_list(data_list))
    pad_cells = ['' for i in range(num_blank_cells)]
    array = array + pad_cells
    array = [array[x:x + columns] for x in xrange(0, len(array), columns)]

    # Render the array
    table = Table(array)
    return table.render()

def table(array, float_format="%0.4f", interactive=True):
    global _TABLE
    _TABLE = Table(array, float_format, interactive)
    return _TABLE._render_update()

def set_cell_style(row, column, bold=None, italic=None, color=None, thick_border=None, no_border=None, row_span=None, column_span=None, align=None, width=None):
    global _TABLE
    return _TABLE.set_cell_style(row, column, bold=bold, italic=italic, color=color, thick_border=thick_border, no_border=no_border, row_span=row_span, column_span=column_span, align=align, width=width)

def set_column_style(column, bold=None, italic=None, color=None, thick_border=None, no_border=None, row_span=None, column_span=None, align=None, width=None):
    global _TABLE
    return _TABLE.set_column_style(column, bold=bold, italic=italic, color=color, thick_border=thick_border, no_border=no_border, row_span=row_span, column_span=column_span, align=align, width=width)

def set_row_style(row, bold=None, italic=None, color=None, thick_border=None, no_border=None, row_span=None, column_span=None, align=None, width=None):
    global _TABLE
    return _TABLE.set_row_style(row, bold=bold, italic=italic, color=color, thick_border=thick_border, no_border=no_border, row_span=row_span, column_span=column_span, align=align, width=width)

def apply_style(style_name):
    global _TABLE
    return _TABLE.apply_style(style_name)

def render():
    global _TABLE
    return _TABLE.render()

class Table(object):

    #---------------------------------
    # External methods
    #---------------------------------

    def __init__(self, array, float_format="%0.4f", interactive=False):
        self.array = array
        self._num_rows = len(array)
        self._num_columns = len(array[0])
        self._float_format = float_format
        self._interactive = interactive

        self._global_style = dict()
        self._row_styles = [dict() for i in range(self._num_rows)]
        self._column_styles = [dict() for i in range(self._num_columns)]
        self._cell_styles = [[dict() for i in range(self._num_columns)] for i in range(self._num_rows)]
        self._debug = False

        self.styles = ['basic']

    def apply_style(self, style_name):
        self.set_row_style(0, bold=True, color='LightGray')
        for row, row_data in enumerate(self.array):
            if row > 0:
                if row % 2:
                    self.set_row_style(row, color='Ivory')
                else:
                    self.set_row_style(row, color='AliceBlue')
        self.set_column_style(0, bold=True, color='LightGray')
        self.set_cell_style(0, 0, color='White', no_border='left,top')
        return self._render_update()

    def set_cell_style(self, row, column, bold=None, italic=None, color=None, thick_border=None, no_border=None, row_span=None, column_span=None, align=None, width=None):
        self._set_cell_style(row, column, bold=bold, italic=italic, color=color, thick_border=thick_border, no_border=no_border, row_span=row_span, column_span=column_span, align=align, width=width)
        return self._render_update()

    def set_row_style(self, row, bold=None, italic=None, color=None, thick_border=None, no_border=None, row_span=None, column_span=None, align=None, width=None):
        self._set_row_style(row, bold=bold, italic=italic, color=color, thick_border=thick_border, no_border=no_border, row_span=row_span, column_span=column_span, align=align, width=width)
        return self._render_update()

    def set_column_style(self, column, bold=None, italic=None, color=None, thick_border=None, no_border=None, row_span=None, column_span=None, align=None, width=None):
        self._set_column_style(column, bold=bold, italic=italic, color=color, thick_border=thick_border, no_border=no_border, row_span=row_span, column_span=column_span, align=align, width=width)
        return self._render_update()

    def render(self):
        # import pdb; pdb.set_trace()
        #---------------------------------------
        # Generate TABLE tag (<tr>)
        #---------------------------------------
        # html = '<table border="1" cellpadding="3" cellspacing="0" style="border:1px solid black;width:10%;border-collapse:collapse;">'
        # html = '<table border="1" cellpadding="3" cellspacing="0" style="border:1px none white;width:10%;border-collapse:collapse;">'
        html = '<table>'
        for row, row_data in enumerate(self.array):

            #---------------------------------------
            # Generate ROW tag (<tr>)
            #---------------------------------------
            html += '<tr>'
            for (column, item) in enumerate(row_data):
                if not valid_key(self._cell_styles[row][column], 'suppress'):
                    #---------------------------------------
                    # Generate CELL tag (<td>)
                    #---------------------------------------
                    # Apply floating point formatter to the cell contents (if it is a float)
                    item_html = self._formatter(item, self._float_format)

                    # Add bold and italic tags if set
                    if valid_key(self._cell_styles[row][column], 'bold'):
                        item_html = '<b>' + item_html + '</b>'
                    if valid_key(self._cell_styles[row][column], 'italic'):
                        item_html = '<i>' + item_html + '</i>'

                    # Get html style string
                    style_html = self._get_style_html(self._cell_styles[row][column])

                    # Append cell
                    html += '<td ' + style_html + '>' + item_html + '</td>'
            html += '</tr>'
        if self._debug:
            print html
        return HTML(html)

    #---------------------------------
    # Internal methods
    #---------------------------------

    def _render_update(self):
        if(self._interactive):
            return self.render()
        return None

    def _build_style_dict(self, bold=None, italic=None, color=None, thick_border=None, no_border=None, row_span=None, column_span=None, align=None, width=None):
        style_dict = dict()
        if bold is not None:
            style_dict['bold'] = bold
        if italic is not None:
            style_dict['italic'] = italic
        if color is not None:
            style_dict['color'] = color
        if thick_border is not None:
            if thick_border == 'all':
                style_dict['thick_border'] = 'left,right,top,bottom'
            else:
                style_dict['thick_border'] = thick_border
        if no_border is not None:
            if no_border == 'all':
                style_dict['no_border'] = 'left,right,top,bottom'
            else:
                style_dict['no_border'] = no_border

        if row_span is not None:
            style_dict['row_span'] = row_span
        if column_span is not None:
            style_dict['column_span'] = column_span
        if align is not None:
            style_dict['align'] = align
        if width is not None:
            style_dict['width'] = width

        return style_dict

    def _merge_cell_style(self, row, column, cell_style):
        """Merge new cell style dict into the old, superseding any existing items"""
        self._cell_styles[row][column] = dict(self._cell_styles[row][column].items() + cell_style.items())

    def _set_cell_style(self, row, column, bold=None, italic=None, color=None, thick_border=None, no_border=None, row_span=None, column_span=None, align=None, width=None):
        cell_style = self._build_style_dict(bold=bold, italic=italic, color=color, thick_border=thick_border, no_border=no_border, row_span=row_span, column_span=column_span, align=align, width=width)
        self._merge_cell_style(row, column, cell_style)
        if row_span:
            for row in range(row + 1, row + row_span):
                self._cell_styles[row][column]['suppress'] = True
        if column_span:
            for column in range(column + 1, column + column_span):
                self._cell_styles[row][column]['suppress'] = True

        # If a thick right hand border was specified, then also apply it to the left of the adjacent cell (if one exists)
        if thick_border and any(x in thick_border for x in ('right', 'all')) and column + 1 < self._num_columns:
            self._merge_cell_style(row, column + 1, self._build_style_dict(thick_border='left'))

        # If a clear left hand border was specified, then also apply it to the right of the adjacent cell (if one exists)
        if no_border and any(x in no_border for x in ('left', 'all')) and column > 0:
            self._merge_cell_style(row, column - 1, self._build_style_dict(no_border='right'))

        # If a thick bottom border was specified, then also apply it to the top of the adjacent cell (if one exists)
        if thick_border and any(x in thick_border for x in ('bottom', 'all')) and row + 1 < self._num_rows:
            self._merge_cell_style(row + 1, column, self._build_style_dict(thick_border='top'))

        # If a clear top border was specified, then also apply it to the bottom of the adjacent cell (if one exists)
        if no_border and any(x in no_border for x in ('top', 'all')) and row > 0:
            self._merge_cell_style(row - 1, column, self._build_style_dict(no_border='bottom'))

    def _set_row_style(self, row, bold=None, italic=None, color=None, thick_border=None, no_border=None, row_span=None, column_span=None, align=None, width=None):
        for column in range(self._num_columns):
            self._set_cell_style(row, column, bold=bold, italic=italic, color=color, thick_border=thick_border, no_border=no_border, row_span=row_span, column_span=column_span, align=align, width=width)

    def _set_column_style(self, column, bold=None, italic=None, color=None, thick_border=None, no_border=None, row_span=None, column_span=None, align=None, width=None):
        for row in range(self._num_rows):
            self._set_cell_style(row, column, bold=bold, italic=italic, color=color, thick_border=thick_border, no_border=no_border, row_span=row_span, column_span=column_span, align=align, width=width)

    def _get_style_html(self, style_dict):
        style_html = ''
        if valid_key(style_dict, 'color'):
            style_html += 'background-color:' + style_dict['color'] + ';'

        if valid_key(style_dict, 'thick_border'):
            edges = style_dict['thick_border'].replace(' ', '').split(',')
            if 'left' in edges:
                style_html += 'border-left: 3px solid black;'
            if 'right' in edges:
                style_html += 'border-right: 3px solid black;'
            if 'top' in edges:
                style_html += 'border-top: 3px solid black;'
            if 'bottom' in edges:
                style_html += 'border-bottom: 2px solid black;'

        if valid_key(style_dict, 'no_border'):
            edges = style_dict['no_border'].replace(' ', '').split(',')
            if 'left' in edges:
                style_html += 'border-left: 1px solid transparent;'
            if 'right' in edges:
                style_html += 'border-right: 1px solid transparent;'
            if 'top' in edges:
                style_html += 'border-top: 1px solid transparent;'
            if 'bottom' in edges:
                style_html += 'border-bottom: 1px solid transparent;'

        if valid_key(style_dict, 'align'):
            style_html += 'text-align:' + str(style_dict['align']) + ';'

        if valid_key(style_dict, 'width'):
            style_html += 'width:' + str(style_dict['width']) + 'px;'

        if style_html:
            style_html = ' style="' + style_html + '"'

        if valid_key(style_dict, 'row_span'):
            style_html = 'rowspan="' + str(style_dict['row_span']) + '";' + style_html

        if valid_key(style_dict, 'column_span'):
            style_html = 'colspan="' + str(style_dict['column_span']) + '";' + style_html

        return style_html


    def _formatter(self, item, float_format):
        if type(item) is float or type(item) is float64:
            return float_format % item
        return item


