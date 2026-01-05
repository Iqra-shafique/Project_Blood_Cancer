"""
Blood Cancer Analysis Dashboard - SUPER INTERACTIVE VERSION
Advanced Dashboard with Multiple Visualization Types
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
    page_title="Blood Cancer Analysis Dashboard",
    page_icon="🩸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header { font-size: 2.5em; color: #1f77b4; font-weight: bold; text-align: center; }
    .section-header { font-size: 1.8em; color: #2ca02c; margin-top: 20px; }
    .metric-card { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; text-align: center; }
    .insight-box { background: #f0f8ff; border-left: 4px solid #1f77b4; padding: 15px; border-radius: 5px; margin: 10px 0; }
    .warning-box { background: #fff3cd; border-left: 4px solid #ff9800; padding: 15px; border-radius: 5px; }
    .success-box { background: #d4edda; border-left: 4px solid #28a745; padding: 15px; border-radius: 5px; }
    .stButton>button { width: 100%; }
</style>
""", unsafe_allow_html=True)

# ==================== DATA LOADING ====================
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
        
        # Map actual column names to simplified names for consistent code usage
        column_mapping = {
            'Age': 'Age',  # Already correct
            'Gender': 'Gender',  # Already correct
            'Total WBC count(/cumm)': 'WBC',
            'Cancer_Type(AML, ALL, CLL)': 'Diagnosis',
            'Treatment_Type(Chemotherapy, Radiation)': 'Treatment',
            'Platelet Count( (/cumm)': 'Platelets',
            'Treatment_Outcome': 'Treatment_Outcome',
            'Diagnosis_Result': 'Diagnosis_Result',
            'Genetic_Data(BCR-ABL, FLT3)': 'Genetic_Data',
            'Side_Effects': 'Side_Effects'
        }
        
        # Only rename columns that exist
        rename_dict = {k: v for k, v in column_mapping.items() if k in df.columns}
        df = df.rename(columns=rename_dict)
        
        # Add missing columns if needed (for code compatibility)
        if 'RBC' not in df.columns:
            df['RBC'] = np.nan
        if 'Hemoglobin' not in df.columns:
            df['Hemoglobin'] = np.nan
        
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
    df = df.copy()
    cleaning_report = {}
    
    # Remove duplicates
    duplicates_before = len(df)
    df = df.drop_duplicates()
    cleaning_report['duplicates_removed'] = duplicates_before - len(df)
    
    # Handle missing values
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        if df[col].isnull().any():
            df[col] = df[col].fillna(df[col].median())
    
    text_cols = df.select_dtypes(include=['object']).columns
    for col in text_cols:
        if df[col].isnull().any():
            fill_value = df[col].mode()[0] if len(df[col].mode()) > 0 else 'Unknown'
            df[col] = df[col].fillna(fill_value)
    
    cleaning_report['missing_handled'] = True
    
    return df, cleaning_report

# ==================== PAGE FUNCTIONS ====================

def show_home():
    """Home page."""
    st.markdown('<h1 class="main-header">🩸 Blood Cancer Analysis Dashboard</h1>', unsafe_allow_html=True)
    
    if not st.session_state.get('data_loaded', False):
        st.markdown("""
        <div class="warning-box">
        <h3>⚠️ Getting Started</h3>
        <p>Click <strong>"🔄 Load Dataset"</strong> in the sidebar to begin your analysis journey!</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        ### 🎯 Project Features
        
        **📊 Comprehensive Visualizations:**
        - Interactive charts and graphs
        - 3D scatter plots
        - Animated visualizations
        - Sunburst and treemap charts
        - Advanced statistical plots
        
        **🔬 Statistical Analysis:**
        - ANOVA testing
        - Correlation analysis
        - Distribution analysis
        - Group comparisons
        
        **📈 Real-time Insights:**
        - Dynamic data loading
        - Interactive filtering
        - Button-based workflow
        - Export capabilities
        """)
        return
    
    st.success("✅ Dataset loaded and ready for analysis!")
    
    if st.session_state.get('data_cleaned', False):
        st.success("✅ Data cleaning completed successfully!")
    
    # Dashboard metrics
    if st.session_state.get('df') is not None:
        df = st.session_state['df']
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("📊 Total Patients", f"{len(df):,}")
        with col2:
            st.metric("📋 Variables", len(df.columns))
        with col3:
            if 'Diagnosis' in df.columns:
                st.metric("🩺 Cancer Types", df['Diagnosis'].nunique())
        with col4:
            if 'Age' in df.columns:
                st.metric("👥 Avg Age", f"{df['Age'].mean():.1f} yrs")
        with col5:
            st.metric("✨ Data Quality", f"{100 - (df.isnull().sum().sum() / (len(df) * len(df.columns)) * 100):.1f}%")

def show_data_overview():
    """Data overview page."""
    st.markdown('<h2 class="section-header">📊 Data Overview & Exploration</h2>', unsafe_allow_html=True)
    
    if not st.session_state.get('data_loaded', False):
        st.warning("⚠️ Please load the dataset first using the sidebar button.")
        return
    
    df = st.session_state.get('df')
    
    # Dataset preview with toggle
    if st.checkbox("📋 Show Dataset Preview", value=True):
        st.markdown("### First 15 Rows")
        st.dataframe(df.head(15), width='stretch', height=400)
    
    # Column information
    if st.checkbox("ℹ️ Show Column Information"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Numeric Columns")
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            for col in numeric_cols:
                st.write(f"• {col}: {df[col].dtype}")
        
        with col2:
            st.markdown("### Categorical Columns")
            cat_cols = df.select_dtypes(include=['object']).columns.tolist()
            for col in cat_cols:
                st.write(f"• {col}: {df[col].nunique()} unique values")
    
    # Interactive statistics
    if st.checkbox("📊 Show Statistical Summary"):
        if st.button("🔄 Generate Statistics", key="gen_stats"):
            st.dataframe(df.describe(), width='stretch')

def show_visualizations():
    """Advanced visualizations page."""
    st.markdown('<h2 class="section-header">📈 Advanced Data Visualizations</h2>', unsafe_allow_html=True)
    
    if not st.session_state.get('data_loaded', False):
        st.warning("⚠️ Please load the dataset first.")
        return
    
    df = st.session_state.get('df')
    
    # Visualization categories
    viz_type = st.selectbox("Select Visualization Category", 
                           ["📊 Distribution Plots", "🔗 Relationship Analysis", 
                            "📉 Comparison Charts", "🎯 Advanced 3D & Animated"])
    
    if viz_type == "📊 Distribution Plots":
        show_distribution_plots(df)
    elif viz_type == "🔗 Relationship Analysis":
        show_relationship_analysis(df)
    elif viz_type == "📉 Comparison Charts":
        show_comparison_charts(df)
    elif viz_type == "🎯 Advanced 3D & Animated":
        show_advanced_plots(df)

def show_distribution_plots(df):
    """Distribution visualization section."""
    st.markdown("### 📊 Distribution Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🎨 Age Distribution Histogram", key="age_hist"):
            if 'Age' in df.columns:
                fig = px.histogram(df, x='Age', nbins=40,
                                 title='Patient Age Distribution',
                                 color_discrete_sequence=['#636EFA'],
                                 marginal='box')
                fig.update_layout(showlegend=False, height=500)
                st.plotly_chart(fig, width='stretch')
    
    with col2:
        if st.button("📊 Diagnosis Pie Chart", key="diag_pie"):
            if 'Diagnosis' in df.columns:
                fig = px.pie(df, names='Diagnosis',
                           title='Cancer Type Distribution',
                           hole=0.4,
                           color_discrete_sequence=px.colors.qualitative.Set3)
                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig, width='stretch')
    
    col3, col4 = st.columns(2)
    
    with col3:
        if st.button("🎯 WBC Distribution", key="wbc_dist"):
            if 'WBC' in df.columns:
                fig = px.violin(df, y='WBC',
                              title='WBC Count Distribution',
                              box=True,
                              color_discrete_sequence=['#EF553B'])
                st.plotly_chart(fig, width='stretch')
    
    with col4:
        if st.button("📉 Hemoglobin KDE Plot", key="hgb_kde"):
            if 'Hemoglobin' in df.columns:
                fig = px.histogram(df, x='Hemoglobin',
                                 marginal='violin',
                                 title='Hemoglobin Distribution with KDE',
                                 color_discrete_sequence=['#00CC96'])
                st.plotly_chart(fig, width='stretch')

def show_relationship_analysis(df):
    """Relationship analysis section."""
    st.markdown("### 🔗 Correlation & Relationships")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔥 Correlation Heatmap", key="corr_heat"):
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
                fig.update_layout(title='Correlation Matrix', height=600)
                st.plotly_chart(fig, width='stretch')
    
    with col2:
        if st.button("📈 Age vs WBC Scatter", key="age_wbc_scatter"):
            if all(col in df.columns for col in ['Age', 'WBC', 'Diagnosis']):
                df_clean = df.dropna(subset=['Age', 'WBC', 'Diagnosis'])
                fig = px.scatter(df_clean, x='Age', y='WBC',
                               color='Diagnosis',
                               size='Hemoglobin' if 'Hemoglobin' in df.columns else None,
                               title='Age vs WBC (sized by Hemoglobin)',
                               trendline='ols',
                               hover_data=['Diagnosis'])
                st.plotly_chart(fig, width='stretch')
    
    # Pairplot section
    if st.button("🎨 Generate Pairplot (Numeric Variables)", key="pairplot"):
        with st.spinner("Creating pairplot..."):
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()[:4]  # Limit to 4 for performance
            if len(numeric_cols) >= 2:
                fig = px.scatter_matrix(df[numeric_cols].dropna(),
                                      title='Pairwise Relationships',
                                      height=800)
                st.plotly_chart(fig, width='stretch')

def show_comparison_charts(df):
    """Comparison charts section."""
    st.markdown("### 📉 Group Comparisons")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📊 WBC by Diagnosis (Box)", key="wbc_box"):
            if all(col in df.columns for col in ['Diagnosis', 'WBC']):
                df_clean = df.dropna(subset=['Diagnosis', 'WBC'])
                fig = px.box(df_clean, x='Diagnosis', y='WBC',
                           title='WBC Levels Across Cancer Types',
                           color='Diagnosis',
                           points='outliers')
                fig.update_layout(xaxis_tickangle=-45, showlegend=False)
                st.plotly_chart(fig, width='stretch')
    
    with col2:
        if st.button("🎻 Hemoglobin by Gender", key="hgb_gender"):
            if all(col in df.columns for col in ['Gender', 'Hemoglobin']):
                df_clean = df.dropna(subset=['Gender', 'Hemoglobin'])
                fig = px.violin(df_clean, x='Gender', y='Hemoglobin',
                              title='Hemoglobin Comparison by Gender',
                              color='Gender',
                              box=True,
                              points='all')
                st.plotly_chart(fig, width='stretch')
    
    col3, col4 = st.columns(2)
    
    with col3:
        if st.button("📊 Treatment Outcome Sunburst", key="outcome_sun"):
            if 'Treatment_Outcome' in df.columns and 'Diagnosis' in df.columns:
                df_clean = df.dropna(subset=['Treatment_Outcome', 'Diagnosis'])
                fig = px.sunburst(df_clean, path=['Treatment_Outcome', 'Diagnosis'],
                                title='Treatment Outcomes by Diagnosis')
                st.plotly_chart(fig, width='stretch')
    
    with col4:
        if st.button("🎯 Risk Category Treemap", key="risk_tree"):
            if 'Risk_Category' in df.columns and 'Diagnosis' in df.columns:
                df_clean = df.dropna(subset=['Risk_Category', 'Diagnosis'])
                fig = px.treemap(df_clean, path=['Risk_Category', 'Diagnosis'],
                               title='Patient Distribution by Risk & Diagnosis')
                st.plotly_chart(fig, width='stretch')

def show_advanced_plots(df):
    """Advanced 3D and animated plots."""
    st.markdown("### 🎯 Advanced 3D & Animated Visualizations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🌐 3D Scatter Plot", key="3d_scatter"):
            if all(col in df.columns for col in ['Age', 'WBC', 'Hemoglobin', 'Diagnosis']):
                df_clean = df.dropna(subset=['Age', 'WBC', 'Hemoglobin', 'Diagnosis'])
                fig = px.scatter_3d(df_clean, x='Age', y='WBC', z='Hemoglobin',
                                  color='Diagnosis',
                                  title='3D View: Age, WBC & Hemoglobin',
                                  height=700)
                st.plotly_chart(fig, width='stretch')
    
    with col2:
        if st.button("📊 Animated Bubble Chart", key="bubble_anim"):
            if all(col in df.columns for col in ['Age', 'WBC', 'Diagnosis']):
                df_clean = df.dropna(subset=['Age', 'WBC', 'Diagnosis'])
                if 'Platelets' in df.columns:
                    df_clean = df_clean.dropna(subset=['Platelets'])
                    fig = px.scatter(df_clean, x='Age', y='WBC',
                                   size='Platelets',
                                   color='Diagnosis',
                                   title='Bubble Chart: Age vs WBC (bubble = Platelets)',
                                   size_max=50,
                                   height=600)
                    st.plotly_chart(fig, width='stretch')
    
    # Parallel coordinates
    if st.button("🌈 Parallel Coordinates Plot", key="parallel"):
        if 'Diagnosis' in df.columns:
            numeric_cols = ['Age', 'WBC', 'RBC', 'Hemoglobin', 'Platelets']
            available_cols = [col for col in numeric_cols if col in df.columns]
            
            if len(available_cols) >= 3:
                df_plot = df[available_cols + ['Diagnosis']].dropna()
                if len(df_plot) > 500:
                    df_plot = df_plot.sample(500)
                
                fig = px.parallel_coordinates(df_plot,
                                            dimensions=available_cols,
                                            color='Age',
                                            title='Parallel Coordinates: Clinical Parameters',
                                            color_continuous_scale=px.colors.sequential.Viridis)
                st.plotly_chart(fig, width='stretch')

def show_statistical_analysis():
    """Statistical analysis page."""
    st.markdown('<h2 class="section-header">🧪 Statistical Analysis & Testing</h2>', unsafe_allow_html=True)
    
    if not st.session_state.get('data_loaded', False):
        st.warning("⚠️ Please load the dataset first.")
        return
    
    df = st.session_state.get('df')
    
    tab1, tab2, tab3 = st.tabs(["📊 ANOVA Tests", "📈 T-Tests", "📉 Chi-Square Tests"])
    
    with tab1:
        st.markdown("### Analysis of Variance (ANOVA)")
        st.info("Tests if there are significant differences in means across different groups")
        
        if st.button("🔬 Run ANOVA Tests", key="run_anova", width='stretch', type="primary"):
            with st.spinner("Performing ANOVA tests..."):
                if 'Diagnosis' in df.columns:
                    test_vars = ['Age', 'WBC', 'RBC', 'Hemoglobin', 'Platelets']
                    results = []
                    
                    for var in test_vars:
                        if var in df.columns:
                            df_clean = df.dropna(subset=['Diagnosis', var])
                            if len(df_clean) > 0:
                                groups = [group[var].dropna().values for name, group in df_clean.groupby('Diagnosis') if len(group[var].dropna()) > 0]
                                
                                if len(groups) >= 2 and all(len(g) > 0 for g in groups):
                                    try:
                                        f_stat, p_value = stats.f_oneway(*groups)
                                        results.append({
                                            'Variable': var,
                                            'F-Statistic': f"{f_stat:.4f}",
                                            'P-Value': f"{p_value:.6f}",
                                            'Significant (α=0.05)': '✅ Yes' if p_value < 0.05 else '❌ No',
                                            'Effect': 'Strong' if p_value < 0.01 else 'Moderate' if p_value < 0.05 else 'None'
                                        })
                                    except Exception as e:
                                        st.error(f"Error testing {var}: {str(e)}")
                    
                    if results:
                        st.success(f"✅ Completed {len(results)} ANOVA tests")
                        results_df = pd.DataFrame(results)
                        st.dataframe(results_df, width='stretch')
                        
                        st.markdown("""
                        **Interpretation:**
                        - **P-value < 0.05**: Significant difference between groups
                        - **P-value ≥ 0.05**: No significant difference
                        - **F-statistic**: Higher values indicate greater between-group variance
                        """)
                    else:
                        st.error("No valid tests could be performed")
    
    with tab2:
        st.markdown("### Independent T-Tests")
        st.info("Compares means between two groups")
        
        if st.button("🔬 Run Gender Comparison T-Tests", key="run_ttest", width='stretch', type="primary"):
            with st.spinner("Performing t-tests..."):
                if 'Gender' in df.columns:
                    df_clean = df.dropna(subset=['Gender'])
                    genders = df_clean['Gender'].unique()
                    
                    if len(genders) >= 2:
                        gender1, gender2 = genders[0], genders[1]
                        test_vars = ['Age', 'WBC', 'RBC', 'Hemoglobin', 'Platelets']
                        results = []
                        
                        for var in test_vars:
                            if var in df.columns:
                                group1 = df_clean[df_clean['Gender'] == gender1][var].dropna()
                                group2 = df_clean[df_clean['Gender'] == gender2][var].dropna()
                                
                                if len(group1) > 1 and len(group2) > 1:
                                    t_stat, p_value = stats.ttest_ind(group1, group2)
                                    results.append({
                                        'Variable': var,
                                        f'{gender1} Mean': f"{group1.mean():.2f}",
                                        f'{gender2} Mean': f"{group2.mean():.2f}",
                                        'T-Statistic': f"{t_stat:.4f}",
                                        'P-Value': f"{p_value:.6f}",
                                        'Significant': '✅ Yes' if p_value < 0.05 else '❌ No'
                                    })
                        
                        if results:
                            st.success(f"✅ Completed {len(results)} t-tests")
                            st.dataframe(pd.DataFrame(results), width='stretch')
    
    with tab3:
        st.markdown("### Chi-Square Tests")
        st.info("Tests independence between categorical variables")
        
        if st.button("🔬 Run Chi-Square Test", key="run_chi", width='stretch', type="primary"):
            with st.spinner("Performing chi-square test..."):
                if all(col in df.columns for col in ['Gender', 'Risk_Category']):
                    df_clean = df.dropna(subset=['Gender', 'Risk_Category'])
                    contingency_table = pd.crosstab(df_clean['Gender'], df_clean['Risk_Category'])
                    
                    chi2, p_value, dof, expected = stats.chi2_contingency(contingency_table)
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Chi-Square Statistic", f"{chi2:.4f}")
                    with col2:
                        st.metric("P-Value", f"{p_value:.6f}")
                    with col3:
                        st.metric("Degrees of Freedom", dof)
                    
                    st.markdown("#### Contingency Table")
                    st.dataframe(contingency_table, width='stretch')

def show_export():
    """Export page."""
    st.markdown('<h2 class="section-header">📥 Export & Download</h2>', unsafe_allow_html=True)
    
    if not st.session_state.get('data_loaded', False):
        st.warning("⚠️ Please load the dataset first.")
        return
    
    df = st.session_state.get('df')
    
    st.markdown("### 📦 Download Data in Multiple Formats")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name="blood_cancer_data.csv",
            mime="text/csv",
            width='stretch'
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
            width='stretch'
        )
    
    with col3:
        json_data = df.to_json(orient='records', indent=2)
        st.download_button(
            label="📋 Download JSON",
            data=json_data,
            file_name="blood_cancer_data.json",
            mime="application/json",
            width='stretch'
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
    
    st.sidebar.markdown("### 📂 Workflow")
    
    # Load Dataset Button
    if not st.session_state['data_loaded']:
        if st.sidebar.button("🔄 Load Dataset", width='stretch', type="primary"):
            with st.spinner("Loading dataset..."):
                df = load_data()
                if df is not None:
                    st.session_state['df_original'] = df.copy()
                    st.session_state['df'] = df.copy()
                    st.session_state['data_loaded'] = True
                    st.sidebar.success("✅ Loaded!")
                    st.rerun()
    else:
        st.sidebar.success("✅ Dataset Loaded")
        
        # Clean Dataset Button
        if not st.session_state['data_cleaned']:
            if st.sidebar.button("🧹 Clean Dataset", width='stretch', type="primary"):
                with st.spinner("Cleaning..."):
                    df_clean, _ = clean_data(st.session_state['df_original'])
                    st.session_state['df'] = df_clean
                    st.session_state['data_cleaned'] = True
                    st.sidebar.success("✅ Cleaned!")
                    st.rerun()
        else:
            st.sidebar.success("✅ Data Cleaned")
        
        # Reset Button
        if st.sidebar.button("🔄 Reset", width='stretch'):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    st.sidebar.markdown("---")
    
    # Navigation
    page = st.sidebar.radio(
        "Navigation",
        ["🏠 Home", "📊 Data Overview", "📈 Visualizations", "🧪 Statistical Analysis", "📥 Export"],
        label_visibility="collapsed"
    )
    
    # Quick Stats
    if st.session_state['data_loaded'] and st.session_state['df'] is not None:
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 📊 Quick Stats")
        df = st.session_state['df']
        st.sidebar.metric("Records", f"{len(df):,}")
        st.sidebar.metric("Variables", len(df.columns))
        st.sidebar.metric("Missing", df.isnull().sum().sum())
    
    # Route to pages
    if page == "🏠 Home":
        show_home()
    elif page == "📊 Data Overview":
        show_data_overview()
    elif page == "📈 Visualizations":
        show_visualizations()
    elif page == "🧪 Statistical Analysis":
        show_statistical_analysis()
    elif page == "📥 Export":
        show_export()

if __name__ == "__main__":
    main()
