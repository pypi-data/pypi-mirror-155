import org.kie.api.runtime.rule
import org.optaplanner.core.api.score
import typing



_ScoreHolder__Score_ = typing.TypeVar('_ScoreHolder__Score_', bound=org.optaplanner.core.api.score.Score)  # <Score_>
class ScoreHolder(typing.Generic[_ScoreHolder__Score_]):
    """
    public interface ScoreHolder<Score_ extends :class:`~org.optaplanner.core.api.score.Score`<Score_>>
    
        This is the base interface for all score holder implementations.
    """
    def penalize(self, ruleContext: org.kie.api.runtime.rule.RuleContext) -> None:
        """
            Penalize a match by the :class:`~org.optaplanner.core.api.domain.constraintweight.ConstraintWeight` negated.
        
            Parameters:
                kcontext (org.kie.api.runtime.rule.RuleContext): never null, the magic variable in DRL
        
        
        """
        ...
    def reward(self, ruleContext: org.kie.api.runtime.rule.RuleContext) -> None:
        """
            Reward a match by the :class:`~org.optaplanner.core.api.domain.constraintweight.ConstraintWeight`.
        
            Parameters:
                kcontext (org.kie.api.runtime.rule.RuleContext): never null, the magic variable in DRL
        
        
        """
        ...


class __module_protocol__(typing.Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.optaplanner.core.api.score.holder")``.

    ScoreHolder: typing.Type[ScoreHolder]
