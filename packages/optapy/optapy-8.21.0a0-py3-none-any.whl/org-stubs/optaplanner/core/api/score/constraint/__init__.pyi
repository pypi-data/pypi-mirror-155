import java.lang
import java.util
import org.optaplanner.core.api.score
import typing



_ConstraintMatch__Score_ = typing.TypeVar('_ConstraintMatch__Score_', bound=org.optaplanner.core.api.score.Score)  # <Score_>
class ConstraintMatch(java.lang.Comparable['ConstraintMatch'[_ConstraintMatch__Score_]], typing.Generic[_ConstraintMatch__Score_]):
    """
    public final class ConstraintMatch<Score_ extends :class:`~org.optaplanner.core.api.score.Score`<Score_>> extends :class:`~org.optaplanner.core.api.score.constraint.https:.docs.oracle.com.javase.8.docs.api.java.lang.Object?is` implements :class:`~org.optaplanner.core.api.score.constraint.https:.docs.oracle.com.javase.8.docs.api.java.lang.Comparable?is`<:class:`~org.optaplanner.core.api.score.constraint.ConstraintMatch`<Score_>>
    
        Retrievable from :meth:`~org.optaplanner.core.api.score.constraint.ConstraintMatchTotal.getConstraintMatchSet` and
        :meth:`~org.optaplanner.core.api.score.constraint.Indictment.getConstraintMatchSet`.
    
        This class has a :meth:`~org.optaplanner.core.api.score.constraint.ConstraintMatch.compareTo` method which is
        inconsistent with equals. (See
        :class:`~org.optaplanner.core.api.score.constraint.https:.docs.oracle.com.javase.8.docs.api.java.lang.Comparable?is`.)
        Two different :class:`~org.optaplanner.core.api.score.constraint.ConstraintMatch` instances with the same justification
        list aren't
        :meth:`~org.optaplanner.core.api.score.constraint.https:.docs.oracle.com.javase.8.docs.api.java.lang.Object.html?is`
        because some ConstraintStream API methods can result in duplicate facts, which are treated as independent matches. Yet
        two instances may :meth:`~org.optaplanner.core.api.score.constraint.ConstraintMatch.compareTo` equal in case they come
        from the same constraint and their justifications are equal. This is for consistent ordering of constraint matches in
        visualizations.
    """
    def __init__(self, string: str, string2: str, list: java.util.List[typing.Any], score_: _ConstraintMatch__Score_): ...
    def compareTo(self, constraintMatch: 'ConstraintMatch'[_ConstraintMatch__Score_]) -> int: ...
    def getConstraintId(self) -> str: ...
    def getConstraintName(self) -> str: ...
    def getConstraintPackage(self) -> str: ...
    def getIdentificationString(self) -> str: ...
    def getJustificationList(self) -> java.util.List[typing.Any]: ...
    def getScore(self) -> _ConstraintMatch__Score_: ...
    def toString(self) -> str:
        """
        
            Overrides:
                :meth:`~org.optaplanner.core.api.score.constraint.https:.docs.oracle.com.javase.8.docs.api.java.lang.Object.html?is` in
                class :class:`~org.optaplanner.core.api.score.constraint.https:.docs.oracle.com.javase.8.docs.api.java.lang.Object?is`
        
        
        """
        ...

_ConstraintMatchTotal__Score_ = typing.TypeVar('_ConstraintMatchTotal__Score_', bound=org.optaplanner.core.api.score.Score)  # <Score_>
class ConstraintMatchTotal(typing.Generic[_ConstraintMatchTotal__Score_]):
    """
    public interface ConstraintMatchTotal<Score_ extends :class:`~org.optaplanner.core.api.score.Score`<Score_>>
    
        Explains the :class:`~org.optaplanner.core.api.score.Score` of a
        :class:`~org.optaplanner.core.api.domain.solution.PlanningSolution`, from the opposite side than
        :class:`~org.optaplanner.core.api.score.constraint.Indictment`. Retrievable from
        :meth:`~org.optaplanner.core.api.score.ScoreExplanation.getConstraintMatchTotalMap`.
    """
    @staticmethod
    def composeConstraintId(string: str, string2: str) -> str:
        """
        
            Parameters:
                constraintPackage (:class:`~org.optaplanner.core.api.score.constraint.https:.docs.oracle.com.javase.8.docs.api.java.lang.String?is`): never null
                constraintName (:class:`~org.optaplanner.core.api.score.constraint.https:.docs.oracle.com.javase.8.docs.api.java.lang.String?is`): never null
        
            Returns:
                never null
        
        
        """
        ...
    def getConstraintId(self) -> str:
        """
            To create a constraintId, use
            :meth:`~org.optaplanner.core.api.score.constraint.ConstraintMatchTotal.composeConstraintId`.
        
            Returns:
                never null
        
        
        """
        ...
    def getConstraintMatchCount(self) -> int:
        """
        
            Returns:
                :code:`>= 0`
        
        
        """
        ...
    def getConstraintMatchSet(self) -> java.util.Set[ConstraintMatch[_ConstraintMatchTotal__Score_]]: ...
    def getConstraintName(self) -> str:
        """
        
            Returns:
                never null
        
        
        """
        ...
    def getConstraintPackage(self) -> str:
        """
        
            Returns:
                never null
        
        
        """
        ...
    def getConstraintWeight(self) -> _ConstraintMatchTotal__Score_:
        """
            The value of the :class:`~org.optaplanner.core.api.domain.constraintweight.ConstraintWeight` annotated member of the
            :class:`~org.optaplanner.core.api.domain.constraintweight.ConstraintConfiguration`. It's independent to the state of the
            :class:`~org.optaplanner.core.api.domain.variable.PlanningVariable`. Do not confuse with
            :meth:`~org.optaplanner.core.api.score.constraint.ConstraintMatchTotal.getScore`.
        
            Returns:
                null if :class:`~org.optaplanner.core.api.domain.constraintweight.ConstraintWeight` isn't used for this constraint
        
        
        """
        ...
    def getScore(self) -> _ConstraintMatchTotal__Score_:
        """
            Sum of the :meth:`~org.optaplanner.core.api.score.constraint.ConstraintMatchTotal.getConstraintMatchSet`'s
            :meth:`~org.optaplanner.core.api.score.constraint.ConstraintMatch.getScore`.
        
            Returns:
                never null
        
        
        """
        ...

_Indictment__Score_ = typing.TypeVar('_Indictment__Score_', bound=org.optaplanner.core.api.score.Score)  # <Score_>
class Indictment(typing.Generic[_Indictment__Score_]):
    """
    public interface Indictment<Score_ extends :class:`~org.optaplanner.core.api.score.Score`<Score_>>
    
        Explains the :class:`~org.optaplanner.core.api.score.Score` of a
        :class:`~org.optaplanner.core.api.domain.solution.PlanningSolution`, from the opposite side than
        :class:`~org.optaplanner.core.api.score.constraint.ConstraintMatchTotal`. Retrievable from
        :meth:`~org.optaplanner.core.api.score.ScoreExplanation.getIndictmentMap`.
    """
    def getConstraintMatchCount(self) -> int:
        """
        
            Returns:
                :code:`>= 0`
        
        
        """
        ...
    def getConstraintMatchSet(self) -> java.util.Set[ConstraintMatch[_Indictment__Score_]]: ...
    def getJustification(self) -> typing.Any:
        """
        
            Returns:
                never null
        
        
        """
        ...
    def getScore(self) -> _Indictment__Score_:
        """
            Sum of the :meth:`~org.optaplanner.core.api.score.constraint.Indictment.getConstraintMatchSet`'s
            :meth:`~org.optaplanner.core.api.score.constraint.ConstraintMatch.getScore`.
        
            Returns:
                never null
        
        
        """
        ...


class __module_protocol__(typing.Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.optaplanner.core.api.score.constraint")``.

    ConstraintMatch: typing.Type[ConstraintMatch]
    ConstraintMatchTotal: typing.Type[ConstraintMatchTotal]
    Indictment: typing.Type[Indictment]
