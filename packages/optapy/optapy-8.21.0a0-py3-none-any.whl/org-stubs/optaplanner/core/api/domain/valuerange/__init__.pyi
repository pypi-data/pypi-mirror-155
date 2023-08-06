import decimal
import java.lang.annotation
import java.math
import java.time
import java.time.temporal
import java.util
import typing



_ValueRange__T = typing.TypeVar('_ValueRange__T')  # <T>
class ValueRange(typing.Generic[_ValueRange__T]):
    """
    public interface ValueRange<T>
    
        A ValueRange is a set of a values for a :class:`~org.optaplanner.core.api.domain.variable.PlanningVariable`. These
        values might be stored in memory as a
        :class:`~org.optaplanner.core.api.domain.valuerange.https:.docs.oracle.com.javase.8.docs.api.java.util.Collection?is`
        (usually a
        :class:`~org.optaplanner.core.api.domain.valuerange.https:.docs.oracle.com.javase.8.docs.api.java.util.List?is` or
        :class:`~org.optaplanner.core.api.domain.valuerange.https:.docs.oracle.com.javase.8.docs.api.java.util.Set?is`), but if
        the values are numbers, they can also be stored in memory by their bounds to use less memory and provide more
        opportunities.
    
        ValueRange is stateful. Prefer using :class:`~org.optaplanner.core.api.domain.valuerange.CountableValueRange` (which
        extends this interface) whenever possible. Implementations must be immutable.
    
        Also see:
            :class:`~org.optaplanner.core.api.domain.valuerange.ValueRangeFactory`,
            :class:`~org.optaplanner.core.api.domain.valuerange.CountableValueRange`
    """
    def contains(self, t: _ValueRange__T) -> bool:
        """
        
            Parameters:
                value (:class:`~org.optaplanner.core.api.domain.valuerange.ValueRange`): sometimes null
        
            Returns:
                true if the ValueRange contains that value
        
        
        """
        ...
    def createRandomIterator(self, random: java.util.Random) -> java.util.Iterator[_ValueRange__T]: ...
    def isEmpty(self) -> bool:
        """
            In a :class:`~org.optaplanner.core.api.domain.valuerange.CountableValueRange`, this must be consistent with
            :meth:`~org.optaplanner.core.api.domain.valuerange.CountableValueRange.getSize`.
        
            Returns:
                true if the range is empty
        
        
        """
        ...

class ValueRangeFactory:
    """
    public final class ValueRangeFactory extends :class:`~org.optaplanner.core.api.domain.valuerange.https:.docs.oracle.com.javase.8.docs.api.java.lang.Object?is`
    
        Factory for :class:`~org.optaplanner.core.api.domain.valuerange.ValueRange`.
    """
    def __init__(self): ...
    @typing.overload
    @staticmethod
    def createBigDecimalValueRange(bigDecimal: typing.Union[java.math.BigDecimal, decimal.Decimal], bigDecimal2: typing.Union[java.math.BigDecimal, decimal.Decimal]) -> 'CountableValueRange'[java.math.BigDecimal]: ...
    @typing.overload
    @staticmethod
    def createBigDecimalValueRange(bigDecimal: typing.Union[java.math.BigDecimal, decimal.Decimal], bigDecimal2: typing.Union[java.math.BigDecimal, decimal.Decimal], bigDecimal3: typing.Union[java.math.BigDecimal, decimal.Decimal]) -> 'CountableValueRange'[java.math.BigDecimal]: ...
    @typing.overload
    @staticmethod
    def createBigIntegerValueRange(bigInteger: java.math.BigInteger, bigInteger2: java.math.BigInteger) -> 'CountableValueRange'[java.math.BigInteger]: ...
    @typing.overload
    @staticmethod
    def createBigIntegerValueRange(bigInteger: java.math.BigInteger, bigInteger2: java.math.BigInteger, bigInteger3: java.math.BigInteger) -> 'CountableValueRange'[java.math.BigInteger]: ...
    @staticmethod
    def createBooleanValueRange() -> 'CountableValueRange'[bool]: ...
    @staticmethod
    def createDoubleValueRange(double: float, double2: float) -> ValueRange[float]: ...
    @typing.overload
    @staticmethod
    def createIntValueRange(int: int, int2: int) -> 'CountableValueRange'[int]: ...
    @typing.overload
    @staticmethod
    def createIntValueRange(int: int, int2: int, int3: int) -> 'CountableValueRange'[int]: ...
    @staticmethod
    def createLocalDateTimeValueRange(localDateTime: java.time.LocalDateTime, localDateTime2: java.time.LocalDateTime, long: int, temporalUnit: java.time.temporal.TemporalUnit) -> 'CountableValueRange'[java.time.LocalDateTime]: ...
    @staticmethod
    def createLocalDateValueRange(localDate: java.time.LocalDate, localDate2: java.time.LocalDate, long: int, temporalUnit: java.time.temporal.TemporalUnit) -> 'CountableValueRange'[java.time.LocalDate]: ...
    @staticmethod
    def createLocalTimeValueRange(localTime: java.time.LocalTime, localTime2: java.time.LocalTime, long: int, temporalUnit: java.time.temporal.TemporalUnit) -> 'CountableValueRange'[java.time.LocalTime]: ...
    @typing.overload
    @staticmethod
    def createLongValueRange(long: int, long2: int) -> 'CountableValueRange'[int]: ...
    @typing.overload
    @staticmethod
    def createLongValueRange(long: int, long2: int, long3: int) -> 'CountableValueRange'[int]: ...
    _createTemporalValueRange__Temporal_ = typing.TypeVar('_createTemporalValueRange__Temporal_', bound=java.time.temporal.Temporal)  # <Temporal_>
    @staticmethod
    def createTemporalValueRange(temporal_: _createTemporalValueRange__Temporal_, temporal_2: _createTemporalValueRange__Temporal_, long: int, temporalUnit: java.time.temporal.TemporalUnit) -> 'CountableValueRange'[_createTemporalValueRange__Temporal_]: ...

class ValueRangeProvider(java.lang.annotation.Annotation):
    """
    :class:`~org.optaplanner.core.api.domain.valuerange.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.Target?is`({:meth:`~org.optaplanner.core.api.domain.valuerange.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.ElementType.html?is`,:meth:`~org.optaplanner.core.api.domain.valuerange.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.ElementType.html?is`}) :class:`~org.optaplanner.core.api.domain.valuerange.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.Retention?is`(:meth:`~org.optaplanner.core.api.domain.valuerange.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.RetentionPolicy.html?is`) public @interface ValueRangeProvider
    
        Provides the planning values that can be used for a :class:`~org.optaplanner.core.api.domain.variable.PlanningVariable`.
    
        This is specified on a getter of a java bean property (or directly on a field) which returns a
        :class:`~org.optaplanner.core.api.domain.valuerange.https:.docs.oracle.com.javase.8.docs.api.java.util.Collection?is` or
        :class:`~org.optaplanner.core.api.domain.valuerange.ValueRange`. A
        :class:`~org.optaplanner.core.api.domain.valuerange.https:.docs.oracle.com.javase.8.docs.api.java.util.Collection?is` is
        implicitly converted to a :class:`~org.optaplanner.core.api.domain.valuerange.ValueRange`.
    """
    def equals(self, object: typing.Any) -> bool: ...
    def hashCode(self) -> int: ...
    def id(self) -> str: ...
    def toString(self) -> str: ...

_CountableValueRange__T = typing.TypeVar('_CountableValueRange__T')  # <T>
class CountableValueRange(ValueRange[_CountableValueRange__T], typing.Generic[_CountableValueRange__T]):
    """
    public interface CountableValueRange<T> extends :class:`~org.optaplanner.core.api.domain.valuerange.ValueRange`<T>
    
        A :class:`~org.optaplanner.core.api.domain.valuerange.ValueRange` that is ending. Therefore, it has a discrete (as in
        non-continuous) range.
    
        Also see:
            :class:`~org.optaplanner.core.api.domain.valuerange.ValueRangeFactory`,
            :class:`~org.optaplanner.core.api.domain.valuerange.ValueRange`
    """
    def createOriginalIterator(self) -> java.util.Iterator[_CountableValueRange__T]: ...
    def get(self, long: int) -> _CountableValueRange__T:
        """
            Used by uniform random selection in a composite or nullable CountableValueRange.
        
            Parameters:
                index (long): always :code:`<` :meth:`~org.optaplanner.core.api.domain.valuerange.CountableValueRange.getSize`
        
            Returns:
                sometimes null (if :meth:`~org.optaplanner.core.api.domain.variable.PlanningVariable.nullable` is true)
        
        
        """
        ...
    def getSize(self) -> int:
        """
            Used by uniform random selection in a composite or nullable CountableValueRange.
        
            Returns:
                the exact number of elements generated by this :class:`~org.optaplanner.core.api.domain.valuerange.CountableValueRange`,
                always :code:`>= 0`
        
        
        """
        ...


class __module_protocol__(typing.Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.optaplanner.core.api.domain.valuerange")``.

    CountableValueRange: typing.Type[CountableValueRange]
    ValueRange: typing.Type[ValueRange]
    ValueRangeFactory: typing.Type[ValueRangeFactory]
    ValueRangeProvider: typing.Type[ValueRangeProvider]
