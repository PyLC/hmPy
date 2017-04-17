import sys
import unittest
from hmpy.component.manager import ComponentManager
from hmpy.component.types import AbstractComponent
from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)


class TestComponentManager(unittest.TestCase):
    """Tests the ComponentManager class"""

    def setUp(self):
        """Initialize test data and ComponentManager."""
        self.name = "test"
        self.manager = ComponentManager()
        self.triggered = False

    def set_triggered(self):
        """Helper method used as slot.  Sets class attribute succeeded to True when invoked."""
        self.triggered = True

    def test_add(self):
        """Test adding a valid component,"""
        component = self.manager.add(self.name, HelperComponent, {})
        # Check that the component was instantiated and as the correct class.
        self.assertIsInstance(component, HelperComponent)

    def test_duplicate_add(self):
        """Test adding a component when a component with the same name already exists."""
        self.manager.add(self.name, HelperComponent, {})
        with self.assertRaises(ValueError):
            self.manager.add(self.name, HelperComponent, {})

    def test_remove_valid(self):
        """Test removing a component that exists."""
        self.manager.add(self.name, HelperComponent, {})
        self.manager.remove(self.name)
        self.assertFalse(self.manager.has_component(self.name))

    def test_remove_invalid(self):
        """Test removing a component that doesn't exist."""
        with self.assertRaises(ValueError):
            self.manager.remove(self.name)

    def test_has_get_valid(self):
        """Test getting and checking for a component when it exists."""
        component = self.manager.add(self.name, HelperComponent, {})

        # Test that has_component returns True
        self.assertTrue(self.manager.has_component(self.name))
        # Test that it returns the right object
        self.assertEqual(self.manager.get_component(self.name), component)

    def test_has_get_invalid(self):
        """Test getting and checking for a component when it does not exist."""
        self.assertFalse(self.manager.has_component(self.name))
        self.assertIsNone(self.manager.get_component(self.name))

    def test_components_changed_emit(self):
        """Test that the components_changed signal is emitted when components are added or removed."""
        self.manager.components_changed.connect(self.set_triggered)
        self.manager.add(self.name, HelperComponent, {})

        # Check the slot was triggered
        self.assertTrue(self.triggered)
        # Reset slot
        self.triggered = False
        self.manager.remove(self.name)
        # Check the slot was triggered
        self.assertTrue(self.triggered)


class HelperComponent(AbstractComponent):
    """Helper class derived from AbstractComponent for testing ComponentManager"""

    def __init__(self, config, parent=None):
        super().__init__(config, parent)
