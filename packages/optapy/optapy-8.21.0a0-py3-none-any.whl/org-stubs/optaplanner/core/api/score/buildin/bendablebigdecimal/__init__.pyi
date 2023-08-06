import decimal
import java.lang
import java.math
import org.kie.api.runtime.rule
import org.optaplanner.core.api.score
import org.optaplanner.core.api.score.holder
import typing



class BendableBigDecimalScore(org.optaplanner.core.api.score.AbstractBendableScore['BendableBigDecimalScore']):
    """
    public final class BendableBigDecimalScore extends :class:`~org.optaplanner.core.api.score.AbstractBendableScore`<:class:`~org.optaplanner.core.api.score.buildin.bendablebigdecimal.BendableBigDecimalScore`>
    
        This :class:`~org.optaplanner.core.api.score.Score` is based on n levels of
        :class:`~org.optaplanner.core.api.score.buildin.bendablebigdecimal.https:.docs.oracle.com.javase.8.docs.api.java.math.BigDecimal?is`
        constraints. The number of levels is bendable at configuration time.
    
        This class is immutable.
    
        The :meth:`~org.optaplanner.core.api.score.buildin.bendablebigdecimal.BendableBigDecimalScore.getHardLevelsSize` and
        :meth:`~org.optaplanner.core.api.score.buildin.bendablebigdecimal.BendableBigDecimalScore.getSoftLevelsSize` must be the
        same as in the :class:`~org.optaplanner.core.impl.score.buildin.BendableScoreDefinition` used.
    
        Also see:
            :class:`~org.optaplanner.core.api.score.Score`, :meth:`~serialized`
    """
    def add(self, bendableBigDecimalScore: 'BendableBigDecimalScore') -> 'BendableBigDecimalScore':
        """
            Description copied from interface: :meth:`~org.optaplanner.core.api.score.Score.add`
            Returns a Score whose value is (this + addend).
        
            Parameters:
                addend (:class:`~org.optaplanner.core.api.score.buildin.bendablebigdecimal.BendableBigDecimalScore`): value to be added to this Score
        
            Returns:
                this + addend
        
        
        """
        ...
    def compareTo(self, bendableBigDecimalScore: 'BendableBigDecimalScore') -> int: ...
    def divide(self, double: float) -> 'BendableBigDecimalScore':
        """
            Description copied from interface: :meth:`~org.optaplanner.core.api.score.Score.divide`
            Returns a Score whose value is (this / divisor). When rounding is needed, it should be floored (as defined by
            :meth:`~org.optaplanner.core.api.score.buildin.bendablebigdecimal.https:.docs.oracle.com.javase.8.docs.api.java.lang.Math.html?is`).
        
            If the implementation has a scale/precision, then the unspecified scale/precision of the double divisor should have no
            impact on the returned scale/precision.
        
            Parameters:
                divisor (double): value by which this Score is to be divided
        
            Returns:
                this / divisor
        
        
        """
        ...
    def equals(self, object: typing.Any) -> bool:
        """
        
            Overrides:
                
                meth:`~org.optaplanner.core.api.score.buildin.bendablebigdecimal.https:.docs.oracle.com.javase.8.docs.api.java.lang.Object.html?is` in
                class :class:`~org.optaplanner.core.api.score.buildin.bendablebigdecimal.https:.docs.oracle.com.javase.8.docs.api.java.lang.Object?is`
        
        
        """
        ...
    def getHardLevelsSize(self) -> int:
        """
            Description copied from class: :meth:`~org.optaplanner.core.api.score.AbstractBendableScore.getHardLevelsSize`
            The sum of this and :meth:`~org.optaplanner.core.api.score.AbstractBendableScore.getSoftLevelsSize` equals
            :meth:`~org.optaplanner.core.api.score.AbstractBendableScore.getLevelsSize`.
        
            Specified by:
                :meth:`~org.optaplanner.core.api.score.AbstractBendableScore.getHardLevelsSize` in
                class :class:`~org.optaplanner.core.api.score.AbstractBendableScore`
        
            Returns:
                :code:`>= 0` and :code:`<` :meth:`~org.optaplanner.core.api.score.AbstractBendableScore.getLevelsSize`
        
        
        """
        ...
    def getHardOrSoftScore(self, int: int) -> java.math.BigDecimal:
        """
        
            Parameters:
                index (int): :code:`0 <= index <`
                    :meth:`~org.optaplanner.core.api.score.buildin.bendablebigdecimal.BendableBigDecimalScore.getLevelsSize`
        
            Returns:
                higher is better
        
        
        """
        ...
    def getHardScore(self, int: int) -> java.math.BigDecimal:
        """
        
            Parameters:
                index (int): :code:`0 <= index <`
                    :meth:`~org.optaplanner.core.api.score.buildin.bendablebigdecimal.BendableBigDecimalScore.getHardLevelsSize`
        
            Returns:
                higher is better
        
        
        """
        ...
    def getHardScores(self) -> typing.List[java.math.BigDecimal]:
        """
        
            Returns:
                not null, array copy because this class is immutable
        
        
        """
        ...
    def getLevelsSize(self) -> int:
        """
        
            Specified by:
                :meth:`~org.optaplanner.core.api.score.AbstractBendableScore.getLevelsSize` in
                class :class:`~org.optaplanner.core.api.score.AbstractBendableScore`
        
            Returns:
                :meth:`~org.optaplanner.core.api.score.AbstractBendableScore.getHardLevelsSize` +
                :meth:`~org.optaplanner.core.api.score.AbstractBendableScore.getSoftLevelsSize`
        
        
        """
        ...
    def getSoftLevelsSize(self) -> int:
        """
            Description copied from class: :meth:`~org.optaplanner.core.api.score.AbstractBendableScore.getSoftLevelsSize`
            The sum of :meth:`~org.optaplanner.core.api.score.AbstractBendableScore.getHardLevelsSize` and this equals
            :meth:`~org.optaplanner.core.api.score.AbstractBendableScore.getLevelsSize`.
        
            Specified by:
                :meth:`~org.optaplanner.core.api.score.AbstractBendableScore.getSoftLevelsSize` in
                class :class:`~org.optaplanner.core.api.score.AbstractBendableScore`
        
            Returns:
                :code:`>= 0` and :code:`<` :meth:`~org.optaplanner.core.api.score.AbstractBendableScore.getLevelsSize`
        
        
        """
        ...
    def getSoftScore(self, int: int) -> java.math.BigDecimal:
        """
        
            Parameters:
                index (int): :code:`0 <= index <`
                    :meth:`~org.optaplanner.core.api.score.buildin.bendablebigdecimal.BendableBigDecimalScore.getSoftLevelsSize`
        
            Returns:
                higher is better
        
        
        """
        ...
    def getSoftScores(self) -> typing.List[java.math.BigDecimal]:
        """
        
            Returns:
                not null, array copy because this class is immutable
        
        
        """
        ...
    def hashCode(self) -> int:
        """
        
            Overrides:
                
                meth:`~org.optaplanner.core.api.score.buildin.bendablebigdecimal.https:.docs.oracle.com.javase.8.docs.api.java.lang.Object.html?is` in
                class :class:`~org.optaplanner.core.api.score.buildin.bendablebigdecimal.https:.docs.oracle.com.javase.8.docs.api.java.lang.Object?is`
        
        
        """
        ...
    def isFeasible(self) -> bool:
        """
            Description copied from interface: :meth:`~org.optaplanner.core.api.score.Score.isFeasible`
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
    def multiply(self, double: float) -> 'BendableBigDecimalScore':
        """
            Description copied from interface: :meth:`~org.optaplanner.core.api.score.Score.multiply`
            Returns a Score whose value is (this * multiplicand). When rounding is needed, it should be floored (as defined by
            :meth:`~org.optaplanner.core.api.score.buildin.bendablebigdecimal.https:.docs.oracle.com.javase.8.docs.api.java.lang.Math.html?is`).
        
            If the implementation has a scale/precision, then the unspecified scale/precision of the double multiplicand should have
            no impact on the returned scale/precision.
        
            Parameters:
                multiplicand (double): value to be multiplied by this Score.
        
            Returns:
                this * multiplicand
        
        
        """
        ...
    def negate(self) -> 'BendableBigDecimalScore':
        """
            Description copied from interface: :meth:`~org.optaplanner.core.api.score.Score.negate`
            Returns a Score whose value is (- this).
        
            Returns:
                - this
        
        
        """
        ...
    @staticmethod
    def of(bigDecimalArray: typing.List[java.math.BigDecimal], bigDecimalArray2: typing.List[java.math.BigDecimal]) -> 'BendableBigDecimalScore':
        """
            Creates a new :class:`~org.optaplanner.core.api.score.buildin.bendablebigdecimal.BendableBigDecimalScore`.
        
            Parameters:
                hardScores (:class:`~org.optaplanner.core.api.score.buildin.bendablebigdecimal.https:.docs.oracle.com.javase.8.docs.api.java.math.BigDecimal?is`[]): never null, never change that array afterwards: it must be immutable
                softScores (:class:`~org.optaplanner.core.api.score.buildin.bendablebigdecimal.https:.docs.oracle.com.javase.8.docs.api.java.math.BigDecimal?is`[]): never null, never change that array afterwards: it must be immutable
        
            Returns:
                never null
        
        
        """
        ...
    @staticmethod
    def ofHard(int: int, int2: int, int3: int, bigDecimal: typing.Union[java.math.BigDecimal, decimal.Decimal]) -> 'BendableBigDecimalScore':
        """
            Creates a new :class:`~org.optaplanner.core.api.score.buildin.bendablebigdecimal.BendableBigDecimalScore`.
        
            Parameters:
                hardLevelsSize (int): at least 0
                softLevelsSize (int): at least 0
                hardLevel (int): at least 0, less than hardLevelsSize
                hardScore (:class:`~org.optaplanner.core.api.score.buildin.bendablebigdecimal.https:.docs.oracle.com.javase.8.docs.api.java.math.BigDecimal?is`): never null
        
            Returns:
                never null
        
        
        """
        ...
    @staticmethod
    def ofSoft(int: int, int2: int, int3: int, bigDecimal: typing.Union[java.math.BigDecimal, decimal.Decimal]) -> 'BendableBigDecimalScore':
        """
            Creates a new :class:`~org.optaplanner.core.api.score.buildin.bendablebigdecimal.BendableBigDecimalScore`.
        
            Parameters:
                hardLevelsSize (int): at least 0
                softLevelsSize (int): at least 0
                softLevel (int): at least 0, less than softLevelsSize
                softScore (:class:`~org.optaplanner.core.api.score.buildin.bendablebigdecimal.https:.docs.oracle.com.javase.8.docs.api.java.math.BigDecimal?is`): never null
        
            Returns:
                never null
        
        
        """
        ...
    @staticmethod
    def ofUninitialized(int: int, bigDecimalArray: typing.List[java.math.BigDecimal], bigDecimalArray2: typing.List[java.math.BigDecimal]) -> 'BendableBigDecimalScore':
        """
            Creates a new :class:`~org.optaplanner.core.api.score.buildin.bendablebigdecimal.BendableBigDecimalScore`.
        
            Parameters:
                initScore (int): see :meth:`~org.optaplanner.core.api.score.Score.getInitScore`
                hardScores (:class:`~org.optaplanner.core.api.score.buildin.bendablebigdecimal.https:.docs.oracle.com.javase.8.docs.api.java.math.BigDecimal?is`[]): never null, never change that array afterwards: it must be immutable
                softScores (:class:`~org.optaplanner.core.api.score.buildin.bendablebigdecimal.https:.docs.oracle.com.javase.8.docs.api.java.math.BigDecimal?is`[]): never null, never change that array afterwards: it must be immutable
        
            Returns:
                never null
        
        
        """
        ...
    @staticmethod
    def parseScore(string: str) -> 'BendableBigDecimalScore':
        """
        
            Parameters:
                scoreString (:class:`~org.optaplanner.core.api.score.buildin.bendablebigdecimal.https:.docs.oracle.com.javase.8.docs.api.java.lang.String?is`): never null
        
            Returns:
                never null
        
        
        """
        ...
    def power(self, double: float) -> 'BendableBigDecimalScore':
        """
            Description copied from interface: :meth:`~org.optaplanner.core.api.score.Score.power`
            Returns a Score whose value is (this ^ exponent). When rounding is needed, it should be floored (as defined by
            :meth:`~org.optaplanner.core.api.score.buildin.bendablebigdecimal.https:.docs.oracle.com.javase.8.docs.api.java.lang.Math.html?is`).
        
            If the implementation has a scale/precision, then the unspecified scale/precision of the double exponent should have no
            impact on the returned scale/precision.
        
            Parameters:
                exponent (double): value by which this Score is to be powered
        
            Returns:
                this ^ exponent
        
        
        """
        ...
    def subtract(self, bendableBigDecimalScore: 'BendableBigDecimalScore') -> 'BendableBigDecimalScore':
        """
            Description copied from interface: :meth:`~org.optaplanner.core.api.score.Score.subtract`
            Returns a Score whose value is (this - subtrahend).
        
            Parameters:
                subtrahend (:class:`~org.optaplanner.core.api.score.buildin.bendablebigdecimal.BendableBigDecimalScore`): value to be subtracted from this Score
        
            Returns:
                this - subtrahend, rounded as necessary
        
        
        """
        ...
    def toLevelNumbers(self) -> typing.List[java.lang.Number]:
        """
            Description copied from interface: :meth:`~org.optaplanner.core.api.score.Score.toLevelNumbers`
            Returns an array of numbers representing the Score. Each number represents 1 score level. A greater score level uses a
            lower array index than a lesser score level.
        
            When rounding is needed, each rounding should be floored (as defined by
            :meth:`~org.optaplanner.core.api.score.buildin.bendablebigdecimal.https:.docs.oracle.com.javase.8.docs.api.java.lang.Math.html?is`).
            The length of the returned array must be stable for a specific :class:`~org.optaplanner.core.api.score.Score`
            implementation.
        
            For example: :code:`-0hard/-7soft` returns :code:`new int{-0, -7}`
        
            The level numbers do not contain the :meth:`~org.optaplanner.core.api.score.Score.getInitScore`. For example:
            :code:`-3init/-0hard/-7soft` also returns :code:`new int{-0, -7}`
        
            Returns:
                never null
        
        
        """
        ...
    def toShortString(self) -> str:
        """
            Description copied from interface: :meth:`~org.optaplanner.core.api.score.Score.toShortString`
            Like
            :meth:`~org.optaplanner.core.api.score.buildin.bendablebigdecimal.https:.docs.oracle.com.javase.8.docs.api.java.lang.Object.html?is`,
            but trims score levels which have a zero weight. For example 0hard/-258soft returns -258soft.
        
            Do not use this format to persist information as text, use
            :meth:`~org.optaplanner.core.api.score.buildin.bendablebigdecimal.https:.docs.oracle.com.javase.8.docs.api.java.lang.Object.html?is`
            instead, so it can be parsed reliably.
        
            Returns:
                never null
        
        
        """
        ...
    def toString(self) -> str:
        """
        
            Overrides:
                
                meth:`~org.optaplanner.core.api.score.buildin.bendablebigdecimal.https:.docs.oracle.com.javase.8.docs.api.java.lang.Object.html?is` in
                class :class:`~org.optaplanner.core.api.score.buildin.bendablebigdecimal.https:.docs.oracle.com.javase.8.docs.api.java.lang.Object?is`
        
        
        """
        ...
    def validateCompatible(self, bendableBigDecimalScore: 'BendableBigDecimalScore') -> None: ...
    def withInitScore(self, int: int) -> 'BendableBigDecimalScore':
        """
            Description copied from interface: :meth:`~org.optaplanner.core.api.score.Score.withInitScore`
            For example :code:`0hard/-8soft` with :code:`-7` returns :code:`-7init/0hard/-8soft`.
        
            Parameters:
                newInitScore (int): always negative (except in statistical calculations), 0 if all planning variables are initialized
        
            Returns:
                equals score except that :meth:`~org.optaplanner.core.api.score.Score.getInitScore` is set to :code:`newInitScore`
        
        
        """
        ...
    @typing.overload
    def zero(self) -> 'BendableBigDecimalScore':
        """
            Description copied from interface: :meth:`~org.optaplanner.core.api.score.Score.zero`
            Returns a Score, all levels of which are zero.
        
            Returns:
                never null
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def zero(int: int, int2: int) -> 'BendableBigDecimalScore':
        """
            Creates a new :class:`~org.optaplanner.core.api.score.buildin.bendablebigdecimal.BendableBigDecimalScore`.
        
            Parameters:
                hardLevelsSize (int): at least 0
                softLevelsSize (int): at least 0
        
            Returns:
                never null
        
        """
        ...

class BendableBigDecimalScoreHolder(org.optaplanner.core.api.score.holder.ScoreHolder[BendableBigDecimalScore]):
    """
    public interface BendableBigDecimalScoreHolder extends :class:`~org.optaplanner.core.api.score.holder.ScoreHolder`<:class:`~org.optaplanner.core.api.score.buildin.bendablebigdecimal.BendableBigDecimalScore`>
    
    
        Also see:
            :class:`~org.optaplanner.core.api.score.buildin.bendablebigdecimal.BendableBigDecimalScore`
    """
    def addHardConstraintMatch(self, ruleContext: org.kie.api.runtime.rule.RuleContext, int: int, bigDecimal: typing.Union[java.math.BigDecimal, decimal.Decimal]) -> None:
        """
        
            Parameters:
                kcontext (org.kie.api.runtime.rule.RuleContext): never null, the magic variable in DRL
                hardLevel (int): :code:`0 <= hardLevel <`
                    :meth:`~org.optaplanner.core.api.score.buildin.bendablebigdecimal.BendableBigDecimalScoreHolder.getHardLevelsSize`. The
                    :code:`scoreLevel` is :code:`hardLevel` for hard levels and :code:`softLevel + hardLevelSize` for soft levels.
                weight (:class:`~org.optaplanner.core.api.score.buildin.bendablebigdecimal.https:.docs.oracle.com.javase.8.docs.api.java.math.BigDecimal?is`): never null, higher is better, negative for a penalty, positive for a reward
        
        
        """
        ...
    def addMultiConstraintMatch(self, ruleContext: org.kie.api.runtime.rule.RuleContext, bigDecimalArray: typing.List[java.math.BigDecimal], bigDecimalArray2: typing.List[java.math.BigDecimal]) -> None:
        """
        
            Parameters:
                kcontext (org.kie.api.runtime.rule.RuleContext): never null, the magic variable in DRL
                hardWeights (:class:`~org.optaplanner.core.api.score.buildin.bendablebigdecimal.https:.docs.oracle.com.javase.8.docs.api.java.math.BigDecimal?is`[]): never null, array of length
                    :meth:`~org.optaplanner.core.api.score.buildin.bendablebigdecimal.BendableBigDecimalScoreHolder.getHardLevelsSize`, does
                    not contain any nulls
                softWeights (:class:`~org.optaplanner.core.api.score.buildin.bendablebigdecimal.https:.docs.oracle.com.javase.8.docs.api.java.math.BigDecimal?is`[]): never null, array of length
                    :meth:`~org.optaplanner.core.api.score.buildin.bendablebigdecimal.BendableBigDecimalScoreHolder.getSoftLevelsSize`, does
                    not contain any nulls
        
        
        """
        ...
    def addSoftConstraintMatch(self, ruleContext: org.kie.api.runtime.rule.RuleContext, int: int, bigDecimal: typing.Union[java.math.BigDecimal, decimal.Decimal]) -> None:
        """
        
            Parameters:
                kcontext (org.kie.api.runtime.rule.RuleContext): never null, the magic variable in DRL
                softLevel (int): :code:`0 <= softLevel <`
                    :meth:`~org.optaplanner.core.api.score.buildin.bendablebigdecimal.BendableBigDecimalScoreHolder.getSoftLevelsSize`. The
                    :code:`scoreLevel` is :code:`hardLevel` for hard levels and :code:`softLevel + hardLevelSize` for soft levels.
                weight (:class:`~org.optaplanner.core.api.score.buildin.bendablebigdecimal.https:.docs.oracle.com.javase.8.docs.api.java.math.BigDecimal?is`): never null, higher is better, negative for a penalty, positive for a reward
        
        
        """
        ...
    def getHardLevelsSize(self) -> int: ...
    def getSoftLevelsSize(self) -> int: ...
    def impactScore(self, ruleContext: org.kie.api.runtime.rule.RuleContext, bigDecimal: typing.Union[java.math.BigDecimal, decimal.Decimal]) -> None: ...
    @typing.overload
    def penalize(self, ruleContext: org.kie.api.runtime.rule.RuleContext, bigDecimal: typing.Union[java.math.BigDecimal, decimal.Decimal]) -> None:
        """
            Penalize a match by the :class:`~org.optaplanner.core.api.domain.constraintweight.ConstraintWeight` negated and
            multiplied with the weightMultiplier for all score levels.
        
            Parameters:
                kcontext (org.kie.api.runtime.rule.RuleContext): never null, the magic variable in DRL
                weightMultiplier (:class:`~org.optaplanner.core.api.score.buildin.bendablebigdecimal.https:.docs.oracle.com.javase.8.docs.api.java.math.BigDecimal?is`): at least 0
        
            Penalize a match by the :class:`~org.optaplanner.core.api.domain.constraintweight.ConstraintWeight` negated and
            multiplied with the specific weightMultiplier per score level. Slower than
            :meth:`~org.optaplanner.core.api.score.buildin.bendablebigdecimal.BendableBigDecimalScoreHolder.penalize`.
        
            Parameters:
                kcontext (org.kie.api.runtime.rule.RuleContext): never null, the magic variable in DRL
                hardWeightsMultiplier (:class:`~org.optaplanner.core.api.score.buildin.bendablebigdecimal.https:.docs.oracle.com.javase.8.docs.api.java.math.BigDecimal?is`[]): elements at least 0
                softWeightsMultiplier (:class:`~org.optaplanner.core.api.score.buildin.bendablebigdecimal.https:.docs.oracle.com.javase.8.docs.api.java.math.BigDecimal?is`[]): elements at least 0
        
        
        """
        ...
    @typing.overload
    def penalize(self, ruleContext: org.kie.api.runtime.rule.RuleContext, bigDecimalArray: typing.List[java.math.BigDecimal], bigDecimalArray2: typing.List[java.math.BigDecimal]) -> None: ...
    @typing.overload
    def penalize(self, ruleContext: org.kie.api.runtime.rule.RuleContext) -> None: ...
    @typing.overload
    def reward(self, ruleContext: org.kie.api.runtime.rule.RuleContext, bigDecimal: typing.Union[java.math.BigDecimal, decimal.Decimal]) -> None:
        """
            Reward a match by the :class:`~org.optaplanner.core.api.domain.constraintweight.ConstraintWeight` multiplied with the
            weightMultiplier for all score levels.
        
            Parameters:
                kcontext (org.kie.api.runtime.rule.RuleContext): never null, the magic variable in DRL
                weightMultiplier (:class:`~org.optaplanner.core.api.score.buildin.bendablebigdecimal.https:.docs.oracle.com.javase.8.docs.api.java.math.BigDecimal?is`): at least 0
        
            Reward a match by the :class:`~org.optaplanner.core.api.domain.constraintweight.ConstraintWeight` multiplied with the
            specific weightMultiplier per score level. Slower than
            :meth:`~org.optaplanner.core.api.score.buildin.bendablebigdecimal.BendableBigDecimalScoreHolder.reward`.
        
            Parameters:
                kcontext (org.kie.api.runtime.rule.RuleContext): never null, the magic variable in DRL
                hardWeightsMultiplier (:class:`~org.optaplanner.core.api.score.buildin.bendablebigdecimal.https:.docs.oracle.com.javase.8.docs.api.java.math.BigDecimal?is`[]): elements at least 0
                softWeightsMultiplier (:class:`~org.optaplanner.core.api.score.buildin.bendablebigdecimal.https:.docs.oracle.com.javase.8.docs.api.java.math.BigDecimal?is`[]): elements at least 0
        
        
        """
        ...
    @typing.overload
    def reward(self, ruleContext: org.kie.api.runtime.rule.RuleContext, bigDecimalArray: typing.List[java.math.BigDecimal], bigDecimalArray2: typing.List[java.math.BigDecimal]) -> None: ...
    @typing.overload
    def reward(self, ruleContext: org.kie.api.runtime.rule.RuleContext) -> None: ...


class __module_protocol__(typing.Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.optaplanner.core.api.score.buildin.bendablebigdecimal")``.

    BendableBigDecimalScore: typing.Type[BendableBigDecimalScore]
    BendableBigDecimalScoreHolder: typing.Type[BendableBigDecimalScoreHolder]
