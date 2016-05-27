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
import importlib

_JPYONS_DATAS = {}

class JList(list):
    def __init__(self, filepath, *args, **kwargs):
        if filepath in _JPYONS_DATAS:
            raise ValueError ("Json file already in use by another object.")
            
        if str(filepath).split('.')[-1] == 'json':
            self._jpyon_filepath = str(filepath)
        else:
            self._jpyon_filepath = str('{}.json'.format(filepath))
            
        if os.path.isfile(filepath):
            _JPYONS_DATAS[filepath] = parse_json(filepath)
            _list = _reinstantiate(_JPYONS_DATAS[filepath])
            
            super(JList, self).__init__(_list)
        else:
            _JPYONS_DATAS[ filepath ] = None 
            super(JList, self).__init__(*args, **kwargs)
    
    def __del__(self):
        self.write()
        _JPYONS_DATAS.pop(self._jpyon_filepath)
        
    def write(self):
        _list_copy = self[:]
            
        if _list_copy != _JPYONS_DATAS[ self._jpyon_filepath ]:
            dump(_list_copy, super(JList, self).__getattribute__('_jpyon_filepath') )
            
        _JPYONS_DATAS[ self._jpyon_filepath ] = _list_copy
                    
class JDict(dict):
    def __init__(self, filepath, myDict={}):
        if filepath in _JPYONS_DATAS:
            raise ValueError ("Json file already in use by another object.")
            
        if str(filepath).split('.')[-1] == 'json':
            self._jpyon_filepath = filepath
        else:
            self._jpyon_filepath = '{}.json'.format(filepath)
        
        if os.path.isfile(self._jpyon_filepath):
            _JPYONS_DATAS[filepath] = parse_json(filepath)
            _dict = _reinstantiate(_JPYONS_DATAS[filepath])
            
            super(JDict, self).__init__( _dict )
        else:
            _JPYONS_DATAS[ filepath ] = None 
            super(JDict, self).__init__( myDict )
        
    def __del__(self):
        self.write()
        _JPYONS_DATAS.pop(self._jpyon_filepath)
        
    def write(self):
        _dict_copy = self.copy()
            
        if _dict_copy != _JPYONS_DATAS[ self._jpyon_filepath ]:
            dump(_dict_copy, super(JDict, self).__getattribute__('_jpyon_filepath') )

        _JPYONS_DATAS[ self._jpyon_filepath ] = _dict_copy

class JPyon(object):
    def __init__(self, filepath):
        self.jPyon_Link(filepath)
        
    def __del__(self):
        self.write()
        _JPYONS_DATAS.pop(self._jpyon_filepath)
            
    def jPyon_Link(self, filepath):
        if filepath in _JPYONS_DATAS:
            raise ValueError ("Json file already in use by another object.")
    
        if os.path.isfile(filepath):
            _JPYONS_DATAS[filepath] = parse_json(filepath)
            obj = _reinstantiate(_JPYONS_DATAS[filepath])
            super(JPyon, self).__setattr__( '__dict__', dict( obj ) )
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
        if hasattr(jsonData, 'items'):
            for k, v in jsonData.items():
                try:
                    if isinstance(k, unicode):
                        k = str(k)
                    if isinstance(v, unicode):
                        v = str(v)
                except NameError:
                    if isinstance(k, str):
                        k = str(k)
                    if isinstance(v, str):
                        v = str(v)
                del jsonData[k]
                jsonData[k] = v
        else:
            for k, v in enumerate(jsonData):
                try:
                    if isinstance(v, unicode):
                        jsonData[k] = str(v)
                except NameError:
                    if isinstance(v, str):
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
                try:
                    if isinstance(v, basestring):
                        objStr += '"' + _tmp + '"'
                    else:
                        objStr += _tmp
                except NameError:
                    if isinstance(v, str):
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
        for k, v in copy.items():
            for _ in range(0, indent*4):
                objStr += ' '
            objStr += '"' + str(k) + '": '
            _tmp = '{}'.format(str(v))
            if ' object at ' in _tmp or isinstance(v, dict) or isinstance(v, list):
                objStr += dumps(v, indent+1)
            else:
                try:
                    if isinstance(v, basestring):
                        objStr += '"' + _tmp + '"'
                    else:
                        objStr += _tmp
                except NameError:
                    if isinstance(v, str):
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
            
def _reinstantiate(obj):
    if hasattr(obj, 'items'):
        obj_copy = obj.copy()
        for k, v in obj_copy.items():
            if issubclass(type(v), dict) or issubclass(type(v), list):
                obj[k] = _reinstantiate(v)
            if k == "|JPYON|":
                module = obj.pop("|JPYON|").split(".")
                className = module.pop(-1)
                module = '.'.join(module)
                MyClass = getattr(importlib.import_module(module), className)
                tmp_obj = MyClass.__new__(MyClass)
                tmp_obj.__dict__ = obj
                obj = tmp_obj
    else:
        obj_copy = obj[:]
        for k, v in enumerate(obj_copy):
            if issubclass(type(v), dict) or issubclass(type(v), list):
                obj[k] = _reinstantiate(v)
    return obj
    
@atexit.register
def safety_test():
    if len(_JPYONS_DATAS) >= 1:
        print(15*"-")
        print("")
        print("SAVE ERROR: ")
        print("    The following JPYON Object(s) did not get deconstructed and therefore did not get saved.")
        print("")
        print(">")
        for k, v in _JPYONS_DATAS.items():
            print("> {}".format(k))
        print(">")
        print("")
        print("*WARNING* Potential memory leak...")
        print(" - Are you storing the object(s) globally?")
        print(" - Is there circular referencing?")
        print("")
        print(15*"-")