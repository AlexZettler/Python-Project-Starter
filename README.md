**********************
Python Project Starter
**********************
This project is written in python and assists in the creation of initializing new projects.


Requirements:
    -A python installation in your system path
    -pipenv [If using windows]


To download with GIT:
    git clone "https://github.com/AlexZettler/Python_Project_Starter" [devdir]

    
To get going:
To create a new project run the following command with [project name] replaced with a string of the project name you wish to create:

Linux:

        >bash project [project name] *args

Windows/cross-platform:

        >cd into [devdir]/source
        >pipenv run python manage_project.py *args

manage_project.py [proj_name] *args
    This script loads all project extensions based on passed flags listed below

<br>

      --pipenv
*Creates a python 3.6 pipenv in the source folder
-[todo] specify a python version to use


<br>

        --git
*Creates a git repository for the project<br>
-[todo]optionally commits your project to either github, or bitbucket<br>
-[semi-implemented] launch your favorite git gui client

<br>

        --vscws
*Creates a json formatted code-workspace file.<br>
VS code workspaces now support pipenv, so your project will get syntex highlighting.<br>
Executing this file will also open vsc in the workspace and save your project preferences.
