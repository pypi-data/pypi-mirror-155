import logging
LOGGER = logging.getLogger(__name__)

import numpy as np
import pytest

from urtools.dict_tools.dict_nans import filter_dict_nans
class Test_filter_dict_nans:
    @pytest.mark.parametrize(('d', 'expected'),
                             (({1: None, 2: None, 3: np.nan}, {}),
                              ({2: None, 1: 2}, {1: 2})))
    def test_filtered_as_expected(self, d: dict, expected: dict):
        assert filter_dict_nans(d) == expected

from urtools.dict_tools.index import (_dict_multindex_prep_keys,
                                DictInvalidKeyError,
                                KeysAndNegKeysAreNoneError,
                                KeysAndNegKeysAreNotNoneError,
                                NoneInKeysError)
# test all errors
class Test__dict_multindex_prep_keys:
    d_1 = {1:1, 2:2, 3:3}
    def test_DictionaryHasInvalidKeyError(self):
        with pytest.raises(DictInvalidKeyError):
            _dict_multindex_prep_keys({**self.d_1, None: 1})

    def test_KeysAndNegKeysAreNoneError(self):
        with pytest.raises(KeysAndNegKeysAreNoneError):
            _dict_multindex_prep_keys(self.d_1, keys=None, neg_keys=None)

    def test_KeysAndNegKeysAreNotNoneError(self):
        with pytest.raises(KeysAndNegKeysAreNotNoneError):
            _dict_multindex_prep_keys(self.d_1, keys=1, neg_keys=2)

    def test_NoneInKeysError_keys(self):
        with pytest.raises(NoneInKeysError) as exc_info:
            _dict_multindex_prep_keys(self.d_1, keys=[None]) #type:ignore

    def test_NoneInKeysError_neg_keys(self):
        with pytest.raises(NoneInKeysError) as exc_info:
            _dict_multindex_prep_keys(self.d_1, neg_keys=[None]) #type:ignore



from urtools.dict_tools.index import dict_multindex
class Test_dict_multindex:
    d_1 = {1: 1, 2: 2, 'key': 'KEY'}
    @pytest.mark.parametrize(('keys', 'expected'),
                             (('key', {'key': 'KEY'}),
                              ([1, 2], {1: 1, 2: 2}),
                              (d_1.keys(), d_1)))
    def test_keys(self, keys, expected: dict):
        result = dict_multindex(self.d_1, keys=keys)
        assert result == expected

    @pytest.mark.parametrize(('neg_keys', 'expected'),
                             ((2, {1: 1, 'key': 'KEY'}),
                              ([1, 3], {2: 2, 'key': 'KEY'}),
                              ([], d_1),
                              (d_1.keys(), {})))
    def test_neg_keys(self, neg_keys, expected):
        result = dict_multindex(self.d_1, neg_keys=neg_keys)
        assert result == expected

from urtools.dict_tools.index import dict_del_keys
class Test_dict_del_keys:
    d_1 = {1: 1, 2: 2, 'a': 'a', 'bb': 'bb'}
    @pytest.mark.parametrize(('del_keys', 'expected'),
                             ((1, {2: 2, 'a': 'a', 'bb': 'bb'}),
                              (d_1.keys(), {}),
                              (list(d_1.keys()) + [3,4,5], {}),
                              ([], d_1)))
    def test(self, del_keys, expected):
        res = dict_del_keys(self.d_1, del_keys)
        assert res == expected
    
from urtools.dict_tools.index import dict_list_index
class Test_dict_list_index:
    dl_1 = [{1: 2}, {1: 3}, {2: 2}]
    @pytest.mark.parametrize(('keys', 'expected'),
                             ((1, [2, 3, None]),
                              (2, [None, None, 2]),
                              ('x', 3*[None])))
    def test(self, keys, expected):
        result = dict_list_index(self.dl_1, keys)
        assert result == expected

from urtools.dict_tools.index import dict_list_multindex
class Test_dict_list_multindex:  
    dl_1 = [{1:1, 2:2, 3:3},
            {3:0, 4:4, 5:5}]
    @pytest.mark.parametrize(('keys', 'expected'),
                             (([1, 2], {1: [1, None], 2: [2, None]}),
                              (1, {1: [1, None]}),
                              ([], {})))
    def test_keys(self, keys, expected):
        result = dict_list_multindex(self.dl_1, keys)
        assert result == expected

    @pytest.mark.parametrize(('neg_keys', 'expected'),
                             (([1,2,3,4,5], {}),
                              ([], {1: [1, None], 2: [2, None], 3: [3, 0], 4: [None, 4], 5: [None, 5]}),
                              ([2, 3], {1: [1, None], 4: [None, 4], 5: [None, 5]})))
    def test_neg_keys(self, neg_keys, expected):
        result = dict_list_multindex(self.dl_1, neg_keys=neg_keys)
        LOGGER.info(f'{result=}')
        assert result == expected
    
from urtools.dict_tools.is_subdict import is_subdict
class Test_is_subdict:
    @pytest.mark.parametrize(('sub_dict', 'sup_dict', 'expected'),
                             (({1:1}, {2:2, 1:1}, True),
                              ({}, {1:1}, True),
                              ({1:1}, {}, False),
                              ({}, {}, True),
                              ({1:1}, {2:2}, False),
                              ({1:1, 2:2}, {1:1, 0:0}, False),
                              ({1:1}, {1:2, 2:2}, False)))
    def test(self, sub_dict, sup_dict, expected):
        assert is_subdict(sub_dict, sup_dict) == expected

from urtools.dict_tools.join_dicts import join_dicts
class Test_join_dicts:
    d1 = {1:1, 2:2, 3:3}
    d2 = {2:2, 3:4, 10:0}    
    @pytest.mark.parametrize(('dicts', 'expected'),
                             (([d1, d2], {1:1,2:2,3:4,10:0}),
                              ([d2, d1], {1:1,2:2,3:3,10:0}),
                              ([{}, {}], {}),
                              ([{}, {1:1}, {2:2}], {1:1,2:2})))
    def test(self, dicts, expected):
        assert join_dicts(*dicts) == expected

#TODO: add sorting by custom keys and reversing?
from urtools.dict_tools.sort_dict import sort_dict
class Test_sort_dict:
    d1 = {3:3, 1:2, 2:1}
    @pytest.mark.parametrize(('d', 'by', 'expected'),
                             ((d1, 'key', {1:2, 2:1, 3:3}),
                              (d1, 'k', {1:2, 2:1, 3:3}),
                              (d1, 'value', {2:1, 1:2, 3:3}),
                              (d1, 'v', {2:1, 1:2, 3:3}),
                              ({}, 'k', {})))
    def test(self, d, by, expected):
        assert sort_dict(d, by) == expected

    def test_value_error(self):
        with pytest.raises(ValueError):
            sort_dict({}, by='x') #type:ignore
