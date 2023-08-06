import java.lang
import java.util.function
import org.optaplanner.core.config.heuristic.selector.move
import org.optaplanner.core.config.localsearch.decider
import org.optaplanner.core.config.localsearch.decider.acceptor
import org.optaplanner.core.config.localsearch.decider.forager
import org.optaplanner.core.config.phase
import typing



class LocalSearchPhaseConfig(org.optaplanner.core.config.phase.PhaseConfig['LocalSearchPhaseConfig']):
    """
    public class LocalSearchPhaseConfig extends :class:`~org.optaplanner.core.config.phase.PhaseConfig`<:class:`~org.optaplanner.core.config.localsearch.LocalSearchPhaseConfig`>
    """
    XML_ELEMENT_NAME: typing.ClassVar[str] = ...
    """
    public static final :class:`~org.optaplanner.core.config.localsearch.https:.docs.oracle.com.javase.8.docs.api.java.lang.String?is` XML_ELEMENT_NAME
    
    
        Also see:
            :meth:`~constant`
    
    
    """
    def __init__(self): ...
    def copyConfig(self) -> 'LocalSearchPhaseConfig':
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
    def getAcceptorConfig(self) -> org.optaplanner.core.config.localsearch.decider.acceptor.LocalSearchAcceptorConfig: ...
    def getForagerConfig(self) -> org.optaplanner.core.config.localsearch.decider.forager.LocalSearchForagerConfig: ...
    def getLocalSearchType(self) -> 'LocalSearchType': ...
    def getMoveSelectorConfig(self) -> org.optaplanner.core.config.heuristic.selector.move.MoveSelectorConfig: ...
    def inherit(self, localSearchPhaseConfig: 'LocalSearchPhaseConfig') -> 'LocalSearchPhaseConfig':
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
                inheritedConfig (:class:`~org.optaplanner.core.config.localsearch.LocalSearchPhaseConfig`): never null
        
            Returns:
                this
        
        
        """
        ...
    def setAcceptorConfig(self, localSearchAcceptorConfig: org.optaplanner.core.config.localsearch.decider.acceptor.LocalSearchAcceptorConfig) -> None: ...
    def setForagerConfig(self, localSearchForagerConfig: org.optaplanner.core.config.localsearch.decider.forager.LocalSearchForagerConfig) -> None: ...
    def setLocalSearchType(self, localSearchType: 'LocalSearchType') -> None: ...
    def setMoveSelectorConfig(self, moveSelectorConfig: org.optaplanner.core.config.heuristic.selector.move.MoveSelectorConfig) -> None: ...
    def visitReferencedClasses(self, consumer: typing.Union[java.util.function.Consumer[typing.Type[typing.Any]], typing.Callable[[typing.Type[typing.Any]], None]]) -> None: ...
    def withAcceptorConfig(self, localSearchAcceptorConfig: org.optaplanner.core.config.localsearch.decider.acceptor.LocalSearchAcceptorConfig) -> 'LocalSearchPhaseConfig': ...
    def withForagerConfig(self, localSearchForagerConfig: org.optaplanner.core.config.localsearch.decider.forager.LocalSearchForagerConfig) -> 'LocalSearchPhaseConfig': ...
    def withLocalSearchType(self, localSearchType: 'LocalSearchType') -> 'LocalSearchPhaseConfig': ...
    def withMoveSelectorConfig(self, moveSelectorConfig: org.optaplanner.core.config.heuristic.selector.move.MoveSelectorConfig) -> 'LocalSearchPhaseConfig': ...

class LocalSearchType(java.lang.Enum['LocalSearchType']):
    """
    public enum LocalSearchType extends :class:`~org.optaplanner.core.config.localsearch.https:.docs.oracle.com.javase.8.docs.api.java.lang.Enum?is`<:class:`~org.optaplanner.core.config.localsearch.LocalSearchType`>
    """
    HILL_CLIMBING: typing.ClassVar['LocalSearchType'] = ...
    TABU_SEARCH: typing.ClassVar['LocalSearchType'] = ...
    SIMULATED_ANNEALING: typing.ClassVar['LocalSearchType'] = ...
    LATE_ACCEPTANCE: typing.ClassVar['LocalSearchType'] = ...
    GREAT_DELUGE: typing.ClassVar['LocalSearchType'] = ...
    VARIABLE_NEIGHBORHOOD_DESCENT: typing.ClassVar['LocalSearchType'] = ...
    @staticmethod
    def getBluePrintTypes() -> typing.List['LocalSearchType']:
        """
        
            Returns:
                :meth:`~org.optaplanner.core.config.localsearch.LocalSearchType.values` without duplicates (abstract types that end up
                behaving as one of the other types).
        
        
        """
        ...
    _valueOf_0__T = typing.TypeVar('_valueOf_0__T', bound=java.lang.Enum)  # <T>
    @typing.overload
    @staticmethod
    def valueOf(class_: typing.Type[_valueOf_0__T], string: str) -> _valueOf_0__T: ...
    @typing.overload
    @staticmethod
    def valueOf(string: str) -> 'LocalSearchType':
        """
            Returns the enum constant of this type with the specified name. The string must match *exactly* an identifier used to
            declare an enum constant in this type. (Extraneous whitespace characters are not permitted.)
        
            Parameters:
                name (:class:`~org.optaplanner.core.config.localsearch.https:.docs.oracle.com.javase.8.docs.api.java.lang.String?is`): the name of the enum constant to be returned.
        
            Returns:
                the enum constant with the specified name
        
            Raises:
                :class:`~org.optaplanner.core.config.localsearch.https:.docs.oracle.com.javase.8.docs.api.java.lang.IllegalArgumentException?is`: if this enum type has no constant with the specified name
                :class:`~org.optaplanner.core.config.localsearch.https:.docs.oracle.com.javase.8.docs.api.java.lang.NullPointerException?is`: if the argument is null
        
        
        """
        ...
    @staticmethod
    def values() -> typing.List['LocalSearchType']:
        """
            Returns an array containing the constants of this enum type, in the order they are declared. This method may be used to
            iterate over the constants as follows:
        
            .. code-block: java
            
            for (LocalSearchType c : LocalSearchType.values())
                System.out.println(c);
            
        
            Returns:
                an array containing the constants of this enum type, in the order they are declared
        
        
        """
        ...


class __module_protocol__(typing.Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.optaplanner.core.config.localsearch")``.

    LocalSearchPhaseConfig: typing.Type[LocalSearchPhaseConfig]
    LocalSearchType: typing.Type[LocalSearchType]
    decider: org.optaplanner.core.config.localsearch.decider.__module_protocol__
