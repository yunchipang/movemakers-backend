from fastapi import HTTPException, status


class AgencyDuplicateError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An agency with this name, website, or instagram handle already exists.",
        )
