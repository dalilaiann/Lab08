import flet as ft

from model.nerc import Nerc


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._idMap = {}
        self.fillIDMap()

    def handleWorstCase(self, e):
        self._view._txtOut.controls.clear()
        if self._view._ddNerc.value is None:
            self._view.create_alert("Selezionare un NERC!")
        elif self._view._txtYears.value=="":
            self._view.create_alert("Selezionare il numero di anni!")
        elif self._view._txtHours.value=="":
            self._view.create_alert("Selezionare il numero di ore!")
        else:
            results=self._model.worstCase(self._idMap.get(self._view._ddNerc.value), int(self._view._txtYears.value), int(self._view._txtHours.value))
            if results is None:
                self._view._txtOut.controls.append(ft.Text("Non esiste worst case per lo scenario indicato"))
                self._view.update_page()
            else:
                self._view._txtOut.controls.append(ft.Text(f"Tot people affected: {results[1]}"))
                self._view._txtOut.controls.append(ft.Text(f"Tot hours of outage: {results[2]}"))
                for result in results[0]:
                    self._view._txtOut.controls.append(ft.Text(result))
                self._view.update_page()

    def fillDD(self):
        nercList = self._model.listNerc

        for n in nercList:
            self._view._ddNerc.options.append(ft.dropdown.Option(n))
        self._view.update_page()

    def fillIDMap(self):
        values = self._model.listNerc
        for v in values:
            self._idMap[v.value] = v
