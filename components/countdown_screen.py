

class SecondScreen(Screen):
    def __init__(self, **kwargs):
        super(SecondScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        label = Label(text='This is the second screen')
        button = Button(text='Go to first screen')
        button.bind(on_press=self.switch_to_first)
        layout.add_widget(label)
        layout.add_widget(button)
        self.add_widget(layout)
    def switch_to_first(self, *args):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'first'
