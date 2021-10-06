
import json
import os
print (json.__file__ )
filepath =os.path.expanduser('~')+'\Documents\\AirSim\AirSim\\PythonClient\\test\\test.json'
print(filepath)


with open(filepath, 'r') as f:

    json_data = json.load(f)

#print(json.dumps(json_data) )
print(json.dumps(json_data, indent="\t") )


print(json_data["box2D"]["max"])
print(json_data["box2D"]["min"])