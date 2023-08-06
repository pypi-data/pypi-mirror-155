__all__ = [
    'CLIPlugins', 'EndpointPlugins', 'ProcessorPlugins', 'ReaderPlugins', 'SerializerPlugins',
    'TDMPlugins', 'TrainerPlugins', 'WrapperPlugins', 'WrapperActionsPlugins'
]

from .cli import CLIPluginManager
from .endpoint import EndpointPluginManager
from .processor import ProcessorPluginManager
from .reader import ReaderPluginManager
from .serializer import SerializerPluginManager
from .tdm import TDMPluginManager
from .trainer import TrainerPluginManager
from .wrapper import WrapperPluginManager
from .wrapper_actions import WrapperActionsPluginManager

CLIPlugins = CLIPluginManager()
EndpointPlugins = EndpointPluginManager()
ProcessorPlugins = ProcessorPluginManager()
ReaderPlugins = ReaderPluginManager()
SerializerPlugins = SerializerPluginManager()
TDMPlugins = TDMPluginManager()
TrainerPlugins = TrainerPluginManager()
WrapperPlugins = WrapperPluginManager()
WrapperActionsPlugins = WrapperActionsPluginManager()
