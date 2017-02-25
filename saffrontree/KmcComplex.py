'''Take in trait and non trait databases and do a complex filter on the kmers'''

import os
import tempfile
import subprocess
import logging
import shutil
from saffrontree.SampleData import SampleData

		

class KmcComplex:
	def __init__(self,output_directory, threads, min_kmers_threshold, trait_samples, nontrait_samples, action):
		self.logger = logging.getLogger(__name__)
		self.output_directory = output_directory
		self.threads = threads
		self.min_kmers_threshold = min_kmers_threshold
		self.trait_samples = trait_samples
		self.nontrait_samples = nontrait_samples
		self.action = action
		
		self.temp_working_dir = tempfile.mkdtemp(dir=output_directory)

	def sample_definition_line(self, sample):
		return ' '.join([sample.basename.replace('#','_'), '=', sample.database_name])	
		
	def write_config_file(self, filename, input_section, output_section, output_parameters):
		self.logger.info("Creating config file for 'complex' task")
		with open(filename, 'w') as complex_config_file:
			complex_config_file.write('INPUT:\n')
			complex_config_file.write(input_section)
			complex_config_file.write('OUTPUT:\n')
			complex_config_file.write( output_section + '\n')
			complex_config_file.write('OUTPUT_PARAMS:\n')
			complex_config_file.write( output_parameters + '\n')
		
	def create_config_files(self):
		traits_config_file = os.path.join(self.temp_working_dir, 'traits_config_file')
		self.write_config_file(traits_config_file, self.sample_definitions_str(), self.trait_samples_to_set_operation_str(),  self.output_parameters_str())
		
		nontraits_config_file = os.path.join(self.temp_working_dir, 'nontraits_config_file')
		self.write_config_file(nontraits_config_file, self.sample_definitions_str(), self.nontrait_samples_to_set_operation_str(),  self.output_parameters_str())
		
		combined_config_file = os.path.join(self.temp_working_dir, 'combined_config_file')
		self.write_config_file(combined_config_file, 'set1 = traits\nset2 = nontraits\n', 'result = set1-set2',  self.output_parameters_str())

	def sample_definitions_str(self):
		sample_definition_lines = ''
		
		for set_of_samples in [self.trait_samples, self.nontrait_samples]:
			for sample in set_of_samples:
				sample_definition_lines += self.sample_definition_line(sample) + "\n"
		return sample_definition_lines
		
	def result_database(self):
		return os.path.join(self.temp_working_dir, 'result')

	def output_parameters_str(self):
		return ' '.join(['-ci'+str(self.min_kmers_threshold)])

	def trait_samples_to_set_operation_str(self):
		trait_basenames = []
		for sample in self.trait_samples:
			trait_basenames.append(sample.basename.replace('#','_'))
	
		trait_set_operation = '+'
		if self.action == 'intersection':
			trait_set_operation = '*'
	
		set_operation_str  = 'traits = '+ trait_set_operation.join(trait_basenames) 
		return set_operation_str
		
	def nontrait_samples_to_set_operation_str(self):
		nontrait_basenames = []
		for sample in self.nontrait_samples:
			nontrait_basenames.append(sample.basename.replace('#','_'))
	
		set_operation_str = 'nontraits = ' + '+'.join(nontrait_basenames)
		return set_operation_str
	
	def kmc_complex_command(self, config_file):
		return " ".join(['kmc_tools', 
			'-t' +  str(self.threads),
			'complex',
			config_file ])
	
	def run(self):
		self.create_config_files()
		self.logger.info("Running KMC complex command")
		# kmc_tools doesnt allow for paths in the output database name (even though they say they do) so change working directory
		# to prevent temp files polluting CWD
		
		original_cwd = os.getcwd()
		os.chdir(self.temp_working_dir)
		subprocess.call(self.kmc_complex_command('traits_config_file'), shell=True)
		subprocess.call(self.kmc_complex_command('nontraits_config_file'), shell=True)
		subprocess.call(self.kmc_complex_command('combined_config_file'), shell=True)
		os.chdir(original_cwd)
		
	def cleanup(self):
		shutil.rmtree(self.temp_working_dir)
		