import shutil, os
import pandas as pd

pd_df = pd.read_csv(r"C:\Users\sarin\Documents\Science Fair Data\drugs_side_effects_drugs_com.csv")
drug_names = list(pd_df["drug_name"])

# print(drug_names)
for i in range(len(drug_names)):
    drug_names[i] = drug_names[i].lower()

print(drug_names)

root_dir = r"C:\Users\sarin\Documents\Science Fair Data\packaging_images"

classes = os.listdir(root_dir)

sum = 0
for c in classes:
    x = [j.lower() for j in c.split()]
    if x[0] in drug_names:
        print(x[0])
        sum += 1

print(sum)