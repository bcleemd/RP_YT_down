# pip install google-generativeai python-dotenv eyed3

import os
import argparse
import logging
from dotenv import load_dotenv
from google.generativeai import configure, GenerativeModel
import json
import sys
from collections import defaultdict

import eyed3

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_title_artist_from_filenames_batch(filenames, model):
    """
    Extracts music titles and artists from a batch of filenames using the GEMINI API.
    Expects a JSON response.
    """
    if not filenames:
        return {}

    prompt = "Extract the song title and artist name from each of the following filenames. " \
             "Respond with a JSON array where each object has 'original_filename', 'title', and 'artist'. " \
             "Please remove words like 'Official Video' or 'Lyrics' from the title"\
             "If you cannot determine the title or artist for a filename, set its 'title' and 'artist' to null. " \
             "Ensure the output is a valid JSON array.\n\n" \
             "Filenames:\n" + "\n".join([f"- {fn}" for fn in filenames]) + "\n\n" \
             "Example JSON format for one item:\n" \
             "{ \"original_filename\": \"Example Song - Artist Name.mp3\", \"title\": \"Example Song\", \"artist\": \"Artist Name\" }"

    try:
        logging.info(f"Calling Gemini API for {len(filenames)} files...")
        response = model.generate_content(prompt)
        text_response = response.text.strip()
        
        # Handle cases where the response is wrapped in ```json ... ```
        if text_response.startswith("```json") and text_response.endswith("```"):
            text_response = text_response[7:-3].strip()

        parsed_data = json.loads(text_response)
        
        results = {}
        for item in parsed_data:
            original_fn = item.get("original_filename")
            title = item.get("title")
            artist = item.get("artist")
            if original_fn:
                results[original_fn] = {"title": title, "artist": artist}
        return results

    except json.JSONDecodeError as e:
        logging.error(f"Failed to parse JSON response from Gemini API: {e}\nResponse: {text_response}")
        return {}
    except Exception as e:
        logging.error(f"Error calling Gemini API for batch processing: {e}")
        return {}


def update_id3_tags(mp3_path, title, artist):
    """
    Updates the ID3 tags (title and artist) of an MP3 file.
    """
    try:
        audiofile = eyed3.load(mp3_path)
        if audiofile is None:
            logging.warning(f"Could not load ID3 tags for: {mp3_path}. File might be corrupted or not a valid MP3.")
            return False
        if audiofile.tag is None:
            audiofile.initTag()
        
        # Only update if the tag value is different or if it's currently None
        if audiofile.tag.title != title or audiofile.tag.artist != artist:
            audiofile.tag.title = title
            audiofile.tag.artist = artist
            audiofile.tag.save()
            logging.info(f"Successfully updated ID3 tags for '{os.path.basename(mp3_path)}': Title='{title}', Artist='{artist}'")
            return True
        else:
            logging.info(f"ID3 tags for '{os.path.basename(mp3_path)}' are already up to date. No changes made.")
            return False
    except Exception as e:
        logging.error(f"Error updating ID3 tags for '{mp3_path}': {e}")
        return False

def rename_mp3_files(root_dir, recursive, model, delimiter, force_tag_update):
    """
    Finds and renames MP3 files in the specified directory, and updates their ID3 tags.
    """
    mp3_files_to_process = [] # List of MP3 file base names (without extension) to process
    original_filepaths_map = {} # Maps base name to a list of full paths (for handling duplicates)

    # Step 1: Collect all MP3 file paths
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if not recursive and dirpath != root_dir:
            continue # If not recursive, only process the current folder

        for filename in filenames:
            if filename.lower().endswith('.mp3'):
                base_name_without_ext = os.path.splitext(filename)[0]
                mp3_files_to_process.append(base_name_without_ext)
                # Store full paths, as the same base_name_without_ext might exist in different folders
                if base_name_without_ext not in original_filepaths_map:
                    original_filepaths_map[base_name_without_ext] = []
                original_filepaths_map[base_name_without_ext].append(os.path.join(dirpath, filename))

        if not recursive and dirpath == root_dir:
            break # If not recursive, stop after processing the root directory

    if not mp3_files_to_process:
        logging.info(f"No MP3 files found in '{root_dir}'. (Recursive search: {recursive})")
        return

    # Call GEMINI after removing duplicate base names
    unique_basenames = list(set(mp3_files_to_process))
    renaming_suggestions = get_title_artist_from_filenames_batch(unique_basenames, model)
    # renaming_suggestions: {original_filename_without_ext: {'title': ..., 'artist': ...}}
    
    # Step 2: Preview the changes to be made
    changes_by_folder = defaultdict(list) # Dictionary to store changes per folder
    
    for base_name in unique_basenames:
        if base_name not in original_filepaths_map:
            continue

        suggestion = renaming_suggestions.get(base_name)
        
        title = None
        artist = None

        if suggestion and suggestion.get("title") is not None and suggestion.get("artist") is not None:
            title = suggestion["title"]
            artist = suggestion["artist"]

        if title and artist:
            # Remove characters not allowed in Windows filenames
            # Keep spaces, hyphens, underscores, dots, and parentheses
            title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_', '.', '(', ')'))
            artist = "".join(c for c in artist if c.isalnum() or c in (' ', '-', '_', '.', '(', ')'))

            # Apply the new filename format: using the custom delimiter
            new_filename = f"{title}{delimiter}{artist}.mp3"

            for original_filepath in original_filepaths_map[base_name]:
                current_filename = os.path.basename(original_filepath)
                dir_path = os.path.dirname(original_filepath)
                new_full_filepath = os.path.join(dir_path, new_filename)

                # Determine if a rename is needed
                rename_needed = (original_filepath != new_full_filepath)

                if rename_needed or force_tag_update:
                    changes_by_folder[dir_path].append({
                        "original_path": original_filepath,
                        "new_path": new_full_filepath,
                        "original_name": current_filename,
                        "new_name": new_filename,
                        "new_title": title, # Store title and artist for ID3 tag update
                        "new_artist": artist,
                        "rename_needed": rename_needed, # Flag if filename change is needed
                        "tag_update_needed": True # Always assume tag update is needed if we're processing it
                    })
        else:
            logging.warning(f"Could not determine title/artist for '{base_name}'. Keeping original filename.")

    if not changes_by_folder:
        logging.info("No suggested or necessary file name changes or tag updates.")
        return

    print("\n--- Predicted Changes ---")
    
    # Sort folder paths for consistent output (current folder -> subfolders)
    sorted_folders = sorted(changes_by_folder.keys())

    for folder_path in sorted_folders:
        print(f"\nPath: {folder_path}")
        for change in changes_by_folder[folder_path]:
            action_desc = []
            if change["rename_needed"]:
                action_desc.append(f"Rename: {change['new_name']} <== {change['original_name']}")
            if change["tag_update_needed"]:
                action_desc.append(f"Update Tags (Title: '{change['new_title']}', Artist: '{change['new_artist']}')")
            
            if action_desc:
                print(f"  * {'; '.join(action_desc)}")
    print("-----------------------------------\n")

    user_input = input("Proceed with these changes? (Type 'yes' to confirm): ").strip().lower()

    if user_input == 'yes':
        logging.info("User confirmed. Proceeding with operations.")
        # Step 3: Rename files and update ID3 tags after confirmation
        for folder_path in sorted_folders:
            for change in changes_by_folder[folder_path]:
                original_filepath = change['original_path']
                new_full_filepath = change['new_path']
                
                # Perform rename first if needed
                if change['rename_needed']:
                    try:
                        # Check if the new file name already exists (e.g., if multiple original files map to the same new name)
                        if os.path.exists(new_full_filepath) and original_filepath != new_full_filepath:
                            logging.warning(f"Skipping rename for '{change['original_name']}' as '{change['new_name']}' already exists.")
                            # If we skip rename, we should still try to update tags on the *original* file if it's not being renamed
                            if not force_tag_update: # Only skip tag update if not forced
                                continue 
                            # If force_tag_update is true, we proceed to update tags on the original file
                            target_filepath_for_tag = original_filepath
                        else:
                            os.rename(original_filepath, new_full_filepath)
                            logging.info(f"Renamed '{change['original_name']}' to '{change['new_name']}'.")
                            target_filepath_for_tag = new_full_filepath
                    except OSError as e:
                        logging.error(f"File renaming error '{original_filepath}' -> '{new_full_filepath}': {e}")
                        continue # Skip tag update if rename failed

                else: # No rename needed, but tags might be updated due to --forcetag
                    target_filepath_for_tag = original_filepath
                
                # Always attempt to update ID3 tags if scheduled
                if change['tag_update_needed']:
                    update_id3_tags(target_filepath_for_tag, change['new_title'], change['new_artist'])
    else:
        logging.info("User cancelled the operation. No files were renamed or tags updated.")


def main():
    parser = argparse.ArgumentParser(
        description="Renames MP3 files to 'Title[Delimiter]Artist.mp3' format (using Gemini API) and updates ID3 tags.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        'path', 
        nargs='?', 
        default='.', 
        help='The target directory. Defaults to the current directory.'
    )
    parser.add_argument(
        '-S', 
        action='store_true', 
        help='Recursively searches subfolders.'
    )
    parser.add_argument(
        '-O', # Only current folder
        action='store_true', 
        help='Processes only the specified folder (non-recursive).'
    )
    parser.add_argument(
        '-C', # Current folder only (alias for -O)
        action='store_true', 
        help='Processes only the specified folder (non-recursive, alias for -O).'
    )
    parser.add_argument(
        '-D', '--delimiter',
        default=" -by ", # Set default delimiter
        help='The delimiter to place between the title and artist. Defaults to " -by ".'
    )
    parser.add_argument(
        '-T', '--forcetag',
        action='store_true',
        help='Force update of ID3 tags even if filename remains unchanged. Tags will be updated based on Gemini API\'s title/artist extraction.'
    )
    
    # Print help if no parameters are provided
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    target_directory = os.path.abspath(args.path)

    if not os.path.isdir(target_directory):
        logging.error(f"Error: Directory not found: '{target_directory}'")
        return

    # Use API key loaded via dotenv
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        logging.critical("GEMINI_API_KEY environment variable is not set. Please create a .env file or set the environment variable.")
        return

    # Load model name from GEMINI_MODEL environment variable, defaults to 'gemini-pro'
    # gemini_model_name = os.getenv("GEMINI_MODEL", "gemini-pro")
    gemini_model_name = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

    try:
        configure(api_key=api_key)
        model = GenerativeModel(gemini_model_name)
        logging.info(f"Initialized Gemini API using '{gemini_model_name}' model.")
    except Exception as e:
        logging.critical(f"Failed to initialize Gemini model. Ensure GEMINI_API_KEY is correctly set. Error: {e}")
        return

    # Logic to determine recursive option
    recursive_search = args.S
    # If -O or -C is explicitly specified, disable recursive mode
    if args.O or args.C:
        recursive_search = False 
    
    logging.info(f"Starting to collect MP3 files in '{target_directory}'. (Recursive search: {recursive_search}, Force Tag Update: {args.forcetag})")
    rename_mp3_files(target_directory, recursive_search, model, args.delimiter, args.forcetag) # Pass force_tag_update
    logging.info("MP3 renaming and ID3 tag update process completed.")

if __name__ == '__main__':
    main()