import json
import os

def create_folder_structure(proj_path, *paths):
	
    for d in (paths):
        try:
            os.mkdir(d)
        except FileExistsError:
            pass

    if "source" not in os.listdir(proj_path):
        raise Exception("project folder could not be created")

def create_workspace(proj_path: str, proj_name: str):
    
	#Make the workspace dictionary
	vs_code_dict = make_workspace_dict()

	#Create the json file to write
	json_code_str = json.dumps(vs_code_dict, sort_keys=True, indent=2, separators=(',', ': '))

	#Create the path including the file name
	file_path_and_name = get_workspace_path(proj_path, proj_name)

	# Write json data
	with open(file_path_and_name,"w") as f:
		f.write(json_code_str)

def get_workspace_name(proj_name:str):
	"""
	returns the name of the workspace file to create
	"""
	return "{}.code-workspace".format(proj_name)

def get_workspace_path(proj_path:str, proj_name:str):
	"""
	returns the path and name of the workspace file to create
	"""
	return "{}/{}".format(
	proj_path, 
	get_workspace_name(proj_name)
	)

def make_workspace_dict():
	"""
	returns the populated vscode dictionary to write
	"""
	vs_code_dict = {
		"folders": [{
			"path": "source"
		}],
		"settings": {
			#vs code by default looks for pipenv so this is irrelevent
			#"python.pythonPath": python_path
		}
	}
	return vs_code_dict