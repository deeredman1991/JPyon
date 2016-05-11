import json
import os.path



class JList(list):
    def __init__(self, parent, *args, **kwargs):
        self.parent = parent
        super(JList, self).__init__(*args, **kwargs)
        
    def __getitem__(self, key):
        _item = super(JList, self).__getitem__(key)
        if type(_item) == type({}):
            super(JList, self).__setitem__( key, JDict(self, _item) )
            _item = super(JList, self).__getitem__(key)
        if type(_item) == type([]):
            super(JList, self).__setitem__( key, JList(self, _item) )
            _item = super(JList, self).__getitem__(key)
        return _item
        
    def __setitem__(self, key, value):
        super(JList, self).__setitem__(key, value)
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
        self.parent.write()

class JDict(dict):
    def __init__(self, parent, *args, **kwargs):
        self.parent = parent
        super(JDict, self).__init__( *args, **kwargs)
    def __getitem__(self, key):
        _item = super(JDict, self).__getitem__(key)
        if type(_item) == type({}):
            super(JDict, self).__setitem__( key, JDict(self, _item) )
            _item = super(JDict, self).__getitem__(key)
        if type(_item) == type([]):
            super(JDict, self).__setitem__( key, JList(self, _item) )
            _item = super(JDict, self).__getitem__(key)
        return _item
        
    def __setitem__(self, key, value):
        super(JDict, self).__setitem__(key, value)
        self.write()
        
    def write(self):
        self.parent.write()
        
class QJson(dict):
    def __init__(self, filepath, *args, **kwargs):
        if str(filepath).split('.')[-1] == 'json':
            self.filepath = str(filepath)
        else:
            self.filepath = str('{}.json'.format(filepath))
            
        if os.path.isfile(self.filepath):
            super(QJson, self).__init__(self.read())
        else:
            super(QJson, self).__init__(*args, **kwargs)
            self.write()
           
    def __getitem__(self, key):
        _item = super(QJson, self).__getitem__(key)
        if type(_item) == type({}):
            super(QJson, self).__setitem__( key, JDict(self, _item) )
            _item = super(QJson, self).__getitem__(key)
        if type(_item) == type([]):
            super(QJson, self).__setitem__( key, JList(self, _item) )
            _item = super(QJson, self).__getitem__(key)
        return _item
        
    def __setitem__(self, key, value):
        super(QJson, self).__setitem__(key, value)
        self.write()
    
    def write(self):
        with open(self.filepath, 'w') as outfile:
            json.dump(self, outfile, sort_keys = True, indent = 4,
                ensure_ascii=False)
        
    def read(self):
        with open(self.filepath, 'r') as infile:
            jsonData = json.load(infile)
        self = jsonData
        return self
