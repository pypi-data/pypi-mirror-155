import enum
from contextlib import contextmanager
from functools import partial
from typing import Any, Iterator, List, Optional, overload

from pglift import db, instances
from pglift._compat import Literal
from pglift.ctx import BaseContext
from pglift.models import interface
from pglift.models.system import Instance
from pglift.types import Role


class AuthType(str, enum.Enum):
    peer = "peer"
    password_command = "password_command"
    pgpass = "pgpass"


def configure_instance(
    ctx: BaseContext,
    manifest: interface.Instance,
    *,
    port: Optional[int] = None,
    creating: bool = False,
    **confitems: Any,
) -> None:
    values = manifest.configuration.copy()
    values["port"] = port or manifest.port
    values.update(confitems)
    instances.configure(ctx, manifest, values=values, _creating=creating)


@contextmanager
def reconfigure_instance(
    ctx: BaseContext, manifest: interface.Instance, **confitems: Any
) -> Iterator[None]:
    configure_instance(ctx, manifest, **confitems)
    try:
        yield
    finally:
        configure_instance(ctx, manifest)


@overload
def execute(
    ctx: BaseContext,
    instance: Instance,
    query: str,
    fetch: Literal[True],
    autocommit: bool = False,
    role: Optional[Role] = None,
    **kwargs: Any,
) -> List[Any]:
    ...


@overload
def execute(
    ctx: BaseContext,
    instance: Instance,
    query: str,
    fetch: bool = False,
    autocommit: bool = False,
    role: Optional[Role] = None,
    **kwargs: Any,
) -> List[Any]:
    ...


def execute(
    ctx: BaseContext,
    instance: Instance,
    query: str,
    fetch: bool = True,
    autocommit: bool = False,
    role: Optional[Role] = None,
    **kwargs: Any,
) -> Optional[List[Any]]:
    if role is None:
        connect = partial(db.connect, ctx)
    elif role.password:
        connect = partial(
            db.connect,
            ctx,
            user=role.name,
            password=role.password.get_secret_value(),
        )
    else:
        connect = partial(db.connect, settings=ctx.settings.postgresql, user=role.name)
    with instances.running(ctx, instance):
        with connect(instance, autocommit=autocommit, **kwargs) as conn:
            cur = conn.execute(query)
            conn.commit()
            if fetch:
                return cur.fetchall()
        return None
