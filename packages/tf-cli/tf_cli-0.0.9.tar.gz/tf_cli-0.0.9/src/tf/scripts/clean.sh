#!/bin/bash

remove_files=(".terraform" ".terraform.lock.hcl") 

echo "Performing terraform clean..."

echo "Removing \"${remove_files[*]}\" files"

rm -rf ${remove_files[*]}
