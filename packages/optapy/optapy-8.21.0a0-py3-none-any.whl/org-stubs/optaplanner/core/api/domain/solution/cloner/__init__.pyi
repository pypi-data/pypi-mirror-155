import java.lang.annotation
import typing



class DeepPlanningClone(java.lang.annotation.Annotation):
    """
    :class:`~org.optaplanner.core.api.domain.solution.cloner.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.Target?is`({:meth:`~org.optaplanner.core.api.domain.solution.cloner.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.ElementType.html?is`,:meth:`~org.optaplanner.core.api.domain.solution.cloner.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.ElementType.html?is`,:meth:`~org.optaplanner.core.api.domain.solution.cloner.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.ElementType.html?is`}) :class:`~org.optaplanner.core.api.domain.solution.cloner.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.Inherited?is` :class:`~org.optaplanner.core.api.domain.solution.cloner.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.Retention?is`(:meth:`~org.optaplanner.core.api.domain.solution.cloner.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.RetentionPolicy.html?is`) public @interface DeepPlanningClone
    
        Marks a problem fact class as being required to be deep planning cloned. Not needed for a
        :class:`~org.optaplanner.core.api.domain.solution.PlanningSolution` or
        :class:`~org.optaplanner.core.api.domain.entity.PlanningEntity` because those are automatically deep cloned.
    
        It can also mark a property (getter for a field) as being required to be deep planning cloned. This is especially useful
        for
        :class:`~org.optaplanner.core.api.domain.solution.cloner.https:.docs.oracle.com.javase.8.docs.api.java.util.Collection?is`
        (or :class:`~org.optaplanner.core.api.domain.solution.cloner.https:.docs.oracle.com.javase.8.docs.api.java.util.Map?is`)
        properties. Not needed for a
        :class:`~org.optaplanner.core.api.domain.solution.cloner.https:.docs.oracle.com.javase.8.docs.api.java.util.Collection?is`
        (or :class:`~org.optaplanner.core.api.domain.solution.cloner.https:.docs.oracle.com.javase.8.docs.api.java.util.Map?is`)
        property with a generic type of :class:`~org.optaplanner.core.api.domain.entity.PlanningEntity` or a class with a
        DeepPlanningClone annotation, because those are automatically deep cloned. Note: If it annotates a property (getter
        method for a field) returning
        :class:`~org.optaplanner.core.api.domain.solution.cloner.https:.docs.oracle.com.javase.8.docs.api.java.util.Collection?is`
        (or
        :class:`~org.optaplanner.core.api.domain.solution.cloner.https:.docs.oracle.com.javase.8.docs.api.java.util.Map?is`), it
        clones the
        :class:`~org.optaplanner.core.api.domain.solution.cloner.https:.docs.oracle.com.javase.8.docs.api.java.util.Collection?is`
        (or
        :class:`~org.optaplanner.core.api.domain.solution.cloner.https:.docs.oracle.com.javase.8.docs.api.java.util.Map?is`),
        but its elements (or keys and values) are only cloned if they are of a type that needs to be planning cloned.
    
        This annotation is ignored if a custom :class:`~org.optaplanner.core.api.domain.solution.cloner.SolutionCloner` is set
        with :meth:`~org.optaplanner.core.api.domain.solution.PlanningSolution.solutionCloner`.
    """
    def equals(self, object: typing.Any) -> bool: ...
    def hashCode(self) -> int: ...
    def toString(self) -> str: ...

_SolutionCloner__Solution_ = typing.TypeVar('_SolutionCloner__Solution_')  # <Solution_>
class SolutionCloner(typing.Generic[_SolutionCloner__Solution_]):
    """
    public interface SolutionCloner<Solution_>
    
        Clones a :class:`~org.optaplanner.core.api.domain.solution.PlanningSolution` during planning. Used to remember the state
        of a good :class:`~org.optaplanner.core.api.domain.solution.PlanningSolution` so it can be recalled at a later time when
        the original :class:`~org.optaplanner.core.api.domain.solution.PlanningSolution` is already modified. Also used in
        population based heuristics to increase or repopulate the population.
    
        Planning cloning is hard: avoid doing it yourself.
    
        An implementing class must be thread-safe after initialization.
    """
    def cloneSolution(self, solution_: _SolutionCloner__Solution_) -> _SolutionCloner__Solution_:
        """
            Does a planning clone. The returned :class:`~org.optaplanner.core.api.domain.solution.PlanningSolution` clone must
            fulfill these requirements:
        
              - The clone must represent the same planning problem. Usually it reuses the same instances of the problem facts and
                problem fact collections as the :code:`original`.
              - The clone must have the same (equal) score as the :code:`original`.
              - The clone must use different, cloned instances of the entities and entity collections. If a cloned entity changes, the
                original must remain unchanged. If an entity is added or removed in a cloned
                :class:`~org.optaplanner.core.api.domain.solution.PlanningSolution`, the original
                :class:`~org.optaplanner.core.api.domain.solution.PlanningSolution` must remain unchanged.
        
            Note that a class might support more than 1 clone method: planning clone is just one of them.
        
            This method is thread-safe.
        
            Parameters:
                original (:class:`~org.optaplanner.core.api.domain.solution.cloner.SolutionCloner`): never null, the original :class:`~org.optaplanner.core.api.domain.solution.PlanningSolution`
        
            Returns:
                never null, the cloned :class:`~org.optaplanner.core.api.domain.solution.PlanningSolution`
        
        
        """
        ...


class __module_protocol__(typing.Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.optaplanner.core.api.domain.solution.cloner")``.

    DeepPlanningClone: typing.Type[DeepPlanningClone]
    SolutionCloner: typing.Type[SolutionCloner]
