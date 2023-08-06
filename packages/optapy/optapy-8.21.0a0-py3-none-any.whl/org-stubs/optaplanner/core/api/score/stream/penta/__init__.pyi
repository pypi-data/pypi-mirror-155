import typing



_PentaJoiner__A = typing.TypeVar('_PentaJoiner__A')  # <A>
_PentaJoiner__B = typing.TypeVar('_PentaJoiner__B')  # <B>
_PentaJoiner__C = typing.TypeVar('_PentaJoiner__C')  # <C>
_PentaJoiner__D = typing.TypeVar('_PentaJoiner__D')  # <D>
_PentaJoiner__E = typing.TypeVar('_PentaJoiner__E')  # <E>
class PentaJoiner(typing.Generic[_PentaJoiner__A, _PentaJoiner__B, _PentaJoiner__C, _PentaJoiner__D, _PentaJoiner__E]):
    """
    public interface PentaJoiner<A, B, C, D, E>
    
        Created with :class:`~org.optaplanner.core.api.score.stream.Joiners`. Used by
        :meth:`~org.optaplanner.core.api.score.stream.quad.QuadConstraintStream.ifExists`, ...
    
        Also see:
            :class:`~org.optaplanner.core.api.score.stream.Joiners`
    """
    ...


class __module_protocol__(typing.Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.optaplanner.core.api.score.stream.penta")``.

    PentaJoiner: typing.Type[PentaJoiner]
