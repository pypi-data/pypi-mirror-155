import itertools
from typing import Iterator, List, TypeVar

from .rest import get_next_query_value

T = TypeVar("T")


class ListableResource(List[T]):
    pagination: Iterator[T]
    """
    Automatic paginating iterator for resources that supports it
    It handles fetching automatically the next set of data from the list

    Example:
    --------
    >>> items = Items(config).get_items()
    ... for item in items.pagination:
    ...     print_item(item)
    """

    def __init__(
        self,
        response,
        auth,
        cls=None,
        path="",
        method="GET",
        query_params={},
        max_items=10,
    ):
        has_data_response = isinstance(response, dict) and "data" in response
        is_pag = has_data_response and "links" in response

        def create(e: any):
            if cls is None:
                return e
            o = cls(**e)
            o.auth = auth
            return o

        list.__init__(
            self,
            [
                create(elem)
                for elem in (response["data"] if has_data_response else response)
            ],
        )
        if is_pag:
            pag_iter = []
            try:
                curr_params = query_params.copy()
                curr_params["next"] = get_next_query_value(
                    response["links"]["next"]["href"]
                )
                rem_max_items = max_items - len(self)
                pag_iter = auth.paginate_rest(
                    path=path,
                    method=method,
                    params=curr_params,
                    max_items=rem_max_items,
                )
            except:
                pass

            def gen():
                for elem in pag_iter:
                    yield create(elem)

            self.pagination = itertools.chain(self, gen())
        else:

            def gen():
                for e in self:
                    yield e

            self.pagination = gen()
