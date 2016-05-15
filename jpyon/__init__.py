# The MIT License (MIT)
# 
# Copyright (c) 2016 deeredman1991
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import json
import os
import atexit
import cPickle

_JPYONS_OBJECTS = {}
_JPYONS_DICTS = {}
_JPYONS_LISTS = {}
_JPYONS_DATAS = {}

class JList(list):
    def __init__(self, filepath, *args, **kwargs):
        if str(filepath).split('.')[-1] == 'json':
            self._jpyon_filepath = str(filepath)
        else:
            self._jpyon_filepath = str('{}.json'.format(filepath))
            
        if os.path.isfile(filepath):
            _JPYONS_DATAS[ filepath ] = parse_json(filepath)
            super(JList, self).__init__(_JPYONS_DATAS[ filepath ])
        else:
            _JPYONS_DATAS[ filepath ] = None 
            super(JList, self).__init__(*args, **kwargs)
        _JPYONS_LISTS[filepath] = self
    '''
    def __lt__(self, other):
       return len(self) < len(other)
    def __le__(self, other):
        return len(self) <= len(other)
    def __eq__(self, other):
        return self.__repr__() == other.__repr__()
    def __ne__(self, other):
        return self.__repr__() != other.__repr__()
    def __gt__(self, other):
        return len(self) > len(other)
    def __ge__(self, other):
        return len(self) >= len(other)
    '''
    
    def __lt__(self, other):
        print("lt")
        print('__repr__ {} - Len {}'.format(self, len(self)))
        print('__repr__ {} - Len {}'.format(other, len(other)))
        print(len(self) < len(other))
        print('')
        return len(self) < len(other)
    def __le__(self, other):
        print("le")
        print('__repr__ {} - Len {}'.format(self, len(self)))
        print('__repr__ {} - Len {}'.format(other, len(other)))
        print(len(self) <= len(other))
        print('')
        return len(self) <= len(other)
    def __eq__(self, other):
        return self.__repr__() == other.__repr__()
    def __ne__(self, other):
        return self.__repr__() != other.__repr__()
    def __gt__(self, other):
        print("gt")
        print('__repr__ {} - Len {}'.format(self, len(self)))
        print('__repr__ {} - Len {}'.format(other, len(other)))
        print(len(self) > len(other))
        print('')
        return len(self) > len(other)
    def __ge__(self, other):
        print("ge")
        print('__repr__ {} - Len {}'.format(self, len(self)))
        print('__repr__ {} - Len {}'.format(other, len(other)))
        print(len(self) >= len(other))
        print('')
        return len(self) >= len(other)
    
    
    '''
    #Python 3.x prep
    def __setitem__(self, *args):
        if len(args) < 2:
            #__setitem__(self, args[0] = key, args[1] = value)
            if len(self) >= args[0]+1:
                _val_copy = self.__getitem__(args[0])
            super(JList, self).__setitem__(args[0], args[1])
            if len(self) >= args[0]+1:
                if '_val_copy' not in locals() or self.__getitem__(args[0]) != _val_copy:
                    self.write()
        else:
            #__setslice__(self, args[0] = i, args[1] = j, args[2] = sequence)
            _old_slice = super(JList, self).__getslice__(args[0], args[1])
            print (_old_slice)
            super(JList, self).__setitem__(args[0], args[1], args[2])
            if super(JList, self).__getslice__(args[0], args[1]) != _old_slice:
                self.write()
        
    def __delitem__(self, *args):
        if len(args) == 1:
            #__delitem__(self, args[0] = key)
            _old_len = len(self)
            super(JList, self).__delitem__(args[0])
            if len(self) < _old_len:
                self.write()
        else:
            #__delslice__(self, args[0] = i, args[1] = j)
            _old_len = len(self)
            super(JList, self).__delitem__(args[0], args[1])
            if len(self) < _old_len:
                self.write()
    '''
    def __getitem__(self, key):
        _item = super(JList, self).__getitem__(key)
        
        #For converting Pyon objects.
        if isinstance(_item, basestring) and ':|PYON|: ' in _item and _JPYONS_OBJECTS.has_key(_item):
            _item = _JPYONS_OBJECTS[_item]
            super(JList, self).__setitem__(key, _item)
            
        #For mirroring lists that share the same .json file.
        elif _JPYONS_LISTS.has_key( self._jpyon_filepath ):
            _existing_JList = _JPYONS_LISTS[self._jpyon_filepath]
            if id(_existing_JList) != id(self):
                _item = _JPYONS_LISTS[self._jpyon_filepath].__getitem__(key)
                
        return _item
    
    def __setitem__(self, key, value):
        _item = super(JList, self).__setitem__(key, value)
        if _JPYONS_LISTS.has_key( self._jpyon_filepath ):
            _existing_JList = _JPYONS_LISTS[self._jpyon_filepath]
            if id(_existing_JList) != id(self):
                _item = _JPYONS_LISTS[self._jpyon_filepath].__setitem__(key, value)
        return _item
    
    def __delitem__(self, key):
        _item = super(JList, self).__delitem__(key)
        if _JPYONS_LISTS.has_key( self._jpyon_filepath ):
            _existing_JList = _JPYONS_LISTS[self._jpyon_filepath]
            if id(_existing_JList) != id(self):
                _item = _JPYONS_LISTS[self._jpyon_filepath].__delitem__(*args, **kwargs)
        return _item
    
    def __setslice__(self, i, j, sequence):
        _slice = super(JList, self).__setslice__(key, i, j, sequence)
        if _JPYONS_LISTS.has_key( self._jpyon_filepath ):
            _existing_JList = _JPYONS_LISTS[self._jpyon_filepath]
            if id(_existing_JList) != id(self):
                _slice = _JPYONS_LISTS[self._jpyon_filepath].__setslice__(i, j, sequence)
        return _slice
    
    def __delslice__(self, i, j):
        _slice = super(JList, self).__delslice__(key, i, j)
        if _JPYONS_LISTS.has_key( self._jpyon_filepath ):
            _existing_JList = _JPYONS_LISTS[self._jpyon_filepath]
            if id(_existing_JList) != id(self):
                _slice = _JPYONS_LISTS[self._jpyon_filepath].__delslice__(i, j)
        return _slice
        
    def __repr__(self):
        _repr = super(JList, self).__repr__()
        if _JPYONS_LISTS.has_key( self._jpyon_filepath ):
            _existing_JList = _JPYONS_LISTS[self._jpyon_filepath]
            if id(_existing_JList) != id(self):
                _repr = _JPYONS_LISTS[self._jpyon_filepath].__repr__()
        return _repr
        
    def __str__(self):
        _str = super(JList, self).__str__()
        if _JPYONS_LISTS.has_key( self._jpyon_filepath ):
            _existing_JList = _JPYONS_LISTS[self._jpyon_filepath]
            if id(_existing_JList) != id(self):
                _str = _JPYONS_LISTS[self._jpyon_filepath].__str__()
        return _str
        
    def append(self, x):
        _append = super(JList, self).append(x)
        if _JPYONS_LISTS.has_key( self._jpyon_filepath ):
            _existing_JList = _JPYONS_LISTS[self._jpyon_filepath]
            if id(_existing_JList) != id(self):
                _append = _JPYONS_LISTS[self._jpyon_filepath].append(x)
        return _append
        
    def extend(self, L):
        _ext = super(JList, self).extend(L)
        if _JPYONS_LISTS.has_key( self._jpyon_filepath ):
            _existing_JList = _JPYONS_LISTS[self._jpyon_filepath]
            if id(_existing_JList) != id(self):
                _item = _JPYONS_LISTS[self._jpyon_filepath].extend(L)
        return _ext
        
    def insert(self, i, x):
        _ins = super(JList, self).insert(i, x)
        if _JPYONS_LISTS.has_key( self._jpyon_filepath ):
            _existing_JList = _JPYONS_LISTS[self._jpyon_filepath]
            if id(_existing_JList) != id(self):
                _ins = _JPYONS_LISTS[self._jpyon_filepath].insert(i, x)
        return _ins
        
    def remove(self, x):
        _rm = super(JList, self).remove(x)
        if _JPYONS_LISTS.has_key( self._jpyon_filepath ):
            _existing_JList = _JPYONS_LISTS[self._jpyon_filepath]
            if id(_existing_JList) != id(self):
                _rm = _JPYONS_LISTS[self._jpyon_filepath].remove(x)
        return _rm
        
    def pop(self, i=0):
        _pop = super(JList, self).pop(i)
        if _JPYONS_LISTS.has_key( self._jpyon_filepath ):
            _existing_JList = _JPYONS_LISTS[self._jpyon_filepath]
            if id(_existing_JList) != id(self):
                _pop = _JPYONS_LISTS[self._jpyon_filepath].pop(i)
        return _pop
        
    def sort(self, cmp=None, key=None, reverse=False):
        _sort = super(JList, self).sort(cmp, key, reverse)
        if _JPYONS_LISTS.has_key( self._jpyon_filepath ):
            _existing_JList = _JPYONS_LISTS[self._jpyon_filepath]
            if id(_existing_JList) != id(self):
                _sort = _JPYONS_LISTS[self._jpyon_filepath].sort(cmp, key, reverse)
        return _sort
        
    def reverse(self):
        _rev = super(JList, self).__setitem__()
        if _JPYONS_LISTS.has_key( self._jpyon_filepath ):
            _existing_JList = _JPYONS_LISTS[self._jpyon_filepath]
            if id(_existing_JList) != id(self):
                _rev = _JPYONS_LISTS[self._jpyon_filepath].func()
        return _rev
        
    def write(self):
        _list_copy = self[:]
        
        for v in _list_copy:
            if issubclass(type(v), JPyon):
                _list_copy[_list_copy.index(v)] = v._jpyon_filepath
            
        if _list_copy != _JPYONS_DATAS[ self._jpyon_filepath ]:
            with open( self._jpyon_filepath, 'w') as outfile:
                json.dump(_list_copy, outfile, sort_keys = True, indent = 4, ensure_ascii=False)
        _JPYONS_DATAS[ self._jpyon_filepath ] = _list_copy
                    
class JDict(dict):
    def __init__(self, filepath, myDict={}):
        if str(filepath).split('.')[-1] == 'json':
            self._jpyon_filepath = filepath
        else:
            self._jpyon_filepath = '{}.json'.format(filepath)
        
        if os.path.isfile(self._jpyon_filepath):
            _JPYONS_DATAS[ filepath ] = parse_json(filepath)
            super(JDict, self).__init__( _JPYONS_DATAS[ filepath ] )
        else:
            _JPYONS_DATAS[ filepath ] = None 
            super(JDict, self).__init__( myDict )
            
        _JPYONS_DICTS[filepath] = self
            
    def __repr__(self):
        _repr = super(JDict, self).__repr__()
        if _JPYONS_DICTS.has_key( super(JDict, self).__getattribute__('_jpyon_filepath') ):
            _existing_JDict = _JPYONS_DICTS[super(JDict, self).__getattribute__('_jpyon_filepath')]
            if id(_existing_JDict) != id(self):
                _repr = _JPYONS_DICTS[ super(JDict, self).__getattribute__('_jpyon_filepath') ].__repr__()
        return _repr
        
    def __lt__(self, other):
        print("lt")
        print('__repr__ {} - Len {}'.format(self, len(self)))
        print('__repr__ {} - Len {}'.format(other, len(other)))
        print(len(self) < len(other))
        print('')
        return len(self) < len(other)
    def __le__(self, other):
        print("le")
        print('__repr__ {} - Len {}'.format(self, len(self)))
        print('__repr__ {} - Len {}'.format(other, len(other)))
        print(len(self) <= len(other))
        print('')
        return len(self) <= len(other)
    def __eq__(self, other):
        return self.__repr__() == other.__repr__()
    def __ne__(self, other):
        return self.__repr__() != other.__repr__()
    def __gt__(self, other):
        print("gt")
        print('__repr__ {} - Len {}'.format(self, len(self)))
        print('__repr__ {} - Len {}'.format(other, len(other)))
        print(len(self) > len(other))
        print('')
        return len(self) > len(other)
    def __ge__(self, other):
        print("ge")
        print('__repr__ {} - Len {}'.format(self, len(self)))
        print('__repr__ {} - Len {}'.format(other, len(other)))
        print(len(self) >= len(other))
        print('')
        return len(self) >= len(other)
            
    def __getitem__(self, key):
        _item = super(JDict, self).__getitem__(key)
        
        if isinstance(_item, basestring) and ':|PYON|: ' in _item and _JPYONS_OBJECTS.has_key(_item):
            _item = _JPYONS_OBJECTS[_item]
            super(JList, self).__setitem__(key, _item)
                
        elif _JPYONS_DICTS.has_key( super(JDict, self).__getattribute__('_jpyon_filepath') ):
            _existing_JDict = _JPYONS_DICTS[super(JDict, self).__getattribute__('_jpyon_filepath')]
            if id(_existing_JDict) != id(self):
                _item = _JPYONS_DICTS[ super(JDict, self).__getattribute__('_jpyon_filepath') ].__getitem__(key)
                    
        return _item
        
    def __setitem__(self, key, value):
        _item = super(JDict, self).__setitem__(key, value)
        if _JPYONS_DICTS.has_key( super(JDict, self).__getattribute__('_jpyon_filepath') ):
            _existing_JDict = _JPYONS_DICTS[super(JDict, self).__getattribute__('_jpyon_filepath')]
            if id(_existing_JDict) != id(self):
                _item = _JPYONS_DICTS[ super(JDict, self).__getattribute__('_jpyon_filepath') ].__setitem__(key, value)
        return _item
        
        
    def clear(self):
        _item = super(JDict, self).clear()
        if _JPYONS_DICTS.has_key( super(JDict, self).__getattribute__('_jpyon_filepath') ):
            _existing_JDict = _JPYONS_DICTS[super(JDict, self).__getattribute__('_jpyon_filepath')]
            if id(_existing_JDict) != id(self):
                _item = _JPYONS_DICTS[ super(JDict, self).__getattribute__('_jpyon_filepath') ].clear()
        return _item
        
    def fromkeys(self, seq, value=None):
        _keys = super(JDict, self).fromkeys(seq, value)
        if _JPYONS_DICTS.has_key( super(JDict, self).__getattribute__('_jpyon_filepath') ):
            _existing_JDict = _JPYONS_DICTS[super(JDict, self).__getattribute__('_jpyon_filepath')]
            if id(_existing_JDict) != id(self):
                _keys = _JPYONS_DICTS[ super(JDict, self).__getattribute__('_jpyon_filepath') ].fromkeys(seq, value)
        return _keys
        
    def pop(self, key, default=None):
        #test this with None...you want;
        #If key is in the dictionary, remove it and return its value, else return default. 
        #If default is not given and key is not in the dictionary, a KeyError is raised.
        _pop = super(JDict, self).pop(key, default)
        if _JPYONS_DICTS.has_key( super(JDict, self).__getattribute__('_jpyon_filepath') ):
            _existing_JDict = _JPYONS_DICTS[super(JDict, self).__getattribute__('_jpyon_filepath')]
            if id(_existing_JDict) != id(self):
                _pop = _JPYONS_DICTS[ super(JDict, self).__getattribute__('_jpyon_filepath') ].pop(key, default)
        return _pop
        
    def popitem(self):
        _popitem = super(JDict, self).popitem()
        if _JPYONS_DICTS.has_key( super(JDict, self).__getattribute__('_jpyon_filepath') ):
            _existing_JDict = _JPYONS_DICTS[super(JDict, self).__getattribute__('_jpyon_filepath')]
            if id(_existing_JDict) != id(self):
                _popitem = _JPYONS_DICTS[ super(JDict, self).__getattribute__('_jpyon_filepath') ].popitem()
        return _popitem
        
    def setdefault(self, key, default=None):
        _def = super(JDict, self).setdefault(self, key, default)
        if _JPYONS_DICTS.has_key( super(JDict, self).__getattribute__('_jpyon_filepath') ):
            _existing_JDict = _JPYONS_DICTS[super(JDict, self).__getattribute__('_jpyon_filepath')]
            if id(_existing_JDict) != id(self):
                _def = _JPYONS_DICTS[ super(JDict, self).__getattribute__('_jpyon_filepath') ].setdefault(self, key, default)
        return _def
        
    def update(self, other={}):
        super(JDict, self).update(other)
        if _JPYONS_DICTS.has_key( super(JDict, self).__getattribute__('_jpyon_filepath') ):
            _existing_JDict = _JPYONS_DICTS[super(JDict, self).__getattribute__('_jpyon_filepath')]
            if id(_existing_JDict) != id(self):
                _JPYONS_DICTS[ super(JDict, self).__getattribute__('_jpyon_filepath') ].update(other)
        return None
        
    def write(self):
        _dict_copy = self.copy()
        
        for k, v in _dict_copy.iteritems():
            if issubclass(type(v), JPyon):
                _dict_copy[k] = v._jpyon_filepath
            
        if _dict_copy != _JPYONS_DATAS[ self._jpyon_filepath ]:
            with open( self._jpyon_filepath, 'w') as outfile:
                json.dump(_dict_copy, outfile, sort_keys = True, indent = 4, ensure_ascii=False)
        _JPYONS_DATAS[ self._jpyon_filepath ] = _dict_copy

class JPyon(object):
    def __init__(self, filepath):
        self.jPyon_Link(filepath)
            
    def __getattribute__(self, name):
        #For linking Pyon objects with the same filepath
        if hasattr(self, '_jpyon_filepath'):
            if _JPYONS_OBJECTS.has_key( ':|PYON|: {}'.format(super(JPyon, self).__getattribute__('_jpyon_filepath')) ):
                _existing_JPyon_dict = _JPYONS_OBJECTS[ ':|PYON|: {}'.format(super(JPyon, self).__getattribute__('_jpyon_filepath')) ]
                if id( super(JPyon, _existing_JPyon_dict).__getattribute__('__dict__') ) != id( super(JPyon, self).__getattribute__('__dict__') ):
                    super(JPyon, self).__setattr__('__dict__', _existing_JPyon_dict)
    
        _attr = super(JPyon, self).__getattribute__(name)
        
        #For unpacking Pyon objects
        if isinstance(_attr, basestring) and ':|PYON|: ' in _attr and _JPYONS_OBJECTS.has_key(_item):
            _attr = _JPYONS_OBJECTS[_attr]
            super(JPyon, self).__setattr__(name, _attr)
                
        return _attr
        
    def __setattr__(self, name, value):
        if hasattr(self, '_jpyon_filepath'):
            if _JPYONS_OBJECTS.has_key( ':|PYON|: {}'.format(super(JPyon, self).__getattribute__('_jpyon_filepath')) ):
                _existing_JPyon = _JPYONS_OBJECTS[ ':|PYON|: {}'.format(super(JPyon, self).__getattribute__('_jpyon_filepath')) ]
                if id(_existing_JPyon) != id(self):
                    _JPYONS_OBJECTS[ ':|PYON|: {}'.format(super(JPyon, self).__getattribute__('_jpyon_filepath')) ].__setattr__(name, value)
        super(JPyon, self).__setattr__(name, value)
            
    def __delattr__(self, name):
        if hasattr(self, '_jpyon_filepath'):
            if _JPYONS_OBJECTS.has_key( ':|PYON|: {}'.format( super(JPyon, self).__getattribute__('_jpyon_filepath') ) ):
                _existing_JPyon = _JPYONS_OBJECTS[ ':|PYON|: {}'.format(super(JPyon, self).__getattribute__('_jpyon_filepath')) ]
                if id(_existing_JPyon) != id(self):
                    _JPYONS_OBJECTS[ ':|PYON|: {}'.format(super(JPyon, self).__getattribute__('_jpyon_filepath')) ].__delattr__(name)
        super(JPyon, self).__delattr__(name)
            
    def jPyon_Link(self, filepath):
        if os.path.isfile(filepath):
            _JPYONS_DATAS[filepath] = parse_json(filepath)
            super(JPyon, self).__setattr__( '__dict__', dict( _JPYONS_DATAS[filepath] ) )
        else:
            _JPYONS_DATAS[filepath] = None
            super(JPyon, self).__setattr__( '__dict__', dict( self.__dict__ ) )
        super(JPyon, self).__setattr__('_jpyon_filepath', filepath)
        if not _JPYONS_OBJECTS.has_key( ':|PYON|: {}'.format(filepath) ):
            _JPYONS_OBJECTS[ ':|PYON|: {}'.format(filepath) ] = self
        
    def write(self):
        _dict_copy = self.__dict__.copy()
        
        for k, v in _dict_copy.iteritems():
            if issubclass(type(v), JPyon):
                _dict_copy[k] = ':|PYON|: {}'.format(v._jpyon_filepath)
                
        del _dict_copy['_jpyon_filepath']
            
        if _dict_copy != _JPYONS_DATAS[ super(JPyon, self).__getattribute__('_jpyon_filepath') ]:
            with open( super(JPyon, self).__getattribute__('_jpyon_filepath'), 'w') as outfile:
                json.dump(_dict_copy, outfile, sort_keys = True, indent = 4, ensure_ascii=False)
                
        _JPYONS_DATAS[ super(JPyon, self).__getattribute__('_jpyon_filepath') ] = _dict_copy

def parse_json(filepath):
    if os.path.isfile(filepath):
        with open(filepath, 'r') as infile:
            jsonData = json.load(infile)
        if hasattr(jsonData, 'iteritems'):
            for k, v in jsonData.iteritems():
                if isinstance(k, unicode):
                    k = str(k)
                if isinstance(v, unicode):
                    v = str(v)
                del jsonData[k]
                jsonData[k] = v
        else:
            for k, v in enumerate(jsonData):
                if isinstance(v, unicode):
                    jsonData[k] = str(v)
        return jsonData
    else:
        return None
        
def dump(obj, filepath):
    jsonData = dumps(obj)
    with open(filepath, 'w') as outfile:
        outfile.write(jsonData)
        
def dumps(obj, indent=1):
    i = 1
    if isinstance(obj, list):
        objStr = '[\n'
        copy = obj[:]
        for v in copy:
            for _ in range(0, indent*4):
                objStr += ' '
            _tmp = '{}'.format(str(v))
            if ' object at ' in _tmp or isinstance(v, dict) or isinstance(v, list):
                objStr += dumps(v, indent+1)
            else:
                if isinstance(v, basestring):
                    objStr += '"' + _tmp + '"'
                else:
                    objStr += _tmp
            if i != len(copy):
                    objStr += ', \n'
            i += 1
    else:
        objStr = '{\n'
        if isinstance(obj, dict):
            copy = obj.copy()
        else:
            for _ in range(0, indent*4):
                objStr += ' '
            objStr += '"|JPYON|": "'
            objType = str(type(obj)).split("'")
            objType = objType[1]
            objStr += objType + '", \n'
            copy = obj.__dict__.copy()
        for k, v in copy.iteritems():
            for _ in range(0, indent*4):
                objStr += ' '
            objStr += '"' + str(k) + '": '
            _tmp = '{}'.format(str(v))
            if ' object at ' in _tmp or isinstance(v, dict) or isinstance(v, list):
                objStr += dumps(v, indent+1)
            else:
                if isinstance(v, basestring):
                    objStr += '"' + _tmp + '"'
                else:
                    objStr += _tmp
            if i != len(copy):
                    objStr += ', \n'
            i += 1
    objStr += '\n'
    for _ in range(0, (indent-1)*4):
        objStr += ' '
    if isinstance(obj, list):
        objStr += ']'
    else:
        objStr += '}'
    return objStr
        
def get_json(filepath, parse=True):
    if _JPYONS_OBJECTS.has_key( ':|PYON|: {}'.format( filepath ) ):
        return _JPYONS_OBJECTS[ ':|PYON|: {}'.format(super(JPyon, self).__getattribute__('_jpyon_filepath')) ].__dict__
    elif _JPYONS_DICTS.has_key( filepath ):
        return _JPYONS_DICTS[filepath]
    elif _JPYONS_LISTS.has_key( filepath ):
        return _JPYONS_LISTS[filepath]
    else:
        return JDict(filepath)
            
@atexit.register
def write_all():
    _jpyons = dict(_JPYONS_OBJECTS, **_JPYONS_DICTS)
    _jpyons.update(_JPYONS_LISTS)
    
    for k,v in _jpyons.iteritems():
        v.write()
        