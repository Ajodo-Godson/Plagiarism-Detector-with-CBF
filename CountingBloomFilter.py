import math


class bitarray:
    """
    A custom bit array class to manage individual bits efficiently.
    Each element in the bit array can be incremented to count occurrences.
    """

    def __init__(self, size):
        """Initialize the bit array with a specified size, setting all bits to 0."""
        self.bits = [0] * size

    def set_bit(self, index, value):
        """Increment the bit at a specified index by the given value."""
        self.bits[index] += value

    def get_bit(self, index):
        """Retrieve the value of the bit at the specified index."""
        return self.bits[index]

    def __repr__(self):
        """Represent the bit array as a string for easy visualization."""
        return "".join(str(bit) for bit in self.bits)


class CountingBloomFilter:
    import bitarray
    """
    Implementation of a Counting Bloom Filter.
    It uses multiple hash functions to map elements to bit positions.
    """

    def __init__(self, num_items, fpr):
        """
        Initialize the Counting Bloom Filter.

        :param num_items: Estimated number of items to store.
        :param fpr: Desired false positive rate.
        """
        self.fpr = fpr
        self.size = -num_items * math.log(fpr) / (math.log(2) ** 2)
        self.num_hashfn = int(self.size * math.log(2) / num_items)
        self.bit_array = bitarray(int(self.size))

    @staticmethod
    def custom_hash(data, seed):
        """
        Custom hash function for hashing data.

        :param data: Data to be hashed.
        :param seed: Seed value for the hash function.
        :return: Hashed value.
        """
        h = seed
        a = 0xB7E15163  # 3074997963
        b = 0x8AED2A6B  # 2334415563
        c = 0xD72A7A45  # 3597765701
        d = 0x9E3779B1  # 2654435761

        total_bytes = len(data)
        remaining_bytes = total_bytes % 4
        total_32bit_blocks = (total_bytes - remaining_bytes) // 4

        def mix(chunk):
            nonlocal h
            h ^= chunk
            h = (h * a) ^ (h >> 9)
            h = (h * b) ^ (h << 11)
            h = (h * c) ^ (h >> 13)
            h = (h * d) ^ (h << 15)
            h &= 0xFFFFFFFF

        for block in range(total_32bit_blocks):
            chunk = int.from_bytes(data[block * 4: block * 4 + 4], byteorder="little")
            mix(chunk)

        if remaining_bytes > 0:
            remaining_chunk = int.from_bytes(
                data[-remaining_bytes:] + b"\x00" * (4 - remaining_bytes),
                byteorder="little",
            )
            mix(remaining_chunk)

        h ^= total_bytes
        h ^= h >> 16
        h = (h * 0x85EBCA6B) & 0xFFFFFFFF
        h ^= h >> 13
        h = (h * 0xC2B2AE35) & 0xFFFFFFFF
        h ^= h >> 16

        return h




    def hash_cbf(self, item):
        """
        Generate multiple hash values for an item using different seeds.

        :param item: Item to hash.
        :return: List of hash values.
        """
        hash_values = []
        for i in range(self.num_hashfn):
            hash_value = CountingBloomFilter.custom_hash(item, i) % int(self.size)
            hash_values.append(hash_value)
        return hash_values

    def search(self, item):
        """
        Check if an item is possibly in the bloom filter.

        :param item: Item to search for.
        :return: Boolean indicating if item is possibly present.
        """
        item = item.encode("utf-8")
        hash_values = self.hash_cbf(item)
        return all(self.bit_array.get_bit(hash_val) for hash_val in hash_values)

    def insert(self, item):
        """
        Insert an item into the bloom filter.

        :param item: Item to insert.
        """
        item = item.encode("utf-8")
        hash_values = self.hash_cbf(item)
        for hash_val in hash_values:
            self.bit_array.set_bit(hash_val, 1)

    def delete(self, item):
        """
        Delete an item from the bloom filter, if present.

        :param item: Item to delete.
        """
        item = item.encode("utf-8")
        hash_values = self.hash_cbf(item)
        for hash_val in hash_values:
            if self.bit_array.get_bit(hash_val) > 0:
                self.bit_array.set_bit(hash_val, self.bit_array.get_bit(hash_val) - 1)

    def insert_words(self, words):
        """
        Insert multiple words into the bloom filter.

        :param words: List of words to insert.
        """
        for word in words:
            self.insert(word)

    def is_word_present(self, word):
        """
        Check if a word is present in the bloom filter.

        :param word: Word to check.
        :return: Boolean indicating if word is present.
        """
        return self.search(word)
