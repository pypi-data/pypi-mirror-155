#!/bin/bash

echo -e "Initializing the directory..."
terraform14 init

echo -e "\nFormating the configuration..."
terraform14 fmt

echo -e "\nValidating the configuration..."
terraform14 validate
