

class DependencyInfo:
    modId: str
    versionRange: str
    ordering: str
    side: str
    mandatory: str

    raw: str

    def __init__(self, raw=None):
        self.raw = raw
