from hmpy.component.types import AbstractComponent
from hmpy.component.views.slider import SliderView


class SliderComponent(AbstractComponent):
    output_names = ["Slider"]

    def __init__(self, config, parent=None):
        super().__init__(config, parent)
        self.view = SliderView()
        self.view.slider.valueChanged.connect(self.value_changed)

    def value_changed(self):
        self.outputs["Slider"].value = self.view.slider.value()
