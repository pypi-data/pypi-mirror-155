import java.util
import java.util.function
import org.optaplanner.core.config
import org.optaplanner.core.config.heuristic.selector.entity
import org.optaplanner.core.config.heuristic.selector.move
import org.optaplanner.core.config.heuristic.selector.value
import typing



_EntityPlacerConfig__Config_ = typing.TypeVar('_EntityPlacerConfig__Config_', bound='EntityPlacerConfig')  # <Config_>
class EntityPlacerConfig(org.optaplanner.core.config.AbstractConfig[_EntityPlacerConfig__Config_], typing.Generic[_EntityPlacerConfig__Config_]):
    """
    public abstract class EntityPlacerConfig<Config_ extends EntityPlacerConfig<Config_>> extends :class:`~org.optaplanner.core.config.AbstractConfig`<Config_>
    
        General superclass for :class:`~org.optaplanner.core.config.constructionheuristic.placer.QueuedEntityPlacerConfig` and
        :class:`~org.optaplanner.core.config.constructionheuristic.placer.PooledEntityPlacerConfig`.
    """
    def __init__(self): ...

class PooledEntityPlacerConfig(EntityPlacerConfig['PooledEntityPlacerConfig']):
    """
    public class PooledEntityPlacerConfig extends :class:`~org.optaplanner.core.config.constructionheuristic.placer.EntityPlacerConfig`<:class:`~org.optaplanner.core.config.constructionheuristic.placer.PooledEntityPlacerConfig`>
    """
    def __init__(self): ...
    def copyConfig(self) -> 'PooledEntityPlacerConfig':
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
    def getMoveSelectorConfig(self) -> org.optaplanner.core.config.heuristic.selector.move.MoveSelectorConfig: ...
    def inherit(self, pooledEntityPlacerConfig: 'PooledEntityPlacerConfig') -> 'PooledEntityPlacerConfig':
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
                inheritedConfig (:class:`~org.optaplanner.core.config.constructionheuristic.placer.PooledEntityPlacerConfig`): never null
        
            Returns:
                this
        
        
        """
        ...
    def setMoveSelectorConfig(self, moveSelectorConfig: org.optaplanner.core.config.heuristic.selector.move.MoveSelectorConfig) -> None: ...
    def toString(self) -> str:
        """
        
            Overrides:
                :meth:`~org.optaplanner.core.config.AbstractConfig.toString` in
                class :class:`~org.optaplanner.core.config.AbstractConfig`
        
        
        """
        ...
    def visitReferencedClasses(self, consumer: typing.Union[java.util.function.Consumer[typing.Type[typing.Any]], typing.Callable[[typing.Type[typing.Any]], None]]) -> None: ...

class QueuedEntityPlacerConfig(EntityPlacerConfig['QueuedEntityPlacerConfig']):
    """
    public class QueuedEntityPlacerConfig extends :class:`~org.optaplanner.core.config.constructionheuristic.placer.EntityPlacerConfig`<:class:`~org.optaplanner.core.config.constructionheuristic.placer.QueuedEntityPlacerConfig`>
    """
    def __init__(self): ...
    def copyConfig(self) -> 'QueuedEntityPlacerConfig':
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
    def getMoveSelectorConfigList(self) -> java.util.List[org.optaplanner.core.config.heuristic.selector.move.MoveSelectorConfig]: ...
    def inherit(self, queuedEntityPlacerConfig: 'QueuedEntityPlacerConfig') -> 'QueuedEntityPlacerConfig':
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
                inheritedConfig (:class:`~org.optaplanner.core.config.constructionheuristic.placer.QueuedEntityPlacerConfig`): never null
        
            Returns:
                this
        
        
        """
        ...
    def setEntitySelectorConfig(self, entitySelectorConfig: org.optaplanner.core.config.heuristic.selector.entity.EntitySelectorConfig) -> None: ...
    def setMoveSelectorConfigList(self, list: java.util.List[org.optaplanner.core.config.heuristic.selector.move.MoveSelectorConfig]) -> None: ...
    def toString(self) -> str:
        """
        
            Overrides:
                :meth:`~org.optaplanner.core.config.AbstractConfig.toString` in
                class :class:`~org.optaplanner.core.config.AbstractConfig`
        
        
        """
        ...
    def visitReferencedClasses(self, consumer: typing.Union[java.util.function.Consumer[typing.Type[typing.Any]], typing.Callable[[typing.Type[typing.Any]], None]]) -> None: ...

class QueuedValuePlacerConfig(EntityPlacerConfig['QueuedValuePlacerConfig']):
    """
    public class QueuedValuePlacerConfig extends :class:`~org.optaplanner.core.config.constructionheuristic.placer.EntityPlacerConfig`<:class:`~org.optaplanner.core.config.constructionheuristic.placer.QueuedValuePlacerConfig`>
    """
    def __init__(self): ...
    def copyConfig(self) -> 'QueuedValuePlacerConfig':
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
    def getMoveSelectorConfig(self) -> org.optaplanner.core.config.heuristic.selector.move.MoveSelectorConfig: ...
    def getValueSelectorConfig(self) -> org.optaplanner.core.config.heuristic.selector.value.ValueSelectorConfig: ...
    def inherit(self, queuedValuePlacerConfig: 'QueuedValuePlacerConfig') -> 'QueuedValuePlacerConfig':
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
                inheritedConfig (:class:`~org.optaplanner.core.config.constructionheuristic.placer.QueuedValuePlacerConfig`): never null
        
            Returns:
                this
        
        
        """
        ...
    def setEntityClass(self, class_: typing.Type[typing.Any]) -> None: ...
    def setMoveSelectorConfig(self, moveSelectorConfig: org.optaplanner.core.config.heuristic.selector.move.MoveSelectorConfig) -> None: ...
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
    # A module protocol which reflects the result of ``jp.JPackage("org.optaplanner.core.config.constructionheuristic.placer")``.

    EntityPlacerConfig: typing.Type[EntityPlacerConfig]
    PooledEntityPlacerConfig: typing.Type[PooledEntityPlacerConfig]
    QueuedEntityPlacerConfig: typing.Type[QueuedEntityPlacerConfig]
    QueuedValuePlacerConfig: typing.Type[QueuedValuePlacerConfig]
