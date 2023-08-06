from typing import Generic, List, TypeVar, Union

T = TypeVar("T")
ResI = TypeVar("ResI")
ReqI = TypeVar("ReqI")


class InterceptorHandler(Generic[T]):
    handlers: List[T]
    "list containing the interceptors"

    def __init__(self):
        self.handlers = []

    def use(self, interceptor: Union[T, List[T]]) -> None:
        """
        method helper for registering an interceptor

        Parameters
        ----------
        interceptor
            function interceptor for requests/responses
        """
        if isinstance(interceptor, list):
            self.handlers = self.handlers + interceptor
        else:
            self.handlers.append(interceptor)


class Interceptors(Generic[ReqI, ResI]):
    response: InterceptorHandler[ResI]
    request: InterceptorHandler[ReqI]
