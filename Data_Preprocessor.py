
class Data_Preprocessor:

    def get_df_within_range(self, df, col_name, START_DATE, END_DATE):
        mask = (df[col_name] > START_DATE) & (df[col_name] <= END_DATE)
        df = df.loc[mask]
        return df