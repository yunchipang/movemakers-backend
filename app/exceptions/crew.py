from fastapi import HTTPException, status


class CrewNotFoundError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Crew not found",
        )
