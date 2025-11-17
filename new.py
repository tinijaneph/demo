"""
Employee Change Tracker - Complete Implementation with Append Mode
Tracks employee data changes with schema evolution support (SCD2 pattern)
"""

from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.sql.window import Window
from pyspark.sql.types import DateType
from datetime import datetime
from typing import List, Set
from transforms.api import transform_df, Input, Output, incremental


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
    
    def detect_and_append_changes(self, new_df: DataFrame, 
                                 historical_df: DataFrame,
                                 effective_date: str = None) -> DataFrame:
        """
        Detect changes and return ONLY new records to append.
        This is used with set_mode="append".
        
        Args:
            new_df: New/current employee data (without tracking columns)
            historical_df: Historical tracking data (with tracking columns)
            effective_date: Date for new changes (YYYY-MM-DD) or None for today
            
        Returns:
            DataFrame with ONLY new records to append (not full history)
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
        
        # Collect records to append
        records_to_append = []
        
        # 1. Handle schema evolution - add new version for all employees if new columns detected
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
            records_to_append.append(schema_change_records)
        
        # 2. Detect new employees
        new_employees = self._detect_new_employees(new_df_aligned, historical_df_aligned)
        if new_employees.count() > 0:
            records_to_append.append(new_employees)
        
        # 3. Detect changed records
        changed_records = self._detect_changes(new_df_aligned, historical_df_aligned, data_columns)
        if changed_records.count() > 0:
            records_to_append.append(changed_records)
        
        # Combine all new records
        if records_to_append:
            result = records_to_append[0]
            for df in records_to_append[1:]:
                result = result.unionByName(df)
            return result.drop_duplicates()
        else:
            # No changes detected - return empty DataFrame with correct schema
            return new_df_aligned.filter(F.lit(False))
    
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


# ============================================================================
# FOUNDRY TRANSFORM IMPLEMENTATION - 1 INPUT, 1 OUTPUT WITH APPEND MODE
# ============================================================================

@transform_df(
    Output("ri.foundry.main.dataset.68d6dc4a-705d-4fcd-97cb-9bdbebe6384d"),
    employee_data=Input("ri.foundry.main.dataset.26c1c4e9-6594-4001-8451-9dbc41aee364")
)
def compute(employee_data, ctx):
    """
    Track employee changes with schema evolution support using append mode.
    
    Uses df.set_mode("append") to append records.
    
    Strategy:
    - First run: Initialize with "Original/1" (snapshot mode)
    - Value changes: Append changed records (append mode)
    - New columns: Append "Original/2" records with new column values (append mode)
      Old records will have NULL for new columns automatically
    
    Args:
        employee_data: Current employee data (your source dataset with 10 columns)
        ctx: Transform context
        
    Returns:
        DataFrame with set_mode configured
    """
    # Initialize tracker
    tracker = EmployeeChangeTracker(
        primary_key="Employee_ID",
        effective_date_col="Effective_Date",
        note_col="Note"
    )
    
    # Try to read existing historical data from output
    try:
        output_dataset = ctx.get_output_dataset()
        historical_output = output_dataset.dataframe()
        
        hist_count = historical_output.count()
        has_tracking_cols = 'Effective_Date' in historical_output.columns and \
                           'Note' in historical_output.columns
        
        if hist_count > 0 and has_tracking_cols:
            # Subsequent run - check for schema changes
            existing_data_cols = set(historical_output.columns) - {'Employee_ID', 'Effective_Date', 'Note'}
            new_data_cols = set(employee_data.columns) - {'Employee_ID'}
            
            new_columns = new_data_cols - existing_data_cols
            
            if new_columns:
                # NEW COLUMNS DETECTED - Append "Original/2" records
                # Get latest record for each employee from historical data
                window_spec = Window.partitionBy('Employee_ID').orderBy(F.desc('Effective_Date'))
                latest_records = historical_output.withColumn("rn", F.row_number().over(window_spec)) \
                                                 .filter(F.col("rn") == 1) \
                                                 .drop("rn")
                
                # Get current employee data with new columns
                current_date = datetime.now().strftime('%Y-%m-%d')
                
                # Create "Original/2" records from current employee_data
                # Add tracking columns
                original_2_records = employee_data.withColumn(
                    'Effective_Date',
                    F.lit(current_date).cast(DateType())
                ).withColumn(
                    'Note',
                    F.lit(f"Original/2 - Added columns: {', '.join(sorted(list(new_columns)))}")
                )
                
                # Add NULL values for new columns to match schema
                for col in new_columns:
                    if col in employee_data.columns:
                        col_type = employee_data.schema[col].dataType
                    else:
                        col_type = StringType()
                    
                    # Add new columns to ensure schema compatibility
                    if col not in original_2_records.columns:
                        original_2_records = original_2_records.withColumn(col, F.lit(None).cast(col_type))
                
                # Return Original/2 records with APPEND mode
                # Old records will automatically have NULL for new columns
                return original_2_records.set_mode("append")
                
            else:
                # NO SCHEMA CHANGE - Detect value changes and append
                new_records = tracker.detect_and_append_changes(
                    new_df=employee_data,
                    historical_df=historical_output
                )
                
                if new_records.count() > 0:
                    # Ensure column order matches existing schema
                    existing_cols = list(historical_output.columns)
                    new_records = new_records.select(existing_cols)
                    
                    # Return with APPEND mode
                    return new_records.set_mode("append")
                else:
                    # No changes - return empty DataFrame
                    return historical_output.limit(0).set_mode("append")
        else:
            # First run - initialize all records with SNAPSHOT mode
            result = tracker.initialize_historical_data(employee_data)
            return result.set_mode("snapshot")
            
    except Exception:
        # First run - output doesn't exist yet
        result = tracker.initialize_historical_data(employee_data)
        return result.set_mode("snapshot")
