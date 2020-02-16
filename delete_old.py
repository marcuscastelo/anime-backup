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

def split_by_date(filenames):


def main():
	target_folders = define_target_folders()
	for folder in target_folders:
		filenames = get_filenames(folder)
		date_file_array = split_by_date(filenames)
		print(date_file_array)


if __name__ == '__main__':
	main()
