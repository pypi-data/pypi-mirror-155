#!/bin/bash

clean_cmd="tf14 --clean"

echo -e "Creating infrastructure..."
terraform14 apply

echo -e "\nInspecting state..."
terraform14 show

echo -e "\nRemember to clean unwanted files by running \"${clean_cmd}\""