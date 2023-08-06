import java.util.function
import org.optaplanner.core.config.heuristic.selector.entity
import org.optaplanner.core.config.heuristic.selector.move
import org.optaplanner.core.config.heuristic.selector.value
import org.optaplanner.core.config.heuristic.selector.value.chained
import typing



class KOptMoveSelectorConfig(org.optaplanner.core.config.heuristic.selector.move.MoveSelectorConfig['KOptMoveSelectorConfig']):
    """
    public class KOptMoveSelectorConfig extends :class:`~org.optaplanner.core.config.heuristic.selector.move.MoveSelectorConfig`<:class:`~org.optaplanner.core.config.heuristic.selector.move.generic.chained.KOptMoveSelectorConfig`>
    
        THIS CLASS IS EXPERIMENTAL AND UNSUPPORTED. Backward compatibility is not guaranteed. It's NOT DOCUMENTED because we'll
        only document it when it actually works in more than 1 use case. Do not use.
    
        Also see:
            :class:`~org.optaplanner.core.config.heuristic.selector.move.generic.chained.TailChainSwapMoveSelectorConfig`
    """
    XML_ELEMENT_NAME: typing.ClassVar[str] = ...
    """
    public static final :class:`~org.optaplanner.core.config.heuristic.selector.move.generic.chained.https:.docs.oracle.com.javase.8.docs.api.java.lang.String?is` XML_ELEMENT_NAME
    
    
        Also see:
            :meth:`~constant`
    
    
    """
    def __init__(self): ...
    def copyConfig(self) -> 'KOptMoveSelectorConfig':
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
    def getValueSelectorConfig(self) -> org.optaplanner.core.config.heuristic.selector.value.ValueSelectorConfig: ...
    def inherit(self, kOptMoveSelectorConfig: 'KOptMoveSelectorConfig') -> 'KOptMoveSelectorConfig':
        """
            Description copied from class: :meth:`~org.optaplanner.core.config.AbstractConfig.inherit`
            Inherits each property of the :code:`inheritedConfig` unless that property (or a semantic alternative) is defined by
            this instance (which overwrites the inherited behaviour).
        
            After the inheritance, if a property on this :class:`~org.optaplanner.core.config.AbstractConfig` composition is
            replaced, it should not affect the inherited composition instance.
        
            Overrides:
                :meth:`~org.optaplanner.core.config.heuristic.selector.move.MoveSelectorConfig.inherit` in
                class :class:`~org.optaplanner.core.config.heuristic.selector.move.MoveSelectorConfig`
        
            Parameters:
                inheritedConfig (:class:`~org.optaplanner.core.config.heuristic.selector.move.generic.chained.KOptMoveSelectorConfig`): never null
        
            Returns:
                this
        
        
        """
        ...
    def setEntitySelectorConfig(self, entitySelectorConfig: org.optaplanner.core.config.heuristic.selector.entity.EntitySelectorConfig) -> None: ...
    def setValueSelectorConfig(self, valueSelectorConfig: org.optaplanner.core.config.heuristic.selector.value.ValueSelectorConfig) -> None: ...
    def toString(self) -> str:
        """
        
            Overrides:
                :meth:`~org.optaplanner.core.config.AbstractConfig.toString` in
                class :class:`~org.optaplanner.core.config.AbstractConfig`
        
        
        """
        ...
    def visitReferencedClasses(self, consumer: typing.Union[java.util.function.Consumer[typing.Type[typing.Any]], typing.Callable[[typing.Type[typing.Any]], None]]) -> None: ...

class SubChainChangeMoveSelectorConfig(org.optaplanner.core.config.heuristic.selector.move.MoveSelectorConfig['SubChainChangeMoveSelectorConfig']):
    """
    public class SubChainChangeMoveSelectorConfig extends :class:`~org.optaplanner.core.config.heuristic.selector.move.MoveSelectorConfig`<:class:`~org.optaplanner.core.config.heuristic.selector.move.generic.chained.SubChainChangeMoveSelectorConfig`>
    """
    XML_ELEMENT_NAME: typing.ClassVar[str] = ...
    """
    public static final :class:`~org.optaplanner.core.config.heuristic.selector.move.generic.chained.https:.docs.oracle.com.javase.8.docs.api.java.lang.String?is` XML_ELEMENT_NAME
    
    
        Also see:
            :meth:`~constant`
    
    
    """
    def __init__(self): ...
    def copyConfig(self) -> 'SubChainChangeMoveSelectorConfig':
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
    def getEntityClass(self) -> typing.Type[typing.Any]: ...
    def getSelectReversingMoveToo(self) -> bool: ...
    def getSubChainSelectorConfig(self) -> org.optaplanner.core.config.heuristic.selector.value.chained.SubChainSelectorConfig: ...
    def getValueSelectorConfig(self) -> org.optaplanner.core.config.heuristic.selector.value.ValueSelectorConfig: ...
    def inherit(self, subChainChangeMoveSelectorConfig: 'SubChainChangeMoveSelectorConfig') -> 'SubChainChangeMoveSelectorConfig':
        """
            Description copied from class: :meth:`~org.optaplanner.core.config.AbstractConfig.inherit`
            Inherits each property of the :code:`inheritedConfig` unless that property (or a semantic alternative) is defined by
            this instance (which overwrites the inherited behaviour).
        
            After the inheritance, if a property on this :class:`~org.optaplanner.core.config.AbstractConfig` composition is
            replaced, it should not affect the inherited composition instance.
        
            Overrides:
                :meth:`~org.optaplanner.core.config.heuristic.selector.move.MoveSelectorConfig.inherit` in
                class :class:`~org.optaplanner.core.config.heuristic.selector.move.MoveSelectorConfig`
        
            Parameters:
                inheritedConfig (:class:`~org.optaplanner.core.config.heuristic.selector.move.generic.chained.SubChainChangeMoveSelectorConfig`): never null
        
            Returns:
                this
        
        
        """
        ...
    def setEntityClass(self, class_: typing.Type[typing.Any]) -> None: ...
    def setSelectReversingMoveToo(self, boolean: bool) -> None: ...
    def setSubChainSelectorConfig(self, subChainSelectorConfig: org.optaplanner.core.config.heuristic.selector.value.chained.SubChainSelectorConfig) -> None: ...
    def setValueSelectorConfig(self, valueSelectorConfig: org.optaplanner.core.config.heuristic.selector.value.ValueSelectorConfig) -> None: ...
    def toString(self) -> str:
        """
        
            Overrides:
                :meth:`~org.optaplanner.core.config.AbstractConfig.toString` in
                class :class:`~org.optaplanner.core.config.AbstractConfig`
        
        
        """
        ...
    def visitReferencedClasses(self, consumer: typing.Union[java.util.function.Consumer[typing.Type[typing.Any]], typing.Callable[[typing.Type[typing.Any]], None]]) -> None: ...

class SubChainSwapMoveSelectorConfig(org.optaplanner.core.config.heuristic.selector.move.MoveSelectorConfig['SubChainSwapMoveSelectorConfig']):
    """
    public class SubChainSwapMoveSelectorConfig extends :class:`~org.optaplanner.core.config.heuristic.selector.move.MoveSelectorConfig`<:class:`~org.optaplanner.core.config.heuristic.selector.move.generic.chained.SubChainSwapMoveSelectorConfig`>
    """
    XML_ELEMENT_NAME: typing.ClassVar[str] = ...
    """
    public static final :class:`~org.optaplanner.core.config.heuristic.selector.move.generic.chained.https:.docs.oracle.com.javase.8.docs.api.java.lang.String?is` XML_ELEMENT_NAME
    
    
        Also see:
            :meth:`~constant`
    
    
    """
    def __init__(self): ...
    def copyConfig(self) -> 'SubChainSwapMoveSelectorConfig':
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
    def getEntityClass(self) -> typing.Type[typing.Any]: ...
    def getSecondarySubChainSelectorConfig(self) -> org.optaplanner.core.config.heuristic.selector.value.chained.SubChainSelectorConfig: ...
    def getSelectReversingMoveToo(self) -> bool: ...
    def getSubChainSelectorConfig(self) -> org.optaplanner.core.config.heuristic.selector.value.chained.SubChainSelectorConfig: ...
    def inherit(self, subChainSwapMoveSelectorConfig: 'SubChainSwapMoveSelectorConfig') -> 'SubChainSwapMoveSelectorConfig':
        """
            Description copied from class: :meth:`~org.optaplanner.core.config.AbstractConfig.inherit`
            Inherits each property of the :code:`inheritedConfig` unless that property (or a semantic alternative) is defined by
            this instance (which overwrites the inherited behaviour).
        
            After the inheritance, if a property on this :class:`~org.optaplanner.core.config.AbstractConfig` composition is
            replaced, it should not affect the inherited composition instance.
        
            Overrides:
                :meth:`~org.optaplanner.core.config.heuristic.selector.move.MoveSelectorConfig.inherit` in
                class :class:`~org.optaplanner.core.config.heuristic.selector.move.MoveSelectorConfig`
        
            Parameters:
                inheritedConfig (:class:`~org.optaplanner.core.config.heuristic.selector.move.generic.chained.SubChainSwapMoveSelectorConfig`): never null
        
            Returns:
                this
        
        
        """
        ...
    def setEntityClass(self, class_: typing.Type[typing.Any]) -> None: ...
    def setSecondarySubChainSelectorConfig(self, subChainSelectorConfig: org.optaplanner.core.config.heuristic.selector.value.chained.SubChainSelectorConfig) -> None: ...
    def setSelectReversingMoveToo(self, boolean: bool) -> None: ...
    def setSubChainSelectorConfig(self, subChainSelectorConfig: org.optaplanner.core.config.heuristic.selector.value.chained.SubChainSelectorConfig) -> None: ...
    def toString(self) -> str:
        """
        
            Overrides:
                :meth:`~org.optaplanner.core.config.AbstractConfig.toString` in
                class :class:`~org.optaplanner.core.config.AbstractConfig`
        
        
        """
        ...
    def visitReferencedClasses(self, consumer: typing.Union[java.util.function.Consumer[typing.Type[typing.Any]], typing.Callable[[typing.Type[typing.Any]], None]]) -> None: ...

class TailChainSwapMoveSelectorConfig(org.optaplanner.core.config.heuristic.selector.move.MoveSelectorConfig['TailChainSwapMoveSelectorConfig']):
    """
    public class TailChainSwapMoveSelectorConfig extends :class:`~org.optaplanner.core.config.heuristic.selector.move.MoveSelectorConfig`<:class:`~org.optaplanner.core.config.heuristic.selector.move.generic.chained.TailChainSwapMoveSelectorConfig`>
    
        Also known as a 2-opt move selector config.
    """
    XML_ELEMENT_NAME: typing.ClassVar[str] = ...
    """
    public static final :class:`~org.optaplanner.core.config.heuristic.selector.move.generic.chained.https:.docs.oracle.com.javase.8.docs.api.java.lang.String?is` XML_ELEMENT_NAME
    
    
        Also see:
            :meth:`~constant`
    
    
    """
    def __init__(self): ...
    def copyConfig(self) -> 'TailChainSwapMoveSelectorConfig':
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
    def getValueSelectorConfig(self) -> org.optaplanner.core.config.heuristic.selector.value.ValueSelectorConfig: ...
    def inherit(self, tailChainSwapMoveSelectorConfig: 'TailChainSwapMoveSelectorConfig') -> 'TailChainSwapMoveSelectorConfig':
        """
            Description copied from class: :meth:`~org.optaplanner.core.config.AbstractConfig.inherit`
            Inherits each property of the :code:`inheritedConfig` unless that property (or a semantic alternative) is defined by
            this instance (which overwrites the inherited behaviour).
        
            After the inheritance, if a property on this :class:`~org.optaplanner.core.config.AbstractConfig` composition is
            replaced, it should not affect the inherited composition instance.
        
            Overrides:
                :meth:`~org.optaplanner.core.config.heuristic.selector.move.MoveSelectorConfig.inherit` in
                class :class:`~org.optaplanner.core.config.heuristic.selector.move.MoveSelectorConfig`
        
            Parameters:
                inheritedConfig (:class:`~org.optaplanner.core.config.heuristic.selector.move.generic.chained.TailChainSwapMoveSelectorConfig`): never null
        
            Returns:
                this
        
        
        """
        ...
    def setEntitySelectorConfig(self, entitySelectorConfig: org.optaplanner.core.config.heuristic.selector.entity.EntitySelectorConfig) -> None: ...
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
    # A module protocol which reflects the result of ``jp.JPackage("org.optaplanner.core.config.heuristic.selector.move.generic.chained")``.

    KOptMoveSelectorConfig: typing.Type[KOptMoveSelectorConfig]
    SubChainChangeMoveSelectorConfig: typing.Type[SubChainChangeMoveSelectorConfig]
    SubChainSwapMoveSelectorConfig: typing.Type[SubChainSwapMoveSelectorConfig]
    TailChainSwapMoveSelectorConfig: typing.Type[TailChainSwapMoveSelectorConfig]
