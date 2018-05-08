##################################
#  # File created by Alex Zettler
#  # pipenv startup script
##################################


##Get the project name from arguements
projectname=$1
gitinit=$2
gitbool=$3

validtrue="y yes t true c create"


##Check if arguement is blank
if [ "$projectname" = "" ]; then
    echo "No arguement given. Please pass the project name as an arguement"

##If arguement isn't blank
else

    ##if a project file doesn't exist Make the project folder
    if [ ! -d "$projectname" ]; then 
        mkdir "$projectname"
    fi;


    ##if a project file has been created or existed
    if [ -d "$projectname" ]; then 

        ##Change into directory and Create the python virtual enviroment
        cd "$projectname"

        ##Create our project source directory
        mkdir "./source"

        ##Verify that pipenv is installed and install it otherwise
        pip install pipenv
        pipenv --python 3.6

        ##Link the path to the executable
        pythonpath=$(pipenv --py)

        ##exit our venture into the project path
        cd "../"

        ##Create variables for our project 
        requirements="./$projectname/requirements.txt"
        vsccreator="./create_vsc_workspace.py"

        ##Format some information regarding the enviroment
        echo "********************************************"
        echo "*  python pipenv virtual enviroment created: "$pythonpath
        echo "*  python version is: " $($pythonpath --version)
        echo "********************************************"

        ##checks if a requirements file exists and installs all required modules if so
        if [ -r $requirements ]; then
            ##Confirmed that the file exists and can be read
            #echo $requirements" exists and can be read"
            if [ ! -z $requirements ]; then
                ##Confirmed that there are requirements in the file
                echo "...the enviroment is being created"
                pipenv install -r $requirements

            ##No requirements in the file  
            else
                echo "empty requirements file... Doing nothing"
            fi

        ##Checks if the requirements file exists
        else
            echo "'"$requirements"' does not exist."
        fi        

        echo $pythonpath
        echo $vsccreator
        echo $projectname 

        ##Launch our python visual studio code workspace creator script
        $pythonpath $vsccreator $projectname

        echo "Enviroment successfully created.."


        #todo git integration
        if [ "$gitinit" = "--git" ]; then
            if echo $validtrue | grep -w $gitbool > /dev/null; then
                echo "Should add a git repo now"
                #git init

                #there shouldn't be files here on a new project but should help integrating old projects 
                #git add "/source/*"

            fi
        fi
        

    ##If the project directory could not be created
    else
        echo "The project folder could not be created"
    fi

fi




## to start a shell process using the pipenv in the Pipenv configuration file in the current directory
#pipenv shell

## to stop the enviroment shell
#exit 



 