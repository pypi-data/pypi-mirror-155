import java.util
import org.optaplanner.core.api.score
import org.optaplanner.core.api.solver
import typing



_BestSolutionChangedEvent__Solution_ = typing.TypeVar('_BestSolutionChangedEvent__Solution_')  # <Solution_>
class BestSolutionChangedEvent(java.util.EventObject, typing.Generic[_BestSolutionChangedEvent__Solution_]):
    """
    public class BestSolutionChangedEvent<Solution_> extends :class:`~org.optaplanner.core.api.solver.event.https:.docs.oracle.com.javase.8.docs.api.java.util.EventObject?is`
    
        Delivered when the :class:`~org.optaplanner.core.api.domain.solution.PlanningSolution` changes during solving. Delivered
        in the solver thread (which is the thread that calls :meth:`~org.optaplanner.core.api.solver.Solver.solve`).
    
        Also see:
            :meth:`~serialized`
    """
    def __init__(self, solver: org.optaplanner.core.api.solver.Solver[_BestSolutionChangedEvent__Solution_], long: int, solution_: _BestSolutionChangedEvent__Solution_, score: org.optaplanner.core.api.score.Score): ...
    def getNewBestScore(self) -> org.optaplanner.core.api.score.Score:
        """
            Returns the :class:`~org.optaplanner.core.api.score.Score` of the
            :meth:`~org.optaplanner.core.api.solver.event.BestSolutionChangedEvent.getNewBestSolution`.
        
            This is useful for generic code, which doesn't know the type of the
            :class:`~org.optaplanner.core.api.domain.solution.PlanningSolution` to retrieve the
            :class:`~org.optaplanner.core.api.score.Score` from the
            :meth:`~org.optaplanner.core.api.solver.event.BestSolutionChangedEvent.getNewBestSolution` easily.
        
            Returns:
                never null, because at this point it's always already calculated
        
        
        """
        ...
    def getNewBestSolution(self) -> _BestSolutionChangedEvent__Solution_:
        """
            Note that:
        
              - In real-time planning, not all :class:`~org.optaplanner.core.api.solver.change.ProblemChange`s might be processed: check
                :meth:`~org.optaplanner.core.api.solver.event.BestSolutionChangedEvent.isEveryProblemFactChangeProcessed`.
              - this :class:`~org.optaplanner.core.api.domain.solution.PlanningSolution` might be uninitialized: check
                :meth:`~org.optaplanner.core.api.score.Score.isSolutionInitialized`.
              - this :class:`~org.optaplanner.core.api.domain.solution.PlanningSolution` might be infeasible: check
                :meth:`~org.optaplanner.core.api.score.Score.isFeasible`.
        
        
            Returns:
                never null
        
        
        """
        ...
    def getTimeMillisSpent(self) -> int:
        """
        
            Returns:
                :code:`>= 0`, the amount of millis spent since the :class:`~org.optaplanner.core.api.solver.Solver` started until
                :meth:`~org.optaplanner.core.api.solver.event.BestSolutionChangedEvent.getNewBestSolution` was found
        
        
        """
        ...
    def isEveryProblemChangeProcessed(self) -> bool:
        """
        
            Returns:
                As defined by :meth:`~org.optaplanner.core.api.solver.Solver.isEveryProblemChangeProcessed`
        
            Also see:
                :meth:`~org.optaplanner.core.api.solver.Solver.isEveryProblemChangeProcessed`
        
        
        """
        ...
    def isEveryProblemFactChangeProcessed(self) -> bool: ...

_SolverEventListener__Solution_ = typing.TypeVar('_SolverEventListener__Solution_')  # <Solution_>
class SolverEventListener(java.util.EventListener, typing.Generic[_SolverEventListener__Solution_]):
    """
    :class:`~org.optaplanner.core.api.solver.event.https:.docs.oracle.com.javase.8.docs.api.java.lang.FunctionalInterface?is` public interface SolverEventListener<Solution_> extends :class:`~org.optaplanner.core.api.solver.event.https:.docs.oracle.com.javase.8.docs.api.java.util.EventListener?is`
    """
    def bestSolutionChanged(self, bestSolutionChangedEvent: BestSolutionChangedEvent[_SolverEventListener__Solution_]) -> None: ...


class __module_protocol__(typing.Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.optaplanner.core.api.solver.event")``.

    BestSolutionChangedEvent: typing.Type[BestSolutionChangedEvent]
    SolverEventListener: typing.Type[SolverEventListener]
