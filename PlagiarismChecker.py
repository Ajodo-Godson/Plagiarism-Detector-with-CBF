from CountingBloomFilter import CountingBloomFilter
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


url_version_1 = "https://bit.ly/39MurYb"
url_version_2 = "https://bit.ly/3we1QCp"
url_version_3 = "https://bit.ly/3vUecRn"
from requests import get


def get_txt_into_list_of_words(url):
    """Cleans the text data
    Input
    ----------
    url : string
    The URL for the txt file.
    Returns
    -------
    data_just_words_lower_case: list
    List of "cleaned-up" words sorted by the order they appear in the original file.
    """
    bad_chars = [";", ",", ".", "?", "!", "_", "[", "]", "(", ")", "*"]
    data = get(url).text
    data = "".join(c for c in data if c not in bad_chars)
    data_without_newlines = "".join(
        c if (c not in ["\n", "\r", "\t"]) else " " for c in data
    )
    data_just_words = [word for word in data_without_newlines.split(" ") if word != ""]
    data_just_words_lower_case = [word.lower() for word in data_just_words]
    return data_just_words_lower_case


version_1 = get_txt_into_list_of_words(url_version_1)
version_2 = get_txt_into_list_of_words(url_version_2)
version_3 = get_txt_into_list_of_words(url_version_3)
num_items = 10000
false_positive_rate = 0.01
# Example usage
complex_score_1_2 = plagiarism_check_complex(version_1, version_2, num_items, false_positive_rate, window_size=3)
print(f"Complex Plagiarism Score between Version 1 and 2: {complex_score_1_2}%")

complex_score_2_3 = plagiarism_check_complex(version_2, version_3, num_items, false_positive_rate, window_size=3)
print(f"Complex Plagiarism Score between Version 2 and 3: {complex_score_2_3}%")

complex_score_1_3 = plagiarism_check_complex(version_1, version_3, num_items, false_positive_rate, window_size=3)
print(f"Complex Plagiarism Score between Version 1 and 3: {complex_score_1_3}%")

complex_score_1_4 = plagiarism_check_complex(version_3, version_2, num_items, false_positive_rate, window_size=3)
print(f"Complex Plagiarism Score between Version 3 and 2: {complex_score_1_4}%")

complex_score_1_5 = plagiarism_check_complex(version_3, version_1, num_items, false_positive_rate, window_size=3)
print(f"Complex Plagiarism Score between Version 3 and 1: {complex_score_1_5}%")

complex_score_1_6 = plagiarism_check_complex(version_2, version_1, num_items, false_positive_rate, window_size=3)
print(f"Complex Plagiarism Score between Version 2 and 1: {complex_score_1_6}%")
