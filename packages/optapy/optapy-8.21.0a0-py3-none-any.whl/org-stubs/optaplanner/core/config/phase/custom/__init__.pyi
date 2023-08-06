import java.util
import java.util.function
import org.optaplanner.core.api.score.director
import org.optaplanner.core.config.phase
import org.optaplanner.core.impl.phase.custom
import typing



class CustomPhaseConfig(org.optaplanner.core.config.phase.PhaseConfig['CustomPhaseConfig']):
    """
    public class CustomPhaseConfig extends :class:`~org.optaplanner.core.config.phase.PhaseConfig`<:class:`~org.optaplanner.core.config.phase.custom.CustomPhaseConfig`>
    """
    XML_ELEMENT_NAME: typing.ClassVar[str] = ...
    """
    public static final :class:`~org.optaplanner.core.config.phase.custom.https:.docs.oracle.com.javase.8.docs.api.java.lang.String?is` XML_ELEMENT_NAME
    
    
        Also see:
            :meth:`~constant`
    
    
    """
    def __init__(self): ...
    def copyConfig(self) -> 'CustomPhaseConfig':
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
    def getCustomPhaseCommandClassList(self) -> java.util.List[typing.Type[org.optaplanner.core.impl.phase.custom.CustomPhaseCommand]]: ...
    def getCustomPhaseCommandList(self) -> java.util.List[org.optaplanner.core.impl.phase.custom.CustomPhaseCommand]: ...
    def getCustomProperties(self) -> java.util.Map[str, str]: ...
    def inherit(self, customPhaseConfig: 'CustomPhaseConfig') -> 'CustomPhaseConfig':
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
                inheritedConfig (:class:`~org.optaplanner.core.config.phase.custom.CustomPhaseConfig`): never null
        
            Returns:
                this
        
        
        """
        ...
    def setCustomPhaseCommandClassList(self, list: java.util.List[typing.Type[org.optaplanner.core.impl.phase.custom.CustomPhaseCommand]]) -> None: ...
    def setCustomPhaseCommandList(self, list: java.util.List[typing.Union[org.optaplanner.core.impl.phase.custom.CustomPhaseCommand, typing.Callable]]) -> None: ...
    def setCustomProperties(self, map: typing.Union[java.util.Map[str, str], typing.Mapping[str, str]]) -> None: ...
    def visitReferencedClasses(self, consumer: typing.Union[java.util.function.Consumer[typing.Type[typing.Any]], typing.Callable[[typing.Type[typing.Any]], None]]) -> None: ...
    def withCustomPhaseCommandClassList(self, list: java.util.List[typing.Type[org.optaplanner.core.impl.phase.custom.CustomPhaseCommand]]) -> 'CustomPhaseConfig': ...
    def withCustomPhaseCommandList(self, list: java.util.List[typing.Union[org.optaplanner.core.impl.phase.custom.CustomPhaseCommand, typing.Callable]]) -> 'CustomPhaseConfig': ...
    _withCustomPhaseCommands__Solution_ = typing.TypeVar('_withCustomPhaseCommands__Solution_')  # <Solution_>
    def withCustomPhaseCommands(self, *customPhaseCommand: typing.Union[org.optaplanner.core.impl.phase.custom.CustomPhaseCommand[_withCustomPhaseCommands__Solution_], typing.Callable[[org.optaplanner.core.api.score.director.ScoreDirector[typing.Any]], None]]) -> 'CustomPhaseConfig': ...
    def withCustomProperties(self, map: typing.Union[java.util.Map[str, str], typing.Mapping[str, str]]) -> None: ...


class __module_protocol__(typing.Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.optaplanner.core.config.phase.custom")``.

    CustomPhaseConfig: typing.Type[CustomPhaseConfig]
