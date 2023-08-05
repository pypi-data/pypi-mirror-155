# -*- coding: utf-8 -*-
"""
Created on Mon Feb 28 13:14:53 2022

@author: PURUSHOT

Add user material and extinction rule to the json object

"""
def start():
    import sys
    import argparse
    from lauetoolsnn.utils_lauenn import resource_path
    import json
    
    parser = argparse.ArgumentParser(description="Add user material to laueNN",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-n", "--name", required=True, help="User string for the material")
    parser.add_argument("-l", "--lattice", required=True, nargs=6, type=float, help="Unit cell lattice parameters of unit cell in the format a b c alpha beta gamma")
    parser.add_argument("-e", "--extinction", required=True, help="String for material extinction; if want sapce group rules provide the spacegroup number")
    args = parser.parse_args()
    config = vars(args)
    print(config)
    
    mat_name = config["name"]
    lat = config["lattice"]
    ext = config["extinction"]
    
    
    filepath = resource_path('xxxx')
    filepathmat = filepath[:-4] + "lauetools//" + 'material.json'
    filepathext = filepath[:-4] + "lauetools//" + 'extinction.json'
    
    print(filepathext)
    print(filepathmat)
    # ## If material key does not exist in Lauetoolsnn dictionary
    # ## you can modify its JSON materials file before import or starting analysis
    
    ## Load the json of material and extinctions
    with open(filepathmat,'r') as f:
        dict_Materials = json.load(f)
    with open(filepathext,'r') as f:
        extinction_json = json.load(f)
        
    ## Modify/ADD the dictionary values to add new entries
    dict_Materials[mat_name] = [mat_name, lat, ext]
    extinction_json[ext] = ext

    ## dump the json back with new values
    with open(filepathmat, 'w') as fp:
        json.dump(dict_Materials, fp)
    with open(filepathext, 'w') as fp:
        json.dump(extinction_json, fp)
        
    print("New material successfully added to the database")
