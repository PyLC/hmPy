from hmpy.component.types import AbstractComponent
from hmpy.component.views.light import LightView


class LightComponent(AbstractComponent):
    """A simple light component"""

    input_names = ['light']
    """List of inputs to be configured by name."""

    def __init__(self, config, parent=None):
        """Initialize the component.

        :param config: Dict holding configuration values, used to set Inputs and Outputs.
        :param parent: The parent QWidget.
        """
        super().__init__(config, parent)
        self.view = LightView()
        self.inputs['light'].valueChanged.connect(self.on_change)

    def on_change(self):
        """Update the light view when the input value changes."""
        self.view.on = self.inputs['light'].value
