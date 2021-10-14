class NonClosable:
    def __init__(self, stream_like):
        self.stream_like = stream_like

    def close(self):
        # Reset file instead of closing it
        if hasattr(self.stream_like, "seek"):
            self.stream_like.seek(0)

    def __bool__(self):
        return self.stream_like.__bool__()

    def __getattr__(self, name):
        return getattr(self.stream_like, name)

    def __iter__(self):
        return self.stream_like.__iter__()

    def __repr__(self):
        return self.stream_like.__repr__()
