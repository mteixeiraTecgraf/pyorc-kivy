#!/bin/bash

python3 -m virtualenv kivy_venv 
source kivy_venv/bin/activate
python -m pip install -I Cython
python3 -m pip install "kivy[base]" kivy_examples


#python kivy_venv/share/kivy-examples/demo/showcase/main.py 


#cd kivy_venv/share/kivy-examples/android/compass/
