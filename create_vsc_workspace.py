import json
import os
import subprocess

import sys
proj_name=sys.argv[1]

#Get current folder name
project_directory = os.path.dirname(os.path.realpath(__file__))
#os.path.
#folder_name = current_folder.split("/")[-1]
#folder_name=proj_directory
    
print("current dir: {}\nfolder name: {}".format(project_directory, proj_name))

#Gets the python virtual enviroment path
os.chdir("./{}".format(proj_name))
result = subprocess.run(["pipenv", "--py"], stdout=subprocess.PIPE)
os.chdir("../")

#formats the path correctly
python_path = result.stdout.decode("utf-8").replace("\n","")

print("your python path is: {}".format(python_path))

#Populate our dictionary to write
vs_code_dict = {
	"folders": [{
        "path": "source"
    }],
	"settings": {
		"python.pythonPath": python_path
	}
}

#Create the json file to write
json_code_str = json.dumps(vs_code_dict, sort_keys=True, indent=2, separators=(',', ': '))

#Create the extention name
extention = "code-workspace"

#Create the path including the file name
file_path_and_name = "{0}/{1}/{1}.{2}".format(
	project_directory, 
	proj_name,
	extention
	)

#Write json data
with open(file_path_and_name,"w") as f:
    f.write(json_code_str)

print("vsc workspace complete")


