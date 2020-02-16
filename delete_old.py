import sys, os
from pathlib import Path
from shutil import copy2, rmtree

LEGACY_FOLDER = 'LEGACY'
DEFAULT_TARGET_FOLDERS = ['oldWindows', 'oldLinux']

def define_target_folders():	
	arguments = sys.argv[1:]
	
	if len(arguments) != 1:
		return DEFAULT_TARGET_FOLDERS
	else:
		return [ arguments[0] ]

def get_filenames(folder):
	for (dirpath, dirnames, filenames) in os.walk(os.getcwd() + '/' + folder):
		return filenames

def convert_file_to_date(file):
	return file[6:16]	

def split_by_date(filenames):
	sorted_files = sorted(filenames)
	lastFile = sorted_files[0]
	lastDate = convert_file_to_date(lastFile)
	result_obj = dict()
	result_obj[lastDate] = [lastFile]
	for currFile in sorted_files:
		currDate = convert_file_to_date(currFile)

		if currDate != lastDate:
			currDateArray = result_obj.get(currDate, [])
			currDateArray.append(currFile)
			result_obj[currDate] = currDateArray

			lastDateArray = result_obj.get(lastDate, [])
			lastDateArray.append(lastFile)
			result_obj[lastDate] = lastDateArray

		lastDate = currDate
		lastFile = currFile


	lastDateArray = result_obj.get(lastDate, [])
	if lastFile not in lastDateArray:
		lastDateArray.append(lastFile)
		result_obj[lastDate] = lastDateArray


	return result_obj


def reassemble_files_as_list(date_file):
	return [ file for date, files in date_file.items() for file in files]

def assert_legacy_folder(subfolder):
	Path(os.getcwd() + '/' + LEGACY_FOLDER + '/' + subfolder).mkdir(parents=True, exist_ok=True)

def copy_files(files, folder):
	source_folder_path = os.getcwd() + '/' + folder
	target_folder_path = os.getcwd() + '/' + LEGACY_FOLDER + '/' + folder

	for file in files:
		copy2(source_folder_path + '/' + file, target_folder_path)
	print("INFO: successfully copied")



def delete_old(folder):
	rmtree(os.getcwd() + '/' + folder)
	os.mkdir(os.getcwd() + '/' + folder)

def main():
	target_folders = define_target_folders()
	for folder in target_folders:
		filenames = get_filenames(folder)
		if filenames == None: #Folder not found
			print("[*] Error: folder", folder, "not found!")
			continue
		date_file = split_by_date(filenames)
		files_to_copy = reassemble_files_as_list(date_file)
		assert_legacy_folder(folder)
		copy_files(files_to_copy, folder)
		delete_old(folder)


if __name__ == '__main__':
	main()
