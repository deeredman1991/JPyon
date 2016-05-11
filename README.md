# QJson
A python library that will store lists and dicts in .json files whenever they are wrote to automatically.
If the .json does not exist; one will be created

usage:
    import QJson
    
    myDict = JDict("json_files/myJsonDict.json", {"myKey": "myValue"}
    myList = JList("json_files/myJsonList.json", ["myValue"])
    
    print(myDict)
    print(myList)
