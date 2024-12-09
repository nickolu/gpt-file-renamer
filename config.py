"""
Configuration file for GPT file renamer prompts and examples.
Modify these settings to customize the behavior for your specific use case.
"""

# System prompt for the file renaming task
SYSTEM_PROMPT = "You are QAing a list of file names of video games with the extension {extension}. Please remove the numeric prefix andcorrect any issues, returning the name of the new file."

# Example conversations to help guide the model
EXAMPLE_CONVERSATIONS = [
    # Example 1
    {
        "user": "574--lien 3 (U){extension}",
        "assistant": "Alien 3 (U){extension}"
    },
    # Example 2
    {
        "user": "400--Home Alone 2 - Lost in New York(1){extension}",
        "assistant": "Home Alone 2 - Lost in New York (1){extension}"
    },
    # Example 3
    {
        "user": "007 Animal kingdom mobilization{extension}",
        "assistant": "Animal Kingdom Mobilization{extension}"
    }
]

# File eligibility rules
# Each rule is a dictionary with:
# - pattern: a regex pattern to match filenames
# - description: a human-readable description of what the rule does
# - exclude: if True, matching files will be excluded; if False, matching files will be included
FILE_ELIGIBILITY_RULES = [
    {
        "pattern": r"^\d+",  # Starts with numbers
        "description": "Files that start with numbers",
        "exclude": False  # Include these files
    },
    {
        "pattern": r"^duplicate--",  # Starts with 'duplicate--'
        "description": "Files that start with 'duplicate--'",
        "exclude": True  # Exclude these files
    }
]

# Set this to True to require ALL include rules to match
# Set to False to include files that match ANY include rule
REQUIRE_ALL_RULES = False

# Alternative prompt examples (commented out by default)
"""
# For music files
SYSTEM_PROMPT = "You are organizing music files with the extension {extension}. Format artist names and song titles properly, ensuring consistent capitalization and removing unnecessary prefixes or numbers."

# For photo files
SYSTEM_PROMPT = "You are organizing photo files with the extension {extension}. Convert dates to YYYY-MM-DD format, remove unnecessary prefixes, and ensure consistent naming."

# For document files
SYSTEM_PROMPT = "You are organizing document files with the extension {extension}. Format titles in proper case, remove unnecessary prefixes or numbers, and ensure consistent naming conventions."
"""
