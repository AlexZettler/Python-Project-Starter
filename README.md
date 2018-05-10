Python Project Starter


This is a project dedicated to assisting in the creation and management of python projects in linux.

create_env.sh

    *The main script to set up a new project

    *To create a new project run the following command with [project name] replaced with a string of the project name you wish to create that has the same naming restrictions as a directory:

        >bash project [project name]


create_vsc_workspace.py

    *The script that creates the enviroment
    
    *The script accepts a single parameter of the project name and:
    
        *Creates the folder structure
    
        *Creates the pipenv

        #*Creates a git repository for the project

        *Creates a json formatted code-workspace file with a link to the pipenv python executable.

    *to create a python project in the managed_projects directory run: 
    
        >python source/manage_project.py [projectname]
