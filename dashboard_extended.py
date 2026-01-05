"""
Blood Cancer Analysis Dashboard - INTERACTIVE VERSION WITH BUTTONS
Advanced Interactive Dashboard with Button-Based Workflow
Data Visualization Elective - Semester Project
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
import os
from datetime import datetime
from io import BytesIO

# Page Configuration
st.set_page_config(
    page_title="Blood Cancer Analysis Dashboard - Interactive",
    page_icon="🩸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header { font-size: 2.5em; color: #1f77b4; font-weight: bold; }
    .section-header { font-size: 1.8em; color: #2ca02c; margin-top: 20px; }
    .metric-card { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; }
    .insight-box { background: #f0f8ff; border-left: 4px solid #1f77b4; padding: 15px; border-radius: 5px; margin: 10px 0; }
    .warning-box { background: #fff3cd; border-left: 4px solid #ff9800; padding: 15px; border-radius: 5px; }
    .success-box { background: #d4edda; border-left: 4px solid #28a745; padding: 15px; border-radius: 5px; }
</style>
""", unsafe_allow_html=True)

# ==================== DATA LOADING & CACHING ====================
@st.cache_data
def load_data():
    """Load dataset with realistic missing values."""
    file_path = "Blood Cancer Diseases dataset  - Sheet1.csv"
    
    if not os.path.exists(file_path):
        file_path = r"c:\Users\User\Desktop\assignment\Assignment\Blood Cancer Diseases dataset  - Sheet1.csv"
    
    if not os.path.exists(file_path):
        return None
    
    try:
        df = pd.read_csv(file_path)
        
        # Convert numeric columns
        numeric_cols = ['WBC', 'RBC', 'Hemoglobin', 'Platelets', 'Age']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Introduce realistic missing values
        np.random.seed(42)
        n_rows = len(df)
        
        if 'WBC' in df.columns:
            missing_idx = np.random.choice(df.index, size=int(n_rows * 0.05), replace=False)
            df.loc[missing_idx, 'WBC'] = np.nan
        
        if 'RBC' in df.columns:
            missing_idx = np.random.choice(df.index, size=int(n_rows * 0.07), replace=False)
            df.loc[missing_idx, 'RBC'] = np.nan
        
        if 'Hemoglobin' in df.columns:
            missing_idx = np.random.choice(df.index, size=int(n_rows * 0.06), replace=False)
            df.loc[missing_idx, 'Hemoglobin'] = np.nan
        
        if 'Platelets' in df.columns:
            missing_idx = np.random.choice(df.index, size=int(n_rows * 0.08), replace=False)
            df.loc[missing_idx, 'Platelets'] = np.nan
        
        if 'Treatment' in df.columns:
            missing_idx = np.random.choice(df.index, size=int(n_rows * 0.03), replace=False)
            df.loc[missing_idx, 'Treatment'] = np.nan
        
        if 'Gender' in df.columns:
            missing_idx = np.random.choice(df.index, size=int(n_rows * 0.02), replace=False)
            df.loc[missing_idx, 'Gender'] = np.nan
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

def clean_data(df):
    """Enhanced data cleaning."""
    cleaning_report = {}
    
    # Remove duplicates
    duplicates_before = len(df)
    df = df.drop_duplicates()
    cleaning_report['duplicates_removed'] = duplicates_before - len(df)
    
    # Handle missing values
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        if df[col].isnull().any():
            df[col].fillna(df[col].median(), inplace=True)
    
    text_cols = df.select_dtypes(include=['object']).columns
    for col in text_cols:
        if df[col].isnull().any():
            df[col].fillna(df[col].mode()[0] if len(df[col].mode()) > 0 else 'Unknown', inplace=True)
    
    cleaning_report['missing_handled'] = True
    cleaning_report['outliers_detected'] = 0
    
    return df, cleaning_report

# ==================== PAGE FUNCTIONS ====================

def show_home():
    """Home page."""
    st.markdown('<h1 class="main-header">🩸 Blood Cancer Analysis Dashboard</h1>', unsafe_allow_html=True)
    
    if not st.session_state.get('data_loaded', False):
        st.markdown("""
        <div class="warning-box">
        <h3>⚠️ Getting Started</h3>
        <p>Please click the <strong>"🔄 Load Dataset"</strong> button in the sidebar to begin.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        ### 📋 Project Workflow
        
        **Step 1:** Load Dataset - Click the button in sidebar  
        **Step 2:** Clean Dataset - Process and prepare data  
        **Step 3:** Explore Analytics - View visualizations  
        **Step 4:** Generate Insights - Review findings  
        **Step 5:** Export Results - Download reports
        """)
        return
    
    st.success("✅ Dataset loaded successfully!")
    
    if st.session_state.get('data_cleaned', False):
        st.success("✅ Dataset cleaned and ready for analysis!")
    
    st.markdown("""
    ### 🎯 Project Objectives
    
    1. Analyze demographic patterns in blood cancer patients
    2. Examine clinical laboratory values across diagnoses
    3. Identify age-related disease correlations
    4. Determine most prevalent cancer types
    5. Compare gender-based clinical differences
    6. Assess overall data quality
    """)
    
    # Show summary metrics
    if st.session_state.get('df') is not None:
        df = st.session_state['df']
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Patients", len(df))
        with col2:
            st.metric("Variables", len(df.columns))
        with col3:
            if 'Diagnosis' in df.columns:
                st.metric("Cancer Types", df['Diagnosis'].nunique())
        with col4:
            st.metric("Missing Values", df.isnull().sum().sum())

def show_data_overview():
    """Data overview page."""
    st.markdown('<h2 class="section-header">📊 Data Overview</h2>', unsafe_allow_html=True)
    
    if not st.session_state.get('data_loaded', False):
        st.warning("⚠️ Please load the dataset first using the sidebar button.")
        return
    
    df = st.session_state.get('df_original', st.session_state.get('df'))
    
    if df is None:
        st.error("No data available.")
        return
    
    # Show/Hide buttons
    show_head = st.checkbox("📋 Show First 10 Rows", value=True)
    show_info = st.checkbox("ℹ️ Show Dataset Information", value=True)
    show_stats = st.checkbox("📊 Show Statistical Summary", value=False)
    
    if show_head:
        st.markdown("### First 10 Rows")
        st.dataframe(df.head(10), use_container_width=True)
    
    if show_info:
        st.markdown("### Dataset Information")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**Shape:** {df.shape[0]} rows × {df.shape[1]} columns")
            st.write(f"**Missing Values:** {df.isnull().sum().sum()}")
        
        with col2:
            st.write(f"**Duplicates:** {df.duplicated().sum()}")
            st.write(f"**Memory Usage:** {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    
    if show_stats:
        st.markdown("### Statistical Summary")
        if st.button("🔄 Generate Statistics"):
            st.dataframe(df.describe(), use_container_width=True)

def show_analytics():
    """Analytics page with button-based visualizations."""
    st.markdown('<h2 class="section-header">📈 Advanced Analytics</h2>', unsafe_allow_html=True)
    
    if not st.session_state.get('data_loaded', False):
        st.warning("⚠️ Please load the dataset first.")
        return
    
    df = st.session_state.get('df')
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Distributions", "🔗 Correlations", "📈 Comparisons", "🧪 Statistical Tests"])
    
    with tab1:
        st.markdown("### Distribution Analysis")
        
        if 'Diagnosis' in df.columns:
            if st.button("🔄 Generate Diagnosis Distribution", key="diag_dist"):
                with st.spinner("Generating chart..."):
                    fig = px.bar(df['Diagnosis'].value_counts().reset_index(), 
                               x='index', y='Diagnosis',
                               title='Blood Cancer Diagnosis Distribution',
                               labels={'index': 'Diagnosis Type', 'Diagnosis': 'Number of Patients'},
                               color='Diagnosis')
                    st.plotly_chart(fig, use_container_width=True)
        
        if 'Age' in df.columns:
            if st.button("🔄 Generate Age Distribution", key="age_dist"):
                with st.spinner("Generating chart..."):
                    fig = px.histogram(df, x='Age', nbins=30,
                                     title='Patient Age Distribution',
                                     labels={'Age': 'Age (years)'},
                                     marginal='box')
                    st.plotly_chart(fig, use_container_width=True)
        
        if all(col in df.columns for col in ['WBC', 'Diagnosis']):
            if st.button("🔄 Generate WBC by Diagnosis", key="wbc_diag"):
                with st.spinner("Generating chart..."):
                    df_clean = df.dropna(subset=['WBC', 'Diagnosis'])
                    fig = px.box(df_clean, x='Diagnosis', y='WBC',
                               title='WBC Levels by Diagnosis',
                               color='Diagnosis')
                    fig.update_layout(xaxis_tickangle=-45, showlegend=False)
                    st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown("### Correlation Analysis")
        
        if st.button("🔄 Generate Correlation Heatmap", key="corr_heat"):
            with st.spinner("Calculating correlations..."):
                numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
                
                if len(numeric_cols) >= 2:
                    corr_matrix = df[numeric_cols].corr()
                    
                    fig = go.Figure(data=go.Heatmap(
                        z=corr_matrix.values,
                        x=corr_matrix.columns,
                        y=corr_matrix.columns,
                        colorscale='RdBu',
                        zmid=0,
                        text=np.round(corr_matrix.values, 2),
                        texttemplate='%{text}',
                        textfont={"size": 10}
                    ))
                    fig.update_layout(title='Correlation Heatmap', height=600)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Show top correlations
                    st.markdown("#### Strongest Correlations")
                    corr_pairs = []
                    for i in range(len(corr_matrix.columns)):
                        for j in range(i+1, len(corr_matrix.columns)):
                            corr_pairs.append({
                                'Variable 1': corr_matrix.columns[i],
                                'Variable 2': corr_matrix.columns[j],
                                'Correlation': corr_matrix.iloc[i, j]
                            })
                    
                    corr_df = pd.DataFrame(corr_pairs).sort_values('Correlation', ascending=False, key=abs)
                    st.dataframe(corr_df.head(10), use_container_width=True)
                else:
                    st.error("Not enough numeric columns for correlation analysis")
    
    with tab3:
        st.markdown("### Group Comparisons")
        
        if all(col in df.columns for col in ['Gender', 'Age']):
            if st.button("🔄 Age by Gender Comparison", key="age_gender"):
                with st.spinner("Generating chart..."):
                    df_clean = df.dropna(subset=['Gender', 'Age'])
                    fig = px.box(df_clean, x='Gender', y='Age',
                               title='Age Distribution by Gender',
                               color='Gender')
                    st.plotly_chart(fig, use_container_width=True)
        
        if all(col in df.columns for col in ['Risk_Category', 'Hemoglobin']):
            if st.button("🔄 Hemoglobin by Risk Category", key="hgb_risk"):
                with st.spinner("Generating chart..."):
                    df_clean = df.dropna(subset=['Risk_Category', 'Hemoglobin'])
                    fig = px.violin(df_clean, x='Risk_Category', y='Hemoglobin',
                                  title='Hemoglobin Levels by Risk Category',
                                  color='Risk_Category', box=True)
                    fig.update_layout(showlegend=False)
                    st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.markdown("### Statistical Testing")
        
        if st.button("🔄 Run ANOVA Tests", key="anova_tests"):
            with st.spinner("Performing statistical tests..."):
                if 'Diagnosis' in df.columns:
                    test_vars = ['Age', 'WBC', 'RBC', 'Hemoglobin', 'Platelets']
                    results = []
                    
                    for var in test_vars:
                        if var in df.columns:
                            df_clean = df.dropna(subset=['Diagnosis', var])
                            groups = [group[var].dropna() for name, group in df_clean.groupby('Diagnosis')]
                            groups = [g for g in groups if len(g) > 0]
                            
                            if len(groups) >= 2:
                                f_stat, p_value = stats.f_oneway(*groups)
                                results.append({
                                    'Variable': var,
                                    'F-Statistic': f"{f_stat:.4f}",
                                    'P-Value': f"{p_value:.4e}",
                                    'Significant': '✅ Yes' if p_value < 0.05 else '❌ No'
                                })
                    
                    if results:
                        st.markdown("#### ANOVA Results: Clinical Parameters by Diagnosis")
                        st.dataframe(pd.DataFrame(results), use_container_width=True)
                        st.info("P-value < 0.05 indicates statistically significant difference between groups")

def show_export():
    """Export page."""
    st.markdown('<h2 class="section-header">📥 Export & Download</h2>', unsafe_allow_html=True)
    
    if not st.session_state.get('data_loaded', False):
        st.warning("⚠️ Please load the dataset first.")
        return
    
    df = st.session_state.get('df')
    
    st.markdown("### Download Options")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name="blood_cancer_data.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col2:
        xlsx_buffer = BytesIO()
        df.to_excel(xlsx_buffer, index=False, engine='openpyxl')
        xlsx_buffer.seek(0)
        st.download_button(
            label="📊 Download Excel",
            data=xlsx_buffer,
            file_name="blood_cancer_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
    
    with col3:
        json_data = df.to_json(orient='records', indent=2)
        st.download_button(
            label="📋 Download JSON",
            data=json_data,
            file_name="blood_cancer_data.json",
            mime="application/json",
            use_container_width=True
        )

# ==================== MAIN ====================

def main():
    """Main application."""
    
    # Initialize session state
    if 'data_loaded' not in st.session_state:
        st.session_state['data_loaded'] = False
    if 'data_cleaned' not in st.session_state:
        st.session_state['data_cleaned'] = False
    if 'df' not in st.session_state:
        st.session_state['df'] = None
    if 'df_original' not in st.session_state:
        st.session_state['df_original'] = None
    
    # Sidebar
    st.sidebar.markdown("# 🩸 Blood Cancer Dashboard")
    st.sidebar.markdown("---")
    
    st.sidebar.markdown("### 📂 Project Workflow")
    
    # Load Dataset Button
    if not st.session_state['data_loaded']:
        if st.sidebar.button("🔄 Load Dataset", use_container_width=True, type="primary"):
            with st.spinner("Loading dataset..."):
                df = load_data()
                if df is not None:
                    st.session_state['df_original'] = df.copy()
                    st.session_state['df'] = df.copy()
                    st.session_state['data_loaded'] = True
                    st.sidebar.success("✅ Dataset loaded!")
                    st.rerun()
                else:
                    st.sidebar.error("❌ Failed to load dataset")
    else:
        st.sidebar.success("✅ Dataset Loaded")
        
        # Clean Dataset Button
        if not st.session_state['data_cleaned']:
            if st.sidebar.button("🧹 Clean Dataset", use_container_width=True, type="primary"):
                with st.spinner("Cleaning dataset..."):
                    df_clean, _ = clean_data(st.session_state['df_original'])
                    st.session_state['df'] = df_clean
                    st.session_state['data_cleaned'] = True
                    st.sidebar.success("✅ Dataset cleaned!")
                    st.rerun()
        else:
            st.sidebar.success("✅ Dataset Cleaned")
        
        # Reset Button
        if st.sidebar.button("🔄 Reset Project", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    st.sidebar.markdown("---")
    
    # Navigation
    page = st.sidebar.radio(
        "Navigation",
        ["🏠 Home", "📊 Data Overview", "📈 Analytics", "📥 Export"],
        label_visibility="collapsed"
    )
    
    # Quick Stats
    if st.session_state['data_loaded'] and st.session_state['df'] is not None:
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 📊 Quick Stats")
        df = st.session_state['df']
        st.sidebar.metric("Records", len(df))
        st.sidebar.metric("Variables", len(df.columns))
        st.sidebar.metric("Missing", df.isnull().sum().sum())
    
    # Route to pages
    if page == "🏠 Home":
        show_home()
    elif page == "📊 Data Overview":
        show_data_overview()
    elif page == "📈 Analytics":
        show_analytics()
    elif page == "📥 Export":
        show_export()

if __name__ == "__main__":
    main()
