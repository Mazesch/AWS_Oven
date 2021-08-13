import PySimpleGUI as sg


class Gui:
    layout = None
    window = None
    
    # Inject
    main = None

    def __init__(self, main):
        self.main = main
        sg.ChangeLookAndFeel('SystemDefault')
        # Define the window's contents
        self.layout = [
            [sg.Text("Desired temperature:"), sg.Input(key='newTemp')],
            [],
            [sg.Text('Current temperature is ' + str(int(0)) + ".", size=(40,1), key='temp')],
            [sg.Button('Set Temperature', key='setTemp'), sg.Button('Quit')],
        ]

        # Create the window
        self.window = sg.Window('Oven Example', self.layout, margins=(10, 10))

        
    def update(self, dt):
        event, values = self.window.read(20)
        # See if user wants to quit or window was closed
        if event == sg.WINDOW_CLOSED or event == sg.WIN_CLOSED or event == 'Quit':
            return False
        
        # See if the setTemp button was pressed
        if event == 'setTemp':
            try:
                newTemp = float(values['newTemp'])
                if newTemp < 0:
                    newTemp = 0
                self.main.raise_set_target_temp(newTemp, True)
            except:
                pass
        # Update the temperature display
        self.setCurrent('Current temperature is ' + str("{:.2f}".format(self.main.getTemp())) + "ºC.")

        return True

    def close(self):
        # Finish up by removing from the screen
        self.window.close()

    def setNewTemp(self, value):
        self.window['newTemp'].update(str(value))

    def setCurrent(self, str):
        self.window['temp'].update(str)
