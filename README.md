# Plagiarism Detector with CBF (Counting Bloom Filter)

## Introduction
This project implements a sophisticated plagiarism detection system using a Counting Bloom Filter (CBF). It is designed to accurately detect similarities between different text versions by leveraging complex hash functions and efficient data structures.

## Features
- Custom Counting Bloom Filter implementation for efficient data handling.
- Advanced rolling hash mechanism for text analysis.
- Modular arithmetic hash function for optimized performance.
- Complex algorithm to calculate plagiarism scores between texts.
- Experimental analysis with visualizations to demonstrate the effectiveness of the approach.
- Comprehensive tests to validate the functionality of the CBF and plagiarism detection.

## File Structure
- `CountingBloomFilter.py`: Implementation of the custom Counting Bloom Filter and the necessary data structures.
- `PlagiarismChecker.py`: Core logic for the plagiarism detection, including the rolling hash and complex scoring algorithm.
- `Plagiarism Checker codes.ipynb`: Jupyter Notebook containing the implementation, test cases, and experimental analysis.
- `Summary.pdf`: A detailed summary and justification of the methodologies used, including complexity analysis.

## Installation
To set up the project, clone the repository and install the necessary dependencies:
```bash
git clone https://github.com/Ajodo-Godson/Plagiarism-Detector-with-CBF.git
cd Plagiarism-Detector-with-CBF
# Install any required dependencies
## Usage
Import the CountingBloomFilter and PlagiarismChecker modules.
Instantiate the Counting Bloom Filter with desired parameters.
Use the plagiarism detection functions to compare text versions.
from CountingBloomFilter import CountingBloomFilter
from PlagiarismChecker import plagiarism_check_complex

### Example usage
result = plagiarism_check_complex(text_version_1, text_version_2, num_items, false_positive_rate)
print(f"Plagiarism Score: {result}%")

