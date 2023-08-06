import java.io
import java.lang
import java.time
import java.util
import java.util.concurrent
import java.util.function
import jpype.protocol
import org.optaplanner.core.api.score.director
import org.optaplanner.core.api.solver.change
import org.optaplanner.core.api.solver.event
import org.optaplanner.core.config.solver
import typing



_ProblemFactChange__Solution_ = typing.TypeVar('_ProblemFactChange__Solution_')  # <Solution_>
class ProblemFactChange(typing.Generic[_ProblemFactChange__Solution_]):
    """
    :class:`~org.optaplanner.core.api.solver.https:.docs.oracle.com.javase.8.docs.api.java.lang.Deprecated?is`(:meth:`~org.optaplanner.core.api.solver.https:.docs.oracle.com.javase.8.docs.api.java.lang.Deprecated.html?is`=true) :class:`~org.optaplanner.core.api.solver.https:.docs.oracle.com.javase.8.docs.api.java.lang.FunctionalInterface?is` public interface ProblemFactChange<Solution_>
    
        Deprecated, for removal: This API element is subject to removal in a future version.
        in favor of :class:`~org.optaplanner.core.api.solver.change.ProblemChange`.
        This interface is deprecated. A ProblemFactChange represents a change in 1 or more problem facts of a
        :class:`~org.optaplanner.core.api.domain.solution.PlanningSolution`. Problem facts used by a
        :class:`~org.optaplanner.core.api.solver.Solver` must not be changed while it is solving, but by scheduling this command
        to the :class:`~org.optaplanner.core.api.solver.Solver`, you can change them when the time is right.
    
        Note that the :class:`~org.optaplanner.core.api.solver.Solver` clones a
        :class:`~org.optaplanner.core.api.domain.solution.PlanningSolution` at will. So any change must be done on the problem
        facts and planning entities referenced by the :class:`~org.optaplanner.core.api.domain.solution.PlanningSolution` of the
        :class:`~org.optaplanner.core.api.score.director.ScoreDirector`. On each change it should also notify the
        :class:`~org.optaplanner.core.api.score.director.ScoreDirector` accordingly.
    """
    def doChange(self, scoreDirector: org.optaplanner.core.api.score.director.ScoreDirector[_ProblemFactChange__Solution_]) -> None: ...

_Solver__Solution_ = typing.TypeVar('_Solver__Solution_')  # <Solution_>
class Solver(typing.Generic[_Solver__Solution_]):
    """
    public interface Solver<Solution_>
    
        A Solver solves a planning problem and returns the best solution found. It's recommended to create a new Solver instance
        for each dataset.
    
        To create a Solver, use :meth:`~org.optaplanner.core.api.solver.SolverFactory.buildSolver`. To solve a planning problem,
        call :meth:`~org.optaplanner.core.api.solver.Solver.solve`. To solve a planning problem without blocking the current
        thread, use :class:`~org.optaplanner.core.api.solver.SolverManager` instead.
    
        These methods are not thread-safe and should be called from the same thread, except for the methods that are explicitly
        marked as thread-safe. Note that despite that :meth:`~org.optaplanner.core.api.solver.Solver.solve` is not thread-safe
        for clients of this class, that method is free to do multithreading inside itself.
    """
    def addEventListener(self, solverEventListener: typing.Union[org.optaplanner.core.api.solver.event.SolverEventListener[_Solver__Solution_], typing.Callable[[org.optaplanner.core.api.solver.event.BestSolutionChangedEvent[typing.Any]], None]]) -> None: ...
    def addProblemChange(self, problemChange: typing.Union[org.optaplanner.core.api.solver.change.ProblemChange[_Solver__Solution_], typing.Callable[[_Solver__Solution_, org.optaplanner.core.api.solver.change.ProblemChangeDirector], None]]) -> None: ...
    def addProblemChanges(self, list: java.util.List[typing.Union[org.optaplanner.core.api.solver.change.ProblemChange[_Solver__Solution_], typing.Callable[[_Solver__Solution_, org.optaplanner.core.api.solver.change.ProblemChangeDirector], None]]]) -> None: ...
    def addProblemFactChange(self, problemFactChange: typing.Union[ProblemFactChange[_Solver__Solution_], typing.Callable[[org.optaplanner.core.api.score.director.ScoreDirector[typing.Any]], None]]) -> bool: ...
    def addProblemFactChanges(self, list: java.util.List[typing.Union[ProblemFactChange[_Solver__Solution_], typing.Callable[[org.optaplanner.core.api.score.director.ScoreDirector[typing.Any]], None]]]) -> bool: ...
    def isEveryProblemChangeProcessed(self) -> bool:
        """
            Checks if all scheduled :class:`~org.optaplanner.core.api.solver.change.ProblemChange`s have been processed.
        
            This method is thread-safe.
        
            Returns:
                true if there are no :class:`~org.optaplanner.core.api.solver.change.ProblemChange`s left to do
        
        
        """
        ...
    def isEveryProblemFactChangeProcessed(self) -> bool: ...
    def isSolving(self) -> bool:
        """
            This method is thread-safe.
        
            Returns:
                true if the :meth:`~org.optaplanner.core.api.solver.Solver.solve` method is still running.
        
        
        """
        ...
    def isTerminateEarly(self) -> bool:
        """
            This method is thread-safe.
        
            Returns:
                true if terminateEarly has been called since the :class:`~org.optaplanner.core.api.solver.Solver` started.
        
            Also see:
                :meth:`~org.optaplanner.core.api.solver.https:.docs.oracle.com.javase.8.docs.api.java.util.concurrent.Future.html?is`
        
        
        """
        ...
    def removeEventListener(self, solverEventListener: typing.Union[org.optaplanner.core.api.solver.event.SolverEventListener[_Solver__Solution_], typing.Callable[[org.optaplanner.core.api.solver.event.BestSolutionChangedEvent[typing.Any]], None]]) -> None: ...
    def solve(self, solution_: _Solver__Solution_) -> _Solver__Solution_:
        """
            Solves the planning problem and returns the best solution encountered (which might or might not be optimal, feasible or
            even initialized).
        
            It can take seconds, minutes, even hours or days before this method returns, depending on the termination configuration.
            To terminate a :class:`~org.optaplanner.core.api.solver.Solver` early, call
            :meth:`~org.optaplanner.core.api.solver.Solver.terminateEarly`.
        
            Parameters:
                problem (:class:`~org.optaplanner.core.api.solver.Solver`): never null, a :class:`~org.optaplanner.core.api.domain.solution.PlanningSolution`, usually its planning variables are
                    uninitialized
        
            Returns:
                never null, but it can return the original, uninitialized
                :class:`~org.optaplanner.core.api.domain.solution.PlanningSolution` with a null
                :class:`~org.optaplanner.core.api.score.Score`.
        
            Also see:
                :meth:`~org.optaplanner.core.api.solver.Solver.terminateEarly`
        
        
        """
        ...
    def terminateEarly(self) -> bool:
        """
            Notifies the solver that it should stop at its earliest convenience. This method returns immediately, but it takes an
            undetermined time for the :meth:`~org.optaplanner.core.api.solver.Solver.solve` to actually return.
        
            If the solver is running in daemon mode, this is the only way to terminate it normally.
        
            This method is thread-safe. It can only be called from a different thread because the original thread is still calling
            :meth:`~org.optaplanner.core.api.solver.Solver.solve`.
        
            Returns:
                true if successful, false if was already terminating or terminated
        
            Also see:
                :meth:`~org.optaplanner.core.api.solver.Solver.isTerminateEarly`,
                :meth:`~org.optaplanner.core.api.solver.https:.docs.oracle.com.javase.8.docs.api.java.util.concurrent.Future.html?is`
        
        
        """
        ...

_SolverFactory__Solution_ = typing.TypeVar('_SolverFactory__Solution_')  # <Solution_>
class SolverFactory(typing.Generic[_SolverFactory__Solution_]):
    """
    public interface SolverFactory<Solution_>
    
        Creates :class:`~org.optaplanner.core.api.solver.Solver` instances. Most applications only need one SolverFactory.
    
        To create a SolverFactory, use :meth:`~org.optaplanner.core.api.solver.SolverFactory.createFromXmlResource`. To change
        the configuration programmatically, create a :class:`~org.optaplanner.core.config.solver.SolverConfig` first and then
        use :meth:`~org.optaplanner.core.api.solver.SolverFactory.create`.
    
        These methods are thread-safe unless explicitly stated otherwise.
    """
    def buildSolver(self) -> Solver[_SolverFactory__Solution_]: ...
    _create__Solution_ = typing.TypeVar('_create__Solution_')  # <Solution_>
    @staticmethod
    def create(solverConfig: org.optaplanner.core.config.solver.SolverConfig) -> 'SolverFactory'[_create__Solution_]:
        """
            Uses a :class:`~org.optaplanner.core.config.solver.SolverConfig` to build a
            :class:`~org.optaplanner.core.api.solver.SolverFactory`. If you don't need to manipulate the
            :class:`~org.optaplanner.core.config.solver.SolverConfig` programmatically, use
            :meth:`~org.optaplanner.core.api.solver.SolverFactory.createFromXmlResource` instead.
        
            Parameters:
                solverConfig (:class:`~org.optaplanner.core.config.solver.SolverConfig`): never null
        
            Returns:
                never null, subsequent changes to the config have no effect on the returned instance
        
        
        """
        ...
    _createFromXmlFile_0__Solution_ = typing.TypeVar('_createFromXmlFile_0__Solution_')  # <Solution_>
    _createFromXmlFile_1__Solution_ = typing.TypeVar('_createFromXmlFile_1__Solution_')  # <Solution_>
    @typing.overload
    @staticmethod
    def createFromXmlFile(file: typing.Union[java.io.File, jpype.protocol.SupportsPath]) -> 'SolverFactory'[_createFromXmlFile_0__Solution_]:
        """
            Reads an XML solver configuration from the file system and uses that
            :class:`~org.optaplanner.core.config.solver.SolverConfig` to build a
            :class:`~org.optaplanner.core.api.solver.SolverFactory`.
        
            Warning: this leads to platform dependent code, it's recommend to use
            :meth:`~org.optaplanner.core.api.solver.SolverFactory.createFromXmlResource` instead.
        
            Parameters:
                solverConfigFile (:class:`~org.optaplanner.core.api.solver.https:.docs.oracle.com.javase.8.docs.api.java.io.File?is`): never null
        
            Returns:
                never null, subsequent changes to the config have no effect on the returned instance
        
            As defined by :meth:`~org.optaplanner.core.api.solver.SolverFactory.createFromXmlFile`.
        
            Parameters:
                solverConfigFile (:class:`~org.optaplanner.core.api.solver.https:.docs.oracle.com.javase.8.docs.api.java.io.File?is`): never null
                classLoader (:class:`~org.optaplanner.core.api.solver.https:.docs.oracle.com.javase.8.docs.api.java.lang.ClassLoader?is`): sometimes null, the
                    :class:`~org.optaplanner.core.api.solver.https:.docs.oracle.com.javase.8.docs.api.java.lang.ClassLoader?is` to use for
                    loading all resources and
                    :class:`~org.optaplanner.core.api.solver.https:.docs.oracle.com.javase.8.docs.api.java.lang.Class?is`es, null to use the
                    default :class:`~org.optaplanner.core.api.solver.https:.docs.oracle.com.javase.8.docs.api.java.lang.ClassLoader?is`
        
            Returns:
                never null, subsequent changes to the config have no effect on the returned instance
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def createFromXmlFile(file: typing.Union[java.io.File, jpype.protocol.SupportsPath], classLoader: java.lang.ClassLoader) -> 'SolverFactory'[_createFromXmlFile_1__Solution_]: ...
    _createFromXmlResource_0__Solution_ = typing.TypeVar('_createFromXmlResource_0__Solution_')  # <Solution_>
    _createFromXmlResource_1__Solution_ = typing.TypeVar('_createFromXmlResource_1__Solution_')  # <Solution_>
    @typing.overload
    @staticmethod
    def createFromXmlResource(string: str) -> 'SolverFactory'[_createFromXmlResource_0__Solution_]:
        """
            Reads an XML solver configuration from the classpath and uses that
            :class:`~org.optaplanner.core.config.solver.SolverConfig` to build a
            :class:`~org.optaplanner.core.api.solver.SolverFactory`. The XML root element must be :code:`<solver>`.
        
            Parameters:
                solverConfigResource (:class:`~org.optaplanner.core.api.solver.https:.docs.oracle.com.javase.8.docs.api.java.lang.String?is`): never null, a classpath resource as defined by
                    :meth:`~org.optaplanner.core.api.solver.https:.docs.oracle.com.javase.8.docs.api.java.lang.ClassLoader.html?is`
        
            Returns:
                never null, subsequent changes to the config have no effect on the returned instance
        
            As defined by :meth:`~org.optaplanner.core.api.solver.SolverFactory.createFromXmlResource`.
        
            Parameters:
                solverConfigResource (:class:`~org.optaplanner.core.api.solver.https:.docs.oracle.com.javase.8.docs.api.java.lang.String?is`): never null, a classpath resource as defined by
                    :meth:`~org.optaplanner.core.api.solver.https:.docs.oracle.com.javase.8.docs.api.java.lang.ClassLoader.html?is`
                classLoader (:class:`~org.optaplanner.core.api.solver.https:.docs.oracle.com.javase.8.docs.api.java.lang.ClassLoader?is`): sometimes null, the
                    :class:`~org.optaplanner.core.api.solver.https:.docs.oracle.com.javase.8.docs.api.java.lang.ClassLoader?is` to use for
                    loading all resources and
                    :class:`~org.optaplanner.core.api.solver.https:.docs.oracle.com.javase.8.docs.api.java.lang.Class?is`es, null to use the
                    default :class:`~org.optaplanner.core.api.solver.https:.docs.oracle.com.javase.8.docs.api.java.lang.ClassLoader?is`
        
            Returns:
                never null, subsequent changes to the config have no effect on the returned instance
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def createFromXmlResource(string: str, classLoader: java.lang.ClassLoader) -> 'SolverFactory'[_createFromXmlResource_1__Solution_]: ...

_SolverJob__Solution_ = typing.TypeVar('_SolverJob__Solution_')  # <Solution_>
_SolverJob__ProblemId_ = typing.TypeVar('_SolverJob__ProblemId_')  # <ProblemId_>
class SolverJob(typing.Generic[_SolverJob__Solution_, _SolverJob__ProblemId_]):
    """
    public interface SolverJob<Solution_, ProblemId_>
    
        Represents a :class:`~org.optaplanner.core.api.domain.solution.PlanningSolution` that has been submitted to solve on the
        :class:`~org.optaplanner.core.api.solver.SolverManager`.
    """
    def addProblemChange(self, problemChange: typing.Union[org.optaplanner.core.api.solver.change.ProblemChange[_SolverJob__Solution_], typing.Callable[[_SolverJob__Solution_, org.optaplanner.core.api.solver.change.ProblemChangeDirector], None]]) -> java.util.concurrent.CompletableFuture[None]: ...
    def getFinalBestSolution(self) -> _SolverJob__Solution_: ...
    def getProblemId(self) -> _SolverJob__ProblemId_:
        """
        
            Returns:
                never null, a value given to :meth:`~org.optaplanner.core.api.solver.SolverManager.solve` or
                :meth:`~org.optaplanner.core.api.solver.SolverManager.solveAndListen`
        
        
        """
        ...
    def getSolverStatus(self) -> 'SolverStatus':
        """
            Returns whether the :class:`~org.optaplanner.core.api.solver.Solver` is scheduled to solve, actively solving or not.
        
            Returns :meth:`~org.optaplanner.core.api.solver.SolverStatus.NOT_SOLVING` if the solver already terminated.
        
            Returns:
                never null
        
        
        """
        ...
    def getSolvingDuration(self) -> java.time.Duration:
        """
            Returns the :class:`~org.optaplanner.core.api.solver.https:.docs.oracle.com.javase.8.docs.api.java.time.Duration?is`
            spent solving since the last start. If it hasn't started it yet, it returns
            :meth:`~org.optaplanner.core.api.solver.https:.docs.oracle.com.javase.8.docs.api.java.time.Duration.html?is`. If it
            hasn't ended yet, it returns the time between the last start and now. If it has ended already, it returns the time
            between the last start and the ending.
        
            Returns:
                the :class:`~org.optaplanner.core.api.solver.https:.docs.oracle.com.javase.8.docs.api.java.time.Duration?is` spent
                solving since the last (re)start, at least 0
        
        
        """
        ...
    def isTerminatedEarly(self) -> bool:
        """
        
            Returns:
                true if :meth:`~org.optaplanner.core.api.solver.SolverJob.terminateEarly` has been called since the underlying
                :class:`~org.optaplanner.core.api.solver.Solver` started solving.
        
        
        """
        ...
    def terminateEarly(self) -> None:
        """
            Terminates the solver or cancels the solver job if it hasn't (re)started yet.
        
            Does nothing if the solver already terminated.
        
            Waits for the termination or cancellation to complete before returning. During termination, a
            :code:`bestSolutionConsumer` could still be called (on a consumer thread), before this method returns.
        
        """
        ...

_SolverManager__Solution_ = typing.TypeVar('_SolverManager__Solution_')  # <Solution_>
_SolverManager__ProblemId_ = typing.TypeVar('_SolverManager__ProblemId_')  # <ProblemId_>
class SolverManager(java.lang.AutoCloseable, typing.Generic[_SolverManager__Solution_, _SolverManager__ProblemId_]):
    """
    public interface SolverManager<Solution_, ProblemId_> extends :class:`~org.optaplanner.core.api.solver.https:.docs.oracle.com.javase.8.docs.api.java.lang.AutoCloseable?is`
    
        A SolverManager solves multiple planning problems of the same domain, asynchronously without blocking the calling
        thread.
    
        To create a SolverManager, use :meth:`~org.optaplanner.core.api.solver.SolverManager.create`. To solve a planning
        problem, call :meth:`~org.optaplanner.core.api.solver.SolverManager.solve` or
        :meth:`~org.optaplanner.core.api.solver.SolverManager.solveAndListen`.
    
        These methods are thread-safe unless explicitly stated otherwise.
    
        Internally a SolverManager manages a thread pool of solver threads (which call
        :meth:`~org.optaplanner.core.api.solver.Solver.solve`) and consumer threads (to handle the
        :class:`~org.optaplanner.core.api.solver.event.BestSolutionChangedEvent`s).
    
        To learn more about problem change semantics, please refer to the
        :class:`~org.optaplanner.core.api.solver.change.ProblemChange` Javadoc.
    """
    def addProblemChange(self, problemId_: _SolverManager__ProblemId_, problemChange: typing.Union[org.optaplanner.core.api.solver.change.ProblemChange[_SolverManager__Solution_], typing.Callable[[_SolverManager__Solution_, org.optaplanner.core.api.solver.change.ProblemChangeDirector], None]]) -> java.util.concurrent.CompletableFuture[None]: ...
    def close(self) -> None:
        """
            Terminates all solvers, cancels all solver jobs that haven't (re)started yet and discards all queued
            :class:`~org.optaplanner.core.api.solver.change.ProblemChange`s. Releases all thread pool resources.
        
            No new planning problems can be submitted after calling this method.
        
            Specified by:
                :meth:`~org.optaplanner.core.api.solver.https:.docs.oracle.com.javase.8.docs.api.java.lang.AutoCloseable.html?is` in
                interface :class:`~org.optaplanner.core.api.solver.https:.docs.oracle.com.javase.8.docs.api.java.lang.AutoCloseable?is`
        
        
        """
        ...
    _create_0__Solution_ = typing.TypeVar('_create_0__Solution_')  # <Solution_>
    _create_0__ProblemId_ = typing.TypeVar('_create_0__ProblemId_')  # <ProblemId_>
    _create_1__Solution_ = typing.TypeVar('_create_1__Solution_')  # <Solution_>
    _create_1__ProblemId_ = typing.TypeVar('_create_1__ProblemId_')  # <ProblemId_>
    _create_2__Solution_ = typing.TypeVar('_create_2__Solution_')  # <Solution_>
    _create_2__ProblemId_ = typing.TypeVar('_create_2__ProblemId_')  # <ProblemId_>
    _create_3__Solution_ = typing.TypeVar('_create_3__Solution_')  # <Solution_>
    _create_3__ProblemId_ = typing.TypeVar('_create_3__ProblemId_')  # <ProblemId_>
    @typing.overload
    @staticmethod
    def create(solverFactory: SolverFactory[_create_0__Solution_]) -> 'SolverManager'[_create_0__Solution_, _create_0__ProblemId_]:
        """
            Use a :class:`~org.optaplanner.core.config.solver.SolverConfig` to build a
            :class:`~org.optaplanner.core.api.solver.SolverManager`.
        
            When using :class:`~org.optaplanner.core.api.score.ScoreManager` too, use
            :meth:`~org.optaplanner.core.api.solver.SolverManager.create` instead so they reuse the same
            :class:`~org.optaplanner.core.api.solver.SolverFactory` instance.
        
            Parameters:
                solverConfig (:class:`~org.optaplanner.core.config.solver.SolverConfig`): never null
        
            Returns:
                never null
        
            Use a :class:`~org.optaplanner.core.config.solver.SolverConfig` and a
            :class:`~org.optaplanner.core.config.solver.SolverManagerConfig` to build a
            :class:`~org.optaplanner.core.api.solver.SolverManager`.
        
            When using :class:`~org.optaplanner.core.api.score.ScoreManager` too, use
            :meth:`~org.optaplanner.core.api.solver.SolverManager.create` instead so they reuse the same
            :class:`~org.optaplanner.core.api.solver.SolverFactory` instance.
        
            Parameters:
                solverConfig (:class:`~org.optaplanner.core.config.solver.SolverConfig`): never null
                solverManagerConfig (:class:`~org.optaplanner.core.config.solver.SolverManagerConfig`): never null
        
            Returns:
                never null
        
            Use a :class:`~org.optaplanner.core.api.solver.SolverFactory` to build a
            :class:`~org.optaplanner.core.api.solver.SolverManager`.
        
            Parameters:
                solverFactory (:class:`~org.optaplanner.core.api.solver.SolverFactory`<Solution_> solverFactory): never null
        
            Returns:
                never null
        
        """
        ...
    @typing.overload
    @staticmethod
    def create(solverFactory: SolverFactory[_create_1__Solution_], solverManagerConfig: org.optaplanner.core.config.solver.SolverManagerConfig) -> 'SolverManager'[_create_1__Solution_, _create_1__ProblemId_]:
        """
            Use a :class:`~org.optaplanner.core.api.solver.SolverFactory` and a
            :class:`~org.optaplanner.core.config.solver.SolverManagerConfig` to build a
            :class:`~org.optaplanner.core.api.solver.SolverManager`.
        
            Parameters:
                solverFactory (:class:`~org.optaplanner.core.api.solver.SolverFactory`<Solution_> solverFactory): never null
                solverManagerConfig (:class:`~org.optaplanner.core.config.solver.SolverManagerConfig`): never null
        
            Returns:
                never null
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def create(solverConfig: org.optaplanner.core.config.solver.SolverConfig) -> 'SolverManager'[_create_2__Solution_, _create_2__ProblemId_]: ...
    @typing.overload
    @staticmethod
    def create(solverConfig: org.optaplanner.core.config.solver.SolverConfig, solverManagerConfig: org.optaplanner.core.config.solver.SolverManagerConfig) -> 'SolverManager'[_create_3__Solution_, _create_3__ProblemId_]: ...
    def getSolverStatus(self, problemId_: _SolverManager__ProblemId_) -> 'SolverStatus':
        """
            Returns if the :class:`~org.optaplanner.core.api.solver.Solver` is scheduled to solve, actively solving or not.
        
            Returns :meth:`~org.optaplanner.core.api.solver.SolverStatus.NOT_SOLVING` if the solver already terminated or if the
            problemId was never added. To distinguish between both cases, use
            :meth:`~org.optaplanner.core.api.solver.SolverJob.getSolverStatus` instead. Here, that distinction is not supported
            because it would cause a memory leak.
        
            Parameters:
                problemId (:class:`~org.optaplanner.core.api.solver.SolverManager`): never null, a value given to :meth:`~org.optaplanner.core.api.solver.SolverManager.solve` or
                    :meth:`~org.optaplanner.core.api.solver.SolverManager.solveAndListen`
        
            Returns:
                never null
        
        
        """
        ...
    @typing.overload
    def solve(self, problemId_: _SolverManager__ProblemId_, function: typing.Union[java.util.function.Function[_SolverManager__ProblemId_, _SolverManager__Solution_], typing.Callable[[_SolverManager__ProblemId_], _SolverManager__Solution_]], consumer: typing.Union[java.util.function.Consumer[_SolverManager__Solution_], typing.Callable[[_SolverManager__Solution_], None]], biConsumer: typing.Union[java.util.function.BiConsumer[_SolverManager__ProblemId_, java.lang.Throwable], typing.Callable[[_SolverManager__ProblemId_, java.lang.Throwable], None]]) -> SolverJob[_SolverManager__Solution_, _SolverManager__ProblemId_]: ...
    @typing.overload
    def solve(self, problemId_: _SolverManager__ProblemId_, solution_: _SolverManager__Solution_) -> SolverJob[_SolverManager__Solution_, _SolverManager__ProblemId_]: ...
    @typing.overload
    def solve(self, problemId_: _SolverManager__ProblemId_, solution_: _SolverManager__Solution_, consumer: typing.Union[java.util.function.Consumer[_SolverManager__Solution_], typing.Callable[[_SolverManager__Solution_], None]]) -> SolverJob[_SolverManager__Solution_, _SolverManager__ProblemId_]: ...
    @typing.overload
    def solve(self, problemId_: _SolverManager__ProblemId_, solution_: _SolverManager__Solution_, consumer: typing.Union[java.util.function.Consumer[_SolverManager__Solution_], typing.Callable[[_SolverManager__Solution_], None]], biConsumer: typing.Union[java.util.function.BiConsumer[_SolverManager__ProblemId_, java.lang.Throwable], typing.Callable[[_SolverManager__ProblemId_, java.lang.Throwable], None]]) -> SolverJob[_SolverManager__Solution_, _SolverManager__ProblemId_]: ...
    @typing.overload
    def solve(self, problemId_: _SolverManager__ProblemId_, function: typing.Union[java.util.function.Function[_SolverManager__ProblemId_, _SolverManager__Solution_], typing.Callable[[_SolverManager__ProblemId_], _SolverManager__Solution_]], consumer: typing.Union[java.util.function.Consumer[_SolverManager__Solution_], typing.Callable[[_SolverManager__Solution_], None]]) -> SolverJob[_SolverManager__Solution_, _SolverManager__ProblemId_]: ...
    @typing.overload
    def solveAndListen(self, problemId_: _SolverManager__ProblemId_, function: typing.Union[java.util.function.Function[_SolverManager__ProblemId_, _SolverManager__Solution_], typing.Callable[[_SolverManager__ProblemId_], _SolverManager__Solution_]], consumer: typing.Union[java.util.function.Consumer[_SolverManager__Solution_], typing.Callable[[_SolverManager__Solution_], None]], consumer2: typing.Union[java.util.function.Consumer[_SolverManager__Solution_], typing.Callable[[_SolverManager__Solution_], None]], biConsumer: typing.Union[java.util.function.BiConsumer[_SolverManager__ProblemId_, java.lang.Throwable], typing.Callable[[_SolverManager__ProblemId_, java.lang.Throwable], None]]) -> SolverJob[_SolverManager__Solution_, _SolverManager__ProblemId_]: ...
    @typing.overload
    def solveAndListen(self, problemId_: _SolverManager__ProblemId_, function: typing.Union[java.util.function.Function[_SolverManager__ProblemId_, _SolverManager__Solution_], typing.Callable[[_SolverManager__ProblemId_], _SolverManager__Solution_]], consumer: typing.Union[java.util.function.Consumer[_SolverManager__Solution_], typing.Callable[[_SolverManager__Solution_], None]]) -> SolverJob[_SolverManager__Solution_, _SolverManager__ProblemId_]: ...
    @typing.overload
    def solveAndListen(self, problemId_: _SolverManager__ProblemId_, function: typing.Union[java.util.function.Function[_SolverManager__ProblemId_, _SolverManager__Solution_], typing.Callable[[_SolverManager__ProblemId_], _SolverManager__Solution_]], consumer: typing.Union[java.util.function.Consumer[_SolverManager__Solution_], typing.Callable[[_SolverManager__Solution_], None]], biConsumer: typing.Union[java.util.function.BiConsumer[_SolverManager__ProblemId_, java.lang.Throwable], typing.Callable[[_SolverManager__ProblemId_, java.lang.Throwable], None]]) -> SolverJob[_SolverManager__Solution_, _SolverManager__ProblemId_]: ...
    def terminateEarly(self, problemId_: _SolverManager__ProblemId_) -> None:
        """
            Terminates the solver or cancels the solver job if it hasn't (re)started yet.
        
            Does nothing if the solver already terminated or the problemId was never added. To distinguish between both cases, use
            :meth:`~org.optaplanner.core.api.solver.SolverJob.terminateEarly` instead. Here, that distinction is not supported
            because it would cause a memory leak.
        
            Waits for the termination or cancellation to complete before returning. During termination, a
            :code:`bestSolutionConsumer` could still be called (on a consumer thread), before this method returns.
        
            Parameters:
                problemId (:class:`~org.optaplanner.core.api.solver.SolverManager`): never null, a value given to :meth:`~org.optaplanner.core.api.solver.SolverManager.solve` or
                    :meth:`~org.optaplanner.core.api.solver.SolverManager.solveAndListen`
        
        
        """
        ...

class SolverStatus(java.lang.Enum['SolverStatus']):
    """
    public enum SolverStatus extends :class:`~org.optaplanner.core.api.solver.https:.docs.oracle.com.javase.8.docs.api.java.lang.Enum?is`<:class:`~org.optaplanner.core.api.solver.SolverStatus`>
    
        The status of :class:`~org.optaplanner.core.api.domain.solution.PlanningSolution` submitted to the
        :class:`~org.optaplanner.core.api.solver.SolverManager`. Retrieve this status with
        :meth:`~org.optaplanner.core.api.solver.SolverManager.getSolverStatus` or
        :meth:`~org.optaplanner.core.api.solver.SolverJob.getSolverStatus`.
    """
    SOLVING_SCHEDULED: typing.ClassVar['SolverStatus'] = ...
    SOLVING_ACTIVE: typing.ClassVar['SolverStatus'] = ...
    NOT_SOLVING: typing.ClassVar['SolverStatus'] = ...
    _valueOf_0__T = typing.TypeVar('_valueOf_0__T', bound=java.lang.Enum)  # <T>
    @typing.overload
    @staticmethod
    def valueOf(class_: typing.Type[_valueOf_0__T], string: str) -> _valueOf_0__T: ...
    @typing.overload
    @staticmethod
    def valueOf(string: str) -> 'SolverStatus':
        """
            Returns the enum constant of this type with the specified name. The string must match *exactly* an identifier used to
            declare an enum constant in this type. (Extraneous whitespace characters are not permitted.)
        
            Parameters:
                name (:class:`~org.optaplanner.core.api.solver.https:.docs.oracle.com.javase.8.docs.api.java.lang.String?is`): the name of the enum constant to be returned.
        
            Returns:
                the enum constant with the specified name
        
            Raises:
                :class:`~org.optaplanner.core.api.solver.https:.docs.oracle.com.javase.8.docs.api.java.lang.IllegalArgumentException?is`: if this enum type has no constant with the specified name
                :class:`~org.optaplanner.core.api.solver.https:.docs.oracle.com.javase.8.docs.api.java.lang.NullPointerException?is`: if the argument is null
        
        
        """
        ...
    @staticmethod
    def values() -> typing.List['SolverStatus']:
        """
            Returns an array containing the constants of this enum type, in the order they are declared. This method may be used to
            iterate over the constants as follows:
        
            .. code-block: java
            
            for (SolverStatus c : SolverStatus.values())
                System.out.println(c);
            
        
            Returns:
                an array containing the constants of this enum type, in the order they are declared
        
        
        """
        ...


class __module_protocol__(typing.Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.optaplanner.core.api.solver")``.

    ProblemFactChange: typing.Type[ProblemFactChange]
    Solver: typing.Type[Solver]
    SolverFactory: typing.Type[SolverFactory]
    SolverJob: typing.Type[SolverJob]
    SolverManager: typing.Type[SolverManager]
    SolverStatus: typing.Type[SolverStatus]
    change: org.optaplanner.core.api.solver.change.__module_protocol__
    event: org.optaplanner.core.api.solver.event.__module_protocol__
