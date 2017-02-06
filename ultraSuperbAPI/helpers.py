import json

def buildResponseDictionary(data={},error={}):
    constructed_dict = {
        "data": data,
        "error": error
    }
    return json.dumps(constructed_dict)

def validJSON(JSON):
    try:
        test = json.loads(JSON)
    except ValueError as e:
        print(e)
        return False
    return True
