"""
.. include:: ../README.md

----
"""

from __future__ import annotations

import typing as t

from sqlglot import expressions as exp
from sqlglot.dialects.dialect import Dialect as Dialect, Dialects as Dialects
from sqlglot.diff import diff as diff
from sqlglot.errors import (
    ErrorLevel as ErrorLevel,
    ParseError as ParseError,
    TokenError as TokenError,
    UnsupportedError as UnsupportedError,
)
from sqlglot.expressions import (
    Expression as Expression,
    alias_ as alias,
    and_ as and_,
    column as column,
    condition as condition,
    except_ as except_,
    from_ as from_,
    intersect as intersect,
    maybe_parse as maybe_parse,
    not_ as not_,
    or_ as or_,
    select as select,
    subquery as subquery,
    table_ as table,
    to_column as to_column,
    to_table as to_table,
    union as union,
)
from sqlglot.generator import Generator as Generator
from sqlglot.parser import Parser as Parser
from sqlglot.schema import MappingSchema as MappingSchema, Schema as Schema
from sqlglot.tokens import Tokenizer as Tokenizer, TokenType as TokenType

if t.TYPE_CHECKING:
    from sqlglot.dialects.dialect import DialectType as DialectType

    T = t.TypeVar("T", bound=Expression)


__version__ = "11.5.9"

pretty = False
"""Whether to format generated SQL by default."""

schema = MappingSchema()
"""The default schema used by SQLGlot (e.g. in the optimizer)."""


def parse(sql: str, read: DialectType = None, **opts) -> t.List[t.Optional[Expression]]:
    """
    Parses the given SQL string into a collection of syntax trees, one per parsed SQL statement.

    Args:
        sql: the SQL code string to parse.
        read: the SQL dialect to apply during parsing (eg. "spark", "hive", "presto", "mysql").
        **opts: other `sqlglot.parser.Parser` options.

    Returns:
        The resulting syntax tree collection.
    """
    dialect = Dialect.get_or_raise(read)()
    return dialect.parse(sql, **opts)


@t.overload
def parse_one(
    sql: str,
    read: None = None,
    into: t.Type[T] = ...,
    **opts,
) -> T:
    ...


@t.overload
def parse_one(
    sql: str,
    read: DialectType,
    into: t.Type[T],
    **opts,
) -> T:
    ...


@t.overload
def parse_one(
    sql: str,
    read: None = None,
    into: t.Union[str, t.Collection[t.Union[str, t.Type[Expression]]]] = ...,
    **opts,
) -> Expression:
    ...


@t.overload
def parse_one(
    sql: str,
    read: DialectType,
    into: t.Union[str, t.Collection[t.Union[str, t.Type[Expression]]]],
    **opts,
) -> Expression:
    ...


@t.overload
def parse_one(
    sql: str,
    **opts,
) -> Expression:
    ...


def parse_one(
    sql: str,
    read: DialectType = None,
    into: t.Optional[exp.IntoType] = None,
    **opts,
) -> Expression:
    """
    Parses the given SQL string and returns a syntax tree for the first parsed SQL statement.

    Args:
        sql: the SQL code string to parse.
        read: the SQL dialect to apply during parsing (eg. "spark", "hive", "presto", "mysql").
        into: the SQLGlot Expression to parse into.
        **opts: other `sqlglot.parser.Parser` options.

    Returns:
        The syntax tree for the first parsed statement.
    """

    dialect = Dialect.get_or_raise(read)()

    if into:
        result = dialect.parse_into(into, sql, **opts)
    else:
        result = dialect.parse(sql, **opts)

    for expression in result:
        if not expression:
            raise ParseError(f"No expression was parsed from '{sql}'")
        return expression
    else:
        raise ParseError(f"No expression was parsed from '{sql}'")


def transpile(
    sql: str,
    read: DialectType = None,
    write: DialectType = None,
    identity: bool = True,
    error_level: t.Optional[ErrorLevel] = None,
    **opts,
) -> t.List[str]:
    """
    Parses the given SQL string in accordance with the source dialect and returns a list of SQL strings transformed
    to conform to the target dialect. Each string in the returned list represents a single transformed SQL statement.

    Args:
        sql: the SQL code string to transpile.
        read: the source dialect used to parse the input string (eg. "spark", "hive", "presto", "mysql").
        write: the target dialect into which the input should be transformed (eg. "spark", "hive", "presto", "mysql").
        identity: if set to `True` and if the target dialect is not specified the source dialect will be used as both:
            the source and the target dialect.
        error_level: the desired error level of the parser.
        **opts: other `sqlglot.generator.Generator` options.

    Returns:
        The list of transpiled SQL statements.
    """
    write = write or read if identity else write
    return [
        Dialect.get_or_raise(write)().generate(expression, **opts)
        for expression in parse(sql, read, error_level=error_level)
    ]
