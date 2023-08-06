import java.lang
import java.lang.annotation
import typing



class LookUpStrategyType(java.lang.Enum['LookUpStrategyType']):
    """
    public enum LookUpStrategyType extends :class:`~org.optaplanner.core.api.domain.lookup.https:.docs.oracle.com.javase.8.docs.api.java.lang.Enum?is`<:class:`~org.optaplanner.core.api.domain.lookup.LookUpStrategyType`>
    
        Determines how :meth:`~org.optaplanner.core.api.score.director.ScoreDirector.lookUpWorkingObject` maps a
        :class:`~org.optaplanner.core.api.domain.solution.ProblemFactCollectionProperty` or a
        :class:`~org.optaplanner.core.api.domain.entity.PlanningEntity` from an external copy to the internal one.
    """
    PLANNING_ID_OR_NONE: typing.ClassVar['LookUpStrategyType'] = ...
    PLANNING_ID_OR_FAIL_FAST: typing.ClassVar['LookUpStrategyType'] = ...
    EQUALITY: typing.ClassVar['LookUpStrategyType'] = ...
    NONE: typing.ClassVar['LookUpStrategyType'] = ...
    _valueOf_0__T = typing.TypeVar('_valueOf_0__T', bound=java.lang.Enum)  # <T>
    @typing.overload
    @staticmethod
    def valueOf(class_: typing.Type[_valueOf_0__T], string: str) -> _valueOf_0__T: ...
    @typing.overload
    @staticmethod
    def valueOf(string: str) -> 'LookUpStrategyType':
        """
            Returns the enum constant of this type with the specified name. The string must match *exactly* an identifier used to
            declare an enum constant in this type. (Extraneous whitespace characters are not permitted.)
        
            Parameters:
                name (:class:`~org.optaplanner.core.api.domain.lookup.https:.docs.oracle.com.javase.8.docs.api.java.lang.String?is`): the name of the enum constant to be returned.
        
            Returns:
                the enum constant with the specified name
        
            Raises:
                :class:`~org.optaplanner.core.api.domain.lookup.https:.docs.oracle.com.javase.8.docs.api.java.lang.IllegalArgumentException?is`: if this enum type has no constant with the specified name
                :class:`~org.optaplanner.core.api.domain.lookup.https:.docs.oracle.com.javase.8.docs.api.java.lang.NullPointerException?is`: if the argument is null
        
        
        """
        ...
    @staticmethod
    def values() -> typing.List['LookUpStrategyType']:
        """
            Returns an array containing the constants of this enum type, in the order they are declared. This method may be used to
            iterate over the constants as follows:
        
            .. code-block: java
            
            for (LookUpStrategyType c : LookUpStrategyType.values())
                System.out.println(c);
            
        
            Returns:
                an array containing the constants of this enum type, in the order they are declared
        
        
        """
        ...

class PlanningId(java.lang.annotation.Annotation):
    """
    :class:`~org.optaplanner.core.api.domain.lookup.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.Target?is`({:meth:`~org.optaplanner.core.api.domain.lookup.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.ElementType.html?is`,:meth:`~org.optaplanner.core.api.domain.lookup.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.ElementType.html?is`}) :class:`~org.optaplanner.core.api.domain.lookup.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.Retention?is`(:meth:`~org.optaplanner.core.api.domain.lookup.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.RetentionPolicy.html?is`) public @interface PlanningId
    
        Specifies that a bean property (or a field) is the id to match when
        :meth:`~org.optaplanner.core.api.score.director.ScoreDirector.lookUpWorkingObject` an externalObject (often from another
        :class:`~org.optaplanner.core.api.domain.lookup.https:.docs.oracle.com.javase.8.docs.api.java.lang.Thread?is` or JVM).
        Used during :class:`~org.optaplanner.core.impl.heuristic.move.Move` rebasing and in a
        :class:`~org.optaplanner.core.api.solver.change.ProblemChange`.
    
        It is specified on a getter of a java bean property (or directly on a field) of a
        :class:`~org.optaplanner.core.api.domain.entity.PlanningEntity` class,
        :class:`~org.optaplanner.core.api.domain.valuerange.ValueRangeProvider` class or any
        :class:`~org.optaplanner.core.api.domain.solution.ProblemFactCollectionProperty` class.
    
        The return type can be any
        :class:`~org.optaplanner.core.api.domain.lookup.https:.docs.oracle.com.javase.8.docs.api.java.lang.Comparable?is` type
        which overrides
        :meth:`~org.optaplanner.core.api.domain.lookup.https:.docs.oracle.com.javase.8.docs.api.java.lang.Object.html?is` and
        :meth:`~org.optaplanner.core.api.domain.lookup.https:.docs.oracle.com.javase.8.docs.api.java.lang.Object.html?is`, and
        is usually :class:`~org.optaplanner.core.api.domain.lookup.https:.docs.oracle.com.javase.8.docs.api.java.lang.Long?is`
        or :class:`~org.optaplanner.core.api.domain.lookup.https:.docs.oracle.com.javase.8.docs.api.java.lang.String?is`. It
        must never return a null instance.
    """
    def equals(self, object: typing.Any) -> bool: ...
    def hashCode(self) -> int: ...
    def toString(self) -> str: ...


class __module_protocol__(typing.Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.optaplanner.core.api.domain.lookup")``.

    LookUpStrategyType: typing.Type[LookUpStrategyType]
    PlanningId: typing.Type[PlanningId]
