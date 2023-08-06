import _jpype
import io.micrometer.core.instrument
import java.lang
import java.util
import java.util.concurrent.atomic
import java.util.function
import org.optaplanner.core.api.score
import org.optaplanner.core.api.solver
import org.optaplanner.core.config
import org.optaplanner.core.impl.score.definition
import typing



class MonitoringConfig(org.optaplanner.core.config.AbstractConfig['MonitoringConfig']):
    """
    public class MonitoringConfig extends :class:`~org.optaplanner.core.config.AbstractConfig`<:class:`~org.optaplanner.core.config.solver.monitoring.MonitoringConfig`>
    """
    def __init__(self): ...
    def copyConfig(self) -> 'MonitoringConfig':
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
    def getSolverMetricList(self) -> java.util.List['SolverMetric']: ...
    def inherit(self, monitoringConfig: 'MonitoringConfig') -> 'MonitoringConfig':
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
                inheritedConfig (:class:`~org.optaplanner.core.config.solver.monitoring.MonitoringConfig`): never null
        
            Returns:
                this
        
        
        """
        ...
    def setSolverMetricList(self, list: java.util.List['SolverMetric']) -> None: ...
    def visitReferencedClasses(self, consumer: typing.Union[java.util.function.Consumer[typing.Type[typing.Any]], typing.Callable[[typing.Type[typing.Any]], None]]) -> None: ...
    def withSolverMetricList(self, list: java.util.List['SolverMetric']) -> 'MonitoringConfig': ...

class SolverMetric(java.lang.Enum['SolverMetric']):
    """
    public enum SolverMetric extends :class:`~org.optaplanner.core.config.solver.monitoring.https:.docs.oracle.com.javase.8.docs.api.java.lang.Enum?is`<:class:`~org.optaplanner.core.config.solver.monitoring.SolverMetric`>
    """
    SOLVE_DURATION: typing.ClassVar['SolverMetric'] = ...
    ERROR_COUNT: typing.ClassVar['SolverMetric'] = ...
    BEST_SCORE: typing.ClassVar['SolverMetric'] = ...
    STEP_SCORE: typing.ClassVar['SolverMetric'] = ...
    SCORE_CALCULATION_COUNT: typing.ClassVar['SolverMetric'] = ...
    BEST_SOLUTION_MUTATION: typing.ClassVar['SolverMetric'] = ...
    MOVE_COUNT_PER_STEP: typing.ClassVar['SolverMetric'] = ...
    MEMORY_USE: typing.ClassVar['SolverMetric'] = ...
    CONSTRAINT_MATCH_TOTAL_BEST_SCORE: typing.ClassVar['SolverMetric'] = ...
    CONSTRAINT_MATCH_TOTAL_STEP_SCORE: typing.ClassVar['SolverMetric'] = ...
    PICKED_MOVE_TYPE_BEST_SCORE_DIFF: typing.ClassVar['SolverMetric'] = ...
    PICKED_MOVE_TYPE_STEP_SCORE_DIFF: typing.ClassVar['SolverMetric'] = ...
    def getMeterId(self) -> str: ...
    def isMetricBestSolutionBased(self) -> bool: ...
    def register(self, solver: org.optaplanner.core.api.solver.Solver[typing.Any]) -> None: ...
    @staticmethod
    def registerScoreMetrics(solverMetric: 'SolverMetric', tags: io.micrometer.core.instrument.Tags, scoreDefinition: org.optaplanner.core.impl.score.definition.ScoreDefinition[typing.Any], map: typing.Union[java.util.Map[io.micrometer.core.instrument.Tags, java.util.List[java.util.concurrent.atomic.AtomicReference[typing.Union[_jpype._JNumberLong, _jpype._JNumberFloat, typing.SupportsIndex, typing.SupportsFloat]]]], typing.Mapping[io.micrometer.core.instrument.Tags, java.util.List[java.util.concurrent.atomic.AtomicReference[typing.Union[_jpype._JNumberLong, _jpype._JNumberFloat, typing.SupportsIndex, typing.SupportsFloat]]]]], score2: org.optaplanner.core.api.score.Score[typing.Any]) -> None: ...
    def unregister(self, solver: org.optaplanner.core.api.solver.Solver[typing.Any]) -> None: ...
    _valueOf_0__T = typing.TypeVar('_valueOf_0__T', bound=java.lang.Enum)  # <T>
    @typing.overload
    @staticmethod
    def valueOf(class_: typing.Type[_valueOf_0__T], string: str) -> _valueOf_0__T: ...
    @typing.overload
    @staticmethod
    def valueOf(string: str) -> 'SolverMetric':
        """
            Returns the enum constant of this type with the specified name. The string must match *exactly* an identifier used to
            declare an enum constant in this type. (Extraneous whitespace characters are not permitted.)
        
            Parameters:
                name (:class:`~org.optaplanner.core.config.solver.monitoring.https:.docs.oracle.com.javase.8.docs.api.java.lang.String?is`): the name of the enum constant to be returned.
        
            Returns:
                the enum constant with the specified name
        
            Raises:
                :class:`~org.optaplanner.core.config.solver.monitoring.https:.docs.oracle.com.javase.8.docs.api.java.lang.IllegalArgumentException?is`: if this enum type has no constant with the specified name
                :class:`~org.optaplanner.core.config.solver.monitoring.https:.docs.oracle.com.javase.8.docs.api.java.lang.NullPointerException?is`: if the argument is null
        
        
        """
        ...
    @staticmethod
    def values() -> typing.List['SolverMetric']:
        """
            Returns an array containing the constants of this enum type, in the order they are declared. This method may be used to
            iterate over the constants as follows:
        
            .. code-block: java
            
            for (SolverMetric c : SolverMetric.values())
                System.out.println(c);
            
        
            Returns:
                an array containing the constants of this enum type, in the order they are declared
        
        
        """
        ...


class __module_protocol__(typing.Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.optaplanner.core.config.solver.monitoring")``.

    MonitoringConfig: typing.Type[MonitoringConfig]
    SolverMetric: typing.Type[SolverMetric]
