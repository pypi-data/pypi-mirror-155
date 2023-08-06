import java.lang
import typing



class RandomType(java.lang.Enum['RandomType']):
    """
    public enum RandomType extends :class:`~org.optaplanner.core.config.solver.random.https:.docs.oracle.com.javase.8.docs.api.java.lang.Enum?is`<:class:`~org.optaplanner.core.config.solver.random.RandomType`>
    
        Defines the pseudo random number generator. See the `PRNG
        <http://commons.apache.org/proper/commons-math/userguide/random.html#a2.7_PRNG_Pluggability>` documentation in
        commons-math.
    """
    JDK: typing.ClassVar['RandomType'] = ...
    MERSENNE_TWISTER: typing.ClassVar['RandomType'] = ...
    WELL512A: typing.ClassVar['RandomType'] = ...
    WELL1024A: typing.ClassVar['RandomType'] = ...
    WELL19937A: typing.ClassVar['RandomType'] = ...
    WELL19937C: typing.ClassVar['RandomType'] = ...
    WELL44497A: typing.ClassVar['RandomType'] = ...
    WELL44497B: typing.ClassVar['RandomType'] = ...
    _valueOf_0__T = typing.TypeVar('_valueOf_0__T', bound=java.lang.Enum)  # <T>
    @typing.overload
    @staticmethod
    def valueOf(class_: typing.Type[_valueOf_0__T], string: str) -> _valueOf_0__T: ...
    @typing.overload
    @staticmethod
    def valueOf(string: str) -> 'RandomType':
        """
            Returns the enum constant of this type with the specified name. The string must match *exactly* an identifier used to
            declare an enum constant in this type. (Extraneous whitespace characters are not permitted.)
        
            Parameters:
                name (:class:`~org.optaplanner.core.config.solver.random.https:.docs.oracle.com.javase.8.docs.api.java.lang.String?is`): the name of the enum constant to be returned.
        
            Returns:
                the enum constant with the specified name
        
            Raises:
                :class:`~org.optaplanner.core.config.solver.random.https:.docs.oracle.com.javase.8.docs.api.java.lang.IllegalArgumentException?is`: if this enum type has no constant with the specified name
                :class:`~org.optaplanner.core.config.solver.random.https:.docs.oracle.com.javase.8.docs.api.java.lang.NullPointerException?is`: if the argument is null
        
        
        """
        ...
    @staticmethod
    def values() -> typing.List['RandomType']:
        """
            Returns an array containing the constants of this enum type, in the order they are declared. This method may be used to
            iterate over the constants as follows:
        
            .. code-block: java
            
            for (RandomType c : RandomType.values())
                System.out.println(c);
            
        
            Returns:
                an array containing the constants of this enum type, in the order they are declared
        
        
        """
        ...


class __module_protocol__(typing.Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.optaplanner.core.config.solver.random")``.

    RandomType: typing.Type[RandomType]
