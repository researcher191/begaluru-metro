import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from metro_data import load_station_data, load_connection_data, load_passenger_data
from route_finder import find_route, get_all_stations
from visualization import (
    plot_monthly_passengers,
    plot_yearly_passengers,
    plot_line_utilization,
    plot_peak_hours,
    plot_passenger_growth,
    plot_station_traffic
)

# Page configuration
st.set_page_config(
    page_title="Bengaluru Metro Analysis",
    page_icon="🚇",
    layout="wide"
)

# Title
st.title("Bengaluru Metro Analysis Dashboard")
st.markdown("""
This application provides analysis and visualization of the Bengaluru Metro system, 
including route finding and passenger statistics.
""")

# Load data
try:
    stations_df = load_station_data()
    connections_df = load_connection_data()
    passenger_df = load_passenger_data()
    all_stations = get_all_stations(stations_df)
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select a page:", ["Route Finder", "Passenger Analysis", "Station Statistics"])

if page == "Route Finder":
    st.header("Metro Route Finder")
    
    col1, col2 = st.columns(2)
    
    with col1:
        source = st.selectbox("Select source station:", all_stations)
    
    with col2:
        # Filter out the source station from destination options
        destination_options = [station for station in all_stations if station != source]
        destination = st.selectbox("Select destination station:", destination_options)
    
    if st.button("Find Route"):
        if source and destination:
            route, lines_used = find_route(source, destination, stations_df, connections_df)
            
            if route:
                st.success(f"Route found from {source} to {destination}!")
                
                # Display route information
                st.subheader("Route Details:")
                route_display = " → ".join(route)
                st.write(route_display)
                
                # Display metro lines to use
                st.subheader("Metro Lines to Use:")
                for line_info in lines_used:
                    line, start, end = line_info
                    line_color = "green" if line == "Green Line" else "purple" if line == "Purple Line" else "blue" if line == "Blue Line" else "yellow"
                    st.markdown(f"<span style='color:{line_color};'>•</span> {line}: From {start} to {end}", unsafe_allow_html=True)
                
                # Number of stations
                st.info(f"Total stations: {len(route) - 1}")
                
                # Estimated time (assuming 2 minutes per station)
                time_mins = (len(route) - 1) * 2
                st.info(f"Estimated travel time: {time_mins} minutes")
            else:
                st.error("No route found between the selected stations.")
        else:
            st.warning("Please select both source and destination stations.")

elif page == "Passenger Analysis":
    st.header("Passenger Data Analysis")
    
    analysis_type = st.selectbox(
        "Select analysis type:",
        ["Monthly Passenger Trends", "Yearly Passenger Trends",  "Passenger Growth"]
    )
    
    if analysis_type == "Monthly Passenger Trends":
        st.subheader("Monthly Passenger Data")
        
        # Year filter
        years = sorted(passenger_df['Year'].unique())
        selected_year = st.selectbox("Select year:", years)
        
        # Filter data for selected year
        year_data = passenger_df[passenger_df['Year'] == selected_year]
        
        # Plot
        fig = plot_monthly_passengers(year_data, selected_year)
        st.pyplot(fig)
        
       
        
    elif analysis_type == "Yearly Passenger Trends":
        st.subheader("Yearly Passenger Data")
        
        fig = plot_yearly_passengers(passenger_df)
        st.pyplot(fig)
        
        # Statistics
        st.subheader("Yearly Statistics")
        yearly_stats = passenger_df.groupby('Year')['Passengers'].agg(['mean', 'min', 'max', 'sum']).reset_index()
        yearly_stats.columns = ['Year', 'Average Monthly', 'Minimum Monthly', 'Maximum Monthly', 'Total']
        st.dataframe(yearly_stats)
        

        
    elif analysis_type == "Passenger Growth":
        st.subheader("Passenger Growth Analysis")
        
        fig = plot_passenger_growth(passenger_df)
        st.pyplot(fig)
        
        # Year-over-year growth statistics
        st.subheader("Year-over-Year Growth")
        yearly_total = passenger_df.groupby('Year')['Passengers'].sum().reset_index()
        yearly_total['Growth'] = yearly_total['Passengers'].pct_change() * 100
        yearly_total['Growth'] = yearly_total['Growth'].apply(lambda x: f"{x:.2f}%" if not pd.isna(x) else "N/A")
        st.dataframe(yearly_total)

elif page == "Station Statistics":
    st.header("Station Traffic Analysis")
    
    # Station selection
    selected_station = st.selectbox("Select a station:", all_stations)
    
    # Year filter
    years = sorted(passenger_df['Year'].unique())
    selected_year = st.selectbox("Select year:", years)
    
    # Peak hours analysis
    st.subheader("Peak Hours Analysis")
    fig_peak = plot_peak_hours(selected_station, selected_year)
    st.pyplot(fig_peak)
    
    # Station traffic comparison
    st.subheader("Station Traffic Comparison")
    top_n = st.slider("Select number of stations to compare:", 5, 20, 10)
    fig_traffic = plot_station_traffic(passenger_df, stations_df, selected_year, top_n)
    st.pyplot(fig_traffic)

# Footer
st.sidebar.markdown("---")