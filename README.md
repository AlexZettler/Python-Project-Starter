**********************
Python Project Starter
**********************
This project is written in python to streamline the initialization new projects.


Requirements:<br>
    -A python installation in your system path<br>
    -pipenv [If using windows]<br>


To download with GIT:

    git clone "https://github.com/AlexZettler/Python_Project_Starter" [devdir]

    
To get going:<br>
To create a new project run the following command with [project name] replaced with a string of the project name you wish to create:
<br>

Linux:

        >bash project [project name] *args

Windows/cross-platform:

        >cd into [devdir]/source
        >pipenv run python manage_project.py *args

**********************

    manage_project.py [proj_name] *args
<br>
This script loads all project extensions based on passed flags listed below

**********************
<br>

      --pipenv
*Creates a python 3.6 pipenv in the source folder<br>
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
