import os
import subprocess
import platform
import sys
import argparse

def create_pip_env(source_path: str):

	"""
	Create a pipenv enviroment in the given directory

		:param proj_path:str:
			The path to the project source folder
	"""

	#Change directory
	os.chdir(source_path)

	# create the working pipenv
	subprocess.run(["pipenv", "--python", "3.6"], stdout=subprocess.PIPE)

	# run platform specific instructions
	if platform.system() == "Windows":
		pass
	elif platform.system() == "Linux":
		pass

def install_requirements(proj_path: str, source_path: str):
	"""
	Installs the requirements from the requirements file if it exists

		:param proj_path:str:
			The path to the project folder
	"""

	requirements_file = "requirements.txt"

	os.chdir(proj_path)
	if requirements_file in os.listdir():
    	
		#go to the source folder and install pipenv requirements
		os.chdir(source_path)
		subprocess.run(["pipenv", "install", "-r", requirements_file], stdout=subprocess.PIPE)

def create_folder_structure(*paths):
    
	for d in (paths):
		try:
			os.mkdir(d)
		except FileExistsError:
			pass

	if "source" not in os.listdir(proj_path):
		raise Exception("project folder could not be created")

def get_pipenv_python_path(source_path: str):
	#Gets the python virtual enviroment path
	
	os.chdir(source_path)
	result = subprocess.run(["pipenv", "--py"], stdout=subprocess.PIPE)

	#formats the path correctly
	python_path = result.stdout.decode("utf-8").replace("\n","")

	return python_path

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


	#full path of the directory containing 
	manager_directory = os.path.dirname(os.path.realpath(__file__))
	print(manager_directory)

	base_path = "{}/managed_projects".format(
		os.path.dirname(manager_directory))
	print(base_path)

	proj_path = "{}/{}".format(base_path, args.name)
	print(proj_path)

	source_path = "{}/{}".format(proj_path, "source")
	print(source_path)



	# create folder structure
	create_folder_structure(
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
	import workspace_maker
	workspace_maker.create_workspace(proj_path, args.name, python_path)

	# Create git repo
	if args.git:
		import git
		print("One day I will be able to create your glorious git repo")
		git.create_git_repo(proj_path)
