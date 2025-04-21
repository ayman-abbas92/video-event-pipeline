#!/bin/bash
cd lambda
zip -r ../function.zip lambda_func.py
cd ..
echo "Lambda package created as function.zip"
