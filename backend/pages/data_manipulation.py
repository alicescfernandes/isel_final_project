import pandas as pd

def extract_dimensions(df, dimensions):
    """
    Returns category/filter dimensions from the dataframe.

    - If dimensions == 1:
        Returns a list containing the column names starting from index 1 (i.e., the labels/filters).
    - If dimensions > 1:
        Returns a list of lists, each containing the values of the first `dimensions` columns.

    Args:
        df (pd.DataFrame): The input dataframe.
        dimensions (int): Number of dimensions to extract.

    Returns:
        list: A single list of column names (if dimensions == 1),
              or a list of lists with column values (if dimensions > 1).

    Examples:
        # For CSV 1 (horizontal):
        dimensions = 1 → [['Costcutter', 'Innovator', 'Mercedes', 'Workhorse', 'Traveler']]
        
        # For CSV 2 (vertical):
        dimensions = 1 → [['Brand', 'Company', 'Price', 'Rebate']]
        dimensions = 2 → [['MOVE 2.1.', 'MORPHEUS', ...], ['SWITCH', 'SWITCH', ...]]
    """
    if dimensions == 1:
        # Special case: return the column names from index 1 onward
        return [df.columns[1:].tolist()]
    else:
        # Return the values from the first `dimensions` columns
        return [df.iloc[:, i].tolist() for i in range(dimensions)]
