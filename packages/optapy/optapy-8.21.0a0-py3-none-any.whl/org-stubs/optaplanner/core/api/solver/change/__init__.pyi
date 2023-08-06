import java.util
import java.util.function
import typing



_ProblemChange__Solution_ = typing.TypeVar('_ProblemChange__Solution_')  # <Solution_>
class ProblemChange(typing.Generic[_ProblemChange__Solution_]):
    """
    :class:`~org.optaplanner.core.api.solver.change.https:.docs.oracle.com.javase.8.docs.api.java.lang.FunctionalInterface?is` public interface ProblemChange<Solution_>
    
        A ProblemChange represents a change in one or more :class:`~org.optaplanner.core.api.domain.entity.PlanningEntity` or
        problem facts of a :class:`~org.optaplanner.core.api.domain.solution.PlanningSolution`.
    
        The :class:`~org.optaplanner.core.api.solver.Solver` checks the presence of waiting problem changes after every
        :class:`~org.optaplanner.core.impl.heuristic.move.Move` evaluation. If there are waiting problem changes, the
        :class:`~org.optaplanner.core.api.solver.Solver`:
    
          1.  clones the last :class:`~org.optaplanner.core.api.domain.solution.PlanningSolution` and sets the clone as the new
            :class:`~org.optaplanner.core.api.domain.solution.PlanningSolution`
          2.  applies every problem change keeping the order in which problem changes have been submitted; after every problem change,
            :class:`~org.optaplanner.core.api.domain.variable.VariableListener` are triggered
          3.  calculates the score and makes the :class:`~org.optaplanner.core.api.domain.solution.PlanningSolution` the new
            :class:`~org.optaplanner.core.api.domain.solution.PlanningSolution`; note that this
            :class:`~org.optaplanner.core.api.domain.solution.PlanningSolution` is not published via the
            :class:`~org.optaplanner.core.api.solver.event.BestSolutionChangedEvent`, as it hasn't been initialized yet
          4.  restarts solving to fill potential uninitialized :class:`~org.optaplanner.core.api.domain.entity.PlanningEntity`
    
    
        Note that the :class:`~org.optaplanner.core.api.solver.Solver` clones a
        :class:`~org.optaplanner.core.api.domain.solution.PlanningSolution` at will. Any change must be done on the problem
        facts and planning entities referenced by the :class:`~org.optaplanner.core.api.domain.solution.PlanningSolution`.
    
        An example implementation, based on the Cloud balancing problem, looks as follows:
    
        .. code-block: java
        
         
         public class DeleteComputerProblemChange implements ProblemChange<CloudBalance> {
        
             private final CloudComputer computer;
        
             public DeleteComputerProblemChange(CloudComputer computer) {
                 this.computer = computer;
             }
        
             {@literal @Override}
             public void doChange(CloudBalance cloudBalance, ProblemChangeDirector problemChangeDirector) {
                 CloudComputer workingComputer = problemChangeDirector.lookUpWorkingObjectOrFail(computer);
                 // First remove the problem fact from all planning entities that use it
                 for (CloudProcess process : cloudBalance.getProcessList()) {
                     if (process.getComputer() == workingComputer) {
                         problemChangeDirector.changeVariable(process, "computer",
                                 workingProcess -> workingProcess.setComputer(null));
                     }
                 }
                 // A SolutionCloner does not clone problem fact lists (such as computerList), only entity lists.
                 // Shallow clone the computerList so only the working solution is affected.
                 ArrayList<CloudComputer> computerList = new ArrayList<>(cloudBalance.getComputerList());
                 cloudBalance.setComputerList(computerList);
                 // Remove the problem fact itself
                 problemChangeDirector.removeProblemFact(workingComputer, computerList::remove);
             }
         }
    """
    def doChange(self, solution_: _ProblemChange__Solution_, problemChangeDirector: 'ProblemChangeDirector') -> None:
        """
            Do the change on the :class:`~org.optaplanner.core.api.domain.solution.PlanningSolution`. Every modification to the
            :class:`~org.optaplanner.core.api.domain.solution.PlanningSolution` must be done via the
            :class:`~org.optaplanner.core.api.solver.change.ProblemChangeDirector`, otherwise the
            :class:`~org.optaplanner.core.api.score.Score` calculation will be corrupted.
        
            Parameters:
                workingSolution (:class:`~org.optaplanner.core.api.solver.change.ProblemChange`): never null; the :class:`~org.optaplanner.core.api.domain.solution.PlanningSolution` which contains the problem facts
                    (and :class:`~org.optaplanner.core.api.domain.entity.PlanningEntity`) to change
                problemChangeDirector (:class:`~org.optaplanner.core.api.solver.change.ProblemChangeDirector`): never null; :class:`~org.optaplanner.core.api.solver.change.ProblemChangeDirector` to perform the change through
        
        
        """
        ...

class ProblemChangeDirector:
    """
    public interface ProblemChangeDirector
    
        Allows external changes to the :class:`~org.optaplanner.core.api.domain.solution.PlanningSolution`. If the changes are
        not applied through the ProblemChangeDirector, :class:`~org.optaplanner.core.api.domain.variable.VariableListener` are
        never notified about them, resulting to inconsistencies in the
        :class:`~org.optaplanner.core.api.domain.solution.PlanningSolution`. Should be used only from a
        :class:`~org.optaplanner.core.api.solver.change.ProblemChange` implementation. To see an example implementation, please
        refer to the :class:`~org.optaplanner.core.api.solver.change.ProblemChange` Javadoc.
    """
    _addEntity__Entity = typing.TypeVar('_addEntity__Entity')  # <Entity>
    def addEntity(self, entity: _addEntity__Entity, consumer: typing.Union[java.util.function.Consumer[_addEntity__Entity], typing.Callable[[_addEntity__Entity], None]]) -> None:
        """
            Add a new :class:`~org.optaplanner.core.api.domain.entity.PlanningEntity` instance into the
            :class:`~org.optaplanner.core.api.domain.solution.PlanningSolution`.
        
            Parameters:
                entity (Entity): never null; the :class:`~org.optaplanner.core.api.domain.entity.PlanningEntity` instance
                entityConsumer (:class:`~org.optaplanner.core.api.solver.change.https:.docs.oracle.com.javase.8.docs.api.java.util.function.Consumer?is`<Entity> entityConsumer): never null; adds the entity to the :class:`~org.optaplanner.core.api.domain.solution.PlanningSolution`
        
        
        """
        ...
    _addProblemFact__ProblemFact = typing.TypeVar('_addProblemFact__ProblemFact')  # <ProblemFact>
    def addProblemFact(self, problemFact: _addProblemFact__ProblemFact, consumer: typing.Union[java.util.function.Consumer[_addProblemFact__ProblemFact], typing.Callable[[_addProblemFact__ProblemFact], None]]) -> None:
        """
            Add a new problem fact into the :class:`~org.optaplanner.core.api.domain.solution.PlanningSolution`.
        
            Parameters:
                problemFact (ProblemFact): never null; the problem fact instance
                problemFactConsumer (:class:`~org.optaplanner.core.api.solver.change.https:.docs.oracle.com.javase.8.docs.api.java.util.function.Consumer?is`<ProblemFact> problemFactConsumer): never null; removes the working problem fact from the
                    :class:`~org.optaplanner.core.api.domain.solution.PlanningSolution`
        
        
        """
        ...
    _changeProblemProperty__EntityOrProblemFact = typing.TypeVar('_changeProblemProperty__EntityOrProblemFact')  # <EntityOrProblemFact>
    def changeProblemProperty(self, entityOrProblemFact: _changeProblemProperty__EntityOrProblemFact, consumer: typing.Union[java.util.function.Consumer[_changeProblemProperty__EntityOrProblemFact], typing.Callable[[_changeProblemProperty__EntityOrProblemFact], None]]) -> None:
        """
            Change a property of either a :class:`~org.optaplanner.core.api.domain.entity.PlanningEntity` or a problem fact.
            Translates the entity or the problem fact to its :class:`~org.optaplanner.core.api.domain.solution.PlanningSolution`
            counterpart by performing a lookup as defined by
            :meth:`~org.optaplanner.core.api.solver.change.ProblemChangeDirector.lookUpWorkingObjectOrFail`.
        
            Parameters:
                problemFactOrEntity (EntityOrProblemFact): never null; the :class:`~org.optaplanner.core.api.domain.entity.PlanningEntity` or the problem fact instance
                problemFactOrEntityConsumer (:class:`~org.optaplanner.core.api.solver.change.https:.docs.oracle.com.javase.8.docs.api.java.util.function.Consumer?is`<EntityOrProblemFact> problemFactOrEntityConsumer): never null; updates the property of the :class:`~org.optaplanner.core.api.domain.entity.PlanningEntity` or the problem
                    fact
        
        
        """
        ...
    _changeVariable__Entity = typing.TypeVar('_changeVariable__Entity')  # <Entity>
    def changeVariable(self, entity: _changeVariable__Entity, string: str, consumer: typing.Union[java.util.function.Consumer[_changeVariable__Entity], typing.Callable[[_changeVariable__Entity], None]]) -> None:
        """
            Change a :class:`~org.optaplanner.core.api.domain.variable.PlanningVariable` value of a
            :class:`~org.optaplanner.core.api.domain.entity.PlanningEntity`. Translates the entity to a working planning entity by
            performing a lookup as defined by
            :meth:`~org.optaplanner.core.api.solver.change.ProblemChangeDirector.lookUpWorkingObjectOrFail`.
        
            Parameters:
                entity (Entity): never null; the :class:`~org.optaplanner.core.api.domain.entity.PlanningEntity` instance
                variableName (:class:`~org.optaplanner.core.api.solver.change.https:.docs.oracle.com.javase.8.docs.api.java.lang.String?is`): never null; name of the :class:`~org.optaplanner.core.api.domain.variable.PlanningVariable`
                entityConsumer (:class:`~org.optaplanner.core.api.solver.change.https:.docs.oracle.com.javase.8.docs.api.java.util.function.Consumer?is`<Entity> entityConsumer): never null; updates the value of the the :class:`~org.optaplanner.core.api.domain.variable.PlanningVariable` inside the
                    :class:`~org.optaplanner.core.api.domain.entity.PlanningEntity`
        
        
        """
        ...
    _lookUpWorkingObject__EntityOrProblemFact = typing.TypeVar('_lookUpWorkingObject__EntityOrProblemFact')  # <EntityOrProblemFact>
    def lookUpWorkingObject(self, entityOrProblemFact: _lookUpWorkingObject__EntityOrProblemFact) -> java.util.Optional[_lookUpWorkingObject__EntityOrProblemFact]:
        """
            As defined by :meth:`~org.optaplanner.core.api.solver.change.ProblemChangeDirector.lookUpWorkingObjectOrFail`, but
            doesn't fail fast if no workingObject was ever added for the externalObject. It's recommended to use
            :meth:`~org.optaplanner.core.api.solver.change.ProblemChangeDirector.lookUpWorkingObjectOrFail` instead.
        
            Parameters:
                externalObject (EntityOrProblemFact): sometimes null
        
            Returns:
                :meth:`~org.optaplanner.core.api.solver.change.https:.docs.oracle.com.javase.8.docs.api.java.util.Optional.html?is` if
                externalObject is null or if there is no workingObject for externalObject
        
            Raises:
                :class:`~org.optaplanner.core.api.solver.change.https:.docs.oracle.com.javase.8.docs.api.java.lang.IllegalArgumentException?is`: if it cannot be looked up or if the externalObject's class is not supported
                :class:`~org.optaplanner.core.api.solver.change.https:.docs.oracle.com.javase.8.docs.api.java.lang.IllegalStateException?is`: if it cannot be looked up
        
        
        """
        ...
    _lookUpWorkingObjectOrFail__EntityOrProblemFact = typing.TypeVar('_lookUpWorkingObjectOrFail__EntityOrProblemFact')  # <EntityOrProblemFact>
    def lookUpWorkingObjectOrFail(self, entityOrProblemFact: _lookUpWorkingObjectOrFail__EntityOrProblemFact) -> _lookUpWorkingObjectOrFail__EntityOrProblemFact:
        """
            Translate an entity or fact instance (often from another
            :class:`~org.optaplanner.core.api.solver.change.https:.docs.oracle.com.javase.8.docs.api.java.lang.Thread?is` or JVM) to
            this :class:`~org.optaplanner.core.api.solver.change.ProblemChangeDirector`'s internal working instance.
        
            Matching is determined by the :class:`~org.optaplanner.core.api.domain.lookup.LookUpStrategyType` on
            :class:`~org.optaplanner.core.api.domain.solution.PlanningSolution`. Matching uses a
            :class:`~org.optaplanner.core.api.domain.lookup.PlanningId` by default.
        
            Parameters:
                externalObject (EntityOrProblemFact): sometimes null
        
            Returns:
                null if externalObject is null
        
            Raises:
                :class:`~org.optaplanner.core.api.solver.change.https:.docs.oracle.com.javase.8.docs.api.java.lang.IllegalArgumentException?is`: if there is no workingObject for externalObject, if it cannot be looked up or if the externalObject's class is not
                    supported
                :class:`~org.optaplanner.core.api.solver.change.https:.docs.oracle.com.javase.8.docs.api.java.lang.IllegalStateException?is`: if it cannot be looked up
        
        
        """
        ...
    _removeEntity__Entity = typing.TypeVar('_removeEntity__Entity')  # <Entity>
    def removeEntity(self, entity: _removeEntity__Entity, consumer: typing.Union[java.util.function.Consumer[_removeEntity__Entity], typing.Callable[[_removeEntity__Entity], None]]) -> None:
        """
            Remove an existing :class:`~org.optaplanner.core.api.domain.entity.PlanningEntity` instance from the
            :class:`~org.optaplanner.core.api.domain.solution.PlanningSolution`. Translates the entity to a working planning entity
            by performing a lookup as defined by
            :meth:`~org.optaplanner.core.api.solver.change.ProblemChangeDirector.lookUpWorkingObjectOrFail`.
        
            Parameters:
                entity (Entity): never null; the :class:`~org.optaplanner.core.api.domain.entity.PlanningEntity` instance
                entityConsumer (:class:`~org.optaplanner.core.api.solver.change.https:.docs.oracle.com.javase.8.docs.api.java.util.function.Consumer?is`<Entity> entityConsumer): never null; removes the working entity from the :class:`~org.optaplanner.core.api.domain.solution.PlanningSolution`
        
        
        """
        ...
    _removeProblemFact__ProblemFact = typing.TypeVar('_removeProblemFact__ProblemFact')  # <ProblemFact>
    def removeProblemFact(self, problemFact: _removeProblemFact__ProblemFact, consumer: typing.Union[java.util.function.Consumer[_removeProblemFact__ProblemFact], typing.Callable[[_removeProblemFact__ProblemFact], None]]) -> None:
        """
            Remove an existing problem fact from the :class:`~org.optaplanner.core.api.domain.solution.PlanningSolution`. Translates
            the problem fact to a working problem fact by performing a lookup as defined by
            :meth:`~org.optaplanner.core.api.solver.change.ProblemChangeDirector.lookUpWorkingObjectOrFail`.
        
            Parameters:
                problemFact (ProblemFact): never null; the problem fact instance
                problemFactConsumer (:class:`~org.optaplanner.core.api.solver.change.https:.docs.oracle.com.javase.8.docs.api.java.util.function.Consumer?is`<ProblemFact> problemFactConsumer): never null; removes the working problem fact from the
                    :class:`~org.optaplanner.core.api.domain.solution.PlanningSolution`
        
        
        """
        ...


class __module_protocol__(typing.Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.optaplanner.core.api.solver.change")``.

    ProblemChange: typing.Type[ProblemChange]
    ProblemChangeDirector: typing.Type[ProblemChangeDirector]
