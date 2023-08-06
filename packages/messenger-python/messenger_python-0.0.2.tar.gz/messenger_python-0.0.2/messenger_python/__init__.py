"""
Copyright (c) 2022, Miles Frantz
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
"""

import os, sys, json, hashlib, pickle

class wrapper():
	def __init__(self, latestStep: str, localDataFile:str=None, load: bool = False):
		self.setlatestStep = latestStep
		self.call_path = []
		self.local = localDataFile or "writing_temp_output.csv"
		self.current_results = None

	def __getitem__(self, key):
		if not isinstance(key, str) or key not in self.current_results.keys():
			return None
		return self.current_results[key]

	def __setitem__(self, key, value):
		if not isinstance(key, str):
			return None
		self.current_results[key] = value

	def __enter__(self):
		print(f"Starting at step {self.setlatestStep}")
		if os.path.exists(self.local):
			if self.local.endswith(".pkl"):
				with open(self.local, "rb") as reader:
					self.current_results = pickle.load(reader)
			elif self.local.endswith(".csv"):
				with open(self.local, "r") as reader:
					self.current_results = json.load(reader)
			os.remove(self.local)
		else:
			self.current_results = {
				'CallChain':[]
			}

		self['LatestStep'] = self.setlatestStep
		self['CallChain'] += [self.setlatestStep]
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		try:
			os.remove(self.local)
		except:
			pass

		def json_cap(obj):
			if isinstance(obj,set):
				return list(obj)
			return TypeError

		if self.local.endswith(".pkl"):
			with open(self.local, "wb+") as output_file:
				pickle.dump(self.current_results, output_file)
		elif self.local.eendswith(".csv"):
			with open(self.local, "w+") as writer:
				json.dump(self.current_results, writer, default=json_cap)

		print(f"Exiting at step {self.setlatestStep}")
		return self

	@property
	def clean(self):
		for ext in [".xlsx", ".csv", ".png", ".jpg", ".json", ".puml", ".svg"]:
			try:
				os.system(f"yes|rm -r *{ext}")
			except:
				pass
		return

	def keys(self):
		return self.current_results.keys()

	@property
	def hash(self):
		current_num = 0
		current_file = f"temp_file_{current_num}.json"
		while os.path.exists(current_file):
			current_num += 1
			current_file = f"temp_file_{current_num}.json"
		
		def json_cap(obj):
			if isinstance(obj,set):
				return list(obj)
			return TypeError

		with open(current_file, "w+") as writer:
			json.dump(self.current_results, writer, default=json_cap)

		BUF_SIZE = 65536
		sha512 = hashlib.sha512()

		with open(current_file,'rb') as reader:
			while True:
				data = reader.read(BUF_SIZE)
				if not data:
					break

				sha512.update(data)
		
		try:
			os.remove(current_file)
		except:
			pass

		return str(sha512.hexdigest())

	def values(self):
		return self.current_results.values()

	def items(self):
		return self.current_results.items()

	def msg(self, string: str = ""):
		string = string or ""
		print(string)

	def get_last_working_step(self, get_last: int = 2):
		synthed, ktr = dc(self['CallChain']), 0
		synthed.reverse()
		for step in synthed:
			ktr += 1
			if ktr == get_last:
				return step
		return None
