from hmpy.component.types import AbstractComponent
from hmpy.component.views.button import ButtonView


class ButtonComponent(AbstractComponent):
    """A simple button component for writing booleans."""

    output_names = ["button"]
    """List of outputs to be configured, by name."""

    def __init__(self, config, parent=None):
        """Initialize the component.

        :param config: The configuration dict, used to populate Inputs and Outputs.
        :param parent: The parent QObject.  Defaults to None.
        """
        super().__init__(config, parent)
        self.view = ButtonView()
        self.view.button.pressed.connect(self.on_press)
        self.view.button.released.connect(self.on_release)

    def on_press(self):
        """On button press, write True to the output."""
        self.outputs["button"].value = True

    def on_release(self):
        """On button release, write False to the output."""
        self.outputs["button"].value = False
