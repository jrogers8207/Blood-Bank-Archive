import logging
from pathlib import Path
import sqlite3

import PySimpleGUI as sg

logging.basicConfig(level=logging.CRITICAL, format="%(asctime)s - %(levelname)s - %(message)s")
logging.debug("Program Start")

databasePath = Path("bloodbank.db")

if databasePath.is_file():
    con = sqlite3.connect("bloodbank.db")
    cur = con.cursor()
else:
    con = sqlite3.connect("bloodbank.db")
    cur = con.cursor()
    # Create tables.
    cur.execute("""CREATE TABLE Patient(
    PatientID INT,
    FirstName TEXT,
    LastName TEXT,
    Address TEXT,
    Phone TEXT,
    BloodType TEXT,
    PRIMARY KEY (PatientID))
    """)

    cur.execute("""CREATE TABLE Donor(
    DonorID INT,
    FirstName TEXT,
    LastName TEXT,
    Address TEXT,
    Phone TEXT,
    BloodType TEXT,
    PRIMARY KEY (DonorID))
    """)

    cur.execute("""CREATE TABLE BloodTransaction(
    TransactionID INT,
    DonorID INT,
    PatientID INT,
    Amount INT,
    TransactionDate TEXT,
    TransactionType TEXT,
    PRIMARY KEY (TransactionID),
    FOREIGN KEY (DonorID)
    REFERENCES Donor(DonorID),
    FOREIGN KEY (PatientID)
    REFERENCES Patient(PatientID))
    """)

donorAttributes = ("DonorID", "FirstName", "LastName", "Address", "Phone", "BloodType")
patientAttributes = ("PatientID", "FirstName", "LastName", "Address", "Phone", "BloodType")
transactionAttributes = ("TransactionID", "DonorID", "PatientID", "Amount", "TransactionDate", "TransactionType")

donorLayout = [
    [sg.Text("Donor ID"), sg.InputText(key="donorID")],
    [sg.Text("First Name"), sg.InputText(key="donorFirstName")],
    [sg.Text("Last Name"), sg.InputText(key="donorLastName")],
    [sg.Text("Address"), sg.InputText(key="donorAddress")],
    [sg.Text("Phone Number"), sg.InputText(key="donorPhoneNumber")],
    [sg.Text("Blood Type"), sg.InputText(key="donorBloodType")]
]
donorFieldKeys = ("donorID", "donorFirstName", "donorLastName", "donorAddress", "donorPhoneNumber", "donorBloodType")

patientLayout = [
    [sg.Text("Patient ID"), sg.InputText(key="patientID")],
    [sg.Text("First Name"), sg.InputText(key="patientFirstName")],
    [sg.Text("Last Name"), sg.InputText(key="patientLastName")],
    [sg.Text("Address"), sg.InputText(key="patientAddress")],
    [sg.Text("Phone Number"), sg.InputText(key="patientPhoneNumber")],
    [sg.Text("Blood Type"), sg.InputText(key="patientBloodType")]
]
patientFieldKeys = (
    "patientID", "patientFirstName", "patientLastName", "patientAddress", "patientPhoneNumber", "patientBloodType")

transactionLayout = [
    [sg.Text("Transaction ID"), sg.InputText(key="transactionID")],
    [sg.Text("Donor ID"), sg.InputText(key="transactionDonorID")],
    [sg.Text("Patient ID"), sg.InputText(key="transactionPatientID")],
    [sg.Text("Amount (mL)"), sg.InputText(key="transactionAmount")],
    [sg.Text("Date"), sg.InputText(key="transactionDate")],
    [sg.Text("Transaction Type"), sg.InputText(key="transactionType")]
]
transactionFieldKeys = (
    "transactionID", "transactionDonorID", "transactionPatientID", "transactionAmount", "transactionDate",
    "transactionType")

layout = [
    [sg.Combo(["Donor", "Patient", "Transaction"], enable_events=True, key="changeLayout", default_value="Donor")],
    [sg.Column(donorLayout, visible=True, key="Donor"), sg.Column(patientLayout, visible=False, key="Patient"),
     sg.Column(transactionLayout, visible=False, key="Transaction")],
    [sg.Button("Add"), sg.Button("Search"), sg.Button("Find Matching Donation")],
    [sg.Output(size=(100, 40))]
]

window = sg.Window("Blood Bank Archive", layout)

abPositive = ["AB+", "AB-", "A+", "A-", "B+", "B-", "O+", "O-"]
abNegative = ["AB-", "A-", "B-", "O-"]
aPositive = ["A+", "A-", "O+", "O-"]
aNegative = ["A-", "O-"]
bPositive = ["B+", "B-", "O+", "O-"]
bNegative = ["B-", "O-"]
oPositive = ["O+", "O-"]
oNegative = ["O-"]

bloodTypes = {"AB+": abPositive, "AB-": abNegative, "A+": aPositive, "A-": aNegative, "B+": bPositive, "B-": bNegative,
              "O+": oPositive, "O-": oNegative}

currentLayout = "Donor"
while True:
    event, values = window.read()

    if event == "changeLayout":
        window[currentLayout].update(visible=False)
        currentLayout = values["changeLayout"]
        window[currentLayout].update(visible=True)

    if event == "Add":
        try:
            if values["changeLayout"] == "Donor":
                cur.execute("INSERT INTO Donor VALUES (?, ?, ?, ?, ?, ?)", (
                    values["donorID"], values["donorFirstName"], values["donorLastName"], values["donorAddress"],
                    values["donorPhoneNumber"], values["donorBloodType"]))
                con.commit()
            elif values["changeLayout"] == "Patient":
                cur.execute("INSERT INTO Patient VALUES (?, ?, ?, ?, ?, ?)", (
                    values["patientID"], values["patientFirstName"], values["patientLastName"],
                    values["patientAddress"],
                    values["patientPhoneNumber"], values["patientBloodType"]))
                con.commit()
            elif values["changeLayout"] == "Transaction":
                cur.execute("INSERT INTO BloodTransaction VALUES (?, ?, ?, ?, ?, ?)", (
                    values["transactionID"], values["transactionDonorID"], values["transactionPatientID"],
                    values["transactionAmount"], values["transactionDate"], values["transactionType"]))
            con.commit()
        except sqlite3.OperationalError:
            print("Not all forms filled.")
        except sqlite3.IntegrityError:
            print("Invalid ID.")
    elif event == "Search":
        i = 0
        fieldValues = []
        tableName = ""
        firstCondition = True
        if values["changeLayout"] == "Donor":
            tableName = "Donor"
            for key in donorFieldKeys:
                if values[key] == "":
                    fieldValues.append("")
                else:
                    if firstCondition:
                        fieldValues.append(f"WHERE {donorAttributes[i]} = '{values[key]}'")
                        firstCondition = False
                    else:
                        fieldValues.append(f"AND {donorAttributes[i]} = '{values[key]}'")
                i += 1
        elif values["changeLayout"] == "Patient":
            tableName = "Patient"
            for key in patientFieldKeys:
                if values[key] == "":
                    fieldValues.append("")
                else:
                    if firstCondition:
                        fieldValues.append(f"WHERE {patientAttributes[i]} = '{values[key]}'")
                        firstCondition = False
                    else:
                        fieldValues.append(f"AND {patientAttributes[i]} = '{values[key]}'")
                i += 1

        elif values["changeLayout"] == "Transaction":
            tableName = "BloodTransaction"
            for key in transactionFieldKeys:
                if values[key] == "":
                    fieldValues.append("")
                else:
                    if firstCondition:
                        fieldValues.append(f"WHERE {transactionAttributes[i]} = '{values[key]}'")
                        firstCondition = False
                    else:
                        fieldValues.append(f"AND {transactionAttributes[i]} = '{values[key]}'")
                i += 1

        fieldValues = [field for field in fieldValues if not field == ""]
        command = f"SELECT * FROM " + tableName + " " + " ".join(fieldValues)
        logging.debug(command)
        print("\n" * 500)
        try:
            for row in cur.execute(command):  # https://xkcd.com/327/
                print(row)
        except sqlite3.OperationalError:
            print("No matches found.")

    elif event == "Find Matching Donation":
        if values["changeLayout"] != "Patient":
            print("Patient must be selected to search for match.")
        else:

            donations = cur.execute(
                """SELECT * FROM BloodTransaction JOIN Donor ON BloodTransaction.DonorID = Donor.DonorID WHERE 
                PatientID = ''""").fetchall()
            logging.debug(donations)
            bestMatches = [donation for donation in donations if donation[11] == values["patientBloodType"]]
            logging.debug(bestMatches)
            secondMatches = [donation for donation in donations if
                             donation not in bestMatches and donation[11] in bloodTypes[values["patientBloodType"]]
                             and "+" in donation[11] and "O" not in donation[11]]
            logging.debug(secondMatches)
            thirdMatches = [donation for donation in donations if
                            donation not in bestMatches and donation not in secondMatches and donation[11] in
                            bloodTypes[values["patientBloodType"]] and donation[11] != "O-"]
            logging.debug(thirdMatches)
            fourthMatches = [donation for donation in donations if donation not in bestMatches and donation[11] == "O-"]
            logging.debug(fourthMatches)
            matches = bestMatches + secondMatches + thirdMatches + fourthMatches
            logging.debug(matches)
            print("\n" * 500)
            print(matches)
    elif event == sg.WIN_CLOSED:
        break

window.close()
logging.debug("Program end")
