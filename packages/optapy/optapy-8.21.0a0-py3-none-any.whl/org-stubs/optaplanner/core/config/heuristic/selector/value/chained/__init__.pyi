import java.util.function
import org.optaplanner.core.config.heuristic.selector
import org.optaplanner.core.config.heuristic.selector.value
import typing



class SubChainSelectorConfig(org.optaplanner.core.config.heuristic.selector.SelectorConfig['SubChainSelectorConfig']):
    """
    public class SubChainSelectorConfig extends :class:`~org.optaplanner.core.config.heuristic.selector.SelectorConfig`<:class:`~org.optaplanner.core.config.heuristic.selector.value.chained.SubChainSelectorConfig`>
    """
    def __init__(self): ...
    def copyConfig(self) -> 'SubChainSelectorConfig':
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
    def getMaximumSubChainSize(self) -> int: ...
    def getMinimumSubChainSize(self) -> int:
        """
        
            Returns:
                sometimes null
        
        
        """
        ...
    def getValueSelectorConfig(self) -> org.optaplanner.core.config.heuristic.selector.value.ValueSelectorConfig: ...
    def inherit(self, subChainSelectorConfig: 'SubChainSelectorConfig') -> 'SubChainSelectorConfig':
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
                inheritedConfig (:class:`~org.optaplanner.core.config.heuristic.selector.value.chained.SubChainSelectorConfig`): never null
        
            Returns:
                this
        
        
        """
        ...
    def setMaximumSubChainSize(self, integer: int) -> None: ...
    def setMinimumSubChainSize(self, integer: int) -> None: ...
    def setValueSelectorConfig(self, valueSelectorConfig: org.optaplanner.core.config.heuristic.selector.value.ValueSelectorConfig) -> None: ...
    def toString(self) -> str:
        """
        
            Overrides:
                :meth:`~org.optaplanner.core.config.AbstractConfig.toString` in
                class :class:`~org.optaplanner.core.config.AbstractConfig`
        
        
        """
        ...
    def visitReferencedClasses(self, consumer: typing.Union[java.util.function.Consumer[typing.Type[typing.Any]], typing.Callable[[typing.Type[typing.Any]], None]]) -> None: ...


class __module_protocol__(typing.Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.optaplanner.core.config.heuristic.selector.value.chained")``.

    SubChainSelectorConfig: typing.Type[SubChainSelectorConfig]
