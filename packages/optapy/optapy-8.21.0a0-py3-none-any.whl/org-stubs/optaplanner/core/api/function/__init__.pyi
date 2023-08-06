import typing



_PentaFunction__A = typing.TypeVar('_PentaFunction__A')  # <A>
_PentaFunction__B = typing.TypeVar('_PentaFunction__B')  # <B>
_PentaFunction__C = typing.TypeVar('_PentaFunction__C')  # <C>
_PentaFunction__D = typing.TypeVar('_PentaFunction__D')  # <D>
_PentaFunction__E = typing.TypeVar('_PentaFunction__E')  # <E>
_PentaFunction__R = typing.TypeVar('_PentaFunction__R')  # <R>
class PentaFunction(typing.Generic[_PentaFunction__A, _PentaFunction__B, _PentaFunction__C, _PentaFunction__D, _PentaFunction__E, _PentaFunction__R]):
    """
    :class:`~org.optaplanner.core.api.function.https:.docs.oracle.com.javase.8.docs.api.java.lang.FunctionalInterface?is` public interface PentaFunction<A, B, C, D, E, R>
    
        Represents a function that accepts five arguments and produces a result. This is the five-arity specialization of
        :class:`~org.optaplanner.core.api.function.https:.docs.oracle.com.javase.8.docs.api.java.util.function.Function?is`.
    
        This is a :class:`~org.optaplanner.core.api.function.package` whose functional method is
        :meth:`~org.optaplanner.core.api.function.PentaFunction.apply`.
    
        Also see:
            :class:`~org.optaplanner.core.api.function.https:.docs.oracle.com.javase.8.docs.api.java.util.function.Function?is`
    """
    def apply(self, a: _PentaFunction__A, b: _PentaFunction__B, c: _PentaFunction__C, d: _PentaFunction__D, e: _PentaFunction__E) -> _PentaFunction__R:
        """
            Applies this function to the given arguments.
        
            Parameters:
                a (:class:`~org.optaplanner.core.api.function.PentaFunction`): the first function argument
                b (:class:`~org.optaplanner.core.api.function.PentaFunction`): the second function argument
                c (:class:`~org.optaplanner.core.api.function.PentaFunction`): the third function argument
                d (:class:`~org.optaplanner.core.api.function.PentaFunction`): the fourth function argument
                e (:class:`~org.optaplanner.core.api.function.PentaFunction`): the fifth function argument
        
            Returns:
                the function result
        
        
        """
        ...

_PentaPredicate__A = typing.TypeVar('_PentaPredicate__A')  # <A>
_PentaPredicate__B = typing.TypeVar('_PentaPredicate__B')  # <B>
_PentaPredicate__C = typing.TypeVar('_PentaPredicate__C')  # <C>
_PentaPredicate__D = typing.TypeVar('_PentaPredicate__D')  # <D>
_PentaPredicate__E = typing.TypeVar('_PentaPredicate__E')  # <E>
class PentaPredicate(typing.Generic[_PentaPredicate__A, _PentaPredicate__B, _PentaPredicate__C, _PentaPredicate__D, _PentaPredicate__E]):
    """
    :class:`~org.optaplanner.core.api.function.https:.docs.oracle.com.javase.8.docs.api.java.lang.FunctionalInterface?is` public interface PentaPredicate<A, B, C, D, E>
    
        Represents a predicate (boolean-valued function) of five arguments. This is the five-arity specialization of
        :class:`~org.optaplanner.core.api.function.https:.docs.oracle.com.javase.8.docs.api.java.util.function.Predicate?is`.
    
        This is a :class:`~org.optaplanner.core.api.function.package` whose functional method is
        :meth:`~org.optaplanner.core.api.function.PentaPredicate.test`.
    
        Also see:
            :class:`~org.optaplanner.core.api.function.https:.docs.oracle.com.javase.8.docs.api.java.util.function.Predicate?is`
    """
    def negate(self) -> 'PentaPredicate'[_PentaPredicate__A, _PentaPredicate__B, _PentaPredicate__C, _PentaPredicate__D, _PentaPredicate__E]: ...
    def test(self, a: _PentaPredicate__A, b: _PentaPredicate__B, c: _PentaPredicate__C, d: _PentaPredicate__D, e: _PentaPredicate__E) -> bool:
        """
            Evaluates this predicate on the given arguments.
        
            Parameters:
                a (:class:`~org.optaplanner.core.api.function.PentaPredicate`): the first input argument
                b (:class:`~org.optaplanner.core.api.function.PentaPredicate`): the second input argument
                c (:class:`~org.optaplanner.core.api.function.PentaPredicate`): the third input argument
                d (:class:`~org.optaplanner.core.api.function.PentaPredicate`): the fourth input argument
                e (:class:`~org.optaplanner.core.api.function.PentaPredicate`): the fifth input argument
        
            Returns:
                :code:`true` if the input arguments match the predicate, otherwise :code:`false`
        
        
        """
        ...

_QuadFunction__A = typing.TypeVar('_QuadFunction__A')  # <A>
_QuadFunction__B = typing.TypeVar('_QuadFunction__B')  # <B>
_QuadFunction__C = typing.TypeVar('_QuadFunction__C')  # <C>
_QuadFunction__D = typing.TypeVar('_QuadFunction__D')  # <D>
_QuadFunction__R = typing.TypeVar('_QuadFunction__R')  # <R>
class QuadFunction(typing.Generic[_QuadFunction__A, _QuadFunction__B, _QuadFunction__C, _QuadFunction__D, _QuadFunction__R]):
    """
    :class:`~org.optaplanner.core.api.function.https:.docs.oracle.com.javase.8.docs.api.java.lang.FunctionalInterface?is` public interface QuadFunction<A, B, C, D, R>
    
        Represents a function that accepts four arguments and produces a result. This is the four-arity specialization of
        :class:`~org.optaplanner.core.api.function.https:.docs.oracle.com.javase.8.docs.api.java.util.function.Function?is`.
    
        This is a :class:`~org.optaplanner.core.api.function.package` whose functional method is
        :meth:`~org.optaplanner.core.api.function.QuadFunction.apply`.
    
        Also see:
            :class:`~org.optaplanner.core.api.function.https:.docs.oracle.com.javase.8.docs.api.java.util.function.Function?is`
    """
    def apply(self, a: _QuadFunction__A, b: _QuadFunction__B, c: _QuadFunction__C, d: _QuadFunction__D) -> _QuadFunction__R:
        """
            Applies this function to the given arguments.
        
            Parameters:
                a (:class:`~org.optaplanner.core.api.function.QuadFunction`): the first function argument
                b (:class:`~org.optaplanner.core.api.function.QuadFunction`): the second function argument
                c (:class:`~org.optaplanner.core.api.function.QuadFunction`): the third function argument
                d (:class:`~org.optaplanner.core.api.function.QuadFunction`): the fourth function argument
        
            Returns:
                the function result
        
        
        """
        ...

_QuadPredicate__A = typing.TypeVar('_QuadPredicate__A')  # <A>
_QuadPredicate__B = typing.TypeVar('_QuadPredicate__B')  # <B>
_QuadPredicate__C = typing.TypeVar('_QuadPredicate__C')  # <C>
_QuadPredicate__D = typing.TypeVar('_QuadPredicate__D')  # <D>
class QuadPredicate(typing.Generic[_QuadPredicate__A, _QuadPredicate__B, _QuadPredicate__C, _QuadPredicate__D]):
    """
    :class:`~org.optaplanner.core.api.function.https:.docs.oracle.com.javase.8.docs.api.java.lang.FunctionalInterface?is` public interface QuadPredicate<A, B, C, D>
    
        Represents a predicate (boolean-valued function) of four arguments. This is the four-arity specialization of
        :class:`~org.optaplanner.core.api.function.https:.docs.oracle.com.javase.8.docs.api.java.util.function.Predicate?is`.
    
        This is a :class:`~org.optaplanner.core.api.function.package` whose functional method is
        :meth:`~org.optaplanner.core.api.function.QuadPredicate.test`.
    
        Also see:
            :class:`~org.optaplanner.core.api.function.https:.docs.oracle.com.javase.8.docs.api.java.util.function.Predicate?is`
    """
    def negate(self) -> 'QuadPredicate'[_QuadPredicate__A, _QuadPredicate__B, _QuadPredicate__C, _QuadPredicate__D]: ...
    def test(self, a: _QuadPredicate__A, b: _QuadPredicate__B, c: _QuadPredicate__C, d: _QuadPredicate__D) -> bool:
        """
            Evaluates this predicate on the given arguments.
        
            Parameters:
                a (:class:`~org.optaplanner.core.api.function.QuadPredicate`): the first input argument
                b (:class:`~org.optaplanner.core.api.function.QuadPredicate`): the second input argument
                c (:class:`~org.optaplanner.core.api.function.QuadPredicate`): the third input argument
                d (:class:`~org.optaplanner.core.api.function.QuadPredicate`): the fourth input argument
        
            Returns:
                :code:`true` if the input arguments match the predicate, otherwise :code:`false`
        
        
        """
        ...

_ToIntQuadFunction__A = typing.TypeVar('_ToIntQuadFunction__A')  # <A>
_ToIntQuadFunction__B = typing.TypeVar('_ToIntQuadFunction__B')  # <B>
_ToIntQuadFunction__C = typing.TypeVar('_ToIntQuadFunction__C')  # <C>
_ToIntQuadFunction__D = typing.TypeVar('_ToIntQuadFunction__D')  # <D>
class ToIntQuadFunction(typing.Generic[_ToIntQuadFunction__A, _ToIntQuadFunction__B, _ToIntQuadFunction__C, _ToIntQuadFunction__D]):
    """
    :class:`~org.optaplanner.core.api.function.https:.docs.oracle.com.javase.8.docs.api.java.lang.FunctionalInterface?is` public interface ToIntQuadFunction<A, B, C, D>
    
        Represents a function that accepts four arguments and produces an int-valued result. This is the :code:`int`-producing
        primitive specialization for :class:`~org.optaplanner.core.api.function.QuadFunction`.
    
        This is a :class:`~org.optaplanner.core.api.function.package` whose functional method is
        :meth:`~org.optaplanner.core.api.function.ToIntQuadFunction.applyAsInt`.
    
        Also see:
            :class:`~org.optaplanner.core.api.function.QuadFunction`
    """
    def applyAsInt(self, a: _ToIntQuadFunction__A, b: _ToIntQuadFunction__B, c: _ToIntQuadFunction__C, d: _ToIntQuadFunction__D) -> int:
        """
            Applies this function to the given arguments.
        
            Parameters:
                a (:class:`~org.optaplanner.core.api.function.ToIntQuadFunction`): the first function argument
                b (:class:`~org.optaplanner.core.api.function.ToIntQuadFunction`): the second function argument
                c (:class:`~org.optaplanner.core.api.function.ToIntQuadFunction`): the third function argument
                d (:class:`~org.optaplanner.core.api.function.ToIntQuadFunction`): the fourth function argument
        
            Returns:
                the function result
        
        
        """
        ...

_ToIntTriFunction__A = typing.TypeVar('_ToIntTriFunction__A')  # <A>
_ToIntTriFunction__B = typing.TypeVar('_ToIntTriFunction__B')  # <B>
_ToIntTriFunction__C = typing.TypeVar('_ToIntTriFunction__C')  # <C>
class ToIntTriFunction(typing.Generic[_ToIntTriFunction__A, _ToIntTriFunction__B, _ToIntTriFunction__C]):
    """
    :class:`~org.optaplanner.core.api.function.https:.docs.oracle.com.javase.8.docs.api.java.lang.FunctionalInterface?is` public interface ToIntTriFunction<A, B, C>
    
        Represents a function that accepts three arguments and produces an int-valued result. This is the :code:`int`-producing
        primitive specialization for :class:`~org.optaplanner.core.api.function.TriFunction`.
    
        This is a :class:`~org.optaplanner.core.api.function.package` whose functional method is
        :meth:`~org.optaplanner.core.api.function.ToIntTriFunction.applyAsInt`.
    
        Also see:
            :class:`~org.optaplanner.core.api.function.TriFunction`
    """
    def applyAsInt(self, a: _ToIntTriFunction__A, b: _ToIntTriFunction__B, c: _ToIntTriFunction__C) -> int:
        """
            Applies this function to the given arguments.
        
            Parameters:
                a (:class:`~org.optaplanner.core.api.function.ToIntTriFunction`): the first function argument
                b (:class:`~org.optaplanner.core.api.function.ToIntTriFunction`): the second function argument
                c (:class:`~org.optaplanner.core.api.function.ToIntTriFunction`): the third function argument
        
            Returns:
                the function result
        
        
        """
        ...

_ToLongQuadFunction__A = typing.TypeVar('_ToLongQuadFunction__A')  # <A>
_ToLongQuadFunction__B = typing.TypeVar('_ToLongQuadFunction__B')  # <B>
_ToLongQuadFunction__C = typing.TypeVar('_ToLongQuadFunction__C')  # <C>
_ToLongQuadFunction__D = typing.TypeVar('_ToLongQuadFunction__D')  # <D>
class ToLongQuadFunction(typing.Generic[_ToLongQuadFunction__A, _ToLongQuadFunction__B, _ToLongQuadFunction__C, _ToLongQuadFunction__D]):
    """
    :class:`~org.optaplanner.core.api.function.https:.docs.oracle.com.javase.8.docs.api.java.lang.FunctionalInterface?is` public interface ToLongQuadFunction<A, B, C, D>
    
        Represents a function that accepts four arguments and produces a long-valued result. This is the :code:`long`-producing
        primitive specialization for :class:`~org.optaplanner.core.api.function.QuadFunction`.
    
        This is a :class:`~org.optaplanner.core.api.function.package` whose functional method is
        :meth:`~org.optaplanner.core.api.function.ToLongQuadFunction.applyAsLong`.
    
        Also see:
            :class:`~org.optaplanner.core.api.function.QuadFunction`
    """
    def applyAsLong(self, a: _ToLongQuadFunction__A, b: _ToLongQuadFunction__B, c: _ToLongQuadFunction__C, d: _ToLongQuadFunction__D) -> int:
        """
            Applies this function to the given arguments.
        
            Parameters:
                a (:class:`~org.optaplanner.core.api.function.ToLongQuadFunction`): the first function argument
                b (:class:`~org.optaplanner.core.api.function.ToLongQuadFunction`): the second function argument
                c (:class:`~org.optaplanner.core.api.function.ToLongQuadFunction`): the third function argument
                d (:class:`~org.optaplanner.core.api.function.ToLongQuadFunction`): the fourth function argument
        
            Returns:
                the function result
        
        
        """
        ...

_ToLongTriFunction__A = typing.TypeVar('_ToLongTriFunction__A')  # <A>
_ToLongTriFunction__B = typing.TypeVar('_ToLongTriFunction__B')  # <B>
_ToLongTriFunction__C = typing.TypeVar('_ToLongTriFunction__C')  # <C>
class ToLongTriFunction(typing.Generic[_ToLongTriFunction__A, _ToLongTriFunction__B, _ToLongTriFunction__C]):
    """
    :class:`~org.optaplanner.core.api.function.https:.docs.oracle.com.javase.8.docs.api.java.lang.FunctionalInterface?is` public interface ToLongTriFunction<A, B, C>
    
        Represents a function that accepts three arguments and produces a long-valued result. This is the :code:`long`-producing
        primitive specialization for :class:`~org.optaplanner.core.api.function.TriFunction`.
    
        This is a :class:`~org.optaplanner.core.api.function.package` whose functional method is
        :meth:`~org.optaplanner.core.api.function.ToLongTriFunction.applyAsLong`.
    
        Also see:
            :class:`~org.optaplanner.core.api.function.TriFunction`
    """
    def applyAsLong(self, a: _ToLongTriFunction__A, b: _ToLongTriFunction__B, c: _ToLongTriFunction__C) -> int:
        """
            Applies this function to the given arguments.
        
            Parameters:
                a (:class:`~org.optaplanner.core.api.function.ToLongTriFunction`): the first function argument
                b (:class:`~org.optaplanner.core.api.function.ToLongTriFunction`): the second function argument
                c (:class:`~org.optaplanner.core.api.function.ToLongTriFunction`): the third function argument
        
            Returns:
                the function result
        
        
        """
        ...

_TriConsumer__A = typing.TypeVar('_TriConsumer__A')  # <A>
_TriConsumer__B = typing.TypeVar('_TriConsumer__B')  # <B>
_TriConsumer__C = typing.TypeVar('_TriConsumer__C')  # <C>
class TriConsumer(typing.Generic[_TriConsumer__A, _TriConsumer__B, _TriConsumer__C]):
    """
    :class:`~org.optaplanner.core.api.function.https:.docs.oracle.com.javase.8.docs.api.java.lang.FunctionalInterface?is` public interface TriConsumer<A, B, C>
    
        Represents a function that accepts three arguments and returns no result. This is the three-arity specialization of
        :class:`~org.optaplanner.core.api.function.https:.docs.oracle.com.javase.8.docs.api.java.util.function.Consumer?is`.
    
        This is a :class:`~org.optaplanner.core.api.function.package` whose functional method is
        :meth:`~org.optaplanner.core.api.function.TriConsumer.accept`.
    
        Also see:
            :class:`~org.optaplanner.core.api.function.https:.docs.oracle.com.javase.8.docs.api.java.util.function.Function?is`
    """
    def accept(self, a: _TriConsumer__A, b: _TriConsumer__B, c: _TriConsumer__C) -> None:
        """
            Performs this operation on the given arguments.
        
            Parameters:
                a (:class:`~org.optaplanner.core.api.function.TriConsumer`): the first function argument
                b (:class:`~org.optaplanner.core.api.function.TriConsumer`): the second function argument
                c (:class:`~org.optaplanner.core.api.function.TriConsumer`): the third function argument
        
        
        """
        ...
    def andThen(self, triConsumer: typing.Union['TriConsumer'[_TriConsumer__A, _TriConsumer__B, _TriConsumer__C], typing.Callable[[_TriConsumer__A, _TriConsumer__B, _TriConsumer__C], None]]) -> 'TriConsumer'[_TriConsumer__A, _TriConsumer__B, _TriConsumer__C]: ...

_TriFunction__A = typing.TypeVar('_TriFunction__A')  # <A>
_TriFunction__B = typing.TypeVar('_TriFunction__B')  # <B>
_TriFunction__C = typing.TypeVar('_TriFunction__C')  # <C>
_TriFunction__R = typing.TypeVar('_TriFunction__R')  # <R>
class TriFunction(typing.Generic[_TriFunction__A, _TriFunction__B, _TriFunction__C, _TriFunction__R]):
    """
    :class:`~org.optaplanner.core.api.function.https:.docs.oracle.com.javase.8.docs.api.java.lang.FunctionalInterface?is` public interface TriFunction<A, B, C, R>
    
        Represents a function that accepts three arguments and produces a result. This is the three-arity specialization of
        :class:`~org.optaplanner.core.api.function.https:.docs.oracle.com.javase.8.docs.api.java.util.function.Function?is`.
    
        This is a :class:`~org.optaplanner.core.api.function.package` whose functional method is
        :meth:`~org.optaplanner.core.api.function.TriFunction.apply`.
    
        Also see:
            :class:`~org.optaplanner.core.api.function.https:.docs.oracle.com.javase.8.docs.api.java.util.function.Function?is`
    """
    def apply(self, a: _TriFunction__A, b: _TriFunction__B, c: _TriFunction__C) -> _TriFunction__R:
        """
            Applies this function to the given arguments.
        
            Parameters:
                a (:class:`~org.optaplanner.core.api.function.TriFunction`): the first function argument
                b (:class:`~org.optaplanner.core.api.function.TriFunction`): the second function argument
                c (:class:`~org.optaplanner.core.api.function.TriFunction`): the third function argument
        
            Returns:
                the function result
        
        
        """
        ...

_TriPredicate__A = typing.TypeVar('_TriPredicate__A')  # <A>
_TriPredicate__B = typing.TypeVar('_TriPredicate__B')  # <B>
_TriPredicate__C = typing.TypeVar('_TriPredicate__C')  # <C>
class TriPredicate(typing.Generic[_TriPredicate__A, _TriPredicate__B, _TriPredicate__C]):
    """
    :class:`~org.optaplanner.core.api.function.https:.docs.oracle.com.javase.8.docs.api.java.lang.FunctionalInterface?is` public interface TriPredicate<A, B, C>
    
        Represents a predicate (boolean-valued function) of three arguments. This is the three-arity specialization of
        :class:`~org.optaplanner.core.api.function.https:.docs.oracle.com.javase.8.docs.api.java.util.function.Predicate?is`.
    
        This is a :class:`~org.optaplanner.core.api.function.package` whose functional method is
        :meth:`~org.optaplanner.core.api.function.TriPredicate.test`.
    
        Also see:
            :class:`~org.optaplanner.core.api.function.https:.docs.oracle.com.javase.8.docs.api.java.util.function.Predicate?is`
    """
    def negate(self) -> 'TriPredicate'[_TriPredicate__A, _TriPredicate__B, _TriPredicate__C]: ...
    def test(self, a: _TriPredicate__A, b: _TriPredicate__B, c: _TriPredicate__C) -> bool:
        """
            Evaluates this predicate on the given arguments.
        
            Parameters:
                a (:class:`~org.optaplanner.core.api.function.TriPredicate`): the first input argument
                b (:class:`~org.optaplanner.core.api.function.TriPredicate`): the second input argument
                c (:class:`~org.optaplanner.core.api.function.TriPredicate`): the third input argument
        
            Returns:
                :code:`true` if the input arguments match the predicate, otherwise :code:`false`
        
        
        """
        ...


class __module_protocol__(typing.Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.optaplanner.core.api.function")``.

    PentaFunction: typing.Type[PentaFunction]
    PentaPredicate: typing.Type[PentaPredicate]
    QuadFunction: typing.Type[QuadFunction]
    QuadPredicate: typing.Type[QuadPredicate]
    ToIntQuadFunction: typing.Type[ToIntQuadFunction]
    ToIntTriFunction: typing.Type[ToIntTriFunction]
    ToLongQuadFunction: typing.Type[ToLongQuadFunction]
    ToLongTriFunction: typing.Type[ToLongTriFunction]
    TriConsumer: typing.Type[TriConsumer]
    TriFunction: typing.Type[TriFunction]
    TriPredicate: typing.Type[TriPredicate]
