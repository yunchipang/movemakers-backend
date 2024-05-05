class ChoreographyNotFoundError(Exception):
    def __init__(self, choreo_id: str):
        self.choreo_id = choreo_id
        super().__init__(f"Choreography {self.choreo_id} not found")
