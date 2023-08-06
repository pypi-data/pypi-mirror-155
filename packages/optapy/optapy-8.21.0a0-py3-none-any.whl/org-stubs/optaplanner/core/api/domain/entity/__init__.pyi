import java.lang.annotation
import java.util
import org.optaplanner.core.impl.heuristic.selector.common.decorator
import typing



_PinningFilter__Solution_ = typing.TypeVar('_PinningFilter__Solution_')  # <Solution_>
_PinningFilter__Entity_ = typing.TypeVar('_PinningFilter__Entity_')  # <Entity_>
class PinningFilter(typing.Generic[_PinningFilter__Solution_, _PinningFilter__Entity_]):
    """
    public interface PinningFilter<Solution_, Entity_>
    
        Decides on accepting or discarding a :class:`~org.optaplanner.core.api.domain.entity.PlanningEntity`. A pinned
        :class:`~org.optaplanner.core.api.domain.entity.PlanningEntity`'s planning variables are never changed.
    """
    def accept(self, solution_: _PinningFilter__Solution_, entity_: _PinningFilter__Entity_) -> bool:
        """
        
            Parameters:
                solution (:class:`~org.optaplanner.core.api.domain.entity.PinningFilter`): working solution to which the entity belongs
                entity (:class:`~org.optaplanner.core.api.domain.entity.PinningFilter`): never null, a :class:`~org.optaplanner.core.api.domain.entity.PlanningEntity`
        
            Returns:
                true if the entity it is pinned, false if the entity is movable.
        
        
        """
        ...

class PlanningPin(java.lang.annotation.Annotation):
    """
    :class:`~org.optaplanner.core.api.domain.entity.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.Target?is`({:meth:`~org.optaplanner.core.api.domain.entity.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.ElementType.html?is`,:meth:`~org.optaplanner.core.api.domain.entity.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.ElementType.html?is`}) :class:`~org.optaplanner.core.api.domain.entity.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.Retention?is`(:meth:`~org.optaplanner.core.api.domain.entity.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.RetentionPolicy.html?is`) public @interface PlanningPin
    
        Specifies that a boolean property (or field) of a :class:`~org.optaplanner.core.api.domain.entity.PlanningEntity`
        determines if the planning entity is pinned. A pinned planning entity is never changed during planning. For example, it
        allows the user to pin a shift to a specific employee before solving and the solver will not undo that, regardless of
        the constraints.
    
        The boolean is false if the planning entity is movable and true if the planning entity is pinned.
    
        It applies to all the planning variables of that planning entity. To make individual variables pinned, see
        https://issues.redhat.com/browse/PLANNER-124
    
        This is syntactic sugar for :meth:`~org.optaplanner.core.api.domain.entity.PlanningEntity.pinningFilter`, which is a
        more flexible and verbose way to pin a planning entity.
    """
    def equals(self, object: typing.Any) -> bool: ...
    def hashCode(self) -> int: ...
    def toString(self) -> str: ...

class PlanningEntity(java.lang.annotation.Annotation):
    """
    :class:`~org.optaplanner.core.api.domain.entity.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.Target?is`(:meth:`~org.optaplanner.core.api.domain.entity.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.ElementType.html?is`) :class:`~org.optaplanner.core.api.domain.entity.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.Retention?is`(:meth:`~org.optaplanner.core.api.domain.entity.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.RetentionPolicy.html?is`) public @interface PlanningEntity
    
        Specifies that the class is a planning entity. Each planning entity must have at least 1
        :class:`~org.optaplanner.core.api.domain.variable.PlanningVariable` property.
    
        The class should have a public no-arg constructor, so it can be cloned (unless the
        :meth:`~org.optaplanner.core.api.domain.solution.PlanningSolution.solutionCloner` is specified).
    """
    def difficultyComparatorClass(self) -> typing.Type[java.util.Comparator]: ...
    def difficultyWeightFactoryClass(self) -> typing.Type[org.optaplanner.core.impl.heuristic.selector.common.decorator.SelectionSorterWeightFactory]: ...
    def equals(self, object: typing.Any) -> bool: ...
    def hashCode(self) -> int: ...
    def pinningFilter(self) -> typing.Type[PinningFilter]: ...
    def toString(self) -> str: ...
    class NullDifficultyComparator(java.util.Comparator):
        def equals(self, object: typing.Any) -> bool: ...
    class NullDifficultyWeightFactory(org.optaplanner.core.impl.heuristic.selector.common.decorator.SelectionSorterWeightFactory): ...
    class NullPinningFilter(PinningFilter): ...


class __module_protocol__(typing.Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.optaplanner.core.api.domain.entity")``.

    PinningFilter: typing.Type[PinningFilter]
    PlanningEntity: typing.Type[PlanningEntity]
    PlanningPin: typing.Type[PlanningPin]
