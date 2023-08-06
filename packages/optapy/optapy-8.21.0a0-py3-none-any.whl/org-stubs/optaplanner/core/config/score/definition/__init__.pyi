import java.lang
import typing



class ScoreDefinitionType(java.lang.Enum['ScoreDefinitionType']):
    """
    public enum ScoreDefinitionType extends :class:`~org.optaplanner.core.config.score.definition.https:.docs.oracle.com.javase.8.docs.api.java.lang.Enum?is`<:class:`~org.optaplanner.core.config.score.definition.ScoreDefinitionType`>
    """
    SIMPLE: typing.ClassVar['ScoreDefinitionType'] = ...
    SIMPLE_LONG: typing.ClassVar['ScoreDefinitionType'] = ...
    SIMPLE_DOUBLE: typing.ClassVar['ScoreDefinitionType'] = ...
    SIMPLE_BIG_DECIMAL: typing.ClassVar['ScoreDefinitionType'] = ...
    HARD_SOFT: typing.ClassVar['ScoreDefinitionType'] = ...
    HARD_SOFT_LONG: typing.ClassVar['ScoreDefinitionType'] = ...
    HARD_SOFT_DOUBLE: typing.ClassVar['ScoreDefinitionType'] = ...
    HARD_SOFT_BIG_DECIMAL: typing.ClassVar['ScoreDefinitionType'] = ...
    HARD_MEDIUM_SOFT: typing.ClassVar['ScoreDefinitionType'] = ...
    HARD_MEDIUM_SOFT_LONG: typing.ClassVar['ScoreDefinitionType'] = ...
    BENDABLE: typing.ClassVar['ScoreDefinitionType'] = ...
    BENDABLE_LONG: typing.ClassVar['ScoreDefinitionType'] = ...
    BENDABLE_BIG_DECIMAL: typing.ClassVar['ScoreDefinitionType'] = ...
    _valueOf_0__T = typing.TypeVar('_valueOf_0__T', bound=java.lang.Enum)  # <T>
    @typing.overload
    @staticmethod
    def valueOf(class_: typing.Type[_valueOf_0__T], string: str) -> _valueOf_0__T: ...
    @typing.overload
    @staticmethod
    def valueOf(string: str) -> 'ScoreDefinitionType':
        """
            Returns the enum constant of this type with the specified name. The string must match *exactly* an identifier used to
            declare an enum constant in this type. (Extraneous whitespace characters are not permitted.)
        
            Parameters:
                name (:class:`~org.optaplanner.core.config.score.definition.https:.docs.oracle.com.javase.8.docs.api.java.lang.String?is`): the name of the enum constant to be returned.
        
            Returns:
                the enum constant with the specified name
        
            Raises:
                :class:`~org.optaplanner.core.config.score.definition.https:.docs.oracle.com.javase.8.docs.api.java.lang.IllegalArgumentException?is`: if this enum type has no constant with the specified name
                :class:`~org.optaplanner.core.config.score.definition.https:.docs.oracle.com.javase.8.docs.api.java.lang.NullPointerException?is`: if the argument is null
        
        
        """
        ...
    @staticmethod
    def values() -> typing.List['ScoreDefinitionType']:
        """
            Returns an array containing the constants of this enum type, in the order they are declared. This method may be used to
            iterate over the constants as follows:
        
            .. code-block: java
            
            for (ScoreDefinitionType c : ScoreDefinitionType.values())
                System.out.println(c);
            
        
            Returns:
                an array containing the constants of this enum type, in the order they are declared
        
        
        """
        ...


class __module_protocol__(typing.Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.optaplanner.core.config.score.definition")``.

    ScoreDefinitionType: typing.Type[ScoreDefinitionType]
