from fastapi import HTTPException, status


class ContactDuplicateError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A contact with this email already exists.",
        )
