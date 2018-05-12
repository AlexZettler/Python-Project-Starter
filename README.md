Python Project Starter

A project to get you up, running and working on new projects as fast as possible

This project is written almost entirely in python with a command line interface to pass arguements into the script
This means that it is *mostly* cross platform but currently only officially supports Linux.


create_env.sh

    *The main script to set up a new project

    *To create a new project run the following command with [project name] replaced with a string of the project name you wish to create that has the same naming restrictions as a directory:

        >bash project [project name] *args


create_vsc_workspace.py

    *The script that creates the enviroment
    
    *The script accepts a single parameter of the project name and:
    
        *Creates the folder structure
    
        *Creates the pipenv

        #*Creates a git repository for the project

        *Creates a json formatted code-workspace file with a link to the pipenv python executable.

    *to create a python project in the managed_projects directory run: 
    
        >python source/manage_project.py [projectname] *args
