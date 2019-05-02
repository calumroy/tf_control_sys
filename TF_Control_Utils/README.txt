# This directory contains some useful funcitons I made.

# To include these funcitons in a jupyter notebook or another python script use the following code to add to the system path.
# Note you will need to change this so it points form the current dir to this directory.

# If you had the following dir structure
        meta_project
            project1
                __init__.py
                lib
                    module.py
                    __init__.py
            notebook_folder
                notebook.jpynb


import os
import sys
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)
    
    
# This allows you to import the desired function from the module hierarchy:


from project1.lib.module import function
# use the function normally
function(...)

E.g we may use for our funciton 
from TF_Control_Utils.nautiContToDis import nautiContToDis





# Another solution is to  do this

A project hierarchy as such:

├── ipynb
│   ├── 20170609-Examine_Database_Requirements.ipynb
│   └── 20170609-Initial_Database_Connection.ipynb
└── lib
    ├── __init__.py
    └── postgres.py
And from 20170609-Initial_Database_Connection.ipynb:

    In [1]: cd ..

    In [2]: from lib.postgres import database_connection
This works because by default the Jupyter Notebook can parse the cd command. Note that this does not make use of Python Notebook magic. It simply works without prepending %bash.

Considering that 99 times out of a 100 I am working in Docker using one of the Project Jupyter Docker images, the following modification is idempotent

    In [1]: cd /home/jovyan

    In [2]: from lib.postgres import database_connection