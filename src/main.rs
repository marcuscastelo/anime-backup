use serde::{Deserialize, Serialize};
use std::{fs::{read_to_string, write, File}, io::{Read, Write}};

//Global variables
const SETTINGS_FILENAME: &str = "settings.toml";
const OS_NAME: &str = "Windows";

fn load_settings() -> Settings {
    // Create settings file path, starting from CWD
    let settings_file_path = std::env::current_dir().unwrap().join(SETTINGS_FILENAME);

    //Check if settings file exists
    let exists = std::fs::metadata(&settings_file_path).is_ok();

    //If settings does not exist, create it
    if !exists {
        println!("Settings file does not exist, creating it...");
        let settings = Settings {
            OLD_FOLDER: String::from("old") + OS_NAME,
            MAX_AGE: 30,
            ORIGINAL_FILE_BASENAME: String::from("anilist"),
            ORIGINAL_FILE_EXTENSION: String::from(".anl"),
        };
        let settings_string = toml::to_string(&settings).unwrap();
        let settings_bytes = settings_string.into_bytes();
        write(&settings_file_path, settings_bytes).expect("Failed to create settings file");
    }

    
    // If it exists, open it in read it to a string
    let settings_file_contents: String = read_to_string(&settings_file_path).expect("Failed to read settings file");
    
    // Deserialize the string into a Settings struct
    return toml::from_str(&settings_file_contents).unwrap();
}

fn open_original_file(settings: &Settings) -> std::io::Result<File> {
    let mut target_file_path = settings.ORIGINAL_FILE_BASENAME.clone();
    target_file_path.push_str(&settings.ORIGINAL_FILE_EXTENSION);

    return File::open(target_file_path)
}

fn create_new_file(settings: &Settings) -> std::io::Result<File> {
    let mut new_file_path = settings.OLD_FOLDER.clone();

    new_file_path.push_str("/");
    std::fs::create_dir_all(&new_file_path).expect("Failed to create new folder");

    new_file_path.push_str(&settings.ORIGINAL_FILE_BASENAME);
    
    //Get current date
    let current_date = chrono::Local::now();
    let current_date_string = current_date.format("%Y-%m-%d-T-%H-%M-%S").to_string();

    new_file_path.push_str("-");
    new_file_path.push_str(&current_date_string);
    new_file_path.push_str(&settings.ORIGINAL_FILE_EXTENSION);

    return File::create(new_file_path);
}

fn make_backup(original_file: &mut File, new_file: &mut File) -> std::io::Result<()> {
    let mut original_file_contents = String::new();
    original_file.read_to_string(&mut original_file_contents)?;

    let new_file_contents = original_file_contents.clone();
    new_file.write(new_file_contents.as_bytes())?;

    return Ok(());
}

fn main() {
    println!("Hello, world!");
    let settings: Settings = load_settings();

    let mut original_file = 
        match open_original_file(&settings) {
            Ok(file) => file,
            Err(e) => panic!("Failed to open target file: {}", e),
        };

    let mut new_file = create_new_file(&settings).expect("Failed to create new file for backup");
    
    make_backup(&mut original_file, &mut new_file).expect("Failed to make backup");

    println!("Backup complete!");
}

// Structs with Deserialize trait
#[derive(Debug)]
#[derive(Deserialize)]
#[derive(Serialize)]
struct Settings {
    OLD_FOLDER: String,
    MAX_AGE: u64,
    ORIGINAL_FILE_BASENAME: String,
    ORIGINAL_FILE_EXTENSION: String,
}