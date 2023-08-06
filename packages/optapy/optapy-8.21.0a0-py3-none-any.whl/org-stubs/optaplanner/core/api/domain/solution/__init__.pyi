import java.lang.annotation
import org.optaplanner.core.api.domain.autodiscover
import org.optaplanner.core.api.domain.lookup
import org.optaplanner.core.api.domain.solution.cloner
import org.optaplanner.core.impl.score.definition
import typing



class PlanningEntityCollectionProperty(java.lang.annotation.Annotation):
    """
    :class:`~org.optaplanner.core.api.domain.solution.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.Target?is`({:meth:`~org.optaplanner.core.api.domain.solution.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.ElementType.html?is`,:meth:`~org.optaplanner.core.api.domain.solution.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.ElementType.html?is`}) :class:`~org.optaplanner.core.api.domain.solution.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.Retention?is`(:meth:`~org.optaplanner.core.api.domain.solution.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.RetentionPolicy.html?is`) public @interface PlanningEntityCollectionProperty
    
        Specifies that a property (or a field) on a :class:`~org.optaplanner.core.api.domain.solution.PlanningSolution` class is
        a :class:`~org.optaplanner.core.api.domain.solution.https:.docs.oracle.com.javase.8.docs.api.java.util.Collection?is` of
        planning entities.
    
        Every element in the planning entity collection should have the
        :class:`~org.optaplanner.core.api.domain.entity.PlanningEntity` annotation. Every element in the planning entity
        collection will be added to the :class:`~org.optaplanner.core.api.score.director.ScoreDirector`.
    """
    def equals(self, object: typing.Any) -> bool: ...
    def hashCode(self) -> int: ...
    def toString(self) -> str: ...

class PlanningEntityProperty(java.lang.annotation.Annotation):
    """
    :class:`~org.optaplanner.core.api.domain.solution.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.Target?is`({:meth:`~org.optaplanner.core.api.domain.solution.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.ElementType.html?is`,:meth:`~org.optaplanner.core.api.domain.solution.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.ElementType.html?is`}) :class:`~org.optaplanner.core.api.domain.solution.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.Retention?is`(:meth:`~org.optaplanner.core.api.domain.solution.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.RetentionPolicy.html?is`) public @interface PlanningEntityProperty
    
        Specifies that a property (or a field) on a :class:`~org.optaplanner.core.api.domain.solution.PlanningSolution` class is
        a planning entity.
    
        The planning entity should have the :class:`~org.optaplanner.core.api.domain.entity.PlanningEntity` annotation. The
        planning entity will be added to the :class:`~org.optaplanner.core.api.score.director.ScoreDirector`.
    """
    def equals(self, object: typing.Any) -> bool: ...
    def hashCode(self) -> int: ...
    def toString(self) -> str: ...

class PlanningScore(java.lang.annotation.Annotation):
    """
    :class:`~org.optaplanner.core.api.domain.solution.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.Target?is`({:meth:`~org.optaplanner.core.api.domain.solution.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.ElementType.html?is`,:meth:`~org.optaplanner.core.api.domain.solution.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.ElementType.html?is`}) :class:`~org.optaplanner.core.api.domain.solution.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.Retention?is`(:meth:`~org.optaplanner.core.api.domain.solution.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.RetentionPolicy.html?is`) public @interface PlanningScore
    
        Specifies that a property (or a field) on a :class:`~org.optaplanner.core.api.domain.solution.PlanningSolution` class
        holds the :class:`~org.optaplanner.core.api.score.Score` of that solution.
    
        This property can be null if the :class:`~org.optaplanner.core.api.domain.solution.PlanningSolution` is uninitialized.
    
        This property is modified by the :class:`~org.optaplanner.core.api.solver.Solver`, every time when the
        :class:`~org.optaplanner.core.api.score.Score` of this
        :class:`~org.optaplanner.core.api.domain.solution.PlanningSolution` has been calculated.
    """
    NO_LEVEL_SIZE: typing.ClassVar[int] = ...
    def bendableHardLevelsSize(self) -> int: ...
    def bendableSoftLevelsSize(self) -> int: ...
    def equals(self, object: typing.Any) -> bool: ...
    def hashCode(self) -> int: ...
    def scoreDefinitionClass(self) -> typing.Type[org.optaplanner.core.impl.score.definition.ScoreDefinition]: ...
    def toString(self) -> str: ...
    class NullScoreDefinition(org.optaplanner.core.impl.score.definition.ScoreDefinition): ...

class PlanningSolution(java.lang.annotation.Annotation):
    """
    :class:`~org.optaplanner.core.api.domain.solution.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.Target?is`(:meth:`~org.optaplanner.core.api.domain.solution.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.ElementType.html?is`) :class:`~org.optaplanner.core.api.domain.solution.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.Retention?is`(:meth:`~org.optaplanner.core.api.domain.solution.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.RetentionPolicy.html?is`) public @interface PlanningSolution
    
        Specifies that the class is a planning solution. A solution represents a problem and a possible solution of that
        problem. A possible solution does not need to be optimal or even feasible. A solution's planning variables might not be
        initialized (especially when delivered as a problem).
    
        A solution is mutable. For scalability reasons (to facilitate incremental score calculation), the same solution instance
        (called the working solution per move thread) is continuously modified. It's cloned to recall the best solution.
    
        Each planning solution must have exactly 1 :class:`~org.optaplanner.core.api.domain.solution.PlanningScore` property.
    
        Each planning solution must have at least 1
        :class:`~org.optaplanner.core.api.domain.solution.PlanningEntityCollectionProperty` or
        :class:`~org.optaplanner.core.api.domain.solution.PlanningEntityProperty` property.
    
        Each planning solution is recommended to have 1
        :class:`~org.optaplanner.core.api.domain.constraintweight.ConstraintConfigurationProvider` property too.
    
        Each planning solution used with Drools score calculation must have at least 1
        :class:`~org.optaplanner.core.api.domain.solution.ProblemFactCollectionProperty` or
        :class:`~org.optaplanner.core.api.domain.solution.ProblemFactProperty` property.
    
        The class should have a public no-arg constructor, so it can be cloned (unless the
        :meth:`~org.optaplanner.core.api.domain.solution.PlanningSolution.solutionCloner` is specified).
    """
    def autoDiscoverMemberType(self) -> org.optaplanner.core.api.domain.autodiscover.AutoDiscoverMemberType: ...
    def equals(self, object: typing.Any) -> bool: ...
    def hashCode(self) -> int: ...
    def lookUpStrategyType(self) -> org.optaplanner.core.api.domain.lookup.LookUpStrategyType: ...
    def solutionCloner(self) -> typing.Type[org.optaplanner.core.api.domain.solution.cloner.SolutionCloner]: ...
    def toString(self) -> str: ...
    class NullSolutionCloner(org.optaplanner.core.api.domain.solution.cloner.SolutionCloner): ...

class ProblemFactCollectionProperty(java.lang.annotation.Annotation):
    """
    :class:`~org.optaplanner.core.api.domain.solution.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.Target?is`({:meth:`~org.optaplanner.core.api.domain.solution.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.ElementType.html?is`,:meth:`~org.optaplanner.core.api.domain.solution.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.ElementType.html?is`}) :class:`~org.optaplanner.core.api.domain.solution.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.Retention?is`(:meth:`~org.optaplanner.core.api.domain.solution.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.RetentionPolicy.html?is`) public @interface ProblemFactCollectionProperty
    
        Specifies that a property (or a field) on a :class:`~org.optaplanner.core.api.domain.solution.PlanningSolution` class is
        a :class:`~org.optaplanner.core.api.domain.solution.https:.docs.oracle.com.javase.8.docs.api.java.util.Collection?is` of
        problem facts. A problem fact must not change during solving (except through a
        :class:`~org.optaplanner.core.api.solver.change.ProblemChange` event).
    
        The constraints in a :class:`~org.optaplanner.core.api.score.stream.ConstraintProvider` rely on problem facts for
        :meth:`~org.optaplanner.core.api.score.stream.ConstraintFactory.forEach`. Alternatively, scoreDRL relies on problem
        facts too.
    
        Do not annotate :class:`~org.optaplanner.core.api.domain.entity.PlanningEntity` as problem facts: they are automatically
        available as facts for :meth:`~org.optaplanner.core.api.score.stream.ConstraintFactory.forEach` or DRL.
    
        Also see:
            :class:`~org.optaplanner.core.api.domain.solution.ProblemFactProperty`
    """
    def equals(self, object: typing.Any) -> bool: ...
    def hashCode(self) -> int: ...
    def toString(self) -> str: ...

class ProblemFactProperty(java.lang.annotation.Annotation):
    """
    :class:`~org.optaplanner.core.api.domain.solution.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.Target?is`({:meth:`~org.optaplanner.core.api.domain.solution.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.ElementType.html?is`,:meth:`~org.optaplanner.core.api.domain.solution.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.ElementType.html?is`}) :class:`~org.optaplanner.core.api.domain.solution.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.Retention?is`(:meth:`~org.optaplanner.core.api.domain.solution.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.RetentionPolicy.html?is`) public @interface ProblemFactProperty
    
        Specifies that a property (or a field) on a :class:`~org.optaplanner.core.api.domain.solution.PlanningSolution` class is
        a problem fact. A problem fact must not change during solving (except through a
        :class:`~org.optaplanner.core.api.solver.change.ProblemChange` event).
    
        The constraints in a :class:`~org.optaplanner.core.api.score.stream.ConstraintProvider` rely on problem facts for
        :meth:`~org.optaplanner.core.api.score.stream.ConstraintFactory.forEach`. Alternatively, scoreDRL relies on problem
        facts too.
    
        Do not annotate a :class:`~org.optaplanner.core.api.domain.entity.PlanningEntity` or a
        :class:`~org.optaplanner.core.api.domain.constraintweight.ConstraintConfiguration` as a problem fact: they are
        automatically available as facts for :meth:`~org.optaplanner.core.api.score.stream.ConstraintFactory.forEach` or DRL.
    
        Also see:
            :class:`~org.optaplanner.core.api.domain.solution.ProblemFactCollectionProperty`
    """
    def equals(self, object: typing.Any) -> bool: ...
    def hashCode(self) -> int: ...
    def toString(self) -> str: ...


class __module_protocol__(typing.Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.optaplanner.core.api.domain.solution")``.

    PlanningEntityCollectionProperty: typing.Type[PlanningEntityCollectionProperty]
    PlanningEntityProperty: typing.Type[PlanningEntityProperty]
    PlanningScore: typing.Type[PlanningScore]
    PlanningSolution: typing.Type[PlanningSolution]
    ProblemFactCollectionProperty: typing.Type[ProblemFactCollectionProperty]
    ProblemFactProperty: typing.Type[ProblemFactProperty]
    cloner: org.optaplanner.core.api.domain.solution.cloner.__module_protocol__
