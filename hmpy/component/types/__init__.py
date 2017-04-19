import pkgutil
import inspect
from PyQt5.QtCore import QObject
from hmpy.component.input import Input
from hmpy.component.output import Output

__all__ = []


def get_component_types():
    """Returns a dict indexing all available implementations of AbstractComponent."""
    types = dict()
    for module in __all__:
        cls = globals()[module]
        types[cls.__name__] = cls
    return types


class AbstractComponent(QObject):
    """Abstract implementation of a Component."""

    input_names = []
    """Defines a list of inputs for this component by name."""
    output_names = []
    """Defines a list of outputs for this component by name."""

    def __init__(self, config, parent=None):
        """Initialize the AbstractComponent"""
        super().__init__(parent)
        self.inputs = dict()
        self.outputs = dict()
        self.process_config(config)

    def process_config(self, config):
        """Map the configuration argument to inputs and outputs.

        :param config: Dict containing configuration options.
        """
        if 'inputs' in config:
            for name, obj in config['inputs'].items():
                self.inputs[name] = Input(obj['interval'], obj['register_type'], obj['address'], obj['connection'])

        if 'outputs' in config:
            for name, obj in config['outputs'].items():
                self.outputs[name] = Output(obj['address'], obj['connection'])


# Load all Component types in module path
for loader, module, is_pkg in pkgutil.walk_packages(__path__):
    members = inspect.getmembers(loader.find_module(module).load_module(module))
    for key, cls in members:
        if inspect.isclass(cls) and cls != AbstractComponent and issubclass(cls, AbstractComponent):
            __all__.append(module)
            globals()[module] = cls
