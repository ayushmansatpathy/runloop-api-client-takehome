import os

# Function to write a text file
def write_text_file(filename, content):
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Successfully wrote {filename}")
    except Exception as error:
        print(f"Error writing {filename}: {error}")

# Write 3 text files to the current directory
write_text_file('file1.txt', 'This is the content of file 1.\nCreated by test.py')
write_text_file('file2.txt', 'This is the content of file 2.\nCreated by test.py')
write_text_file('file3.txt', 'This is the content of file 3.\nCreated by test.py')

print('All files have been created successfully!')
