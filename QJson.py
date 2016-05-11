import json
import os.path



class JList(list):
    def __init__(self, filepath_or_parent, *args, **kwargs):
    
        assert (filepath_or_parent)
        
        self.filepath = None
        self.parent = None
        
        if type(filepath_or_parent) == type(""):
            if str(filepath_or_parent).split('.')[-1] == 'json':
                self.filepath = str(filepath_or_parent)
            else:
                self.filepath = str('{}.json'.format(filepath_or_parent))
                
            if os.path.isfile(self.filepath):
                super(JList, self).__init__(self.read())
            else:
                super(JList, self).__init__(*args, **kwargs)
                self.write()
        else:
            self.parent = filepath_or_parent
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
        if self.parent != None and self.filepath == None:
            self.parent.write()
        else:
            with open(self.filepath, 'w') as outfile:
                json.dump(self, outfile, sort_keys = True, indent = 4,
                    ensure_ascii=False)
                    
    def read(self):
        if self.parent != None and self.filepath == None:
            return self
        else:
            with open(self.filepath, 'r') as infile:
                jsonData = json.load(infile)
            self = jsonData
            return self

class JDict(dict):
    def __init__(self, filepath_or_parent, *args, **kwargs):
    
        assert (filepath_or_parent)
        
        self.filepath = None
        self.parent = None
        
        if type(filepath_or_parent) == type(""):
            if str(filepath_or_parent).split('.')[-1] == 'json':
                self.filepath = str(filepath_or_parent)
            else:
                self.filepath = str('{}.json'.format(filepath_or_parent))
                
            if os.path.isfile(self.filepath):
                super(JDict, self).__init__(self.read())
            else:
                super(JDict, self).__init__(*args, **kwargs)
                self.write()
        else:
            self.parent = filepath_or_parent
            super(JDict, self).__init__(*args, **kwargs)
            
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
        if self.parent != None and self.filepath == None:
            self.parent.write()
        else:
            with open(self.filepath, 'w') as outfile:
                json.dump(self, outfile, sort_keys = True, indent = 4,
                    ensure_ascii=False)
                    
    def read(self):
        if self.parent != None and self.filepath == None:
            return self
        else:
            with open(self.filepath, 'r') as infile:
                jsonData = json.load(infile)
            self = jsonData
            return self
