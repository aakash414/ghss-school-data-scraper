import pandas as pd

HSST_POST_OPTIONS = [
    "HSST Jr Arabic", "HSST Jr Botany", "HSST Botany", "HSST Chemistry", "HSST Jr Commerce",
    "HSST Commerce", "HSST Communicative English", "HSST Jr Computer Science", "HSST Computer Science",
    "HSST Jr Economics", "HSST Economics", "HSST Electronics", "HSST Jr English", "HSST English",
    "HSST Gandhian Studies", "HSST Jr Geography", "HSST Geography", "HSST Geology", "HSST Jr German",
    "HSST Jr Hindi", "HSST Hindi", "HSST Jr History", "HSST History", "HSST Home Science",
    "HSST Journalism", "HSST Jr Malayalam", "HSST Malayalam", "HSST Jr Mathematics", "HSST Mathematics",
    "HSST Jr Physics", "HSST Physics", "HSST Jr Political Science", "HSST Political Science",
    "HSST Psychology", "HSST Jr Russian", "HSST Jr Sanskrit", "HSST Social Work", "HSST Sociology",
    "HSST Jr Statistics", "HSST Statistics", "HSST Jr Tamil", "HSST Jr Zoology", "HSST Zoology"
]

def clean_post(post):
    if not isinstance(post, str):
        return ""
    for option in HSST_POST_OPTIONS:
        if option in post:
            return option
    return ""

df = pd.read_csv("master_school_data.csv")

df['post'] = df['post'].apply(clean_post)

# Optionally, drop rows where 'post' is blank (no valid post found)
df = df[df['post'] != ""]

# Save cleaned CSV
df.to_csv("schools_cleaned.csv", index=False)