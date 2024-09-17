import pandas as pd

def load_excel_words(excel_file):
    # Load the Excel file and extract the words from the "word" column
    df = pd.read_excel(excel_file)
    return df['word'].tolist()

def load_txt_kannada_words(txt_file):
    # Load the text file, ignoring the first line (English text)
    with open(txt_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        # Ignore the first line (assuming it contains English text)
        kannada_lines = lines[1:]
        # Split each line into words using comma as a separator
        kannada_words = [line.strip().split(',') for line in kannada_lines]
    return kannada_words

def compare_words_with_txt(excel_words, kannada_words):
    # Compare each word from the text file against the words in the Excel file
    results = []
    for line_words in kannada_words:
        line_result = []
        for word in line_words:
            # Check if the word is present in the Excel word list
            if word in excel_words:
                line_result.append(f"{word}: Correct")
            else:
                line_result.append(f"{word}: Wrong")
        results.append(line_result)
    
    return results

def main(excel_file, txt_file):
    # Load words from the Excel file
    excel_words = load_excel_words(excel_file)
    
    # Load Kannada words from the text file
    kannada_words = load_txt_kannada_words(txt_file)
    
    # Compare the words with the text file
    comparison_results = compare_words_with_txt(excel_words, kannada_words)
    
    # Print results
    for i, line_result in enumerate(comparison_results):
        print(f"Line {i+1} results:")
        for result in line_result:
            print(result)
        print()

# Replace with the path to your files
excel_file = "words.xlsx"
txt_file = "output.txt"

main(excel_file, txt_file)
