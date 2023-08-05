#!/bin/bash

echo -e "Initializing the directory..."
terraform init

echo -e "\nFormating the configuration..."
terraform fmt

echo -e "\nValidating the configuration..."
terraform validate
