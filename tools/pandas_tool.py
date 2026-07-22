import os
import pandas as pd


class PandasTool:
    def __init__(self):
        self.df = None
        self.file_name = None

    def load_csv(self, file_path="data/sales.csv"):
        """
        Load a CSV file.
        By default, it loads data/sales.csv.
        """

        if not os.path.exists(file_path):
            return f"❌ File not found: {file_path}"

        try:
            self.df = pd.read_csv(file_path)
            self.file_name = os.path.basename(file_path)

            return (
                f"✅ Successfully loaded '{self.file_name}'\n"
                f"Rows: {self.df.shape[0]}\n"
                f"Columns: {self.df.shape[1]}"
            )

        except Exception as e:
            return f"❌ Error loading CSV:\n{e}"

    def is_loaded(self):
        return self.df is not None

    def get_dataframe(self):
        return self.df

    def get_shape(self):
        if not self.is_loaded():
            return "No dataset loaded."

        return self.df.shape

    def get_columns(self):
        if not self.is_loaded():
            return []

        return list(self.df.columns)

    def preview(self, rows=5):
        if not self.is_loaded():
            return "No dataset loaded."

        return self.df.head(rows)

    def tail(self, rows=5):
        if not self.is_loaded():
            return "No dataset loaded."

        return self.df.tail(rows)

    def sample(self, rows=5):
        if not self.is_loaded():
            return "No dataset loaded."

        return self.df.sample(min(rows, len(self.df)))

    def dataset_info(self):
        if not self.is_loaded():
            return {}

        return {
            "File": self.file_name,
            "Rows": self.df.shape[0],
            "Columns": self.df.shape[1],
            "Column Names": list(self.df.columns),
            "Data Types": self.df.dtypes.astype(str).to_dict(),
            "Missing Values": self.df.isnull().sum().to_dict(),
            "Duplicate Rows": int(self.df.duplicated().sum()),
            "Memory Usage (KB)": round(
                self.df.memory_usage(deep=True).sum() / 1024, 2
            ),
        }

    def numeric_columns(self):
        if not self.is_loaded():
            return []

        return list(self.df.select_dtypes(include="number").columns)

    def categorical_columns(self):
        if not self.is_loaded():
            return []

        return list(
            self.df.select_dtypes(
                include=["object", "category"]
            ).columns
        )

    def describe(self):
        if not self.is_loaded():
            return "No dataset loaded."

        return self.df.describe(include="all")

    def missing_values(self):
        if not self.is_loaded():
            return "No dataset loaded."

        return self.df.isnull().sum()

    def correlation(self):
        if not self.is_loaded():
            return "No dataset loaded."

        numeric = self.df.select_dtypes(include="number")

        if numeric.empty:
            return "No numeric columns found."

        return numeric.corr()

    def group_by(self, column, agg_column, agg="sum"):
        if not self.is_loaded():
            return "No dataset loaded."

        if column not in self.df.columns:
            return f"Column '{column}' not found."

        if agg_column not in self.df.columns:
            return f"Column '{agg_column}' not found."

        return (
            self.df.groupby(column)[agg_column]
            .agg(agg)
            .sort_values(ascending=False)
        )

    def filter_rows(self, column, value):
        if not self.is_loaded():
            return "No dataset loaded."

        if column not in self.df.columns:
            return f"Column '{column}' not found."

        return self.df[self.df[column] == value]

    def unique_values(self, column):
        if not self.is_loaded():
            return "No dataset loaded."

        if column not in self.df.columns:
            return f"Column '{column}' not found."

        return self.df[column].unique().tolist()

    def value_counts(self, column):
        if not self.is_loaded():
            return "No dataset loaded."

        if column not in self.df.columns:
            return f"Column '{column}' not found."

        return self.df[column].value_counts()