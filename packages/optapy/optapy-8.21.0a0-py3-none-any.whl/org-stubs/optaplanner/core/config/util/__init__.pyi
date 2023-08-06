import java.lang.annotation
import java.lang.reflect
import java.util
import java.util.function
import org.optaplanner.core.api.domain.common
import org.optaplanner.core.config
import org.optaplanner.core.impl.domain.common.accessor
import typing



class ConfigUtils:
    """
    public class ConfigUtils extends :class:`~org.optaplanner.core.config.util.https:.docs.oracle.com.javase.8.docs.api.java.lang.Object?is`
    """
    @typing.overload
    @staticmethod
    def abbreviate(list: java.util.List[str]) -> str: ...
    @typing.overload
    @staticmethod
    def abbreviate(list: java.util.List[str], int: int) -> str: ...
    @staticmethod
    def applyCustomProperties(object: typing.Any, string: str, map: typing.Union[java.util.Map[str, str], typing.Mapping[str, str]], string2: str) -> None: ...
    @staticmethod
    def ceilDivide(int: int, int2: int) -> int:
        """
            Divides and ceils the result without using floating point arithmetic. For floor division, see
            :meth:`~org.optaplanner.core.config.util.https:.docs.oracle.com.javase.8.docs.api.java.lang.Math.html?is`.
        
            Parameters:
                dividend (int): the dividend
                divisor (int): the divisor
        
            Returns:
                dividend / divisor, ceiled
        
            Raises:
                :class:`~org.optaplanner.core.config.util.https:.docs.oracle.com.javase.8.docs.api.java.lang.ArithmeticException?is`: if :code:`divisor == 0`
        
        
        """
        ...
    @staticmethod
    def extractAnnotationClass(member: java.lang.reflect.Member, *class_: typing.Type[java.lang.annotation.Annotation]) -> typing.Type[java.lang.annotation.Annotation]: ...
    @staticmethod
    def extractCollectionGenericTypeParameterLeniently(string: str, class_: typing.Type[typing.Any], class2: typing.Type[typing.Any], type: java.lang.reflect.Type, class3: typing.Type[java.lang.annotation.Annotation], string2: str) -> typing.Type[typing.Any]: ...
    @staticmethod
    def extractCollectionGenericTypeParameterStrictly(string: str, class_: typing.Type[typing.Any], class2: typing.Type[typing.Any], type: java.lang.reflect.Type, class3: typing.Type[java.lang.annotation.Annotation], string2: str) -> typing.Type[typing.Any]: ...
    _findPlanningIdMemberAccessor__C = typing.TypeVar('_findPlanningIdMemberAccessor__C')  # <C>
    @staticmethod
    def findPlanningIdMemberAccessor(class_: typing.Type[_findPlanningIdMemberAccessor__C], domainAccessType: org.optaplanner.core.api.domain.common.DomainAccessType, map: typing.Union[java.util.Map[str, org.optaplanner.core.impl.domain.common.accessor.MemberAccessor], typing.Mapping[str, org.optaplanner.core.impl.domain.common.accessor.MemberAccessor]]) -> org.optaplanner.core.impl.domain.common.accessor.MemberAccessor: ...
    @staticmethod
    def getAllAnnotatedLineageClasses(class_: typing.Type[typing.Any], class2: typing.Type[java.lang.annotation.Annotation]) -> java.util.List[typing.Type[typing.Any]]: ...
    @staticmethod
    def getAllMembers(class_: typing.Type[typing.Any], class2: typing.Type[java.lang.annotation.Annotation]) -> java.util.List[java.lang.reflect.Member]: ...
    @staticmethod
    def getDeclaredMembers(class_: typing.Type[typing.Any]) -> java.util.List[java.lang.reflect.Member]: ...
    _inheritConfig__Config_ = typing.TypeVar('_inheritConfig__Config_', bound=org.optaplanner.core.config.AbstractConfig)  # <Config_>
    @staticmethod
    def inheritConfig(config_: _inheritConfig__Config_, config_2: _inheritConfig__Config_) -> _inheritConfig__Config_: ...
    _inheritMergeableListConfig__Config_ = typing.TypeVar('_inheritMergeableListConfig__Config_', bound=org.optaplanner.core.config.AbstractConfig)  # <Config_>
    @staticmethod
    def inheritMergeableListConfig(list: java.util.List[_inheritMergeableListConfig__Config_], list2: java.util.List[_inheritMergeableListConfig__Config_]) -> java.util.List[_inheritMergeableListConfig__Config_]: ...
    _inheritMergeableListProperty__T = typing.TypeVar('_inheritMergeableListProperty__T')  # <T>
    @staticmethod
    def inheritMergeableListProperty(list: java.util.List[_inheritMergeableListProperty__T], list2: java.util.List[_inheritMergeableListProperty__T]) -> java.util.List[_inheritMergeableListProperty__T]: ...
    _inheritMergeableMapProperty__K = typing.TypeVar('_inheritMergeableMapProperty__K')  # <K>
    _inheritMergeableMapProperty__T = typing.TypeVar('_inheritMergeableMapProperty__T')  # <T>
    @staticmethod
    def inheritMergeableMapProperty(map: typing.Union[java.util.Map[_inheritMergeableMapProperty__K, _inheritMergeableMapProperty__T], typing.Mapping[_inheritMergeableMapProperty__K, _inheritMergeableMapProperty__T]], map2: typing.Union[java.util.Map[_inheritMergeableMapProperty__K, _inheritMergeableMapProperty__T], typing.Mapping[_inheritMergeableMapProperty__K, _inheritMergeableMapProperty__T]]) -> java.util.Map[_inheritMergeableMapProperty__K, _inheritMergeableMapProperty__T]: ...
    _inheritOverwritableProperty__T = typing.TypeVar('_inheritOverwritableProperty__T')  # <T>
    @staticmethod
    def inheritOverwritableProperty(t: _inheritOverwritableProperty__T, t2: _inheritOverwritableProperty__T) -> _inheritOverwritableProperty__T: ...
    @staticmethod
    def isEmptyCollection(collection: typing.Union[java.util.Collection[typing.Any], typing.Sequence[typing.Any], typing.Set[typing.Any]]) -> bool: ...
    @staticmethod
    def isNativeImage() -> bool: ...
    _meldProperty__T = typing.TypeVar('_meldProperty__T')  # <T>
    @staticmethod
    def meldProperty(t: _meldProperty__T, t2: _meldProperty__T) -> _meldProperty__T:
        """
            A relaxed version of :meth:`~org.optaplanner.core.config.util.ConfigUtils.mergeProperty`. Used primarily for merging
            failed benchmarks, where a property remains the same over benchmark runs (for example: dataset problem size), but the
            property in the failed benchmark isn't initialized, therefore null. When merging, we can still use the correctly
            initialized property of the benchmark that didn't fail.
        
            Null-handling:
        
              - if **both** properties **are null**, returns null
              - if **only one** of the properties **is not null**, returns that property
              - if **both** properties **are not null**, returns :meth:`~org.optaplanner.core.config.util.ConfigUtils.mergeProperty`
        
        
            Parameters:
                a (T): property :code:`a`
                b (T): property :code:`b`
        
            Returns:
                sometimes null
        
            Also see:
                :meth:`~org.optaplanner.core.config.util.ConfigUtils.mergeProperty`
        
        
        """
        ...
    _mergeProperty__T = typing.TypeVar('_mergeProperty__T')  # <T>
    @staticmethod
    def mergeProperty(t: _mergeProperty__T, t2: _mergeProperty__T) -> _mergeProperty__T: ...
    _newInstance_0__T = typing.TypeVar('_newInstance_0__T')  # <T>
    _newInstance_1__T = typing.TypeVar('_newInstance_1__T')  # <T>
    @typing.overload
    @staticmethod
    def newInstance(object: typing.Any, string: str, class_: typing.Type[_newInstance_0__T]) -> _newInstance_0__T:
        """
            Create a new instance of clazz from a config's property.
        
            If the instantiation fails, the simple class name of :code:`configBean` will be used as the owner of
            :code:`propertyName`.
        
            Intended usage:
        
            .. code-block: java
            
             selectionFilter = ConfigUtils.newInstance(
                     config, "filterClass", config.getFilterClass());
             
        
            Parameters:
                configBean (:class:`~org.optaplanner.core.config.util.https:.docs.oracle.com.javase.8.docs.api.java.lang.Object?is`): the bean holding the :code:`clazz` to be instantiated
                propertyName (:class:`~org.optaplanner.core.config.util.https:.docs.oracle.com.javase.8.docs.api.java.lang.String?is`): :code:`configBean`'s property holding :code:`clazz`
                clazz (:class:`~org.optaplanner.core.config.util.https:.docs.oracle.com.javase.8.docs.api.java.lang.Class?is`<T> clazz): :code:`Class` representation of the type :code:`T`
        
            Returns:
                new instance of clazz
        
        public static <T> T newInstance (:class:`~org.optaplanner.core.config.util.https:.docs.oracle.com.javase.8.docs.api.java.util.function.Supplier?is`<:class:`~org.optaplanner.core.config.util.https:.docs.oracle.com.javase.8.docs.api.java.lang.String?is`> ownerDescriptor, :class:`~org.optaplanner.core.config.util.https:.docs.oracle.com.javase.8.docs.api.java.lang.String?is` propertyName, :class:`~org.optaplanner.core.config.util.https:.docs.oracle.com.javase.8.docs.api.java.lang.Class?is`<T> clazz)
        
            Create a new instance of clazz from a general source.
        
            If the instantiation fails, the result of :code:`ownerDescriptor` will be used to describe the owner of
            :code:`propertyName`.
        
            Parameters:
                ownerDescriptor (:class:`~org.optaplanner.core.config.util.https:.docs.oracle.com.javase.8.docs.api.java.util.function.Supplier?is`<:class:`~org.optaplanner.core.config.util.https:.docs.oracle.com.javase.8.docs.api.java.lang.String?is`> ownerDescriptor): describes the owner of :code:`propertyName`
                propertyName (:class:`~org.optaplanner.core.config.util.https:.docs.oracle.com.javase.8.docs.api.java.lang.String?is`): property holding the :code:`clazz`
                clazz (:class:`~org.optaplanner.core.config.util.https:.docs.oracle.com.javase.8.docs.api.java.lang.Class?is`<T> clazz): :code:`Class` representation of the type :code:`T`
        
            Returns:
                new instance of clazz
        
        
        """
        ...
    @typing.overload
    @staticmethod
    def newInstance(supplier: typing.Union[java.util.function.Supplier[str], typing.Callable[[], str]], string: str, class_: typing.Type[_newInstance_1__T]) -> _newInstance_1__T: ...
    @staticmethod
    def resolvePoolSize(string: str, string2: str, *string3: str) -> int: ...


class __module_protocol__(typing.Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.optaplanner.core.config.util")``.

    ConfigUtils: typing.Type[ConfigUtils]
