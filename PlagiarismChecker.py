from CountingBloomFilter import CountingBloomFilter
import re
class RollingHash:
    """
    Implementation of a rolling hash for efficient text hashing,
    particularly useful for algorithms like Rabin-Karp.
    """

    def __init__(self, base, window_size):
        """
        Initialize the rolling hash.

        :param base: Base value for the hash function.
        :param window_size: Size of the window (number of words) to hash.
        """
        self.base = base
        self.window_size = window_size
        self.hash_value = 0
        self.base_pow = 1
        self.hash_mod = 1000000007
        self.window = []
        for _ in range(window_size - 1):
            self.base_pow = (self.base_pow * self.base) % self.hash_mod

    def append(self, word):
        """
        Append a word to the rolling hash.

        :param word: Word to append.
        """
        self.hash_value = (self.hash_value * self.base + ord('|')) % self.hash_mod  # Separator
        for char in word:
            self.hash_value = (self.hash_value * self.base + ord(char)) % self.hash_mod
        self.window.append(word)

    def skip(self):
        """
        Skip the oldest word from the rolling hash window.
        """
        if self.window:
            old_word = self.window.pop(0)
            word_pow = 1
            for char in old_word:
                self.hash_value = (self.hash_value - ord(char) * word_pow) % self.hash_mod
                word_pow = (word_pow * self.base) % self.hash_mod
            self.hash_value = (self.hash_value - ord('|') * word_pow) % self.hash_mod  # Separator

    def slide(self, new_word):
        """
        Slide the rolling hash window to include a new word.

        :param new_word: New word to include in the window.
        """
        if len(self.window) >= self.window_size:
            self.skip()
        self.append(new_word)

    def current_hash(self):
        """
        Get the current hash value of the rolling hash.

        :return: Current hash value.
        """
        return self.hash_value

    def reset(self):
        """
        Reset the rolling hash to its initial state.
        """
        self.hash_value = 0
        self.base_pow = 1
        self.window = []


def plagiarism_check_complex(version1, version2, num_items, fpr, window_size=2):
    """
    Check for plagiarism between two versions of a text using a complex algorithm.
    
    :param version1: List of words in the first version.
    :param version2: List of words in the second version.
    
    return: plagiarism score
    """
    cbf = CountingBloomFilter(num_items, fpr)
    rh = RollingHash(256, window_size)

    # Process version1
    for i in range(len(version1) - window_size + 1):
        window_words = version1[i:i + window_size]
        rh.slide(' '.join(window_words))
        hash_value = rh.current_hash()
        cbf.insert(str(hash_value))
        rh.reset()

    # Process version2 and check plagiarism
    match_count = 0
    plagiarized_sequences = []
    for i in range(len(version2) - window_size + 1):
        window_words = version2[i:i + window_size]
        rh.slide(' '.join(window_words))
        hash_value = rh.current_hash()
        if cbf.is_word_present(str(hash_value)):
            match_count += 1
            plagiarized_sequences.append(' '.join(window_words))
        rh.reset()

    plagiarism_score = (match_count / max(1, len(version2) - window_size + 1)) * 100
    
    return plagiarism_score


def clean_and_split_text(text):
    """Cleans the input text and splits it into a list of words."""
    bad_chars = [";", ",", ".", "?", "!", "_", "[", "]", "(", ")", "*"]
    text = "".join(c for c in text if c not in bad_chars)
    text_without_newlines = " ".join(text.splitlines())
    return [word.lower() for word in text_without_newlines.split() if word]

def main():
    print("Plagiarism Checker")
    text_version_1 = input("Enter the first text: ")
    text_version_2 = input("Enter the second text: ")

    # Clean and process the input text
    version_1 = clean_and_split_text(text_version_1)
    version_2 = clean_and_split_text(text_version_2)

    # Set parameters for the Counting Bloom Filter
    num_items = 10000  # Adjust as needed
    false_positive_rate = 0.01  # Adjust as needed

    # Calculate the plagiarism score
    score = plagiarism_check_complex(version_1, version_2, num_items, false_positive_rate, window_size=3)
    print(f"Plagiarism Score between the two texts: {score}%")

if __name__ == "__main__":
    main()
