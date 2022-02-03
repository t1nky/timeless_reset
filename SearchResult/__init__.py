class SearchResult:
    def __init__(self, pos: int, num: int) -> None:
        self.pos = pos
        self.num = num

    def __str__(self):
        return f"{self.num}: {self.pos}"
