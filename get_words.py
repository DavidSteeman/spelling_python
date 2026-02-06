import re
import argparse
from turtle import st
import unicodedata

def remove_accents_nfd(text):
    """
    Remove accents using Unicode Normalization Form Decomposition (NFD).
    This separates base characters from combining diacritical marks.
    """
    # Normalize to NFD (decomposed form)
    nfd_form = unicodedata.normalize('NFD', text)
    # Filter out combining characters (accents)
    return ''.join(char for char in nfd_form if unicodedata.category(char) != 'Mn')

def valid_required_letter(value):
    """Custom type function that validates an input to consist of 6 valid (non-accented) letters."""
    converted_value = remove_accents_nfd(value)
    if not value.isalpha():
        raise argparse.ArgumentTypeError(f"{value} is not a valid letter")
    if len(value) != 1:
        raise argparse.ArgumentTypeError(f"{value} must be exactly 1 letter")
    return converted_value


def valid_optional_letters(value):
    """Custom type function that validates an input to consist of 6 valid (non-accented) letters."""
    converted_value = remove_accents_nfd(value)
    if not value.isalpha():
        raise argparse.ArgumentTypeError(f"{value} is not a valid letter")
    if len(value) != 6:
        raise argparse.ArgumentTypeError(f"{value} must be exactly 6 letters")
    return converted_value


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description = "Generate valid words to use with NYT Games' Spelling Bee"
    )
    
    # Required argument
    parser.add_argument(
        '-df', '--dictionary_file',
        type=str,
        default='words_alpha.txt',
        required=True,
        help='File containing a list of valid words (required)'
    )
    
    # Optional argument with flag
    parser.add_argument(
        '-rl', '--required-letter',
        type=valid_required_letter,
        required=True,
        help='The letter that must appear in every valid word (required)'
    )
    
    
    parser.add_argument(
        '-ol', '--optional-letters',
        type=valid_optional_letters,
        required=True,
        help='Six optional letters that can be used in addition to the required letter (required)'
    )
    
    
    # Parse arguments
    args = parser.parse_args()
    words_file = args.dictionary_file.lower()
    required_letter = args.required_letter.lower()
    optional_letters = args.optional_letters.lower()
    
    # Access the arguments
    print(f"Dictionary file: {words_file}")
    
    # Example usage of re module
    # Check if input file has a valid extension
    if re.search(r'\.(txt|csv|json)$', words_file):
        print("Valid file extension detected")
    else:
        print("Warning: Unexpected file extension")
    
    if words_file[-4:] == '.txt':
        with open(words_file, 'r') as f:
            all_words = [line.strip() for line in f]
    elif words_file[-4:] == '.csv':
        import csv
        with open(words_file, 'r') as f:
            reader = csv.reader(f)
            all_words = [row[0].strip() for row in reader if row]
    elif words_file[-5:] == '.json':
        import json
        with open(words_file, 'r') as f:
            data = json.load(f)
            all_words = [word.strip() for word in data if isinstance(word, str)]
    else:
        print("Unsupported file format. Please provide a .txt, .csv, or .json file.")
        return
    
    print(f"Loaded {len(all_words)} words from {words_file}")
    
    results = find_valid_words(all_words, required_letter, optional_letters)
    
    print(f"Required letter: {required_letter}")
    print(f"Optional letters: {optional_letters}")
    print(f"\nFound {len(results)} valid words:")
    for word in results:
        print(f"  {word} ({len(word)} letters)")

def find_valid_words(word_list, required_letter, optional_letters):
    """
    Find all valid words of four or more letters containing the required letter
    and using only the required and optional letters.
    
    Args:
        word_list: List of valid words to search through
        required_letter: The letter that must appear at least once (string)
        optional_letters: Six letters that can be used (string or list)
    
    Returns:
        List of valid words sorted from longest to shortest
    """
    # Combine required and optional letters into a set of allowed letters
    if isinstance(optional_letters, str):
        optional_letters = list(optional_letters)
    
    allowed_letters = set([required_letter] + optional_letters)
    
    valid_words = []
    
    for word in word_list:        
        # Check if word is at least 4 letters
        if len(word) < 4:
            continue
    
        # Convert word to lowercase for consistent comparison
        word_lower = remove_accents_nfd(word).lower()
        
        # Check if word contains the required letter
        if required_letter not in word_lower:
            continue
        
        # Check if all letters in the word are in allowed_letters
        word_letters = set(word_lower)
        if word_letters.issubset(allowed_letters):
            valid_words.append(word)
    
    # Sort by length (longest first), then alphabetically for same length
    valid_words.sort(key=lambda w: (-len(w), w.lower()))
    
    return valid_words


# Example usage


if __name__ == '__main__':
    main()