import java.util
import org.optaplanner.core.api.score
import org.optaplanner.core.api.score.constraint
import typing



_EasyScoreCalculator__Solution_ = typing.TypeVar('_EasyScoreCalculator__Solution_')  # <Solution_>
_EasyScoreCalculator__Score_ = typing.TypeVar('_EasyScoreCalculator__Score_', bound=org.optaplanner.core.api.score.Score)  # <Score_>
class EasyScoreCalculator(typing.Generic[_EasyScoreCalculator__Solution_, _EasyScoreCalculator__Score_]):
    """
    public interface EasyScoreCalculator<Solution_, Score_ extends :class:`~org.optaplanner.core.api.score.Score`<Score_>>
    
        Used for easy java :class:`~org.optaplanner.core.api.score.Score` calculation. This is non-incremental calculation,
        which is slow.
    
        An implementation must be stateless.
    """
    def calculateScore(self, solution_: _EasyScoreCalculator__Solution_) -> _EasyScoreCalculator__Score_:
        """
            This method is only called if the :class:`~org.optaplanner.core.api.score.Score` cannot be predicted. The
            :class:`~org.optaplanner.core.api.score.Score` can be predicted for example after an undo move.
        
            Parameters:
                solution (:class:`~org.optaplanner.core.api.score.calculator.EasyScoreCalculator`): never null
        
            Returns:
                never null
        
        
        """
        ...

_IncrementalScoreCalculator__Solution_ = typing.TypeVar('_IncrementalScoreCalculator__Solution_')  # <Solution_>
_IncrementalScoreCalculator__Score_ = typing.TypeVar('_IncrementalScoreCalculator__Score_', bound=org.optaplanner.core.api.score.Score)  # <Score_>
class IncrementalScoreCalculator(typing.Generic[_IncrementalScoreCalculator__Solution_, _IncrementalScoreCalculator__Score_]):
    """
    public interface IncrementalScoreCalculator<Solution_, Score_ extends :class:`~org.optaplanner.core.api.score.Score`<Score_>>
    
        Used for incremental java :class:`~org.optaplanner.core.api.score.Score` calculation. This is much faster than
        :class:`~org.optaplanner.core.api.score.calculator.EasyScoreCalculator` but requires much more code to implement too.
    
        Any implementation is naturally stateful.
    """
    def afterEntityAdded(self, object: typing.Any) -> None:
        """
        
            Parameters:
                entity (:class:`~org.optaplanner.core.api.score.calculator.https:.docs.oracle.com.javase.8.docs.api.java.lang.Object?is`): never null, an instance of a :class:`~org.optaplanner.core.api.domain.entity.PlanningEntity` class
        
        
        """
        ...
    def afterEntityRemoved(self, object: typing.Any) -> None:
        """
        
            Parameters:
                entity (:class:`~org.optaplanner.core.api.score.calculator.https:.docs.oracle.com.javase.8.docs.api.java.lang.Object?is`): never null, an instance of a :class:`~org.optaplanner.core.api.domain.entity.PlanningEntity` class
        
        
        """
        ...
    def afterVariableChanged(self, object: typing.Any, string: str) -> None:
        """
        
            Parameters:
                entity (:class:`~org.optaplanner.core.api.score.calculator.https:.docs.oracle.com.javase.8.docs.api.java.lang.Object?is`): never null, an instance of a :class:`~org.optaplanner.core.api.domain.entity.PlanningEntity` class
                variableName (:class:`~org.optaplanner.core.api.score.calculator.https:.docs.oracle.com.javase.8.docs.api.java.lang.String?is`): never null, either a genuine or shadow :class:`~org.optaplanner.core.api.domain.variable.PlanningVariable`
        
        
        """
        ...
    def beforeEntityAdded(self, object: typing.Any) -> None:
        """
        
            Parameters:
                entity (:class:`~org.optaplanner.core.api.score.calculator.https:.docs.oracle.com.javase.8.docs.api.java.lang.Object?is`): never null, an instance of a :class:`~org.optaplanner.core.api.domain.entity.PlanningEntity` class
        
        
        """
        ...
    def beforeEntityRemoved(self, object: typing.Any) -> None:
        """
        
            Parameters:
                entity (:class:`~org.optaplanner.core.api.score.calculator.https:.docs.oracle.com.javase.8.docs.api.java.lang.Object?is`): never null, an instance of a :class:`~org.optaplanner.core.api.domain.entity.PlanningEntity` class
        
        
        """
        ...
    def beforeVariableChanged(self, object: typing.Any, string: str) -> None:
        """
        
            Parameters:
                entity (:class:`~org.optaplanner.core.api.score.calculator.https:.docs.oracle.com.javase.8.docs.api.java.lang.Object?is`): never null, an instance of a :class:`~org.optaplanner.core.api.domain.entity.PlanningEntity` class
                variableName (:class:`~org.optaplanner.core.api.score.calculator.https:.docs.oracle.com.javase.8.docs.api.java.lang.String?is`): never null, either a genuine or shadow :class:`~org.optaplanner.core.api.domain.variable.PlanningVariable`
        
        
        """
        ...
    def calculateScore(self) -> _IncrementalScoreCalculator__Score_:
        """
            This method is only called if the :class:`~org.optaplanner.core.api.score.Score` cannot be predicted. The
            :class:`~org.optaplanner.core.api.score.Score` can be predicted for example after an undo move.
        
            Returns:
                never null
        
        
        """
        ...
    def resetWorkingSolution(self, solution_: _IncrementalScoreCalculator__Solution_) -> None:
        """
            There are no :meth:`~org.optaplanner.core.api.score.calculator.IncrementalScoreCalculator.beforeEntityAdded` and
            :meth:`~org.optaplanner.core.api.score.calculator.IncrementalScoreCalculator.afterEntityAdded` calls for entities that
            are already present in the workingSolution.
        
            Parameters:
                workingSolution (:class:`~org.optaplanner.core.api.score.calculator.IncrementalScoreCalculator`): never null
        
        
        """
        ...

_ConstraintMatchAwareIncrementalScoreCalculator__Solution_ = typing.TypeVar('_ConstraintMatchAwareIncrementalScoreCalculator__Solution_')  # <Solution_>
_ConstraintMatchAwareIncrementalScoreCalculator__Score_ = typing.TypeVar('_ConstraintMatchAwareIncrementalScoreCalculator__Score_', bound=org.optaplanner.core.api.score.Score)  # <Score_>
class ConstraintMatchAwareIncrementalScoreCalculator(IncrementalScoreCalculator[_ConstraintMatchAwareIncrementalScoreCalculator__Solution_, _ConstraintMatchAwareIncrementalScoreCalculator__Score_], typing.Generic[_ConstraintMatchAwareIncrementalScoreCalculator__Solution_, _ConstraintMatchAwareIncrementalScoreCalculator__Score_]):
    """
    public interface ConstraintMatchAwareIncrementalScoreCalculator<Solution_, Score_ extends :class:`~org.optaplanner.core.api.score.Score`<Score_>> extends :class:`~org.optaplanner.core.api.score.calculator.IncrementalScoreCalculator`<Solution_, Score_>
    
        Allows a :class:`~org.optaplanner.core.api.score.calculator.IncrementalScoreCalculator` to report
        :class:`~org.optaplanner.core.api.score.constraint.ConstraintMatchTotal`s for explaining a score (= which score
        constraints match for how much) and also for score corruption analysis.
    """
    def getConstraintMatchTotals(self) -> java.util.Collection[org.optaplanner.core.api.score.constraint.ConstraintMatchTotal[_ConstraintMatchAwareIncrementalScoreCalculator__Score_]]: ...
    def getIndictmentMap(self) -> java.util.Map[typing.Any, org.optaplanner.core.api.score.constraint.Indictment[_ConstraintMatchAwareIncrementalScoreCalculator__Score_]]: ...
    @typing.overload
    def resetWorkingSolution(self, solution_: _ConstraintMatchAwareIncrementalScoreCalculator__Solution_, boolean: bool) -> None:
        """
            Allows for increased performance because it only tracks if constraintMatchEnabled is true.
        
            Every implementation should call
            :meth:`~org.optaplanner.core.api.score.calculator.ConstraintMatchAwareIncrementalScoreCalculator.resetWorkingSolution`
            and only handle the constraintMatchEnabled parameter specifically (or ignore it).
        
            Parameters:
                workingSolution (:class:`~org.optaplanner.core.api.score.calculator.ConstraintMatchAwareIncrementalScoreCalculator`): never null, to pass to
                    :meth:`~org.optaplanner.core.api.score.calculator.ConstraintMatchAwareIncrementalScoreCalculator.resetWorkingSolution`.
                constraintMatchEnabled (boolean): true if
                    :meth:`~org.optaplanner.core.api.score.calculator.ConstraintMatchAwareIncrementalScoreCalculator.getConstraintMatchTotals`
                    or :meth:`~org.optaplanner.core.api.score.calculator.ConstraintMatchAwareIncrementalScoreCalculator.getIndictmentMap`
                    might be called.
        
        
        """
        ...
    @typing.overload
    def resetWorkingSolution(self, solution_: _ConstraintMatchAwareIncrementalScoreCalculator__Solution_) -> None: ...


class __module_protocol__(typing.Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.optaplanner.core.api.score.calculator")``.

    ConstraintMatchAwareIncrementalScoreCalculator: typing.Type[ConstraintMatchAwareIncrementalScoreCalculator]
    EasyScoreCalculator: typing.Type[EasyScoreCalculator]
    IncrementalScoreCalculator: typing.Type[IncrementalScoreCalculator]
