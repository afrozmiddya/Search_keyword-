import concurrent.futures
import os

def highlight_keyword(line, keyword):
    """
    Highlights the keyword in the line by wrapping it in '**'.
    """
    keyword_lower = keyword.lower()
    line_lower = line.lower()
    highlighted_line = ""
    start = 0

    # Find all occurrences of the keyword in the line (case-insensitive)
    while True:
        idx = line_lower.find(keyword_lower, start)
        if idx == -1:
            highlighted_line += line[start:]
            break
        # Add the part before the keyword
        highlighted_line += line[start:idx]
        # Add the highlighted keyword
        highlighted_line += f"**{line[idx:idx+len(keyword)]}**"
        start = idx + len(keyword)
    return highlighted_line

def search_keywords_in_text(text, keywords):
    keyword_matches = {}
    for keyword in keywords:
        matches = []
        for line_number, line in enumerate(text.splitlines(), start=1):
            if keyword.lower() in line.lower():  # Case-insensitive search
                highlighted_line = highlight_keyword(line, keyword)  # Highlight the keyword
                matches.append((line_number, highlighted_line))
        if matches:
            keyword_matches[keyword] = matches
    return keyword_matches

def search_with_timeout(file_name, keywords, timeout):
    try:
        # Get the full path to the file in the same directory as the script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, file_name)
        
        with open(file_path, 'r') as file:
            text = file.read()
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(search_keywords_in_text, text, keywords)
            try:
                keyword_matches = future.result(timeout=timeout)
                return keyword_matches
            except concurrent.futures.TimeoutError:
                print(f"Search timed out after {timeout} seconds.")
                return {}
    except FileNotFoundError:
        print(f"File not found: {file_name}")
        return {}

# Example usage
file_name = 'afroz.txt'  # Only the file name (file must be in the same directory as the script)
keywords = ['Afroz']     # Keyword to search for
timeout = 5              # Time limit in seconds

keyword_matches = search_with_timeout(file_name, keywords, timeout)
if keyword_matches:
    for keyword, matches in keyword_matches.items():
        print(f"Keyword '{keyword}' found in the following lines:")
        for line_number, line in matches:
            print(f"Line {line_number}: {line}")
else:
    print("No keywords found or search timed out.")
