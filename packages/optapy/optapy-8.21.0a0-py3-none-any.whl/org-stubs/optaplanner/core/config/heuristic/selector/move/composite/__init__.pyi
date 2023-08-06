import java.util
import java.util.function
import org.optaplanner.core.config.heuristic.selector.move
import org.optaplanner.core.impl.heuristic.selector.common.decorator
import typing



class CartesianProductMoveSelectorConfig(org.optaplanner.core.config.heuristic.selector.move.MoveSelectorConfig['CartesianProductMoveSelectorConfig']):
    """
    public class CartesianProductMoveSelectorConfig extends :class:`~org.optaplanner.core.config.heuristic.selector.move.MoveSelectorConfig`<:class:`~org.optaplanner.core.config.heuristic.selector.move.composite.CartesianProductMoveSelectorConfig`>
    """
    XML_ELEMENT_NAME: typing.ClassVar[str] = ...
    """
    public static final :class:`~org.optaplanner.core.config.heuristic.selector.move.composite.https:.docs.oracle.com.javase.8.docs.api.java.lang.String?is` XML_ELEMENT_NAME
    
    
        Also see:
            :meth:`~constant`
    
    
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, list: java.util.List[org.optaplanner.core.config.heuristic.selector.move.MoveSelectorConfig]): ...
    def copyConfig(self) -> 'CartesianProductMoveSelectorConfig':
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
    def extractLeafMoveSelectorConfigsIntoList(self, list: java.util.List[org.optaplanner.core.config.heuristic.selector.move.MoveSelectorConfig]) -> None: ...
    def getIgnoreEmptyChildIterators(self) -> bool: ...
    def getMoveSelectorConfigList(self) -> java.util.List[org.optaplanner.core.config.heuristic.selector.move.MoveSelectorConfig]: ...
    def getMoveSelectorList(self) -> java.util.List[org.optaplanner.core.config.heuristic.selector.move.MoveSelectorConfig]: ...
    def inherit(self, cartesianProductMoveSelectorConfig: 'CartesianProductMoveSelectorConfig') -> 'CartesianProductMoveSelectorConfig':
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
                inheritedConfig (:class:`~org.optaplanner.core.config.heuristic.selector.move.composite.CartesianProductMoveSelectorConfig`): never null
        
            Returns:
                this
        
        
        """
        ...
    def setIgnoreEmptyChildIterators(self, boolean: bool) -> None: ...
    def setMoveSelectorConfigList(self, list: java.util.List[org.optaplanner.core.config.heuristic.selector.move.MoveSelectorConfig]) -> None: ...
    def setMoveSelectorList(self, list: java.util.List[org.optaplanner.core.config.heuristic.selector.move.MoveSelectorConfig]) -> None: ...
    def toString(self) -> str:
        """
        
            Overrides:
                :meth:`~org.optaplanner.core.config.AbstractConfig.toString` in
                class :class:`~org.optaplanner.core.config.AbstractConfig`
        
        
        """
        ...
    def visitReferencedClasses(self, consumer: typing.Union[java.util.function.Consumer[typing.Type[typing.Any]], typing.Callable[[typing.Type[typing.Any]], None]]) -> None: ...
    def withIgnoreEmptyChildIterators(self, boolean: bool) -> 'CartesianProductMoveSelectorConfig': ...
    def withMoveSelectorList(self, list: java.util.List[org.optaplanner.core.config.heuristic.selector.move.MoveSelectorConfig]) -> 'CartesianProductMoveSelectorConfig': ...
    def withMoveSelectors(self, *moveSelectorConfig: org.optaplanner.core.config.heuristic.selector.move.MoveSelectorConfig) -> 'CartesianProductMoveSelectorConfig': ...

class UnionMoveSelectorConfig(org.optaplanner.core.config.heuristic.selector.move.MoveSelectorConfig['UnionMoveSelectorConfig']):
    """
    public class UnionMoveSelectorConfig extends :class:`~org.optaplanner.core.config.heuristic.selector.move.MoveSelectorConfig`<:class:`~org.optaplanner.core.config.heuristic.selector.move.composite.UnionMoveSelectorConfig`>
    """
    XML_ELEMENT_NAME: typing.ClassVar[str] = ...
    """
    public static final :class:`~org.optaplanner.core.config.heuristic.selector.move.composite.https:.docs.oracle.com.javase.8.docs.api.java.lang.String?is` XML_ELEMENT_NAME
    
    
        Also see:
            :meth:`~constant`
    
    
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, list: java.util.List[org.optaplanner.core.config.heuristic.selector.move.MoveSelectorConfig]): ...
    def copyConfig(self) -> 'UnionMoveSelectorConfig':
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
    def extractLeafMoveSelectorConfigsIntoList(self, list: java.util.List[org.optaplanner.core.config.heuristic.selector.move.MoveSelectorConfig]) -> None: ...
    def getMoveSelectorConfigList(self) -> java.util.List[org.optaplanner.core.config.heuristic.selector.move.MoveSelectorConfig]: ...
    def getMoveSelectorList(self) -> java.util.List[org.optaplanner.core.config.heuristic.selector.move.MoveSelectorConfig]: ...
    def getSelectorProbabilityWeightFactoryClass(self) -> typing.Type[org.optaplanner.core.impl.heuristic.selector.common.decorator.SelectionProbabilityWeightFactory]: ...
    def inherit(self, unionMoveSelectorConfig: 'UnionMoveSelectorConfig') -> 'UnionMoveSelectorConfig':
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
                inheritedConfig (:class:`~org.optaplanner.core.config.heuristic.selector.move.composite.UnionMoveSelectorConfig`): never null
        
            Returns:
                this
        
        
        """
        ...
    def setMoveSelectorConfigList(self, list: java.util.List[org.optaplanner.core.config.heuristic.selector.move.MoveSelectorConfig]) -> None: ...
    def setMoveSelectorList(self, list: java.util.List[org.optaplanner.core.config.heuristic.selector.move.MoveSelectorConfig]) -> None: ...
    def setSelectorProbabilityWeightFactoryClass(self, class_: typing.Type[org.optaplanner.core.impl.heuristic.selector.common.decorator.SelectionProbabilityWeightFactory]) -> None: ...
    def toString(self) -> str:
        """
        
            Overrides:
                :meth:`~org.optaplanner.core.config.AbstractConfig.toString` in
                class :class:`~org.optaplanner.core.config.AbstractConfig`
        
        
        """
        ...
    def visitReferencedClasses(self, consumer: typing.Union[java.util.function.Consumer[typing.Type[typing.Any]], typing.Callable[[typing.Type[typing.Any]], None]]) -> None: ...
    def withMoveSelectorList(self, list: java.util.List[org.optaplanner.core.config.heuristic.selector.move.MoveSelectorConfig]) -> 'UnionMoveSelectorConfig': ...
    def withMoveSelectors(self, *moveSelectorConfig: org.optaplanner.core.config.heuristic.selector.move.MoveSelectorConfig) -> 'UnionMoveSelectorConfig': ...
    def withSelectorProbabilityWeightFactoryClass(self, class_: typing.Type[org.optaplanner.core.impl.heuristic.selector.common.decorator.SelectionProbabilityWeightFactory]) -> 'UnionMoveSelectorConfig': ...


class __module_protocol__(typing.Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.optaplanner.core.config.heuristic.selector.move.composite")``.

    CartesianProductMoveSelectorConfig: typing.Type[CartesianProductMoveSelectorConfig]
    UnionMoveSelectorConfig: typing.Type[UnionMoveSelectorConfig]
