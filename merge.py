import pandas as pd

# Load both CSV files
df1 = pd.read_csv("final_traffic_dataset1.csv")
df2 = pd.read_csv("traffic_prediction6.csv")

# Concatenate along rows
merged_df = pd.concat([df1, df2], ignore_index=True)

# Save the merged file as a new CSV
merged_df.to_csv("final_traffic_dataset2.csv", index=False)

print("CSV files merged successfully!")
