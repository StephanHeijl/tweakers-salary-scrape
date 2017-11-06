from __future__ import print_function
import json
import pandas
import pprint
import re
import matplotlib.pyplot as plt
from scipy.stats import *
import numpy as np
from collections import defaultdict

data = []
with open("messages_3.json") as f:
    for line in f:
        try:
            message = json.loads(line.strip().strip(","))
        except:
            continue
        user = message["username"]
        content = "".join(message["content"])

        data.append((user, content))

age_re = re.compile("Leeftijd: (\d{2})")
salary_re = re.compile("[Mm]aand ?salaris( \(bruto\))?: (\d{3,5})")
hours_re = re.compile("Werkweek: ?(\d{2})")
role_re = re.compile("Huidige functie:(.+)")

role_tokens = defaultdict(int)
role_token_idx = []

parsed_data = []
for user, content in data:
    if "Leeftijd: " in content:

        try:
            age = int(age_re.findall(content)[0])
        except:
            continue

        try:
            s = float(salary_re.findall(content)[0][-1])
        except:
            continue

        try:
            hours = float(hours_re.findall(content)[0])
        except:
            continue

        if s > 10000:
            s /= 12

        if s * (40 / hours) > 8000:
            continue

        try:
            role = role_re.findall(content)[0].strip()
        except:
            role = ""

        for token in re.split("[^a-z]", role.lower()):
            if len(token) > 2:
                role_tokens[token] += 1

        parsed_data.append({
            "user": user,
            "age": age,
            "salary": s,
            "hours": hours,
            "salary_adjusted": s * (40 / hours),
            "role": role
        })

top_role_tokens = sorted(role_tokens.items(), key=lambda x: x[1], reverse=True)[:200]

df = pandas.DataFrame(parsed_data)
unique_users = True
if unique_users:
    filtered_data = []
    for user, group in df.groupby("user"):
        filtered_data.append(group.sort_values("age").iloc[-1].to_dict())

    df = pandas.DataFrame(filtered_data)

in_age_range = np.logical_and(df.age.values >= 22, df.age.values <= 26)
#df = df.iloc[in_age_range]

plt.figure(figsize=(16, 9))
df.loc[:, "salary_adjusted"].plot(kind="hist", bins=50)
plt.savefig("AdjustedSalaries.png", dpi=100)

print(
    "Token", "N", "Median", "Mean", "Std", "Correlation w/ age", "Mean age",
    sep="\t"
)

for role_token, n_tokens in top_role_tokens:
    role_df = df.iloc[np.array([role_token in row.role.lower() for r, row in df.iterrows()])]
    if role_df.shape[0] < 6:
        continue
    print(
        role_token,
        role_df.shape[0],
        np.median(role_df.salary_adjusted.values),
        np.mean(role_df.salary_adjusted.values),
        np.std(role_df.salary_adjusted.values),
        pearsonr(role_df.age, role_df.salary_adjusted)[0],
        np.mean(role_df.age.values),
        sep="\t"
    )

print(
    "|all|",
    df.shape[0],
    np.median(df.salary_adjusted.values),
    np.mean(df.salary_adjusted.values),
    np.std(df.salary_adjusted.values),
    pearsonr(df.age, df.salary_adjusted)[0],
    np.mean(role_df.age.values),
    sep="\t"
)
exit()


#df.loc[:, "salary_adjusted"].plot(kind="hist", bins=50)
df.plot(kind="scatter", x="age", y="salary_adjusted")

plt.show()
