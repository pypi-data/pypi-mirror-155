import org.optaplanner.core.config
import org.optaplanner.core.config.heuristic.selector.common
import org.optaplanner.core.config.heuristic.selector.entity
import org.optaplanner.core.config.heuristic.selector.move
import org.optaplanner.core.config.heuristic.selector.value
import typing



_SelectorConfig__Config_ = typing.TypeVar('_SelectorConfig__Config_', bound='SelectorConfig')  # <Config_>
class SelectorConfig(org.optaplanner.core.config.AbstractConfig[_SelectorConfig__Config_], typing.Generic[_SelectorConfig__Config_]):
    """
    public abstract class SelectorConfig<Config_ extends SelectorConfig<Config_>> extends :class:`~org.optaplanner.core.config.AbstractConfig`<Config_>
    
        General superclass for :class:`~org.optaplanner.core.config.heuristic.selector.move.MoveSelectorConfig`,
        :class:`~org.optaplanner.core.config.heuristic.selector.entity.EntitySelectorConfig` and
        :class:`~org.optaplanner.core.config.heuristic.selector.value.ValueSelectorConfig`.
    """
    def __init__(self): ...


class __module_protocol__(typing.Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.optaplanner.core.config.heuristic.selector")``.

    SelectorConfig: typing.Type[SelectorConfig]
    common: org.optaplanner.core.config.heuristic.selector.common.__module_protocol__
    entity: org.optaplanner.core.config.heuristic.selector.entity.__module_protocol__
    move: org.optaplanner.core.config.heuristic.selector.move.__module_protocol__
    value: org.optaplanner.core.config.heuristic.selector.value.__module_protocol__
