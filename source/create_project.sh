##################################
#  # File created by Alex Zettler
#  # pipenv startup script
##################################

##Get the project name from arguements
projectname=$1
gitinit=$2
gitbool=$3

##Check if arguement is blank
if [ "$projectname" = "" ]; then
    echo "No arguement given. Please pass the project name as an arguement"

##If arguement isn't blank
else
    pip install pipenv
    pipenv --python 3.6
    pythonpath=$(pipenv --py)
    vsccreator="create_vsc_workspace.py"

    echo "Shell shit: " $pythonpath $vsccreator $projectname

    ##Launch our python visual studio code workspace creator script
    $pythonpath $vsccreator $projectname
    #pipenv --rm

    echo "Enviroment successfully created.."

    #todo git integration
    #if [ "$gitinit" = "--git" ]; then
    #    if echo $validtrue | grep -w $gitbool > /dev/null; then
    #        echo "Should add a git repo now"
    #        #git init
    #        #there shouldn't be files here on a new project but should help integrating old projects 
    #        #git add "/source/*"
    #    fi
    #fi


fi




## to start a shell process using the pipenv in the Pipenv configuration file in the current directory
#pipenv shell

## to stop the enviroment shell
#exit 



 