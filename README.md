# JPyon for Python 2.7
A python library that will associate python objects/dicts/lists with .json files where the contents of said objects/dicts/lists will be converted to json objects/arrays and stored in their associated .json files whenever a modification is made to the python object/dict/list and only when a modification is ACTUALLY made (i.e. if `myJList[0] == 5` then `myJList[0] = 5` will NOT trigger a write to the .json but `myJList[0] = 1` will) 

If for some reason you want to manually write to the .json you can always call `myJList.write()` however if you do have to call this method it is most likely a bug in my code.

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
        #Member variables that get saved to .json files go here, before the call to jPyon_Link().
        
        self.myVar = myVar
        self.jPyon_Link(filepath)
        
        #Member variables that get re-initialized every session go here, after the call to jPyon_Link().
    
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

Again; you should NOT need to call `write()`

# Proper Documentation

## `class JPyon(object):`

>JPyon() is a class that is meant to be sub-classed.
>
>If two JPyon() objects share a .json file; they will both share the same member variables.
>
>JPyon() objects being stored by other JPyon() objects get written to .json files as a filepath and then converted back into JPyon() objects durring runtime.
>
>The JPyon class overwrites it's \_\_dict\_\_ with a JDict as a result any lists or dicts stored in a JPyon object will be converted to a JList or JDict.
>
>##### `def jPyon_Link(filepath): `
>>Takes a [basestring](https://docs.python.org/2/library/functions.html#basestring) as an argument.
>>
>>Links the member variables of a JPyon object to a .json file.
>>
>>Call this function in your constructor and member variables assigned before it was called will be overwritten by
>>the .json file every time that object is instantiated while member variables assigned after the function call will not be.
>>
>>If your object does not have a constructor that is fine jPyon_Link() gets called in the JPyon constructor which just takes a filepath as an argument.


## `class JDict(dict):`

>JDict behaves like a native python dictionary, aside from it's instantiation.
>If a JDict shares a .json file with another JDict; they will both share the same key, value pairs.
> 
>Usage: `myJDict = JDict( 'filepath.json', {"foo": "bar"} )`
>>From this point forward myJDict should behave like any other native python dictionary. With the exception that `myJDict.copy()` will return an object of type dict as I figure that if you are making a copy of a dict you probably do not want the copy to write to the .json. That and when you instantiate two JDicts linked to the same .json the second JDict to be instantiated will point to the first so that both will mirror the .json file without having to actually read from the file.
>>    
>>While JDict cannot store native python objects; it can store JPyon objects, which inherit from object.
>>
>>When storing a JPyon object; the JPyon object will be stored as a string leading to it's associated .json file.
>>
>>JDicts storing Lists or Dicts will automatically be converted to JLists and JDicts and linked to the JDict. This way if a change is made to the JList or JDict; it will propegate up the stack until it reaches the JDict linked to the .json which can then write the changes to the .json.


## `class JList(list):`

>JList behaves like a native python list, aside from it's instantiation.
>if a JList shares a .json file with another JList; they will both share the same key, value pairs.
>
>Usage: `myJList = JList( 'filepath.json', ["foo", "bar"] )`
>>From this point forward myJList should behave like any other native python list. With the exception that `myJList[:]` will return an object of type list as I figure that if you are making a copy of a list you probably do not want the copy to write to the .json. That and when you instantiate two JLists linked to the same .json the second JList to be instantiated will point to the first so that both will mirror the .json file without having to actually read from the file.
>>
>>While JList cannot store native python objects; it can store JPyon objects, which inherit from object.
>>
>>When storing a JPyon object; the JPyon object will be stored as a string leading to it's associated .json file.
>>
>>JLists storing Lists or Dicts will automatically be converted to JLists and JDicts and linked to the JList. This way if a change is made to the JList or JDict; it will propegate up the stack until it reaches the JList linked to the .json which can then write the changes to the .json.
