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
import cython_helpers as cy
import importlib

_JPYONS_DATAS = {}

class JList(list):
    def __init__(self, filepath, *args, **kwargs):
        if _JPYONS_DATAS.has_key(filepath):
            raise ValueError ("Json file already in use by another object.")
            
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
    
    def __del__(self):
        _JPYONS_DATAS.pop(self._jpyon_filepath)
        self.write()
    
    def __lt__(self, other):
        return cy.get_len(self) < cy.get_len(other)
    def __le__(self, other):
        return cy.get_len(self) <= cy.get_len(other)
    def __eq__(self, other):
        return self.__repr__() == other.__repr__()
    def __ne__(self, other):
        return self.__repr__() != other.__repr__()
    def __gt__(self, other):
        return cy.get_len(self) > cy.get_len(other)
    def __ge__(self, other):
        return cy.get_len(self) >= cy.get_len(other)
    
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
        
        #For re-instantiating objects.
        if isinstance(_item, dict) and _item.has_key("|JPYON|"):
            #recursively re-instantiate object(s)
            pass
                
        return _item
        
    def write(self):
        _list_copy = self[:]
            
        if _list_copy != _JPYONS_DATAS[ self._jpyon_filepath ]:
            dump(_list_copy, super(JPyon, self).__getattribute__('_jpyon_filepath') )
            
        _JPYONS_DATAS[ self._jpyon_filepath ] = _list_copy
                    
class JDict(dict):
    def __init__(self, filepath, myDict={}):
        if _JPYONS_DATAS.has_key(filepath):
            raise ValueError ("Json file already in use by another object.")
            
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
        
    def __del__(self):
        _JPYONS_DATAS.pop(self._jpyon_filepath)
        self.write()
        
    def __lt__(self, other):
        return cy.get_len(self) < cy.get_len(other)
    def __le__(self, other):
        return cy.get_len(self) <= cy.get_len(other)
    def __eq__(self, other):
        return self.__repr__() == other.__repr__()
    def __ne__(self, other):
        return self.__repr__() != other.__repr__()
    def __gt__(self, other):
        return cy.get_len(self) > cy.get_len(other)
    def __ge__(self, other):
        return cy.get_len(self) >= cy.get_len(other)
            
    def __getitem__(self, key):
        _item = super(JDict, self).__getitem__(key)
        
        #For re-instantiating objects.
        if isinstance(_item, dict) and _item.has_key("|JPYON|"):
            #recursively re-instantiate object(s)
            pass
                    
        return _item
        
    def write(self):
        _dict_copy = self.copy()
            
        if _dict_copy != _JPYONS_DATAS[ self._jpyon_filepath ]:
            dump(_dict_copy, super(JPyon, self).__getattribute__('_jpyon_filepath') )

        _JPYONS_DATAS[ self._jpyon_filepath ] = _dict_copy

class JPyon(object):
    def __init__(self, filepath):
        self.jPyon_Link(filepath)
        
    def __del__(self):
        _JPYONS_DATAS.pop(self._jpyon_filepath)
        self.write()
            
    def __getattribute__(self, name):
        _attr = super(JPyon, self).__getattribute__(name)
        
        #For re-instantiating objects.
        if isinstance(_attr, dict) and _attr.has_key("|JPYON|"):
            #recursively re-instantiate object(s)
            pass
                
        return _attr
            
    def jPyon_Link(self, filepath):
        if _JPYONS_DATAS.has_key(filepath):
            raise ValueError ("Json file already in use by another object.")
    
        if os.path.isfile(filepath):
            _JPYONS_DATAS[filepath] = parse_json(filepath)
            super(JPyon, self).__setattr__( '__dict__', dict( _JPYONS_DATAS[filepath] ) )
        else:
            _JPYONS_DATAS[filepath] = None
            super(JPyon, self).__setattr__( '__dict__', dict( self.__dict__ ) )
        super(JPyon, self).__setattr__('_jpyon_filepath', filepath)
        
    def write(self):
        _dict_copy = self.__dict__.copy()

        del _dict_copy['_jpyon_filepath']
            
        if _dict_copy != _JPYONS_DATAS[ super(JPyon, self).__getattribute__('_jpyon_filepath') ]:
            dump(_dict_copy, super(JPyon, self).__getattribute__('_jpyon_filepath') )
                
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
            
def reinstantiate(obj):
    #if obj is dict or list and if obj has a dict or list
    #recursively call self on that dict or list
    #if dict or list has attribute '|JPYON|'
    #Instantiate that object from the class listed under the key '|JPYON|'
    if hasattr(obj, 'iteritems'):
        obj_copy = obj.copy()
        for k, v in obj_copy.iteritems:
            if issubclass(v, dict) or issubclass(v, list):
                obj[k] = reinstantiate(v)
            if k == "|JPYON|":
                module = v.split(".")
                className = v.pop(-1)
                module = '.'.join(v)
                MyClass = getattr(importlib.import_module(module), className)
                obj[k] = MyClass()
    else:
        obj_copy = obj[:]
        for k, v in enumerate(obj_copy):
            if issubclass(v, dict) or issubclass(v, list):
                obj[k] = reinstantiate(v)
        
    return obj
           
@atexit.register
def safety_test():
    if len(_JPYONS_DATAS) >= 1:
        print("*WARNING* Object did not get deconstructed and therefore did not get saved.")
        print("Potential memory leak...")
        print("Are you storing the object globally?")
        print("Are the object/objects attributes referencing themselves?")
        print(_JPYONS_DATAS)
           
#@atexit.register
#def write_all():
#    _jpyons = dict(_JPYONS_OBJECTS, **_JPYONS_DICTS)
#    _jpyons.update(_JPYONS_LISTS)
#    
#    for k,v in _jpyons.iteritems():
#        v.write()        