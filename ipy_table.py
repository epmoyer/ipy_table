"""Table formatting package for IP[y] Notebooks

ipy_table is a support module for creating formatted tables in an
IPython Notebook. ipy_table is an independent project and is not
an official component of the IPython package.

Documentation is provided by the documentation notebooks supplied with
this package:
    ipy_table-Introduction.ipynb
    ipy_table-Reference.ipynb

All cell, row, column, and global style formatting functions accept
optional style_args. style_args support the following arguments:
    color=<colorstring>
        <colorstring> can be any any standard web/X11 color name.
        For a list see http://en.wikipedia.org/wiki/Web_colors
    bold=<True/False>
    italic=<True/False>
    thick_border=<edgelist>
        <edgelist> is a comma delimited string containing any of the
        keywords 'left', 'right', 'bottom' and 'top' to specify
        individual edges, or 'all' to specify all edges.
    no_border=<edgelist>
        <edgelist> is a comma delimited string containing any of the
        keywords 'left', 'right', 'bottom' and 'top' to specify
        individual edges, or 'all' to specify all edges.
    row_span=<row count>
    column_span=<column_count>
    width=<width in pixels>
    align=<alignmentstring>
        <alignmentstring> can be 'left', 'right', or 'center'
    wrap=<True/False>
    float_format=<formatstring>
        <formatstring> is a standard Python '%' format string
        (e.g. '%0.6f' or '$%0.2f')

Design goals:
    * Easy to use in an interactive IPython Notebook session.
      (minimal syntax, interactive modification of styles)
    * Maintainability
      (minimize the overhead of adding new style features)
    * Robustness over HTML verbosity
      (HTML styles are only manipulated at the cell level, which
      results in robust style flexibility and general implementation
      simplicity at the expense of occasional HTML verbosity.
      HTML row styles and table styles are never manipulated).

---------------------------------------------------------------------------
Copyright (c) 2012-2013, ipy_table Development Team.

Distributed under the terms of the Modified BSD License.

The full license is in the file COPYING.txt, distributed with this software.

This project is maintained at http://github.com/epmoyer/ipy_table
"""

import copy
from collections import Counter
import numpy as np

__version__ = 1.12

# Private table object used for interactive mode
_TABLE = None
_INTERACTIVE = True

#-----------------------------
# Classes
#-----------------------------


class IpyTable(object):

    _valid_borders = {'left', 'right', 'top', 'bottom', 'all'}

    # could / should be global
    # Map style alignment to number
    ALIGN_NUM = { 'left': 0,
                 'right': 1,
                'centre': 2 }
    
    # Map number alignments to latex styles
    ALIGN_TEX = { 0: 'l',
                  1: 'r',
                  2: 'c' }
    
    # Map style borders to numbers
    BORDER_NUM = { 'single_border': 0,
		       'no_border': 1,
                    'thick_border': 2,
                    'double_thick': 3 }

    # Map number borders to latex vertical border styles
    VBORDER_TEX = { 0: '|',
                   1: ' ',
                   2: '!{\\vrule width 1pt}',
                   3: '!{\\vrule width 2pt}' } # Double thick line for first and last columns


    #---------------------------------
    # External methods
    #---------------------------------

    def __init__(self, array):
        self.array = array

        self._num_rows = len(array)
        self._num_columns = len(array[0])

        # Check that array is well formed
        for row in array:
            if len(row) != self._num_columns:
                raise ValueError("Array rows must all be of equal length.")

        self._cell_styles = [[{'float_format': '%0.4f'}
                              for dummy in range(self._num_columns)]
                             for dummy2 in range(self._num_rows)]

    def _repr_html_(self):
        """IPython display protocol: HTML representation.

        The IPython display protocol calls this method to get the HTML
        representation of this object.
        """
        #---------------------------------------
        # Generate TABLE tag (<tr>)
        #---------------------------------------
        html = '<table border="1" cellpadding="3" cellspacing="0" ' \
            + ' style="border:1px solid black;border-collapse:collapse;">'

        for row, row_data in enumerate(self.array):

            #---------------------------------------
            # Generate ROW tag (<tr>)
            #---------------------------------------
            html += '<tr>'
            for (column, item) in enumerate(row_data):
                if not _key_is_valid(
                        self._cell_styles[row][column], 'suppress'):

                    #---------------------------------------
                    # Generate CELL tag (<td>)
                    #---------------------------------------
                    # Apply floating point formatter to the cell contents
                    # (if it is a float)
                    item_html = self._formatter(
                        item, self._cell_styles[row][column])

                    # Add bold and italic tags if set
                    if _key_is_valid(self._cell_styles[row][column], 'bold'):
                        item_html = '<b>' + item_html + '</b>'
                    if _key_is_valid(self._cell_styles[row][column], 'italic'):
                        item_html = '<i>' + item_html + '</i>'

                    # Get html style string
                    style_html = self._get_style_html(
                        self._cell_styles[row][column])

                    # Append cell
                    html += '<td' + style_html + '>' + item_html + '</td>'
            html += '</tr>'
        html += '</table>'
        return html

    def _repr_latex_(self):
        """IPython display protocol: LaTex representation.

        The IPython display protocol calls this method to get the LaTex
        representation of this object.
        """

        latex = ''
        if not hasattr(self, '_has_latex_macros'):
            print 'WARNING: include \\usepackage{array} on latex template\n'
            latex += '% Some macros could be added the first time table is created\n'
            latex += '\\newlength{\\Oldarrayrulewidth}\n'
            latex += '\\newcommand{\\thickline}[2]{%\n'
            latex += '  \\noalign{\\global\\setlength{\\Oldarrayrulewidth}{\\arrayrulewidth}}%\n'
            latex += '  \\noalign{\\global\\setlength{\\arrayrulewidth}{#1}}\\cline{#2}%\n'
            latex += '  \\noalign{\\global\\setlength{\\arrayrulewidth}{\Oldarrayrulewidth}}}\n'
            
            latex += '\n'
            self._has_latex_macros = True


        #---------------------------------------
        # Begin tabular
        #---------------------------------------
        latex += '\\begin{tabular}'

        cell_align = self._build_align_matrix()
        cell_vBorder = self._build_vborder_matrix()
        pref_align = [ _get_most_common(cell_align[:,i]) for i in range(self._num_columns) ]
        pref_border = [ _get_most_common(cell_vBorder[:,i]) for i in range(self._num_columns+1) ]
        
        cell_hBorder = self._build_hborder_matrix()


        latex += '{'
        for i in range(self._num_columns):
            latex += self.VBORDER_TEX[pref_border[i]] + self.ALIGN_TEX[pref_align[i]]
        latex += self.VBORDER_TEX[pref_border[-1]]
        latex += '}\n' + self._build_line_separator(cell_hBorder[0,:])

        for row, row_data in enumerate(self.array):
            #---------------------------------------
            # Generate rows
            #---------------------------------------
            for (column, item) in enumerate(row_data):
                if not _key_is_valid(self._cell_styles[row][column], 'suppress'):
                    #---------------------------------------
                    # Generate CELL tag (<td>)
                    #---------------------------------------
                    # Apply floating point formatter to the cell contents
                    # (if it is a float)
                    item_tex = self._formatter(item, self._cell_styles[row][column], useHTML=False)

                    # Add bold and italic tags if set
                    if _key_is_valid(self._cell_styles[row][column], 'bold'):
                        item_tex = '\\textbf{' + item_tex + '}'
                    if _key_is_valid(self._cell_styles[row][column], 'italic'):
                        item_tex = '\\textit{' + item_tex + '}'

                    # Get html style string
                    # style_html = self._get_style_html(self._cell_styles[row][column])
                    # Should there be a _get_style_latex

                    if 'row_span' in self._cell_styles[row][column]:
                        row_span = str(self._cell_styles[row][column]['row_span'])
                        item_tex = '\\multirow{' + row_span + '}{*}{' + item_tex + '}'

                    if cell_align[row,column] != pref_align[column] or cell_vBorder[row,column] != pref_border[column] or cell_vBorder[row,column+1] != pref_border[column+1]:
                        cell_format = self.VBORDER_TEX[cell_vBorder[row,column]] + self.ALIGN_TEX[cell_align[row,column]] + self.VBORDER_TEX[cell_vBorder[row,column+1]]
                        item_tex = '\\multicolumn{1}{' + cell_format + '}{' + item_tex + '}'

                    # Append cell
                    latex += item_tex
                if column<self._num_columns-1:
                    latex += ' & '

            latex += ' \\\\  '
            latex += self._build_line_separator(cell_hBorder[row+1,:])
            latex += '\n'
        latex += '\\end{tabular}'

        return latex

    def _build_line_separator(self, col_borders):
        style_changes = np.nonzero(abs(np.diff(col_borders)))[0] + 1
    
        style = col_borders[0]
        prev_idx = 0
    
        styles = []
        for idx in style_changes:
            styles.append((style,prev_idx,idx))
            style = col_borders[idx]
            prev_idx = idx
        styles.append((style,prev_idx,len(col_borders)))
    
        clines = ''
        for style,col0,coln in styles:
            if style == self.BORDER_NUM['single_border']:
                clines += '\\cline{%d-%d}'%(col0+1,coln)
            elif style == self.BORDER_NUM['no_border']:
                # Nothing to do for no-border
                pass
            elif style == self.BORDER_NUM['thick_border']:
                clines += '\\thickline{2pt}{%d-%d}'%(col0+1,coln)
        return clines

    def _build_align_matrix(self):
        aligns = np.zeros((self._num_rows,self._num_columns))
        for col in range(self._num_columns):
            for row in range(self._num_rows):
                if 'align' in self._cell_styles[row][col]:
                    align = self._cell_styles[row][col]['align']
                    aligns[row,col] = self.ALIGN_NUM[align]
                else:
                    # The default align
                    aligns[row,col] = self.ALIGN_NUM['left']
        return aligns

    def _build_vborder_matrix(self):
        # Vertical borders
        # By default, unless otherwise specified, border is single_border
        v_borders = np.zeros((self._num_rows,self._num_columns + 1))
        for col in range(self._num_columns):
            for row in range(self._num_rows):
                if 'thick_border' in self._cell_styles[row][col]:
                    side = self._cell_styles[row][col]['thick_border']
                    if 'left' in side:
                        v_borders[row,col] = self.BORDER_NUM['thick_border']
                    if 'right' in side and col>0:
                        v_borders[row,col+1] = self.BORDER_NUM['thick_border']
                if 'no_border' in self._cell_styles[row][col]:
                    side = self._cell_styles[row][col]['no_border']
                    if 'left' in side:
                        v_borders[row,col] = self.BORDER_NUM['no_border']
                    if 'right' in side and col>0:
                        v_borders[row,col+1] = self.BORDER_NUM['no_border']

        # Make first and last columns with thick border have double thickness
        # this compensates that central cells gets 'thick border' from left and right
        first = v_borders[:,0]
        first[first==self.BORDER_NUM['thick_border']] = self.BORDER_NUM['double_thick']
        last = v_borders[:,-1]
        last[last==self.BORDER_NUM['thick_border']] = self.BORDER_NUM['double_thick']

        return v_borders

    def _build_hborder_matrix(self):
        # Horizontal borders
        # By default, unless otherwise specified, border is single_border
        h_borders = np.zeros((self._num_rows + 1,self._num_columns))
        for col in range(self._num_columns):
            for row in range(self._num_rows):
                if 'thick_border' in self._cell_styles[row][col]:
                    side = self._cell_styles[row][col]['thick_border']
                    if 'top' in side:
                        h_borders[row,col] = self.BORDER_NUM['thick_border']
                    if 'bottom' in side and col>0:
                        h_borders[row+1,col] = self.BORDER_NUM['thick_border']
                if 'no_border' in self._cell_styles[row][col]:
                    side = self._cell_styles[row][col]['no_border']
                    if 'top' in side:
                        h_borders[row,col] = self.BORDER_NUM['no_border']
                    if 'bottom' in side and col>0:
                        h_borders[row+1,col] = self.BORDER_NUM['no_border']
                if 'row_span' in self._cell_styles[row][col]:
                    nrows = self._cell_styles[row][col]['row_span']
                    for i in range(nrows-1):
                        h_borders[row+i+1,col] = self.BORDER_NUM['no_border']

        return h_borders














    @property
    def themes(self):
        """Get list of supported formatting themes."""
        return ['basic', 'basic_left', 'basic_both']

    def apply_theme(self, theme_name):
        """Apply a formatting theme to the entire table.

        The list of available themes is returned by the .themes property.
        """

        if theme_name in self.themes:
            # Color rows in alternating colors
            for row in range(len(self.array)):
                if row % 2:
                    self.set_row_style(row, color='Ivory')
                else:
                    self.set_row_style(row, color='AliceBlue')
            # Color column header
            if not theme_name == 'basic_left':
                self.set_row_style(0, bold=True, color='LightGray')
            # Color row header
            if not theme_name == 'basic':
                self.set_column_style(0, bold=True, color='LightGray')
            # Remove upper left corner cell (make white with no left
            # and no top border)
            if theme_name == 'basic_both':
                self.set_cell_style(0, 0, color='White', no_border='left,top')
        else:
            raise ValueError('Unknown theme "%s". Expected one of %s.' %
                             (theme_name, str(self.themes)))

    def set_cell_style(self, row, column, **style_args):
        """Apply style(s) to a single cell."""
        self._range_check(row=row, column=column)
        self._set_cell_style_norender(row, column, **style_args)

    def set_row_style(self, row, **style_args):
        """Apply style(s) to a table row."""
        self._range_check(row=row)
        for column in range(self._num_columns):
            self._set_cell_style_norender(row, column, **style_args)

    def set_column_style(self, column, **style_args):
        """Apply style(s) to  a table column."""
        self._range_check(column=column)
        for row in range(self._num_rows):
            self._set_cell_style_norender(row, column, **style_args)

    def set_global_style(self, **style_args):
        """Apply style(s) to all table cells."""
        for row in range(self._num_rows):
            for column in range(self._num_columns):
                self._set_cell_style_norender(row, column, **style_args)

    def _range_check(self, **check_args):
        """Range check row and/or column index

        Expected argyments:
            row = <row number>
            column = <column number>
        """
        if 'row' in check_args:
            row = check_args['row']
            if row < 0 or row >= self._num_rows:
                raise ValueError(
                    'Bad row (%d).  Expected row in range 0 to %d.' %
                    (row, self._num_rows - 1))

        if 'column' in check_args:
            column = check_args['column']
            if column < 0 or column >= self._num_columns:
                raise ValueError(
                    'Bad column (%d).  Expected column in range 0 to %d.' %
                    (column, self._num_columns - 1))

    #---------------------------------
    # Internal methods
    #---------------------------------

    def _build_style_dict(self, **style_args):
        """Returns a cell style dictionary based on the style arguments."""
        style_dict = copy.deepcopy(style_args)
        for border_type in ['thick_border', 'no_border']:
            if border_type in style_dict:
                border_setting = style_dict[border_type]

                # Type checking
                if type(border_setting) != str:
                    raise TypeError(
                        ('%s must be a string of comma ' % border_type) +
                        'separated border names (e.g. "left,right")')
                # Value checking
                if (set(border_setting.replace(' ', '').split(',')) -
                        IpyTable._valid_borders):
                    raise ValueError(
                        ('%s must be a string of comma ' % border_type) +
                        'separated border names (e.g. "left,right"). Valid ' +
                        'border names: %s' %
                        str(IpyTable._valid_borders))
                # Substitute all edges for 'all'
                if border_setting == 'all':
                    style_dict[border_type] = 'left,right,top,bottom'

        return style_dict

    def _merge_cell_style(self, row, column, cell_style):
        """Merge new cell style dictionary into the old

        Existing items are superseded by new.
        """
        styles = self._cell_styles[row][column]
        for (new_key, new_value) in cell_style.items():
            if (new_key in ['thick_border', 'no_border']) and (new_key in styles):
                # Merge the two border lists
                old_borders = self._split_by_comma(styles[new_key])
                new_borders = self._split_by_comma(new_value)
                styles[new_key] = ",".join(
                    old_borders + list(set(new_borders) - set(old_borders)))
            else:
                styles[new_key] = new_value

    def _set_cell_style_norender(self, row, column, **style_args):
        """Apply style(s) to a single cell, without rendering."""
        cell_style = self._build_style_dict(**style_args)

        self._merge_cell_style(row, column, cell_style)
        if 'row_span' in cell_style:
            for row in range(row + 1, row + cell_style['row_span']):
                self._cell_styles[row][column]['suppress'] = True
        if 'column_span' in cell_style:
            for column in range(
                    column + 1,
                    column + cell_style['column_span']):
                self._cell_styles[row][column]['suppress'] = True

        # If a thick right hand border was specified, then also apply it
        # to the left of the adjacent cell (if one exists)
        if ('thick_border' in cell_style
                and 'right' in cell_style['thick_border']
                and column + 1 < self._num_columns):
            self._merge_cell_style(
                row, column + 1,
                self._build_style_dict(thick_border='left'))

        # If a clear left hand border was specified, then also apply it
        # to the right of the adjacent cell (if one exists)
        if ('no_border' in cell_style
                and 'left' in cell_style['no_border']
                and column > 0):
            self._merge_cell_style(
                row, column - 1,
                self._build_style_dict(no_border='right'))

        # If a thick bottom border was specified, then also apply it to
        # the top of the adjacent cell (if one exists)
        if ('thick_border' in cell_style
                and 'bottom' in cell_style['thick_border']
                and row + 1 < self._num_rows):
            self._merge_cell_style(
                row + 1, column,
                self._build_style_dict(thick_border='top'))

        # If a clear top border was specified, then also apply it to
        # the bottom of the adjacent cell (if one exists)
        if ('no_border' in cell_style
                and 'top' in cell_style['no_border']
                and row > 0):
            self._merge_cell_style(
                row - 1, column,
                self._build_style_dict(no_border='bottom'))

    def _get_style_html(self, style_dict):
        """Parse the style dictionary and return equivalent html style text."""
        style_html = ''
        if _key_is_valid(style_dict, 'color'):
            style_html += 'background-color:' + style_dict['color'] + ';'

        if _key_is_valid(style_dict, 'thick_border'):
            for edge in self._split_by_comma(style_dict['thick_border']):
                style_html += 'border-%s: 3px solid black;' % edge

        if _key_is_valid(style_dict, 'no_border'):
            for edge in self._split_by_comma(style_dict['no_border']):
                style_html += 'border-%s: 1px solid transparent;' % edge

        if _key_is_valid(style_dict, 'align'):
            style_html += 'text-align:' + str(style_dict['align']) + ';'

        if _key_is_valid(style_dict, 'width'):
            style_html += 'width:' + str(style_dict['width']) + 'px;'

        if style_html:
            style_html = ' style="' + style_html + '"'

        if _key_is_valid(style_dict, 'row_span'):
            style_html = 'rowspan="' + str(style_dict['row_span']) + \
                '";' + style_html

        if _key_is_valid(style_dict, 'column_span'):
            style_html = 'colspan="' + str(style_dict['column_span']) + \
                '";' + style_html

        # Prepend a space if non-blank
        if style_html:
            return ' ' + style_html
        return ''

    def _formatter(self, item, cell_style, useHTML=True):
        """Apply formating to cell contents.

        Applies float format to item if item is a float or float64.
        Converts spaces to non-breaking if wrap is not enabled.
        Returns string.
        """

        # The following check is performed as a string comparison
        # so that ipy_table does not need to require (import) numpy.
        if (str(type(item)) in ["<type 'float'>", "<type 'numpy.float64'>"]
                and 'float_format' in cell_style):
            text = cell_style['float_format'] % item
        else:
            text = str(item)

        # If cell wrapping is not specified
        if not ('wrap' in cell_style and cell_style['wrap']) and useHTML:
            # Convert all spaces to non-breaking and return
            text = text.replace(' ', '&nbsp')
        return text

    def _split_by_comma(self, comma_delimited_text):
        """Returns a list of the words in the comma delimited text."""
        return comma_delimited_text.replace(' ', '').split(',')

#-----------------------------
# Public functions
#-----------------------------


def tabulate(data_list, columns, interactive=True):
    """Renders a list (not array) of items into an HTML table."""
    global _TABLE
    global _INTERACTIVE

    _INTERACTIVE = interactive
    total_items = len(data_list)
    rows = total_items / columns
    if total_items % columns:
        rows += 1
    num_blank_cells = rows * columns - total_items
    if num_blank_cells:
        rows += 1

    # Create an array and pad the ending cells with null strings
    array = copy.copy(_convert_to_list(data_list))
    pad_cells = ['' for dummy in range(num_blank_cells)]
    array = array + pad_cells
    array = [array[x:x + columns] for x in xrange(0, len(array), columns)]

    # Render the array
    _TABLE = IpyTable(array)
    return get_interactive_return_value()


def make_table(array, interactive=True):
    """Create a table in interactive mode."""
    global _TABLE
    global _INTERACTIVE
    _TABLE = IpyTable(array)
    _INTERACTIVE = interactive
    return get_interactive_return_value()


def set_cell_style(row, column, **style_args):
    """Apply style(s) to a single cell."""
    global _TABLE
    _TABLE.set_cell_style(row, column, **style_args)
    return get_interactive_return_value()


def set_column_style(column, **style_args):
    """Apply style(s) to  a table column."""
    global _TABLE
    _TABLE.set_column_style(column, **style_args)
    return get_interactive_return_value()


def set_row_style(row, **style_args):
    """Apply style(s) to a table row."""
    global _TABLE
    _TABLE.set_row_style(row, **style_args)
    return get_interactive_return_value()


def set_global_style(**style_args):
    """Apply style(s) to all table cells."""
    global _TABLE
    _TABLE.set_global_style(**style_args)
    return get_interactive_return_value()


def apply_theme(style_name):
    """Apply a formatting theme to the entire table.

    The list of available themes is returned by the .themes property of
    an IpyTable object.
    """
    global _TABLE
    _TABLE.apply_theme(style_name)
    return get_interactive_return_value()


def render():
    """Render the current table.  Returns the global IpyTable object instance"""
    global _TABLE
    return _TABLE


def get_interactive_return_value():
    """Generates the return value for all interactive functions.

    The interactive functions (make_table(), set_cell_style(), etc.) can
    be used instead of the class interface to build up a table and
    interactively modify it's style, rendering the new table on each call.

    By default all interactive functions return the working global
    IpyTable object (_TABLE), which typically gets rendered by IPython.
    That behavior can be suppressed by setting interactive=False
    when creating a new table with make_table() or tabulate().  If
    interactive rendering is suppressed then all interactive functions will
    return None, and rendering can be achieved explicitly by calling
    render() (which will always return the working global IpyTable object).
    """
    global _INTERACTIVE
    global _TABLE
    if _INTERACTIVE:
        return _TABLE
    else:
        return None

#-----------------------------
# Private functions
#-----------------------------

def _get_most_common(data):
    ctr = Counter(data)
    choice, times = ctr.most_common()[0]
    return choice


def _convert_to_list(data):
    """Accepts a list or a numpy.ndarray and returns a list."""

    # The following check is performed as a string comparison
    # so that ipy_table does not need to require (import) numpy.
    if str(type(data)) == "<type 'numpy.ndarray'>":
        return data.tolist()

    return data


def _key_is_valid(dictionary, key):
    """Test that a dictionary key exists and that it's value is not blank."""
    if key in dictionary:
        if dictionary[key]:
            return True
    return False
