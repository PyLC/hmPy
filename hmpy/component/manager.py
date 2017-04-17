from PyQt5.QtCore import QObject, pyqtSignal


class ComponentManager(QObject):
    """Manages and controls access to all Components."""

    components_changed = pyqtSignal()
    """Signal indicating a change to the Components."""

    def __init__(self, parent=None):
        """Initialize component manager"""
        super().__init__(parent)
        self.__components = {}

    def add(self, name, component_type, config):
        """Add and initialize a new component.

        :param name: Name of the component.
        :param component_type: Class inheriting from hmpy.component.types.AbstractComponent.
        :param config: Dict holding configuration info.
        :raise ValueError: When a component already exists with the same name.
        """
        if self.has_component(name):
            raise ValueError("A component already exists named %s" % name)

        self.__components[name] = component_type(config)
        self.components_changed.emit()
        return self.__components[name]

    def remove(self, name):
        """Remove a component by name.

        :param name: Name of the component to remove.
        :raise ValueError: If name does not match any existing components.
        """
        if not self.has_component(name):
            raise ValueError("No component exists names %s." % name)
        del self.__components[name]
        self.components_changed.emit()

    def get_components(self):
        """Get components dict.

        :return: Dict of components.
        """
        return self.__components

    def get_component(self, name):
        """Get a component by name.

        :param name: Name of the component to return.
        :return: Component or None if no matching components are found.
        """
        return self.__components.get(name)

    def has_component(self, name):
        """Check if a component exists by name,

        :param name: Name to check.
        :return: True if component with name exists, False otherwise.
        """
        return name in self.__components


