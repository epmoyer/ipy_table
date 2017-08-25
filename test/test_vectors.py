import os
import pytest
from ipy_table import VectorManager

vector_manager = VectorManager(os.path.join('test', 'test_vectors.json'))
vectors = vector_manager.vectors

@pytest.mark.parametrize('vector', vectors)
def test_vector(vector):
    vector_manager.run_vector(vector)
    assert vector['result_html'] == vector['expected_html']