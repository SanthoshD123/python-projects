import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import io
import base64

# Set page configuration
st.set_page_config(
    page_title="Data Visualization Dashboard",
    page_icon="📊",
    layout="wide"
)

# Define functions for data processing and visualization
def load_data(file):
    if file.name.endswith('.csv'):
        df = pd.read_csv(file)
    elif file.name.endswith(('.xls', '.xlsx')):
        df = pd.read_excel(file)
    else:
        st.error("Unsupported file format. Please upload a CSV or Excel file.")
        return None
    return df

def get_download_link(df, filename="dashboard_data.csv"):
    """Generate a download link for the dataframe"""
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">Download processed data as CSV</a>'
    return href

def create_visualization(df, viz_type, x_col, y_col, color_col=None, size_col=None, facet_col=None):
    """Create visualization based on selected parameters"""
    if viz_type == "Bar Chart":
        fig = px.bar(df, x=x_col, y=y_col, color=color_col, title=f"Bar Chart: {y_col} by {x_col}")
        
    elif viz_type == "Line Chart":
        fig = px.line(df, x=x_col, y=y_col, color=color_col, title=f"Line Chart: {y_col} over {x_col}")
        
    elif viz_type == "Scatter Plot":
        fig = px.scatter(df, x=x_col, y=y_col, color=color_col, size=size_col,
                        title=f"Scatter Plot: {y_col} vs {x_col}")
        
    elif viz_type == "Histogram":
        fig = px.histogram(df, x=x_col, color=color_col, title=f"Histogram of {x_col}")
        
    elif viz_type == "Box Plot":
        fig = px.box(df, x=x_col, y=y_col, color=color_col, title=f"Box Plot: {y_col} by {x_col}")
        
    elif viz_type == "Heatmap":
        if x_col and y_col:
            pivot_table = pd.pivot_table(df, values=size_col or df.columns[0], index=y_col, columns=x_col, aggfunc='mean')
            fig = px.imshow(pivot_table, title=f"Heatmap: {y_col} vs {x_col}")
        else:
            correlation_matrix = df.select_dtypes(include=[np.number]).corr()
            fig = px.imshow(correlation_matrix, title="Correlation Heatmap")
            
    elif viz_type == "Pie Chart":
        fig = px.pie(df, names=x_col, values=y_col, title=f"Pie Chart: {y_col} by {x_col}")
        
    elif viz_type == "Area Chart":
        fig = px.area(df, x=x_col, y=y_col, color=color_col, title=f"Area Chart: {y_col} over {x_col}")
        
    # Make the visualization responsive and add grid
    fig.update_layout(
        autosize=True,
        xaxis=dict(showgrid=True),
        yaxis=dict(showgrid=True),
        plot_bgcolor='rgba(240, 240, 240, 0.8)'
    )
    
    return fig

# Application UI
st.title("📊 Interactive Data Visualization Dashboard")
st.write("Upload your data and create interactive visualizations in seconds.")

# Sidebar for data upload and options
with st.sidebar:
    st.header("Data Input")
    uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx", "xls"])
    
    if uploaded_file is not None:
        df = load_data(uploaded_file)
        if df is not None:
            st.success(f"Successfully loaded data with {df.shape[0]} rows and {df.shape[1]} columns.")
            
            # Data processing options
            st.header("Data Processing")
            
            # Show sample of the data
            if st.checkbox("Show data sample"):
                sample_size = st.slider("Sample size", min_value=5, max_value=min(50, df.shape[0]), value=5)
                st.dataframe(df.head(sample_size))
            
            # Handle missing values
            if df.isna().any().any():
                st.warning("Your data contains missing values.")
                missing_handling = st.selectbox(
                    "How to handle missing values?",
                    ["Keep as is", "Drop rows with any missing", "Fill numeric with mean", "Fill with zeros", "Fill with custom value"]
                )
                
                if missing_handling == "Drop rows with any missing":
                    df = df.dropna()
                    st.info(f"Dropped rows with missing values. New shape: {df.shape}")
                elif missing_handling == "Fill numeric with mean":
                    for col in df.select_dtypes(include=[np.number]).columns:
                        df[col] = df[col].fillna(df[col].mean())
                    st.info("Filled numeric missing values with column means")
                elif missing_handling == "Fill with zeros":
                    df = df.fillna(0)
                    st.info("Filled missing values with zeros")
                elif missing_handling == "Fill with custom value":
                    fill_value = st.text_input("Custom fill value:", "0")
                    df = df.fillna(fill_value)
                    st.info(f"Filled missing values with: {fill_value}")
    else:
        # Use sample data if no file is uploaded
        st.info("No file uploaded. Using sample data for demonstration.")
        # Create sample data
        np.random.seed(42)
        dates = pd.date_range(start='2023-01-01', periods=100, freq='D')
        categories = ['A', 'B', 'C', 'D']
        
        sample_data = {
            'Date': dates,
            'Category': np.random.choice(categories, size=100),
            'Value': np.random.normal(100, 15, size=100),
            'Count': np.random.randint(1, 100, size=100),
            'Growth': np.random.uniform(-0.5, 0.5, size=100)
        }
        
        df = pd.DataFrame(sample_data)
        st.write("Sample data preview:")
        st.dataframe(df.head())

# Main content area
if 'df' in locals():
    # Visualization options
    st.header("Create Visualization")
    
    # Create columns for controls
    col1, col2 = st.columns(2)
    
    with col1:
        viz_type = st.selectbox(
            "Visualization Type",
            ["Bar Chart", "Line Chart", "Scatter Plot", "Histogram", 
             "Box Plot", "Heatmap", "Pie Chart", "Area Chart"]
        )
        
        # Determine which columns can be used for x, y based on data types
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        date_cols = df.select_dtypes(include=['datetime']).columns.tolist()
        all_cols = df.columns.tolist()
        
        # Default column selections based on visualization type
        if viz_type in ["Histogram"]:
            x_options = numeric_cols + categorical_cols
            y_options = [None] + numeric_cols
            default_y = None
        elif viz_type in ["Pie Chart"]:
            x_options = categorical_cols
            y_options = numeric_cols
            default_y = numeric_cols[0] if numeric_cols else None
        elif viz_type in ["Bar Chart", "Box Plot"]:
            x_options = categorical_cols + date_cols
            y_options = numeric_cols
            default_y = numeric_cols[0] if numeric_cols else None
        else:
            x_options = numeric_cols + date_cols
            y_options = numeric_cols
            default_y = numeric_cols[1] if len(numeric_cols) > 1 else numeric_cols[0] if numeric_cols else None
        
        # Avoid errors with empty lists
        x_options = x_options if x_options else all_cols
        y_options = y_options if y_options else all_cols
        
        # Column selections
        x_col = st.selectbox("X-axis", options=x_options, index=0 if x_options else None)
        
        if viz_type != "Histogram":
            y_col = st.selectbox("Y-axis", options=y_options, 
                               index=y_options.index(default_y) if default_y in y_options else 0 if y_options else None)
        else:
            y_col = None
    
    with col2:
        color_col = st.selectbox("Color by (optional)", options=[None] + categorical_cols)
        
        if viz_type == "Scatter Plot":
            size_col = st.selectbox("Size by (optional)", options=[None] + numeric_cols)
        else:
            size_col = None
            
        facet_col = st.selectbox("Facet by (split into subplots)", options=[None] + categorical_cols)
    
    # Create the visualization
    try:
        if viz_type == "Heatmap" and x_col is None:
            st.warning("Please select columns for visualization")
        else:
            fig = create_visualization(df, viz_type, x_col, y_col, color_col, size_col, facet_col)
            st.plotly_chart(fig, use_container_width=True)
            
            # Add download options for the chart
            st.download_button(
                label="Download Chart as PNG",
                data=io.BytesIO(),
                file_name=f"{viz_type.lower().replace(' ', '_')}.png",
                mime="image/png",
                help="This would download the chart as PNG in a real implementation"
            )
            
            # Download link for processed data
            st.markdown(get_download_link(df), unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error creating visualization: {str(e)}")
        st.info("Try selecting different columns or visualization type")

# Add dashboard info and help
with st.expander("About this Dashboard"):
    st.markdown("""
    ## How to use this dashboard
    
    1. **Upload Data**: Use the sidebar to upload your CSV or Excel file
    2. **Process Data**: Handle missing values and explore your dataset
    3. **Create Visualizations**: Select chart type and configure axes
    4. **Export Results**: Download visualizations or processed data
    
    ## Features
    
    - Support for multiple chart types
    - Interactive plots (hover, zoom, pan)
    - Basic data processing capabilities
    - Export options for charts and data
    
    ## Tips
    
    - For best results, ensure your data is clean and properly formatted
    - Try different visualization types to find the best representation
    - Use color and size options to add more dimensions to your charts
    """)

# Footer
st.markdown("---")
st.markdown("📊 Data Visualization Dashboard | Created with Streamlit and Plotly")
