import json

def create_workspace(proj_path: str, proj_name: str, python_path: str):
    
	#print("project dir: {}\nfolder name: {}".format(proj_path, proj_name))

	#Populate our dictionary to write
	vs_code_dict = {
		"folders": [{
			"path": "source"
		}],
		"settings": {
			#vs code by default looks for pipenv so this is irrelevent
			#"python.pythonPath": python_path
		}
	}

	#Create the json file to write
	json_code_str = json.dumps(vs_code_dict, sort_keys=True, indent=2, separators=(',', ': '))

	#Create the path including the file name
	file_path_and_name = "{}/{}.code-workspace".format(
		proj_path, 
		proj_name
		)

	# Write json data
	with open(file_path_and_name,"w") as f:
		f.write(json_code_str)