import java.lang
import java.util.function
import org.optaplanner.core.config.heuristic.selector
import org.optaplanner.core.config.heuristic.selector.common
import org.optaplanner.core.config.heuristic.selector.entity
import org.optaplanner.core.impl.heuristic.selector.common.nearby
import typing



class NearbySelectionConfig(org.optaplanner.core.config.heuristic.selector.SelectorConfig['NearbySelectionConfig']):
    """
    public class NearbySelectionConfig extends :class:`~org.optaplanner.core.config.heuristic.selector.SelectorConfig`<:class:`~org.optaplanner.core.config.heuristic.selector.common.nearby.NearbySelectionConfig`>
    """
    def __init__(self): ...
    def copyConfig(self) -> 'NearbySelectionConfig':
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
    def getBetaDistributionAlpha(self) -> float: ...
    def getBetaDistributionBeta(self) -> float: ...
    def getBlockDistributionSizeMaximum(self) -> int: ...
    def getBlockDistributionSizeMinimum(self) -> int: ...
    def getBlockDistributionSizeRatio(self) -> float: ...
    def getBlockDistributionUniformDistributionProbability(self) -> float: ...
    def getLinearDistributionSizeMaximum(self) -> int: ...
    def getNearbyDistanceMeterClass(self) -> typing.Type[org.optaplanner.core.impl.heuristic.selector.common.nearby.NearbyDistanceMeter]: ...
    def getNearbySelectionDistributionType(self) -> 'NearbySelectionDistributionType': ...
    def getOriginEntitySelectorConfig(self) -> org.optaplanner.core.config.heuristic.selector.entity.EntitySelectorConfig: ...
    def getParabolicDistributionSizeMaximum(self) -> int: ...
    def inherit(self, nearbySelectionConfig: 'NearbySelectionConfig') -> 'NearbySelectionConfig':
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
                inheritedConfig (:class:`~org.optaplanner.core.config.heuristic.selector.common.nearby.NearbySelectionConfig`): never null
        
            Returns:
                this
        
        
        """
        ...
    def setBetaDistributionAlpha(self, double: float) -> None: ...
    def setBetaDistributionBeta(self, double: float) -> None: ...
    def setBlockDistributionSizeMaximum(self, integer: int) -> None: ...
    def setBlockDistributionSizeMinimum(self, integer: int) -> None: ...
    def setBlockDistributionSizeRatio(self, double: float) -> None: ...
    def setBlockDistributionUniformDistributionProbability(self, double: float) -> None: ...
    def setLinearDistributionSizeMaximum(self, integer: int) -> None: ...
    def setNearbyDistanceMeterClass(self, class_: typing.Type[org.optaplanner.core.impl.heuristic.selector.common.nearby.NearbyDistanceMeter]) -> None: ...
    def setNearbySelectionDistributionType(self, nearbySelectionDistributionType: 'NearbySelectionDistributionType') -> None: ...
    def setOriginEntitySelectorConfig(self, entitySelectorConfig: org.optaplanner.core.config.heuristic.selector.entity.EntitySelectorConfig) -> None: ...
    def setParabolicDistributionSizeMaximum(self, integer: int) -> None: ...
    def validateNearby(self, selectionCacheType: org.optaplanner.core.config.heuristic.selector.common.SelectionCacheType, selectionOrder: org.optaplanner.core.config.heuristic.selector.common.SelectionOrder) -> None: ...
    def visitReferencedClasses(self, consumer: typing.Union[java.util.function.Consumer[typing.Type[typing.Any]], typing.Callable[[typing.Type[typing.Any]], None]]) -> None: ...

class NearbySelectionDistributionType(java.lang.Enum['NearbySelectionDistributionType']):
    """
    public enum NearbySelectionDistributionType extends :class:`~org.optaplanner.core.config.heuristic.selector.common.nearby.https:.docs.oracle.com.javase.8.docs.api.java.lang.Enum?is`<:class:`~org.optaplanner.core.config.heuristic.selector.common.nearby.NearbySelectionDistributionType`>
    """
    BLOCK_DISTRIBUTION: typing.ClassVar['NearbySelectionDistributionType'] = ...
    LINEAR_DISTRIBUTION: typing.ClassVar['NearbySelectionDistributionType'] = ...
    PARABOLIC_DISTRIBUTION: typing.ClassVar['NearbySelectionDistributionType'] = ...
    BETA_DISTRIBUTION: typing.ClassVar['NearbySelectionDistributionType'] = ...
    _valueOf_0__T = typing.TypeVar('_valueOf_0__T', bound=java.lang.Enum)  # <T>
    @typing.overload
    @staticmethod
    def valueOf(class_: typing.Type[_valueOf_0__T], string: str) -> _valueOf_0__T: ...
    @typing.overload
    @staticmethod
    def valueOf(string: str) -> 'NearbySelectionDistributionType':
        """
            Returns the enum constant of this type with the specified name. The string must match *exactly* an identifier used to
            declare an enum constant in this type. (Extraneous whitespace characters are not permitted.)
        
            Parameters:
                name (:class:`~org.optaplanner.core.config.heuristic.selector.common.nearby.https:.docs.oracle.com.javase.8.docs.api.java.lang.String?is`): the name of the enum constant to be returned.
        
            Returns:
                the enum constant with the specified name
        
            Raises:
                :class:`~org.optaplanner.core.config.heuristic.selector.common.nearby.https:.docs.oracle.com.javase.8.docs.api.java.lang.IllegalArgumentException?is`: if this enum type has no constant with the specified name
                :class:`~org.optaplanner.core.config.heuristic.selector.common.nearby.https:.docs.oracle.com.javase.8.docs.api.java.lang.NullPointerException?is`: if the argument is null
        
        
        """
        ...
    @staticmethod
    def values() -> typing.List['NearbySelectionDistributionType']:
        """
            Returns an array containing the constants of this enum type, in the order they are declared. This method may be used to
            iterate over the constants as follows:
        
            .. code-block: java
            
            for (NearbySelectionDistributionType c : NearbySelectionDistributionType.values())
                System.out.println(c);
            
        
            Returns:
                an array containing the constants of this enum type, in the order they are declared
        
        
        """
        ...


class __module_protocol__(typing.Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.optaplanner.core.config.heuristic.selector.common.nearby")``.

    NearbySelectionConfig: typing.Type[NearbySelectionConfig]
    NearbySelectionDistributionType: typing.Type[NearbySelectionDistributionType]
