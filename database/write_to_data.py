import json

def write_json(embd, name_img):
    with open("database/database.json") as fp:
        listObj = json.load(fp)

    listObj.append({
        name_img:embd.tolist()
    })

    with open("database/database.json", 'w') as json_file:
        json.dump(listObj, json_file, 
                            indent=4,  
                            separators=(',',': '))


def load_data(name_database = "database/database.json"):
    myfile = open(name_database, "rb")
    myfile = json.load(myfile)
    return myfile