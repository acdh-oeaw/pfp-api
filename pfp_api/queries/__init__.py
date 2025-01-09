from pathlib import Path


class QueryBuilder:
    filename: Path = None

    def __init__(self, filename: str):
        self.filename = Path(__file__).parent / filename

    def __str__(self):
        return self.filename.read_text()
