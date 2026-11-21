import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# 1. LOAD THE DATASET
# ==========================================

df = pd.read_csv("monthly_expenses_250.csv")

print("=" * 65)
print("             MONTHLY EXPENSE ANALYSIS")
print("=" * 65)

print("\n1. DATASET OVERVIEW")
print("-" * 65)

print("\nFirst 5 Records:")
print(df.head())

print("\nDataset Shape:", df.shape)

print("\nColumn Names:")
print(df.columns.tolist())

print("\nData Types:")
print(df.dtypes)

print("\nMissing Values:")
print(df.isnull().sum())


# ==========================================
# 2. DATA CLEANING
# ==========================================

print("\n2. DATA CLEANING")
print("-" * 65)

print("Duplicate Rows:", df.duplicated().sum())

df = df.drop_duplicates()

df["Age"] = pd.to_numeric(df["Age"], errors="coerce")
df["Monthly Expense"] = pd.to_numeric(
    df["Monthly Expense"], errors="coerce"
)

df = df.dropna(
    subset=["Name", "Age", "Job", "Monthly Expense"]
)

print("\nMissing Values After Cleaning:")
print(df.isnull().sum())

print("\nTotal Records:", len(df))


# ==========================================
# 3. OVERALL EXPENSE STATISTICS
# ==========================================

print("\n3. OVERALL MONTHLY EXPENSE STATISTICS")
print("-" * 65)

print("Total Individuals:", len(df))

print("Total Monthly Expense: ₹",
      round(df["Monthly Expense"].sum(), 2))

print("Average Monthly Expense: ₹",
      round(df["Monthly Expense"].mean(), 2))

print("Highest Monthly Expense: ₹",
      df["Monthly Expense"].max())

print("Lowest Monthly Expense: ₹",
      df["Monthly Expense"].min())

print("Median Monthly Expense: ₹",
      df["Monthly Expense"].median())


# ==========================================
# 4. PROFESSION-WISE ANALYSIS
# ==========================================

print("\n4. PROFESSION-WISE EXPENSE ANALYSIS")
print("-" * 65)

profession_summary = df.groupby("Job").agg(
    Number_of_People=("Name", "count"),
    Average_Age=("Age", "mean"),
    Average_Monthly_Expense=("Monthly Expense", "mean"),
    Minimum_Expense=("Monthly Expense", "min"),
    Maximum_Expense=("Monthly Expense", "max")
)

profession_summary = profession_summary.sort_values(
    by="Average_Monthly_Expense"
)

print(profession_summary.round(1).to_string())


# ==========================================
# 5. GRAPH: AVERAGE EXPENSE BY PROFESSION
# ==========================================

print("\n5. GENERATING GRAPH...")

plt.figure(figsize=(15, 8))

jobs = profession_summary.index
amounts = profession_summary["Average_Monthly_Expense"]

plt.plot(
    jobs,
    amounts,
    marker="o",
    color="darkblue",
    linewidth=2
)

plt.title(
    "Average Monthly Amount by Profession",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel("Profession", fontsize=12)
plt.ylabel("Average Monthly Amount (₹)", fontsize=12)

plt.xticks(rotation=45, ha="right")

plt.grid(True, linestyle="--", alpha=0.5)

# Display values above each point
for i, value in enumerate(amounts):
    plt.annotate(
        "₹{:,.0f}".format(value),
        (i, value),
        textcoords="offset points",
        xytext=(0, 8),
        ha="center",
        fontsize=8,
        rotation=20
    )

plt.tight_layout()

plt.savefig("average_expense_by_profession.png", dpi=300)

plt.show()


# ==========================================
# 6. TOP 5 HIGHEST-SPENDING INDIVIDUALS
# ==========================================

print("\n6. TOP 5 HIGHEST SPENDING INDIVIDUALS")
print("-" * 65)

top_5 = df.nlargest(5, "Monthly Expense")

print(
    top_5[
        ["Name", "Age", "Job", "Monthly Expense"]
    ].to_string(index=False)
)


# ==========================================
# 7. KEY TAKEAWAYS
# ==========================================

print("\n7. KEY TAKEAWAYS")
print("-" * 65)

highest_spender = df.loc[
    df["Monthly Expense"].idxmax()
]

print(
    "Highest Spender:",
    highest_spender["Name"],
    "| Age:", int(highest_spender["Age"]),
    "| Job:", highest_spender["Job"],
    "| Amount: ₹",
    highest_spender["Monthly Expense"]
)

# Highest spending age group
df["Age_Group"] = pd.cut(
    df["Age"],
    bins=[0, 19, 29, 39, 49, 59, 100],
    labels=[
        "Under 20", "20-29", "30-39",
        "40-49", "50-59", "60+"
    ]
)

age_analysis = df.groupby(
    "Age_Group",
    observed=True
)["Monthly Expense"].mean()

print(
    "\nTop Age Bracket:",
    age_analysis.idxmax(),
    "(Average: ₹",
    round(age_analysis.max(), 2),
    ")"
)

# Highest average expense by exact age
exact_age = df.groupby("Age")["Monthly Expense"].mean()

print(
    "\nTop Exact Age:",
    int(exact_age.idxmax()),
    "(Average: ₹",
    round(exact_age.max(), 2),
    ")"
)

# Highest spending profession
top_profession = profession_summary[
    "Average_Monthly_Expense"
].idxmax()

print(
    "\nTop Profession:",
    top_profession,
    "(Average: ₹",
    round(
        profession_summary.loc[
            top_profession,
            "Average_Monthly_Expense"
        ], 2
    ),
    ")"
)

print("\n" + "=" * 65)
print("       ANALYSIS COMPLETED SUCCESSFULLY!")
print("=" * 65)