#!/usr/bin/env bash

PATH=.:$PATH

#state the version of Python you wish to use
#and the list of source directories at the top level


toget=3.11.0
source_dirs="source/src  source/test"
target_dir=../../

target_python=${target_dir}Python${toget}

current_dir=`pwd`

echo " The target python is $target_python" 


test_dir(){
  echo " $1" 
  if [ -d "$1" ]; then
     echo " exists  "
  else
     echo " does not exist "
    mkdir "$1"
fi
 
}


for name in $source_dirs
do
   test_dir  ${target_dir}$name
done


get_python(){

	command -v git >/dev/null 2>&1 ||
	{ echo >&2 "Git is not installed. Please install..";
	  exit 1
	}

       echo " Git is installed" 

       if [ -d "pyenv" ] 
       then
             echo " Pyenv exists"
       else
           git clone  https://github.com/pyenv/pyenv.git pyenv
       fi 

       pyenv/plugins/python-build/bin/python-build $toget  $target_python
       rm -rf   pyenv

}

test_python(){
 echo " $1" 
  if [ -d "$1" ]; then
     echo "$1 exists  "
  else
     echo "$1 needs to be downloaded"
    get_python
fi
}

test_python ${target_python}

echo "Going to do Update" 
${target_python}/bin/python3 updatescriptfiles.py

echo " Update complete" 

