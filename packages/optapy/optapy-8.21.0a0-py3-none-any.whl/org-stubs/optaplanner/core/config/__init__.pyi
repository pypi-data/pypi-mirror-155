import java.util.function
import org.optaplanner.core.config.constructionheuristic
import org.optaplanner.core.config.exhaustivesearch
import org.optaplanner.core.config.heuristic
import org.optaplanner.core.config.localsearch
import org.optaplanner.core.config.partitionedsearch
import org.optaplanner.core.config.phase
import org.optaplanner.core.config.score
import org.optaplanner.core.config.solver
import org.optaplanner.core.config.util
import typing



_AbstractConfig__Config_ = typing.TypeVar('_AbstractConfig__Config_', bound='AbstractConfig')  # <Config_>
class AbstractConfig(typing.Generic[_AbstractConfig__Config_]):
    """
    public abstract class AbstractConfig<Config_ extends AbstractConfig<Config_>> extends :class:`~org.optaplanner.core.config.https:.docs.oracle.com.javase.8.docs.api.java.lang.Object?is`
    
        A config class is a user friendly, validating configuration class that maps XML input. It builds the runtime impl
        classes (which are optimized for scalability and performance instead).
    
        A config class should adhere to "configuration by exception" in its XML/JSON input/output, so all non-static fields
        should be null by default. Using the config class to build a runtime class, must not alter the config class's XML/JSON
        output.
    """
    def __init__(self): ...
    def copyConfig(self) -> _AbstractConfig__Config_:
        """
            Typically implemented by constructing a new instance and calling
            :meth:`~org.optaplanner.core.config.AbstractConfig.inherit` on it
        
            Returns:
                new instance
        
        
        """
        ...
    def inherit(self, config_: _AbstractConfig__Config_) -> _AbstractConfig__Config_:
        """
            Inherits each property of the :code:`inheritedConfig` unless that property (or a semantic alternative) is defined by
            this instance (which overwrites the inherited behaviour).
        
            After the inheritance, if a property on this :class:`~org.optaplanner.core.config.AbstractConfig` composition is
            replaced, it should not affect the inherited composition instance.
        
            Parameters:
                inheritedConfig (:class:`~org.optaplanner.core.config.AbstractConfig`): never null
        
            Returns:
                this
        
        
        """
        ...
    def toString(self) -> str:
        """
        
            Overrides:
                :meth:`~org.optaplanner.core.config.https:.docs.oracle.com.javase.8.docs.api.java.lang.Object.html?is` in
                class :class:`~org.optaplanner.core.config.https:.docs.oracle.com.javase.8.docs.api.java.lang.Object?is`
        
        
        """
        ...
    def visitReferencedClasses(self, consumer: typing.Union[java.util.function.Consumer[typing.Type[typing.Any]], typing.Callable[[typing.Type[typing.Any]], None]]) -> None: ...


class __module_protocol__(typing.Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.optaplanner.core.config")``.

    AbstractConfig: typing.Type[AbstractConfig]
    constructionheuristic: org.optaplanner.core.config.constructionheuristic.__module_protocol__
    exhaustivesearch: org.optaplanner.core.config.exhaustivesearch.__module_protocol__
    heuristic: org.optaplanner.core.config.heuristic.__module_protocol__
    localsearch: org.optaplanner.core.config.localsearch.__module_protocol__
    partitionedsearch: org.optaplanner.core.config.partitionedsearch.__module_protocol__
    phase: org.optaplanner.core.config.phase.__module_protocol__
    score: org.optaplanner.core.config.score.__module_protocol__
    solver: org.optaplanner.core.config.solver.__module_protocol__
    util: org.optaplanner.core.config.util.__module_protocol__
