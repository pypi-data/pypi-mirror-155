import java.util.function
import org.optaplanner.core.config
import org.optaplanner.core.config.phase.custom
import org.optaplanner.core.config.solver.termination
import typing



_PhaseConfig__Config_ = typing.TypeVar('_PhaseConfig__Config_', bound='PhaseConfig')  # <Config_>
class PhaseConfig(org.optaplanner.core.config.AbstractConfig[_PhaseConfig__Config_], typing.Generic[_PhaseConfig__Config_]):
    """
    public abstract class PhaseConfig<Config_ extends PhaseConfig<Config_>> extends :class:`~org.optaplanner.core.config.AbstractConfig`<Config_>
    """
    def __init__(self): ...
    def getTerminationConfig(self) -> org.optaplanner.core.config.solver.termination.TerminationConfig: ...
    def inherit(self, config_: _PhaseConfig__Config_) -> _PhaseConfig__Config_:
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
                inheritedConfig (:class:`~org.optaplanner.core.config.phase.PhaseConfig`): never null
        
            Returns:
                this
        
        
        """
        ...
    def setTerminationConfig(self, terminationConfig: org.optaplanner.core.config.solver.termination.TerminationConfig) -> None: ...
    def toString(self) -> str:
        """
        
            Overrides:
                :meth:`~org.optaplanner.core.config.AbstractConfig.toString` in
                class :class:`~org.optaplanner.core.config.AbstractConfig`
        
        
        """
        ...

class NoChangePhaseConfig(PhaseConfig['NoChangePhaseConfig']):
    """
    public class NoChangePhaseConfig extends :class:`~org.optaplanner.core.config.phase.PhaseConfig`<:class:`~org.optaplanner.core.config.phase.NoChangePhaseConfig`>
    """
    XML_ELEMENT_NAME: typing.ClassVar[str] = ...
    """
    public static final :class:`~org.optaplanner.core.config.phase.https:.docs.oracle.com.javase.8.docs.api.java.lang.String?is` XML_ELEMENT_NAME
    
    
        Also see:
            :meth:`~constant`
    
    
    """
    def __init__(self): ...
    def copyConfig(self) -> 'NoChangePhaseConfig':
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
    def inherit(self, noChangePhaseConfig: 'NoChangePhaseConfig') -> 'NoChangePhaseConfig':
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
                inheritedConfig (:class:`~org.optaplanner.core.config.phase.NoChangePhaseConfig`): never null
        
            Returns:
                this
        
        
        """
        ...
    def visitReferencedClasses(self, consumer: typing.Union[java.util.function.Consumer[typing.Type[typing.Any]], typing.Callable[[typing.Type[typing.Any]], None]]) -> None: ...


class __module_protocol__(typing.Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.optaplanner.core.config.phase")``.

    NoChangePhaseConfig: typing.Type[NoChangePhaseConfig]
    PhaseConfig: typing.Type[PhaseConfig]
    custom: org.optaplanner.core.config.phase.custom.__module_protocol__
