# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spamfighter/core/message/attribute.py
# Compiled at: 2009-01-30 08:10:10
"""
Атрибуты сообщений и их домены.
"""
from zope.interface import implements
from spamfighter.interfaces import IAttribute, IAttributeDomain
from netaddr import IP

class AttributeNotFoundError(Exception):
    """
    Атрибут по имени не был обнаружен.
    """
    pass


class AttributeDomain(object):
    """
    Домент (тип атрибута).

    @ivar _name: имя атрибута
    @type _name: C{str}
    """
    implements(IAttributeDomain)

    def __init__(self, name):
        u"""
        Конструктор.

        @param name: имя атрибута
        @type name: C{str}
        """
        self._name = name

    def name(self):
        u"""
        Получить имя атрибута.

        @return: имя атрибута
        @rtype: C{str}
        """
        return self._name

    def serialize(self, attribute):
        u"""
        Получить сериализованное значение атрибута.

        @param attribute: атрибут
        @type attribute: L{IAttribute}
        @return: сериализованное значение атрибута
        """
        raise NotImplementedError, self

    def deserialize(self, value):
        u"""
        Десериализовать значение в атрибут.

        @param value: сериализованное значение
        @return: атрибут
        @rtype: L{IAttribute}
        """
        raise NotImplementedError, self

    def __eq__(self, other):
        return isinstance(other, AttributeDomain) and self._name == other._name

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self._name)


class TextAttributeDomain(AttributeDomain):
    """
    Тип атрибута "текст сообщения". Основной тип атрибутов при анализе сообщений.
    """

    def serialize(self, attribute):
        u"""
        Получить сериализованное значение атрибута.

        Сериализованное представление - это всегда строка в utf-8.

        @param attribute: атрибут
        @type attribute: L{IAttribute}
        @return: сериализованное значение атрибута
        """
        if isinstance(attribute.value(), unicode):
            return attribute.value().encode('utf-8')
        return attribute.value()

    def deserialize(self, value):
        u"""
        Десериализовать значение в атрибут.

        @param value: сериализованное значение
        @return: атрибут
        @rtype: L{IAttribute}
        """
        if isinstance(value, unicode):
            return Attribute(self, value)
        return Attribute(self, value.decode('utf-8').strip())


class IPAttributeDomain(AttributeDomain):
    """
    Атрибут, в котором хранится IP.
    """

    def serialize(self, attribute):
        u"""
        Получить сериализованное значение атрибута.

        @param attribute: атрибут
        @type attribute: L{IAttribute}
        @return: сериализованное значение атрибута
        """
        return str(attribute.value())

    def deserialize(self, value):
        u"""
        Десериализовать значение в атрибут.

        @param value: сериализованное значение
        @return: атрибут
        @rtype: L{IAttribute}
        """
        return Attribute(self, IP(value))


class IntAttributeDomain(AttributeDomain):
    """
    Тип атрибута "целое число".
    """

    def serialize(self, attribute):
        u"""
        Получить сериализованное значение атрибута.

        Сериализованное представление - это всегда число

        @param attribute: атрибут
        @type attribute: L{IAttribute}
        @return: сериализованное значение атрибута
        """
        if not isinstance(attribute.value(), (int, long)):
            raise TypeError(attribute.value())
        return attribute.value()

    def deserialize(self, value):
        u"""
        Десериализовать значение в атрибут.

        @param value: сериализованное значение
        @return: атрибут
        @rtype: L{IAttribute}
        """
        if not isinstance(value, (int, long)):
            raise TypeError(value)
        return Attribute(self, value)


class UniqueIntAttributeDomain(IntAttributeDomain):
    """
    Уникальный атрибут, тип "целое число".
    """
    pass


class Attribute(object):
    """
    Атрибуты характеризуют отправителя и получателя сообщений, они могут нести разную информацию.

    Атрибут является частью сообщения (L{IMessage}), тип атрибута (L{IAttributeDomain}) - его свойством.

    @ivar _domain: домен атрибута
    @type _domain: L{IAttributeDomain}
    @ivar _value: значение атрибута
    """
    implements(IAttribute)

    def __init__(self, domain, value):
        u"""
        Конструктор.

        @ivar domain: домен атрибута
        @type domain: L{IAttributeDomain}
        @ivar value: значение атрибута
        """
        self._domain = domain
        self._value = value

    def domain(self):
        u"""
        Получить домен атрибута.

        @return: домен атрибута
        @rtype: L{IAttributeDomain}
        """
        return self._domain

    def value(self):
        u"""
        Получить значение атрибута.

        @return: значение атрибута
        """
        return self._value

    def serialize(self):
        u"""
        Получить сериализованное значение атрибута.

        @return: сериализованное значение атрибута
        """
        return self._domain.serialize(self)

    def __eq__(self, other):
        return isinstance(other, Attribute) and self._domain is other._domain and self._value == other._value

    def __repr__(self):
        return 'Attribute(%r, %r)' % (self._domain, self._value)