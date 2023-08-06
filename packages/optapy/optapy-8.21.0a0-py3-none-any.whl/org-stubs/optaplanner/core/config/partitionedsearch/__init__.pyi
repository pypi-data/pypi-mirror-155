import java.util
import java.util.function
import org.optaplanner.core.config.phase
import org.optaplanner.core.impl.partitionedsearch.partitioner
import typing



class PartitionedSearchPhaseConfig(org.optaplanner.core.config.phase.PhaseConfig['PartitionedSearchPhaseConfig']):
    """
    public class PartitionedSearchPhaseConfig extends :class:`~org.optaplanner.core.config.phase.PhaseConfig`<:class:`~org.optaplanner.core.config.partitionedsearch.PartitionedSearchPhaseConfig`>
    """
    XML_ELEMENT_NAME: typing.ClassVar[str] = ...
    """
    public static final :class:`~org.optaplanner.core.config.partitionedsearch.https:.docs.oracle.com.javase.8.docs.api.java.lang.String?is` XML_ELEMENT_NAME
    
    
        Also see:
            :meth:`~constant`
    
    
    """
    ACTIVE_THREAD_COUNT_AUTO: typing.ClassVar[str] = ...
    """
    public static final :class:`~org.optaplanner.core.config.partitionedsearch.https:.docs.oracle.com.javase.8.docs.api.java.lang.String?is` ACTIVE_THREAD_COUNT_AUTO
    
    
        Also see:
            :meth:`~constant`
    
    
    """
    ACTIVE_THREAD_COUNT_UNLIMITED: typing.ClassVar[str] = ...
    """
    public static final :class:`~org.optaplanner.core.config.partitionedsearch.https:.docs.oracle.com.javase.8.docs.api.java.lang.String?is` ACTIVE_THREAD_COUNT_UNLIMITED
    
    
        Also see:
            :meth:`~constant`
    
    
    """
    def __init__(self): ...
    def copyConfig(self) -> 'PartitionedSearchPhaseConfig':
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
    def getPhaseConfigList(self) -> java.util.List[org.optaplanner.core.config.phase.PhaseConfig]: ...
    def getRunnablePartThreadLimit(self) -> str:
        """
            Similar to a thread pool size, but instead of limiting the number of
            :class:`~org.optaplanner.core.config.partitionedsearch.https:.docs.oracle.com.javase.8.docs.api.java.lang.Thread?is`s,
            it limits the number of
            :meth:`~org.optaplanner.core.config.partitionedsearch.https:.docs.oracle.com.javase.8.docs.api.java.lang.Thread.State.html?is`
            :class:`~org.optaplanner.core.config.partitionedsearch.https:.docs.oracle.com.javase.8.docs.api.java.lang.Thread?is`s to
            avoid consuming all CPU resources (which would starve UI, Servlets and REST threads).
        
            The number of
            :class:`~org.optaplanner.core.config.partitionedsearch.https:.docs.oracle.com.javase.8.docs.api.java.lang.Thread?is`s is
            always equal to the number of partitions returned by
            :meth:`~org.optaplanner.core.impl.partitionedsearch.partitioner.SolutionPartitioner.splitWorkingSolution`, because
            otherwise some partitions would never run (especially with
            :meth:`~org.optaplanner.core.api.solver.Solver.terminateEarly`). If this limit (or
            :meth:`~org.optaplanner.core.config.partitionedsearch.https:.docs.oracle.com.javase.8.docs.api.java.lang.Runtime.html?is`)
            is lower than the number of partitions, this results in a slower score calculation speed per partition
            :class:`~org.optaplanner.core.api.solver.Solver`.
        
            Defaults to :meth:`~org.optaplanner.core.config.partitionedsearch.PartitionedSearchPhaseConfig.ACTIVE_THREAD_COUNT_AUTO`
            which consumes the majority but not all of the CPU cores on multi-core machines, to prevent a livelock that hangs other
            processes (such as your IDE, REST servlets threads or SSH connections) on the machine.
        
            Use :meth:`~org.optaplanner.core.config.partitionedsearch.PartitionedSearchPhaseConfig.ACTIVE_THREAD_COUNT_UNLIMITED` to
            give it all CPU cores. This is useful if you're handling the CPU consumption on an OS level.
        
            Returns:
                null, a number,
                :meth:`~org.optaplanner.core.config.partitionedsearch.PartitionedSearchPhaseConfig.ACTIVE_THREAD_COUNT_AUTO` or
                :meth:`~org.optaplanner.core.config.partitionedsearch.PartitionedSearchPhaseConfig.ACTIVE_THREAD_COUNT_UNLIMITED`.
        
        
        """
        ...
    def getSolutionPartitionerClass(self) -> typing.Type[org.optaplanner.core.impl.partitionedsearch.partitioner.SolutionPartitioner[typing.Any]]: ...
    def getSolutionPartitionerCustomProperties(self) -> java.util.Map[str, str]: ...
    def inherit(self, partitionedSearchPhaseConfig: 'PartitionedSearchPhaseConfig') -> 'PartitionedSearchPhaseConfig':
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
                inheritedConfig (:class:`~org.optaplanner.core.config.partitionedsearch.PartitionedSearchPhaseConfig`): never null
        
            Returns:
                this
        
        
        """
        ...
    def setPhaseConfigList(self, list: java.util.List[org.optaplanner.core.config.phase.PhaseConfig]) -> None: ...
    def setRunnablePartThreadLimit(self, string: str) -> None: ...
    def setSolutionPartitionerClass(self, class_: typing.Type[org.optaplanner.core.impl.partitionedsearch.partitioner.SolutionPartitioner[typing.Any]]) -> None: ...
    def setSolutionPartitionerCustomProperties(self, map: typing.Union[java.util.Map[str, str], typing.Mapping[str, str]]) -> None: ...
    def visitReferencedClasses(self, consumer: typing.Union[java.util.function.Consumer[typing.Type[typing.Any]], typing.Callable[[typing.Type[typing.Any]], None]]) -> None: ...


class __module_protocol__(typing.Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.optaplanner.core.config.partitionedsearch")``.

    PartitionedSearchPhaseConfig: typing.Type[PartitionedSearchPhaseConfig]
