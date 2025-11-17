"""
Employee Change Tracker - Complete Implementation
Tracks employee data changes with schema evolution support (SCD2 pattern)
"""

from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.sql.window import Window
from pyspark.sql.types import DateType
from datetime import datetime
from typing import List, Set
from transforms.api import transform_df, Input, Output


class EmployeeChangeTracker:
    """
    A class to track employee data changes with support for schema evolution.
    Implements Slowly Changing Dimension Type 2 (SCD2) pattern.
    """
    
    def __init__(self, primary_key: str = "Employee_ID", 
                 effective_date_col: str = "Effective_Date",
                 note_col: str = "Note"):
        """
        Initialize the change tracker.
        
        Args:
            primary_key: Column name for unique employee identifier
            effective_date_col: Column name for tracking effective date
            note_col: Column name for tracking change notes
        """
        self.primary_key = primary_key
        self.effective_date_col = effective_date_col
        self.note_col = note_col
        self.tracking_columns = {primary_key, effective_date_col, note_col}
        
    def initialize_historical_data(self, df: DataFrame, 
                                   effective_date: str = None) -> DataFrame:
        """
        Initialize historical tracking for first load.
        
        Args:
            df: Source DataFrame
            effective_date: Date string (YYYY-MM-DD) or None for today
            
        Returns:
            DataFrame with Effective_Date and Note columns added
        """
        if effective_date is None:
            effective_date = datetime.now().strftime('%Y-%m-%d')
            
        return df.withColumn(self.effective_date_col, F.lit(effective_date).cast(DateType())) \
                 .withColumn(self.note_col, F.lit("Original/1"))
    
    def _get_data_columns(self, df: DataFrame) -> Set[str]:
        """Get data columns excluding tracking columns."""
        return set(df.columns) - self.tracking_columns
    
    def _align_schemas(self, new_df: DataFrame, 
                      historical_df: DataFrame) -> tuple:
        """
        Align schemas between new and historical data, handling new columns.
        
        Returns:
            Tuple of (aligned_new_df, aligned_historical_df, new_columns_list)
        """
        new_cols = set(new_df.columns)
        hist_cols = set(historical_df.columns)
        
        # Find truly new columns (excluding tracking columns)
        new_data_cols = (new_cols - hist_cols) - self.tracking_columns
        missing_in_new = (hist_cols - new_cols) - self.tracking_columns
        
        # Add missing columns to new_df with null values
        for col in missing_in_new:
            col_type = historical_df.schema[col].dataType
            new_df = new_df.withColumn(col, F.lit(None).cast(col_type))
        
        # Add new columns to historical_df with null values
        for col in new_data_cols:
            col_type = new_df.schema[col].dataType
            historical_df = historical_df.withColumn(col, F.lit(None).cast(col_type))
        
        # Ensure column order matches
        all_cols = [self.primary_key] + \
                   sorted(list((new_cols | hist_cols) - self.tracking_columns - {self.primary_key})) + \
                   [self.effective_date_col, self.note_col]
        
        return (new_df.select(all_cols), 
                historical_df.select(all_cols), 
                sorted(list(new_data_cols)))
    
    def _detect_changes(self, new_df: DataFrame, 
                       historical_df: DataFrame,
                       data_columns: List[str]) -> DataFrame:
        """
        Detect which records have changed values.
        
        Returns:
            DataFrame with changed records and change descriptions
        """
        # Get latest record for each employee
        window_spec = Window.partitionBy(self.primary_key).orderBy(F.desc(self.effective_date_col))
        latest_historical = historical_df.withColumn("rn", F.row_number().over(window_spec)) \
                                        .filter(F.col("rn") == 1) \
                                        .drop("rn")
        
        # Join new data with latest historical
        joined = new_df.alias("new").join(
            latest_historical.alias("hist"),
            on=self.primary_key,
            how="inner"
        )
        
        # Build change detection expressions
        change_conditions = []
        change_descriptions = []
        
        for col in data_columns:
            if col == self.primary_key:
                continue
                
            # Handle null comparisons properly
            change_condition = (
                ~F.col(f"new.{col}").eqNullSafe(F.col(f"hist.{col}"))
            )
            change_conditions.append(change_condition)
            
            # Create change description
            change_desc = F.when(
                change_condition,
                F.lit(f"Changed {col}")
            )
            change_descriptions.append(change_desc)
        
        # Combine all change conditions
        if not change_conditions:
            # No columns to compare, return empty DataFrame
            return joined.filter(F.lit(False)).select(
                [F.col(f"new.{col}").alias(col) for col in new_df.columns]
            )
        
        any_change = change_conditions[0]
        for condition in change_conditions[1:]:
            any_change = any_change | condition
        
        # Create consolidated change note
        change_note = F.concat_ws(", ", *[desc for desc in change_descriptions if desc is not None])
        
        # Filter to only changed records and select new values
        changed_records = joined.filter(any_change).select(
            [F.col(f"new.{col}").alias(col) for col in new_df.columns if col != self.note_col]
        ).withColumn(self.note_col, change_note)
        
        return changed_records
    
    def _detect_new_employees(self, new_df: DataFrame, 
                             historical_df: DataFrame) -> DataFrame:
        """Detect completely new employees not in historical data."""
        new_employees = new_df.join(
            historical_df.select(self.primary_key).distinct(),
            on=self.primary_key,
            how="left_anti"
        )
        
        # Mark as new employees
        if new_employees.count() > 0:
            return new_employees.withColumn(self.note_col, F.lit("New Employee"))
        return new_employees
    
    def track_changes(self, new_df: DataFrame, 
                     historical_df: DataFrame,
                     effective_date: str = None) -> DataFrame:
        """
        Main function to track changes between new and historical data.
        
        Args:
            new_df: New/current employee data (without tracking columns)
            historical_df: Historical tracking data (with tracking columns)
            effective_date: Date for new changes (YYYY-MM-DD) or None for today
            
        Returns:
            Updated DataFrame with all historical records plus new changes
        """
        if effective_date is None:
            effective_date = datetime.now().strftime('%Y-%m-%d')
        
        # Handle schema changes
        new_df_aligned, historical_df_aligned, new_columns = self._align_schemas(
            new_df, historical_df
        )
        
        # Add effective date to new data
        new_df_aligned = new_df_aligned.withColumn(
            self.effective_date_col, 
            F.lit(effective_date).cast(DateType())
        )
        
        # Get data columns for comparison (excluding tracking columns)
        data_columns = sorted(list(self._get_data_columns(new_df_aligned)))
        
        # Detect new employees
        new_employees = self._detect_new_employees(new_df_aligned, historical_df_aligned)
        
        # Detect changed records
        changed_records = self._detect_changes(new_df_aligned, historical_df_aligned, data_columns)
        
        # Handle schema evolution - add new version for all employees if new columns detected
        schema_change_records = None
        if new_columns:
            # Get latest record for each employee
            window_spec = Window.partitionBy(self.primary_key).orderBy(F.desc(self.effective_date_col))
            latest_records = historical_df_aligned.withColumn("rn", F.row_number().over(window_spec)) \
                                                 .filter(F.col("rn") == 1) \
                                                 .drop("rn", self.effective_date_col, self.note_col)
            
            # Create new version with schema update
            schema_change_records = latest_records.withColumn(
                self.effective_date_col,
                F.lit(effective_date).cast(DateType())
            ).withColumn(
                self.note_col,
                F.lit(f"Original/2 - Added columns: {', '.join(new_columns)}")
            )
        
        # Combine all records
        result_df = historical_df_aligned
        
        if schema_change_records and schema_change_records.count() > 0:
            result_df = result_df.unionByName(schema_change_records)
        
        if new_employees.count() > 0:
            result_df = result_df.unionByName(new_employees)
            
        if changed_records.count() > 0:
            result_df = result_df.unionByName(changed_records)
        
        return result_df.drop_duplicates()
    
    def filter_by_date_rules(self, df: DataFrame, 
                            keep_latest: bool = True,
                            keep_month_end: bool = True) -> DataFrame:
        """
        Filter records based on date rules (month-end and latest date).
        
        Args:
            df: DataFrame to filter
            keep_latest: Keep records with the latest effective date
            keep_month_end: Keep records at end of month
            
        Returns:
            Filtered DataFrame
        """
        conditions = []
        
        if keep_month_end:
            is_month_end = F.expr(f"last_day({self.effective_date_col}) = {self.effective_date_col}")
            conditions.append(is_month_end)
        
        if keep_latest:
            latest_date = df.agg(F.max(self.effective_date_col)).collect()[0][0]
            is_latest = F.col(self.effective_date_col) == F.lit(latest_date)
            conditions.append(is_latest)
        
        if conditions:
            combined_condition = conditions[0]
            for condition in conditions[1:]:
                combined_condition = combined_condition | condition
            return df.filter(combined_condition).drop_duplicates()
        
        return df


# ============================================================================
# FOUNDRY TRANSFORM IMPLEMENTATION
# ============================================================================

@transform_df(
    Output("ri.foundry.main.dataset.68d6dc4a-705d-4fcd-97cb-9bdbebe6384d"),
    employee_data=Input("ri.foundry.main.dataset.26c1c4e9-6594-4001-8451-9dbc41aee364")
)
def compute(employee_data, ctx):
    """
    Track employee changes with schema evolution support.
    
    Uses incremental mode: reads previous output, compares with new input, writes combined result.
    
    First run: Initialize with employee_data 
    Subsequent runs: Track changes between employee_data and previous output
    
    Args:
        employee_data: Current employee data (your source dataset with 10 columns)
        ctx: Transform context to access previous output
        
    Returns:
        Updated historical dataset with all changes tracked
    """
    # Initialize tracker with your primary key
    tracker = EmployeeChangeTracker(
        primary_key="Employee_ID",
        effective_date_col="Effective_Date",
        note_col="Note"
    )
    
    try:
        # Try to read previous output (historical data)
        previous_output = ctx.spark_session.read.format("foundry").load(
            "ri.foundry.main.dataset.68d6dc4a-705d-4fcd-97cb-9bdbebe6384d"
        )
        
        hist_count = previous_output.count()
        has_tracking_cols = 'Effective_Date' in previous_output.columns and \
                           'Note' in previous_output.columns
        
        if hist_count == 0 or not has_tracking_cols:
            # First initialization - this is your first run
            print("Initializing historical tracking - First run")
            output_df = tracker.initialize_historical_data(employee_data)
        else:
            # Track changes - compare current data with previous output
            print(f"Tracking changes - Historical records: {hist_count}")
            output_df = tracker.track_changes(
                new_df=employee_data,
                historical_df=previous_output
            )
            
            # Apply date filtering rules (keep month-end and latest date)
            output_df = tracker.filter_by_date_rules(
                output_df,
                keep_latest=True,
                keep_month_end=True
            )
            
            print(f"Output records after tracking: {output_df.count()}")
            
    except Exception as e:
        # First run or error reading previous output - initialize fresh
        print(f"Initializing (first run or error): {e}")
        output_df = tracker.initialize_historical_data(employee_data)
    
    return output_df.drop_duplicates()
