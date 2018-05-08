Python Project Starter


This is a project dedicated to assisting in the creation and management of python projects in linux.

create_env.sh
    *The main script to set up a new project
    *To create a new project run the following command with [project name] replaced with a string of the project name you wish to create that has the same naming restrictions as a directory:
        
        >bash create_env.sh [project name]

create_vsc_workspace.py
    *The script that creates the visual studio code workspace
    *The script accepts a single parameter of the project name and creates a json formatted code-workspace file with a link to the pipenv python executable.
    *to create a python executable in a child folder dictated by the project name and with pyojectname.code-workspace as the project name run: 
    
        >python create_vsc_workspace.py [projectname]
