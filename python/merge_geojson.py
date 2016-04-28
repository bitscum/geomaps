#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  merge_geojson.py
#  
#  Written by werner <werner@Baltar>
#
# This program merges polygons in a geojson file, based on
# 2 merging files.
# It uses ogr2ogr to perform the merge operation.
#

import argparse         #necessary for parsing arguments @ command line
import os, subprocess   
import json


# define and parse the arguments of the program
parser = argparse.ArgumentParser(description='merge geojson files')
parser.add_argument('-p', '--path', help= 'Base file path', required=True)
parser.add_argument('-i','--input', help='Input file name',required=True)
parser.add_argument('-o','--output',help='Output file name', required=True)
parser.add_argument('-n', '--name', help='Name member file name', required = False)
parser.add_argument('-d', '--descr', help='Description member file name', required=False)
args = parser.parse_args()
#

def main():
	d = {}
	namefile = os.path.join(args.path, args.name)
	with open(namefile) as f:
		for line in f:
			(key, val) = line.rstrip("\n").split("\t")
			d[key] = val            #d{} contains the old and new "Name" properties
        
	e = {}
	descrfile = os.path.join(args.path, args.descr)
	with open(descrfile) as f:
		for line in f:
			(key, val) = line.rstrip("\n").split("\t")
			e[key] = val            #e{} contains the new "Name" and "Description" properties
	
	inputfile = os.path.join(args.path, args.input)
	with open(inputfile) as f:
		data = json.load(f)              #read input geojson file

	for feature in data['features']:        #now replace the old values with the new ones
		key = (feature['properties']['Name'])
		if key in d:
			(feature['properties']['Name']) = d.get(key)
			(feature['properties']['Description']) = e.get(d.get(key)) 
	
	outputfile = os.path.join(args.path, args.output)	
	with open(outputfile, 'w') as outfile:
		json.dump(data, outfile)        #write temp geojson file
	merged = '%s%s' % ('merged_',args.output)
	out = os.path.join(args.path, merged)
	subprocess.run(['ogr2ogr', '-f',  'GeoJSON', #run ogr2ogr
					out, outputfile, 
					'-dialect', 'sqlite', 
					'-sql', 'SELECT Name as Name, Description as Description, ST_Union(geometry) as geometry FROM OGRGeoJSON GROUP BY Name'])	
			
if __name__ == '__main__':
	main()

