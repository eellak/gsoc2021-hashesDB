from create import is_valid_db_path, create as create_create
from os.path import abspath
from os import getcwd

class App:
	#Class initialization
	def __init__(self, used_database_path_param = None):

		#By default our app runs sequentially
		self.max_threads = 1

		#Set the working directory
		self.working_directory = getcwd()

		if used_database_path_param == None:
			#If no specific database-to-use is set, set the appropriate flag to False.
			self.database_used_flag = False
			self.used_database_path = None
		else:
			#If a specific database-to-use is set, try to use it
			db_absolute_path = abspath(used_database_path_param)

			try:
				self.use(db_absolute_path)
			except Exception as e:
				#If you succeeded in using a database, set the appropriate flag to False, and print an error message.
				self.database_used_flag = False
				self.used_database_path = None
				print(e)
			else:
				#This will probably be moved to the self.use() method
				#If you succeeded in using a database, set the appropriate flag to True.
				self.database_used_flag = True
				self.used_database_path = db_absolute_path

	def help(self, command_param = None):
		#help command implementation here...
		pass

	def version(self):
		#version command implementation here...
		pass

	def about(self):
		"""def about(self):
		Result: Prints information about the project."""
		print("------------------------------------------------------------------------------------------------------------------------------------------")
		print("""
		hashesDB is a command line tool that helps users manage a database of hashes of files. It provides several database
		functionalities such as insertion, deletion and searching.It also supports fuzzy hashing, a hashing technique based
		on Locality-Sensitive Hashing that makes it possible to perform similarity	checking with the use of hashing.""")
		print("""
		The development of this project began by the Open Technologies Alliance(GFOSS) during the Google Summer of Code 2021
		program. hashesDB is licenced under the GPL-3.0 License.""")
		print("""
		If you want to report an issue or you are interested in contributing, visit:
		https://github.com/eellak/gsoc2021-hashesDB
		""")
		print("------------------------------------------------------------------------------------------------------------------------------------------")

	def exit(self):
		#exit command implementation here...
		#__del__ constructor will be called in here
		pass

	def threads(self,max_threads_number_parameter):
		"""def threads(self,max_threads_number_parameter):
		Parameters: max_threads_number_parameter - sets the maximum number of threads that can be used at parallel scanning

		Result: The method sets self.max_threads = max_threads_number_parameter

		Errors: Throws an error if the parameter is not an integer or if the parameter is not greater than zero."""
		try:
			max_threads_number = int(max_threads_number_parameter)
		except (TypeError, ValueError) as e:
			print("Error: max_threads parameter should be an integer.")
		else:
			if max_threads_number > 0:
				self.max_threads = max_threads_number
			else:
				print("Error: max_threads parameter should be greater than zero.")

	def create(self, path_param, overwrite_flag = False):
		create_create(path_param, overwrite_flag)

	def use(self, path_param):
		#use command implementation here...
		pass

	def unuse(self):
		#unuse command implementation here...
		pass

	def status(self):
		if not self.database_used_flag:
			#If there is no database currently used:
			print("No database is currently active. You can choose a database to manage with the 'use database_path' command.\n")
		else:
			#If there is a database currently used, check if there are unsaved changes waiting to be commited
			print(f"Database currently used: {self.used_database_path}\n")
			if self.unsaved_changes_flag:
				print("There are unsaved changes made regarding this database. You can commit them to the database with the 'save' command.")
			else:
				print("There are no unsaved changes made regarding this database.")

		#Print maximum threads
		print(f"Number of maximum threads allowed: {self.max_threads}\n")

		#Print maximum threads
		print(f"Working directory: {self.working_directory}\n")		

	def schema(self):
		#schema command implementation here...
		pass

	def import_db(self, import_database_path_param, import_file_path_param, import_file_format_param, overwrite_flag = False):
		#import command implementation here...
		pass

	def export_db(self, export_database_path_param, export_file_path_param, export_file_format_param, overwrite_flag = False):
		#export command implementation here...
		pass
