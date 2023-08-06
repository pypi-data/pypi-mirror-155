import java.lang
import java.util.function
import org.optaplanner.core.config
import typing



class ConstructionHeuristicForagerConfig(org.optaplanner.core.config.AbstractConfig['ConstructionHeuristicForagerConfig']):
    """
    public class ConstructionHeuristicForagerConfig extends :class:`~org.optaplanner.core.config.AbstractConfig`<:class:`~org.optaplanner.core.config.constructionheuristic.decider.forager.ConstructionHeuristicForagerConfig`>
    """
    def __init__(self): ...
    def copyConfig(self) -> 'ConstructionHeuristicForagerConfig':
        """
            Description copied from class: :meth:`~org.optaplanner.core.config.AbstractConfig.copyConfig`
            Typically implemented by constructing a new instance and calling
            :meth:`~org.optaplanner.core.config.AbstractConfig.inherit` on it
        
            Specified by:
                :meth:`~org.optaplanner.core.config.AbstractConfig.copyConfig` in
                class :class:`~org.optaplanner.core.config.AbstractConfig`
        
            Returns:
                new instance
        
        
        """
        ...
    def getPickEarlyType(self) -> 'ConstructionHeuristicPickEarlyType': ...
    def inherit(self, constructionHeuristicForagerConfig: 'ConstructionHeuristicForagerConfig') -> 'ConstructionHeuristicForagerConfig':
        """
            Description copied from class: :meth:`~org.optaplanner.core.config.AbstractConfig.inherit`
            Inherits each property of the :code:`inheritedConfig` unless that property (or a semantic alternative) is defined by
            this instance (which overwrites the inherited behaviour).
        
            After the inheritance, if a property on this :class:`~org.optaplanner.core.config.AbstractConfig` composition is
            replaced, it should not affect the inherited composition instance.
        
            Specified by:
                :meth:`~org.optaplanner.core.config.AbstractConfig.inherit` in
                class :class:`~org.optaplanner.core.config.AbstractConfig`
        
            Parameters:
                inheritedConfig (:class:`~org.optaplanner.core.config.constructionheuristic.decider.forager.ConstructionHeuristicForagerConfig`): never null
        
            Returns:
                this
        
        
        """
        ...
    def setPickEarlyType(self, constructionHeuristicPickEarlyType: 'ConstructionHeuristicPickEarlyType') -> None: ...
    def visitReferencedClasses(self, consumer: typing.Union[java.util.function.Consumer[typing.Type[typing.Any]], typing.Callable[[typing.Type[typing.Any]], None]]) -> None: ...

class ConstructionHeuristicPickEarlyType(java.lang.Enum['ConstructionHeuristicPickEarlyType']):
    """
    public enum ConstructionHeuristicPickEarlyType extends :class:`~org.optaplanner.core.config.constructionheuristic.decider.forager.https:.docs.oracle.com.javase.8.docs.api.java.lang.Enum?is`<:class:`~org.optaplanner.core.config.constructionheuristic.decider.forager.ConstructionHeuristicPickEarlyType`>
    """
    NEVER: typing.ClassVar['ConstructionHeuristicPickEarlyType'] = ...
    FIRST_NON_DETERIORATING_SCORE: typing.ClassVar['ConstructionHeuristicPickEarlyType'] = ...
    FIRST_FEASIBLE_SCORE: typing.ClassVar['ConstructionHeuristicPickEarlyType'] = ...
    FIRST_FEASIBLE_SCORE_OR_NON_DETERIORATING_HARD: typing.ClassVar['ConstructionHeuristicPickEarlyType'] = ...
    _valueOf_0__T = typing.TypeVar('_valueOf_0__T', bound=java.lang.Enum)  # <T>
    @typing.overload
    @staticmethod
    def valueOf(class_: typing.Type[_valueOf_0__T], string: str) -> _valueOf_0__T: ...
    @typing.overload
    @staticmethod
    def valueOf(string: str) -> 'ConstructionHeuristicPickEarlyType':
        """
            Returns the enum constant of this type with the specified name. The string must match *exactly* an identifier used to
            declare an enum constant in this type. (Extraneous whitespace characters are not permitted.)
        
            Parameters:
                name (:class:`~org.optaplanner.core.config.constructionheuristic.decider.forager.https:.docs.oracle.com.javase.8.docs.api.java.lang.String?is`): the name of the enum constant to be returned.
        
            Returns:
                the enum constant with the specified name
        
            Raises:
                :class:`~org.optaplanner.core.config.constructionheuristic.decider.forager.https:.docs.oracle.com.javase.8.docs.api.java.lang.IllegalArgumentException?is`: if this enum type has no constant with the specified name
                :class:`~org.optaplanner.core.config.constructionheuristic.decider.forager.https:.docs.oracle.com.javase.8.docs.api.java.lang.NullPointerException?is`: if the argument is null
        
        
        """
        ...
    @staticmethod
    def values() -> typing.List['ConstructionHeuristicPickEarlyType']:
        """
            Returns an array containing the constants of this enum type, in the order they are declared. This method may be used to
            iterate over the constants as follows:
        
            .. code-block: java
            
            for (ConstructionHeuristicPickEarlyType c : ConstructionHeuristicPickEarlyType.values())
                System.out.println(c);
            
        
            Returns:
                an array containing the constants of this enum type, in the order they are declared
        
        
        """
        ...


class __module_protocol__(typing.Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.optaplanner.core.config.constructionheuristic.decider.forager")``.

    ConstructionHeuristicForagerConfig: typing.Type[ConstructionHeuristicForagerConfig]
    ConstructionHeuristicPickEarlyType: typing.Type[ConstructionHeuristicPickEarlyType]
