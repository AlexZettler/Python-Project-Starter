# Python Project Starter

This project is written in python to streamline the initialization new projects.


## Requirements
- A python installation in your system path
- pipenv [If using windows]<br>

## Lets get going
To create a new project run the following

- Using pipenv:

        >cd into [devdir]/source
        >pipenv run python manage_project.py [project name] *args


- Using the Linux bash script:

        >bash project [project name] *args


## manage_project.py [proj_name] *args
This script loads all project extensions based on passed flags listed below

      --pipenv
      
- Creates a python 3.6 pipenv in the source folder
- [todo] specify a python version to use


        --git
- Creates a git repository for the project<br>
- [todo] optionally commits your project to either github, or bitbucket<br>
- [semi-implemented] launch your favorite git gui client


        --vscws
- Creates a json formatted code-workspace file. VS code workspaces now support pipenv, so your project will get syntex highlighting. Executing this file will also open vsc in the workspace and save your project preferences.
