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

_JPYONS_OBJECTS = {}
_JPYONS_DICTS = {}
_JPYONS_LISTS = {}

class JList(list):
    def __init__(self, filepath_or_parent, *args, **kwargs):
    
        assert (filepath_or_parent)
        
        if type(filepath_or_parent) == type(""):
            if str(filepath_or_parent).split('.')[-1] == 'json':
                self._jpyon_filepath = str(filepath_or_parent)
            else:
                self._jpyon_filepath = str('{}.json'.format(filepath_or_parent))
                
            if os.path.isfile(self._jpyon_filepath):
                super(JList, self).__init__(parseJson(self._jpyon_filepath))
            else:
                super(JList, self).__init__(*args, **kwargs)
                self.write()
            
            _JPYONS_LISTS[self._jpyon_filepath] = self
                
        else:
            self._jpyon_parent = filepath_or_parent
            super(JList, self).__init__(*args, **kwargs)
            
    def __repr__(self):
        _repr = super(JList, self).__repr__()
        if hasattr(self, '_jpyon_filepath'):
            if _JPYONS_LISTS.has_key( self._jpyon_filepath ):
                _existing_JList = _JPYONS_LISTS[self._jpyon_filepath]
                if id(_existing_JList) != id(self):
                    _repr = _JPYONS_LISTS[self._jpyon_filepath].__repr__()
        return _repr
            
    def __getitem__(self, key):
        _item = super(JList, self).__getitem__(key)
        if type(_item) == type({}):
            super(JList, self).__setitem__( key, JDict(self, _item) )
            _item = super(JList, self).__getitem__(key)
        elif type(_item) == type([]):
            super(JList, self).__setitem__( key, JList(self, _item) )
            _item = super(JList, self).__getitem__(key)
        elif isinstance(_item, unicode) and '.json' in _item:
            if _JPYONS_OBJECTS.has_key(_item):
                _item = _JPYONS_OBJECTS[_item]
        elif hasattr(self, '_jpyon_filepath'):
            if _JPYONS_LISTS.has_key( self._jpyon_filepath ):
                _existing_JList = _JPYONS_LISTS[self._jpyon_filepath]
                if id(_existing_JList) != id(self):
                    _item = _JPYONS_LISTS[self._jpyon_filepath].__getitem__(key)
        return _item
    
    def __setitem__(self, key, value):
        if len(self) >= key+1:
            _val_copy = super(JList, self).__getitem__(key)
        
        if hasattr(self, '_jpyon_filepath'):
            if _JPYONS_LISTS.has_key( self._jpyon_filepath ):
                _existing_JList = _JPYONS_LISTS[self._jpyon_filepath]
                if id(_existing_JList) != id(self):
                    _JPYONS_LISTS[self._jpyon_filepath].__setitem__(key, value)
        super(JList, self).__setitem__(key, value)
                    
        if len(self) >= key+1:
            if '_val_copy' not in locals() or super(JList, self).__getitem__(key) != _val_copy:
                self.write()
    
    def __delitem__(self, key):
        key = self.__getitem__(key)
        _old_len = len(self)
        
        if hasattr(self, '_jpyon_filepath'):
            if _JPYONS_LISTS.has_key( self._jpyon_filepath ):
                _existing_JList = _JPYONS_LISTS[self._jpyon_filepath]
                if id(_existing_JList) != id(self):
                    _JPYONS_LISTS[self._jpyon_filepath].__delitem__(key)
        super(JList, self).__delitem__(key)
        
        if len(self) < _old_len:
            self.write()
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
    def __setslice__(self, i, j, sequence):
        _old_slice = super(JList, self).__getslice__(i, j)
        
        if hasattr(self, '_jpyon_filepath'):
            if _JPYONS_LISTS.has_key( self._jpyon_filepath ):
                _existing_JList = _JPYONS_LISTS[self._jpyon_filepath]
                if id(_existing_JList) != id(self):
                    _JPYONS_LISTS[self._jpyon_filepath].__setslice__(i, j, sequence)
        super(JList, self).__setslice__(i, j, sequence)
        
        if super(JList, self).__getslice__(i, j) != _old_slice:
            self.write()
    
    def __delslice__(self, i, j):
        _old_len = len(self)
        
        if hasattr(self, '_jpyon_filepath'):
            if _JPYONS_LISTS.has_key( self._jpyon_filepath ):
                _existing_JList = _JPYONS_LISTS[self._jpyon_filepath]
                if id(_existing_JList) != id(self):
                    _JPYONS_LISTS[self._jpyon_filepath].__delslice__(i, j)
        super(JList, self).__delslice__(i, j)
        
        if len(self) < _old_len:
            self.write()
    
    def append(self, x):
        super(JList, self).append(x)
        self.write()
        
    def extend(self, L):
        super(JList, self).extend(L)
        self.write()
        
    def insert(self, i, x):
        super(JList, self).insert(i, x)
        self.write()
        
    def remove(self, x):
        super(JList, self).remove(x)
        self.write()
        
    def pop(self, i=0):
        _pop = super(JList, self).pop(i)
        self.write()
        return _pop
        
    def sort(self, cmp=None, key=None, reverse=False):
        _sort = super(JList, self).sort(cmp, key, reverse)
        self.write()
        return _sort
        
    def reverse(self):
        _reverse = super(JList, self).reverse()
        self.write()
        return _reverse
        
    def write(self):
        if hasattr(self, '_jpyon_parent'):
            self._jpyon_parent.write()
        else:
            with open(self._jpyon_filepath, 'w') as outfile:
                _list_copy = self[:]
                for v in _list_copy:
                    if issubclass(type(v), JPyon):
                        _list_copy[_list_copy.index(v)] = v._jpyon_filepath
                json.dump(_list_copy, outfile, sort_keys = True, indent = 4,
                    ensure_ascii=False)
                    
class JDict(dict):
    def __init__(self, filepath_or_parent, dicti={}):
        assert (filepath_or_parent)
        
        path_or_parent_dict = {}
        if isinstance(filepath_or_parent, basestring):
            if str(filepath_or_parent).split('.')[-1] == 'json':
                self._jpyon_filepath = filepath_or_parent
            else:
                self._jpyon_filepath = '{}.json'.format(filepath_or_parent)
            
            if os.path.isfile(self._jpyon_filepath):
                super(JDict, self).__init__( parseJson(filepath_or_parent) )
            else:
                super(JDict, self).__init__( dicti )
                self.write()
                
            if not _JPYONS_DICTS.has_key(filepath_or_parent):
                _JPYONS_DICTS[filepath_or_parent] = self
                
        else:
            self._jpyon_parent = filepath_or_parent
            super(JDict, self).__init__( dicti )
            
    def __repr__(self):
        _repr = super(JDict, self).__repr__()
        if hasattr(self, '_jpyon_filepath'):
            if _JPYONS_DICTS.has_key( super(JDict, self).__getattribute__('_jpyon_filepath') ):
                _existing_JDict = _JPYONS_DICTS[super(JDict, self).__getattribute__('_jpyon_filepath')]
                if id(_existing_JDict) != id(self):
                    _repr = _JPYONS_DICTS[ super(JDict, self).__getattribute__('_jpyon_filepath') ].__repr__()
        return _repr
            
    def __getitem__(self, key):
        _item = super(JDict, self).__getitem__(key)
        if type(_item) == type({}):
            super(JDict, self).__setitem__( key, JDict(self, _item) )
            _item = super(JDict, self).__getitem__(key)
        elif type(_item) == type([]):
            super(JDict, self).__setitem__( key, JList(self, _item) )
            _item = super(JDict, self).__getitem__(key)
        elif isinstance(_item, basestring) and '.json' in _item:
            if _JPYONS_OBJECTS.has_key(_item):
                _item = _JPYONS_OBJECTS[_item]
        elif hasattr(self, '_jpyon_filepath'):
            if _JPYONS_DICTS.has_key( super(JDict, self).__getattribute__('_jpyon_filepath') ):
                _existing_JDict = _JPYONS_DICTS[super(JDict, self).__getattribute__('_jpyon_filepath')]
                if id(_existing_JDict) != id(self):
                    _item = _JPYONS_DICTS[ super(JDict, self).__getattribute__('_jpyon_filepath') ].__getitem__(key)
        return _item
        
    def __setitem__(self, key, value):
        if self.has_key(key):
            _val_copy = self.__getitem__(key)
            
        if hasattr(self, '_jpyon_filepath'):
            if _JPYONS_DICTS.has_key( super(JDict, self).__getattribute__('_jpyon_filepath') ):
                _existing_JDict = _JPYONS_DICTS[super(JDict, self).__getattribute__('_jpyon_filepath')]
                if id(_existing_JDict) != id(self):
                    _item = _JPYONS_DICTS[ super(JDict, self).__getattribute__('_jpyon_filepath') ].__setitem__(key, value)
        super(JDict, self).__setitem__(key, value)
        
        if self.has_key(key):
            if '_val_copy' not in locals() or self.__getitem__(key) != _val_copy:
                self.write()
        
    def __delitem__(self, key):
        _had_key = self.has_key(key)
        
        super(JDict, self).__delitem__(key)
        
        if _had_key and not self.has_key(key):
            self.write()
            
    def clear(self):
        super(JDict, self).clear()
        self.write()
        
    def fromkeys(self, seq, value=None):
        _fromkeys = super(JDict, self).fromkeys(seq, value)
        self.write()
        return _fromkeys
        
    def pop(self, key, default=object()):
        _pop = super(JDict, self).pop(key, default)
        self.write()
        return _pop
        
    def popitem(self):
        _popitem = super(JDict, self).popitem()
        self.write()
        return _popitem
        
    def setdefault(self, key, default=None):
        _setdefault = super(JDict, self).setdefault(key, default)
        self.write()
        return _setdefault
        
    def update(self, arg=None, **kwargs):
        _update = super(JDict, self).update(arg, **kwargs)
        self.write()
        return _update
        
    def write(self):
        if hasattr(self, '_jpyon_parent'):
            self._jpyon_parent.write()
        else:
            with open(self._jpyon_filepath, 'w') as outfile:
                _dict_copy = self.copy()
                for k, v in _dict_copy.iteritems():
                    if issubclass(type(v), JPyon):
                        _dict_copy[k] = v._jpyon_filepath
                json.dump(_dict_copy, outfile, sort_keys = True, indent = 4,
                    ensure_ascii=False)

class JPyon(object):
    def __init__(self, filepath):
        self.jPyon_Link(filepath)
            
    def __getattribute__(self, name):
        _attr = super(JPyon, self).__getattribute__(name)
        
        if hasattr(self, '_jpyon_filepath'):
            if _JPYONS_OBJECTS.has_key( super(JPyon, self).__getattribute__('_jpyon_filepath') ):
                _existing_JPyon = _JPYONS_OBJECTS[super(JPyon, self).__getattribute__('_jpyon_filepath')]
                if id(_existing_JPyon) != id(self):
                   _attr = _JPYONS_OBJECTS[ super(JPyon, self).__getattribute__('_jpyon_filepath') ].__getattribute__(name)
        
        if isinstance(_attr, basestring) and '.json' in _attr and _attr != super(JPyon, self).__getattribute__('_jpyon_filepath'):
            if _JPYONS_OBJECTS.has_key(_attr):
                _attr = _JPYONS_OBJECTS[_attr]
                
        return _attr
        
    def __setattr__(self, name, value):
        if hasattr(self, name):
            _attr_copy = self.__dict__[name]
            
        if hasattr(self, '_jpyon_filepath'):
            if _JPYONS_OBJECTS.has_key( super(JPyon, self).__getattribute__('_jpyon_filepath') ):
                _existing_JPyon = _JPYONS_OBJECTS[super(JPyon, self).__getattribute__('_jpyon_filepath')]
                if id(_existing_JPyon) != id(self):
                    _JPYONS_OBJECTS[ super(JPyon, self).__getattribute__('_jpyon_filepath') ].__setattr__(name, value)
        super(JPyon, self).__setattr__(name, value)
        
        if hasattr(self, name):
            if'_attr_copy' not in locals() or self.__dict__[name] != _attr_copy:
                if hasattr(self.__dict__, "write"):
                    self.write()
            
    def __delattr__(self, name):
        _hadattr = hasattr(self, name)
        
        if _JPYONS_OBJECTS.has_key( super(JPyon, self).__getattribute__('_jpyon_filepath') ):
            _existing_JPyon = _JPYONS_OBJECTS[super(JPyon, self).__getattribute__('_jpyon_filepath')]
            if id(_existing_JPyon) != id(self):
                _JPYONS_OBJECTS[ super(JPyon, self).__getattribute__('_jpyon_filepath') ].__delattr__(name)
        super(JPyon, self).__delattr__(name)
        
        if _hadattr and not hasattr(self, name):
            self.write()
            
    def jPyon_Link(self, filepath):
        super(JPyon, self).__setattr__('_jpyon_filepath', filepath)
        if os.path.isfile(filepath):
            super(JPyon, self).__setattr__( '__dict__', JDict( self, parseJson(filepath) ) )
        else:
            super(JPyon, self).__setattr__( '__dict__', JDict( self, self.__dict__ ) )
        _JPYONS_OBJECTS[filepath] = self
        self.write()
        
    def write(self):
        with open(self._jpyon_filepath, 'w') as outfile:
            _dict_copy = self.__dict__.copy()
            for k, v in _dict_copy.iteritems():
                if issubclass(type(v), JPyon):
                    _dict_copy[k] = v._jpyon_filepath
                    
            if hasattr(_dict_copy, '_jpyon_filepath'):
                del _dict_copy['_jpyon_filepath']
            json.dump(_dict_copy, outfile, sort_keys = True, indent = 4,
                ensure_ascii=False)
        
def parseJson(filepath):
    with open(filepath, 'r') as infile:
        jsonData = json.load(infile) 
    return jsonData
           
class MyJPyon(JPyon):
    def __init__(self, filepath, myVar):
        self.myVar = myVar
        self.jPyon_Link(filepath)
    
if __name__ == '__main__':
    import time
    # Returns current time in seconds from epoch UTC
    current_utc_time = lambda: int(round(time.time()))

    # Returns current time in millis from epoch UTC
    current_utc_time_millis = lambda: int(round(time.time()) * 1000)

    startUTC = current_utc_time_millis()
    print("Start Instantiate")
    myObj = MyJPyon("myJsonObj.json", "foobar")
    myObj2 = MyJPyon("myJsonObj2.json", "barfoo")
    myDict = JDict("myJsonDict.json", {"foo": "bar"})
    myDict2 = JDict("myJsonDict2.json", {"bar": "foo"})
    myList = JList("myJsonList.json", ["foobar"])
    myList2 = JList("myJsonList2.json", ["barfoo"])

    myObj3 = MyJPyon("myJsonObj.json", "notbar")
    myDict3 = JDict("myJsonDict.json", {"foo": "notbar"})
    myList3 = JList("myJsonList.json", ["notbar"])
    print("Finish Instantiate")
    print("-")
    print('Took {} to instantiate'.format(current_utc_time_millis()-startUTC))

    print("~~~")

    startUTC = current_utc_time_millis()
    print("Start Assignments")
    myList3[0] = "defnotbar"
    myObj3.myVar = "defnotbar"
    myDict3["foo"] = "defnotfoo"
    print("Finish Assignments")
    print("-")
    print('Took {} to assign'.format(current_utc_time_millis()-startUTC))

    print("~~~")

    startUTC = current_utc_time_millis()
    print("Start Prints")
    listStartUTC = current_utc_time_millis()
    print(myList)
    print(myList2)
    print(myList3)
    print("-")
    print('Took {} to print lists'.format(current_utc_time_millis()-listStartUTC))

    DictStartUTC = current_utc_time_millis()
    print(myDict)
    print(myDict2)
    print(myDict3)
    print('Took {} to print dicts'.format(current_utc_time_millis()-DictStartUTC))

    DictStartUTC = current_utc_time_millis()
    print(myObj.myVar)
    print(myObj2.myVar)
    print(myObj3.myVar)
    print('Took {} to print objs'.format(current_utc_time_millis()-DictStartUTC))
    print("Finish Prints")
    print("-")
    print('Took {} to print'.format(current_utc_time_millis()-startUTC))

    #myDict3["foo"] = "defnotbar"

    #print(myList[0])
    #print(myList3[0])

    #print(myList)
    #print(myList3)

    #myDict3["foo"] = "notbar"

    #myDict["foo"]

    #print(myDict)
    #print(myDict3)

    #myList[0].myVar = "foobar"

    #print('{} | {} | {}'.format(myObj.objTest.myVar, myDict["objTest"].myVar, myList[0]))


    #myObj.myVar = "notrarra"

    #del myObj.myVar

    #myDict["foo"] = 'not bar'

    #del myDict["foo"]

    #myList[0] = "bar"

    #myList[0:4] = ["asd", "aecae", "aevv", "aeac"]

    #print (myList)

    #print(myList)

    #del myList[0]

    #myList[0] = myObj2
    #print(myObj2)
    #print(myList[0])

    #myListTest = JList("listTest.json", ["foobar"])
    #myListTest2 = JList("listTest.json", ["foobar"])

    #myListTest[0] = "notbarrr"

    #print(myListTest[0])
    #print(myListTest2[0])

    '''
    #Object Test
    myObj.objTest = myObj2
    myDict["objTest"] = myObj2
    myList[0] = myObj2

    #DictTest
    myObj.dictTest = myDict2
    myDict["dictTest"] = myDict2
    myList.append(myList2)

    #ListTest
    myObj.listTest = myList2
    myDict["listTest"] = myList2
    myList.insert(-1, myDict2)

    print("Start")
    print("Object Test")
    print('ObjTest = {} DictTest = {} ListTest = {}'.format(myObj.objTest, myObj.dictTest, myObj.listTest))
    print("Dict Test")
    print(myDict)
    print("List Test")
    print(myList)
    '''
    '''
    myList.append(x)
    myList.extend(x)
    myList.insert(i, x)
    myList.remove(x)
    myList.pop([i])
    myList.index(x)
    myList.count(x)
    myList.sort(cmp=None, key=None, reverse=False)
    myList.reverse()

    len(myDict)
    myDict[key]
    myDict[key] = value
    del myDict[key]
    key in myDict
    key not in myDict
    iter(myDict)
    myDict.clear()
    myDict.copy()
    myDict.fromkeys(seq[, value])
    myDict.get(key[, default])
    myDict.has_key(key)
    myDict.items()
    myDict.iteritems()
    myDict.iterkeys()
    itervalues()
    keys()
    pop(key[, default])
    popitem()
    setdefault(key[, default])
    update([other])
    values()
    viewitems()
    viewkeys()
    viewvalues()
    '''
