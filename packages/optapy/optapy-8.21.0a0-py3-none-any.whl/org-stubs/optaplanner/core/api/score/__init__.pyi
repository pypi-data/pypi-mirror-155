import java.io
import java.lang
import java.util
import org.optaplanner.core.api.score.buildin
import org.optaplanner.core.api.score.calculator
import org.optaplanner.core.api.score.constraint
import org.optaplanner.core.api.score.director
import org.optaplanner.core.api.score.holder
import org.optaplanner.core.api.score.stream
import org.optaplanner.core.api.solver
import typing



_Score__Score_ = typing.TypeVar('_Score__Score_', bound='Score')  # <Score_>
class Score(java.lang.Comparable[_Score__Score_], typing.Generic[_Score__Score_]):
    """
    public interface Score<Score_ extends Score<Score_>> extends :class:`~org.optaplanner.core.api.score.https:.docs.oracle.com.javase.8.docs.api.java.lang.Comparable?is`<Score_>
    
        A Score is result of the score function (AKA fitness function) on a single possible solution.
    
        Implementations must be immutable.
    
        Implementations are allowed to optionally implement Pareto comparison and therefore slightly violate the transitive
        requirement of
        :meth:`~org.optaplanner.core.api.score.https:.docs.oracle.com.javase.8.docs.api.java.lang.Comparable.html?is`.
    
        An implementation must extend :class:`~org.optaplanner.core.api.score.AbstractScore` to ensure backwards compatibility
        in future versions.
    
        Also see:
            :class:`~org.optaplanner.core.api.score.AbstractScore`,
            :class:`~org.optaplanner.core.api.score.buildin.hardsoft.HardSoftScore`
    """
    def add(self, score_: _Score__Score_) -> _Score__Score_:
        """
            Returns a Score whose value is (this + addend).
        
            Parameters:
                addend (:class:`~org.optaplanner.core.api.score.Score`): value to be added to this Score
        
            Returns:
                this + addend
        
        
        """
        ...
    def divide(self, double: float) -> _Score__Score_:
        """
            Returns a Score whose value is (this / divisor). When rounding is needed, it should be floored (as defined by
            :meth:`~org.optaplanner.core.api.score.https:.docs.oracle.com.javase.8.docs.api.java.lang.Math.html?is`).
        
            If the implementation has a scale/precision, then the unspecified scale/precision of the double divisor should have no
            impact on the returned scale/precision.
        
            Parameters:
                divisor (double): value by which this Score is to be divided
        
            Returns:
                this / divisor
        
        
        """
        ...
    def getInitScore(self) -> int:
        """
            The init score is the negative of the number of uninitialized genuine planning variables. If it's 0 (which it usually
            is), the :class:`~org.optaplanner.core.api.domain.solution.PlanningSolution` is fully initialized and the score's
            :meth:`~org.optaplanner.core.api.score.https:.docs.oracle.com.javase.8.docs.api.java.lang.Object.html?is` does not
            mention it.
        
            During :meth:`~org.optaplanner.core.api.score.https:.docs.oracle.com.javase.8.docs.api.java.lang.Comparable.html?is`,
            it's even more important than the hard score: if you don't want this behaviour, read about overconstrained planning in
            the reference manual.
        
            Returns:
                higher is better, always negative (except in statistical calculations), 0 if all planning variables are initialized
        
        
        """
        ...
    def isFeasible(self) -> bool:
        """
            A :class:`~org.optaplanner.core.api.domain.solution.PlanningSolution` is feasible if it has no broken hard constraints
            and :meth:`~org.optaplanner.core.api.score.Score.isSolutionInitialized` is true. Simple scores
            (:class:`~org.optaplanner.core.api.score.buildin.simple.SimpleScore`,
            :class:`~org.optaplanner.core.api.score.buildin.simplelong.SimpleLongScore`,
            :class:`~org.optaplanner.core.api.score.buildin.simplebigdecimal.SimpleBigDecimalScore`) are always feasible, if their
            :meth:`~org.optaplanner.core.api.score.Score.getInitScore` is 0.
        
            Returns:
                true if the hard score is 0 or higher and the :meth:`~org.optaplanner.core.api.score.Score.getInitScore` is 0.
        
        
        """
        ...
    def isSolutionInitialized(self) -> bool:
        """
            Checks if the :class:`~org.optaplanner.core.api.domain.solution.PlanningSolution` of this score was fully initialized
            when it was calculated.
        
            Returns:
                true if :meth:`~org.optaplanner.core.api.score.Score.getInitScore` is 0
        
        
        """
        ...
    def isZero(self) -> bool:
        """
        
            Returns:
                true when this :code:`is equal to` :meth:`~org.optaplanner.core.api.score.Score.zero`.
        
        
        """
        ...
    def multiply(self, double: float) -> _Score__Score_:
        """
            Returns a Score whose value is (this * multiplicand). When rounding is needed, it should be floored (as defined by
            :meth:`~org.optaplanner.core.api.score.https:.docs.oracle.com.javase.8.docs.api.java.lang.Math.html?is`).
        
            If the implementation has a scale/precision, then the unspecified scale/precision of the double multiplicand should have
            no impact on the returned scale/precision.
        
            Parameters:
                multiplicand (double): value to be multiplied by this Score.
        
            Returns:
                this * multiplicand
        
        
        """
        ...
    def negate(self) -> _Score__Score_:
        """
            Returns a Score whose value is (- this).
        
            Returns:
                - this
        
        
        """
        ...
    def power(self, double: float) -> _Score__Score_:
        """
            Returns a Score whose value is (this ^ exponent). When rounding is needed, it should be floored (as defined by
            :meth:`~org.optaplanner.core.api.score.https:.docs.oracle.com.javase.8.docs.api.java.lang.Math.html?is`).
        
            If the implementation has a scale/precision, then the unspecified scale/precision of the double exponent should have no
            impact on the returned scale/precision.
        
            Parameters:
                exponent (double): value by which this Score is to be powered
        
            Returns:
                this ^ exponent
        
        
        """
        ...
    def subtract(self, score_: _Score__Score_) -> _Score__Score_:
        """
            Returns a Score whose value is (this - subtrahend).
        
            Parameters:
                subtrahend (:class:`~org.optaplanner.core.api.score.Score`): value to be subtracted from this Score
        
            Returns:
                this - subtrahend, rounded as necessary
        
        
        """
        ...
    def toLevelDoubles(self) -> typing.List[float]:
        """
            As defined by :meth:`~org.optaplanner.core.api.score.Score.toLevelNumbers`, only returns double[] instead of Number[].
        
            Returns:
                never null
        
        
        """
        ...
    def toLevelNumbers(self) -> typing.List[java.lang.Number]:
        """
            Returns an array of numbers representing the Score. Each number represents 1 score level. A greater score level uses a
            lower array index than a lesser score level.
        
            When rounding is needed, each rounding should be floored (as defined by
            :meth:`~org.optaplanner.core.api.score.https:.docs.oracle.com.javase.8.docs.api.java.lang.Math.html?is`). The length of
            the returned array must be stable for a specific :class:`~org.optaplanner.core.api.score.Score` implementation.
        
            For example: :code:`-0hard/-7soft` returns :code:`new int{-0, -7}`
        
            The level numbers do not contain the :meth:`~org.optaplanner.core.api.score.Score.getInitScore`. For example:
            :code:`-3init/-0hard/-7soft` also returns :code:`new int{-0, -7}`
        
            Returns:
                never null
        
        
        """
        ...
    def toShortString(self) -> str:
        """
            Like :meth:`~org.optaplanner.core.api.score.https:.docs.oracle.com.javase.8.docs.api.java.lang.Object.html?is`, but
            trims score levels which have a zero weight. For example 0hard/-258soft returns -258soft.
        
            Do not use this format to persist information as text, use
            :meth:`~org.optaplanner.core.api.score.https:.docs.oracle.com.javase.8.docs.api.java.lang.Object.html?is` instead, so it
            can be parsed reliably.
        
            Returns:
                never null
        
        
        """
        ...
    def withInitScore(self, int: int) -> _Score__Score_:
        """
            For example :code:`0hard/-8soft` with :code:`-7` returns :code:`-7init/0hard/-8soft`.
        
            Parameters:
                newInitScore (int): always negative (except in statistical calculations), 0 if all planning variables are initialized
        
            Returns:
                equals score except that :meth:`~org.optaplanner.core.api.score.Score.getInitScore` is set to :code:`newInitScore`
        
        
        """
        ...
    def zero(self) -> _Score__Score_:
        """
            Returns a Score, all levels of which are zero.
        
            Returns:
                never null
        
        
        """
        ...

_ScoreExplanation__Solution_ = typing.TypeVar('_ScoreExplanation__Solution_')  # <Solution_>
_ScoreExplanation__Score_ = typing.TypeVar('_ScoreExplanation__Score_', bound=Score)  # <Score_>
class ScoreExplanation(typing.Generic[_ScoreExplanation__Solution_, _ScoreExplanation__Score_]):
    """
    public interface ScoreExplanation<Solution_, Score_ extends :class:`~org.optaplanner.core.api.score.Score`<Score_>>
    
        Build by :meth:`~org.optaplanner.core.api.score.ScoreManager.explainScore` to hold
        :class:`~org.optaplanner.core.api.score.constraint.ConstraintMatchTotal`s and
        :class:`~org.optaplanner.core.api.score.constraint.Indictment`s necessary to explain the quality of a particular
        :class:`~org.optaplanner.core.api.score.Score`.
    """
    def getConstraintMatchTotalMap(self) -> java.util.Map[str, org.optaplanner.core.api.score.constraint.ConstraintMatchTotal[_ScoreExplanation__Score_]]: ...
    def getIndictmentMap(self) -> java.util.Map[typing.Any, org.optaplanner.core.api.score.constraint.Indictment[_ScoreExplanation__Score_]]: ...
    def getScore(self) -> _ScoreExplanation__Score_:
        """
            Return the :class:`~org.optaplanner.core.api.score.Score` being explained. If the specific
            :class:`~org.optaplanner.core.api.score.Score` type used by the
            :class:`~org.optaplanner.core.api.domain.solution.PlanningSolution` is required, call
            :meth:`~org.optaplanner.core.api.score.ScoreExplanation.getSolution` and retrieve it from there.
        
            Returns:
                never null
        
        
        """
        ...
    def getSolution(self) -> _ScoreExplanation__Solution_:
        """
            Retrieve the :class:`~org.optaplanner.core.api.domain.solution.PlanningSolution` that the score being explained comes
            from.
        
            Returns:
                never null
        
        
        """
        ...
    def getSummary(self) -> str:
        """
            Returns a diagnostic text that explains the :class:`~org.optaplanner.core.api.score.Score` through the
            :class:`~org.optaplanner.core.api.score.constraint.ConstraintMatch` API to identify which constraints or planning
            entities cause that score quality. In case of an :meth:`~org.optaplanner.core.api.score.Score.isFeasible` solution, this
            can help diagnose the cause of that.
        
            Do not parse this string. Instead, to provide this information in a UI or a service, use
            :meth:`~org.optaplanner.core.api.score.ScoreExplanation.getConstraintMatchTotalMap` and
            :meth:`~org.optaplanner.core.api.score.ScoreExplanation.getIndictmentMap` and convert those into a domain specific API.
        
            Returns:
                never null
        
        
        """
        ...

_ScoreManager__Solution_ = typing.TypeVar('_ScoreManager__Solution_')  # <Solution_>
_ScoreManager__Score_ = typing.TypeVar('_ScoreManager__Score_', bound=Score)  # <Score_>
class ScoreManager(typing.Generic[_ScoreManager__Solution_, _ScoreManager__Score_]):
    """
    public interface ScoreManager<Solution_, Score_ extends :class:`~org.optaplanner.core.api.score.Score`<Score_>>
    
        A stateless service to help calculate :class:`~org.optaplanner.core.api.score.Score`,
        :class:`~org.optaplanner.core.api.score.constraint.ConstraintMatchTotal`,
        :class:`~org.optaplanner.core.api.score.constraint.Indictment`, etc.
    
        To create a ScoreManager, use :meth:`~org.optaplanner.core.api.score.ScoreManager.create`.
    
        These methods are thread-safe unless explicitly stated otherwise.
    """
    _create_0__Solution_ = typing.TypeVar('_create_0__Solution_')  # <Solution_>
    _create_0__Score_ = typing.TypeVar('_create_0__Score_', bound=Score)  # <Score_>
    _create_1__Solution_ = typing.TypeVar('_create_1__Solution_')  # <Solution_>
    _create_1__Score_ = typing.TypeVar('_create_1__Score_', bound=Score)  # <Score_>
    _create_1__ProblemId_ = typing.TypeVar('_create_1__ProblemId_')  # <ProblemId_>
    @typing.overload
    @staticmethod
    def create(solverFactory: org.optaplanner.core.api.solver.SolverFactory[_create_0__Solution_]) -> 'ScoreManager'[_create_0__Solution_, _create_0__Score_]:
        """
            Uses a :class:`~org.optaplanner.core.api.solver.SolverFactory` to build a
            :class:`~org.optaplanner.core.api.score.ScoreManager`.
        
            Parameters:
                solverFactory (:class:`~org.optaplanner.core.api.solver.SolverFactory`<Solution_> solverFactory): never null
        
            Returns:
                never null
        
        """
        ...
    @typing.overload
    @staticmethod
    def create(solverManager: org.optaplanner.core.api.solver.SolverManager[_create_1__Solution_, _create_1__ProblemId_]) -> 'ScoreManager'[_create_1__Solution_, _create_1__Score_]:
        """
            Uses a :class:`~org.optaplanner.core.api.solver.SolverManager` to build a
            :class:`~org.optaplanner.core.api.score.ScoreManager`.
        
            Parameters:
                solverManager (:class:`~org.optaplanner.core.api.solver.SolverManager`<Solution_, ProblemId_> solverManager): never null
        
            Returns:
                never null
        
        
        """
        ...
    def explainScore(self, solution_: _ScoreManager__Solution_) -> ScoreExplanation[_ScoreManager__Solution_, _ScoreManager__Score_]: ...
    def getSummary(self, solution_: _ScoreManager__Solution_) -> str:
        """
            Returns a diagnostic text that explains the solution through the
            :class:`~org.optaplanner.core.api.score.constraint.ConstraintMatch` API to identify which constraints or planning
            entities cause that score quality. In case of an :meth:`~org.optaplanner.core.api.score.Score.isFeasible` solution, this
            can help diagnose the cause of that.
        
            Do not parse this string. Instead, to provide this information in a UI or a service, use
            :meth:`~org.optaplanner.core.api.score.ScoreManager.explainScore` to retrieve
            :meth:`~org.optaplanner.core.api.score.ScoreExplanation.getConstraintMatchTotalMap` and
            :meth:`~org.optaplanner.core.api.score.ScoreExplanation.getIndictmentMap` and convert those into a domain specific API.
        
            Parameters:
                solution (:class:`~org.optaplanner.core.api.score.ScoreManager`): never null
        
            Returns:
                null if :meth:`~org.optaplanner.core.api.score.ScoreManager.updateScore` returns null with the same solution
        
            Raises:
                :class:`~org.optaplanner.core.api.score.https:.docs.oracle.com.javase.8.docs.api.java.lang.IllegalStateException?is`: when constraint matching is disabled or not supported by the underlying score calculator, such as
                    :class:`~org.optaplanner.core.api.score.calculator.EasyScoreCalculator`.
        
        
        """
        ...
    def updateScore(self, solution_: _ScoreManager__Solution_) -> _ScoreManager__Score_:
        """
            Calculates the :class:`~org.optaplanner.core.api.score.Score` of a
            :class:`~org.optaplanner.core.api.domain.solution.PlanningSolution` and updates its
            :class:`~org.optaplanner.core.api.domain.solution.PlanningScore` member.
        
            Parameters:
                solution (:class:`~org.optaplanner.core.api.score.ScoreManager`): never null
        
        
        """
        ...

_AbstractScore__Score_ = typing.TypeVar('_AbstractScore__Score_', bound='AbstractScore')  # <Score_>
class AbstractScore(Score[_AbstractScore__Score_], java.io.Serializable, typing.Generic[_AbstractScore__Score_]):
    """
    public abstract class AbstractScore<Score_ extends AbstractScore<Score_>> extends :class:`~org.optaplanner.core.api.score.https:.docs.oracle.com.javase.8.docs.api.java.lang.Object?is` implements :class:`~org.optaplanner.core.api.score.Score`<Score_>, :class:`~org.optaplanner.core.api.score.https:.docs.oracle.com.javase.8.docs.api.java.io.Serializable?is`
    
        Abstract superclass for :class:`~org.optaplanner.core.api.score.Score`.
    
        Subclasses must be immutable.
    
        Also see:
            :class:`~org.optaplanner.core.api.score.Score`, :class:`~org.optaplanner.core.api.score.buildin.hardsoft.HardSoftScore`,
            :meth:`~serialized`
    """
    def getInitScore(self) -> int:
        """
            Description copied from interface: :meth:`~org.optaplanner.core.api.score.Score.getInitScore`
            The init score is the negative of the number of uninitialized genuine planning variables. If it's 0 (which it usually
            is), the :class:`~org.optaplanner.core.api.domain.solution.PlanningSolution` is fully initialized and the score's
            :meth:`~org.optaplanner.core.api.score.https:.docs.oracle.com.javase.8.docs.api.java.lang.Object.html?is` does not
            mention it.
        
            During :meth:`~org.optaplanner.core.api.score.https:.docs.oracle.com.javase.8.docs.api.java.lang.Comparable.html?is`,
            it's even more important than the hard score: if you don't want this behaviour, read about overconstrained planning in
            the reference manual.
        
            Specified by:
                :meth:`~org.optaplanner.core.api.score.Score.getInitScore` in interface :class:`~org.optaplanner.core.api.score.Score`
        
            Returns:
                higher is better, always negative (except in statistical calculations), 0 if all planning variables are initialized
        
        
        """
        ...
    def isSolutionInitialized(self) -> bool:
        """
            Description copied from interface: :meth:`~org.optaplanner.core.api.score.Score.isSolutionInitialized`
            Checks if the :class:`~org.optaplanner.core.api.domain.solution.PlanningSolution` of this score was fully initialized
            when it was calculated.
        
            Specified by:
                :meth:`~org.optaplanner.core.api.score.Score.isSolutionInitialized` in
                interface :class:`~org.optaplanner.core.api.score.Score`
        
            Returns:
                true if :meth:`~org.optaplanner.core.api.score.Score.getInitScore` is 0
        
        
        """
        ...

_AbstractBendableScore__Score_ = typing.TypeVar('_AbstractBendableScore__Score_', bound='AbstractBendableScore')  # <Score_>
class AbstractBendableScore(AbstractScore[_AbstractBendableScore__Score_], typing.Generic[_AbstractBendableScore__Score_]):
    """
    public abstract class AbstractBendableScore<Score_ extends AbstractBendableScore<Score_>> extends :class:`~org.optaplanner.core.api.score.AbstractScore`<Score_>
    
        Abstract superclass for bendable :class:`~org.optaplanner.core.api.score.Score` types.
    
        Subclasses must be immutable.
    
        Also see:
            :class:`~org.optaplanner.core.api.score.buildin.bendable.BendableScore`, :meth:`~serialized`
    """
    def getHardLevelsSize(self) -> int:
        """
            The sum of this and :meth:`~org.optaplanner.core.api.score.AbstractBendableScore.getSoftLevelsSize` equals
            :meth:`~org.optaplanner.core.api.score.AbstractBendableScore.getLevelsSize`.
        
            Returns:
                :code:`>= 0` and :code:`<` :meth:`~org.optaplanner.core.api.score.AbstractBendableScore.getLevelsSize`
        
        
        """
        ...
    def getLevelsSize(self) -> int:
        """
        
            Returns:
                :meth:`~org.optaplanner.core.api.score.AbstractBendableScore.getHardLevelsSize` +
                :meth:`~org.optaplanner.core.api.score.AbstractBendableScore.getSoftLevelsSize`
        
        
        """
        ...
    def getSoftLevelsSize(self) -> int:
        """
            The sum of :meth:`~org.optaplanner.core.api.score.AbstractBendableScore.getHardLevelsSize` and this equals
            :meth:`~org.optaplanner.core.api.score.AbstractBendableScore.getLevelsSize`.
        
            Returns:
                :code:`>= 0` and :code:`<` :meth:`~org.optaplanner.core.api.score.AbstractBendableScore.getLevelsSize`
        
        
        """
        ...


class __module_protocol__(typing.Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.optaplanner.core.api.score")``.

    AbstractBendableScore: typing.Type[AbstractBendableScore]
    AbstractScore: typing.Type[AbstractScore]
    Score: typing.Type[Score]
    ScoreExplanation: typing.Type[ScoreExplanation]
    ScoreManager: typing.Type[ScoreManager]
    buildin: org.optaplanner.core.api.score.buildin.__module_protocol__
    calculator: org.optaplanner.core.api.score.calculator.__module_protocol__
    constraint: org.optaplanner.core.api.score.constraint.__module_protocol__
    director: org.optaplanner.core.api.score.director.__module_protocol__
    holder: org.optaplanner.core.api.score.holder.__module_protocol__
    stream: org.optaplanner.core.api.score.stream.__module_protocol__
