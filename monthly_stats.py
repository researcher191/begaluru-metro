from BengaluruMetroTracker.app import year_data


monthly_stats = year_data.groupby('Month')['Passengers'].agg(['mean', 'median', 'min', 'max', 'sum']).reset_index()