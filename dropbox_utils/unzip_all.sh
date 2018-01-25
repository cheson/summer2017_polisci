#!/bin/bash

# AUTHOR: JASON CHEN (cheson@stanford.edu)
# Date: July 24, 2017
# This short shell script can be copied into any folder and it will unzip all
# the zip files within that folder into new folders with the same name as the 
# original zip. 
# It can be run by calling the following terminal command: 
# ./unzip_all.sh

# REFERENCES + NOTES: 

#https://askubuntu.com/questions/518370/extract-several-zip-files-each-in-a-new-folder-with-the-same-name-via-ubuntu-t
#http://wiki.bash-hackers.org/syntax/pe
#http://www.tuxarena.com/2014/11/bash-10-examples-of-parameter-expansion/

#tbh I don't quite understand the parameter expansion and the _ at the end

find . -name "*.zip" -exec sh -c 'unzip {} -d "${1%.*}"' _ {} \; 
