from typing import Any
from typing import Optional

from .. import util as util
from ..orm import strategy_options as strategy_options
from ..orm.query import Query as Query
from ..orm.session import Session as Session
from ..sql import func as func
from ..sql import literal_column as literal_column
from ..util import collections_abc as collections_abc

log: Any

class Bakery:
    cls: Any = ...
    cache: Any = ...
    def __init__(self, cls_: Any, cache: Any) -> None: ...
    def __call__(self, initial_fn: Any, *args: Any): ...

class BakedQuery:
    steps: Any = ...
    def __init__(
        self, bakery: Any, initial_fn: Any, args: Any = ...
    ) -> None: ...
    @classmethod
    def bakery(cls, size: int = ..., _size_alert: Optional[Any] = ...): ...
    def __iadd__(self, other: Any): ...
    def __add__(self, other: Any): ...
    def add_criteria(self, fn: Any, *args: Any): ...
    def with_criteria(self, fn: Any, *args: Any): ...
    def for_session(self, session: Any): ...
    def __call__(self, session: Any): ...
    def spoil(self, full: bool = ...): ...
    def to_query(self, query_or_session: Any): ...

class Result:
    bq: Any = ...
    session: Any = ...
    def __init__(self, bq: Any, session: Any) -> None: ...
    def params(self, *args: Any, **kw: Any): ...
    def with_post_criteria(self, fn: Any): ...
    def __iter__(self) -> Any: ...
    def count(self): ...
    def scalar(self): ...
    def first(self): ...
    def one(self): ...
    def one_or_none(self): ...
    def all(self): ...
    def get(self, ident: Any): ...

def bake_lazy_loaders() -> None: ...
def unbake_lazy_loaders() -> None: ...
def baked_lazyload_all(*keys: Any): ...

baked_lazyload: Any
baked_lazyload_all: Any
bakery: Any
