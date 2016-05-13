# JPyon for Python 2.7
A python library that will associate python objects/dicts/lists with .json files where the contents of said objects/dicts/lists will be converted to json objects/arrays and stored in their associated .json files whenever a modification is made, and only when a modification is ACTUALLY made (i.e. if `myJList[0] == 5` then `myJList[0] = 5` will NOT trigger a write to the .json), to the python object/dict/list.

If for some reason you want to manually write to the .json you can always call `myJList.write()`

If I have done my job correctly; you shouldn't notice ANY differance between using my objects/dicts/lists and native python objects/dicts/lists aside from how they are instantiated.

If an object/dict/list shares a .json with another object/dict/list; the second object instantiated will point to the first object. In this way; all objects should always mirror the contents of the .json without actually having to read and parse the .json every time a value is changed. While I do not recommend instantiating two objects that share the same .json file; that option is now availible to you. (You still cannot have two objects of differant types that share the same .json file for obvious reasons.)

If a .json file does not exist, to help speed up production; the library will create one automatically but if a folder in the path does not exist, in an effort to reduce messy repos due to typos; it will not create the folders. I feel this is a solid compromise between speed and safety.

usage:
  Create a folder called "json_files" in your working directory and then run the following code.
```
from JPyon import JPyon(), JDict(), JList()


#JPyon inherits from object so you have access to tools like @property and @x.setter.
class MyJPyon(JPyon):
    def __init__(self, filepath, myVar):
        #Member variables that get saved to .json files go here, before the call to super().
        
        self.myVar = myVar
        super(MyJPyon, self).__init__(filepath)
        
        #Member variables that get re-initialized every session go here, after the call to super().
    
#This is how you initialize each datatype.
# variable_name = ClassName(path_to_json, instance_attributes)

#Objects
myObj = MyJPyon("json_files/myJsonObj.json", "foobar")
myObj2 = MyJPyon("json_files/myJsonObj2.json", "barfoo")

#Dictionaries
myDict = JDict("json_files/myJsonDict.json", {"foo": "bar"})
myDict2 = JDict("json_files/myJsonDict2.json", {"bar": "foo"})

#Lists
myList = JList("json_files/myJsonList.json", ["foobar"])
myList2 = JList("json_files/myJsonList2.json", ["barfoo"])
```
As mentioned previously you will shouldn't notice a differance between Pyons/JDicts/JLists and native python Objects/Dicts/Lists.
To test this out; go ahead and give the following code a try.
```
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
print("")
print("Dict Test")
print(myDict)
print("")
print("List Test")
print(myList)
```

#Proper Documentation

###class JPyon(object):
```
# JPyon() is a class that is meant to be sub-classed.
# If two JPyon objects share a .json file; they will both share the same member variables.
# JPyon() objects get written to .json files as strings that lead to their associated .json file.
```
```    
def __init__(filepath):
    # __init__() must be called with a `filepath` of type `string` using super() from your subclasses 
    # constructor. 
    
    # Any member variables written to your JPyon sub-class before __init__() is called 
    # will be overwritten by it's associated .json file if one exists; if one does not exist then 
    # your sub-classes attributes will be written to the .json file at `filepath` for the next 
    # time your object gets instantiated. 
    
    # Any attribute written after the call to __init__() will be re-instantiated every time 
    # with their default values. 
    
    # If this seems confusing; see the code examples above.
```

###class JDict(dict):
```
# JDict behaves like a native python dictionary, aside from it's instantiation.
# If a JDict shares a .json file with another JDict; they will both share the same key, value pairs.
```
``` 
#Usage: myJDict = JDict('filepath.json', {"foo": "bar"})
#    From this point forward myJDict should behave like any other native python dictionary.
#    While JDict cannot store native python objects; it can store JPyon objects, which inherit from object.
#    When storing a JPyon object; the JPyon object will be stored as a string leading to it's 
#    associated .json file.
```

###class JList(list):
```
# JList behaves like a native python list, aside from it's instantiation.
# if a JList shares a .json file with another JList; they will both share the same key, value pairs.
```
```
#Usage: myJList = JList('filepath.json', ["foo", "bar"])
#    From this point forward myJList should behave like any other native python list.
#    While JList cannot store native python objects; it can store JPyon objects, which inherit from object.
#    When storing a JPyon object; the JPyon object will be stored as a string leading to it's 
#    associated .json file.
```
