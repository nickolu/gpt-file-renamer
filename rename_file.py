import os
import openai
from openai.types.chat import ChatCompletionMessageParam, ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam, ChatCompletionAssistantMessageParam
from typing import Optional
import re
from config import SYSTEM_PROMPT, EXAMPLE_CONVERSATIONS, FILE_ELIGIBILITY_RULES, REQUIRE_ALL_RULES

def get_new_filename(current_filename: str) -> Optional[str]:
    """
    Get a new filename suggestion from OpenAI for the given filename.
    """
    print(f"\nProcessing file: {current_filename}")
    # Make sure to set your OpenAI API key in environment variables
    filename, file_extension = os.path.splitext(current_filename)
    print(f"  Base filename: {filename}")
    print(f"  Extension: {file_extension}")
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OpenAI API key not found. Please set OPENAI_API_KEY environment variable.")
    
    client = openai.OpenAI(api_key=api_key)
    
    try:
        print("  Requesting new filename from OpenAI...")
        messages: list[ChatCompletionMessageParam] = [
            ChatCompletionSystemMessageParam(
                role="system",
                content=SYSTEM_PROMPT.format(extension=file_extension)
            )
        ]
        
        # Add example conversations
        for example in EXAMPLE_CONVERSATIONS:
            user_message = str(example["user"].format(extension=file_extension))
            assistant_message = str(example["assistant"].format(extension=file_extension))
            
            messages.extend([
                ChatCompletionUserMessageParam(
                    role="user",
                    content=user_message
                ),
                ChatCompletionAssistantMessageParam(
                    role="assistant",
                    content=assistant_message
                )
            ])
        
        messages.extend([
            ChatCompletionSystemMessageParam(
                role="system",
                content="Provide a filename suggestion based on the given filename: {}".format(current_filename)
            )
        ])
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=50
        )
        
        content = response.choices[0].message.content
        if not content:
            print("  OpenAI response was empty. Skipping this file.")
            return None
            
        new_filename = content.strip()
        print(f"  Suggested new filename: {new_filename}")
        return new_filename
    except Exception as e:
        print(f"  Error getting new filename: {str(e)}")
        return current_filename

def handle_duplicate(directory: str, new_filename: str) -> str:
    """
    Handle duplicate filenames by appending a number
    """
    base, ext = os.path.splitext(new_filename)
    counter = 1
    while os.path.exists(os.path.join(directory, new_filename)):
        print(f"  Found duplicate: {new_filename}")
        new_filename = f"{base} ({counter}){ext}"
        print(f"  Trying: {new_filename}")
        counter += 1
    return new_filename

def is_file_eligible(filename: str) -> bool:
    """
    Check if a file is eligible for renaming based on the configured rules.
    """
    include_matches = []
    
    for rule in FILE_ELIGIBILITY_RULES:
        matches = bool(re.search(rule["pattern"], filename))
        if rule["exclude"] and matches:
            return False
        if not rule["exclude"]:
            include_matches.append(matches)
    
    if not include_matches:  # If no include rules defined, accept all files
        return True
    
    if REQUIRE_ALL_RULES:
        return all(include_matches)
    return any(include_matches)

def process_directory(directory_path: str) -> None:
    """
    Process all eligible files in the specified directory.
    """
    import time
    start_time = time.time()
    
    def print_progress(processed, total):
        elapsed = time.time() - start_time
        remaining = total - processed
        print(f"\nProgress: {processed}/{total} eligible files processed ({remaining} remaining)")
        print(f"Time elapsed: {elapsed:.1f} seconds")
        if processed > 0:
            avg_time = elapsed / processed
            est_remaining = avg_time * remaining
            print(f"Estimated time remaining: {est_remaining:.1f} seconds")
    
    print(f"\nProcessing directory: {directory_path}")
    
    if not os.path.exists(directory_path):
        print(f"Error: Directory '{directory_path}' does not exist")
        return

    all_files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
    eligible_files = [f for f in all_files if is_file_eligible(f)]
    total_files = len(eligible_files)
    
    print(f"Found {len(all_files)} total files")
    print(f"Found {total_files} eligible files to process")
    
    if total_files == 0:
        print("No eligible files to process")
        return

    processed = 0
    print_progress(processed, total_files)

    for filename in eligible_files:
        old_path = os.path.join(directory_path, filename)
        
        # Get new filename suggestion
        new_filename = get_new_filename(filename)
        if new_filename is None:
            print(f"  Skipping {filename} - could not get new filename")
            continue
            
        # Handle potential duplicates
        new_filename = handle_duplicate(directory_path, new_filename)
        new_path = os.path.join(directory_path, new_filename)
        
        # Rename the file
        try:
            if old_path != new_path:
                os.rename(old_path, new_path)
                print(f"  Renamed: {filename} -> {new_filename}")
            else:
                print("  No rename needed - filename already correct")
        except Exception as e:
            print(f"  Error renaming file: {str(e)}")
        
        processed += 1
        print_progress(processed, total_files)

    print("\nDirectory processing complete!")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python rename_file.py <directory_path>")
        sys.exit(1)
    
    directory_path = sys.argv[1]
    process_directory(directory_path)
