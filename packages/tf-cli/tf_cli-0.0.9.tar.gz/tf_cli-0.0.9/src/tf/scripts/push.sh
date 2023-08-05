#!/bin/bash

clean_cmd="tf --clean"

echo -e "Creating infrastructure..."
terraform apply

echo -e "\nInspecting state..."
terraform show

echo -e "\nRemember to clean unwanted files by running \"${clean_cmd}\""