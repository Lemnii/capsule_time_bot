import pandas as pd
from database import fetch_all_letters

def export_letters_to_excel(filename="letters_data.xlsx"):
    letters = fetch_all_letters()
    df = pd.DataFrame(letters, columns=["ID", "ФИО", "Письмо"])
    df.to_excel(filename, index=False)