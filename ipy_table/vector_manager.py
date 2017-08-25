''' vectors.py

A test vector manager for validating ipy_table
'''

import json
import re
import pprint
from copy import deepcopy

from six import string_types
import numpy as np
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
        print('Vector {}:'.format(len(self.vectors)-1))
        self._show(vector, indent = '    ')
    
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

        # Convert numpy types for (custom) JSON serialization
        save_vectors = deepcopy(self.vectors)
        for vector in save_vectors:
            vector['data'] = _serialize_numpy(vector['data'])

        with open(filename, 'w') as out_file:
            out_file.write(json.dumps(save_vectors, indent=4))
        print('Saved {} vectors.'.format(len(save_vectors)))
            
    def _load(self, filename):
        ''' Load test vectors from a JSON file 
        '''
        with open(filename, 'r') as in_file:
            self.vectors = json.load(in_file)

        # Deserialize numpy types from (custom) JSON storage format
        for vector in self.vectors:
            vector['data'] = _deserialize_numpy(vector['data'])
            
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
                      _kwargs_to_str(kwargs_dict) +
                      ')'
                     )
        print(indent + 'expected_html:')
        display(HTML(_html_indent(vector['expected_html'])))
        if vector['result_html']:
            print(indent + 'result_html:')
            display(HTML(_html_indent(vector['result_html'])))
        
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
            _kwargs_to_str(kwargs_dict) +
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

def _kwargs_to_str(kwargs_dict):
    ''' Converts a kwargs dict into a string representation of normal fn call syntax

        render_table_call({'this': 5, 'that':7}) => 'this=5, that=7'
        '''
    return ', '.join([key + '=' + repr(value) for key, value in kwargs_dict.items()])

def _html_indent(html):
    '''Return html wrapped by an indenting div'''
    return '<div style="margin-left: 35px;">' + html + '</div>'

def _serialize_numpy(item):
    '''Serialize a list or item containing 0 or more numpy float objects

    Arguments:
        item: list or object
    Returns:
        The item, with all instances of numpy float types converted to a
        string of the form: 'numpy.<numpy_type>(<value>)'
    
    Example:
        _serialize_numpy(numpy.float64(1.234)) => 'numpy.float64(1.234)'
        _serialize_numpy([ numpy.float64(1.234), numpy.float32(5.678)]) =>
            ['numpy.float64(1.234)', 'numpy.float32(5.678)']
    '''
    if isinstance(item, (list, tuple)):
        # item is a list.  Process the elements
        return [_serialize_numpy(x) for x in item]
    else:
        type_str = repr(type(item))
        if type_str.startswith("<type 'numpy") or type_str.startswith("<class 'numpy"):
            type_str = type_str.strip("'>").strip("<type '").strip("<class '")
            # Serialize numpy object into a string of the form
            #    'numpy.<numpy_type>(<value>)'
            # example:
            #    'numpy.float64(1.234)'
            return type_str + '(' + str(item) + ')'

        # Return the item unmodified
        return item

def _deserialize_numpy(item):
    '''De-serialize a list or item containing 0 or more serialized numpy float objects

    Serialized numpy objects have the form: 'numpy.<numpy_type>(<value>)'

    Arguments:
        item: list or object
    Returns:
        The item, with all instances of serialized numpy float types converted 
        to the associated numpy float type.
    
    Example:
        _serialize_numpy('numpy.float64(1.234)') => numpy.float64(1.234)
        _serialize_numpy(['numpy.float64(1.234)', 'numpy.float32(5.678)']) =>
            [ numpy.float64(1.234), numpy.float32(5.678)]
    '''
    
    if isinstance(item, (list, tuple)):
        # item is a list.  Process the elements
        return [_deserialize_numpy(x) for x in item]
    else:
        if isinstance(item, string_types) and item.startswith('numpy.'):
            match = re.match(r'^numpy\.(\w*)\(([\d\.]*)\)', item)
            if match and len(match.groups()) == 2:
                type_str, value_str = match.groups()
                if type_str == 'float16':
                    return np.float16(value_str)
                elif type_str == 'float32':
                    return np.float32(value_str)
                elif type_str == 'float64':
                    return np.float64(value_str)
                elif type_str == 'float128':
                    return np.float128(value_str)
                
            raise ValueError("Unexpected numpy serialization format: '{}'".format(item))

        # Return the item unmodified
        return item


