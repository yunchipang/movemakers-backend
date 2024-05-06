class StudioNotFoundError(Exception):
    def __init__(self, studio_id: str):
        self.studio_id = studio_id
        super().__init__(f"Studio {self.studio_id} not found")
