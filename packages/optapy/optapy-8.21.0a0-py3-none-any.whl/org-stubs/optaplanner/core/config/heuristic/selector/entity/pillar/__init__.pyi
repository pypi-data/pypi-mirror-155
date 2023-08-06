import java.util
import java.util.function
import org.optaplanner.core.config.heuristic.selector
import org.optaplanner.core.config.heuristic.selector.entity
import typing



class PillarSelectorConfig(org.optaplanner.core.config.heuristic.selector.SelectorConfig['PillarSelectorConfig']):
    """
    public class PillarSelectorConfig extends :class:`~org.optaplanner.core.config.heuristic.selector.SelectorConfig`<:class:`~org.optaplanner.core.config.heuristic.selector.entity.pillar.PillarSelectorConfig`>
    """
    def __init__(self): ...
    def copyConfig(self) -> 'PillarSelectorConfig':
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
    def getEntitySelectorConfig(self) -> org.optaplanner.core.config.heuristic.selector.entity.EntitySelectorConfig: ...
    def getMaximumSubPillarSize(self) -> int: ...
    def getMinimumSubPillarSize(self) -> int: ...
    def inherit(self, pillarSelectorConfig: 'PillarSelectorConfig') -> 'PillarSelectorConfig':
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
                inheritedConfig (:class:`~org.optaplanner.core.config.heuristic.selector.entity.pillar.PillarSelectorConfig`): never null
        
            Returns:
                this
        
        
        """
        ...
    def setEntitySelectorConfig(self, entitySelectorConfig: org.optaplanner.core.config.heuristic.selector.entity.EntitySelectorConfig) -> None: ...
    def setMaximumSubPillarSize(self, integer: int) -> None: ...
    def setMinimumSubPillarSize(self, integer: int) -> None: ...
    def toString(self) -> str:
        """
        
            Overrides:
                :meth:`~org.optaplanner.core.config.AbstractConfig.toString` in
                class :class:`~org.optaplanner.core.config.AbstractConfig`
        
        
        """
        ...
    def visitReferencedClasses(self, consumer: typing.Union[java.util.function.Consumer[typing.Type[typing.Any]], typing.Callable[[typing.Type[typing.Any]], None]]) -> None: ...

class SubPillarConfigPolicy:
    """
    public final class SubPillarConfigPolicy extends :class:`~org.optaplanner.core.config.heuristic.selector.entity.pillar.https:.docs.oracle.com.javase.8.docs.api.java.lang.Object?is`
    """
    def getEntityComparator(self) -> java.util.Comparator[typing.Any]:
        """
        
            Returns:
                Not null if the subpillars are to be treated as sequential. Always null if
                :meth:`~org.optaplanner.core.config.heuristic.selector.entity.pillar.SubPillarConfigPolicy.subPillarEnabled` is false.
        
        
        """
        ...
    def getMaximumSubPillarSize(self) -> int:
        """
        
            Returns:
                Less than 1 when
                :meth:`~org.optaplanner.core.config.heuristic.selector.entity.pillar.SubPillarConfigPolicy.isSubPillarEnabled` false.
        
        
        """
        ...
    def getMinimumSubPillarSize(self) -> int:
        """
        
            Returns:
                Less than 1 when
                :meth:`~org.optaplanner.core.config.heuristic.selector.entity.pillar.SubPillarConfigPolicy.isSubPillarEnabled` false.
        
        
        """
        ...
    def isSubPillarEnabled(self) -> bool: ...
    @staticmethod
    def sequential(int: int, int2: int, comparator: typing.Union[java.util.Comparator[typing.Any], typing.Callable[[typing.Any, typing.Any], int]]) -> 'SubPillarConfigPolicy': ...
    @staticmethod
    def sequentialUnlimited(comparator: typing.Union[java.util.Comparator[typing.Any], typing.Callable[[typing.Any, typing.Any], int]]) -> 'SubPillarConfigPolicy': ...
    @staticmethod
    def withSubpillars(int: int, int2: int) -> 'SubPillarConfigPolicy': ...
    @staticmethod
    def withSubpillarsUnlimited() -> 'SubPillarConfigPolicy': ...
    @staticmethod
    def withoutSubpillars() -> 'SubPillarConfigPolicy': ...


class __module_protocol__(typing.Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.optaplanner.core.config.heuristic.selector.entity.pillar")``.

    PillarSelectorConfig: typing.Type[PillarSelectorConfig]
    SubPillarConfigPolicy: typing.Type[SubPillarConfigPolicy]
