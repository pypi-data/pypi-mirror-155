import decimal
import java.lang
import java.math
import java.util.function
import org.optaplanner.core.api.function
import org.optaplanner.core.api.score
import org.optaplanner.core.api.score.stream
import org.optaplanner.core.api.score.stream.quad
import org.optaplanner.core.api.score.stream.tri
import org.optaplanner.core.api.score.stream.uni
import typing



_BiConstraintCollector__A = typing.TypeVar('_BiConstraintCollector__A')  # <A>
_BiConstraintCollector__B = typing.TypeVar('_BiConstraintCollector__B')  # <B>
_BiConstraintCollector__ResultContainer_ = typing.TypeVar('_BiConstraintCollector__ResultContainer_')  # <ResultContainer_>
_BiConstraintCollector__Result_ = typing.TypeVar('_BiConstraintCollector__Result_')  # <Result_>
class BiConstraintCollector(typing.Generic[_BiConstraintCollector__A, _BiConstraintCollector__B, _BiConstraintCollector__ResultContainer_, _BiConstraintCollector__Result_]):
    """
    public interface BiConstraintCollector<A, B, ResultContainer_, Result_>
    
        Usually created with :class:`~org.optaplanner.core.api.score.stream.ConstraintCollectors`. Used by
        :meth:`~org.optaplanner.core.api.score.stream.bi.BiConstraintStream.groupBy`, ...
    
        Loosely based on JDK's
        :class:`~org.optaplanner.core.api.score.stream.bi.https:.docs.oracle.com.javase.8.docs.api.java.util.stream.Collector?is`,
        but it returns an undo operation for each accumulation to enable incremental score calculation in
        :class:`~org.optaplanner.core.api.score.stream.ConstraintStream`.
    
        Also see:
            :class:`~org.optaplanner.core.api.score.stream.ConstraintCollectors`
    """
    def accumulator(self) -> org.optaplanner.core.api.function.TriFunction[_BiConstraintCollector__ResultContainer_, _BiConstraintCollector__A, _BiConstraintCollector__B, java.lang.Runnable]: ...
    def finisher(self) -> java.util.function.Function[_BiConstraintCollector__ResultContainer_, _BiConstraintCollector__Result_]: ...
    def supplier(self) -> java.util.function.Supplier[_BiConstraintCollector__ResultContainer_]: ...

_BiConstraintStream__A = typing.TypeVar('_BiConstraintStream__A')  # <A>
_BiConstraintStream__B = typing.TypeVar('_BiConstraintStream__B')  # <B>
class BiConstraintStream(org.optaplanner.core.api.score.stream.ConstraintStream, typing.Generic[_BiConstraintStream__A, _BiConstraintStream__B]):
    """
    public interface BiConstraintStream<A, B> extends :class:`~org.optaplanner.core.api.score.stream.ConstraintStream`
    
        A :class:`~org.optaplanner.core.api.score.stream.ConstraintStream` that matches two facts.
    
        Also see:
            :class:`~org.optaplanner.core.api.score.stream.ConstraintStream`
    """
    def distinct(self) -> 'BiConstraintStream'[_BiConstraintStream__A, _BiConstraintStream__B]: ...
    def filter(self, biPredicate: typing.Union[java.util.function.BiPredicate[_BiConstraintStream__A, _BiConstraintStream__B], typing.Callable[[_BiConstraintStream__A, _BiConstraintStream__B], bool]]) -> 'BiConstraintStream'[_BiConstraintStream__A, _BiConstraintStream__B]: ...
    _flattenLast__ResultB_ = typing.TypeVar('_flattenLast__ResultB_')  # <ResultB_>
    def flattenLast(self, function: typing.Union[java.util.function.Function[_BiConstraintStream__B, typing.Union[java.lang.Iterable[_flattenLast__ResultB_], typing.Sequence[_flattenLast__ResultB_], typing.Set[_flattenLast__ResultB_]]], typing.Callable[[_BiConstraintStream__B], typing.Union[java.lang.Iterable[_flattenLast__ResultB_], typing.Sequence[_flattenLast__ResultB_], typing.Set[_flattenLast__ResultB_]]]]) -> 'BiConstraintStream'[_BiConstraintStream__A, _flattenLast__ResultB_]: ...
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
    def groupBy(self, biFunction: typing.Union[java.util.function.BiFunction[_BiConstraintStream__A, _BiConstraintStream__B, _groupBy_0__GroupKeyA_], typing.Callable[[_BiConstraintStream__A, _BiConstraintStream__B], _groupBy_0__GroupKeyA_]], biFunction2: typing.Union[java.util.function.BiFunction[_BiConstraintStream__A, _BiConstraintStream__B, _groupBy_0__GroupKeyB_], typing.Callable[[_BiConstraintStream__A, _BiConstraintStream__B], _groupBy_0__GroupKeyB_]]) -> 'BiConstraintStream'[_groupBy_0__GroupKeyA_, _groupBy_0__GroupKeyB_]: ...
    @typing.overload
    def groupBy(self, biFunction: typing.Union[java.util.function.BiFunction[_BiConstraintStream__A, _BiConstraintStream__B, _groupBy_1__GroupKey_], typing.Callable[[_BiConstraintStream__A, _BiConstraintStream__B], _groupBy_1__GroupKey_]], biConstraintCollector: BiConstraintCollector[_BiConstraintStream__A, _BiConstraintStream__B, _groupBy_1__ResultContainer_, _groupBy_1__Result_]) -> 'BiConstraintStream'[_groupBy_1__GroupKey_, _groupBy_1__Result_]: ...
    @typing.overload
    def groupBy(self, biConstraintCollector: BiConstraintCollector[_BiConstraintStream__A, _BiConstraintStream__B, _groupBy_2__ResultContainerA_, _groupBy_2__ResultA_], biConstraintCollector2: BiConstraintCollector[_BiConstraintStream__A, _BiConstraintStream__B, _groupBy_2__ResultContainerB_, _groupBy_2__ResultB_]) -> 'BiConstraintStream'[_groupBy_2__ResultA_, _groupBy_2__ResultB_]: ...
    @typing.overload
    def groupBy(self, biFunction: typing.Union[java.util.function.BiFunction[_BiConstraintStream__A, _BiConstraintStream__B, _groupBy_3__GroupKeyA_], typing.Callable[[_BiConstraintStream__A, _BiConstraintStream__B], _groupBy_3__GroupKeyA_]], biFunction2: typing.Union[java.util.function.BiFunction[_BiConstraintStream__A, _BiConstraintStream__B, _groupBy_3__GroupKeyB_], typing.Callable[[_BiConstraintStream__A, _BiConstraintStream__B], _groupBy_3__GroupKeyB_]], biFunction3: typing.Union[java.util.function.BiFunction[_BiConstraintStream__A, _BiConstraintStream__B, _groupBy_3__GroupKeyC_], typing.Callable[[_BiConstraintStream__A, _BiConstraintStream__B], _groupBy_3__GroupKeyC_]], biFunction4: typing.Union[java.util.function.BiFunction[_BiConstraintStream__A, _BiConstraintStream__B, _groupBy_3__GroupKeyD_], typing.Callable[[_BiConstraintStream__A, _BiConstraintStream__B], _groupBy_3__GroupKeyD_]]) -> org.optaplanner.core.api.score.stream.quad.QuadConstraintStream[_groupBy_3__GroupKeyA_, _groupBy_3__GroupKeyB_, _groupBy_3__GroupKeyC_, _groupBy_3__GroupKeyD_]: ...
    @typing.overload
    def groupBy(self, biFunction: typing.Union[java.util.function.BiFunction[_BiConstraintStream__A, _BiConstraintStream__B, _groupBy_4__GroupKeyA_], typing.Callable[[_BiConstraintStream__A, _BiConstraintStream__B], _groupBy_4__GroupKeyA_]], biFunction2: typing.Union[java.util.function.BiFunction[_BiConstraintStream__A, _BiConstraintStream__B, _groupBy_4__GroupKeyB_], typing.Callable[[_BiConstraintStream__A, _BiConstraintStream__B], _groupBy_4__GroupKeyB_]], biFunction3: typing.Union[java.util.function.BiFunction[_BiConstraintStream__A, _BiConstraintStream__B, _groupBy_4__GroupKeyC_], typing.Callable[[_BiConstraintStream__A, _BiConstraintStream__B], _groupBy_4__GroupKeyC_]], biConstraintCollector: BiConstraintCollector[_BiConstraintStream__A, _BiConstraintStream__B, _groupBy_4__ResultContainerD_, _groupBy_4__ResultD_]) -> org.optaplanner.core.api.score.stream.quad.QuadConstraintStream[_groupBy_4__GroupKeyA_, _groupBy_4__GroupKeyB_, _groupBy_4__GroupKeyC_, _groupBy_4__ResultD_]: ...
    @typing.overload
    def groupBy(self, biFunction: typing.Union[java.util.function.BiFunction[_BiConstraintStream__A, _BiConstraintStream__B, _groupBy_5__GroupKeyA_], typing.Callable[[_BiConstraintStream__A, _BiConstraintStream__B], _groupBy_5__GroupKeyA_]], biFunction2: typing.Union[java.util.function.BiFunction[_BiConstraintStream__A, _BiConstraintStream__B, _groupBy_5__GroupKeyB_], typing.Callable[[_BiConstraintStream__A, _BiConstraintStream__B], _groupBy_5__GroupKeyB_]], biConstraintCollector: BiConstraintCollector[_BiConstraintStream__A, _BiConstraintStream__B, _groupBy_5__ResultContainerC_, _groupBy_5__ResultC_], biConstraintCollector2: BiConstraintCollector[_BiConstraintStream__A, _BiConstraintStream__B, _groupBy_5__ResultContainerD_, _groupBy_5__ResultD_]) -> org.optaplanner.core.api.score.stream.quad.QuadConstraintStream[_groupBy_5__GroupKeyA_, _groupBy_5__GroupKeyB_, _groupBy_5__ResultC_, _groupBy_5__ResultD_]: ...
    @typing.overload
    def groupBy(self, biFunction: typing.Union[java.util.function.BiFunction[_BiConstraintStream__A, _BiConstraintStream__B, _groupBy_6__GroupKey_], typing.Callable[[_BiConstraintStream__A, _BiConstraintStream__B], _groupBy_6__GroupKey_]], biConstraintCollector: BiConstraintCollector[_BiConstraintStream__A, _BiConstraintStream__B, _groupBy_6__ResultContainerB_, _groupBy_6__ResultB_], biConstraintCollector2: BiConstraintCollector[_BiConstraintStream__A, _BiConstraintStream__B, _groupBy_6__ResultContainerC_, _groupBy_6__ResultC_], biConstraintCollector3: BiConstraintCollector[_BiConstraintStream__A, _BiConstraintStream__B, _groupBy_6__ResultContainerD_, _groupBy_6__ResultD_]) -> org.optaplanner.core.api.score.stream.quad.QuadConstraintStream[_groupBy_6__GroupKey_, _groupBy_6__ResultB_, _groupBy_6__ResultC_, _groupBy_6__ResultD_]: ...
    @typing.overload
    def groupBy(self, biConstraintCollector: BiConstraintCollector[_BiConstraintStream__A, _BiConstraintStream__B, _groupBy_7__ResultContainerA_, _groupBy_7__ResultA_], biConstraintCollector2: BiConstraintCollector[_BiConstraintStream__A, _BiConstraintStream__B, _groupBy_7__ResultContainerB_, _groupBy_7__ResultB_], biConstraintCollector3: BiConstraintCollector[_BiConstraintStream__A, _BiConstraintStream__B, _groupBy_7__ResultContainerC_, _groupBy_7__ResultC_], biConstraintCollector4: BiConstraintCollector[_BiConstraintStream__A, _BiConstraintStream__B, _groupBy_7__ResultContainerD_, _groupBy_7__ResultD_]) -> org.optaplanner.core.api.score.stream.quad.QuadConstraintStream[_groupBy_7__ResultA_, _groupBy_7__ResultB_, _groupBy_7__ResultC_, _groupBy_7__ResultD_]: ...
    @typing.overload
    def groupBy(self, biFunction: typing.Union[java.util.function.BiFunction[_BiConstraintStream__A, _BiConstraintStream__B, _groupBy_8__GroupKeyA_], typing.Callable[[_BiConstraintStream__A, _BiConstraintStream__B], _groupBy_8__GroupKeyA_]], biFunction2: typing.Union[java.util.function.BiFunction[_BiConstraintStream__A, _BiConstraintStream__B, _groupBy_8__GroupKeyB_], typing.Callable[[_BiConstraintStream__A, _BiConstraintStream__B], _groupBy_8__GroupKeyB_]], biFunction3: typing.Union[java.util.function.BiFunction[_BiConstraintStream__A, _BiConstraintStream__B, _groupBy_8__GroupKeyC_], typing.Callable[[_BiConstraintStream__A, _BiConstraintStream__B], _groupBy_8__GroupKeyC_]]) -> org.optaplanner.core.api.score.stream.tri.TriConstraintStream[_groupBy_8__GroupKeyA_, _groupBy_8__GroupKeyB_, _groupBy_8__GroupKeyC_]: ...
    @typing.overload
    def groupBy(self, biFunction: typing.Union[java.util.function.BiFunction[_BiConstraintStream__A, _BiConstraintStream__B, _groupBy_9__GroupKeyA_], typing.Callable[[_BiConstraintStream__A, _BiConstraintStream__B], _groupBy_9__GroupKeyA_]], biFunction2: typing.Union[java.util.function.BiFunction[_BiConstraintStream__A, _BiConstraintStream__B, _groupBy_9__GroupKeyB_], typing.Callable[[_BiConstraintStream__A, _BiConstraintStream__B], _groupBy_9__GroupKeyB_]], biConstraintCollector: BiConstraintCollector[_BiConstraintStream__A, _BiConstraintStream__B, _groupBy_9__ResultContainer_, _groupBy_9__Result_]) -> org.optaplanner.core.api.score.stream.tri.TriConstraintStream[_groupBy_9__GroupKeyA_, _groupBy_9__GroupKeyB_, _groupBy_9__Result_]: ...
    @typing.overload
    def groupBy(self, biFunction: typing.Union[java.util.function.BiFunction[_BiConstraintStream__A, _BiConstraintStream__B, _groupBy_10__GroupKey_], typing.Callable[[_BiConstraintStream__A, _BiConstraintStream__B], _groupBy_10__GroupKey_]], biConstraintCollector: BiConstraintCollector[_BiConstraintStream__A, _BiConstraintStream__B, _groupBy_10__ResultContainerB_, _groupBy_10__ResultB_], biConstraintCollector2: BiConstraintCollector[_BiConstraintStream__A, _BiConstraintStream__B, _groupBy_10__ResultContainerC_, _groupBy_10__ResultC_]) -> org.optaplanner.core.api.score.stream.tri.TriConstraintStream[_groupBy_10__GroupKey_, _groupBy_10__ResultB_, _groupBy_10__ResultC_]: ...
    @typing.overload
    def groupBy(self, biConstraintCollector: BiConstraintCollector[_BiConstraintStream__A, _BiConstraintStream__B, _groupBy_11__ResultContainerA_, _groupBy_11__ResultA_], biConstraintCollector2: BiConstraintCollector[_BiConstraintStream__A, _BiConstraintStream__B, _groupBy_11__ResultContainerB_, _groupBy_11__ResultB_], biConstraintCollector3: BiConstraintCollector[_BiConstraintStream__A, _BiConstraintStream__B, _groupBy_11__ResultContainerC_, _groupBy_11__ResultC_]) -> org.optaplanner.core.api.score.stream.tri.TriConstraintStream[_groupBy_11__ResultA_, _groupBy_11__ResultB_, _groupBy_11__ResultC_]: ...
    @typing.overload
    def groupBy(self, biFunction: typing.Union[java.util.function.BiFunction[_BiConstraintStream__A, _BiConstraintStream__B, _groupBy_12__GroupKey_], typing.Callable[[_BiConstraintStream__A, _BiConstraintStream__B], _groupBy_12__GroupKey_]]) -> org.optaplanner.core.api.score.stream.uni.UniConstraintStream[_groupBy_12__GroupKey_]: ...
    @typing.overload
    def groupBy(self, biConstraintCollector: BiConstraintCollector[_BiConstraintStream__A, _BiConstraintStream__B, _groupBy_13__ResultContainer_, _groupBy_13__Result_]) -> org.optaplanner.core.api.score.stream.uni.UniConstraintStream[_groupBy_13__Result_]: ...
    _ifExists_0__C = typing.TypeVar('_ifExists_0__C')  # <C>
    _ifExists_1__C = typing.TypeVar('_ifExists_1__C')  # <C>
    _ifExists_2__C = typing.TypeVar('_ifExists_2__C')  # <C>
    _ifExists_3__C = typing.TypeVar('_ifExists_3__C')  # <C>
    _ifExists_4__C = typing.TypeVar('_ifExists_4__C')  # <C>
    @typing.overload
    def ifExists(self, class_: typing.Type[_ifExists_0__C], *triJoiner: org.optaplanner.core.api.score.stream.tri.TriJoiner[_BiConstraintStream__A, _BiConstraintStream__B, _ifExists_0__C]) -> 'BiConstraintStream'[_BiConstraintStream__A, _BiConstraintStream__B]: ...
    @typing.overload
    def ifExists(self, class_: typing.Type[_ifExists_1__C], triJoiner: org.optaplanner.core.api.score.stream.tri.TriJoiner[_BiConstraintStream__A, _BiConstraintStream__B, _ifExists_1__C]) -> 'BiConstraintStream'[_BiConstraintStream__A, _BiConstraintStream__B]: ...
    @typing.overload
    def ifExists(self, class_: typing.Type[_ifExists_2__C], triJoiner: org.optaplanner.core.api.score.stream.tri.TriJoiner[_BiConstraintStream__A, _BiConstraintStream__B, _ifExists_2__C], triJoiner2: org.optaplanner.core.api.score.stream.tri.TriJoiner[_BiConstraintStream__A, _BiConstraintStream__B, _ifExists_2__C]) -> 'BiConstraintStream'[_BiConstraintStream__A, _BiConstraintStream__B]: ...
    @typing.overload
    def ifExists(self, class_: typing.Type[_ifExists_3__C], triJoiner: org.optaplanner.core.api.score.stream.tri.TriJoiner[_BiConstraintStream__A, _BiConstraintStream__B, _ifExists_3__C], triJoiner2: org.optaplanner.core.api.score.stream.tri.TriJoiner[_BiConstraintStream__A, _BiConstraintStream__B, _ifExists_3__C], triJoiner3: org.optaplanner.core.api.score.stream.tri.TriJoiner[_BiConstraintStream__A, _BiConstraintStream__B, _ifExists_3__C]) -> 'BiConstraintStream'[_BiConstraintStream__A, _BiConstraintStream__B]: ...
    @typing.overload
    def ifExists(self, class_: typing.Type[_ifExists_4__C], triJoiner: org.optaplanner.core.api.score.stream.tri.TriJoiner[_BiConstraintStream__A, _BiConstraintStream__B, _ifExists_4__C], triJoiner2: org.optaplanner.core.api.score.stream.tri.TriJoiner[_BiConstraintStream__A, _BiConstraintStream__B, _ifExists_4__C], triJoiner3: org.optaplanner.core.api.score.stream.tri.TriJoiner[_BiConstraintStream__A, _BiConstraintStream__B, _ifExists_4__C], triJoiner4: org.optaplanner.core.api.score.stream.tri.TriJoiner[_BiConstraintStream__A, _BiConstraintStream__B, _ifExists_4__C]) -> 'BiConstraintStream'[_BiConstraintStream__A, _BiConstraintStream__B]: ...
    _ifExistsIncludingNullVars_0__C = typing.TypeVar('_ifExistsIncludingNullVars_0__C')  # <C>
    _ifExistsIncludingNullVars_1__C = typing.TypeVar('_ifExistsIncludingNullVars_1__C')  # <C>
    _ifExistsIncludingNullVars_2__C = typing.TypeVar('_ifExistsIncludingNullVars_2__C')  # <C>
    _ifExistsIncludingNullVars_3__C = typing.TypeVar('_ifExistsIncludingNullVars_3__C')  # <C>
    _ifExistsIncludingNullVars_4__C = typing.TypeVar('_ifExistsIncludingNullVars_4__C')  # <C>
    @typing.overload
    def ifExistsIncludingNullVars(self, class_: typing.Type[_ifExistsIncludingNullVars_0__C], *triJoiner: org.optaplanner.core.api.score.stream.tri.TriJoiner[_BiConstraintStream__A, _BiConstraintStream__B, _ifExistsIncludingNullVars_0__C]) -> 'BiConstraintStream'[_BiConstraintStream__A, _BiConstraintStream__B]: ...
    @typing.overload
    def ifExistsIncludingNullVars(self, class_: typing.Type[_ifExistsIncludingNullVars_1__C], triJoiner: org.optaplanner.core.api.score.stream.tri.TriJoiner[_BiConstraintStream__A, _BiConstraintStream__B, _ifExistsIncludingNullVars_1__C]) -> 'BiConstraintStream'[_BiConstraintStream__A, _BiConstraintStream__B]: ...
    @typing.overload
    def ifExistsIncludingNullVars(self, class_: typing.Type[_ifExistsIncludingNullVars_2__C], triJoiner: org.optaplanner.core.api.score.stream.tri.TriJoiner[_BiConstraintStream__A, _BiConstraintStream__B, _ifExistsIncludingNullVars_2__C], triJoiner2: org.optaplanner.core.api.score.stream.tri.TriJoiner[_BiConstraintStream__A, _BiConstraintStream__B, _ifExistsIncludingNullVars_2__C]) -> 'BiConstraintStream'[_BiConstraintStream__A, _BiConstraintStream__B]: ...
    @typing.overload
    def ifExistsIncludingNullVars(self, class_: typing.Type[_ifExistsIncludingNullVars_3__C], triJoiner: org.optaplanner.core.api.score.stream.tri.TriJoiner[_BiConstraintStream__A, _BiConstraintStream__B, _ifExistsIncludingNullVars_3__C], triJoiner2: org.optaplanner.core.api.score.stream.tri.TriJoiner[_BiConstraintStream__A, _BiConstraintStream__B, _ifExistsIncludingNullVars_3__C], triJoiner3: org.optaplanner.core.api.score.stream.tri.TriJoiner[_BiConstraintStream__A, _BiConstraintStream__B, _ifExistsIncludingNullVars_3__C]) -> 'BiConstraintStream'[_BiConstraintStream__A, _BiConstraintStream__B]: ...
    @typing.overload
    def ifExistsIncludingNullVars(self, class_: typing.Type[_ifExistsIncludingNullVars_4__C], triJoiner: org.optaplanner.core.api.score.stream.tri.TriJoiner[_BiConstraintStream__A, _BiConstraintStream__B, _ifExistsIncludingNullVars_4__C], triJoiner2: org.optaplanner.core.api.score.stream.tri.TriJoiner[_BiConstraintStream__A, _BiConstraintStream__B, _ifExistsIncludingNullVars_4__C], triJoiner3: org.optaplanner.core.api.score.stream.tri.TriJoiner[_BiConstraintStream__A, _BiConstraintStream__B, _ifExistsIncludingNullVars_4__C], triJoiner4: org.optaplanner.core.api.score.stream.tri.TriJoiner[_BiConstraintStream__A, _BiConstraintStream__B, _ifExistsIncludingNullVars_4__C]) -> 'BiConstraintStream'[_BiConstraintStream__A, _BiConstraintStream__B]: ...
    _ifNotExists_0__C = typing.TypeVar('_ifNotExists_0__C')  # <C>
    _ifNotExists_1__C = typing.TypeVar('_ifNotExists_1__C')  # <C>
    _ifNotExists_2__C = typing.TypeVar('_ifNotExists_2__C')  # <C>
    _ifNotExists_3__C = typing.TypeVar('_ifNotExists_3__C')  # <C>
    _ifNotExists_4__C = typing.TypeVar('_ifNotExists_4__C')  # <C>
    @typing.overload
    def ifNotExists(self, class_: typing.Type[_ifNotExists_0__C], *triJoiner: org.optaplanner.core.api.score.stream.tri.TriJoiner[_BiConstraintStream__A, _BiConstraintStream__B, _ifNotExists_0__C]) -> 'BiConstraintStream'[_BiConstraintStream__A, _BiConstraintStream__B]: ...
    @typing.overload
    def ifNotExists(self, class_: typing.Type[_ifNotExists_1__C], triJoiner: org.optaplanner.core.api.score.stream.tri.TriJoiner[_BiConstraintStream__A, _BiConstraintStream__B, _ifNotExists_1__C]) -> 'BiConstraintStream'[_BiConstraintStream__A, _BiConstraintStream__B]: ...
    @typing.overload
    def ifNotExists(self, class_: typing.Type[_ifNotExists_2__C], triJoiner: org.optaplanner.core.api.score.stream.tri.TriJoiner[_BiConstraintStream__A, _BiConstraintStream__B, _ifNotExists_2__C], triJoiner2: org.optaplanner.core.api.score.stream.tri.TriJoiner[_BiConstraintStream__A, _BiConstraintStream__B, _ifNotExists_2__C]) -> 'BiConstraintStream'[_BiConstraintStream__A, _BiConstraintStream__B]: ...
    @typing.overload
    def ifNotExists(self, class_: typing.Type[_ifNotExists_3__C], triJoiner: org.optaplanner.core.api.score.stream.tri.TriJoiner[_BiConstraintStream__A, _BiConstraintStream__B, _ifNotExists_3__C], triJoiner2: org.optaplanner.core.api.score.stream.tri.TriJoiner[_BiConstraintStream__A, _BiConstraintStream__B, _ifNotExists_3__C], triJoiner3: org.optaplanner.core.api.score.stream.tri.TriJoiner[_BiConstraintStream__A, _BiConstraintStream__B, _ifNotExists_3__C]) -> 'BiConstraintStream'[_BiConstraintStream__A, _BiConstraintStream__B]: ...
    @typing.overload
    def ifNotExists(self, class_: typing.Type[_ifNotExists_4__C], triJoiner: org.optaplanner.core.api.score.stream.tri.TriJoiner[_BiConstraintStream__A, _BiConstraintStream__B, _ifNotExists_4__C], triJoiner2: org.optaplanner.core.api.score.stream.tri.TriJoiner[_BiConstraintStream__A, _BiConstraintStream__B, _ifNotExists_4__C], triJoiner3: org.optaplanner.core.api.score.stream.tri.TriJoiner[_BiConstraintStream__A, _BiConstraintStream__B, _ifNotExists_4__C], triJoiner4: org.optaplanner.core.api.score.stream.tri.TriJoiner[_BiConstraintStream__A, _BiConstraintStream__B, _ifNotExists_4__C]) -> 'BiConstraintStream'[_BiConstraintStream__A, _BiConstraintStream__B]: ...
    _ifNotExistsIncludingNullVars_0__C = typing.TypeVar('_ifNotExistsIncludingNullVars_0__C')  # <C>
    _ifNotExistsIncludingNullVars_1__C = typing.TypeVar('_ifNotExistsIncludingNullVars_1__C')  # <C>
    _ifNotExistsIncludingNullVars_2__C = typing.TypeVar('_ifNotExistsIncludingNullVars_2__C')  # <C>
    _ifNotExistsIncludingNullVars_3__C = typing.TypeVar('_ifNotExistsIncludingNullVars_3__C')  # <C>
    _ifNotExistsIncludingNullVars_4__C = typing.TypeVar('_ifNotExistsIncludingNullVars_4__C')  # <C>
    @typing.overload
    def ifNotExistsIncludingNullVars(self, class_: typing.Type[_ifNotExistsIncludingNullVars_0__C], *triJoiner: org.optaplanner.core.api.score.stream.tri.TriJoiner[_BiConstraintStream__A, _BiConstraintStream__B, _ifNotExistsIncludingNullVars_0__C]) -> 'BiConstraintStream'[_BiConstraintStream__A, _BiConstraintStream__B]: ...
    @typing.overload
    def ifNotExistsIncludingNullVars(self, class_: typing.Type[_ifNotExistsIncludingNullVars_1__C], triJoiner: org.optaplanner.core.api.score.stream.tri.TriJoiner[_BiConstraintStream__A, _BiConstraintStream__B, _ifNotExistsIncludingNullVars_1__C]) -> 'BiConstraintStream'[_BiConstraintStream__A, _BiConstraintStream__B]: ...
    @typing.overload
    def ifNotExistsIncludingNullVars(self, class_: typing.Type[_ifNotExistsIncludingNullVars_2__C], triJoiner: org.optaplanner.core.api.score.stream.tri.TriJoiner[_BiConstraintStream__A, _BiConstraintStream__B, _ifNotExistsIncludingNullVars_2__C], triJoiner2: org.optaplanner.core.api.score.stream.tri.TriJoiner[_BiConstraintStream__A, _BiConstraintStream__B, _ifNotExistsIncludingNullVars_2__C]) -> 'BiConstraintStream'[_BiConstraintStream__A, _BiConstraintStream__B]: ...
    @typing.overload
    def ifNotExistsIncludingNullVars(self, class_: typing.Type[_ifNotExistsIncludingNullVars_3__C], triJoiner: org.optaplanner.core.api.score.stream.tri.TriJoiner[_BiConstraintStream__A, _BiConstraintStream__B, _ifNotExistsIncludingNullVars_3__C], triJoiner2: org.optaplanner.core.api.score.stream.tri.TriJoiner[_BiConstraintStream__A, _BiConstraintStream__B, _ifNotExistsIncludingNullVars_3__C], triJoiner3: org.optaplanner.core.api.score.stream.tri.TriJoiner[_BiConstraintStream__A, _BiConstraintStream__B, _ifNotExistsIncludingNullVars_3__C]) -> 'BiConstraintStream'[_BiConstraintStream__A, _BiConstraintStream__B]: ...
    @typing.overload
    def ifNotExistsIncludingNullVars(self, class_: typing.Type[_ifNotExistsIncludingNullVars_4__C], triJoiner: org.optaplanner.core.api.score.stream.tri.TriJoiner[_BiConstraintStream__A, _BiConstraintStream__B, _ifNotExistsIncludingNullVars_4__C], triJoiner2: org.optaplanner.core.api.score.stream.tri.TriJoiner[_BiConstraintStream__A, _BiConstraintStream__B, _ifNotExistsIncludingNullVars_4__C], triJoiner3: org.optaplanner.core.api.score.stream.tri.TriJoiner[_BiConstraintStream__A, _BiConstraintStream__B, _ifNotExistsIncludingNullVars_4__C], triJoiner4: org.optaplanner.core.api.score.stream.tri.TriJoiner[_BiConstraintStream__A, _BiConstraintStream__B, _ifNotExistsIncludingNullVars_4__C]) -> 'BiConstraintStream'[_BiConstraintStream__A, _BiConstraintStream__B]: ...
    @typing.overload
    def impact(self, string: str, string2: str, score: org.optaplanner.core.api.score.Score[typing.Any]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def impact(self, string: str, string2: str, score: org.optaplanner.core.api.score.Score[typing.Any], toIntBiFunction: typing.Union[java.util.function.ToIntBiFunction[_BiConstraintStream__A, _BiConstraintStream__B], typing.Callable[[_BiConstraintStream__A, _BiConstraintStream__B], int]]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def impact(self, string: str, score: org.optaplanner.core.api.score.Score[typing.Any]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def impact(self, string: str, score: org.optaplanner.core.api.score.Score[typing.Any], toIntBiFunction: typing.Union[java.util.function.ToIntBiFunction[_BiConstraintStream__A, _BiConstraintStream__B], typing.Callable[[_BiConstraintStream__A, _BiConstraintStream__B], int]]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def impactBigDecimal(self, string: str, string2: str, score: org.optaplanner.core.api.score.Score[typing.Any], biFunction: typing.Union[java.util.function.BiFunction[_BiConstraintStream__A, _BiConstraintStream__B, typing.Union[java.math.BigDecimal, decimal.Decimal]], typing.Callable[[_BiConstraintStream__A, _BiConstraintStream__B], typing.Union[java.math.BigDecimal, decimal.Decimal]]]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def impactBigDecimal(self, string: str, score: org.optaplanner.core.api.score.Score[typing.Any], biFunction: typing.Union[java.util.function.BiFunction[_BiConstraintStream__A, _BiConstraintStream__B, typing.Union[java.math.BigDecimal, decimal.Decimal]], typing.Callable[[_BiConstraintStream__A, _BiConstraintStream__B], typing.Union[java.math.BigDecimal, decimal.Decimal]]]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def impactConfigurable(self, string: str, string2: str, toIntBiFunction: typing.Union[java.util.function.ToIntBiFunction[_BiConstraintStream__A, _BiConstraintStream__B], typing.Callable[[_BiConstraintStream__A, _BiConstraintStream__B], int]]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def impactConfigurable(self, string: str, toIntBiFunction: typing.Union[java.util.function.ToIntBiFunction[_BiConstraintStream__A, _BiConstraintStream__B], typing.Callable[[_BiConstraintStream__A, _BiConstraintStream__B], int]]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def impactConfigurableBigDecimal(self, string: str, string2: str, biFunction: typing.Union[java.util.function.BiFunction[_BiConstraintStream__A, _BiConstraintStream__B, typing.Union[java.math.BigDecimal, decimal.Decimal]], typing.Callable[[_BiConstraintStream__A, _BiConstraintStream__B], typing.Union[java.math.BigDecimal, decimal.Decimal]]]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def impactConfigurableBigDecimal(self, string: str, biFunction: typing.Union[java.util.function.BiFunction[_BiConstraintStream__A, _BiConstraintStream__B, typing.Union[java.math.BigDecimal, decimal.Decimal]], typing.Callable[[_BiConstraintStream__A, _BiConstraintStream__B], typing.Union[java.math.BigDecimal, decimal.Decimal]]]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def impactConfigurableLong(self, string: str, string2: str, toLongBiFunction: typing.Union[java.util.function.ToLongBiFunction[_BiConstraintStream__A, _BiConstraintStream__B], typing.Callable[[_BiConstraintStream__A, _BiConstraintStream__B], int]]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def impactConfigurableLong(self, string: str, toLongBiFunction: typing.Union[java.util.function.ToLongBiFunction[_BiConstraintStream__A, _BiConstraintStream__B], typing.Callable[[_BiConstraintStream__A, _BiConstraintStream__B], int]]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def impactLong(self, string: str, string2: str, score: org.optaplanner.core.api.score.Score[typing.Any], toLongBiFunction: typing.Union[java.util.function.ToLongBiFunction[_BiConstraintStream__A, _BiConstraintStream__B], typing.Callable[[_BiConstraintStream__A, _BiConstraintStream__B], int]]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def impactLong(self, string: str, score: org.optaplanner.core.api.score.Score[typing.Any], toLongBiFunction: typing.Union[java.util.function.ToLongBiFunction[_BiConstraintStream__A, _BiConstraintStream__B], typing.Callable[[_BiConstraintStream__A, _BiConstraintStream__B], int]]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    _join_0__C = typing.TypeVar('_join_0__C')  # <C>
    _join_1__C = typing.TypeVar('_join_1__C')  # <C>
    _join_2__C = typing.TypeVar('_join_2__C')  # <C>
    _join_3__C = typing.TypeVar('_join_3__C')  # <C>
    _join_4__C = typing.TypeVar('_join_4__C')  # <C>
    _join_5__C = typing.TypeVar('_join_5__C')  # <C>
    _join_6__C = typing.TypeVar('_join_6__C')  # <C>
    _join_7__C = typing.TypeVar('_join_7__C')  # <C>
    _join_8__C = typing.TypeVar('_join_8__C')  # <C>
    _join_9__C = typing.TypeVar('_join_9__C')  # <C>
    _join_10__C = typing.TypeVar('_join_10__C')  # <C>
    _join_11__C = typing.TypeVar('_join_11__C')  # <C>
    @typing.overload
    def join(self, class_: typing.Type[_join_0__C], *triJoiner: org.optaplanner.core.api.score.stream.tri.TriJoiner[_BiConstraintStream__A, _BiConstraintStream__B, _join_0__C]) -> org.optaplanner.core.api.score.stream.tri.TriConstraintStream[_BiConstraintStream__A, _BiConstraintStream__B, _join_0__C]: ...
    @typing.overload
    def join(self, uniConstraintStream: org.optaplanner.core.api.score.stream.uni.UniConstraintStream[_join_1__C], *triJoiner: org.optaplanner.core.api.score.stream.tri.TriJoiner[_BiConstraintStream__A, _BiConstraintStream__B, _join_1__C]) -> org.optaplanner.core.api.score.stream.tri.TriConstraintStream[_BiConstraintStream__A, _BiConstraintStream__B, _join_1__C]: ...
    @typing.overload
    def join(self, class_: typing.Type[_join_2__C]) -> org.optaplanner.core.api.score.stream.tri.TriConstraintStream[_BiConstraintStream__A, _BiConstraintStream__B, _join_2__C]: ...
    @typing.overload
    def join(self, class_: typing.Type[_join_3__C], triJoiner: org.optaplanner.core.api.score.stream.tri.TriJoiner[_BiConstraintStream__A, _BiConstraintStream__B, _join_3__C]) -> org.optaplanner.core.api.score.stream.tri.TriConstraintStream[_BiConstraintStream__A, _BiConstraintStream__B, _join_3__C]: ...
    @typing.overload
    def join(self, class_: typing.Type[_join_4__C], triJoiner: org.optaplanner.core.api.score.stream.tri.TriJoiner[_BiConstraintStream__A, _BiConstraintStream__B, _join_4__C], triJoiner2: org.optaplanner.core.api.score.stream.tri.TriJoiner[_BiConstraintStream__A, _BiConstraintStream__B, _join_4__C]) -> org.optaplanner.core.api.score.stream.tri.TriConstraintStream[_BiConstraintStream__A, _BiConstraintStream__B, _join_4__C]: ...
    @typing.overload
    def join(self, class_: typing.Type[_join_5__C], triJoiner: org.optaplanner.core.api.score.stream.tri.TriJoiner[_BiConstraintStream__A, _BiConstraintStream__B, _join_5__C], triJoiner2: org.optaplanner.core.api.score.stream.tri.TriJoiner[_BiConstraintStream__A, _BiConstraintStream__B, _join_5__C], triJoiner3: org.optaplanner.core.api.score.stream.tri.TriJoiner[_BiConstraintStream__A, _BiConstraintStream__B, _join_5__C]) -> org.optaplanner.core.api.score.stream.tri.TriConstraintStream[_BiConstraintStream__A, _BiConstraintStream__B, _join_5__C]: ...
    @typing.overload
    def join(self, class_: typing.Type[_join_6__C], triJoiner: org.optaplanner.core.api.score.stream.tri.TriJoiner[_BiConstraintStream__A, _BiConstraintStream__B, _join_6__C], triJoiner2: org.optaplanner.core.api.score.stream.tri.TriJoiner[_BiConstraintStream__A, _BiConstraintStream__B, _join_6__C], triJoiner3: org.optaplanner.core.api.score.stream.tri.TriJoiner[_BiConstraintStream__A, _BiConstraintStream__B, _join_6__C], triJoiner4: org.optaplanner.core.api.score.stream.tri.TriJoiner[_BiConstraintStream__A, _BiConstraintStream__B, _join_6__C]) -> org.optaplanner.core.api.score.stream.tri.TriConstraintStream[_BiConstraintStream__A, _BiConstraintStream__B, _join_6__C]: ...
    @typing.overload
    def join(self, uniConstraintStream: org.optaplanner.core.api.score.stream.uni.UniConstraintStream[_join_7__C]) -> org.optaplanner.core.api.score.stream.tri.TriConstraintStream[_BiConstraintStream__A, _BiConstraintStream__B, _join_7__C]: ...
    @typing.overload
    def join(self, uniConstraintStream: org.optaplanner.core.api.score.stream.uni.UniConstraintStream[_join_8__C], triJoiner: org.optaplanner.core.api.score.stream.tri.TriJoiner[_BiConstraintStream__A, _BiConstraintStream__B, _join_8__C]) -> org.optaplanner.core.api.score.stream.tri.TriConstraintStream[_BiConstraintStream__A, _BiConstraintStream__B, _join_8__C]: ...
    @typing.overload
    def join(self, uniConstraintStream: org.optaplanner.core.api.score.stream.uni.UniConstraintStream[_join_9__C], triJoiner: org.optaplanner.core.api.score.stream.tri.TriJoiner[_BiConstraintStream__A, _BiConstraintStream__B, _join_9__C], triJoiner2: org.optaplanner.core.api.score.stream.tri.TriJoiner[_BiConstraintStream__A, _BiConstraintStream__B, _join_9__C]) -> org.optaplanner.core.api.score.stream.tri.TriConstraintStream[_BiConstraintStream__A, _BiConstraintStream__B, _join_9__C]: ...
    @typing.overload
    def join(self, uniConstraintStream: org.optaplanner.core.api.score.stream.uni.UniConstraintStream[_join_10__C], triJoiner: org.optaplanner.core.api.score.stream.tri.TriJoiner[_BiConstraintStream__A, _BiConstraintStream__B, _join_10__C], triJoiner2: org.optaplanner.core.api.score.stream.tri.TriJoiner[_BiConstraintStream__A, _BiConstraintStream__B, _join_10__C], triJoiner3: org.optaplanner.core.api.score.stream.tri.TriJoiner[_BiConstraintStream__A, _BiConstraintStream__B, _join_10__C]) -> org.optaplanner.core.api.score.stream.tri.TriConstraintStream[_BiConstraintStream__A, _BiConstraintStream__B, _join_10__C]: ...
    @typing.overload
    def join(self, uniConstraintStream: org.optaplanner.core.api.score.stream.uni.UniConstraintStream[_join_11__C], triJoiner: org.optaplanner.core.api.score.stream.tri.TriJoiner[_BiConstraintStream__A, _BiConstraintStream__B, _join_11__C], triJoiner2: org.optaplanner.core.api.score.stream.tri.TriJoiner[_BiConstraintStream__A, _BiConstraintStream__B, _join_11__C], triJoiner3: org.optaplanner.core.api.score.stream.tri.TriJoiner[_BiConstraintStream__A, _BiConstraintStream__B, _join_11__C], triJoiner4: org.optaplanner.core.api.score.stream.tri.TriJoiner[_BiConstraintStream__A, _BiConstraintStream__B, _join_11__C]) -> org.optaplanner.core.api.score.stream.tri.TriConstraintStream[_BiConstraintStream__A, _BiConstraintStream__B, _join_11__C]: ...
    _map__ResultA_ = typing.TypeVar('_map__ResultA_')  # <ResultA_>
    def map(self, biFunction: typing.Union[java.util.function.BiFunction[_BiConstraintStream__A, _BiConstraintStream__B, _map__ResultA_], typing.Callable[[_BiConstraintStream__A, _BiConstraintStream__B], _map__ResultA_]]) -> org.optaplanner.core.api.score.stream.uni.UniConstraintStream[_map__ResultA_]: ...
    @typing.overload
    def penalize(self, string: str, string2: str, score: org.optaplanner.core.api.score.Score[typing.Any]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def penalize(self, string: str, string2: str, score: org.optaplanner.core.api.score.Score[typing.Any], toIntBiFunction: typing.Union[java.util.function.ToIntBiFunction[_BiConstraintStream__A, _BiConstraintStream__B], typing.Callable[[_BiConstraintStream__A, _BiConstraintStream__B], int]]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def penalize(self, string: str, score: org.optaplanner.core.api.score.Score[typing.Any]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def penalize(self, string: str, score: org.optaplanner.core.api.score.Score[typing.Any], toIntBiFunction: typing.Union[java.util.function.ToIntBiFunction[_BiConstraintStream__A, _BiConstraintStream__B], typing.Callable[[_BiConstraintStream__A, _BiConstraintStream__B], int]]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def penalizeBigDecimal(self, string: str, string2: str, score: org.optaplanner.core.api.score.Score[typing.Any], biFunction: typing.Union[java.util.function.BiFunction[_BiConstraintStream__A, _BiConstraintStream__B, typing.Union[java.math.BigDecimal, decimal.Decimal]], typing.Callable[[_BiConstraintStream__A, _BiConstraintStream__B], typing.Union[java.math.BigDecimal, decimal.Decimal]]]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def penalizeBigDecimal(self, string: str, score: org.optaplanner.core.api.score.Score[typing.Any], biFunction: typing.Union[java.util.function.BiFunction[_BiConstraintStream__A, _BiConstraintStream__B, typing.Union[java.math.BigDecimal, decimal.Decimal]], typing.Callable[[_BiConstraintStream__A, _BiConstraintStream__B], typing.Union[java.math.BigDecimal, decimal.Decimal]]]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def penalizeConfigurable(self, string: str, string2: str) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def penalizeConfigurable(self, string: str, string2: str, toIntBiFunction: typing.Union[java.util.function.ToIntBiFunction[_BiConstraintStream__A, _BiConstraintStream__B], typing.Callable[[_BiConstraintStream__A, _BiConstraintStream__B], int]]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def penalizeConfigurable(self, string: str) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def penalizeConfigurable(self, string: str, toIntBiFunction: typing.Union[java.util.function.ToIntBiFunction[_BiConstraintStream__A, _BiConstraintStream__B], typing.Callable[[_BiConstraintStream__A, _BiConstraintStream__B], int]]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def penalizeConfigurableBigDecimal(self, string: str, string2: str, biFunction: typing.Union[java.util.function.BiFunction[_BiConstraintStream__A, _BiConstraintStream__B, typing.Union[java.math.BigDecimal, decimal.Decimal]], typing.Callable[[_BiConstraintStream__A, _BiConstraintStream__B], typing.Union[java.math.BigDecimal, decimal.Decimal]]]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def penalizeConfigurableBigDecimal(self, string: str, biFunction: typing.Union[java.util.function.BiFunction[_BiConstraintStream__A, _BiConstraintStream__B, typing.Union[java.math.BigDecimal, decimal.Decimal]], typing.Callable[[_BiConstraintStream__A, _BiConstraintStream__B], typing.Union[java.math.BigDecimal, decimal.Decimal]]]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def penalizeConfigurableLong(self, string: str, string2: str, toLongBiFunction: typing.Union[java.util.function.ToLongBiFunction[_BiConstraintStream__A, _BiConstraintStream__B], typing.Callable[[_BiConstraintStream__A, _BiConstraintStream__B], int]]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def penalizeConfigurableLong(self, string: str, toLongBiFunction: typing.Union[java.util.function.ToLongBiFunction[_BiConstraintStream__A, _BiConstraintStream__B], typing.Callable[[_BiConstraintStream__A, _BiConstraintStream__B], int]]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def penalizeLong(self, string: str, string2: str, score: org.optaplanner.core.api.score.Score[typing.Any], toLongBiFunction: typing.Union[java.util.function.ToLongBiFunction[_BiConstraintStream__A, _BiConstraintStream__B], typing.Callable[[_BiConstraintStream__A, _BiConstraintStream__B], int]]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def penalizeLong(self, string: str, score: org.optaplanner.core.api.score.Score[typing.Any], toLongBiFunction: typing.Union[java.util.function.ToLongBiFunction[_BiConstraintStream__A, _BiConstraintStream__B], typing.Callable[[_BiConstraintStream__A, _BiConstraintStream__B], int]]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def reward(self, string: str, string2: str, score: org.optaplanner.core.api.score.Score[typing.Any]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def reward(self, string: str, string2: str, score: org.optaplanner.core.api.score.Score[typing.Any], toIntBiFunction: typing.Union[java.util.function.ToIntBiFunction[_BiConstraintStream__A, _BiConstraintStream__B], typing.Callable[[_BiConstraintStream__A, _BiConstraintStream__B], int]]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def reward(self, string: str, score: org.optaplanner.core.api.score.Score[typing.Any]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def reward(self, string: str, score: org.optaplanner.core.api.score.Score[typing.Any], toIntBiFunction: typing.Union[java.util.function.ToIntBiFunction[_BiConstraintStream__A, _BiConstraintStream__B], typing.Callable[[_BiConstraintStream__A, _BiConstraintStream__B], int]]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def rewardBigDecimal(self, string: str, string2: str, score: org.optaplanner.core.api.score.Score[typing.Any], biFunction: typing.Union[java.util.function.BiFunction[_BiConstraintStream__A, _BiConstraintStream__B, typing.Union[java.math.BigDecimal, decimal.Decimal]], typing.Callable[[_BiConstraintStream__A, _BiConstraintStream__B], typing.Union[java.math.BigDecimal, decimal.Decimal]]]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def rewardBigDecimal(self, string: str, score: org.optaplanner.core.api.score.Score[typing.Any], biFunction: typing.Union[java.util.function.BiFunction[_BiConstraintStream__A, _BiConstraintStream__B, typing.Union[java.math.BigDecimal, decimal.Decimal]], typing.Callable[[_BiConstraintStream__A, _BiConstraintStream__B], typing.Union[java.math.BigDecimal, decimal.Decimal]]]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def rewardConfigurable(self, string: str, string2: str) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def rewardConfigurable(self, string: str, string2: str, toIntBiFunction: typing.Union[java.util.function.ToIntBiFunction[_BiConstraintStream__A, _BiConstraintStream__B], typing.Callable[[_BiConstraintStream__A, _BiConstraintStream__B], int]]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def rewardConfigurable(self, string: str) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def rewardConfigurable(self, string: str, toIntBiFunction: typing.Union[java.util.function.ToIntBiFunction[_BiConstraintStream__A, _BiConstraintStream__B], typing.Callable[[_BiConstraintStream__A, _BiConstraintStream__B], int]]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def rewardConfigurableBigDecimal(self, string: str, string2: str, biFunction: typing.Union[java.util.function.BiFunction[_BiConstraintStream__A, _BiConstraintStream__B, typing.Union[java.math.BigDecimal, decimal.Decimal]], typing.Callable[[_BiConstraintStream__A, _BiConstraintStream__B], typing.Union[java.math.BigDecimal, decimal.Decimal]]]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def rewardConfigurableBigDecimal(self, string: str, biFunction: typing.Union[java.util.function.BiFunction[_BiConstraintStream__A, _BiConstraintStream__B, typing.Union[java.math.BigDecimal, decimal.Decimal]], typing.Callable[[_BiConstraintStream__A, _BiConstraintStream__B], typing.Union[java.math.BigDecimal, decimal.Decimal]]]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def rewardConfigurableLong(self, string: str, string2: str, toLongBiFunction: typing.Union[java.util.function.ToLongBiFunction[_BiConstraintStream__A, _BiConstraintStream__B], typing.Callable[[_BiConstraintStream__A, _BiConstraintStream__B], int]]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def rewardConfigurableLong(self, string: str, toLongBiFunction: typing.Union[java.util.function.ToLongBiFunction[_BiConstraintStream__A, _BiConstraintStream__B], typing.Callable[[_BiConstraintStream__A, _BiConstraintStream__B], int]]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def rewardLong(self, string: str, string2: str, score: org.optaplanner.core.api.score.Score[typing.Any], toLongBiFunction: typing.Union[java.util.function.ToLongBiFunction[_BiConstraintStream__A, _BiConstraintStream__B], typing.Callable[[_BiConstraintStream__A, _BiConstraintStream__B], int]]) -> org.optaplanner.core.api.score.stream.Constraint: ...
    @typing.overload
    def rewardLong(self, string: str, score: org.optaplanner.core.api.score.Score[typing.Any], toLongBiFunction: typing.Union[java.util.function.ToLongBiFunction[_BiConstraintStream__A, _BiConstraintStream__B], typing.Callable[[_BiConstraintStream__A, _BiConstraintStream__B], int]]) -> org.optaplanner.core.api.score.stream.Constraint: ...

_BiJoiner__A = typing.TypeVar('_BiJoiner__A')  # <A>
_BiJoiner__B = typing.TypeVar('_BiJoiner__B')  # <B>
class BiJoiner(typing.Generic[_BiJoiner__A, _BiJoiner__B]):
    """
    public interface BiJoiner<A, B>
    
        Created with :class:`~org.optaplanner.core.api.score.stream.Joiners`. Used by
        :meth:`~org.optaplanner.core.api.score.stream.uni.UniConstraintStream.join`, ...
    
        Also see:
            :class:`~org.optaplanner.core.api.score.stream.Joiners`
    """
    ...


class __module_protocol__(typing.Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.optaplanner.core.api.score.stream.bi")``.

    BiConstraintCollector: typing.Type[BiConstraintCollector]
    BiConstraintStream: typing.Type[BiConstraintStream]
    BiJoiner: typing.Type[BiJoiner]
