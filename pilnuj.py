#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

from database import Database



def print_usage(cmd=None):
	print("Usage:\n pilnuj.py add <filename>\n pilnuj.py check\n pilnuj.py list\n\n");



if(len(sys.argv)<2):
	print_usage();
	sys.exit(2);

cmd = sys.argv[1];


db = Database();

if(cmd=="add"):
	if(len(sys.argv) != 3):
		print_usage(cmd);
		sys.exit(2);


	filename = sys.argv[2];
	if(os.path.exists(filename)):
		db.add(filename);
	else:
		print("File does not exist:" + filename);


if(cmd=="check"):
	if(len(sys.argv) != 2):
		print_usage(cmd);
		sys.exit(2);

	for abs_path in db.check():
		print(abs_path);

if(cmd=="list"):
	if(len(sys.argv) != 2):
		print_usage(cmd);
		sys.exit(2);

	for abs_path in db.list():
		print(abs_path);

