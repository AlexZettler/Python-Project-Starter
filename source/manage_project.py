import json
import os
import subprocess
import platform
import sys
import argparse

def create_pip_env(proj_path: str):

	os.chdir(proj_path)

	# create the working pipenv
	subprocess.run(["pipenv", "--python", "3.6"], stdout=subprocess.PIPE)

	# run platform specific instructions
	if platform.system() == "Windows":
		pass
	elif platform.system() == "Linux":
		pass

def install_requirements(proj_path: str):
	requirements_file = "requirements.txt"

	os.chdir(proj_path)
	if requirements_file in os.listdir():
		subprocess.run(["pipenv", "install", "-r", requirements_file], stdout=subprocess.PIPE)

def create_workspace_folder_structure(*paths):
    
	for d in (paths):
		try:
			os.mkdir(d)
		except FileExistsError:
			pass

	if "source" not in os.listdir(proj_path):
		raise Exception("project folder could not be created")

def create_workspace(proj_path: str, proj_name: str, python_path: str):

	#print("project dir: {}\nfolder name: {}".format(proj_path, proj_name))

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

	# Write json data
	with open(file_path_and_name,"w") as f:
		f.write(json_code_str)

	#print("vsc workspace creation complete")

def get_pipenv_python_path(source_path: str):
	#Gets the python virtual enviroment path
	
	os.chdir(source_path)
	result = subprocess.run(["pipenv", "--py"], stdout=subprocess.PIPE)

	#formats the path correctly
	python_path = result.stdout.decode("utf-8").replace("\n","")

	return python_path

def create_git_repo(proj_path: str):
    raise NotImplementedError


def title_text(string_to_title, title_bar_length=15):
    print("\n{1}\n{0}\n{1}".format(string_to_title, "*"*title_bar_length))

if __name__ == "__main__":
    	
	title_text("Arguements Parsing Details")

	############
	#  Parser  #
	############
	parser = argparse.ArgumentParser(
		description='Optional app description'
		)

	# Required positional argument
	parser.add_argument(
		'name',
		type=str,
		help='A required string for the project name')
	
	# Switch for git initialization
	parser.add_argument('--git', action='store_true',
		help='Add to initialize a git repository')

	# Parse the args
	args = parser.parse_args()

	#Print these bad bois
	print("Project name is: {}".format(args.name))
	print("Git is {} created".format({True:"being", False:"not being"}[args.git]))

	###########
	#  Paths  #
	###########
	
	file_path = os.path.realpath(__file__)
	base_path = "{}/../managed_projects".format(
		os.path.dirname(file_path))
	proj_path = "{}/{}".format(base_path, args.name)
	source_path = "{}/{}".format(proj_path, "source")
	
	# create folder structure
	create_workspace_folder_structure(
		base_path,
		proj_path,
		source_path
		)

	# Create pipenv and get the path
	title_text("Creating pip enviroment")
	create_pip_env(source_path)
	python_path = get_pipenv_python_path(source_path)

	# Create the vs code workspace
	title_text("Creating workspace")
	create_workspace(proj_path, args.name, python_path)

	# Create git repo
	if args.git:
		print("One day I will be able to create your glorious git repo")
		create_git_repo(proj_path)
