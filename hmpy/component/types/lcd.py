from hmpy.component.types import AbstractComponent
from hmpy.component.views.lcd import LCDView


class LCDComponent(AbstractComponent):
    input_names = ["LCD"]

    def __init__(self, config, parent=None):
        super().__init__(config, parent)
        self.view = LCDView()
        self.inputs['LCD'].valueChanged.connect(self.on_change)

    def on_change(self):
        self.view.lcd.display(self.inputs['LCD'].value)
