# QJson
A python library that will associate python objects/dicts/lists with json files where the contents of said objects/dicts/lists will be converted to json objects/arrays and stored in their associated .json files whenever a modification is made to the python object/dict/list.

If I have done my job correctly; you shouldn't notice ANY differance between using my objects/dicts/lists and native python objects/dicts/lists aside from how they are instantiated.

If a .json file does not exist the library will create one automatically, but if a folder in the path does not exist, in an effort to reduce messy repos due to typos, it will not create the folders.

usage:
Create a folder called "json_files" in your working directory and then run the following code.

    from JPyon import JPyon(), JDict(), JList()
    
    
    #JPyon inherits from object so you have access to tools like @property and @x.setter.
    class MyJPyon(JPyon):
        def __init__(self, filepath, myVar):
            #Attributes that get saved to .json files go here, before the call to super().
            
            self.myVar = myVar
            super(MyJPyon, self).__init__(filepath)
            
            #Attributes that get re-initialized every session go here, after the call to super().
        
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
    
As mentioned previously you will shouldn't notice a differance between Pyons/JDicts/JLists and native python Objects/Dicts/Lists.
To test this out; go ahead and give the following code a try.
    
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
