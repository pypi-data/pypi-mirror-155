import java.lang
import java.util
import java.util.function
import org.optaplanner.core.config.heuristic.selector.entity
import org.optaplanner.core.config.heuristic.selector.move
import org.optaplanner.core.config.heuristic.selector.value
import org.optaplanner.core.config.phase
import org.optaplanner.core.impl.exhaustivesearch.node
import typing



class ExhaustiveSearchPhaseConfig(org.optaplanner.core.config.phase.PhaseConfig['ExhaustiveSearchPhaseConfig']):
    """
    public class ExhaustiveSearchPhaseConfig extends :class:`~org.optaplanner.core.config.phase.PhaseConfig`<:class:`~org.optaplanner.core.config.exhaustivesearch.ExhaustiveSearchPhaseConfig`>
    """
    XML_ELEMENT_NAME: typing.ClassVar[str] = ...
    """
    public static final :class:`~org.optaplanner.core.config.exhaustivesearch.https:.docs.oracle.com.javase.8.docs.api.java.lang.String?is` XML_ELEMENT_NAME
    
    
        Also see:
            :meth:`~constant`
    
    
    """
    def __init__(self): ...
    def copyConfig(self) -> 'ExhaustiveSearchPhaseConfig':
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
    def getEntitySorterManner(self) -> org.optaplanner.core.config.heuristic.selector.entity.EntitySorterManner: ...
    def getExhaustiveSearchType(self) -> 'ExhaustiveSearchType': ...
    def getMoveSelectorConfig(self) -> org.optaplanner.core.config.heuristic.selector.move.MoveSelectorConfig: ...
    def getNodeExplorationType(self) -> 'NodeExplorationType': ...
    def getValueSorterManner(self) -> org.optaplanner.core.config.heuristic.selector.value.ValueSorterManner: ...
    def inherit(self, exhaustiveSearchPhaseConfig: 'ExhaustiveSearchPhaseConfig') -> 'ExhaustiveSearchPhaseConfig':
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
                inheritedConfig (:class:`~org.optaplanner.core.config.exhaustivesearch.ExhaustiveSearchPhaseConfig`): never null
        
            Returns:
                this
        
        
        """
        ...
    def setEntitySelectorConfig(self, entitySelectorConfig: org.optaplanner.core.config.heuristic.selector.entity.EntitySelectorConfig) -> None: ...
    def setEntitySorterManner(self, entitySorterManner: org.optaplanner.core.config.heuristic.selector.entity.EntitySorterManner) -> None: ...
    def setExhaustiveSearchType(self, exhaustiveSearchType: 'ExhaustiveSearchType') -> None: ...
    def setMoveSelectorConfig(self, moveSelectorConfig: org.optaplanner.core.config.heuristic.selector.move.MoveSelectorConfig) -> None: ...
    def setNodeExplorationType(self, nodeExplorationType: 'NodeExplorationType') -> None: ...
    def setValueSorterManner(self, valueSorterManner: org.optaplanner.core.config.heuristic.selector.value.ValueSorterManner) -> None: ...
    def visitReferencedClasses(self, consumer: typing.Union[java.util.function.Consumer[typing.Type[typing.Any]], typing.Callable[[typing.Type[typing.Any]], None]]) -> None: ...

class ExhaustiveSearchType(java.lang.Enum['ExhaustiveSearchType']):
    """
    public enum ExhaustiveSearchType extends :class:`~org.optaplanner.core.config.exhaustivesearch.https:.docs.oracle.com.javase.8.docs.api.java.lang.Enum?is`<:class:`~org.optaplanner.core.config.exhaustivesearch.ExhaustiveSearchType`>
    """
    BRUTE_FORCE: typing.ClassVar['ExhaustiveSearchType'] = ...
    BRANCH_AND_BOUND: typing.ClassVar['ExhaustiveSearchType'] = ...
    def getDefaultEntitySorterManner(self) -> org.optaplanner.core.config.heuristic.selector.entity.EntitySorterManner: ...
    def getDefaultValueSorterManner(self) -> org.optaplanner.core.config.heuristic.selector.value.ValueSorterManner: ...
    def isScoreBounderEnabled(self) -> bool: ...
    _valueOf_0__T = typing.TypeVar('_valueOf_0__T', bound=java.lang.Enum)  # <T>
    @typing.overload
    @staticmethod
    def valueOf(class_: typing.Type[_valueOf_0__T], string: str) -> _valueOf_0__T: ...
    @typing.overload
    @staticmethod
    def valueOf(string: str) -> 'ExhaustiveSearchType':
        """
            Returns the enum constant of this type with the specified name. The string must match *exactly* an identifier used to
            declare an enum constant in this type. (Extraneous whitespace characters are not permitted.)
        
            Parameters:
                name (:class:`~org.optaplanner.core.config.exhaustivesearch.https:.docs.oracle.com.javase.8.docs.api.java.lang.String?is`): the name of the enum constant to be returned.
        
            Returns:
                the enum constant with the specified name
        
            Raises:
                :class:`~org.optaplanner.core.config.exhaustivesearch.https:.docs.oracle.com.javase.8.docs.api.java.lang.IllegalArgumentException?is`: if this enum type has no constant with the specified name
                :class:`~org.optaplanner.core.config.exhaustivesearch.https:.docs.oracle.com.javase.8.docs.api.java.lang.NullPointerException?is`: if the argument is null
        
        
        """
        ...
    @staticmethod
    def values() -> typing.List['ExhaustiveSearchType']:
        """
            Returns an array containing the constants of this enum type, in the order they are declared. This method may be used to
            iterate over the constants as follows:
        
            .. code-block: java
            
            for (ExhaustiveSearchType c : ExhaustiveSearchType.values())
                System.out.println(c);
            
        
            Returns:
                an array containing the constants of this enum type, in the order they are declared
        
        
        """
        ...

class NodeExplorationType(java.lang.Enum['NodeExplorationType']):
    """
    public enum NodeExplorationType extends :class:`~org.optaplanner.core.config.exhaustivesearch.https:.docs.oracle.com.javase.8.docs.api.java.lang.Enum?is`<:class:`~org.optaplanner.core.config.exhaustivesearch.NodeExplorationType`>
    """
    ORIGINAL_ORDER: typing.ClassVar['NodeExplorationType'] = ...
    DEPTH_FIRST: typing.ClassVar['NodeExplorationType'] = ...
    BREADTH_FIRST: typing.ClassVar['NodeExplorationType'] = ...
    SCORE_FIRST: typing.ClassVar['NodeExplorationType'] = ...
    OPTIMISTIC_BOUND_FIRST: typing.ClassVar['NodeExplorationType'] = ...
    def buildNodeComparator(self, boolean: bool) -> java.util.Comparator[org.optaplanner.core.impl.exhaustivesearch.node.ExhaustiveSearchNode]: ...
    _valueOf_0__T = typing.TypeVar('_valueOf_0__T', bound=java.lang.Enum)  # <T>
    @typing.overload
    @staticmethod
    def valueOf(class_: typing.Type[_valueOf_0__T], string: str) -> _valueOf_0__T: ...
    @typing.overload
    @staticmethod
    def valueOf(string: str) -> 'NodeExplorationType':
        """
            Returns the enum constant of this type with the specified name. The string must match *exactly* an identifier used to
            declare an enum constant in this type. (Extraneous whitespace characters are not permitted.)
        
            Parameters:
                name (:class:`~org.optaplanner.core.config.exhaustivesearch.https:.docs.oracle.com.javase.8.docs.api.java.lang.String?is`): the name of the enum constant to be returned.
        
            Returns:
                the enum constant with the specified name
        
            Raises:
                :class:`~org.optaplanner.core.config.exhaustivesearch.https:.docs.oracle.com.javase.8.docs.api.java.lang.IllegalArgumentException?is`: if this enum type has no constant with the specified name
                :class:`~org.optaplanner.core.config.exhaustivesearch.https:.docs.oracle.com.javase.8.docs.api.java.lang.NullPointerException?is`: if the argument is null
        
        
        """
        ...
    @staticmethod
    def values() -> typing.List['NodeExplorationType']:
        """
            Returns an array containing the constants of this enum type, in the order they are declared. This method may be used to
            iterate over the constants as follows:
        
            .. code-block: java
            
            for (NodeExplorationType c : NodeExplorationType.values())
                System.out.println(c);
            
        
            Returns:
                an array containing the constants of this enum type, in the order they are declared
        
        
        """
        ...


class __module_protocol__(typing.Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.optaplanner.core.config.exhaustivesearch")``.

    ExhaustiveSearchPhaseConfig: typing.Type[ExhaustiveSearchPhaseConfig]
    ExhaustiveSearchType: typing.Type[ExhaustiveSearchType]
    NodeExplorationType: typing.Type[NodeExplorationType]
