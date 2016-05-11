# QJson
A python library that will associate python dicts/lists with json files where the contents of said dicts/lists will be converted to json objects/arrays and stored in it's associated json file whenever a modification is made to the dict/list.

If a .json file does not exist the library will create one automatically, but if a folder in the path does not exist; it will not create the folders.

usage:
Create a folder called "json_files" in your working directory and then run the following code.

    import QJson
    
    myDict = QJson.JDict("json_files/myJsonDict.json", {"foo": "bar"})
    myList = QJson.JList("json_files/myJsonList.json", ["foobar"])
    
    myDict["bar"] = "foo"
    
    myList.pop()
    myList.append("barfoo")
    
    print(myDict)
    print(myList)
