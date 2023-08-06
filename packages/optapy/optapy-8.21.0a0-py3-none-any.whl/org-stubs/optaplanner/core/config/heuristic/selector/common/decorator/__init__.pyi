import java.lang
import typing



class SelectionSorterOrder(java.lang.Enum['SelectionSorterOrder']):
    """
    public enum SelectionSorterOrder extends :class:`~org.optaplanner.core.config.heuristic.selector.common.decorator.https:.docs.oracle.com.javase.8.docs.api.java.lang.Enum?is`<:class:`~org.optaplanner.core.config.heuristic.selector.common.decorator.SelectionSorterOrder`>
    
    
        Also see:
            :class:`~org.optaplanner.core.impl.heuristic.selector.common.decorator.SelectionSorter`
    """
    ASCENDING: typing.ClassVar['SelectionSorterOrder'] = ...
    DESCENDING: typing.ClassVar['SelectionSorterOrder'] = ...
    @staticmethod
    def resolve(selectionSorterOrder: 'SelectionSorterOrder') -> 'SelectionSorterOrder': ...
    _valueOf_0__T = typing.TypeVar('_valueOf_0__T', bound=java.lang.Enum)  # <T>
    @typing.overload
    @staticmethod
    def valueOf(class_: typing.Type[_valueOf_0__T], string: str) -> _valueOf_0__T: ...
    @typing.overload
    @staticmethod
    def valueOf(string: str) -> 'SelectionSorterOrder':
        """
            Returns the enum constant of this type with the specified name. The string must match *exactly* an identifier used to
            declare an enum constant in this type. (Extraneous whitespace characters are not permitted.)
        
            Parameters:
                name (:class:`~org.optaplanner.core.config.heuristic.selector.common.decorator.https:.docs.oracle.com.javase.8.docs.api.java.lang.String?is`): the name of the enum constant to be returned.
        
            Returns:
                the enum constant with the specified name
        
            Raises:
                :class:`~org.optaplanner.core.config.heuristic.selector.common.decorator.https:.docs.oracle.com.javase.8.docs.api.java.lang.IllegalArgumentException?is`: if this enum type has no constant with the specified name
                :class:`~org.optaplanner.core.config.heuristic.selector.common.decorator.https:.docs.oracle.com.javase.8.docs.api.java.lang.NullPointerException?is`: if the argument is null
        
        
        """
        ...
    @staticmethod
    def values() -> typing.List['SelectionSorterOrder']:
        """
            Returns an array containing the constants of this enum type, in the order they are declared. This method may be used to
            iterate over the constants as follows:
        
            .. code-block: java
            
            for (SelectionSorterOrder c : SelectionSorterOrder.values())
                System.out.println(c);
            
        
            Returns:
                an array containing the constants of this enum type, in the order they are declared
        
        
        """
        ...


class __module_protocol__(typing.Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.optaplanner.core.config.heuristic.selector.common.decorator")``.

    SelectionSorterOrder: typing.Type[SelectionSorterOrder]
