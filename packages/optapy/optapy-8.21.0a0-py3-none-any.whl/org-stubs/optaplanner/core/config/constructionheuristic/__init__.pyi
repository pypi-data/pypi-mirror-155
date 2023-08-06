import java.lang
import java.util
import java.util.function
import org.optaplanner.core.config.constructionheuristic.decider
import org.optaplanner.core.config.constructionheuristic.decider.forager
import org.optaplanner.core.config.constructionheuristic.placer
import org.optaplanner.core.config.heuristic.selector.entity
import org.optaplanner.core.config.heuristic.selector.move
import org.optaplanner.core.config.heuristic.selector.value
import org.optaplanner.core.config.phase
import typing



class ConstructionHeuristicPhaseConfig(org.optaplanner.core.config.phase.PhaseConfig['ConstructionHeuristicPhaseConfig']):
    """
    public class ConstructionHeuristicPhaseConfig extends :class:`~org.optaplanner.core.config.phase.PhaseConfig`<:class:`~org.optaplanner.core.config.constructionheuristic.ConstructionHeuristicPhaseConfig`>
    """
    XML_ELEMENT_NAME: typing.ClassVar[str] = ...
    """
    public static final :class:`~org.optaplanner.core.config.constructionheuristic.https:.docs.oracle.com.javase.8.docs.api.java.lang.String?is` XML_ELEMENT_NAME
    
    
        Also see:
            :meth:`~constant`
    
    
    """
    def __init__(self): ...
    def copyConfig(self) -> 'ConstructionHeuristicPhaseConfig':
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
    def getConstructionHeuristicType(self) -> 'ConstructionHeuristicType': ...
    def getEntityPlacerConfig(self) -> org.optaplanner.core.config.constructionheuristic.placer.EntityPlacerConfig: ...
    def getEntitySorterManner(self) -> org.optaplanner.core.config.heuristic.selector.entity.EntitySorterManner: ...
    def getForagerConfig(self) -> org.optaplanner.core.config.constructionheuristic.decider.forager.ConstructionHeuristicForagerConfig: ...
    def getMoveSelectorConfigList(self) -> java.util.List[org.optaplanner.core.config.heuristic.selector.move.MoveSelectorConfig]: ...
    def getValueSorterManner(self) -> org.optaplanner.core.config.heuristic.selector.value.ValueSorterManner: ...
    def inherit(self, constructionHeuristicPhaseConfig: 'ConstructionHeuristicPhaseConfig') -> 'ConstructionHeuristicPhaseConfig':
        """
            Description copied from class: :meth:`~org.optaplanner.core.config.AbstractConfig.inherit`
            Inherits each property of the :code:`inheritedConfig` unless that property (or a semantic alternative) is defined by
            this instance (which overwrites the inherited behaviour).
        
            After the inheritance, if a property on this :class:`~org.optaplanner.core.config.AbstractConfig` composition is
            replaced, it should not affect the inherited composition instance.
        
            Overrides:
                :meth:`~org.optaplanner.core.config.phase.PhaseConfig.inherit` in
                class :class:`~org.optaplanner.core.config.phase.PhaseConfig`
        
            Parameters:
                inheritedConfig (:class:`~org.optaplanner.core.config.constructionheuristic.ConstructionHeuristicPhaseConfig`): never null
        
            Returns:
                this
        
        
        """
        ...
    def setConstructionHeuristicType(self, constructionHeuristicType: 'ConstructionHeuristicType') -> None: ...
    def setEntityPlacerConfig(self, entityPlacerConfig: org.optaplanner.core.config.constructionheuristic.placer.EntityPlacerConfig) -> None: ...
    def setEntitySorterManner(self, entitySorterManner: org.optaplanner.core.config.heuristic.selector.entity.EntitySorterManner) -> None: ...
    def setForagerConfig(self, constructionHeuristicForagerConfig: org.optaplanner.core.config.constructionheuristic.decider.forager.ConstructionHeuristicForagerConfig) -> None: ...
    def setMoveSelectorConfigList(self, list: java.util.List[org.optaplanner.core.config.heuristic.selector.move.MoveSelectorConfig]) -> None: ...
    def setValueSorterManner(self, valueSorterManner: org.optaplanner.core.config.heuristic.selector.value.ValueSorterManner) -> None: ...
    def visitReferencedClasses(self, consumer: typing.Union[java.util.function.Consumer[typing.Type[typing.Any]], typing.Callable[[typing.Type[typing.Any]], None]]) -> None: ...
    def withConstructionHeuristicType(self, constructionHeuristicType: 'ConstructionHeuristicType') -> 'ConstructionHeuristicPhaseConfig': ...
    def withEntityPlacerConfig(self, entityPlacerConfig: org.optaplanner.core.config.constructionheuristic.placer.EntityPlacerConfig[typing.Any]) -> 'ConstructionHeuristicPhaseConfig': ...
    def withEntitySorterManner(self, entitySorterManner: org.optaplanner.core.config.heuristic.selector.entity.EntitySorterManner) -> 'ConstructionHeuristicPhaseConfig': ...
    def withForagerConfig(self, constructionHeuristicForagerConfig: org.optaplanner.core.config.constructionheuristic.decider.forager.ConstructionHeuristicForagerConfig) -> 'ConstructionHeuristicPhaseConfig': ...
    def withMoveSelectorConfigList(self, list: java.util.List[org.optaplanner.core.config.heuristic.selector.move.MoveSelectorConfig]) -> 'ConstructionHeuristicPhaseConfig': ...
    def withValueSorterManner(self, valueSorterManner: org.optaplanner.core.config.heuristic.selector.value.ValueSorterManner) -> 'ConstructionHeuristicPhaseConfig': ...

class ConstructionHeuristicType(java.lang.Enum['ConstructionHeuristicType']):
    """
    public enum ConstructionHeuristicType extends :class:`~org.optaplanner.core.config.constructionheuristic.https:.docs.oracle.com.javase.8.docs.api.java.lang.Enum?is`<:class:`~org.optaplanner.core.config.constructionheuristic.ConstructionHeuristicType`>
    """
    FIRST_FIT: typing.ClassVar['ConstructionHeuristicType'] = ...
    FIRST_FIT_DECREASING: typing.ClassVar['ConstructionHeuristicType'] = ...
    WEAKEST_FIT: typing.ClassVar['ConstructionHeuristicType'] = ...
    WEAKEST_FIT_DECREASING: typing.ClassVar['ConstructionHeuristicType'] = ...
    STRONGEST_FIT: typing.ClassVar['ConstructionHeuristicType'] = ...
    STRONGEST_FIT_DECREASING: typing.ClassVar['ConstructionHeuristicType'] = ...
    ALLOCATE_ENTITY_FROM_QUEUE: typing.ClassVar['ConstructionHeuristicType'] = ...
    ALLOCATE_TO_VALUE_FROM_QUEUE: typing.ClassVar['ConstructionHeuristicType'] = ...
    CHEAPEST_INSERTION: typing.ClassVar['ConstructionHeuristicType'] = ...
    ALLOCATE_FROM_POOL: typing.ClassVar['ConstructionHeuristicType'] = ...
    @staticmethod
    def getBluePrintTypes() -> typing.List['ConstructionHeuristicType']:
        """
        
            Returns:
                :meth:`~org.optaplanner.core.config.constructionheuristic.ConstructionHeuristicType.values` without duplicates (abstract
                types that end up behaving as one of the other types).
        
        
        """
        ...
    def getDefaultEntitySorterManner(self) -> org.optaplanner.core.config.heuristic.selector.entity.EntitySorterManner: ...
    def getDefaultValueSorterManner(self) -> org.optaplanner.core.config.heuristic.selector.value.ValueSorterManner: ...
    _valueOf_0__T = typing.TypeVar('_valueOf_0__T', bound=java.lang.Enum)  # <T>
    @typing.overload
    @staticmethod
    def valueOf(class_: typing.Type[_valueOf_0__T], string: str) -> _valueOf_0__T: ...
    @typing.overload
    @staticmethod
    def valueOf(string: str) -> 'ConstructionHeuristicType':
        """
            Returns the enum constant of this type with the specified name. The string must match *exactly* an identifier used to
            declare an enum constant in this type. (Extraneous whitespace characters are not permitted.)
        
            Parameters:
                name (:class:`~org.optaplanner.core.config.constructionheuristic.https:.docs.oracle.com.javase.8.docs.api.java.lang.String?is`): the name of the enum constant to be returned.
        
            Returns:
                the enum constant with the specified name
        
            Raises:
                :class:`~org.optaplanner.core.config.constructionheuristic.https:.docs.oracle.com.javase.8.docs.api.java.lang.IllegalArgumentException?is`: if this enum type has no constant with the specified name
                :class:`~org.optaplanner.core.config.constructionheuristic.https:.docs.oracle.com.javase.8.docs.api.java.lang.NullPointerException?is`: if the argument is null
        
        
        """
        ...
    @staticmethod
    def values() -> typing.List['ConstructionHeuristicType']:
        """
            Returns an array containing the constants of this enum type, in the order they are declared. This method may be used to
            iterate over the constants as follows:
        
            .. code-block: java
            
            for (ConstructionHeuristicType c : ConstructionHeuristicType.values())
                System.out.println(c);
            
        
            Returns:
                an array containing the constants of this enum type, in the order they are declared
        
        
        """
        ...


class __module_protocol__(typing.Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.optaplanner.core.config.constructionheuristic")``.

    ConstructionHeuristicPhaseConfig: typing.Type[ConstructionHeuristicPhaseConfig]
    ConstructionHeuristicType: typing.Type[ConstructionHeuristicType]
    decider: org.optaplanner.core.config.constructionheuristic.decider.__module_protocol__
    placer: org.optaplanner.core.config.constructionheuristic.placer.__module_protocol__
