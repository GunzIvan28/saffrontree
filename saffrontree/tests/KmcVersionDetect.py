import os
import re
import logging
from subprocess import check_output

'''The syntax has changed between version 2 and 3 so detect which major version it is'''
class KmcVersionDetect:
	def __init__(self, verbose):
		self.verbose = verbose
		self.kmc_version = self.find_version()
	
	'''Run the kmc command which contains the version string at the top'''
	'''K-Mer Counter (KMC) ver. 2.3.0 (2015-08-21)'''
	'''K-Mer Counter (KMC) ver. 3.0.0 (2017-01-28)'''
	def find_version(self):	
		self.logger.info("Detecting the version of KMC" )
		kmc_output = check_output(["kmc"])
		version_search_results = re.search("ver\. ([\d]+\.[\d]+\.[\d]+) ", kmc_output)
		if version_search_results:
			return search_results.group(1)
		else:
			return '0.0.0'
		
	'''extract out the components of the version'''
	def __version_search__(self, group):
		search_results = re.search("([\d]+)\.([\d]+)\.([\d]+)", self.kmc_version)
		if search_results:
			return search_results.group(group)
		else:
			return 0
		
	def major_version(self):
		return self.__version_search__(1)
		
	def full_version(self):
		return self.__version_search__(0)

		