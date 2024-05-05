class DancerNotFoundError(Exception):
    def __init__(self, dancer_id: str):
        self.dancer_id = dancer_id
        super().__init__(f"Dancer {self.dancer_id} not found")
