import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button 
from kivy.uix. label import Label

class BasicApp (App):
    '''
    Aplicativo básico kivy
    '''
    def build(self):
        '''
        Construir o aplicativo
        '''
        layout = BoxLayout (orientation="vertical")
        bt = Button(text='Botão 1')
        lb = Label(text='Label 1')
        layout.add_widget(bt)
        layout.add_widget(lb)
        layout2 = BoxLayout (orientation='horizontal')
        lb2 = Label(text='Label 2')
        lb3 = Label (text='Label 3')
        layout2.add_widget (lb2)
        layout2.add_widget(lb3)
        layout.add_widget (layout2)

        return layout

if __name__ == '__main__':
    BasicApp().run()