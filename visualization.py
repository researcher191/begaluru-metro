import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from calendar import month_name

# Set Seaborn style for plots
sns.set_style("whitegrid")
plt.rcParams.update({'font.size': 12})

def plot_monthly_passengers(data, year):
    """
    Plot monthly passenger data for a specific year
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Month names for the x-axis
    months = [month_name[i] for i in range(1, 13)]
    
    # Prepare data
    monthly_data = data.sort_values('Month')
    
    # Plot bars for Purple and Green lines
    x = np.arange(len(months))
    width = 0.35
    
    purple = ax.bar(x - width/2, monthly_data['Purple_Line_Passengers'], width, label='Purple Line', color='purple', alpha=0.7)
    green = ax.bar(x + width/2, monthly_data['Green_Line_Passengers'], width, label='Green Line', color='green', alpha=0.7)
    
    # Add total line
    ax2 = ax.twinx()
    total_line = ax2.plot(x, monthly_data['Passengers'], 'r-', marker='o', linewidth=2, label='Total Passengers')
    
    # Set labels and title
    ax.set_title(f'Monthly Passenger Data for {year}')
    ax.set_xlabel('Month')
    ax.set_ylabel('Passengers by Line')
    ax2.set_ylabel('Total Passengers')
    
    # Set x-ticks
    ax.set_xticks(x)
    ax.set_xticklabels(months, rotation=45)
    
    # Add legend
    lines, labels = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines + lines2, labels + labels2, loc='upper left')
    
    plt.tight_layout()
    return fig

def plot_yearly_passengers(data):
    """
    Plot yearly passenger data
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Aggregate data by year
    yearly_data = data.groupby('Year').agg({
        'Passengers': 'sum',
        'Purple_Line_Passengers': 'sum',
        'Green_Line_Passengers': 'sum'
    }).reset_index()
    
    # Plot stacked bars
    ax.bar(yearly_data['Year'], yearly_data['Purple_Line_Passengers'], color='purple', alpha=0.7, label='Purple Line')
    ax.bar(yearly_data['Year'], yearly_data['Green_Line_Passengers'], bottom=yearly_data['Purple_Line_Passengers'], 
           color='green', alpha=0.7, label='Green Line')
    
    # Add labels and title
    ax.set_title('Yearly Passenger Data')
    ax.set_xlabel('Year')
    ax.set_ylabel('Total Passengers')
    ax.legend()
    
    # Add total passenger numbers on top of bars
    for i, year in enumerate(yearly_data['Year']):
        total = yearly_data.iloc[i]['Passengers']
        ax.text(year, total + 50000, f'{total:,}', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    return fig

def plot_line_utilization(data, year):
    """
    Plot metro line utilization for a specific year
    """
    fig, ax = plt.subplots(figsize=(14, 7))
    
    # Filter data for the selected year
    year_data = data[data['Year'] == year].copy()
    year_data['Purple_Line_Percentage'] = year_data['Purple_Line_Passengers'] / year_data['Passengers'] * 100
    year_data['Green_Line_Percentage'] = year_data['Green_Line_Passengers'] / year_data['Passengers'] * 100
    
    # Month names for the x-axis
    months = [month_name[i] for i in range(1, 13)]
    
    # Create line plot
    x = np.arange(len(months))
    
    ax.plot(x, year_data['Purple_Line_Percentage'], 'purple', marker='o', linewidth=2, label='Purple Line')
    ax.plot(x, year_data['Green_Line_Percentage'], 'green', marker='s', linewidth=2, label='Green Line')
    
    # Set labels and title
    ax.set_title(f'Line Utilization Percentage in {year}')
    ax.set_xlabel('Month')
    ax.set_ylabel('Percentage of Total Passengers')
    
    # Set x-ticks
    ax.set_xticks(x)
    ax.set_xticklabels(months, rotation=45)
    
    # Set y-axis to percentage
    ax.set_ylim(0, 100)
    ax.axhline(y=50, color='gray', linestyle='--', alpha=0.7)
    
    # Add legend
    ax.legend()
    
    plt.tight_layout()
    return fig

def plot_passenger_growth(data):
    """
    Plot passenger growth rate year over year
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Calculate year over year growth
    yearly_total = data.groupby('Year')['Passengers'].sum().reset_index()
    yearly_total['Growth'] = yearly_total['Passengers'].pct_change() * 100
    
    # Bar chart for total passengers
    bars = ax.bar(yearly_total['Year'], yearly_total['Passengers'], color='royalblue', alpha=0.7)
    
    # Create a second y-axis for growth rate
    ax2 = ax.twinx()
    line = ax2.plot(yearly_total['Year'][1:], yearly_total['Growth'][1:], 'r-o', linewidth=2, label='Growth Rate')
    
    # Set labels and title
    ax.set_title('Annual Passenger Growth')
    ax.set_xlabel('Year')
    ax.set_ylabel('Total Passengers')
    ax2.set_ylabel('Year-over-Year Growth (%)')
    
    # Add data labels on bars
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 5000,
                f'{int(height):,}',
                ha='center', va='bottom', rotation=0)
    
    # Format second y-axis
    ax2.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
    
    # Add legend
    lines, labels = ax2.get_legend_handles_labels()
    ax2.legend(lines, labels, loc='upper right')
    
    plt.tight_layout()
    return fig

def plot_peak_hours(station, year):
    """
    Plot peak hours analysis for a station
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Create sample hourly distribution data
    hours = list(range(5, 24))  # 5 AM to 11 PM
    
    # Morning peak (8-10 AM), evening peak (5-8 PM)
    hourly_distribution = [
        500, 1200, 2500, 3500, 3000,  # 5-9 AM
        2000, 1500, 1200, 1500, 1800,  # 10AM-2PM
        2000, 2500, 3500, 4000, 3500,  # 3-7PM
        2500, 1500, 800, 300  # 8-11PM
    ]
    
    # Add some randomness
    hourly_distribution = [h * (1 + np.random.uniform(-0.1, 0.1)) for h in hourly_distribution]
    
    # Plot bar chart
    bars = ax.bar(hours, hourly_distribution, color='royalblue')
    
    # Highlight peak hours
    peak_hours_morning = [8, 9]
    peak_hours_evening = [17, 18, 19]
    
    for hour in peak_hours_morning:
        idx = hours.index(hour)
        bars[idx].set_color('red')
    
    for hour in peak_hours_evening:
        idx = hours.index(hour)
        bars[idx].set_color('red')
    
    # Set labels and title
    ax.set_title(f'Hourly Traffic at {station} Station ({year})')
    ax.set_xlabel('Hour of Day')
    ax.set_ylabel('Average Number of Passengers')
    ax.set_xticks(hours)
    ax.set_xticklabels([f'{h}:00' for h in hours])
    
    # Add morning and evening peak hour annotations
    ax.annotate('Morning\nPeak', xy=(8.5, 3500), xytext=(8.5, 4000),
                arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8),
                ha='center', fontweight='bold')
    
    ax.annotate('Evening\nPeak', xy=(18, 4000), xytext=(18, 4500),
                arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8),
                ha='center', fontweight='bold')
    
    plt.tight_layout()
    return fig

def plot_station_traffic(passenger_data, station_data, year, top_n=10):
    """
    Plot station traffic comparison
    """
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Create sample station traffic data
    stations = station_data['Station_Name'].tolist()[:top_n]
    
    # Generate traffic data with busier central stations
    traffic = []
    for i, station in enumerate(stations):
        if i < top_n // 3:  # Busier stations (central)
            base = 800000 + np.random.randint(-50000, 50000)
        elif i < 2 * top_n // 3:  # Medium traffic
            base = 500000 + np.random.randint(-40000, 40000)
        else:  # Lower traffic
            base = 300000 + np.random.randint(-30000, 30000)
        traffic.append(base)
    
    # Get station lines
    lines = station_data['Line'].tolist()[:top_n]
    colors = ['purple' if line == 'Purple Line' else 'green' for line in lines]
    
    # Sort from highest to lowest
    sorted_indices = np.argsort(traffic)[::-1]
    sorted_stations = [stations[i] for i in sorted_indices]
    sorted_traffic = [traffic[i] for i in sorted_indices]
    sorted_colors = [colors[i] for i in sorted_indices]
    
    # Plot horizontal bar chart
    bars = ax.barh(sorted_stations, sorted_traffic, color=sorted_colors, alpha=0.7)
    
    # Set labels and title
    ax.set_title(f'Station Traffic Comparison ({year})')
    ax.set_xlabel('Annual Passenger Count')
    ax.set_ylabel('Station')
    
    # Add data labels
    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax.text(width + 10000, bar.get_y() + bar.get_height()/2,
                f'{int(width):,}',
                ha='left', va='center')
    
    # Add legend
    from matplotlib.patches import Patch
    
    
    plt.tight_layout()
    return fig
