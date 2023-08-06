import numpy as np
rolling_window = np.lib.stride_tricks.sliding_window_view
np.random.seed(42)
def get_minimizer(kmer, k, m):
    mmer_mask = 4**m-1
    shifts = np.arange(k-m+1)*2
    mmers = (kmer>>shifts[:, None])& mmer_mask
    minimizers = np.min(mmers, axis=0)
    return minimizers

class MinimizerHash:
    def __init__(self, k, m):
        dtype=np.uint64
        self._k = k
        self._m = m
        self._n_letters_in_dtype = 4*dtype(0).nbytes
        self._shifts = 2*np.arange(self._n_letters_in_dtype, dtype=dtype)
        self._rev_shifts = 2*np.arange(self._n_letters_in_dtype, 0, -1, dtype=dtype)
        self._mask = dtype(4**k-1)
   
    def get_minimizers(self, sequence):
        kmers = (sequence[:-1, None] >> self._shifts)
        kmers |= (sequence[1:, None] << self._rev_shifts)
        kmers = kmers.ravel()
        kmers &= self._mask
        print(kmers)
        minimizers = np.min(rolling_window(kmers, self._m-self._k+1), axis=-1)
        print(minimizers)
        u = np.flatnonzero(minimizers[:-1] != minimizers[1:])+1
        return minimizers[np.insert(u,0,0)]

a = np.array([3727, 6534])
print([bin(r) for r in a])
print([bin(r) for r in get_minimizer(a, 7, 4)])
a = np.random.rand(4).view(np.uint64)
print(MinimizerHash(13, 31).get_minimizers(a))
