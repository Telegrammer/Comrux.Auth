__all__ = ["GatewayFailedError"]


from application.exceptions import ApplicationError


class GatewayFailedError(ApplicationError): ...
