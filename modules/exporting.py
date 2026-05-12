def export_results(processed_df, path: str = 'data/bank-permata-labeling-data-set-result.xlsx'):
    processed_df.to_excel(path, index=False)
