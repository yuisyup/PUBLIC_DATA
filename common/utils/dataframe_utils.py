from pandas.core.frame import DataFrame

class DataFrameUtils:
    
    def insert_last_column_fixed_value(self, df_resolved: DataFrame, column_name, column_content):
        """
        DataFrame最後列に任意の列名と固定値を付与する。
        
        :param column_name: カラム名
        :param column_content: カラム内容（固定値）
        """     
        
        df_resolved.insert(len(df_resolved.columns), column_name, column_content)
        
        return 