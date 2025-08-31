class ApplicationError(Exception): ...


class UsecaseError(ApplicationError): ...




class ErrorFactory:


    def __call__(self, *args, exception: Exception, **kwds) -> ApplicationError:
        return 