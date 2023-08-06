import logging
import time

import numpy as np


class KmerLookup:
    def __init__(self, kmers, representative_kmers, lookup):
        self._kmers = kmers
        self._representative_kmers = representative_kmers
        self._lookup = lookup

    def to_file(self, file_name):
        np.savez(file_name, 
                 kmers = self._kmers,
                 representative_kmers = self._representative_kmers,
                 lookup = self._lookup)

    @classmethod
    def from_file(cls, file_name):
        data = np.load(file_name)
        return cls(data["kmers"],
                   data["representative_kmers"],
                   data["lookup"])

    def index_kmers(self):
        self._kmers.sort()
        self._representative_kmers = np.searchsorted(self._kmers, self._representative_kmers)

    def _get_indexes(self, kmers):
        return np.searchsorted(self._kmers, kmers)

    def count_kmers(self, kmers):
        indexes = self._get_indexes(kmers)
        #return np.bincount(indexes[kmers==self._kmers[indexes]], minlength=self._kmers.size)
        return np.bincount(indexes[kmers==self._kmers[np.minimum(indexes, self._kmers.size-1)]], minlength=self._kmers.size)

    def get_node_counts(self, kmers):
        counts = self.count_kmers(kmers)
        cum_counts = np.insert(np.cumsum(counts[self._representative_kmers]), 0, 0)
        node_counts = cum_counts[self._lookup[:, 1]]-cum_counts[self._lookup[:, 0]]
        return node_counts

    def max_node_id(self):
        return np.max(self._lookup)


class SimpleKmerLookup(KmerLookup):
    def get_node_counts(self, kmers):
        t = time.perf_counter()
        counts = self.count_kmers(kmers)
        result = np.bincount(self._lookup, counts[self._representative_kmers])
        logging.info("Took %.4f sec to get node counts" % (time.perf_counter()-t))
        return result

    @classmethod
    def from_old_index_files(cls, filename):
        data = np.load(filename)
        kmers = data["kmers"]
        unique_kmers = np.unique(kmers)
        k = cls(unique_kmers, kmers, data["nodes"])
        k.index_kmers()
        return k
