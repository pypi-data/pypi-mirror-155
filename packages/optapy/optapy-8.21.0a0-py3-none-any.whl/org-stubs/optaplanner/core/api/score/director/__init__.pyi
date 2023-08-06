import typing



_ScoreDirector__Solution_ = typing.TypeVar('_ScoreDirector__Solution_')  # <Solution_>
class ScoreDirector(typing.Generic[_ScoreDirector__Solution_]):
    """
    public interface ScoreDirector<Solution_>
    
        The ScoreDirector holds the :class:`~org.optaplanner.core.api.domain.solution.PlanningSolution` and calculates the
        :class:`~org.optaplanner.core.api.score.Score` for it.
    """
    def afterEntityAdded(self, object: typing.Any) -> None: ...
    def afterEntityRemoved(self, object: typing.Any) -> None: ...
    def afterProblemFactAdded(self, object: typing.Any) -> None: ...
    def afterProblemFactRemoved(self, object: typing.Any) -> None: ...
    def afterProblemPropertyChanged(self, object: typing.Any) -> None: ...
    def afterVariableChanged(self, object: typing.Any, string: str) -> None: ...
    def beforeEntityAdded(self, object: typing.Any) -> None: ...
    def beforeEntityRemoved(self, object: typing.Any) -> None: ...
    def beforeProblemFactAdded(self, object: typing.Any) -> None: ...
    def beforeProblemFactRemoved(self, object: typing.Any) -> None: ...
    def beforeProblemPropertyChanged(self, object: typing.Any) -> None: ...
    def beforeVariableChanged(self, object: typing.Any, string: str) -> None: ...
    def getWorkingSolution(self) -> _ScoreDirector__Solution_:
        """
            The :class:`~org.optaplanner.core.api.domain.solution.PlanningSolution` that is used to calculate the
            :class:`~org.optaplanner.core.api.score.Score`.
        
            Because a :class:`~org.optaplanner.core.api.score.Score` is best calculated incrementally (by deltas), the
            :class:`~org.optaplanner.core.api.score.director.ScoreDirector` needs to be notified when its
            :class:`~org.optaplanner.core.api.domain.solution.PlanningSolution` changes.
        
            Returns:
                never null
        
        
        """
        ...
    _lookUpWorkingObject__E = typing.TypeVar('_lookUpWorkingObject__E')  # <E>
    def lookUpWorkingObject(self, e: _lookUpWorkingObject__E) -> _lookUpWorkingObject__E:
        """
            Translates an entity or fact instance (often from another
            :class:`~org.optaplanner.core.api.score.director.https:.docs.oracle.com.javase.8.docs.api.java.lang.Thread?is` or JVM)
            to this :class:`~org.optaplanner.core.api.score.director.ScoreDirector`'s internal working instance. Useful for move
            rebasing and in a :class:`~org.optaplanner.core.api.solver.change.ProblemChange`.
        
            Matching is determined by the :class:`~org.optaplanner.core.api.domain.lookup.LookUpStrategyType` on
            :class:`~org.optaplanner.core.api.domain.solution.PlanningSolution`. Matching uses a
            :class:`~org.optaplanner.core.api.domain.lookup.PlanningId` by default.
        
            Parameters:
                externalObject (E): sometimes null
        
            Returns:
                null if externalObject is null
        
            Raises:
                :class:`~org.optaplanner.core.api.score.director.https:.docs.oracle.com.javase.8.docs.api.java.lang.IllegalArgumentException?is`: if there is no workingObject for externalObject, if it cannot be looked up or if the externalObject's class is not
                    supported
                :class:`~org.optaplanner.core.api.score.director.https:.docs.oracle.com.javase.8.docs.api.java.lang.IllegalStateException?is`: if it cannot be looked up
        
        
        """
        ...
    _lookUpWorkingObjectOrReturnNull__E = typing.TypeVar('_lookUpWorkingObjectOrReturnNull__E')  # <E>
    def lookUpWorkingObjectOrReturnNull(self, e: _lookUpWorkingObjectOrReturnNull__E) -> _lookUpWorkingObjectOrReturnNull__E:
        """
            As defined by :meth:`~org.optaplanner.core.api.score.director.ScoreDirector.lookUpWorkingObject`, but doesn't fail fast
            if no workingObject was ever added for the externalObject. It's recommended to use
            :meth:`~org.optaplanner.core.api.score.director.ScoreDirector.lookUpWorkingObject` instead, especially in move rebasing
            code.
        
            Parameters:
                externalObject (E): sometimes null
        
            Returns:
                null if externalObject is null or if there is no workingObject for externalObject
        
            Raises:
                :class:`~org.optaplanner.core.api.score.director.https:.docs.oracle.com.javase.8.docs.api.java.lang.IllegalArgumentException?is`: if it cannot be looked up or if the externalObject's class is not supported
                :class:`~org.optaplanner.core.api.score.director.https:.docs.oracle.com.javase.8.docs.api.java.lang.IllegalStateException?is`: if it cannot be looked up
        
        
        """
        ...
    def triggerVariableListeners(self) -> None: ...


class __module_protocol__(typing.Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.optaplanner.core.api.score.director")``.

    ScoreDirector: typing.Type[ScoreDirector]
