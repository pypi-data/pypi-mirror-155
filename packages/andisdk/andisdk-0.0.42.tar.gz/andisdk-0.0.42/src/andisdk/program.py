from operator import le
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
# we need to set the runtime of pythonnet to use netcoreapp instead of netframework
from clr_loader import get_coreclr
from pythonnet import set_runtime
# we get the core runtime configuration from the runtimeconfig file
rt = get_coreclr(os.path.join(current_dir, 'runtimeconfig.json'))

# we set the pythonnet runtime to use the core runtime we loaded from the config file
set_runtime(rt)

dlls = os.path.join(current_dir, 'dlls')
# add dll path to system path for clr to work 
import sys
sys.path.append(dlls)
import clr
clr.AddReference('PrimaTestCaseLibrary')
from PrimaITestCaseLibrary.OutputView import IOutputViewer, OutputStringType
from PrimaTestCaseLibrary.BusinessTestCaseLibrary import MessageBuilderImpl, TestProjectImpl, ScriptSessionImpl
from PrimaTestCaseLibrary.Utils import Andi
from PrimaTestCaseLibrary.Utils.Series import SeriesBuilder
import logging
default_handlers = logging.root.handlers
logging.basicConfig(level=logging.NOTSET, format="%(message)s", datefmt="[%X]", handlers=default_handlers)
default_logger = logging.getLogger("andi.default")
# make sure that linux files are executables
import platform
import stat
if platform.system().lower() == "linux":
    linux_executables = ["canconvert-linux", "ldf2json-linux"]
    for exe in linux_executables:
        exe_file_path = os.path.join(dlls, exe)
        if not os.access(exe_file_path, os.X_OK):
            try:
                st = os.stat(exe_file_path)
                os.chmod(exe_file_path, st.st_mode | stat.S_IEXEC)
            except:
                default_logger.warn(f"{exe_file_path} is not marked as executable, this might cause the related feautre to not function properly")
          
class PythonOutputViewer(IOutputViewer):
    __namespace__ = "PrimaITestCaseLibrary.OutputView"
    def __init__(self, name) -> None:
        self.logger = logging.getLogger('andi.' + name)
    
    def log(self, msg):
        self.logger.debug(msg)
    def log(self, msg, ty):
        if ty == OutputStringType.Error:
            self.logger.error(msg)
            return
        if ty == OutputStringType.Warning:
            self.logger.warning(msg)
            return
        if ty == OutputStringType.Success or ty == OutputStringType.Information:
            self.logger.info(msg)
        self.logger.debug(msg)
    def clear(self):
        pass

class AndiApi(dict):
    def __init__(self, *args, **kwargs):
        super(AndiApi, self).__init__(*args, **kwargs)
        self.__dict__ = self

    @property
    def message_builder(self):
        """message builder object."""
        return self['message_builder']

    @property
    def andi(self):
        """andi object."""
        return self['andi']

    @property
    def channels(self):
        """project channels"""
        return self['channels']
    
    @property
    def databases(self):
        """project databases"""
        return self['databases']
    
    @property
    def messages(self):
        """project messages"""
        return self['messages']

    @property
    def ecus(self):
        """project ecus"""
        return self['ecus']

# give user ability to load project
__project = TestProjectImpl()
__project.SetOutputViewer("python", IOutputViewer(PythonOutputViewer('default')))
message_builder = MessageBuilderImpl(__project)
series_builder = SeriesBuilder()
ScriptSessionImpl.getInstance().IOutputViewer = IOutputViewer(PythonOutputViewer('andi.session'))
andi = Andi(__project)
def load_project(atp) -> AndiApi:
    project = TestProjectImpl.Deserialize(atp)
    project.SetOutputViewer("python", IOutputViewer(PythonOutputViewer(project.name)))
    scope = AndiApi()
    scope['__project'] = project
    scope['andi'] = Andi(project)
    scope['message_builder'] = MessageBuilderImpl(project)
    scope['channels'] = {}
    scope['databases'] = {}
    scope['messages'] = {}
    scope['ecus'] = {}
    if project.Adapters:
        for channel in project.Adapters.Adapters:
            scope['channels'][channel.name] = channel.__implementation__
            scope[channel.name] = channel.__implementation__
    if project.DataBases:
        for db in project.DataBases.DataBases:
            scope['databases'][db.name] = db.__implementation__
            scope[db.name] = db.__implementation__
    if project.Messages:
        for msg in project.Messages.Messages:
            scope['messages'][msg.name] = msg.__implementation__
            scope[msg.name] = msg.__implementation__
    if project.Ecus:
        for ecu in project.Ecus.nodes:
            scope['ecus'][ecu.name] = ecu.__implementation__
            scope[ecu.name] = ecu.__implementation__
    return scope

rich_handler = None
def enable_rich_logging():
    """Setup rich-based logging."""
    global rich_handler
    import rich.logging
    rich_handler = rich.logging.RichHandler()
    logging.basicConfig(level=logging.NOTSET, format="%(message)s", datefmt="[%X]", handlers = [rich_handler])

def disable_rich_logging():
    """Disable rich-based logging"""
    global rich_handler
    logging.root.removeHandler(rich_handler)