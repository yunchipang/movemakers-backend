from fastapi import HTTPException, status


class ChoreographyNotFoundError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Choreography not found",
        )
