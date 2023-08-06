import java.lang.annotation
import typing



class ConstraintConfiguration(java.lang.annotation.Annotation):
    """
    :class:`~org.optaplanner.core.api.domain.constraintweight.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.Target?is`(:meth:`~org.optaplanner.core.api.domain.constraintweight.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.ElementType.html?is`) :class:`~org.optaplanner.core.api.domain.constraintweight.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.Retention?is`(:meth:`~org.optaplanner.core.api.domain.constraintweight.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.RetentionPolicy.html?is`) public @interface ConstraintConfiguration
    
        Allows end users to change the constraint weights, by not hard coding them. This annotation specifies that the class
        holds a number of :class:`~org.optaplanner.core.api.domain.constraintweight.ConstraintWeight` annotated members. That
        class must also have a :class:`~org.optaplanner.core.api.domain.constraintweight.ConstraintWeight` for each of the
        constraints.
    
        A :class:`~org.optaplanner.core.api.domain.solution.PlanningSolution` has at most one field or property annotated with
        :class:`~org.optaplanner.core.api.domain.constraintweight.ConstraintConfigurationProvider` with returns a type of the
        :class:`~org.optaplanner.core.api.domain.constraintweight.ConstraintConfiguration` annotated class.
    """
    def constraintPackage(self) -> str: ...
    def equals(self, object: typing.Any) -> bool: ...
    def hashCode(self) -> int: ...
    def toString(self) -> str: ...

class ConstraintConfigurationProvider(java.lang.annotation.Annotation):
    """
    :class:`~org.optaplanner.core.api.domain.constraintweight.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.Target?is`({:meth:`~org.optaplanner.core.api.domain.constraintweight.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.ElementType.html?is`,:meth:`~org.optaplanner.core.api.domain.constraintweight.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.ElementType.html?is`}) :class:`~org.optaplanner.core.api.domain.constraintweight.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.Retention?is`(:meth:`~org.optaplanner.core.api.domain.constraintweight.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.RetentionPolicy.html?is`) public @interface ConstraintConfigurationProvider
    
        Specifies that a property (or a field) on a :class:`~org.optaplanner.core.api.domain.solution.PlanningSolution` class is
        a :class:`~org.optaplanner.core.api.domain.constraintweight.ConstraintConfiguration`. This property is automatically a
        :class:`~org.optaplanner.core.api.domain.solution.ProblemFactProperty` too, so no need to declare that explicitly.
    
        The type of this property (or field) must have a
        :class:`~org.optaplanner.core.api.domain.constraintweight.ConstraintConfiguration` annotation.
    """
    def equals(self, object: typing.Any) -> bool: ...
    def hashCode(self) -> int: ...
    def toString(self) -> str: ...

class ConstraintWeight(java.lang.annotation.Annotation):
    """
    :class:`~org.optaplanner.core.api.domain.constraintweight.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.Target?is`({:meth:`~org.optaplanner.core.api.domain.constraintweight.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.ElementType.html?is`,:meth:`~org.optaplanner.core.api.domain.constraintweight.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.ElementType.html?is`}) :class:`~org.optaplanner.core.api.domain.constraintweight.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.Retention?is`(:meth:`~org.optaplanner.core.api.domain.constraintweight.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.RetentionPolicy.html?is`) public @interface ConstraintWeight
    
        Specifies that a bean property (or a field) set the constraint weight and score level of a constraint. For example, with
        a constraint weight of :code:`2soft`, a constraint match penalization with weightMultiplier :code:`3` will result in a
        :class:`~org.optaplanner.core.api.score.Score` of :code:`-6soft`.
    
        It is specified on a getter of a java bean property (or directly on a field) of a
        :class:`~org.optaplanner.core.api.domain.constraintweight.ConstraintConfiguration` class.
    """
    def constraintPackage(self) -> str: ...
    def equals(self, object: typing.Any) -> bool: ...
    def hashCode(self) -> int: ...
    def toString(self) -> str: ...
    def value(self) -> str: ...


class __module_protocol__(typing.Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.optaplanner.core.api.domain.constraintweight")``.

    ConstraintConfiguration: typing.Type[ConstraintConfiguration]
    ConstraintConfigurationProvider: typing.Type[ConstraintConfigurationProvider]
    ConstraintWeight: typing.Type[ConstraintWeight]
