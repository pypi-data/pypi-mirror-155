#!/bin/bash

#uninstalling monai

echo "uninstaling monai"

pip uninstall monai

#Deleting Cloned Repo

echo "Deleting cloned Repo"

DIR="MONAI"
if [ -d "$DIR" ]; then
   # Take action if $DIR exists. #
   echo "Deleting cloned directory"
   sudo rm -rf MONAI
else
   echo "Git repository does not exist to Delete"
fi
