import pandas as pd

df = pd.read_csv("./data/tienda_cafe.csv")
print(df.head(10))  # print(df.head())
# print(df.info())
# print(df['producto'].value_counts())
df["producto"] = df["producto"].str.lower()
df["producto"] = df["producto"].str.strip()
print(df["producto"].value_counts())

df["producto"] = df["producto"].replace(
    {
        "latet": "latte",
        "té evrde": "té verde",
        "epsresso": "espresso",
        "cold brwe": "cold brew",
        "codl brew": "cold brew",
        "ameriacno": "americano",
        "chocolate calienet": "chocolate caliente",
        "té verede": "té verde",
        "americaon": "americano",
        "farppé": "frappé",
        "té vedre": "té verde",
        "cold brwe": "cold brew",
        "mahciato": "machiato",
        "chocolate calienet ": "chocolate caliente",
        "mohca": "mocha",
        "cohcolate caliente": "chocolate caliente",
        "t éverde": "té verde",
        "maericano": "americano",
        "mcahiato": "machiato",
        "machiaot": "machiato",
        "capupccino": "cappuccino",
        "espersso": "espresso",
        "té verede": "té verde",
        "cappuccion": "cappuccino",
        "té vered": "té verde",
        "cpapuccino": "cappuccino",
    },
    regex=True,
)
print(df["producto"].value_counts())