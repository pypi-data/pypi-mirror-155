import java.lang
import java.util
import java.util.function
import org.optaplanner.core.config.heuristic.selector.entity
import org.optaplanner.core.config.heuristic.selector.entity.pillar
import org.optaplanner.core.config.heuristic.selector.move
import org.optaplanner.core.config.heuristic.selector.move.generic.chained
import org.optaplanner.core.config.heuristic.selector.value
import typing



_AbstractPillarMoveSelectorConfig__Config_ = typing.TypeVar('_AbstractPillarMoveSelectorConfig__Config_', bound='AbstractPillarMoveSelectorConfig')  # <Config_>
class AbstractPillarMoveSelectorConfig(org.optaplanner.core.config.heuristic.selector.move.MoveSelectorConfig[_AbstractPillarMoveSelectorConfig__Config_], typing.Generic[_AbstractPillarMoveSelectorConfig__Config_]):
    """
    public abstract class AbstractPillarMoveSelectorConfig<Config_ extends AbstractPillarMoveSelectorConfig<Config_>> extends :class:`~org.optaplanner.core.config.heuristic.selector.move.MoveSelectorConfig`<Config_>
    """
    def __init__(self): ...
    def getPillarSelectorConfig(self) -> org.optaplanner.core.config.heuristic.selector.entity.pillar.PillarSelectorConfig: ...
    def getSubPillarSequenceComparatorClass(self) -> typing.Type[java.util.Comparator]: ...
    def getSubPillarType(self) -> 'SubPillarType': ...
    def inherit(self, config_: _AbstractPillarMoveSelectorConfig__Config_) -> _AbstractPillarMoveSelectorConfig__Config_:
        """
            Description copied from class: :meth:`~org.optaplanner.core.config.AbstractConfig.inherit`
            Inherits each property of the :code:`inheritedConfig` unless that property (or a semantic alternative) is defined by
            this instance (which overwrites the inherited behaviour).
        
            After the inheritance, if a property on this :class:`~org.optaplanner.core.config.AbstractConfig` composition is
            replaced, it should not affect the inherited composition instance.
        
            Overrides:
                :meth:`~org.optaplanner.core.config.heuristic.selector.move.MoveSelectorConfig.inherit` in
                class :class:`~org.optaplanner.core.config.heuristic.selector.move.MoveSelectorConfig`
        
            Parameters:
                inheritedConfig (:class:`~org.optaplanner.core.config.heuristic.selector.move.generic.AbstractPillarMoveSelectorConfig`): never null
        
            Returns:
                this
        
        
        """
        ...
    def setPillarSelectorConfig(self, pillarSelectorConfig: org.optaplanner.core.config.heuristic.selector.entity.pillar.PillarSelectorConfig) -> None: ...
    def setSubPillarSequenceComparatorClass(self, class_: typing.Type[java.util.Comparator]) -> None: ...
    def setSubPillarType(self, subPillarType: 'SubPillarType') -> None: ...

class ChangeMoveSelectorConfig(org.optaplanner.core.config.heuristic.selector.move.MoveSelectorConfig['ChangeMoveSelectorConfig']):
    """
    public class ChangeMoveSelectorConfig extends :class:`~org.optaplanner.core.config.heuristic.selector.move.MoveSelectorConfig`<:class:`~org.optaplanner.core.config.heuristic.selector.move.generic.ChangeMoveSelectorConfig`>
    """
    XML_ELEMENT_NAME: typing.ClassVar[str] = ...
    """
    public static final :class:`~org.optaplanner.core.config.heuristic.selector.move.generic.https:.docs.oracle.com.javase.8.docs.api.java.lang.String?is` XML_ELEMENT_NAME
    
    
        Also see:
            :meth:`~constant`
    
    
    """
    def __init__(self): ...
    def copyConfig(self) -> 'ChangeMoveSelectorConfig':
        """
            Description copied from class: :meth:`~org.optaplanner.core.config.AbstractConfig.copyConfig`
            Typically implemented by constructing a new instance and calling
            :meth:`~org.optaplanner.core.config.AbstractConfig.inherit` on it
        
            Specified by:
                :meth:`~org.optaplanner.core.config.AbstractConfig.copyConfig` in
                class :class:`~org.optaplanner.core.config.AbstractConfig`
        
            Returns:
                new instance
        
        
        """
        ...
    def getEntitySelectorConfig(self) -> org.optaplanner.core.config.heuristic.selector.entity.EntitySelectorConfig: ...
    def getValueSelectorConfig(self) -> org.optaplanner.core.config.heuristic.selector.value.ValueSelectorConfig: ...
    def inherit(self, changeMoveSelectorConfig: 'ChangeMoveSelectorConfig') -> 'ChangeMoveSelectorConfig':
        """
            Description copied from class: :meth:`~org.optaplanner.core.config.AbstractConfig.inherit`
            Inherits each property of the :code:`inheritedConfig` unless that property (or a semantic alternative) is defined by
            this instance (which overwrites the inherited behaviour).
        
            After the inheritance, if a property on this :class:`~org.optaplanner.core.config.AbstractConfig` composition is
            replaced, it should not affect the inherited composition instance.
        
            Overrides:
                :meth:`~org.optaplanner.core.config.heuristic.selector.move.MoveSelectorConfig.inherit` in
                class :class:`~org.optaplanner.core.config.heuristic.selector.move.MoveSelectorConfig`
        
            Parameters:
                inheritedConfig (:class:`~org.optaplanner.core.config.heuristic.selector.move.generic.ChangeMoveSelectorConfig`): never null
        
            Returns:
                this
        
        
        """
        ...
    def setEntitySelectorConfig(self, entitySelectorConfig: org.optaplanner.core.config.heuristic.selector.entity.EntitySelectorConfig) -> None: ...
    def setValueSelectorConfig(self, valueSelectorConfig: org.optaplanner.core.config.heuristic.selector.value.ValueSelectorConfig) -> None: ...
    def toString(self) -> str:
        """
        
            Overrides:
                :meth:`~org.optaplanner.core.config.AbstractConfig.toString` in
                class :class:`~org.optaplanner.core.config.AbstractConfig`
        
        
        """
        ...
    def visitReferencedClasses(self, consumer: typing.Union[java.util.function.Consumer[typing.Type[typing.Any]], typing.Callable[[typing.Type[typing.Any]], None]]) -> None: ...

class SubPillarType(java.lang.Enum['SubPillarType']):
    """
    public enum SubPillarType extends :class:`~org.optaplanner.core.config.heuristic.selector.move.generic.https:.docs.oracle.com.javase.8.docs.api.java.lang.Enum?is`<:class:`~org.optaplanner.core.config.heuristic.selector.move.generic.SubPillarType`>
    """
    NONE: typing.ClassVar['SubPillarType'] = ...
    SEQUENCE: typing.ClassVar['SubPillarType'] = ...
    ALL: typing.ClassVar['SubPillarType'] = ...
    _valueOf_0__T = typing.TypeVar('_valueOf_0__T', bound=java.lang.Enum)  # <T>
    @typing.overload
    @staticmethod
    def valueOf(class_: typing.Type[_valueOf_0__T], string: str) -> _valueOf_0__T: ...
    @typing.overload
    @staticmethod
    def valueOf(string: str) -> 'SubPillarType':
        """
            Returns the enum constant of this type with the specified name. The string must match *exactly* an identifier used to
            declare an enum constant in this type. (Extraneous whitespace characters are not permitted.)
        
            Parameters:
                name (:class:`~org.optaplanner.core.config.heuristic.selector.move.generic.https:.docs.oracle.com.javase.8.docs.api.java.lang.String?is`): the name of the enum constant to be returned.
        
            Returns:
                the enum constant with the specified name
        
            Raises:
                :class:`~org.optaplanner.core.config.heuristic.selector.move.generic.https:.docs.oracle.com.javase.8.docs.api.java.lang.IllegalArgumentException?is`: if this enum type has no constant with the specified name
                :class:`~org.optaplanner.core.config.heuristic.selector.move.generic.https:.docs.oracle.com.javase.8.docs.api.java.lang.NullPointerException?is`: if the argument is null
        
        
        """
        ...
    @staticmethod
    def values() -> typing.List['SubPillarType']:
        """
            Returns an array containing the constants of this enum type, in the order they are declared. This method may be used to
            iterate over the constants as follows:
        
            .. code-block: java
            
            for (SubPillarType c : SubPillarType.values())
                System.out.println(c);
            
        
            Returns:
                an array containing the constants of this enum type, in the order they are declared
        
        
        """
        ...

class SwapMoveSelectorConfig(org.optaplanner.core.config.heuristic.selector.move.MoveSelectorConfig['SwapMoveSelectorConfig']):
    """
    public class SwapMoveSelectorConfig extends :class:`~org.optaplanner.core.config.heuristic.selector.move.MoveSelectorConfig`<:class:`~org.optaplanner.core.config.heuristic.selector.move.generic.SwapMoveSelectorConfig`>
    """
    XML_ELEMENT_NAME: typing.ClassVar[str] = ...
    """
    public static final :class:`~org.optaplanner.core.config.heuristic.selector.move.generic.https:.docs.oracle.com.javase.8.docs.api.java.lang.String?is` XML_ELEMENT_NAME
    
    
        Also see:
            :meth:`~constant`
    
    
    """
    def __init__(self): ...
    def copyConfig(self) -> 'SwapMoveSelectorConfig':
        """
            Description copied from class: :meth:`~org.optaplanner.core.config.AbstractConfig.copyConfig`
            Typically implemented by constructing a new instance and calling
            :meth:`~org.optaplanner.core.config.AbstractConfig.inherit` on it
        
            Specified by:
                :meth:`~org.optaplanner.core.config.AbstractConfig.copyConfig` in
                class :class:`~org.optaplanner.core.config.AbstractConfig`
        
            Returns:
                new instance
        
        
        """
        ...
    def getEntitySelectorConfig(self) -> org.optaplanner.core.config.heuristic.selector.entity.EntitySelectorConfig: ...
    def getSecondaryEntitySelectorConfig(self) -> org.optaplanner.core.config.heuristic.selector.entity.EntitySelectorConfig: ...
    def getVariableNameIncludeList(self) -> java.util.List[str]: ...
    def inherit(self, swapMoveSelectorConfig: 'SwapMoveSelectorConfig') -> 'SwapMoveSelectorConfig':
        """
            Description copied from class: :meth:`~org.optaplanner.core.config.AbstractConfig.inherit`
            Inherits each property of the :code:`inheritedConfig` unless that property (or a semantic alternative) is defined by
            this instance (which overwrites the inherited behaviour).
        
            After the inheritance, if a property on this :class:`~org.optaplanner.core.config.AbstractConfig` composition is
            replaced, it should not affect the inherited composition instance.
        
            Overrides:
                :meth:`~org.optaplanner.core.config.heuristic.selector.move.MoveSelectorConfig.inherit` in
                class :class:`~org.optaplanner.core.config.heuristic.selector.move.MoveSelectorConfig`
        
            Parameters:
                inheritedConfig (:class:`~org.optaplanner.core.config.heuristic.selector.move.generic.SwapMoveSelectorConfig`): never null
        
            Returns:
                this
        
        
        """
        ...
    def setEntitySelectorConfig(self, entitySelectorConfig: org.optaplanner.core.config.heuristic.selector.entity.EntitySelectorConfig) -> None: ...
    def setSecondaryEntitySelectorConfig(self, entitySelectorConfig: org.optaplanner.core.config.heuristic.selector.entity.EntitySelectorConfig) -> None: ...
    def setVariableNameIncludeList(self, list: java.util.List[str]) -> None: ...
    def toString(self) -> str:
        """
        
            Overrides:
                :meth:`~org.optaplanner.core.config.AbstractConfig.toString` in
                class :class:`~org.optaplanner.core.config.AbstractConfig`
        
        
        """
        ...
    def visitReferencedClasses(self, consumer: typing.Union[java.util.function.Consumer[typing.Type[typing.Any]], typing.Callable[[typing.Type[typing.Any]], None]]) -> None: ...

class PillarChangeMoveSelectorConfig(AbstractPillarMoveSelectorConfig['PillarChangeMoveSelectorConfig']):
    """
    public class PillarChangeMoveSelectorConfig extends :class:`~org.optaplanner.core.config.heuristic.selector.move.generic.AbstractPillarMoveSelectorConfig`<:class:`~org.optaplanner.core.config.heuristic.selector.move.generic.PillarChangeMoveSelectorConfig`>
    """
    XML_ELEMENT_NAME: typing.ClassVar[str] = ...
    """
    public static final :class:`~org.optaplanner.core.config.heuristic.selector.move.generic.https:.docs.oracle.com.javase.8.docs.api.java.lang.String?is` XML_ELEMENT_NAME
    
    
        Also see:
            :meth:`~constant`
    
    
    """
    def __init__(self): ...
    def copyConfig(self) -> 'PillarChangeMoveSelectorConfig':
        """
            Description copied from class: :meth:`~org.optaplanner.core.config.AbstractConfig.copyConfig`
            Typically implemented by constructing a new instance and calling
            :meth:`~org.optaplanner.core.config.AbstractConfig.inherit` on it
        
            Specified by:
                :meth:`~org.optaplanner.core.config.AbstractConfig.copyConfig` in
                class :class:`~org.optaplanner.core.config.AbstractConfig`
        
            Returns:
                new instance
        
        
        """
        ...
    def getValueSelectorConfig(self) -> org.optaplanner.core.config.heuristic.selector.value.ValueSelectorConfig: ...
    def inherit(self, pillarChangeMoveSelectorConfig: 'PillarChangeMoveSelectorConfig') -> 'PillarChangeMoveSelectorConfig':
        """
            Description copied from class: :meth:`~org.optaplanner.core.config.AbstractConfig.inherit`
            Inherits each property of the :code:`inheritedConfig` unless that property (or a semantic alternative) is defined by
            this instance (which overwrites the inherited behaviour).
        
            After the inheritance, if a property on this :class:`~org.optaplanner.core.config.AbstractConfig` composition is
            replaced, it should not affect the inherited composition instance.
        
            Overrides:
                :meth:`~org.optaplanner.core.config.heuristic.selector.move.generic.AbstractPillarMoveSelectorConfig.inherit` in
                class :class:`~org.optaplanner.core.config.heuristic.selector.move.generic.AbstractPillarMoveSelectorConfig`
        
            Parameters:
                inheritedConfig (:class:`~org.optaplanner.core.config.heuristic.selector.move.generic.PillarChangeMoveSelectorConfig`): never null
        
            Returns:
                this
        
        
        """
        ...
    def setValueSelectorConfig(self, valueSelectorConfig: org.optaplanner.core.config.heuristic.selector.value.ValueSelectorConfig) -> None: ...
    def toString(self) -> str:
        """
        
            Overrides:
                :meth:`~org.optaplanner.core.config.AbstractConfig.toString` in
                class :class:`~org.optaplanner.core.config.AbstractConfig`
        
        
        """
        ...
    def visitReferencedClasses(self, consumer: typing.Union[java.util.function.Consumer[typing.Type[typing.Any]], typing.Callable[[typing.Type[typing.Any]], None]]) -> None: ...

class PillarSwapMoveSelectorConfig(AbstractPillarMoveSelectorConfig['PillarSwapMoveSelectorConfig']):
    """
    public class PillarSwapMoveSelectorConfig extends :class:`~org.optaplanner.core.config.heuristic.selector.move.generic.AbstractPillarMoveSelectorConfig`<:class:`~org.optaplanner.core.config.heuristic.selector.move.generic.PillarSwapMoveSelectorConfig`>
    """
    XML_ELEMENT_NAME: typing.ClassVar[str] = ...
    """
    public static final :class:`~org.optaplanner.core.config.heuristic.selector.move.generic.https:.docs.oracle.com.javase.8.docs.api.java.lang.String?is` XML_ELEMENT_NAME
    
    
        Also see:
            :meth:`~constant`
    
    
    """
    def __init__(self): ...
    def copyConfig(self) -> 'PillarSwapMoveSelectorConfig':
        """
            Description copied from class: :meth:`~org.optaplanner.core.config.AbstractConfig.copyConfig`
            Typically implemented by constructing a new instance and calling
            :meth:`~org.optaplanner.core.config.AbstractConfig.inherit` on it
        
            Specified by:
                :meth:`~org.optaplanner.core.config.AbstractConfig.copyConfig` in
                class :class:`~org.optaplanner.core.config.AbstractConfig`
        
            Returns:
                new instance
        
        
        """
        ...
    def getSecondaryPillarSelectorConfig(self) -> org.optaplanner.core.config.heuristic.selector.entity.pillar.PillarSelectorConfig: ...
    def getVariableNameIncludeList(self) -> java.util.List[str]: ...
    def inherit(self, pillarSwapMoveSelectorConfig: 'PillarSwapMoveSelectorConfig') -> 'PillarSwapMoveSelectorConfig':
        """
            Description copied from class: :meth:`~org.optaplanner.core.config.AbstractConfig.inherit`
            Inherits each property of the :code:`inheritedConfig` unless that property (or a semantic alternative) is defined by
            this instance (which overwrites the inherited behaviour).
        
            After the inheritance, if a property on this :class:`~org.optaplanner.core.config.AbstractConfig` composition is
            replaced, it should not affect the inherited composition instance.
        
            Overrides:
                :meth:`~org.optaplanner.core.config.heuristic.selector.move.generic.AbstractPillarMoveSelectorConfig.inherit` in
                class :class:`~org.optaplanner.core.config.heuristic.selector.move.generic.AbstractPillarMoveSelectorConfig`
        
            Parameters:
                inheritedConfig (:class:`~org.optaplanner.core.config.heuristic.selector.move.generic.PillarSwapMoveSelectorConfig`): never null
        
            Returns:
                this
        
        
        """
        ...
    def setSecondaryPillarSelectorConfig(self, pillarSelectorConfig: org.optaplanner.core.config.heuristic.selector.entity.pillar.PillarSelectorConfig) -> None: ...
    def setVariableNameIncludeList(self, list: java.util.List[str]) -> None: ...
    def toString(self) -> str:
        """
        
            Overrides:
                :meth:`~org.optaplanner.core.config.AbstractConfig.toString` in
                class :class:`~org.optaplanner.core.config.AbstractConfig`
        
        
        """
        ...
    def visitReferencedClasses(self, consumer: typing.Union[java.util.function.Consumer[typing.Type[typing.Any]], typing.Callable[[typing.Type[typing.Any]], None]]) -> None: ...


class __module_protocol__(typing.Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.optaplanner.core.config.heuristic.selector.move.generic")``.

    AbstractPillarMoveSelectorConfig: typing.Type[AbstractPillarMoveSelectorConfig]
    ChangeMoveSelectorConfig: typing.Type[ChangeMoveSelectorConfig]
    PillarChangeMoveSelectorConfig: typing.Type[PillarChangeMoveSelectorConfig]
    PillarSwapMoveSelectorConfig: typing.Type[PillarSwapMoveSelectorConfig]
    SubPillarType: typing.Type[SubPillarType]
    SwapMoveSelectorConfig: typing.Type[SwapMoveSelectorConfig]
    chained: org.optaplanner.core.config.heuristic.selector.move.generic.chained.__module_protocol__
