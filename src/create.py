from sqlalchemy import create_engine, inspect
from os.path import split, splitext, abspath, isdir, isfile, basename
from os import remove

from initialize_database import initialize_db
from table_classes import *

def create(database_path_parameter, overwrite_flag = False):
	"""
	Description
	-----------
	Creates a hashesDB database located at database_path_parameter, if the given path is a .db file and the directory that contains it exists.
	If the file already exists, it is overwritten if overwrite_flag = True. Otherwise, an error is printed.

	Parameters
	-----------
	database_path_parameter: string
		An absolute path that specifies where the new database will be located. This has to be a path to a .db file.
	
	overwrite_flag - boolean, optional
		In case a .db file exists at the given path, then if overwrite_flag = True the file will be overwritten.
		Otherwise an error message will be printed.

	Results
	-----------
	Returns True if the database was created and False otherwise"""

	#Check if the directory exists AND if the file is a .db file.
	if not is_valid_db_path(database_path_parameter):
		return False

	#Handle .db file overwriting: if overwrite_param = True then delete the existing file, otherwise print an error message
	if isfile(database_path_parameter):
		if overwrite_flag:
			delete_file(database_path_parameter)
		else:	
			print(f"Error: File {database_path_parameter} already exists.")
			print("Use -overwrite flag to allow overwriting.")
			return False

	#Try to create the database
	try:
		create_database(database_path_parameter)
	except RuntimeError as e:
		print(e)
		return False
	
	return True


def is_valid_db_path(database_path_parameter):
	"""
	Description
	-----------
	Checks that a given path refers to a file with a .db extension located an existing directory.
	The directory must exist but the .db file may not exist.

	Parameters
	-----------
	database_path_parameter: string
		A path(relative or absolute) that specifies where the new database will be located. This has to be a path to a .db file.

	Results
	-----------
	Returns True if database_path_parameter is a .db file located in an existing directory. Otherwise it returns False."""
	
	#Convert parameter to absolute path, in case it is a relative path.
	database_path = abspath(database_path_parameter)

	#Check if the direcory exists.
	#If the direcotry does not exist, then sqlite will throw an error when it will try to create the new .db format.
	dir, basename = split(database_path)
	if not isdir(dir):
		print(f"Error: Directory {dir} does not exist.")
		return False
	
	#Check if the file has a .db extension.
	filename, extension = splitext(basename)
	if extension != ".db":
		print(f"Error: File {basename} is not a .db file.")
		return False

	return True
		
def delete_file(database_path_parameter):
	"""
	Description
	-----------
	Deletes a .db database file located at database_path_parameter. 
	Prints an error message if the path refers to a directory or a non-existing file

	Parameters
	-----------
	database_path_parameter: string
		A path(relative or absolute) that specifies where the new database will be located. This has to be a path to a .db file."""
	
	#Convert the path to absolute path in case it is relative path.
	database_path = abspath(database_path_parameter)
	
	#Try to remove the file
	try:
		remove(database_path)
	except IsADirectoryError:
		print(f"Overwrite Error: {database_path} is a directory.")
	except FileNotFoundError:
		print(f"Overwrite Error: {database_path} is not found.")
	except:
		print(f"An unexpected error occured while deleting file {database_path}.")

def create_database(database_path_parameter):
	"""
	Description
	-----------
	Compares the schema of a database with the expected schema of a hashesDB database, in order to find out if a database is a hashesDB database.

	Parameters
	-----------
	database_path_parameter: string
		An absolute path that specifies where the new database will be located. This has to be a path to a .db file.

	Raises
	-----------
	Raises a RuntimeError if the database we try to create already exists, since overwriting should be handled before calling this function
	Raises a RuntimeError if the creation of the database fails."""

	#Check if a file already exists at the given path.
	if isfile(database_path_parameter):
		raise RuntimeError("Error: Tried to create a database using the path of an already existing file")

	engine_url = "sqlite:///" + database_path_parameter

	#Create a database. The .db file will be automatically created after the execution of engine.connect() 
	#After the creation, the DB_INFORMATION, SCAN_CODE and HASH_FUNCTION tables will be initialized by initialize_db
	engine = create_engine(engine_url, echo = False)
	with engine.connect() as conn:
		#Try to create the tables and to initialize them
		Base.metadata.create_all(engine)
		initialize_db(engine, database_path_parameter)