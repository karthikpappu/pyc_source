# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gerardo/Projects/nlp_model_gen/nlp_model_gen/packages/taskManager/TaskManager.py
# Compiled at: 2019-07-04 20:26:01
# Size of source mod 2**32: 11181 bytes
from threading import Lock
from nlp_model_gen.packages.logger.Logger import Logger
from nlp_model_gen.packages.errorHandler.ErrorHandler import ErrorHandler
from nlp_model_gen.packages.logger.assets.logColors import HIGHLIGHT_COLOR
from nlp_model_gen.constants.constants import TASK_STATUS_QUEUED, TASK_STATUS_RUNNING
from nlp_model_gen.base import MAX_CONCURRENT_TASKS
from nlp_model_gen.utils.classUtills import Observer
from .modelCreationTask.ModelCreationTask import ModelCreationTask
from .modelTrainingTask.ModelTrainingTask import ModelTrainingTask
from .textAnalysisTask.TextAnalysisTask import TextAnalysisTask
from .filesAnalysisTask.FilesAnalysisTask import FilesAnalysisTask

class TaskManager(Observer):

    def __init__(self):
        Observer.__init__(self)
        self._TaskManager__active_tasks = list([])
        self._TaskManager__completed_tasks = list([])
        self._TaskManager__last_id = 0
        self._TaskManager__lock = Lock()

    def update(self, data):
        """
        Escucha a las tareas y realiza las actualizaciones necesarias
        """
        try:
            try:
                self._TaskManager__lock.acquire()
                Logger.log('L-0235')
                task = data
                self._TaskManager__move_completed_task(task)
                if not self._TaskManager__active_tasks:
                    Logger.log('L-0236')
                    return
                running_tasks_count = len([task for task in self._TaskManager__active_tasks if task.get_task_status_data()['status'] == TASK_STATUS_RUNNING])
                for active_task in self._TaskManager__active_tasks:
                    if not running_tasks_count <= MAX_CONCURRENT_TASKS:
                        break
                    active_task_status = active_task.get_task_status_data()
                    active_task_data = active_task.get_task_data()
                    model_id = active_task_data.get('model_id', None)
                    model_name = active_task_data.get('model_name', None)
                    if active_task_status['status'] == TASK_STATUS_QUEUED and not self._TaskManager__check_active_status_for_model(model_id, model_name):
                        running_tasks_count += 1
                        active_task.init()

                Logger.log('L-0238')
            except:
                pass

        finally:
            self._TaskManager__lock.release()

    def __get_next_task_id(self):
        """
        Devuelve el proximo id disponible para colocar una tarea en cola.
        """
        next_index = self._TaskManager__last_id + 1
        self._TaskManager__last_id = next_index
        return next_index

    def __check_active_status_for_model(self, model_id=None, model_name=None):
        """
        Checkea si existe alguna tarea en cola (activa o no) para un determinado id de modelo
        o nombre de modelo.
        """
        for task in self._TaskManager__active_tasks:
            if task.check_model_relation(model_id, model_name):
                if task.get_status() == TASK_STATUS_RUNNING:
                    return True

        return False

    def __create_task(self, task, is_able_to_start):
        """
        Crea una tarea, la agrega al administrador y si es posible la inicializa.

        :task: [Task] - Tarea a crear.

        :is_able_to_start: [boolean] - Indica si la tarea se puede inicializar inmediatamente 
        después de creada.
        """
        try:
            try:
                self._TaskManager__lock.acquire()
                Logger.log('L-0227')
                self._TaskManager__active_tasks.append(task)
                task.add_observer(self)
                Logger.log('L-0228')
                running_tasks_count = len([task for task in self._TaskManager__active_tasks if task.get_task_status_data()['status'] == TASK_STATUS_RUNNING])
                if is_able_to_start:
                    if running_tasks_count <= MAX_CONCURRENT_TASKS:
                        if not task.is_alive():
                            task.init()
            except:
                pass

        finally:
            self._TaskManager__lock.release()

    def __move_completed_task(self, task):
        """
        Mueve una tarea completada de la lista de activas a la lista de completadas

        :task: Tarea a mover
        """
        self._TaskManager__active_tasks = list(filter(lambda active_task: active_task is not task, self._TaskManager__active_tasks))
        self._TaskManager__completed_tasks.append(task)

    def __get_task_from_active_list(self, task_id):
        """
        Obtiene una tarea de la lista de tareas activas.

        :task_id: [int] - Id de la tarea a buscar.

        :return: [Task] - Tarea correspondiente al id, None si no se ha encontrado.
        """
        try:
            founded_task = next(active_task for active_task in self._TaskManager__active_tasks if active_task.get_id() == task_id)
            return founded_task
        except:
            return

    def __get_task_from_finished_list(self, task_id):
        """
        Obtiene una tarea de la lista de tareas finalizadas.

        :task_id: [int] - Id de la tarea a buscar.

        :return: [Task] - Tarea correspondiente al id, None si no se ha encontrado.
        """
        try:
            founded_task = next(completed_task for completed_task in self._TaskManager__completed_tasks if completed_task.get_id() == task_id)
            return founded_task
        except:
            return

    def __get_task(self, task_id):
        """
        Obtiene una tarea de las listas de tareas.

        :task_id: [int] - Id de la tarea a buscar.

        :return: [Task] - Tarea correspondiente al id, None si no se ha encontrado.
        """
        founded_task = self._TaskManager__get_task_from_active_list(task_id)
        if founded_task is None:
            return self._TaskManager__get_task_from_finished_list(task_id)
        else:
            return founded_task

    def create_model_training_task(self, model_id):
        """
        Crea y agrega a la cola una nueva tarea de entrenamiento de modelo.

        :model_id: [String] - Id del modelo a utilizar.

        :return: [int] - Id. de la tarea creada.
        """
        Logger.log('L-0231')
        next_task_id = self._TaskManager__get_next_task_id()
        new_task = ModelTrainingTask(next_task_id, model_id)
        is_able_to_init = not self._TaskManager__check_active_status_for_model(model_id)
        self._TaskManager__create_task(new_task, is_able_to_init)
        Logger.log('L-0232')
        return next_task_id

    def create_model_creation_task(self, model_id, model_name, description, author, tokenizer_exceptions, max_dist):
        """
        Crea y agrega a la cola una nueva tarea de creación de modelo.

        :model_id: [String] - Id del modelo a crear.

        :model_name: [String] - Nombre del modelo a crear.

        :description: [String] - Descripcion del modelo a crear.

        :author: [String] - Autor del modelo a crear.

        :tokenizer_exceptions: [Dict] - Datos de las excepciones al tokenizer a aplicar al nuevo modelo.

        :max_dist: [int] - Distancia de demerau levenshtein máxima.

        :return: [int] - Id. de la tarea creada.
        """
        Logger.log('L-0225')
        next_task_id = self._TaskManager__get_next_task_id()
        new_task = ModelCreationTask(next_task_id, model_id, model_name, description, author, tokenizer_exceptions, max_dist)
        is_able_to_init = not self._TaskManager__check_active_status_for_model(model_id, model_name)
        self._TaskManager__create_task(new_task, is_able_to_init)
        Logger.log('L-0226')
        return next_task_id

    def create_text_analysis_task(self, model_id, text, only_positives):
        """
        Crea y agrega a la cola una nueva tarea de análisis de texto.

        :model_id: [String] - Id del modelo a utilizar.

        :text: [String] - Texto a analizar.

        :only_positives: [boolean] - Flag que indica si los resultados solo deben contener los positivos
        encontrados.

        :return: [int] - Id. de la tarea creada.
        """
        Logger.log('L-0233')
        next_task_id = self._TaskManager__get_next_task_id()
        new_task = TextAnalysisTask(next_task_id, model_id, text, only_positives)
        is_able_to_init = not self._TaskManager__check_active_status_for_model(model_id)
        self._TaskManager__create_task(new_task, is_able_to_init)
        Logger.log('L-0234')
        return next_task_id

    def create_files_analysis_task(self, model_id, files, only_positives):
        """
        Crea y agrega a la cola una nueva tarea de análisis de mútilples archivos de texto.

        :model_id: [String] - Id del modelo a utilizar para el análisis.

        :files: [List(files)] - Lista con los archivos a analizar, los mismos deben estar abiertos
        previamente.

        :only_positives: [boolean] - Indica si deben almacenarse los resultados positivos
        solamente.

        :return: [int] - Id. de la tarea creada.
        """
        next_task_id = self._TaskManager__get_next_task_id()
        new_task = FilesAnalysisTask(next_task_id, model_id, files, only_positives)
        is_able_to_init = not self._TaskManager__check_active_status_for_model(model_id)
        self._TaskManager__create_task(new_task, is_able_to_init)
        return next_task_id

    def get_task_status(self, task_id):
        """
        Devuelve el status de una tarea, la misma debe existir en la cola de tareas.

        :task_id: [int] - Id de la tarea a buscar

        :return: [Dict] - Diccionario con el estado de la tarea.
        """
        founded_task = self._TaskManager__get_task(task_id)
        if founded_task is None:
            ErrorHandler.raise_error('E-0097')
        return founded_task.get_task_status_data()

    def get_active_tasks(self):
        """
        Devuelve una lista con las tareas activas del sistema.

        :return: [List] - Listado de todas las tareas activas.
        """
        active_tasks_data = list([])
        for task in self._TaskManager__active_tasks:
            active_tasks_data.append(task.get_task_status_data())

        return active_tasks_data

    def get_finished_tasks(self):
        """
        Devuelve una lista con las tareas finalizadas del sistema.

        :return: [List] - Listado con las tareas finalizadas
        """
        completed_tasks_data = list([])
        for task in self._TaskManager__completed_tasks:
            completed_tasks_data.append(task.get_task_status_data())

        return completed_tasks_data

    def abort_task(self, task_id):
        """
        Aborta alguna de las tareas activas.

        :task_id: [int] - Id de la tarea.

        :return: [boolean] - True si la tarea pudo ser abortada, False en caso contrario
        """
        Logger.log('L-0239', [{'text':task_id,  'color':HIGHLIGHT_COLOR}])
        founded_task = self._TaskManager__get_task_from_active_list(task_id)
        if founded_task is None:
            Logger.log('L-0240')
            return False
        else:
            if founded_task.abort():
                self._TaskManager__move_completed_task(founded_task)
                Logger.log('L-0241')
                return True
            Logger.log('L-0242')
            return False

    def check_model_creation_tasks(self, taks_keys):
        """
        Verifica si hay una tarea de creación de modelo pendiente o en ejecución.

        :task_keys: [List] - Lista con las claves de las tareas a verificar

        :return: [boolean] - True si se encuentra alguna tarea, false en caso contrario.
        """
        for task in self._TaskManager__active_tasks:
            if task.is_blocking(taks_keys):
                return True

        return False