#!/bin/bash

# Remove .pyc files
find . -name '*.pyc' -exec rm {} +

# Remove empty directories
find . -type d -empty -delete