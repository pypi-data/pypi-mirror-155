import java.util
import java.util.function
import org.optaplanner.core.config.heuristic.selector.move
import org.optaplanner.core.impl.heuristic.selector.move.factory
import typing



class MoveIteratorFactoryConfig(org.optaplanner.core.config.heuristic.selector.move.MoveSelectorConfig['MoveIteratorFactoryConfig']):
    """
    public class MoveIteratorFactoryConfig extends :class:`~org.optaplanner.core.config.heuristic.selector.move.MoveSelectorConfig`<:class:`~org.optaplanner.core.config.heuristic.selector.move.factory.MoveIteratorFactoryConfig`>
    """
    XML_ELEMENT_NAME: typing.ClassVar[str] = ...
    """
    public static final :class:`~org.optaplanner.core.config.heuristic.selector.move.factory.https:.docs.oracle.com.javase.8.docs.api.java.lang.String?is` XML_ELEMENT_NAME
    
    
        Also see:
            :meth:`~constant`
    
    
    """
    def __init__(self): ...
    def copyConfig(self) -> 'MoveIteratorFactoryConfig':
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
    def getMoveIteratorFactoryClass(self) -> typing.Type[org.optaplanner.core.impl.heuristic.selector.move.factory.MoveIteratorFactory]: ...
    def getMoveIteratorFactoryCustomProperties(self) -> java.util.Map[str, str]: ...
    def inherit(self, moveIteratorFactoryConfig: 'MoveIteratorFactoryConfig') -> 'MoveIteratorFactoryConfig':
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
                inheritedConfig (:class:`~org.optaplanner.core.config.heuristic.selector.move.factory.MoveIteratorFactoryConfig`): never null
        
            Returns:
                this
        
        
        """
        ...
    def setMoveIteratorFactoryClass(self, class_: typing.Type[org.optaplanner.core.impl.heuristic.selector.move.factory.MoveIteratorFactory]) -> None: ...
    def setMoveIteratorFactoryCustomProperties(self, map: typing.Union[java.util.Map[str, str], typing.Mapping[str, str]]) -> None: ...
    def toString(self) -> str:
        """
        
            Overrides:
                :meth:`~org.optaplanner.core.config.AbstractConfig.toString` in
                class :class:`~org.optaplanner.core.config.AbstractConfig`
        
        
        """
        ...
    def visitReferencedClasses(self, consumer: typing.Union[java.util.function.Consumer[typing.Type[typing.Any]], typing.Callable[[typing.Type[typing.Any]], None]]) -> None: ...

class MoveListFactoryConfig(org.optaplanner.core.config.heuristic.selector.move.MoveSelectorConfig['MoveListFactoryConfig']):
    """
    public class MoveListFactoryConfig extends :class:`~org.optaplanner.core.config.heuristic.selector.move.MoveSelectorConfig`<:class:`~org.optaplanner.core.config.heuristic.selector.move.factory.MoveListFactoryConfig`>
    """
    XML_ELEMENT_NAME: typing.ClassVar[str] = ...
    """
    public static final :class:`~org.optaplanner.core.config.heuristic.selector.move.factory.https:.docs.oracle.com.javase.8.docs.api.java.lang.String?is` XML_ELEMENT_NAME
    
    
        Also see:
            :meth:`~constant`
    
    
    """
    def __init__(self): ...
    def copyConfig(self) -> 'MoveListFactoryConfig':
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
    def getMoveListFactoryClass(self) -> typing.Type[org.optaplanner.core.impl.heuristic.selector.move.factory.MoveListFactory]: ...
    def getMoveListFactoryCustomProperties(self) -> java.util.Map[str, str]: ...
    def inherit(self, moveListFactoryConfig: 'MoveListFactoryConfig') -> 'MoveListFactoryConfig':
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
                inheritedConfig (:class:`~org.optaplanner.core.config.heuristic.selector.move.factory.MoveListFactoryConfig`): never null
        
            Returns:
                this
        
        
        """
        ...
    def setMoveListFactoryClass(self, class_: typing.Type[org.optaplanner.core.impl.heuristic.selector.move.factory.MoveListFactory]) -> None: ...
    def setMoveListFactoryCustomProperties(self, map: typing.Union[java.util.Map[str, str], typing.Mapping[str, str]]) -> None: ...
    def toString(self) -> str:
        """
        
            Overrides:
                :meth:`~org.optaplanner.core.config.AbstractConfig.toString` in
                class :class:`~org.optaplanner.core.config.AbstractConfig`
        
        
        """
        ...
    def visitReferencedClasses(self, consumer: typing.Union[java.util.function.Consumer[typing.Type[typing.Any]], typing.Callable[[typing.Type[typing.Any]], None]]) -> None: ...


class __module_protocol__(typing.Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.optaplanner.core.config.heuristic.selector.move.factory")``.

    MoveIteratorFactoryConfig: typing.Type[MoveIteratorFactoryConfig]
    MoveListFactoryConfig: typing.Type[MoveListFactoryConfig]
