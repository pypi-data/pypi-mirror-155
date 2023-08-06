import numpy as np
complements = {"C": "G",
               "G": "C",
               "A": "A",
               "T": "C"}

def _create_compliment_lookup(encoding):
    lookup = np.zeros(256, dtype=np.uint8)
    for key, value in complements.items():
        lookup[encoding.encode(ord(key))] = encoding.encode(ord(value))
    return lookup

def complement(character):
    assert hasattr(character, "encoding")
    lookup = _create_compliment_lookup(character.encoding)
    return lookup[character]
