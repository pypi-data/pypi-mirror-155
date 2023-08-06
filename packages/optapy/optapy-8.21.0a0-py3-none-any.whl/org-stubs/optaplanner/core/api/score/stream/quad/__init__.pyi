import decimal
import java.lang
import java.math
import java.util.function
import org.optaplanner.core.api.function
import org.optaplanner.core.api.score
import org.optaplanner.core.api.score.stream
import org.optaplanner.core.api.score.stream.bi
import org.optaplanner.core.api.score.stream.penta
import org.optaplanner.core.api.score.stream.tri
import org.optaplanner.core.api.score.stream.uni
import typing



_QuadConstraintCollector__A = typing.TypeVar('_QuadConstraintCollector__A')  # <A>
_QuadConstraintCollector__B = typing.TypeVar('_QuadConstraintCollector__B')  # <B>
_QuadConstraintCollector__C = typing.TypeVar('_QuadConstraintCollector__C')  # <C>
_QuadConstraintCollector__D = typing.TypeVar('_QuadConstraintCollector__D')  # <D>
_QuadConstraintCollector__ResultContainer_ = typing.TypeVar('_QuadConstraintCollector__ResultContainer_')  # <ResultContainer_>
_QuadConstraintCollector__Result_ = typing.TypeVar('_QuadConstraintCollector__Result_')  # <Result_>
class QuadConstraintCollector(typing.Generic[_QuadConstraintCollector__A, _QuadConstraintCollector__B, _QuadConstraintCollector__C, _QuadConstraintCollector__D, _QuadConstraintCollector__ResultContainer_, _QuadConstraintCollector__Result_]):
    """
    public interface QuadConstraintCollector<A, B, C, D, ResultContainer_, Result_>
    
        Usually created with :class:`~org.optaplanner.core.api.score.stream.ConstraintCollectors`. Used by
        :meth:`~org.optaplanner.core.api.score.stream.quad.QuadConstraintStream.groupBy`, ...
    
        Loosely based on JDK's
        :class:`~org.optaplanner.core.api.score.stream.quad.https:.docs.oracle.com.javase.8.docs.api.java.util.stream.Collector?is`,
        but it returns an undo operation for each accumulation to enable incremental score calculation in
        :class:`~org.optaplanner.core.api.score.stream.ConstraintStream`.
    
        Also see:
            :class:`~org.optaplanner.core.api.score.stream.ConstraintCollectors`
    """
    def accumulator(self) -> org.optaplanner.core.api.function.PentaFunction[_QuadConstraintCollector__ResultContainer_, _QuadConstraintCollector__A, _QuadConstraintCollector__B, _QuadConstraintCollector__C, _QuadConstraintCollector__D, java.lang.Runnable]: ...
    def finisher(self) -> java.util.function.Function[_QuadConstraintCollector__ResultContainer_, _QuadConstraintCollector__Result_]: ...
    def supplier(self) -> java.util.function.Supplier[_QuadConstraintCollector__ResultContainer_]: ...

_QuadConstraintStream__A = typing.TypeVar('_QuadConstraintStream__A')  # <A>
_QuadConstraintStream__B = typing.TypeVar('_QuadConstraintStream__B')  # <B>
_QuadConstraintStream__C = typing.TypeVar('_QuadConstraintStream__C')  # <C>
_QuadConstraintStream__D = typing.TypeVar('_QuadConstraintStream__D')  # <D>
class QuadConstraintStream(org.optaplanner.core.api.score.stream.ConstraintStream, typing.Generic[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D]):
    """
    public interface QuadConstraintStream<A, B, C, D> extends :class:`~org.optaplanner.core.api.score.stream.ConstraintStream`
    
        A :class:`~org.optaplanner.core.api.score.stream.ConstraintStream` that matches four facts.
    
        Also see:
            :class:`~org.optaplanner.core.api.score.stream.ConstraintStream`
    """
    def distinct(self) -> 'QuadConstraintStream'[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D]: ...
    def filter(self, quadPredicate: typing.Union[org.optaplanner.core.api.function.QuadPredicate[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], typing.Callable[[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], bool]]) -> 'QuadConstraintStream'[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D]: ...
    _flattenLast__ResultD_ = typing.TypeVar('_flattenLast__ResultD_')  # <ResultD_>
    def flattenLast(self, function: typing.Union[java.util.function.Function[_QuadConstraintStream__D, typing.Union[java.lang.Iterable[_flattenLast__ResultD_], typing.Sequence[_flattenLast__ResultD_], typing.Set[_flattenLast__ResultD_]]], typing.Callable[[_QuadConstraintStream__D], typing.Union[java.lang.Iterable[_flattenLast__ResultD_], typing.Sequence[_flattenLast__ResultD_], typing.Set[_flattenLast__ResultD_]]]]) -> 'QuadConstraintStream'[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _flattenLast__ResultD_]: ...
    _groupBy_0__GroupKeyA_ = typing.TypeVar('_groupBy_0__GroupKeyA_')  # <GroupKeyA_>
    _groupBy_0__GroupKeyB_ = typing.TypeVar('_groupBy_0__GroupKeyB_')  # <GroupKeyB_>
    _groupBy_1__GroupKey_ = typing.TypeVar('_groupBy_1__GroupKey_')  # <GroupKey_>
    _groupBy_1__ResultContainer_ = typing.TypeVar('_groupBy_1__ResultContainer_')  # <ResultContainer_>
    _groupBy_1__Result_ = typing.TypeVar('_groupBy_1__Result_')  # <Result_>
    _groupBy_2__ResultContainerA_ = typing.TypeVar('_groupBy_2__ResultContainerA_')  # <ResultContainerA_>
    _groupBy_2__ResultA_ = typing.TypeVar('_groupBy_2__ResultA_')  # <ResultA_>
    _groupBy_2__ResultContainerB_ = typing.TypeVar('_groupBy_2__ResultContainerB_')  # <ResultContainerB_>
    _groupBy_2__ResultB_ = typing.TypeVar('_groupBy_2__ResultB_')  # <ResultB_>
    _groupBy_3__GroupKeyA_ = typing.TypeVar('_groupBy_3__GroupKeyA_')  # <GroupKeyA_>
    _groupBy_3__GroupKeyB_ = typing.TypeVar('_groupBy_3__GroupKeyB_')  # <GroupKeyB_>
    _groupBy_3__GroupKeyC_ = typing.TypeVar('_groupBy_3__GroupKeyC_')  # <GroupKeyC_>
    _groupBy_3__GroupKeyD_ = typing.TypeVar('_groupBy_3__GroupKeyD_')  # <GroupKeyD_>
    _groupBy_4__GroupKeyA_ = typing.TypeVar('_groupBy_4__GroupKeyA_')  # <GroupKeyA_>
    _groupBy_4__GroupKeyB_ = typing.TypeVar('_groupBy_4__GroupKeyB_')  # <GroupKeyB_>
    _groupBy_4__GroupKeyC_ = typing.TypeVar('_groupBy_4__GroupKeyC_')  # <GroupKeyC_>
    _groupBy_4__ResultContainerD_ = typing.TypeVar('_groupBy_4__ResultContainerD_')  # <ResultContainerD_>
    _groupBy_4__ResultD_ = typing.TypeVar('_groupBy_4__ResultD_')  # <ResultD_>
    _groupBy_5__GroupKeyA_ = typing.TypeVar('_groupBy_5__GroupKeyA_')  # <GroupKeyA_>
    _groupBy_5__GroupKeyB_ = typing.TypeVar('_groupBy_5__GroupKeyB_')  # <GroupKeyB_>
    _groupBy_5__ResultContainerC_ = typing.TypeVar('_groupBy_5__ResultContainerC_')  # <ResultContainerC_>
    _groupBy_5__ResultC_ = typing.TypeVar('_groupBy_5__ResultC_')  # <ResultC_>
    _groupBy_5__ResultContainerD_ = typing.TypeVar('_groupBy_5__ResultContainerD_')  # <ResultContainerD_>
    _groupBy_5__ResultD_ = typing.TypeVar('_groupBy_5__ResultD_')  # <ResultD_>
    _groupBy_6__GroupKey_ = typing.TypeVar('_groupBy_6__GroupKey_')  # <GroupKey_>
    _groupBy_6__ResultContainerB_ = typing.TypeVar('_groupBy_6__ResultContainerB_')  # <ResultContainerB_>
    _groupBy_6__ResultB_ = typing.TypeVar('_groupBy_6__ResultB_')  # <ResultB_>
    _groupBy_6__ResultContainerC_ = typing.TypeVar('_groupBy_6__ResultContainerC_')  # <ResultContainerC_>
    _groupBy_6__ResultC_ = typing.TypeVar('_groupBy_6__ResultC_')  # <ResultC_>
    _groupBy_6__ResultContainerD_ = typing.TypeVar('_groupBy_6__ResultContainerD_')  # <ResultContainerD_>
    _groupBy_6__ResultD_ = typing.TypeVar('_groupBy_6__ResultD_')  # <ResultD_>
    _groupBy_7__ResultContainerA_ = typing.TypeVar('_groupBy_7__ResultContainerA_')  # <ResultContainerA_>
    _groupBy_7__ResultA_ = typing.TypeVar('_groupBy_7__ResultA_')  # <ResultA_>
    _groupBy_7__ResultContainerB_ = typing.TypeVar('_groupBy_7__ResultContainerB_')  # <ResultContainerB_>
    _groupBy_7__ResultB_ = typing.TypeVar('_groupBy_7__ResultB_')  # <ResultB_>
    _groupBy_7__ResultContainerC_ = typing.TypeVar('_groupBy_7__ResultContainerC_')  # <ResultContainerC_>
    _groupBy_7__ResultC_ = typing.TypeVar('_groupBy_7__ResultC_')  # <ResultC_>
    _groupBy_7__ResultContainerD_ = typing.TypeVar('_groupBy_7__ResultContainerD_')  # <ResultContainerD_>
    _groupBy_7__ResultD_ = typing.TypeVar('_groupBy_7__ResultD_')  # <ResultD_>
    _groupBy_8__GroupKeyA_ = typing.TypeVar('_groupBy_8__GroupKeyA_')  # <GroupKeyA_>
    _groupBy_8__GroupKeyB_ = typing.TypeVar('_groupBy_8__GroupKeyB_')  # <GroupKeyB_>
    _groupBy_8__GroupKeyC_ = typing.TypeVar('_groupBy_8__GroupKeyC_')  # <GroupKeyC_>
    _groupBy_9__GroupKeyA_ = typing.TypeVar('_groupBy_9__GroupKeyA_')  # <GroupKeyA_>
    _groupBy_9__GroupKeyB_ = typing.TypeVar('_groupBy_9__GroupKeyB_')  # <GroupKeyB_>
    _groupBy_9__ResultContainer_ = typing.TypeVar('_groupBy_9__ResultContainer_')  # <ResultContainer_>
    _groupBy_9__Result_ = typing.TypeVar('_groupBy_9__Result_')  # <Result_>
    _groupBy_10__GroupKey_ = typing.TypeVar('_groupBy_10__GroupKey_')  # <GroupKey_>
    _groupBy_10__ResultContainerB_ = typing.TypeVar('_groupBy_10__ResultContainerB_')  # <ResultContainerB_>
    _groupBy_10__ResultB_ = typing.TypeVar('_groupBy_10__ResultB_')  # <ResultB_>
    _groupBy_10__ResultContainerC_ = typing.TypeVar('_groupBy_10__ResultContainerC_')  # <ResultContainerC_>
    _groupBy_10__ResultC_ = typing.TypeVar('_groupBy_10__ResultC_')  # <ResultC_>
    _groupBy_11__ResultContainerA_ = typing.TypeVar('_groupBy_11__ResultContainerA_')  # <ResultContainerA_>
    _groupBy_11__ResultA_ = typing.TypeVar('_groupBy_11__ResultA_')  # <ResultA_>
    _groupBy_11__ResultContainerB_ = typing.TypeVar('_groupBy_11__ResultContainerB_')  # <ResultContainerB_>
    _groupBy_11__ResultB_ = typing.TypeVar('_groupBy_11__ResultB_')  # <ResultB_>
    _groupBy_11__ResultContainerC_ = typing.TypeVar('_groupBy_11__ResultContainerC_')  # <ResultContainerC_>
    _groupBy_11__ResultC_ = typing.TypeVar('_groupBy_11__ResultC_')  # <ResultC_>
    _groupBy_12__GroupKey_ = typing.TypeVar('_groupBy_12__GroupKey_')  # <GroupKey_>
    _groupBy_13__ResultContainer_ = typing.TypeVar('_groupBy_13__ResultContainer_')  # <ResultContainer_>
    _groupBy_13__Result_ = typing.TypeVar('_groupBy_13__Result_')  # <Result_>
    @typing.overload
    def groupBy(self, quadFunction: typing.Union[org.optaplanner.core.api.function.QuadFunction[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _groupBy_0__GroupKeyA_], typing.Callable[[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], _groupBy_0__GroupKeyA_]], quadFunction2: typing.Union[org.optaplanner.core.api.function.QuadFunction[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _groupBy_0__GroupKeyB_], typing.Callable[[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], _groupBy_0__GroupKeyB_]]) -> org.optaplanner.core.api.score.stream.bi.BiConstraintStream[_groupBy_0__GroupKeyA_, _groupBy_0__GroupKeyB_]: ...
    @typing.overload
    def groupBy(self, quadFunction: typing.Union[org.optaplanner.core.api.function.QuadFunction[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _groupBy_1__GroupKey_], typing.Callable[[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], _groupBy_1__GroupKey_]], quadConstraintCollector: QuadConstraintCollector[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _groupBy_1__ResultContainer_, _groupBy_1__Result_]) -> org.optaplanner.core.api.score.stream.bi.BiConstraintStream[_groupBy_1__GroupKey_, _groupBy_1__Result_]: ...
    @typing.overload
    def groupBy(self, quadConstraintCollector: QuadConstraintCollector[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _groupBy_2__ResultContainerA_, _groupBy_2__ResultA_], quadConstraintCollector2: QuadConstraintCollector[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _groupBy_2__ResultContainerB_, _groupBy_2__ResultB_]) -> org.optaplanner.core.api.score.stream.bi.BiConstraintStream[_groupBy_2__ResultA_, _groupBy_2__ResultB_]: ...
    @typing.overload
    def groupBy(self, quadFunction: typing.Union[org.optaplanner.core.api.function.QuadFunction[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _groupBy_3__GroupKeyA_], typing.Callable[[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], _groupBy_3__GroupKeyA_]], quadFunction2: typing.Union[org.optaplanner.core.api.function.QuadFunction[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _groupBy_3__GroupKeyB_], typing.Callable[[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], _groupBy_3__GroupKeyB_]], quadFunction3: typing.Union[org.optaplanner.core.api.function.QuadFunction[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _groupBy_3__GroupKeyC_], typing.Callable[[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], _groupBy_3__GroupKeyC_]], quadFunction4: typing.Union[org.optaplanner.core.api.function.QuadFunction[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _groupBy_3__GroupKeyD_], typing.Callable[[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], _groupBy_3__GroupKeyD_]]) -> 'QuadConstraintStream'[_groupBy_3__GroupKeyA_, _groupBy_3__GroupKeyB_, _groupBy_3__GroupKeyC_, _groupBy_3__GroupKeyD_]: ...
    @typing.overload
    def groupBy(self, quadFunction: typing.Union[org.optaplanner.core.api.function.QuadFunction[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _groupBy_4__GroupKeyA_], typing.Callable[[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], _groupBy_4__GroupKeyA_]], quadFunction2: typing.Union[org.optaplanner.core.api.function.QuadFunction[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _groupBy_4__GroupKeyB_], typing.Callable[[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], _groupBy_4__GroupKeyB_]], quadFunction3: typing.Union[org.optaplanner.core.api.function.QuadFunction[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _groupBy_4__GroupKeyC_], typing.Callable[[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], _groupBy_4__GroupKeyC_]], quadConstraintCollector: QuadConstraintCollector[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _groupBy_4__ResultContainerD_, _groupBy_4__ResultD_]) -> 'QuadConstraintStream'[_groupBy_4__GroupKeyA_, _groupBy_4__GroupKeyB_, _groupBy_4__GroupKeyC_, _groupBy_4__ResultD_]: ...
    @typing.overload
    def groupBy(self, quadFunction: typing.Union[org.optaplanner.core.api.function.QuadFunction[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _groupBy_5__GroupKeyA_], typing.Callable[[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], _groupBy_5__GroupKeyA_]], quadFunction2: typing.Union[org.optaplanner.core.api.function.QuadFunction[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _groupBy_5__GroupKeyB_], typing.Callable[[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], _groupBy_5__GroupKeyB_]], quadConstraintCollector: QuadConstraintCollector[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _groupBy_5__ResultContainerC_, _groupBy_5__ResultC_], quadConstraintCollector2: QuadConstraintCollector[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _groupBy_5__ResultContainerD_, _groupBy_5__ResultD_]) -> 'QuadConstraintStream'[_groupBy_5__GroupKeyA_, _groupBy_5__GroupKeyB_, _groupBy_5__ResultC_, _groupBy_5__ResultD_]: ...
    @typing.overload
    def groupBy(self, quadFunction: typing.Union[org.optaplanner.core.api.function.QuadFunction[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _groupBy_6__GroupKey_], typing.Callable[[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], _groupBy_6__GroupKey_]], quadConstraintCollector: QuadConstraintCollector[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _groupBy_6__ResultContainerB_, _groupBy_6__ResultB_], quadConstraintCollector2: QuadConstraintCollector[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _groupBy_6__ResultContainerC_, _groupBy_6__ResultC_], quadConstraintCollector3: QuadConstraintCollector[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _groupBy_6__ResultContainerD_, _groupBy_6__ResultD_]) -> 'QuadConstraintStream'[_groupBy_6__GroupKey_, _groupBy_6__ResultB_, _groupBy_6__ResultC_, _groupBy_6__ResultD_]: ...
    @typing.overload
    def groupBy(self, quadConstraintCollector: QuadConstraintCollector[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _groupBy_7__ResultContainerA_, _groupBy_7__ResultA_], quadConstraintCollector2: QuadConstraintCollector[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _groupBy_7__ResultContainerB_, _groupBy_7__ResultB_], quadConstraintCollector3: QuadConstraintCollector[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _groupBy_7__ResultContainerC_, _groupBy_7__ResultC_], quadConstraintCollector4: QuadConstraintCollector[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _groupBy_7__ResultContainerD_, _groupBy_7__ResultD_]) -> 'QuadConstraintStream'[_groupBy_7__ResultA_, _groupBy_7__ResultB_, _groupBy_7__ResultC_, _groupBy_7__ResultD_]: ...
    @typing.overload
    def groupBy(self, quadFunction: typing.Union[org.optaplanner.core.api.function.QuadFunction[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _groupBy_8__GroupKeyA_], typing.Callable[[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], _groupBy_8__GroupKeyA_]], quadFunction2: typing.Union[org.optaplanner.core.api.function.QuadFunction[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _groupBy_8__GroupKeyB_], typing.Callable[[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], _groupBy_8__GroupKeyB_]], quadFunction3: typing.Union[org.optaplanner.core.api.function.QuadFunction[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _groupBy_8__GroupKeyC_], typing.Callable[[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], _groupBy_8__GroupKeyC_]]) -> org.optaplanner.core.api.score.stream.tri.TriConstraintStream[_groupBy_8__GroupKeyA_, _groupBy_8__GroupKeyB_, _groupBy_8__GroupKeyC_]: ...
    @typing.overload
    def groupBy(self, quadFunction: typing.Union[org.optaplanner.core.api.function.QuadFunction[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _groupBy_9__GroupKeyA_], typing.Callable[[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], _groupBy_9__GroupKeyA_]], quadFunction2: typing.Union[org.optaplanner.core.api.function.QuadFunction[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _groupBy_9__GroupKeyB_], typing.Callable[[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], _groupBy_9__GroupKeyB_]], quadConstraintCollector: QuadConstraintCollector[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _groupBy_9__ResultContainer_, _groupBy_9__Result_]) -> org.optaplanner.core.api.score.stream.tri.TriConstraintStream[_groupBy_9__GroupKeyA_, _groupBy_9__GroupKeyB_, _groupBy_9__Result_]: ...
    @typing.overload
    def groupBy(self, quadFunction: typing.Union[org.optaplanner.core.api.function.QuadFunction[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _groupBy_10__GroupKey_], typing.Callable[[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], _groupBy_10__GroupKey_]], quadConstraintCollector: QuadConstraintCollector[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _groupBy_10__ResultContainerB_, _groupBy_10__ResultB_], quadConstraintCollector2: QuadConstraintCollector[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _groupBy_10__ResultContainerC_, _groupBy_10__ResultC_]) -> org.optaplanner.core.api.score.stream.tri.TriConstraintStream[_groupBy_10__GroupKey_, _groupBy_10__ResultB_, _groupBy_10__ResultC_]: ...
    @typing.overload
    def groupBy(self, quadConstraintCollector: QuadConstraintCollector[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _groupBy_11__ResultContainerA_, _groupBy_11__ResultA_], quadConstraintCollector2: QuadConstraintCollector[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _groupBy_11__ResultContainerB_, _groupBy_11__ResultB_], quadConstraintCollector3: QuadConstraintCollector[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _groupBy_11__ResultContainerC_, _groupBy_11__ResultC_]) -> org.optaplanner.core.api.score.stream.tri.TriConstraintStream[_groupBy_11__ResultA_, _groupBy_11__ResultB_, _groupBy_11__ResultC_]: ...
    @typing.overload
    def groupBy(self, quadFunction: typing.Union[org.optaplanner.core.api.function.QuadFunction[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _groupBy_12__GroupKey_], typing.Callable[[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], _groupBy_12__GroupKey_]]) -> org.optaplanner.core.api.score.stream.uni.UniConstraintStream[_groupBy_12__GroupKey_]: ...
    @typing.overload
    def groupBy(self, quadConstraintCollector: QuadConstraintCollector[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _groupBy_13__ResultContainer_, _groupBy_13__Result_]) -> org.optaplanner.core.api.score.stream.uni.UniConstraintStream[_groupBy_13__Result_]: ...
    _ifExists_0__E = typing.TypeVar('_ifExists_0__E')  # <E>
    _ifExists_1__E = typing.TypeVar('_ifExists_1__E')  # <E>
    _ifExists_2__E = typing.TypeVar('_ifExists_2__E')  # <E>
    _ifExists_3__E = typing.TypeVar('_ifExists_3__E')  # <E>
    _ifExists_4__E = typing.TypeVar('_ifExists_4__E')  # <E>
    @typing.overload
    def ifExists(self, class_: typing.Type[_ifExists_0__E], *pentaJoiner: org.optaplanner.core.api.score.stream.penta.PentaJoiner[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _ifExists_0__E]) -> 'QuadConstraintStream'[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D]: ...
    @typing.overload
    def ifExists(self, class_: typing.Type[_ifExists_1__E], pentaJoiner: org.optaplanner.core.api.score.stream.penta.PentaJoiner[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _ifExists_1__E]) -> 'QuadConstraintStream'[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D]: ...
    @typing.overload
    def ifExists(self, class_: typing.Type[_ifExists_2__E], pentaJoiner: org.optaplanner.core.api.score.stream.penta.PentaJoiner[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _ifExists_2__E], pentaJoiner2: org.optaplanner.core.api.score.stream.penta.PentaJoiner[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _ifExists_2__E]) -> 'QuadConstraintStream'[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D]: ...
    @typing.overload
    def ifExists(self, class_: typing.Type[_ifExists_3__E], pentaJoiner: org.optaplanner.core.api.score.stream.penta.PentaJoiner[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _ifExists_3__E], pentaJoiner2: org.optaplanner.core.api.score.stream.penta.PentaJoiner[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _ifExists_3__E], pentaJoiner3: org.optaplanner.core.api.score.stream.penta.PentaJoiner[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _ifExists_3__E]) -> 'QuadConstraintStream'[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D]: ...
    @typing.overload
    def ifExists(self, class_: typing.Type[_ifExists_4__E], pentaJoiner: org.optaplanner.core.api.score.stream.penta.PentaJoiner[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _ifExists_4__E], pentaJoiner2: org.optaplanner.core.api.score.stream.penta.PentaJoiner[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _ifExists_4__E], pentaJoiner3: org.optaplanner.core.api.score.stream.penta.PentaJoiner[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _ifExists_4__E], pentaJoiner4: org.optaplanner.core.api.score.stream.penta.PentaJoiner[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _ifExists_4__E]) -> 'QuadConstraintStream'[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D]: ...
    _ifExistsIncludingNullVars_0__E = typing.TypeVar('_ifExistsIncludingNullVars_0__E')  # <E>
    _ifExistsIncludingNullVars_1__E = typing.TypeVar('_ifExistsIncludingNullVars_1__E')  # <E>
    _ifExistsIncludingNullVars_2__E = typing.TypeVar('_ifExistsIncludingNullVars_2__E')  # <E>
    _ifExistsIncludingNullVars_3__E = typing.TypeVar('_ifExistsIncludingNullVars_3__E')  # <E>
    _ifExistsIncludingNullVars_4__E = typing.TypeVar('_ifExistsIncludingNullVars_4__E')  # <E>
    @typing.overload
    def ifExistsIncludingNullVars(self, class_: typing.Type[_ifExistsIncludingNullVars_0__E], *pentaJoiner: org.optaplanner.core.api.score.stream.penta.PentaJoiner[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _ifExistsIncludingNullVars_0__E]) -> 'QuadConstraintStream'[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D]: ...
    @typing.overload
    def ifExistsIncludingNullVars(self, class_: typing.Type[_ifExistsIncludingNullVars_1__E], pentaJoiner: org.optaplanner.core.api.score.stream.penta.PentaJoiner[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _ifExistsIncludingNullVars_1__E]) -> 'QuadConstraintStream'[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D]: ...
    @typing.overload
    def ifExistsIncludingNullVars(self, class_: typing.Type[_ifExistsIncludingNullVars_2__E], pentaJoiner: org.optaplanner.core.api.score.stream.penta.PentaJoiner[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _ifExistsIncludingNullVars_2__E], pentaJoiner2: org.optaplanner.core.api.score.stream.penta.PentaJoiner[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _ifExistsIncludingNullVars_2__E]) -> 'QuadConstraintStream'[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D]: ...
    @typing.overload
    def ifExistsIncludingNullVars(self, class_: typing.Type[_ifExistsIncludingNullVars_3__E], pentaJoiner: org.optaplanner.core.api.score.stream.penta.PentaJoiner[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _ifExistsIncludingNullVars_3__E], pentaJoiner2: org.optaplanner.core.api.score.stream.penta.PentaJoiner[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _ifExistsIncludingNullVars_3__E], pentaJoiner3: org.optaplanner.core.api.score.stream.penta.PentaJoiner[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _ifExistsIncludingNullVars_3__E]) -> 'QuadConstraintStream'[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D]: ...
    @typing.overload
    def ifExistsIncludingNullVars(self, class_: typing.Type[_ifExistsIncludingNullVars_4__E], pentaJoiner: org.optaplanner.core.api.score.stream.penta.PentaJoiner[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _ifExistsIncludingNullVars_4__E], pentaJoiner2: org.optaplanner.core.api.score.stream.penta.PentaJoiner[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _ifExistsIncludingNullVars_4__E], pentaJoiner3: org.optaplanner.core.api.score.stream.penta.PentaJoiner[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _ifExistsIncludingNullVars_4__E], pentaJoiner4: org.optaplanner.core.api.score.stream.penta.PentaJoiner[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _ifExistsIncludingNullVars_4__E]) -> 'QuadConstraintStream'[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D]: ...
    _ifNotExists_0__E = typing.TypeVar('_ifNotExists_0__E')  # <E>
    _ifNotExists_1__E = typing.TypeVar('_ifNotExists_1__E')  # <E>
    _ifNotExists_2__E = typing.TypeVar('_ifNotExists_2__E')  # <E>
    _ifNotExists_3__E = typing.TypeVar('_ifNotExists_3__E')  # <E>
    _ifNotExists_4__E = typing.TypeVar('_ifNotExists_4__E')  # <E>
    @typing.overload
    def ifNotExists(self, class_: typing.Type[_ifNotExists_0__E], *pentaJoiner: org.optaplanner.core.api.score.stream.penta.PentaJoiner[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _ifNotExists_0__E]) -> 'QuadConstraintStream'[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D]: ...
    @typing.overload
    def ifNotExists(self, class_: typing.Type[_ifNotExists_1__E], pentaJoiner: org.optaplanner.core.api.score.stream.penta.PentaJoiner[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _ifNotExists_1__E]) -> 'QuadConstraintStream'[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D]: ...
    @typing.overload
    def ifNotExists(self, class_: typing.Type[_ifNotExists_2__E], pentaJoiner: org.optaplanner.core.api.score.stream.penta.PentaJoiner[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _ifNotExists_2__E], pentaJoiner2: org.optaplanner.core.api.score.stream.penta.PentaJoiner[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _ifNotExists_2__E]) -> 'QuadConstraintStream'[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D]: ...
    @typing.overload
    def ifNotExists(self, class_: typing.Type[_ifNotExists_3__E], pentaJoiner: org.optaplanner.core.api.score.stream.penta.PentaJoiner[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _ifNotExists_3__E], pentaJoiner2: org.optaplanner.core.api.score.stream.penta.PentaJoiner[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _ifNotExists_3__E], pentaJoiner3: org.optaplanner.core.api.score.stream.penta.PentaJoiner[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _ifNotExists_3__E]) -> 'QuadConstraintStream'[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D]: ...
    @typing.overload
    def ifNotExists(self, class_: typing.Type[_ifNotExists_4__E], pentaJoiner: org.optaplanner.core.api.score.stream.penta.PentaJoiner[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _ifNotExists_4__E], pentaJoiner2: org.optaplanner.core.api.score.stream.penta.PentaJoiner[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _ifNotExists_4__E], pentaJoiner3: org.optaplanner.core.api.score.stream.penta.PentaJoiner[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _ifNotExists_4__E], pentaJoiner4: org.optaplanner.core.api.score.stream.penta.PentaJoiner[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _ifNotExists_4__E]) -> 'QuadConstraintStream'[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D]: ...
    _ifNotExistsIncludingNullVars_0__E = typing.TypeVar('_ifNotExistsIncludingNullVars_0__E')  # <E>
    _ifNotExistsIncludingNullVars_1__E = typing.TypeVar('_ifNotExistsIncludingNullVars_1__E')  # <E>
    _ifNotExistsIncludingNullVars_2__E = typing.TypeVar('_ifNotExistsIncludingNullVars_2__E')  # <E>
    _ifNotExistsIncludingNullVars_3__E = typing.TypeVar('_ifNotExistsIncludingNullVars_3__E')  # <E>
    _ifNotExistsIncludingNullVars_4__E = typing.TypeVar('_ifNotExistsIncludingNullVars_4__E')  # <E>
    @typing.overload
    def ifNotExistsIncludingNullVars(self, class_: typing.Type[_ifNotExistsIncludingNullVars_0__E], *pentaJoiner: org.optaplanner.core.api.score.stream.penta.PentaJoiner[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _ifNotExistsIncludingNullVars_0__E]) -> 'QuadConstraintStream'[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D]: ...
    @typing.overload
    def ifNotExistsIncludingNullVars(self, class_: typing.Type[_ifNotExistsIncludingNullVars_1__E], pentaJoiner: org.optaplanner.core.api.score.stream.penta.PentaJoiner[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _ifNotExistsIncludingNullVars_1__E]) -> 'QuadConstraintStream'[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D]: ...
    @typing.overload
    def ifNotExistsIncludingNullVars(self, class_: typing.Type[_ifNotExistsIncludingNullVars_2__E], pentaJoiner: org.optaplanner.core.api.score.stream.penta.PentaJoiner[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _ifNotExistsIncludingNullVars_2__E], pentaJoiner2: org.optaplanner.core.api.score.stream.penta.PentaJoiner[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _ifNotExistsIncludingNullVars_2__E]) -> 'QuadConstraintStream'[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D]: ...
    @typing.overload
    def ifNotExistsIncludingNullVars(self, class_: typing.Type[_ifNotExistsIncludingNullVars_3__E], pentaJoiner: org.optaplanner.core.api.score.stream.penta.PentaJoiner[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _ifNotExistsIncludingNullVars_3__E], pentaJoiner2: org.optaplanner.core.api.score.stream.penta.PentaJoiner[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _ifNotExistsIncludingNullVars_3__E], pentaJoiner3: org.optaplanner.core.api.score.stream.penta.PentaJoiner[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _ifNotExistsIncludingNullVars_3__E]) -> 'QuadConstraintStream'[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D]: ...
    @typing.overload
    def ifNotExistsIncludingNullVars(self, class_: typing.Type[_ifNotExistsIncludingNullVars_4__E], pentaJoiner: org.optaplanner.core.api.score.stream.penta.PentaJoiner[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _ifNotExistsIncludingNullVars_4__E], pentaJoiner2: org.optaplanner.core.api.score.stream.penta.PentaJoiner[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _ifNotExistsIncludingNullVars_4__E], pentaJoiner3: org.optaplanner.core.api.score.stream.penta.PentaJoiner[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _ifNotExistsIncludingNullVars_4__E], pentaJoiner4: org.optaplanner.core.api.score.stream.penta.PentaJoiner[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _ifNotExistsIncludingNullVars_4__E]) -> 'QuadConstraintStream'[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D]: ...
    @typing.overload
    def impact(self, string: str, string2: str, score: org.optaplanner.core.api.score.Score[typing.Any]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def impact(self, string: str, string2: str, score: org.optaplanner.core.api.score.Score[typing.Any], toIntQuadFunction: typing.Union[org.optaplanner.core.api.function.ToIntQuadFunction[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], typing.Callable[[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], int]]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def impact(self, string: str, score: org.optaplanner.core.api.score.Score[typing.Any]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def impact(self, string: str, score: org.optaplanner.core.api.score.Score[typing.Any], toIntQuadFunction: typing.Union[org.optaplanner.core.api.function.ToIntQuadFunction[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], typing.Callable[[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], int]]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def impactBigDecimal(self, string: str, string2: str, score: org.optaplanner.core.api.score.Score[typing.Any], quadFunction: typing.Union[org.optaplanner.core.api.function.QuadFunction[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, typing.Union[java.math.BigDecimal, decimal.Decimal]], typing.Callable[[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], typing.Union[java.math.BigDecimal, decimal.Decimal]]]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def impactBigDecimal(self, string: str, score: org.optaplanner.core.api.score.Score[typing.Any], quadFunction: typing.Union[org.optaplanner.core.api.function.QuadFunction[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, typing.Union[java.math.BigDecimal, decimal.Decimal]], typing.Callable[[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], typing.Union[java.math.BigDecimal, decimal.Decimal]]]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def impactConfigurable(self, string: str, string2: str, toIntQuadFunction: typing.Union[org.optaplanner.core.api.function.ToIntQuadFunction[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], typing.Callable[[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], int]]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def impactConfigurable(self, string: str, toIntQuadFunction: typing.Union[org.optaplanner.core.api.function.ToIntQuadFunction[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], typing.Callable[[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], int]]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def impactConfigurableBigDecimal(self, string: str, string2: str, quadFunction: typing.Union[org.optaplanner.core.api.function.QuadFunction[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, typing.Union[java.math.BigDecimal, decimal.Decimal]], typing.Callable[[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], typing.Union[java.math.BigDecimal, decimal.Decimal]]]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def impactConfigurableBigDecimal(self, string: str, quadFunction: typing.Union[org.optaplanner.core.api.function.QuadFunction[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, typing.Union[java.math.BigDecimal, decimal.Decimal]], typing.Callable[[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], typing.Union[java.math.BigDecimal, decimal.Decimal]]]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def impactConfigurableLong(self, string: str, string2: str, toLongQuadFunction: typing.Union[org.optaplanner.core.api.function.ToLongQuadFunction[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], typing.Callable[[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], int]]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def impactConfigurableLong(self, string: str, toLongQuadFunction: typing.Union[org.optaplanner.core.api.function.ToLongQuadFunction[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], typing.Callable[[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], int]]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def impactLong(self, string: str, string2: str, score: org.optaplanner.core.api.score.Score[typing.Any], toLongQuadFunction: typing.Union[org.optaplanner.core.api.function.ToLongQuadFunction[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], typing.Callable[[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], int]]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def impactLong(self, string: str, score: org.optaplanner.core.api.score.Score[typing.Any], toLongQuadFunction: typing.Union[org.optaplanner.core.api.function.ToLongQuadFunction[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], typing.Callable[[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], int]]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    _map__ResultA_ = typing.TypeVar('_map__ResultA_')  # <ResultA_>
    def map(self, quadFunction: typing.Union[org.optaplanner.core.api.function.QuadFunction[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, _map__ResultA_], typing.Callable[[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], _map__ResultA_]]) -> org.optaplanner.core.api.score.stream.uni.UniConstraintStream[_map__ResultA_]: ...
    @typing.overload
    def penalize(self, string: str, string2: str, score: org.optaplanner.core.api.score.Score[typing.Any]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def penalize(self, string: str, string2: str, score: org.optaplanner.core.api.score.Score[typing.Any], toIntQuadFunction: typing.Union[org.optaplanner.core.api.function.ToIntQuadFunction[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], typing.Callable[[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], int]]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def penalize(self, string: str, score: org.optaplanner.core.api.score.Score[typing.Any]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def penalize(self, string: str, score: org.optaplanner.core.api.score.Score[typing.Any], toIntQuadFunction: typing.Union[org.optaplanner.core.api.function.ToIntQuadFunction[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], typing.Callable[[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], int]]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def penalizeBigDecimal(self, string: str, string2: str, score: org.optaplanner.core.api.score.Score[typing.Any], quadFunction: typing.Union[org.optaplanner.core.api.function.QuadFunction[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, typing.Union[java.math.BigDecimal, decimal.Decimal]], typing.Callable[[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], typing.Union[java.math.BigDecimal, decimal.Decimal]]]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def penalizeBigDecimal(self, string: str, score: org.optaplanner.core.api.score.Score[typing.Any], quadFunction: typing.Union[org.optaplanner.core.api.function.QuadFunction[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, typing.Union[java.math.BigDecimal, decimal.Decimal]], typing.Callable[[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], typing.Union[java.math.BigDecimal, decimal.Decimal]]]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def penalizeConfigurable(self, string: str, string2: str) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def penalizeConfigurable(self, string: str, string2: str, toIntQuadFunction: typing.Union[org.optaplanner.core.api.function.ToIntQuadFunction[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], typing.Callable[[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], int]]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def penalizeConfigurable(self, string: str) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def penalizeConfigurable(self, string: str, toIntQuadFunction: typing.Union[org.optaplanner.core.api.function.ToIntQuadFunction[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], typing.Callable[[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], int]]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def penalizeConfigurableBigDecimal(self, string: str, string2: str, quadFunction: typing.Union[org.optaplanner.core.api.function.QuadFunction[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, typing.Union[java.math.BigDecimal, decimal.Decimal]], typing.Callable[[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], typing.Union[java.math.BigDecimal, decimal.Decimal]]]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def penalizeConfigurableBigDecimal(self, string: str, quadFunction: typing.Union[org.optaplanner.core.api.function.QuadFunction[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, typing.Union[java.math.BigDecimal, decimal.Decimal]], typing.Callable[[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], typing.Union[java.math.BigDecimal, decimal.Decimal]]]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def penalizeConfigurableLong(self, string: str, string2: str, toLongQuadFunction: typing.Union[org.optaplanner.core.api.function.ToLongQuadFunction[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], typing.Callable[[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], int]]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def penalizeConfigurableLong(self, string: str, toLongQuadFunction: typing.Union[org.optaplanner.core.api.function.ToLongQuadFunction[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], typing.Callable[[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], int]]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def penalizeLong(self, string: str, string2: str, score: org.optaplanner.core.api.score.Score[typing.Any], toLongQuadFunction: typing.Union[org.optaplanner.core.api.function.ToLongQuadFunction[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], typing.Callable[[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], int]]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def penalizeLong(self, string: str, score: org.optaplanner.core.api.score.Score[typing.Any], toLongQuadFunction: typing.Union[org.optaplanner.core.api.function.ToLongQuadFunction[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], typing.Callable[[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], int]]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def reward(self, string: str, string2: str, score: org.optaplanner.core.api.score.Score[typing.Any]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def reward(self, string: str, string2: str, score: org.optaplanner.core.api.score.Score[typing.Any], toIntQuadFunction: typing.Union[org.optaplanner.core.api.function.ToIntQuadFunction[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], typing.Callable[[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], int]]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def reward(self, string: str, score: org.optaplanner.core.api.score.Score[typing.Any]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def reward(self, string: str, score: org.optaplanner.core.api.score.Score[typing.Any], toIntQuadFunction: typing.Union[org.optaplanner.core.api.function.ToIntQuadFunction[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], typing.Callable[[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], int]]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def rewardBigDecimal(self, string: str, string2: str, score: org.optaplanner.core.api.score.Score[typing.Any], quadFunction: typing.Union[org.optaplanner.core.api.function.QuadFunction[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, typing.Union[java.math.BigDecimal, decimal.Decimal]], typing.Callable[[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], typing.Union[java.math.BigDecimal, decimal.Decimal]]]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def rewardBigDecimal(self, string: str, score: org.optaplanner.core.api.score.Score[typing.Any], quadFunction: typing.Union[org.optaplanner.core.api.function.QuadFunction[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, typing.Union[java.math.BigDecimal, decimal.Decimal]], typing.Callable[[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], typing.Union[java.math.BigDecimal, decimal.Decimal]]]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def rewardConfigurable(self, string: str, string2: str) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def rewardConfigurable(self, string: str, string2: str, toIntQuadFunction: typing.Union[org.optaplanner.core.api.function.ToIntQuadFunction[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], typing.Callable[[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], int]]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def rewardConfigurable(self, string: str) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def rewardConfigurable(self, string: str, toIntQuadFunction: typing.Union[org.optaplanner.core.api.function.ToIntQuadFunction[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], typing.Callable[[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], int]]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def rewardConfigurableBigDecimal(self, string: str, string2: str, quadFunction: typing.Union[org.optaplanner.core.api.function.QuadFunction[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, typing.Union[java.math.BigDecimal, decimal.Decimal]], typing.Callable[[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], typing.Union[java.math.BigDecimal, decimal.Decimal]]]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def rewardConfigurableBigDecimal(self, string: str, quadFunction: typing.Union[org.optaplanner.core.api.function.QuadFunction[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D, typing.Union[java.math.BigDecimal, decimal.Decimal]], typing.Callable[[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], typing.Union[java.math.BigDecimal, decimal.Decimal]]]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def rewardConfigurableLong(self, string: str, string2: str, toLongQuadFunction: typing.Union[org.optaplanner.core.api.function.ToLongQuadFunction[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], typing.Callable[[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], int]]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def rewardConfigurableLong(self, string: str, toLongQuadFunction: typing.Union[org.optaplanner.core.api.function.ToLongQuadFunction[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], typing.Callable[[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], int]]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def rewardLong(self, string: str, string2: str, score: org.optaplanner.core.api.score.Score[typing.Any], toLongQuadFunction: typing.Union[org.optaplanner.core.api.function.ToLongQuadFunction[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], typing.Callable[[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], int]]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def rewardLong(self, string: str, score: org.optaplanner.core.api.score.Score[typing.Any], toLongQuadFunction: typing.Union[org.optaplanner.core.api.function.ToLongQuadFunction[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], typing.Callable[[_QuadConstraintStream__A, _QuadConstraintStream__B, _QuadConstraintStream__C, _QuadConstraintStream__D], int]]) -> org.optaplanner.core.api.score.stream.Constraint: ...

_QuadJoiner__A = typing.TypeVar('_QuadJoiner__A')  # <A>
_QuadJoiner__B = typing.TypeVar('_QuadJoiner__B')  # <B>
_QuadJoiner__C = typing.TypeVar('_QuadJoiner__C')  # <C>
_QuadJoiner__D = typing.TypeVar('_QuadJoiner__D')  # <D>
class QuadJoiner(typing.Generic[_QuadJoiner__A, _QuadJoiner__B, _QuadJoiner__C, _QuadJoiner__D]):
    """
    public interface QuadJoiner<A, B, C, D>
    
        Created with :class:`~org.optaplanner.core.api.score.stream.Joiners`. Used by
        :meth:`~org.optaplanner.core.api.score.stream.tri.TriConstraintStream.join`, ...
    
        Also see:
            :class:`~org.optaplanner.core.api.score.stream.Joiners`
    """
    ...


class __module_protocol__(typing.Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.optaplanner.core.api.score.stream.quad")``.

    QuadConstraintCollector: typing.Type[QuadConstraintCollector]
    QuadConstraintStream: typing.Type[QuadConstraintStream]
    QuadJoiner: typing.Type[QuadJoiner]
