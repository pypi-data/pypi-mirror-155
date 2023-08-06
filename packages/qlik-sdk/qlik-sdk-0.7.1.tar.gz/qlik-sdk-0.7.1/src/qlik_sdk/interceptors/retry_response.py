import re


class RetryResponseInterceptor:
    def __init__(self, rpc):
        self._rpc = rpc

    def intercept(self, res):
        request_data = res["request_data"]
        # request_data = req
        # retry on request_aborted for get methods, except GetHyperCube and GetListObject
        # - exclude GetHyperCube* and GetListObject*.
        # - if they are aborted a new layout need to be fetched first to know if retrying the same parameter is relevant
        is_get_method = bool(
            re.match(
                r"(?!^GetHyperCube|^GetListObject)(^Get)",
                request_data.method,
                flags=re.IGNORECASE,
            )
        )
        request_aborted_code = 15
        is_request_aborted = (
            "error" in res and res["error"]["code"] == request_aborted_code
        )
        retry_allowed = is_get_method and is_request_aborted
        if "result" in res or not retry_allowed:
            return res
        return self._rpc.send(request_data)
