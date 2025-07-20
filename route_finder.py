import pandas as pd
import networkx as nx

def get_all_stations(stations_df):
    """
    Get a list of all station names
    """
    return sorted(stations_df['Station_Name'].unique())

def create_metro_graph(stations_df, connections_df):
    """
    Create a graph representation of the metro network
    """
    G = nx.Graph()
    
    # Add stations as nodes
    for _, row in stations_df.iterrows():
        G.add_node(
            row['Station_Name'], 
            id=row['Station_ID'],
            line=row['Line'],
            latitude=row['Latitude'],
            longitude=row['Longitude']
        )
    
    # Add connections as edges
    for _, row in connections_df.iterrows():
        station1_id = row['Station_1']
        station2_id = row['Station_2']
        line = row['Line']
        distance = row['Distance_KM']
        
        # Get station names from IDs
        station1_name = stations_df[stations_df['Station_ID'] == station1_id]['Station_Name'].values[0]
        station2_name = stations_df[stations_df['Station_ID'] == station2_id]['Station_Name'].values[0]
        
        # Add edge with attributes
        G.add_edge(
            station1_name, 
            station2_name, 
            line=line, 
            distance=distance
        )
    
    return G

def find_route(source, destination, stations_df, connections_df):
    """
    Find the shortest route between source and destination stations
    Returns route as list of station names and the lines to use
    """
    # Create graph
    G = create_metro_graph(stations_df, connections_df)
    
    # Check if both stations exist in the graph
    if source not in G.nodes or destination not in G.nodes:
        return None, None
    
    try:
        # Find shortest path
        path = nx.shortest_path(G, source, destination, weight='distance')
        
        # Determine metro lines to use
        lines_used = []
        current_line = None
        line_start = None
        
        for i in range(len(path) - 1):
            edge_data = G.get_edge_data(path[i], path[i+1])
            line = edge_data['line']
            
            if current_line is None:
                current_line = line
                line_start = path[i]
            elif line != current_line:
                # Line change detected
                lines_used.append((current_line, line_start, path[i]))
                current_line = line
                line_start = path[i]
        
        # Add the last line segment
        if current_line is not None:
            lines_used.append((current_line, line_start, path[-1]))
        
        return path, lines_used
    
    except nx.NetworkXNoPath:
        return None, None
