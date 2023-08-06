import java.lang
import org.optaplanner.core.config.heuristic.selector.common.decorator
import org.optaplanner.core.config.heuristic.selector.common.nearby
import typing



class SelectionCacheType(java.lang.Enum['SelectionCacheType']):
    """
    public enum SelectionCacheType extends :class:`~org.optaplanner.core.config.heuristic.selector.common.https:.docs.oracle.com.javase.8.docs.api.java.lang.Enum?is`<:class:`~org.optaplanner.core.config.heuristic.selector.common.SelectionCacheType`>
    
        There is no INHERIT by design because 2 sequential caches provides no benefit, only memory overhead.
    """
    JUST_IN_TIME: typing.ClassVar['SelectionCacheType'] = ...
    STEP: typing.ClassVar['SelectionCacheType'] = ...
    PHASE: typing.ClassVar['SelectionCacheType'] = ...
    SOLVER: typing.ClassVar['SelectionCacheType'] = ...
    def isCached(self) -> bool: ...
    def isNotCached(self) -> bool: ...
    @staticmethod
    def max(selectionCacheType: 'SelectionCacheType', selectionCacheType2: 'SelectionCacheType') -> 'SelectionCacheType': ...
    @staticmethod
    def resolve(selectionCacheType: 'SelectionCacheType', selectionCacheType2: 'SelectionCacheType') -> 'SelectionCacheType': ...
    _valueOf_0__T = typing.TypeVar('_valueOf_0__T', bound=java.lang.Enum)  # <T>
    @typing.overload
    @staticmethod
    def valueOf(class_: typing.Type[_valueOf_0__T], string: str) -> _valueOf_0__T: ...
    @typing.overload
    @staticmethod
    def valueOf(string: str) -> 'SelectionCacheType':
        """
            Returns the enum constant of this type with the specified name. The string must match *exactly* an identifier used to
            declare an enum constant in this type. (Extraneous whitespace characters are not permitted.)
        
            Parameters:
                name (:class:`~org.optaplanner.core.config.heuristic.selector.common.https:.docs.oracle.com.javase.8.docs.api.java.lang.String?is`): the name of the enum constant to be returned.
        
            Returns:
                the enum constant with the specified name
        
            Raises:
                :class:`~org.optaplanner.core.config.heuristic.selector.common.https:.docs.oracle.com.javase.8.docs.api.java.lang.IllegalArgumentException?is`: if this enum type has no constant with the specified name
                :class:`~org.optaplanner.core.config.heuristic.selector.common.https:.docs.oracle.com.javase.8.docs.api.java.lang.NullPointerException?is`: if the argument is null
        
        
        """
        ...
    @staticmethod
    def values() -> typing.List['SelectionCacheType']:
        """
            Returns an array containing the constants of this enum type, in the order they are declared. This method may be used to
            iterate over the constants as follows:
        
            .. code-block: java
            
            for (SelectionCacheType c : SelectionCacheType.values())
                System.out.println(c);
            
        
            Returns:
                an array containing the constants of this enum type, in the order they are declared
        
        
        """
        ...

class SelectionOrder(java.lang.Enum['SelectionOrder']):
    """
    public enum SelectionOrder extends :class:`~org.optaplanner.core.config.heuristic.selector.common.https:.docs.oracle.com.javase.8.docs.api.java.lang.Enum?is`<:class:`~org.optaplanner.core.config.heuristic.selector.common.SelectionOrder`>
    
        Defines in which order the elements or a selector are selected.
    """
    INHERIT: typing.ClassVar['SelectionOrder'] = ...
    ORIGINAL: typing.ClassVar['SelectionOrder'] = ...
    SORTED: typing.ClassVar['SelectionOrder'] = ...
    RANDOM: typing.ClassVar['SelectionOrder'] = ...
    SHUFFLED: typing.ClassVar['SelectionOrder'] = ...
    PROBABILISTIC: typing.ClassVar['SelectionOrder'] = ...
    @staticmethod
    def fromRandomSelectionBoolean(boolean: bool) -> 'SelectionOrder': ...
    @staticmethod
    def resolve(selectionOrder: 'SelectionOrder', selectionOrder2: 'SelectionOrder') -> 'SelectionOrder':
        """
        
            Parameters:
                selectionOrder (:class:`~org.optaplanner.core.config.heuristic.selector.common.SelectionOrder`): sometimes null
                inheritedSelectionOrder (:class:`~org.optaplanner.core.config.heuristic.selector.common.SelectionOrder`): never null
        
            Returns:
                never null
        
        
        """
        ...
    def toRandomSelectionBoolean(self) -> bool: ...
    _valueOf_0__T = typing.TypeVar('_valueOf_0__T', bound=java.lang.Enum)  # <T>
    @typing.overload
    @staticmethod
    def valueOf(class_: typing.Type[_valueOf_0__T], string: str) -> _valueOf_0__T: ...
    @typing.overload
    @staticmethod
    def valueOf(string: str) -> 'SelectionOrder':
        """
            Returns the enum constant of this type with the specified name. The string must match *exactly* an identifier used to
            declare an enum constant in this type. (Extraneous whitespace characters are not permitted.)
        
            Parameters:
                name (:class:`~org.optaplanner.core.config.heuristic.selector.common.https:.docs.oracle.com.javase.8.docs.api.java.lang.String?is`): the name of the enum constant to be returned.
        
            Returns:
                the enum constant with the specified name
        
            Raises:
                :class:`~org.optaplanner.core.config.heuristic.selector.common.https:.docs.oracle.com.javase.8.docs.api.java.lang.IllegalArgumentException?is`: if this enum type has no constant with the specified name
                :class:`~org.optaplanner.core.config.heuristic.selector.common.https:.docs.oracle.com.javase.8.docs.api.java.lang.NullPointerException?is`: if the argument is null
        
        
        """
        ...
    @staticmethod
    def values() -> typing.List['SelectionOrder']:
        """
            Returns an array containing the constants of this enum type, in the order they are declared. This method may be used to
            iterate over the constants as follows:
        
            .. code-block: java
            
            for (SelectionOrder c : SelectionOrder.values())
                System.out.println(c);
            
        
            Returns:
                an array containing the constants of this enum type, in the order they are declared
        
        
        """
        ...


class __module_protocol__(typing.Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.optaplanner.core.config.heuristic.selector.common")``.

    SelectionCacheType: typing.Type[SelectionCacheType]
    SelectionOrder: typing.Type[SelectionOrder]
    decorator: org.optaplanner.core.config.heuristic.selector.common.decorator.__module_protocol__
    nearby: org.optaplanner.core.config.heuristic.selector.common.nearby.__module_protocol__
