''' vectors.py

A test vector manager for validating ipy_table
'''

import json
import pprint

from ipy_table import make_table, tabulate
from IPython.display import display, HTML

pp = pprint.PrettyPrinter(indent=4)

class VectorManager(object):
    ''' Test vector manager for validating ipy_table
    '''

    def __init__(self, filename=None):
        self.vectors = []
        if filename is not None:
            self._load(filename)

    def add(self, description, data, operations, tabulate_columns=None):
        ''' Add a new vector

        Creates a test vector describing the various data and method calls
        necessary to create a table object.

        Can be used to create vectors describing tables constructed using
        make_table() or tabulate()

        The appropriate table constructors and methods will be called, 
        then the resulting table object will be queried to get its
        HTML representation, which will be set in the vector's
        vector['expected_HTML'] field.

        At a later time, the vector can be checked using run_vector()

        Arguments:
            description: A text description for the vector
                If there is one and only one operation in the operations
                argument, then description can be blank, and a default 
                description will be created from the operation.
            data: The data from which to create the table.
                For make_table() vectors this is a list of lists.
                For tabulate() vectors this is a list
            operations: A list of tuples of the form (method, kwargs)
                were kwargs is a dict.
            tabulate_columns: If None then the vector is a make_table()
                vector, else it is a tabulate() vector and this value
                represents the number of columns.
        '''
        if not description:
            if len(operations) != 1:
                raise ValueError (
                    'Must pass one and only one operation to use default description')
            else:
                # Create default description from requested operation
                method_name, kwargs_dict = operations[0]
                description = self.render_table_call(
                    method_name, kwargs_dict)
        
        vector = dict(
            description=description,
            data=data,
            operations=operations,
            expected_html='',
            result_html='',
            tabulate_columns=tabulate_columns
            )

        # Execute the test vector
        self.run_vector(vector)

        # Since we are creating the test vector,
        # copy the result into expected, and clear
        # the result.
        vector['expected_html'] = vector['result_html']
        vector['result_html'] = ''

        self.vectors.append(vector)
        self._show(vector)
    
    def show_all(self):
        ''' Show all test vectors

        This method should be run in a Jupyter notebook 
        environment, as the results use display() to
        render HTML results. 
        '''
        for index, vector in enumerate(self.vectors):
            print('Vector {}:'.format(index))
            self._show(vector, indent='    ')
            
    def save(self, filename):
        ''' Save test vectors to a JSON file 
        '''
        with open(filename, 'w') as out_file:
            out_file.write(json.dumps(self.vectors, indent=4))
        print('Saved {} vectors.'.format(len(self.vectors)))
            
    def _load(self, filename):
        ''' Load test vectors from a JSON file 
        '''
        with open(filename, 'r') as in_file:
            self.vectors = json.load(in_file)
            
    @staticmethod
    def _show(vector, indent=''):
        ''' Show a test vector

        This method should be run in a Jupyter notebook 
        environment, as it uses display() to
        render expected/result HTML. 
        '''
        print(indent + 'description: ' + repr(vector['description']))
        print(indent + 'data:{}'.format(pp.pformat(vector['data'])))
        print(indent + 'operations:')
        if not vector['operations']:
            print(indent + '    (None)')
        else:
            for operation in vector['operations']:
                method_name, kwargs_dict = operation
                print(indent + 
                      '    ' +
                      'table.' +
                      method_name +
                      '(' +
                      kwargs_to_str(kwargs_dict) +
                      ')'
                     )
        print(indent + 'expected_html:')
        display(HTML(html_indent(vector['expected_html'])))
        if vector['result_html']:
            print(indent + 'result_html:')
            display(HTML(vector['result_html']))
        
    @staticmethod
    def render_table_call(method_name, kwargs_dict):
        ''' Renders a method name and a kwargs dict into a table call

        render_table_call('my_method', {'this': 5, 'that':7}) 
            => 'table.my_method(this=5, that=7)'
        '''
        return (
            'table.' +
            method_name +
            '(' +
            kwargs_to_str(kwargs_dict) +
            ')')

    @staticmethod
    def run_vector(vector):
        ''' Executes a test vector, sets vector['result_html'] to the result

        Returns: True if (after execution) vector['result_html'] matches
            vector['expected_html']
        '''
        if vector['tabulate_columns']:
            # This is a tabulate() vector.
            table = tabulate(
                vector['data'],
                vector['tabulate_columns'])
        else:
            # This is a make_table() vector
            table = make_table(vector['data'])
            
        # For each operation, call the designated table method with
        # the designated keyword arguments
        for operation in vector['operations']:
            method_name, kwargs_dict = operation
            method = getattr(table, method_name)
            method(**kwargs_dict)

        # Update the vector with the result
        vector['result_html'] = table._repr_html_()

        return vector['result_html'] == vector['expected_html']

def kwargs_to_str(kwargs_dict):
    ''' Converts a kwargs dict into a string representation of normal fn call syntax

        render_table_call({'this': 5, 'that':7}) => 'this=5, that=7'
        '''
    return ', '.join([key + '=' + repr(value) for key, value in kwargs_dict.items()])

def html_indent(html):
    '''Return html wrapped by an indenting div'''
    return '<div style="margin-left: 35px;">' + html + '</div>'