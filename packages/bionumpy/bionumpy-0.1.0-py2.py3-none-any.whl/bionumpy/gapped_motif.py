import numpy as np
import dataclasses
from bionumpy.util import convolution
from npstructures import RaggedArray

@dataclasses.dataclass
class GappedMotif:
    characters: np.ndarray
    mask: np.ndarray # True if

    def match(self, substring):
        matches = substring==self.characters
        matches |= self.mask
        return np.all(matches, axis=-1)


@dataclasses.dataclass
class 2dGappedMotif:
    characters: np.ndarray # n_motifs x motif_length
    mask: np.ndarray # n_motifs x motif_length

    def match(self, substring):
        """something

        Something more

        Parameters
        ----------

        """
        matches = substring==self.characters
        matches |= self.mask
        return np.all(matches, axis=-1)



 
sequence = np.array([ord(c) for c in "GGGATVGTCGT"], dtype=np.uint8)
sequences = RaggedArray([[ord(c) for c in seq] for seq in  ["GGGATVGTCGT", "JKHKJHKJHGU"]], dtype=np.uint8)


motif = GappedMotif(np.array([ord(c) for c in "TVGT"], dtype=np.uint8), np.array([False, False, False, False]))


my_func = apply_to_sequences(GappedMotif.match)
                   

@convolution
def match_sequence(sequence, window_size, motif):
    windows = np.lib.stride_tricks.sliding_window_view(sequence, window_size)
    window_matches = motif.match(windows)
    return window_matches


total_matches
for motif in general_motif.generate_motifs():
    total_matches |= match_sequence(sequences, moif.length(), motif)


print(np.any(match_sequence, axis=-1))

