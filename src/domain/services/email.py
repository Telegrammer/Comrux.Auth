from domain.entities import Email
from domain.value_objects import EmailAddress
from domain.ports import EmailIdGenerator


class EmailService:

    def __init__(self, id_generator: EmailIdGenerator):
        self._id_generator = id_generator

    def create_email(self, address: EmailAddress) -> Email:
        return Email(id_=self._id_generator(), address=address, is_verified=False)

    # It can be more complicated. For example we could add some "stage" parameter,
    # which can be read only from service to ensure that changing email is safe
    def verify_email(self, email: Email) -> None:
        email.is_verified = True
