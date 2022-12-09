from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from datacards import CardCoil, CardHoldingRegister, CardInputRegister
from kivy.lang import Builder
from pyModbusTCP.client import ModbusClient
from kivymd.uix.snackbar import Snackbar
from kivy.clock import Clock


class MyWidget(MDScreen):
    """
    Construtor
    """

    def __init__(self, tags, **kwargs): 

        super().__init__(**kwargs)
        self._tags = tags
        self._modclient = ModbusClient()
        for tag in self._tags:
            
            if tag["type"] == "input":
                self.ids.modbus_data.add_widget(CardInputRegister(tag,self._modclient))
            elif tag["type"]== "holding":
                self.ids.modbus_data.add_widget(CardHoldingRegister(tag,self._modclient))
            elif tag["type"] == "coil":
                self.ids.modbus_data.add_widget(CardCoil(tag,self._modclient))

    def connect(self):
        if self.ids.conectar.text == "CONECTAR":
            self.ids.conectar.text =  "DESCONSCTAR"
            
            try:
                if self._modclient.open():
                    self._modclient.host = self.ids.hostname.text
                    self._modclient.port = int(self.ids.port.text)
                    self._modclient.open()
                    Snackbar(text="Conexão realizada com sucesso!", bg_color=(0,1,0,1)).open()
                    self._ev = []
                    for card in self.ids.modbus_data.children:
                        # aqui é para atualizar os dados 1 vez sem atrapalhar o cliente de editar
                        if card.tag['type'] == "holding" or card.tag['type'] == "coil": 
                            self._ev.append(Clock.schedule_once(card.update_data,1))
                        else:
                            self._ev.append(Clock.schedule_interval(card.update_data,1))
                else:
                    self.ids.conectar.text = "CONECTAR"
                    self._modclient.close()
                    Snackbar(text="Porta ou IP não encontrado", bg_color=(1,0,0,1)).open()
            
            except Exception as e:
                Snackbar(text=f"Erro de conexão:{e.args}", bg_color=(1,1,0,1)).open()
                self.ids.conectar.text = "CONECTAR"

        else:
            self.ids.conectar.text = "CONECTAR"
            for event in self._ev: 
                event.cancel()
            self._modclient.close()
            Snackbar(text="Cliente desconectado", bg_color=(1,0,0,1)).open()


    
    
class BasicApp(MDApp):
    __tags = [
            {"name": 'tempForno', "description": "Temperatura Forno", "unit": "°C", "address": 1000, "type": "input"}, 
            {"name": 'setpoint', "description": "Temperatura desejada", "unit": "°C", "address": 2000, "type": "holding"}, 
            {"name": 'status', "description": "Estado atuador", "address": 1000, "type": "coil"}
            ] 


    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.primary_hue = "500" 
        self.theme_cls.accent_palette = "Blue"
        self.theme_cls.material_style = "M3"
        Builder.load_file("kivymd.kv")
        return MyWidget(self.__tags)


if __name__ == '__main__':
    BasicApp().run()