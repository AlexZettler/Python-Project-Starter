Python Project Starter

A project to get YOU, up, running and working on new projects as fast as possible

This project is written in python and assists in the creation of initializing new projects


A command line interface assists in the installation of pipenv and creates a virtualenviroment to run the python script. This means that this tool can be used regardless of the python version you have installed


The command line interface also passes arguements into the project creation script. This allows for the command line interface to execute the script with parameters as the python virtual enviroment.

This means that the script is *mostly* cross platform but currently only officially supports Linux.



To create a new project run the following command with [project name] replaced with a string of the project name you wish to create:

    Linux:
        >bash project [project name] *args

create_vsc_workspace.py
    This script loads all project extensions based on passed flags

        *The script requires an initial positional arg of the project name:
            *Creates the folder structure
        
        --pipenv
            *Creates a pipenv in the source folder

        --git
            *Creates a git repository for the project[NEW]

        --vscws
            *Creates a json formatted code-workspace file. VS code workspaces now support pipenv so your project will get syntex highlighting based on your installed packages.


