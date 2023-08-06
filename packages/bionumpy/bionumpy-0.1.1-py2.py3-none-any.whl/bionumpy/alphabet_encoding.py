from encodings import Encoding

class AlphabetEncoding:

    def __init__(self, alphabet: str):
        alphabet = [c.lower() for c in alphabet]
        upper_alphabet = [c.upper() for c in alphabet]
        self._alphabet = np.array([ord(l) for l in letters], dtype=np.uint8)
        self._lookup = np.zeros(256, dtype=np.uint8)
        self._lookup[alphabet] = np.arange(len(alphabet))
        self._lookup[uppper_alphabet] = np.arange(len(alphabet))
        self._mask = np.zeros(256, dtype=bool)
        self._mask[alphabet] = True
        self._mask[upper_alphabet] = True

    def encode(self, byte_array):
        return self._lookup[byte_array]

    def decode(self, encoded):
        return self._alphabet[encoded]

    def alphabet_size(self):
        return self._alphabet.size

    def __eq__(self, other):
        if not isinstance(other, AlphabetEncoding):
            return False
        return np.all(self._alphabet == other._alphabet)

    @classmethod
    def from_alphabet(cls, letters):
        return cls(lookup, alphabet)

ACTGEncoding = AlphabetEncoding("ACTG")
