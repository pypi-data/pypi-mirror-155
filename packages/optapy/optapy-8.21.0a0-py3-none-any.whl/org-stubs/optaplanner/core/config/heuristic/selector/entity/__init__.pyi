import java.lang
import java.util
import java.util.function
import org.optaplanner.core.config.heuristic.selector
import org.optaplanner.core.config.heuristic.selector.common
import org.optaplanner.core.config.heuristic.selector.common.decorator
import org.optaplanner.core.config.heuristic.selector.common.nearby
import org.optaplanner.core.config.heuristic.selector.entity.pillar
import org.optaplanner.core.impl.domain.entity.descriptor
import org.optaplanner.core.impl.heuristic.selector.common.decorator
import typing



class EntitySelectorConfig(org.optaplanner.core.config.heuristic.selector.SelectorConfig['EntitySelectorConfig']):
    """
    public class EntitySelectorConfig extends :class:`~org.optaplanner.core.config.heuristic.selector.SelectorConfig`<:class:`~org.optaplanner.core.config.heuristic.selector.entity.EntitySelectorConfig`>
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, class_: typing.Type[typing.Any]): ...
    @typing.overload
    def __init__(self, entitySelectorConfig: 'EntitySelectorConfig'): ...
    def copyConfig(self) -> 'EntitySelectorConfig':
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
    _determineSorter__Solution_ = typing.TypeVar('_determineSorter__Solution_')  # <Solution_>
    _determineSorter__T = typing.TypeVar('_determineSorter__T')  # <T>
    @staticmethod
    def determineSorter(entitySorterManner: 'EntitySorterManner', entityDescriptor: org.optaplanner.core.impl.domain.entity.descriptor.EntityDescriptor[_determineSorter__Solution_]) -> org.optaplanner.core.impl.heuristic.selector.common.decorator.SelectionSorter[_determineSorter__Solution_, _determineSorter__T]: ...
    def getCacheType(self) -> org.optaplanner.core.config.heuristic.selector.common.SelectionCacheType: ...
    def getEntityClass(self) -> typing.Type[typing.Any]: ...
    def getFilterClass(self) -> typing.Type[org.optaplanner.core.impl.heuristic.selector.common.decorator.SelectionFilter]: ...
    def getId(self) -> str: ...
    def getMimicSelectorRef(self) -> str: ...
    def getNearbySelectionConfig(self) -> org.optaplanner.core.config.heuristic.selector.common.nearby.NearbySelectionConfig: ...
    def getProbabilityWeightFactoryClass(self) -> typing.Type[org.optaplanner.core.impl.heuristic.selector.common.decorator.SelectionProbabilityWeightFactory]: ...
    def getSelectedCountLimit(self) -> int: ...
    def getSelectionOrder(self) -> org.optaplanner.core.config.heuristic.selector.common.SelectionOrder: ...
    def getSorterClass(self) -> typing.Type[org.optaplanner.core.impl.heuristic.selector.common.decorator.SelectionSorter]: ...
    def getSorterComparatorClass(self) -> typing.Type[java.util.Comparator]: ...
    def getSorterManner(self) -> 'EntitySorterManner': ...
    def getSorterOrder(self) -> org.optaplanner.core.config.heuristic.selector.common.decorator.SelectionSorterOrder: ...
    def getSorterWeightFactoryClass(self) -> typing.Type[org.optaplanner.core.impl.heuristic.selector.common.decorator.SelectionSorterWeightFactory]: ...
    _hasSorter__Solution_ = typing.TypeVar('_hasSorter__Solution_')  # <Solution_>
    @staticmethod
    def hasSorter(entitySorterManner: 'EntitySorterManner', entityDescriptor: org.optaplanner.core.impl.domain.entity.descriptor.EntityDescriptor[_hasSorter__Solution_]) -> bool: ...
    def inherit(self, entitySelectorConfig: 'EntitySelectorConfig') -> 'EntitySelectorConfig':
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
                inheritedConfig (:class:`~org.optaplanner.core.config.heuristic.selector.entity.EntitySelectorConfig`): never null
        
            Returns:
                this
        
        
        """
        ...
    @staticmethod
    def newMimicSelectorConfig(string: str) -> 'EntitySelectorConfig': ...
    def setCacheType(self, selectionCacheType: org.optaplanner.core.config.heuristic.selector.common.SelectionCacheType) -> None: ...
    def setEntityClass(self, class_: typing.Type[typing.Any]) -> None: ...
    def setFilterClass(self, class_: typing.Type[org.optaplanner.core.impl.heuristic.selector.common.decorator.SelectionFilter]) -> None: ...
    def setId(self, string: str) -> None: ...
    def setMimicSelectorRef(self, string: str) -> None: ...
    def setNearbySelectionConfig(self, nearbySelectionConfig: org.optaplanner.core.config.heuristic.selector.common.nearby.NearbySelectionConfig) -> None: ...
    def setProbabilityWeightFactoryClass(self, class_: typing.Type[org.optaplanner.core.impl.heuristic.selector.common.decorator.SelectionProbabilityWeightFactory]) -> None: ...
    def setSelectedCountLimit(self, long: int) -> None: ...
    def setSelectionOrder(self, selectionOrder: org.optaplanner.core.config.heuristic.selector.common.SelectionOrder) -> None: ...
    def setSorterClass(self, class_: typing.Type[org.optaplanner.core.impl.heuristic.selector.common.decorator.SelectionSorter]) -> None: ...
    def setSorterComparatorClass(self, class_: typing.Type[java.util.Comparator]) -> None: ...
    def setSorterManner(self, entitySorterManner: 'EntitySorterManner') -> None: ...
    def setSorterOrder(self, selectionSorterOrder: org.optaplanner.core.config.heuristic.selector.common.decorator.SelectionSorterOrder) -> None: ...
    def setSorterWeightFactoryClass(self, class_: typing.Type[org.optaplanner.core.impl.heuristic.selector.common.decorator.SelectionSorterWeightFactory]) -> None: ...
    def toString(self) -> str:
        """
        
            Overrides:
                :meth:`~org.optaplanner.core.config.AbstractConfig.toString` in
                class :class:`~org.optaplanner.core.config.AbstractConfig`
        
        
        """
        ...
    def visitReferencedClasses(self, consumer: typing.Union[java.util.function.Consumer[typing.Type[typing.Any]], typing.Callable[[typing.Type[typing.Any]], None]]) -> None: ...

class EntitySorterManner(java.lang.Enum['EntitySorterManner']):
    """
    public enum EntitySorterManner extends :class:`~org.optaplanner.core.config.heuristic.selector.entity.https:.docs.oracle.com.javase.8.docs.api.java.lang.Enum?is`<:class:`~org.optaplanner.core.config.heuristic.selector.entity.EntitySorterManner`>
    
        The manner of sorting :class:`~org.optaplanner.core.api.domain.entity.PlanningEntity` instances.
    """
    NONE: typing.ClassVar['EntitySorterManner'] = ...
    DECREASING_DIFFICULTY: typing.ClassVar['EntitySorterManner'] = ...
    DECREASING_DIFFICULTY_IF_AVAILABLE: typing.ClassVar['EntitySorterManner'] = ...
    _valueOf_0__T = typing.TypeVar('_valueOf_0__T', bound=java.lang.Enum)  # <T>
    @typing.overload
    @staticmethod
    def valueOf(class_: typing.Type[_valueOf_0__T], string: str) -> _valueOf_0__T: ...
    @typing.overload
    @staticmethod
    def valueOf(string: str) -> 'EntitySorterManner':
        """
            Returns the enum constant of this type with the specified name. The string must match *exactly* an identifier used to
            declare an enum constant in this type. (Extraneous whitespace characters are not permitted.)
        
            Parameters:
                name (:class:`~org.optaplanner.core.config.heuristic.selector.entity.https:.docs.oracle.com.javase.8.docs.api.java.lang.String?is`): the name of the enum constant to be returned.
        
            Returns:
                the enum constant with the specified name
        
            Raises:
                :class:`~org.optaplanner.core.config.heuristic.selector.entity.https:.docs.oracle.com.javase.8.docs.api.java.lang.IllegalArgumentException?is`: if this enum type has no constant with the specified name
                :class:`~org.optaplanner.core.config.heuristic.selector.entity.https:.docs.oracle.com.javase.8.docs.api.java.lang.NullPointerException?is`: if the argument is null
        
        
        """
        ...
    @staticmethod
    def values() -> typing.List['EntitySorterManner']:
        """
            Returns an array containing the constants of this enum type, in the order they are declared. This method may be used to
            iterate over the constants as follows:
        
            .. code-block: java
            
            for (EntitySorterManner c : EntitySorterManner.values())
                System.out.println(c);
            
        
            Returns:
                an array containing the constants of this enum type, in the order they are declared
        
        
        """
        ...


class __module_protocol__(typing.Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.optaplanner.core.config.heuristic.selector.entity")``.

    EntitySelectorConfig: typing.Type[EntitySelectorConfig]
    EntitySorterManner: typing.Type[EntitySorterManner]
    pillar: org.optaplanner.core.config.heuristic.selector.entity.pillar.__module_protocol__
