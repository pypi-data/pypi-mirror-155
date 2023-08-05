# fmt: off
from typing import Any
from typing import Optional

from . import attributes as attributes
from . import interfaces as interfaces
from . import loading as loading
from .interfaces import ORMColumnsClauseRole as ORMColumnsClauseRole
from .path_registry import PathRegistry as PathRegistry
from .util import aliased as aliased
from .util import Bundle as Bundle
from .util import ORMAdapter as ORMAdapter
from .. import future as future
from .. import inspect as inspect
from .. import sql as sql
from .. import util as util
from .._typing import _ExecuteOptions
from ..sql import coercions as coercions
from ..sql import expression as expression
from ..sql import roles as roles
from ..sql import visitors as visitors
from ..sql.base import CacheableOptions as CacheableOptions
from ..sql.base import CompileState as CompileState
from ..sql.base import Options as Options
from ..sql.selectable import LABEL_STYLE_DISAMBIGUATE_ONLY as LABEL_STYLE_DISAMBIGUATE_ONLY
from ..sql.selectable import LABEL_STYLE_NONE as LABEL_STYLE_NONE
from ..sql.selectable import LABEL_STYLE_TABLENAME_PLUS_COL as LABEL_STYLE_TABLENAME_PLUS_COL
from ..sql.selectable import SelectState as SelectState
from ..sql.visitors import ExtendedInternalTraversal as ExtendedInternalTraversal
from ..sql.visitors import InternalTraversal as InternalTraversal
# fmt: on

LABEL_STYLE_LEGACY_ORM: Any

class QueryContext:
    class default_load_options(Options): ...
    load_options: Any = ...
    execution_options: _ExecuteOptions = ...
    bind_arguments: Any = ...
    compile_state: Any = ...
    query: Any = ...
    session: Any = ...
    loaders_require_buffering: bool = ...
    loaders_require_uniquing: bool = ...
    params: Any = ...
    propagated_loader_options: Any = ...
    attributes: Any = ...
    autoflush: Any = ...
    populate_existing: Any = ...
    invoke_all_eagers: Any = ...
    version_check: Any = ...
    refresh_state: Any = ...
    yield_per: Any = ...
    identity_token: Any = ...
    def __init__(
        self,
        compile_state: Any,
        statement: Any,
        params: Any,
        session: Any,
        load_options: Any,
        execution_options: Optional[_ExecuteOptions] = ...,
        bind_arguments: Optional[Any] = ...,
    ) -> None: ...

class ORMCompileState(CompileState):
    class default_compile_options(CacheableOptions): ...
    current_path: Any = ...
    def __init__(self, *arg: Any, **kw: Any) -> None: ...
    @classmethod
    def create_for_statement(
        cls, statement_container: Any, compiler: Any, **kw: Any
    ) -> None: ...
    @classmethod
    def get_column_descriptions(cls, statement: Any): ...
    @classmethod
    def orm_pre_session_exec(
        cls,
        session: Any,
        statement: Any,
        params: Any,
        execution_options: Optional[_ExecuteOptions],
        bind_arguments: Any,
        is_reentrant_invoke: Any,
    ): ...
    @classmethod
    def orm_setup_cursor_result(
        cls,
        session: Any,
        statement: Any,
        params: Any,
        execution_options: Optional[_ExecuteOptions],
        bind_arguments: Any,
        result: Any,
    ): ...

class ORMFromStatementCompileState(ORMCompileState):
    multi_row_eager_loaders: bool = ...
    compound_eager_adapter: Any = ...
    extra_criteria_entities: Any = ...
    eager_joins: Any = ...
    use_legacy_query_style: Any = ...
    statement_container: Any = ...
    requested_statement: Any = ...
    dml_table: Any = ...
    compile_options: Any = ...
    statement: Any = ...
    current_path: Any = ...
    attributes: Any = ...
    global_attributes: Any = ...
    primary_columns: Any = ...
    secondary_columns: Any = ...
    create_eager_joins: Any = ...
    order_by: Any = ...
    @classmethod
    def create_for_statement(
        cls, statement_container: Any, compiler: Any, **kw: Any
    ): ...

class ORMSelectCompileState(ORMCompileState, SelectState):
    multi_row_eager_loaders: bool = ...
    compound_eager_adapter: Any = ...
    correlate: Any = ...
    correlate_except: Any = ...
    global_attributes: Any = ...
    select_statement: Any = ...
    for_statement: Any = ...
    use_legacy_query_style: Any = ...
    compile_options: Any = ...
    label_style: Any = ...
    current_path: Any = ...
    eager_order_by: Any = ...
    attributes: Any = ...
    primary_columns: Any = ...
    secondary_columns: Any = ...
    eager_joins: Any = ...
    extra_criteria_entities: Any = ...
    create_eager_joins: Any = ...
    from_clauses: Any = ...
    @classmethod
    def create_for_statement(
        cls, statement: Any, compiler: Any, **kw: Any
    ): ...
    @classmethod
    def determine_last_joined_entity(cls, statement: Any): ...
    @classmethod
    def exported_columns_iterator(cls, statement: Any) -> None: ...
    @classmethod
    def from_statement(cls, statement: Any, from_statement: Any): ...

class _QueryEntity:
    @classmethod
    def to_compile_state(cls, compile_state: Any, entities: Any) -> None: ...

class _MapperEntity(_QueryEntity):
    expr: Any = ...
    mapper: Any = ...
    is_aliased_class: Any = ...
    path: Any = ...
    selectable: Any = ...
    def __init__(self, compile_state: Any, entity: Any) -> None: ...
    supports_single_entity: bool = ...
    use_id_for_hash: bool = ...
    @property
    def type(self): ...
    @property
    def entity_zero_or_selectable(self): ...
    def corresponds_to(self, entity: Any): ...
    def row_processor(self, context: Any, result: Any): ...
    def setup_compile_state(self, compile_state: Any) -> None: ...

class _BundleEntity(_QueryEntity):
    use_id_for_hash: bool = ...
    bundle: Any = ...
    type: Any = ...
    supports_single_entity: Any = ...
    def __init__(
        self,
        compile_state: Any,
        expr: Any,
        setup_entities: bool = ...,
        parent_bundle: Optional[Any] = ...,
    ) -> None: ...
    @property
    def mapper(self): ...
    @property
    def entity_zero(self): ...
    def corresponds_to(self, entity: Any): ...
    @property
    def entity_zero_or_selectable(self): ...
    def setup_compile_state(self, compile_state: Any) -> None: ...
    def row_processor(self, context: Any, result: Any): ...

class _ColumnEntity(_QueryEntity):
    @property
    def type(self): ...
    @property
    def use_id_for_hash(self): ...
    def row_processor(self, context: Any, result: Any): ...

class _RawColumnEntity(_ColumnEntity):
    entity_zero: Any = ...
    mapper: Any = ...
    supports_single_entity: bool = ...
    expr: Any = ...
    column: Any = ...
    entity_zero_or_selectable: Any = ...
    def __init__(
        self,
        compile_state: Any,
        column: Any,
        parent_bundle: Optional[Any] = ...,
    ) -> None: ...
    def corresponds_to(self, entity: Any): ...
    def setup_compile_state(self, compile_state: Any) -> None: ...

class _ORMColumnEntity(_ColumnEntity):
    supports_single_entity: bool = ...
    expr: Any = ...
    entity_zero: Any = ...
    mapper: Any = ...
    column: Any = ...
    def __init__(
        self,
        compile_state: Any,
        column: Any,
        parententity: Any,
        parent_bundle: Optional[Any] = ...,
    ) -> None: ...
    def corresponds_to(self, entity: Any): ...
    def setup_compile_state(self, compile_state: Any) -> None: ...

class _IdentityTokenEntity(_ORMColumnEntity):
    def setup_compile_state(self, compile_state: Any) -> None: ...
    def row_processor(self, context: Any, result: Any): ...
