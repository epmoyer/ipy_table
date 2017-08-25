import os
import pytest
from ipy_table import VectorManager

vectors = VectorManager(os.path.join('test', 'test_vectors.json'))

vector_ids = [x for x in range(len(vectors.vectors))]

@pytest.mark.parametrize('vector_id', vector_ids)
def test_vectors(vector_id):
    vector_manager = VectorManager()
    vector = vectors.vectors[vector_id]
    vector_manager.run_vector(vector)
    assert vector['result_html'] == vector['expected_html']