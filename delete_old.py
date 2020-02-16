import sys, os

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
	return [[file for file in files] for date, files in date_file.items()]


def main():
	target_folders = define_target_folders()
	for folder in target_folders:
		filenames = get_filenames(folder)
		if filenames == None: #Folder not found
			print("[*] Error: folder", folder, "not found!")
			continue
		date_file = split_by_date(filenames)
		print(reassemble_files_as_list(date_file))


if __name__ == '__main__':
	main()
