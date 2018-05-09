import json
import os
import subprocess
import platform
import sys

def create_pip_env(proj_path: str):

	
	#install pipenv if it hasn't been
	subprocess.run(["pip", "install", "pipenv"], stdout=subprocess.PIPE)
	

	os.chdir(proj_path)

	#create the working pipenv
	print("**creating pip enviroment at {}".format(proj_path))
	subprocess.run(["pipenv", "--python", "3.6"], stdout=subprocess.PIPE)
	print("**created pip enviroment")

	if platform.system() == "Windows":
		pass
	elif platform.system() == "Linux":
		pass


def install_requirements(proj_path: str):
	requirements_file = "requirements.txt"

	os.chdir(proj_path)
	if requirements_file in os.listdir():
		subprocess.run(["pipenv", "install", "-r", "requirements.txt"], stdout=subprocess.PIPE)


def create_workspace_folder_structure(base_path: str, proj_path: str):
    
	for d in (base_path, proj_path,"{}/source".format(proj_path)):
		try:
			os.mkdir(d)
		except FileExistsError:
			pass

	if "source" not in os.listdir(proj_path):
		raise Exception("project folder could not be created")

def create_workspace(proj_path: str, proj_name: str, python_path: str):
		
	print("project dir: {}\nfolder name: {}".format(proj_path, proj_name))

	#Populate our dictionary to write
	vs_code_dict = {
		"folders": [{
			"path": "source"
		}],
		"settings": {
			#vs code by default looks for pipenv
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

	#Write json data
	with open(file_path_and_name,"w") as f:
		f.write(json_code_str)

	print("vsc workspace creation complete")

def get_pipenv_python_path(proj_path: str):
	#Gets the python virtual enviroment path
	
	os.chdir(proj_path)
	result = subprocess.run(["pipenv", "--py"], stdout=subprocess.PIPE)

	#formats the path correctly
	python_path = result.stdout.decode("utf-8").replace("\n","")

	return python_path

def print_spacer():
    print("*"*20)

if __name__ == "__main__":
    	
	#Interperate the arguements
	proj_name = sys.argv[1]
	

	#Define our paths
	print_spacer()
	base_path = "{}/../managed_projects".format(
		os.path.dirname(
			os.path.realpath(
				__file__)))

	proj_path = "{}/{}".format(base_path, proj_name)


	#create folder structure
	create_workspace_folder_structure(base_path, proj_path)
	print_spacer()

	create_pip_env(proj_path)
	print_spacer()


	python_path = get_pipenv_python_path(proj_path)
	create_workspace(proj_path, proj_name, python_path)
	print_spacer()




