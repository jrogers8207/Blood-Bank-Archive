import sqlite3

import PySimpleGUI as sg

donorLayout = [
    [sg.Text("Donor ID"), sg.InputText()],
    [sg.Text("First Name"), sg.InputText()],
    [sg.Text("Last Name"), sg.InputText()],
    [sg.Text("Address ID"), sg.InputText()],
    [sg.Text("Phone Number"), sg.InputText()],
    [sg.Text("Blood Type"), sg.InputText()]
]

patientLayout = [
    [sg.Text("Patient ID"), sg.InputText()],
    [sg.Text("First Name"), sg.InputText()],
    [sg.Text("Last Name"), sg.InputText()],
    [sg.Text("Address ID"), sg.InputText()],
    [sg.Text("Phone Number"), sg.InputText()],
    [sg.Text("Blood Type"), sg.InputText()]
]

transactionLayout = [
    [sg.Text("Transaction ID"), sg.InputText()],
    [sg.Text("Donor ID"), sg.InputText()],
    [sg.Text("Patient ID"), sg.InputText()],
    [sg.Text("Amount (mL)"), sg.InputText()],
    [sg.Text("Date"), sg.InputText()],
    [sg.Text("Transaction Type"), sg.InputText()]
]

layout = [
    [sg.Combo(["Donor", "Patient", "Transaction"], enable_events=True, key="changeLayout", default_value="Donor")],
    [sg.Column(donorLayout, visible=True, key="Donor"), sg.Column(patientLayout, visible=False, key="Patient"),
     sg.Column(transactionLayout, visible=False, key="Transaction")], [sg.Button("Add"), sg.Button("Search")]
]
window = sg.Window("Blood Bank Archive", layout)

layoutName = "Donor"
while True:
    event, values = window.read()

    if event == "changeLayout":
        window[layoutName].update(visible=False)
        layoutName = values["changeLayout"]
        window[layoutName].update(visible=True)

    if event == sg.WIN_CLOSED:
        break
window.close()
