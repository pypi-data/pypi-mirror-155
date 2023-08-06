import java.io
import java.lang
import java.time
import java.util
import java.util.concurrent
import java.util.function
import jpype.protocol
import org.optaplanner.core.api.domain.common
import org.optaplanner.core.api.domain.solution.cloner
import org.optaplanner.core.api.score.calculator
import org.optaplanner.core.api.score.stream
import org.optaplanner.core.config
import org.optaplanner.core.config.phase
import org.optaplanner.core.config.score.director
import org.optaplanner.core.config.solver.monitoring
import org.optaplanner.core.config.solver.random
import org.optaplanner.core.config.solver.termination
import org.optaplanner.core.impl.domain.common.accessor
import org.optaplanner.core.impl.solver.random
import typing



class EnvironmentMode(java.lang.Enum['EnvironmentMode']):
    """
    public enum EnvironmentMode extends :class:`~org.optaplanner.core.config.solver.https:.docs.oracle.com.javase.8.docs.api.java.lang.Enum?is`<:class:`~org.optaplanner.core.config.solver.EnvironmentMode`>
    
        The environment mode also allows you to detect common bugs in your implementation.
    
        Also, a :class:`~org.optaplanner.core.api.solver.Solver` has a single
        :class:`~org.optaplanner.core.config.solver.https:.docs.oracle.com.javase.8.docs.api.java.util.Random?is` instance. Some
        optimization algorithms use the
        :class:`~org.optaplanner.core.config.solver.https:.docs.oracle.com.javase.8.docs.api.java.util.Random?is` instance a lot
        more than others. For example simulated annealing depends highly on random numbers, while tabu search only depends on it
        to deal with score ties. This environment mode influences the seed of that
        :class:`~org.optaplanner.core.config.solver.https:.docs.oracle.com.javase.8.docs.api.java.util.Random?is` instance.
    """
    FULL_ASSERT: typing.ClassVar['EnvironmentMode'] = ...
    NON_INTRUSIVE_FULL_ASSERT: typing.ClassVar['EnvironmentMode'] = ...
    FAST_ASSERT: typing.ClassVar['EnvironmentMode'] = ...
    REPRODUCIBLE: typing.ClassVar['EnvironmentMode'] = ...
    NON_REPRODUCIBLE: typing.ClassVar['EnvironmentMode'] = ...
    def isAsserted(self) -> bool: ...
    def isIntrusiveFastAsserted(self) -> bool: ...
    def isNonIntrusiveFullAsserted(self) -> bool: ...
    def isReproducible(self) -> bool: ...
    _valueOf_0__T = typing.TypeVar('_valueOf_0__T', bound=java.lang.Enum)  # <T>
    @typing.overload
    @staticmethod
    def valueOf(class_: typing.Type[_valueOf_0__T], string: str) -> _valueOf_0__T: ...
    @typing.overload
    @staticmethod
    def valueOf(string: str) -> 'EnvironmentMode':
        """
            Returns the enum constant of this type with the specified name. The string must match *exactly* an identifier used to
            declare an enum constant in this type. (Extraneous whitespace characters are not permitted.)
        
            Parameters:
                name (:class:`~org.optaplanner.core.config.solver.https:.docs.oracle.com.javase.8.docs.api.java.lang.String?is`): the name of the enum constant to be returned.
        
            Returns:
                the enum constant with the specified name
        
            Raises:
                :class:`~org.optaplanner.core.config.solver.https:.docs.oracle.com.javase.8.docs.api.java.lang.IllegalArgumentException?is`: if this enum type has no constant with the specified name
                :class:`~org.optaplanner.core.config.solver.https:.docs.oracle.com.javase.8.docs.api.java.lang.NullPointerException?is`: if the argument is null
        
        
        """
        ...
    @staticmethod
    def values() -> typing.List['EnvironmentMode']:
        """
            Returns an array containing the constants of this enum type, in the order they are declared. This method may be used to
            iterate over the constants as follows:
        
            .. code-block: java
            
            for (EnvironmentMode c : EnvironmentMode.values())
                System.out.println(c);
            
        
            Returns:
                an array containing the constants of this enum type, in the order they are declared
        
        
        """
        ...

class SolverConfig(org.optaplanner.core.config.AbstractConfig['SolverConfig']):
    """
    public class SolverConfig extends :class:`~org.optaplanner.core.config.AbstractConfig`<:class:`~org.optaplanner.core.config.solver.SolverConfig`>
    
        To read it from XML, use :meth:`~org.optaplanner.core.config.solver.SolverConfig.createFromXmlResource`. To build a
        :class:`~org.optaplanner.core.api.solver.SolverFactory` with it, use
        :meth:`~org.optaplanner.core.api.solver.SolverFactory.create`.
    """
    XML_ELEMENT_NAME: typing.ClassVar[str] = ...
    """
    public static final :class:`~org.optaplanner.core.config.solver.https:.docs.oracle.com.javase.8.docs.api.java.lang.String?is` XML_ELEMENT_NAME
    
    
        Also see:
            :meth:`~constant`
    
    
    """
    XML_NAMESPACE: typing.ClassVar[str] = ...
    """
    public static final :class:`~org.optaplanner.core.config.solver.https:.docs.oracle.com.javase.8.docs.api.java.lang.String?is` XML_NAMESPACE
    
    
        Also see:
            :meth:`~constant`
    
    
    """
    XML_TYPE_NAME: typing.ClassVar[str] = ...
    """
    public static final :class:`~org.optaplanner.core.config.solver.https:.docs.oracle.com.javase.8.docs.api.java.lang.String?is` XML_TYPE_NAME
    
    
        Also see:
            :meth:`~constant`
    
    
    """
    MOVE_THREAD_COUNT_NONE: typing.ClassVar[str] = ...
    """
    public static final :class:`~org.optaplanner.core.config.solver.https:.docs.oracle.com.javase.8.docs.api.java.lang.String?is` MOVE_THREAD_COUNT_NONE
    
    
        Also see:
            :meth:`~constant`
    
    
    """
    MOVE_THREAD_COUNT_AUTO: typing.ClassVar[str] = ...
    """
    public static final :class:`~org.optaplanner.core.config.solver.https:.docs.oracle.com.javase.8.docs.api.java.lang.String?is` MOVE_THREAD_COUNT_AUTO
    
    
        Also see:
            :meth:`~constant`
    
    
    """
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, classLoader: java.lang.ClassLoader): ...
    @typing.overload
    def __init__(self, solverConfig: 'SolverConfig'): ...
    def copyConfig(self) -> 'SolverConfig':
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
    @typing.overload
    @staticmethod
    def createFromXmlFile(file: typing.Union[java.io.File, jpype.protocol.SupportsPath]) -> 'SolverConfig':
        """
            Reads an XML solver configuration from the file system.
        
            Warning: this leads to platform dependent code, it's recommend to use
            :meth:`~org.optaplanner.core.config.solver.SolverConfig.createFromXmlResource` instead.
        
            Parameters:
                solverConfigFile (:class:`~org.optaplanner.core.config.solver.https:.docs.oracle.com.javase.8.docs.api.java.io.File?is`): never null
        
            Returns:
                never null
        
            As defined by :meth:`~org.optaplanner.core.config.solver.SolverConfig.createFromXmlFile`.
        
            Parameters:
                solverConfigFile (:class:`~org.optaplanner.core.config.solver.https:.docs.oracle.com.javase.8.docs.api.java.io.File?is`): never null
                classLoader (:class:`~org.optaplanner.core.config.solver.https:.docs.oracle.com.javase.8.docs.api.java.lang.ClassLoader?is`): sometimes null, the
                    :class:`~org.optaplanner.core.config.solver.https:.docs.oracle.com.javase.8.docs.api.java.lang.ClassLoader?is` to use
                    for loading all resources and
                    :class:`~org.optaplanner.core.config.solver.https:.docs.oracle.com.javase.8.docs.api.java.lang.Class?is`es, null to use
                    the default
                    :class:`~org.optaplanner.core.config.solver.https:.docs.oracle.com.javase.8.docs.api.java.lang.ClassLoader?is`
        
            Returns:
                never null
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def createFromXmlFile(file: typing.Union[java.io.File, jpype.protocol.SupportsPath], classLoader: java.lang.ClassLoader) -> 'SolverConfig': ...
    @typing.overload
    @staticmethod
    def createFromXmlInputStream(inputStream: java.io.InputStream) -> 'SolverConfig':
        """
        
            Parameters:
                in (:class:`~org.optaplanner.core.config.solver.https:.docs.oracle.com.javase.8.docs.api.java.io.InputStream?is`): never null, gets closed
        
            Returns:
                never null
        
            As defined by :meth:`~org.optaplanner.core.config.solver.SolverConfig.createFromXmlInputStream`.
        
            Parameters:
                in (:class:`~org.optaplanner.core.config.solver.https:.docs.oracle.com.javase.8.docs.api.java.io.InputStream?is`): never null, gets closed
                classLoader (:class:`~org.optaplanner.core.config.solver.https:.docs.oracle.com.javase.8.docs.api.java.lang.ClassLoader?is`): sometimes null, the
                    :class:`~org.optaplanner.core.config.solver.https:.docs.oracle.com.javase.8.docs.api.java.lang.ClassLoader?is` to use
                    for loading all resources and
                    :class:`~org.optaplanner.core.config.solver.https:.docs.oracle.com.javase.8.docs.api.java.lang.Class?is`es, null to use
                    the default
                    :class:`~org.optaplanner.core.config.solver.https:.docs.oracle.com.javase.8.docs.api.java.lang.ClassLoader?is`
        
            Returns:
                never null
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def createFromXmlInputStream(inputStream: java.io.InputStream, classLoader: java.lang.ClassLoader) -> 'SolverConfig': ...
    @typing.overload
    @staticmethod
    def createFromXmlReader(reader: java.io.Reader) -> 'SolverConfig':
        """
        
            Parameters:
                reader (:class:`~org.optaplanner.core.config.solver.https:.docs.oracle.com.javase.8.docs.api.java.io.Reader?is`): never null, gets closed
        
            Returns:
                never null
        
            As defined by :meth:`~org.optaplanner.core.config.solver.SolverConfig.createFromXmlReader`.
        
            Parameters:
                reader (:class:`~org.optaplanner.core.config.solver.https:.docs.oracle.com.javase.8.docs.api.java.io.Reader?is`): never null, gets closed
                classLoader (:class:`~org.optaplanner.core.config.solver.https:.docs.oracle.com.javase.8.docs.api.java.lang.ClassLoader?is`): sometimes null, the
                    :class:`~org.optaplanner.core.config.solver.https:.docs.oracle.com.javase.8.docs.api.java.lang.ClassLoader?is` to use
                    for loading all resources and
                    :class:`~org.optaplanner.core.config.solver.https:.docs.oracle.com.javase.8.docs.api.java.lang.Class?is`es, null to use
                    the default
                    :class:`~org.optaplanner.core.config.solver.https:.docs.oracle.com.javase.8.docs.api.java.lang.ClassLoader?is`
        
            Returns:
                never null
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def createFromXmlReader(reader: java.io.Reader, classLoader: java.lang.ClassLoader) -> 'SolverConfig': ...
    @typing.overload
    @staticmethod
    def createFromXmlResource(string: str) -> 'SolverConfig':
        """
            Reads an XML solver configuration from the classpath.
        
            Parameters:
                solverConfigResource (:class:`~org.optaplanner.core.config.solver.https:.docs.oracle.com.javase.8.docs.api.java.lang.String?is`): never null, a classpath resource as defined by
                    :meth:`~org.optaplanner.core.config.solver.https:.docs.oracle.com.javase.8.docs.api.java.lang.ClassLoader.html?is`
        
            Returns:
                never null
        
            As defined by :meth:`~org.optaplanner.core.config.solver.SolverConfig.createFromXmlResource`.
        
            Parameters:
                solverConfigResource (:class:`~org.optaplanner.core.config.solver.https:.docs.oracle.com.javase.8.docs.api.java.lang.String?is`): never null, a classpath resource as defined by
                    :meth:`~org.optaplanner.core.config.solver.https:.docs.oracle.com.javase.8.docs.api.java.lang.ClassLoader.html?is`
                classLoader (:class:`~org.optaplanner.core.config.solver.https:.docs.oracle.com.javase.8.docs.api.java.lang.ClassLoader?is`): sometimes null, the
                    :class:`~org.optaplanner.core.config.solver.https:.docs.oracle.com.javase.8.docs.api.java.lang.ClassLoader?is` to use
                    for loading all resources and
                    :class:`~org.optaplanner.core.config.solver.https:.docs.oracle.com.javase.8.docs.api.java.lang.Class?is`es, null to use
                    the default
                    :class:`~org.optaplanner.core.config.solver.https:.docs.oracle.com.javase.8.docs.api.java.lang.ClassLoader?is`
        
            Returns:
                never null
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def createFromXmlResource(string: str, classLoader: java.lang.ClassLoader) -> 'SolverConfig': ...
    def determineDomainAccessType(self) -> org.optaplanner.core.api.domain.common.DomainAccessType: ...
    def determineEnvironmentMode(self) -> EnvironmentMode: ...
    def determineMetricConfig(self) -> org.optaplanner.core.config.solver.monitoring.MonitoringConfig: ...
    def getClassLoader(self) -> java.lang.ClassLoader: ...
    def getDaemon(self) -> bool: ...
    def getDomainAccessType(self) -> org.optaplanner.core.api.domain.common.DomainAccessType: ...
    def getEntityClassList(self) -> java.util.List[typing.Type[typing.Any]]: ...
    def getEnvironmentMode(self) -> EnvironmentMode: ...
    def getGizmoMemberAccessorMap(self) -> java.util.Map[str, org.optaplanner.core.impl.domain.common.accessor.MemberAccessor]: ...
    def getGizmoSolutionClonerMap(self) -> java.util.Map[str, org.optaplanner.core.api.domain.solution.cloner.SolutionCloner]: ...
    def getMonitoringConfig(self) -> org.optaplanner.core.config.solver.monitoring.MonitoringConfig: ...
    def getMoveThreadBufferSize(self) -> int: ...
    def getMoveThreadCount(self) -> str: ...
    def getPhaseConfigList(self) -> java.util.List[org.optaplanner.core.config.phase.PhaseConfig]: ...
    def getRandomFactoryClass(self) -> typing.Type[org.optaplanner.core.impl.solver.random.RandomFactory]: ...
    def getRandomSeed(self) -> int: ...
    def getRandomType(self) -> org.optaplanner.core.config.solver.random.RandomType: ...
    def getScoreDirectorFactoryConfig(self) -> org.optaplanner.core.config.score.director.ScoreDirectorFactoryConfig: ...
    def getSolutionClass(self) -> typing.Type[typing.Any]: ...
    def getTerminationConfig(self) -> org.optaplanner.core.config.solver.termination.TerminationConfig: ...
    def getThreadFactoryClass(self) -> typing.Type[java.util.concurrent.ThreadFactory]: ...
    def inherit(self, solverConfig: 'SolverConfig') -> 'SolverConfig':
        """
            Do not use this method, it is an internal method. Use
            :meth:`~org.optaplanner.core.config.solver.SolverConfig.%3Cinit%3E` instead.
        
            Specified by:
                :meth:`~org.optaplanner.core.config.AbstractConfig.inherit` in
                class :class:`~org.optaplanner.core.config.AbstractConfig`
        
            Parameters:
                inheritedConfig (:class:`~org.optaplanner.core.config.solver.SolverConfig`): never null
        
            Returns:
                this
        
        
        """
        ...
    def offerRandomSeedFromSubSingleIndex(self, long: int) -> None: ...
    def setClassLoader(self, classLoader: java.lang.ClassLoader) -> None: ...
    def setDaemon(self, boolean: bool) -> None: ...
    def setDomainAccessType(self, domainAccessType: org.optaplanner.core.api.domain.common.DomainAccessType) -> None: ...
    def setEntityClassList(self, list: java.util.List[typing.Type[typing.Any]]) -> None: ...
    def setEnvironmentMode(self, environmentMode: EnvironmentMode) -> None: ...
    def setGizmoMemberAccessorMap(self, map: typing.Union[java.util.Map[str, org.optaplanner.core.impl.domain.common.accessor.MemberAccessor], typing.Mapping[str, org.optaplanner.core.impl.domain.common.accessor.MemberAccessor]]) -> None: ...
    def setGizmoSolutionClonerMap(self, map: typing.Union[java.util.Map[str, org.optaplanner.core.api.domain.solution.cloner.SolutionCloner], typing.Mapping[str, org.optaplanner.core.api.domain.solution.cloner.SolutionCloner]]) -> None: ...
    def setMonitoringConfig(self, monitoringConfig: org.optaplanner.core.config.solver.monitoring.MonitoringConfig) -> None: ...
    def setMoveThreadBufferSize(self, integer: int) -> None: ...
    def setMoveThreadCount(self, string: str) -> None: ...
    def setPhaseConfigList(self, list: java.util.List[org.optaplanner.core.config.phase.PhaseConfig]) -> None: ...
    def setRandomFactoryClass(self, class_: typing.Type[org.optaplanner.core.impl.solver.random.RandomFactory]) -> None: ...
    def setRandomSeed(self, long: int) -> None: ...
    def setRandomType(self, randomType: org.optaplanner.core.config.solver.random.RandomType) -> None: ...
    def setScoreDirectorFactoryConfig(self, scoreDirectorFactoryConfig: org.optaplanner.core.config.score.director.ScoreDirectorFactoryConfig) -> None: ...
    def setSolutionClass(self, class_: typing.Type[typing.Any]) -> None: ...
    def setTerminationConfig(self, terminationConfig: org.optaplanner.core.config.solver.termination.TerminationConfig) -> None: ...
    def setThreadFactoryClass(self, class_: typing.Type[java.util.concurrent.ThreadFactory]) -> None: ...
    def visitReferencedClasses(self, consumer: typing.Union[java.util.function.Consumer[typing.Type[typing.Any]], typing.Callable[[typing.Type[typing.Any]], None]]) -> None: ...
    def withConstraintProviderClass(self, class_: typing.Type[org.optaplanner.core.api.score.stream.ConstraintProvider]) -> 'SolverConfig': ...
    def withDaemon(self, boolean: bool) -> 'SolverConfig': ...
    def withDomainAccessType(self, domainAccessType: org.optaplanner.core.api.domain.common.DomainAccessType) -> 'SolverConfig': ...
    def withEasyScoreCalculatorClass(self, class_: typing.Type[org.optaplanner.core.api.score.calculator.EasyScoreCalculator]) -> 'SolverConfig': ...
    def withEntityClassList(self, list: java.util.List[typing.Type[typing.Any]]) -> 'SolverConfig': ...
    def withEntityClasses(self, *class_: typing.Type[typing.Any]) -> 'SolverConfig': ...
    def withEnvironmentMode(self, environmentMode: EnvironmentMode) -> 'SolverConfig': ...
    def withGizmoMemberAccessorMap(self, map: typing.Union[java.util.Map[str, org.optaplanner.core.impl.domain.common.accessor.MemberAccessor], typing.Mapping[str, org.optaplanner.core.impl.domain.common.accessor.MemberAccessor]]) -> 'SolverConfig': ...
    def withGizmoSolutionClonerMap(self, map: typing.Union[java.util.Map[str, org.optaplanner.core.api.domain.solution.cloner.SolutionCloner], typing.Mapping[str, org.optaplanner.core.api.domain.solution.cloner.SolutionCloner]]) -> 'SolverConfig': ...
    def withMonitoringConfig(self, monitoringConfig: org.optaplanner.core.config.solver.monitoring.MonitoringConfig) -> 'SolverConfig': ...
    def withMoveThreadBufferSize(self, integer: int) -> 'SolverConfig': ...
    def withMoveThreadCount(self, string: str) -> 'SolverConfig': ...
    def withPhaseList(self, list: java.util.List[org.optaplanner.core.config.phase.PhaseConfig]) -> 'SolverConfig': ...
    def withPhases(self, *phaseConfig: org.optaplanner.core.config.phase.PhaseConfig) -> 'SolverConfig': ...
    def withRandomFactoryClass(self, class_: typing.Type[org.optaplanner.core.impl.solver.random.RandomFactory]) -> 'SolverConfig': ...
    def withRandomSeed(self, long: int) -> 'SolverConfig': ...
    def withRandomType(self, randomType: org.optaplanner.core.config.solver.random.RandomType) -> 'SolverConfig': ...
    def withScoreDirectorFactory(self, scoreDirectorFactoryConfig: org.optaplanner.core.config.score.director.ScoreDirectorFactoryConfig) -> 'SolverConfig': ...
    def withSolutionClass(self, class_: typing.Type[typing.Any]) -> 'SolverConfig': ...
    def withTerminationConfig(self, terminationConfig: org.optaplanner.core.config.solver.termination.TerminationConfig) -> 'SolverConfig': ...
    def withTerminationSpentLimit(self, duration: java.time.Duration) -> 'SolverConfig':
        """
            As defined by :meth:`~org.optaplanner.core.config.solver.termination.TerminationConfig.withSpentLimit`, but returns
            this.
        
            Parameters:
                spentLimit (:class:`~org.optaplanner.core.config.solver.https:.docs.oracle.com.javase.8.docs.api.java.time.Duration?is`): sometimes null
        
            Returns:
                this, never null
        
        
        """
        ...
    def withThreadFactoryClass(self, class_: typing.Type[java.util.concurrent.ThreadFactory]) -> 'SolverConfig': ...

class SolverManagerConfig(org.optaplanner.core.config.AbstractConfig['SolverManagerConfig']):
    """
    public class SolverManagerConfig extends :class:`~org.optaplanner.core.config.AbstractConfig`<:class:`~org.optaplanner.core.config.solver.SolverManagerConfig`>
    """
    PARALLEL_SOLVER_COUNT_AUTO: typing.ClassVar[str] = ...
    """
    public static final :class:`~org.optaplanner.core.config.solver.https:.docs.oracle.com.javase.8.docs.api.java.lang.String?is` PARALLEL_SOLVER_COUNT_AUTO
    
    
        Also see:
            :meth:`~constant`
    
    
    """
    def __init__(self): ...
    def copyConfig(self) -> 'SolverManagerConfig':
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
    def getParallelSolverCount(self) -> str: ...
    def getThreadFactoryClass(self) -> typing.Type[java.util.concurrent.ThreadFactory]: ...
    def inherit(self, solverManagerConfig: 'SolverManagerConfig') -> 'SolverManagerConfig':
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
                inheritedConfig (:class:`~org.optaplanner.core.config.solver.SolverManagerConfig`): never null
        
            Returns:
                this
        
        
        """
        ...
    def resolveParallelSolverCount(self) -> int: ...
    def setParallelSolverCount(self, string: str) -> None: ...
    def setThreadFactoryClass(self, class_: typing.Type[java.util.concurrent.ThreadFactory]) -> None: ...
    def visitReferencedClasses(self, consumer: typing.Union[java.util.function.Consumer[typing.Type[typing.Any]], typing.Callable[[typing.Type[typing.Any]], None]]) -> None: ...
    def withParallelSolverCount(self, string: str) -> 'SolverManagerConfig': ...
    def withThreadFactoryClass(self, class_: typing.Type[java.util.concurrent.ThreadFactory]) -> 'SolverManagerConfig': ...


class __module_protocol__(typing.Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.optaplanner.core.config.solver")``.

    EnvironmentMode: typing.Type[EnvironmentMode]
    SolverConfig: typing.Type[SolverConfig]
    SolverManagerConfig: typing.Type[SolverManagerConfig]
    monitoring: org.optaplanner.core.config.solver.monitoring.__module_protocol__
    random: org.optaplanner.core.config.solver.random.__module_protocol__
    termination: org.optaplanner.core.config.solver.termination.__module_protocol__
