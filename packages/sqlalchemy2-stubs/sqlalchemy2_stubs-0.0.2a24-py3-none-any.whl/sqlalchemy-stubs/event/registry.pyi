from typing import Any
from typing import Optional

from .. import exc as exc
from .. import util as util

class _EventKey:
    target: Any = ...
    identifier: Any = ...
    fn: Any = ...
    fn_key: Any = ...
    fn_wrap: Any = ...
    dispatch_target: Any = ...
    def __init__(
        self,
        target: Any,
        identifier: Any,
        fn: Any,
        dispatch_target: Any,
        _fn_wrap: Optional[Any] = ...,
    ) -> None: ...
    def with_wrapper(self, fn_wrap: Any): ...
    def with_dispatch_target(self, dispatch_target: Any): ...
    def listen(self, *args: Any, **kw: Any) -> None: ...
    def remove(self) -> None: ...
    def contains(self): ...
    def base_listen(
        self,
        propagate: bool = ...,
        insert: bool = ...,
        named: bool = ...,
        retval: Optional[Any] = ...,
        asyncio: bool = ...,
    ) -> None: ...
    def append_to_list(self, owner: Any, list_: Any): ...
    def remove_from_list(self, owner: Any, list_: Any) -> None: ...
    def prepend_to_list(self, owner: Any, list_: Any): ...
