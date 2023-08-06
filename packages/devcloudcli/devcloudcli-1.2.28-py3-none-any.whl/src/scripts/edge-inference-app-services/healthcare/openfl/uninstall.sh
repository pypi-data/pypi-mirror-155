#!/bin/bash

#uninstalling openfl
echo "uninstaling openfl"

pip uninstall openfl

#Deleting Cloned Repo

echo "Deleting cloned Repo"

DIR="openfl"
if [ -d "$DIR" ]; then
   # Take action if $DIR exists. #
   echo "Deleting cloned directory"
   sudo rm -rf openfl
else
   echo "Git repository does not exist to Delete"
fi
