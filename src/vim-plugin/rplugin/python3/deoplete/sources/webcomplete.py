import os
import select
from .base import Base


class Source(Base):
    def __init__(self, vim):
        Base.__init__(self, vim)

        self.name = 'webcomplete'
        self.mark = '[webcomplete]'
        self.min_pattern_length = 0
        self.words = []
        self.fifopath = '/tmp/webcomplete-fifo'

    def _update_words(self):
        if os.path.exists(self.fifopath):
            io = os.open(self.fifopath, os.O_RDONLY | os.O_NONBLOCK)
            self.words += [i[:-1] for i in io.read().split()]
            return
            with open(self.fifopath, 'r') as f:
                r, _, _ = select.select([f], [], [], 0)
                if r:
                    self.words = ['rsuccess']
                    # self.words += [i[:-1] for i in f.read().split()]
                else:
                    self.words = ['rfailure']
        else:
            self.words = ['failure']

    def gather_candidates(self, context):
        self._update_words()
        return self.words
