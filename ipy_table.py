"""Table formatting package for IP[y] Notebooks"""

from IPython.core.display import HTML
import copy


__version__ = 1.07

# Private table object used for interactive mode
_TABLE = None

#-----------------------------
# Classes
#-----------------------------


class IpyTable(object):

    #---------------------------------
    # External methods
    #---------------------------------

    def __init__(self, array, interactive=False, debug=False):
        self.array = array
        self._interactive = interactive
        self._debug = debug

        self._num_rows = len(array)
        self._num_columns = len(array[0])

        # Check that array is well formed
        for row in array:
            if len(row) != self._num_columns:
                raise ValueError("Array rows must all be of equal length.")

        self._cell_styles = [[{'float_format': '%0.4f'}
                              for dummy in range(self._num_columns)]
                             for dummy2 in range(self._num_rows)]

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

        return self._render_update()

    def set_cell_style(self, row, column, **style_args):
        """Apply style(s) to a single cell."""
        self._set_cell_style_norender(row, column, **style_args)
        return self._render_update()

    def set_row_style(self, row, **style_args):
        """Apply style(s) to a table row."""
        for column in range(self._num_columns):
            self._set_cell_style_norender(row, column, **style_args)
        return self._render_update()

    def set_column_style(self, column, **style_args):
        """Apply style(s) to  a table column."""
        for row in range(self._num_rows):
            self._set_cell_style_norender(row, column, **style_args)
        return self._render_update()

    def set_global_style(self, **style_args):
        """Apply style(s) to all table cells."""
        for row in range(self._num_rows):
            for column in range(self._num_columns):
                self._set_cell_style_norender(row, column, **style_args)
        return self._render_update()

    def render(self):
        """Render the table.  Return an iPython IPython.core.display object."""

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
                    html += '<td ' + style_html + '>' + item_html + '</td>'
            html += '</tr>'
        if self._debug:
            print html
        return HTML(html)

    #---------------------------------
    # Internal methods
    #---------------------------------

    def _render_update(self):
        """Renders the table only if in interactive mode."""
        if(self._interactive):
            return self.render()
        return None

    def _build_style_dict(self, **style_args):
        """Returns a cell style dictionary based on the style arguments."""
        style_dict = copy.deepcopy(style_args)
        if 'thick_border' in style_dict:
            if style_dict['thick_border'] == 'all':
                style_dict['thick_border'] = 'left,right,top,bottom'
        if 'no_border' in style_dict:
            if style_dict['no_border'] == 'all':
                style_dict['no_border'] = 'left,right,top,bottom'
        return style_dict

    def _merge_cell_style(self, row, column, cell_style):
        """Merge new cell style dictionary into the old

        Existing items are superseded by new.
        """
        styles = self._cell_styles[row][column]
        for (new_key, new_value) in cell_style.items():
            if (new_key in ['border', 'no_border']) and (new_key in styles):
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

        return style_html

    def _formatter(self, item, cell_style):
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
        if not ('wrap' in cell_style and cell_style['wrap']):
            # Convert all spaces to non-breaking and return
            text = text.replace(' ', '&nbsp')
        return text

    def _split_by_comma(self, comma_delimited_text):
        """Returns a list of the words in the comma delimited text."""
        return comma_delimited_text.replace(' ', '').split(',')

#-----------------------------
# Public functions
#-----------------------------


def tabulate(data_list, columns, float_format="%0.4f"):
    """Renders a list (not array) of items into an HTML table."""
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
    table = IpyTable(array)
    return table.render()


def make_table(array, interactive=True, debug=False):
    """Create a table in interactive mode."""
    global _TABLE
    _TABLE = IpyTable(array, interactive=interactive, debug=debug)
    return _TABLE._render_update()


def set_cell_style(row, column, **style_args):
    """Apply style(s) to a single cell."""
    global _TABLE
    return _TABLE.set_cell_style(row, column, **style_args)


def set_column_style(column, **style_args):
    """Apply style(s) to  a table column."""
    global _TABLE
    return _TABLE.set_column_style(column, **style_args)


def set_row_style(row, **style_args):
    """Apply style(s) to a table row."""
    global _TABLE
    return _TABLE.set_row_style(row, **style_args)


def set_global_style(**style_args):
    """Apply style(s) to all table cells."""
    global _TABLE
    return _TABLE.set_global_style(**style_args)


def apply_theme(style_name):
    """Apply a formatting theme to the entire table.

    The list of available themes is returned by the .themes property of
    an IpyTable object.
    """
    global _TABLE
    return _TABLE.apply_theme(style_name)


def render():
    """Render the table.  Returns an iPython IPython.core.display object."""
    global _TABLE
    return _TABLE.render()

#-----------------------------
# Private functions
#-----------------------------


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
