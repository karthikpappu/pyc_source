# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spamfighter/rules/model.py
# Compiled at: 2009-01-30 08:10:10
"""
Правила, управляющие моделями.
"""
from spamfighter.interfaces import IModel
from spamfighter.core.commands import errors
from spamfighter.core.rules import factory
from spamfighter.core.domain import DomainKeyError
from spamfighter.core.message import AttributeNotFoundError

class ModelRule(object):
    """
    Базовый класс для правило, использующее модель анализа сообщений.

    @ivar model: модель анализа сообщений
    @type model: L{IModel}
    @ivar modelName: имя модели в домене
    @type modelName: C{str}
    @ivar text: текст сообщения
    @type text: C{unicode}
    """

    def __init__(self, model='model'):
        u"""
        Конструктор.

        @param model: имя модели в домене
        @type model: C{str}
        """
        self.modelName = model

    def analyze(self, domain, message, attribute='text'):
        u"""
        Анализ сообщения.

        @param domain: домен, относительно которого идёт анализ
        @type domain: L{IDomain}
        @param message: сообщение
        @type message: L{spamfighter.interfaces.IMessage}
        @param attribute: имя атрибута сообщения, содержащего текст
        @type attribute: C{str}
        """
        try:
            self.model = domain.get(self.modelName)
        except DomainKeyError:
            raise errors.AttributeKeyException, self.modelName

        if not IModel.providedBy(self.model):
            raise errors.NotAModelError, self.modelName
        try:
            self.text = message[attribute].value()
        except AttributeNotFoundError:
            raise errors.MessageAttributeKeyException, attribute


class modelClassify(ModelRule):
    """
    Классификация сообщения по модели: истинно, если модель сообщает, что сообщение
    относится к классу *плохих*.
    """

    def analyze(self, domain, message, **kwargs):
        super(modelClassify, self).analyze(domain, message, **kwargs)
        return self.model.classify(self.text)


class modelTrain(ModelRule):
    """
    Обучить модель на сообщении: всегда истинно.
    """

    def analyze(self, domain, message, marker='good', **kwargs):
        u"""
        @param marker: тип сообщения для модели, "good" или "bad"
        @type marker: C{str}
        """
        super(modelTrain, self).analyze(domain, message, **kwargs)
        return self.model.train(self.text, marker == 'good').addCallback(lambda _: True)


factory.registerRule(modelClassify)
factory.registerRule(modelTrain)