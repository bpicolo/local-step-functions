import pytest

from local_step_functions.exceptions import StateException
from local_step_functions.util import path_update


def test_path_update():
    assert path_update('$', {}, 'hello') == 'hello'
    assert path_update('$.foo', {}, 'hello') == {'foo': 'hello'}
    assert path_update('$.foo.bar', {}, 'hello' == {'foo': {'bar': 'hello'}})
    assert path_update('$.foo.bar', {'hello': 'there'}, 'boy') == {
        'hello': 'there',
        'foo': {
            'bar': 'boy'
        }
    }


def test_path_update_raise():
    with pytest.raises(StateException) as e:
        path_update('$.bar.baz', {'bar': 'not a dict'}, 'anything')

    assert e.value.message == 'Unable to apply step "bar" to input {"bar": "not a dict"}'
