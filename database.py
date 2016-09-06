#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

home_dir = os.path.expanduser("~");
app_dir = home_dir+"/.pilnuj";
db_file = "sqlite:///"+app_dir+"/baza.sql"

if(not os.path.exists(app_dir)):
	os.makedirs(app_dir);
                
class Pliki(Base):
	__tablename__="pliki";
	abs_path = Column(String, primary_key=True);
	last_mod_time = Column(Integer);

class Database:
	def __init__(self):
		self.engine = create_engine(db_file)
		self.engine.raw_connection().connection.text_factory = str

		self.Session = sessionmaker(bind=self.engine)
		self.session = self.Session()
		Base.metadata.create_all(self.engine) # to tworzy bazę, jeśli nie istnieje

	def add(self, filename):

		abs_path = os.path.abspath(filename);
		last_mod_time = int(os.path.getmtime(abs_path));

		#print(filename, abs_path, last_mod_time)

		entry = Pliki();
		entry.abs_path = abs_path;
		entry.last_mod_time = last_mod_time;

		self.session.merge(entry);
		self.session.commit();
		
	def add_all(self):
		changed = self.check();
		for abs_path in changed:
			if(os.path.exists(abs_path)):
				self.add(abs_path);

	def check(self):
		changed=[];
		entries = self.session.query(Pliki).all();
		if entries:
			for entry in entries:
				if(os.path.exists(entry.abs_path)):
					last_mod_time = int(os.path.getmtime(entry.abs_path));
					if(last_mod_time != entry.last_mod_time):
						changed.append(entry.abs_path);
				else:
					changed.append(entry.abs_path);
		return changed;

	def list(self):
		entries = self.session.query(Pliki).all();
		if(entries):
			lista=[entry.abs_path for entry in entries];
		else:
			lista=[];
		return lista;

