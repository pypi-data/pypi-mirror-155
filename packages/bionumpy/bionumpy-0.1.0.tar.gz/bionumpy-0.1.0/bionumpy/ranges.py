class Z:
    def __init__(n):
        self._n = n

    def contains(self, values):
        return (values >= 0) & (values < self._n)
    
        
