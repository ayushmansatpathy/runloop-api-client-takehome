const fs = require('fs');
const path = require('path');

// Function to write a text file
function writeTextFile(filename, content) {
    try {
        fs.writeFileSync(filename, content, 'utf8');
        console.log(`Successfully wrote ${filename}`);
    } catch (error) {
        console.error(`Error writing ${filename}:`, error);
    }
}

// Write 3 text files to the current directory
writeTextFile('file1.txt', 'This is the content of file 1.\nCreated by test.js');
writeTextFile('file2.txt', 'This is the content of file 2.\nCreated by test.js');
writeTextFile('file3.txt', 'This is the content of file 3.\nCreated by test.js');

console.log('All files have been created successfully!');
