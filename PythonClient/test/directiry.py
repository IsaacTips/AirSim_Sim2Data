import os.path
from datetime import datetime

print(os.path.expanduser('~')+'\Documents\AirSim\\bbox')
print(os.getenv('USERPROFILE')+'\Documents\AirSim\\bbox')


filenames = datetime.now().strftime("%Y%m%d-%H%M%S")

print(filenames)



