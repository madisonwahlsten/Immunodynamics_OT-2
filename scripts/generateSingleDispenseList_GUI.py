'''
Script to create a GUI to run a singleDispense Protocol on the Opentrons written by Madison and ChatGPT
'''

import os
import tkinter as tk
from tkinter import messagebox

import pickle

class DispenseParametersGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry("500x400")
        self.title("Dispense Parameters")

        self.available_deck_positions = [i for i in range(1, 10)]

        self.dispenseParameters = {
            'reservoirDeckSlot': None,
            'reservoirType': None,
            'reservoirLocation': None,
            'plateType': [],
            'destinationPlates': [],
            'volume': None
        }

        self.reservoir_info_label = tk.Label(self, text="No Reservoir Added")
        self.reservoir_info_label.pack()

        self.add_reservoir_button = tk.Button(self, text="Add Reservoir", command=self.open_add_reservoir_window)
        self.add_reservoir_button.pack()

        self.add_plate_button = tk.Button(self, text="Add Plate", command=self.open_add_plate_window, state=tk.DISABLED)
        self.add_plate_button.pack()

        self.volume_label = tk.Label(self, text="Volume (uL):")
        self.volume_label.pack()

        self.volume_entry = tk.Entry(self)
        self.volume_entry.pack()

        self.save_button = tk.Button(self, text="Save Parameters", command=self.save_parameters)
        self.save_button.pack()

        self.plates_listbox = tk.Listbox(self)
        self.plates_listbox.pack()

        self.update_reservoir_info_label()
        self.update_plates_listbox()

    def open_add_reservoir_window(self):
        add_reservoir_window = AddReservoirWindow(self)

    def add_reservoir_parameters(self, reservoir_deck_slot, reservoir_type, reservoir_location):
        self.dispenseParameters['reservoirDeckSlot'] = reservoir_deck_slot
        self.dispenseParameters['reservoirType'] = reservoir_type
        self.dispenseParameters['reservoirLocation'] = reservoir_location

        self.update_reservoir_info_label()
        self.update_plates_listbox()
        self.enable_add_plate_button()

        self.available_deck_positions.remove(reservoir_deck_slot)

    def open_add_plate_window(self):
        add_plate_window = AddPlateWindow(self)

    def add_plate_parameters(self, plate_slot, plate_type):
        self.dispenseParameters['destinationPlates'].append(plate_slot)
        self.dispenseParameters['plateType'].append(plate_type)

        self.update_available_deck_positions()
        self.update_plates_listbox()

    def update_reservoir_info_label(self):
        reservoir_deck_slot = self.dispenseParameters['reservoirDeckSlot']
        reservoir_type = self.dispenseParameters['reservoirType']
        reservoir_location = self.dispenseParameters['reservoirLocation']

        if reservoir_deck_slot:
            if reservoir_type == 'divided':
                if reservoir_location:
                    reservoir_info = f"Reservoir Deck Slot: {reservoir_deck_slot}, Type: {reservoir_type}, " \
                                     f"Location: {reservoir_location}"
                else:
                    reservoir_info = f"Reservoir Deck Slot: {reservoir_deck_slot}, Type: {reservoir_type}"
            else:
                reservoir_info = f"Reservoir Deck Slot: {reservoir_deck_slot}, Type: {reservoir_type}"
        else:
            reservoir_info = "No Reservoir Added"

        self.reservoir_info_label.config(text=reservoir_info)

    def update_available_deck_positions(self):
        for plate_slot in self.dispenseParameters['destinationPlates']:
            if plate_slot in self.available_deck_positions:
                self.available_deck_positions.remove(plate_slot)

    def update_plates_listbox(self):
        self.plates_listbox.delete(0, "end")
        for i in range(len(self.dispenseParameters['destinationPlates'])):
            plate_slot = self.dispenseParameters['destinationPlates'][i]
            plate_type = self.dispenseParameters['plateType'][i]
            self.plates_listbox.insert(tk.END, f"Slot: {plate_slot}, Type: {plate_type}")

    def enable_add_plate_button(self):
        self.add_plate_button.config(state=tk.NORMAL)

    def save_parameters(self):
        volume = float(self.volume_entry.get())
        self.dispenseParameters['volume'] = volume

        path = os.getcwd()
        pickle.dump(self.dispenseParameters, open(f"{path}/BenchItems.pkl", "wb"))
        messagebox.showinfo("Parameters Saved",
                            f"Parameters saved to: {os.path.abspath(f'{path}/BenchItems.pkl')}")
        self.destroy()


class AddReservoirWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.geometry("300x200")
        self.title("Add Reservoir")

        self.parent = parent

        self.deck_slot_label = tk.Label(self, text="Reservoir Deck Slot:")
        self.deck_slot_label.pack()

        self.deck_slot_var = tk.StringVar(self)
        self.deck_slot_dropdown = tk.OptionMenu(self, self.deck_slot_var, *self.parent.available_deck_positions)
        self.deck_slot_dropdown.pack()

        self.reservoir_type_label = tk.Label(self, text="Reservoir Type:")
        self.reservoir_type_label.pack()

        self.reservoir_type_var = tk.StringVar(self)
        self.reservoir_type_dropdown = tk.OptionMenu(self, self.reservoir_type_var, "single", "divided")
        self.reservoir_type_dropdown.pack()

        self.reservoir_location_label = tk.Label(self, text="Reservoir Location:")
        self.reservoir_location_label.pack()

        self.reservoir_location_var = tk.StringVar(self)
        self.reservoir_location_dropdown = tk.OptionMenu(self, self.reservoir_location_var, *["A" + str(i) for i in range(1, 13)])
        self.reservoir_location_dropdown.pack()

        self.add_reservoir_button = tk.Button(self, text="Add Reservoir", command=self.add_reservoir)
        self.add_reservoir_button.pack()

    def add_reservoir(self):
        reservoir_deck_slot = int(self.deck_slot_var.get())
        reservoir_type = self.reservoir_type_var.get()
        reservoir_location = self.reservoir_location_var.get() if reservoir_type == "divided" else None

        self.parent.add_reservoir_parameters(reservoir_deck_slot, reservoir_type, reservoir_location)
        self.destroy()


class AddPlateWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.geometry("300x200")
        self.title("Add Plate")

        self.parent = parent

        self.deck_slot_label = tk.Label(self, text="Plate Deck Slot:")
        self.deck_slot_label.pack()

        self.deck_slot_var = tk.StringVar(self)
        self.deck_slot_dropdown = tk.OptionMenu(self, self.deck_slot_var, *self.parent.available_deck_positions)
        self.deck_slot_dropdown.pack()

        self.plate_type_label = tk.Label(self, text="Plate Type:")
        self.plate_type_label.pack()

        self.plate_type_var = tk.StringVar(self)
        self.plate_type_dropdown = tk.OptionMenu(self, self.plate_type_var, "96-well", "384-well")
        self.plate_type_dropdown.pack()

        self.add_plate_button = tk.Button(self, text="Add Plate", command=self.add_plate)
        self.add_plate_button.pack()

    def add_plate(self):
        plate_slot = int(self.deck_slot_var.get())
        plate_type = self.plate_type_var.get()

        self.parent.add_plate_parameters(plate_slot, plate_type)
        self.destroy()


if __name__ == "__main__":
    dispense_parameters_gui = DispenseParametersGUI()
    dispense_parameters_gui.mainloop()
