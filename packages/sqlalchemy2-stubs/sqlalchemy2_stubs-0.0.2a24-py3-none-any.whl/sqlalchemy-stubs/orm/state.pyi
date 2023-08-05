from typing import Any

from . import base as base
from . import interfaces as interfaces
from .base import ATTR_WAS_SET as ATTR_WAS_SET
from .base import INIT_OK as INIT_OK
from .base import NEVER_SET as NEVER_SET
from .base import NO_VALUE as NO_VALUE
from .base import PASSIVE_NO_INITIALIZE as PASSIVE_NO_INITIALIZE
from .base import PASSIVE_NO_RESULT as PASSIVE_NO_RESULT
from .base import PASSIVE_OFF as PASSIVE_OFF
from .base import SQL_OK as SQL_OK
from .path_registry import PathRegistry as PathRegistry
from .. import inspection as inspection
from .. import util as util

class InstanceState(interfaces.InspectionAttrInfo):
    session_id: Any = ...
    key: Any = ...
    runid: Any = ...
    load_options: Any = ...
    load_path: Any = ...
    insert_order: Any = ...
    modified: bool = ...
    expired: bool = ...
    is_instance: bool = ...
    identity_token: Any = ...
    callables: Any = ...
    class_: Any = ...
    manager: Any = ...
    committed_state: Any = ...
    expired_attributes: Any = ...
    def __init__(self, obj: Any, manager: Any) -> None: ...
    @util.memoized_property
    def attrs(self): ...
    @property
    def transient(self): ...
    @property
    def pending(self): ...
    @property
    def deleted(self): ...
    @property
    def was_deleted(self): ...
    @property
    def persistent(self): ...
    @property
    def detached(self): ...
    @property
    def session(self): ...
    @property
    def object(self): ...
    @property
    def identity(self): ...
    @property
    def identity_key(self): ...
    @util.memoized_property
    def parents(self): ...
    @util.memoized_property
    def mapper(self): ...
    @property
    def has_identity(self): ...
    def obj(self) -> None: ...
    @property
    def dict(self): ...
    def get_history(self, key: Any, passive: Any): ...
    def get_impl(self, key: Any): ...
    @property
    def unmodified(self): ...
    def unmodified_intersection(self, keys: Any): ...
    @property
    def unloaded(self): ...
    @property
    def unloaded_expirable(self): ...

class AttributeState:
    state: Any = ...
    key: Any = ...
    def __init__(self, state: Any, key: Any) -> None: ...
    @property
    def loaded_value(self): ...
    @property
    def value(self): ...
    @property
    def history(self): ...
    def load_history(self): ...

class PendingCollection:
    deleted_items: Any = ...
    added_items: Any = ...
    def __init__(self) -> None: ...
    def append(self, value: Any) -> None: ...
    def remove(self, value: Any) -> None: ...
