class Picture():

    def __init__(self, pid, rotation, tags):
        self.id = pid
        self.rotation = rotation
        self.tags = tags

    def score(self, other):
        return min(
            len(self.tags.intersection(other.tags)),
            len(self.tags.difference(other.tags)),
            len(other.tags.difference(self.tags))
        )

    def __repr__(self):
        return "(id: '%s', tags: %s)" % (self.id, self.tags)
