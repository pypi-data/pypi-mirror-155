import logging
import pytest
LOGGER = logging.getLogger(__name__)

from urtools.list_tools.packing import get_depth
class Test_get_depth:
    @pytest.mark.parametrize(('x', 'expected'),
                             (([], 1),
                              ([1], 1),
                              ([[]], 2),
                              (1, 0),
                              ({1, (2, 3)}, 2),
                              (['1', ['2', ['333', ('4444',)]]], 4)))
    def test(self, x, expected):
        assert get_depth(x) == expected

from urtools.list_tools.packing import pack
class Test_pack:
    @pytest.mark.parametrize(('x', 'depth_out', 'expected'),
                             ((1, 2, [[1]]),
                              ([1], 2, [[1]]),
                              ([[1]], 2, [[1]]),
                              ([[1]], 1, [1]),
                              ([1], 0, 1)
                              ))
    def test(self, x, depth_out, expected):
        assert pack(x, depth_out) == expected

from urtools.list_tools.packing import unpack_to_max_depth
class Test_unpack:
    @pytest.mark.parametrize(('packed', 'max_depth', 'expected'),
                             (([[1]], None, [1]),
                              ([[1]], 1, [1]),
                              ([[1]], 0, 1),
                              ))
    def test(self, packed, max_depth, expected):
        assert unpack_to_max_depth(packed, max_depth=max_depth) == expected
