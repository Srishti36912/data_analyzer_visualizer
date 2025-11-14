# Profiling = Understanding the dataset automatically.
import pandas as pd
from ydata_profiling import ProfileReport


class DataProfiler:
    """Handles all data profiling (analysis-only) tasks."""

    def __init__(self, df: pd.DataFrame):
        self.df = df

    # ----------------------------------------------------
    # 1. BASIC SUMMARY
    # ----------------------------------------------------
    def get_basic_summary(self):
        """Returns shape, column names and basic info."""
        return {
            "num_rows": self.df.shape[0],
            "num_columns": self.df.shape[1],
            "columns": list(self.df.columns)
        }

    # ----------------------------------------------------
    # 2. MISSING VALUES SUMMARY
    # ----------------------------------------------------
    def get_missing_summary(self):
        """Returns count and percentage of missing values per column."""
        missing = self.df.isna().sum()
        percent = (missing / len(self.df)) * 100

        summary = pd.DataFrame({
            "missing_count": missing,
            "missing_percent": percent.round(2)
        })

        return summary.sort_values("missing_percent", ascending=False)

    # ----------------------------------------------------
    # 3. NUMERIC SUMMARY (min, max, mean, etc.)
    # ----------------------------------------------------
    def get_numeric_summary(self):
        """Returns describe() stats only for numeric columns."""
        return self.df.describe(include="number").T

    # ----------------------------------------------------
    # 4. CATEGORICAL SUMMARY (unique counts)
    # ----------------------------------------------------
    def get_categorical_summary(self):
        """Returns unique value counts for categorical columns."""
        cat_df = self.df.select_dtypes(include="object")
        return cat_df.nunique().sort_values(ascending=False)

    # ----------------------------------------------------
    # 5. DUPLICATE SUMMARY
    # ----------------------------------------------------
    def get_duplicate_summary(self):
        """Returns number of duplicate rows."""
        duplicate_count = self.df.duplicated().sum()
        return {
            "duplicate_rows": duplicate_count,
            "duplicate_percent": round(duplicate_count / len(self.df) * 100, 2)
        }

    # ----------------------------------------------------
    # 6. GENERATE FULL HTML REPORT (optional)
    # ----------------------------------------------------
    def get_profile_report(self, output_file="profile_report.html"):
        """
        Generates an HTML profiling report using ydata_profiling.
        Returns the file path so Streamlit can show/download it.
        """
        profile = ProfileReport(self.df, title="Smart Data Profiler Report")
        profile.to_file(output_file)
        return output_file


