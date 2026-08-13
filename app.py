"""
app.py
Campus Placement Analytics - Live Streamlit Web Dashboard
Deployable on Hugging Face Spaces & Streamlit Cloud
"""

import sqlite3
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Campus Placement Data Analytics",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium UI
st.markdown("""
    <style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #475569;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: bold;
        color: #1E40AF;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #64748B;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv("placement_clean.csv")
    return df

@st.cache_resource
def get_db_connection():
    conn = sqlite3.connect("placement.db", check_same_thread=False)
    return conn

df_raw = load_data()
conn = get_db_connection()

# Sidebar Filters
st.sidebar.image("https://img.icons8.com/illustrations/100/graduation-cap.png", width=70)
st.sidebar.title("🔍 Data Filters")

spec_options = ["All"] + list(df_raw['specialisation'].unique())
selected_spec = st.sidebar.selectbox("MBA Specialisation", spec_options)

workex_options = ["All"] + list(df_raw['workex'].unique())
selected_workex = st.sidebar.selectbox("Work Experience", workex_options)

degree_options = ["All"] + list(df_raw['degree_t'].unique())
selected_degree = st.sidebar.selectbox("Degree Field", degree_options)

gender_options = ["All"] + list(df_raw['gender'].unique())
selected_gender = st.sidebar.selectbox("Gender", gender_options)

# Filter Dataframe based on selections
filtered_df = df_raw.copy()
if selected_spec != "All":
    filtered_df = filtered_df[filtered_df['specialisation'] == selected_spec]
if selected_workex != "All":
    filtered_df = filtered_df[filtered_df['workex'] == selected_workex]
if selected_degree != "All":
    filtered_df = filtered_df[filtered_df['degree_t'] == selected_degree]
if selected_gender != "All":
    filtered_df = filtered_df[filtered_df['gender'] == selected_gender]

# Header Section
st.markdown('<div class="main-header">🎓 Campus Placement Analytics & Insights</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Interactive Portfolio Dashboard examining 215 MBA Recruitment Records with SQLite & Visual Analytics</div>', unsafe_allow_html=True)

# KPI Summary Banner
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

total_students = len(filtered_df)
placed_students = (filtered_df['status'] == 'Placed').sum()
placement_rate = (placed_students / total_students * 100) if total_students > 0 else 0
placed_df = filtered_df[filtered_df['status'] == 'Placed']
avg_salary = placed_df['salary'].mean() if len(placed_df) > 0 else 0
max_salary = placed_df['salary'].max() if len(placed_df) > 0 else 0

with kpi1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Total Candidates</div>
        <div class="metric-value">{total_students}</div>
    </div>
    """, unsafe_allow_html=True)

with kpi2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Placement Rate</div>
        <div class="metric-value">{placement_rate:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)

with kpi3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Average Salary Offer</div>
        <div class="metric-value">₹{avg_salary/100000:.2f}L</div>
    </div>
    """, unsafe_allow_html=True)

with kpi4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Highest Package</div>
        <div class="metric-value">₹{max_salary/100000:.2f}L</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Navigation Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Visual Analytics", 
    "💻 Live SQL Console", 
    "🔍 Data Explorer", 
    "💡 Executive Insights"
])

# -----------------------------------------------------------------------------
# TAB 1: VISUAL ANALYTICS
# -----------------------------------------------------------------------------
with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Placement Rate by Specialisation")
        spec_summary = filtered_df.groupby('specialisation')['Placed_Flag'].mean().reset_index()
        spec_summary['Placement_Rate'] = spec_summary['Placed_Flag'] * 100
        fig_spec = px.bar(
            spec_summary, x='specialisation', y='Placement_Rate',
            text=spec_summary['Placement_Rate'].apply(lambda x: f"{x:.1f}%"),
            color='specialisation',
            color_discrete_sequence=['#1E40AF', '#3B82F6'],
            labels={'Placement_Rate': 'Placement Rate (%)', 'specialisation': 'Specialisation'}
        )
        fig_spec.update_layout(yaxis_range=[0, 100], showlegend=False)
        st.plotly_chart(fig_spec, use_container_width=True)

    with col2:
        st.subheader("Placement Rate by Work Experience")
        workex_summary = filtered_df.groupby('workex')['Placed_Flag'].mean().reset_index()
        workex_summary['Placement_Rate'] = workex_summary['Placed_Flag'] * 100
        fig_workex = px.bar(
            workex_summary, x='workex', y='Placement_Rate',
            text=workex_summary['Placement_Rate'].apply(lambda x: f"{x:.1f}%"),
            color='workex',
            color_discrete_sequence=['#EF4444', '#10B981'],
            labels={'Placement_Rate': 'Placement Rate (%)', 'workex': 'Work Experience'}
        )
        fig_workex.update_layout(yaxis_range=[0, 100], showlegend=False)
        st.plotly_chart(fig_workex, use_container_width=True)

    st.markdown("---")
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.subheader("Key Academic Score Comparison (Placed vs Not Placed)")
        score_df = filtered_df.groupby('status')[['ssc_p', 'hsc_p', 'degree_p', 'mba_p']].mean().reset_index()
        melted = pd.melt(score_df, id_vars=['status'], value_vars=['ssc_p', 'hsc_p', 'degree_p', 'mba_p'],
                         var_name='Stage', value_name='Average_Percentage')
        stage_map = {'ssc_p': '10th (SSC)', 'hsc_p': '12th (HSC)', 'degree_p': 'Degree', 'mba_p': 'MBA'}
        melted['Stage_Label'] = melted['Stage'].map(stage_map)
        
        fig_academic = px.bar(
            melted, x='Stage_Label', y='Average_Percentage', color='status',
            barmode='group',
            color_discrete_map={'Placed': '#10B981', 'Not Placed': '#EF4444'},
            text=melted['Average_Percentage'].apply(lambda x: f"{x:.1f}%"),
            labels={'Average_Percentage': 'Average Score (%)', 'Stage_Label': 'Academic Stage', 'status': 'Status'}
        )
        fig_academic.update_layout(yaxis_range=[0, 100])
        st.plotly_chart(fig_academic, use_container_width=True)
        
    with col4:
        st.subheader("Salary Offer Distribution (Placed Candidates)")
        if len(placed_df) > 0:
            fig_sal = px.histogram(
                placed_df, x='salary', nbins=15,
                color_discrete_sequence=['#3B82F6'],
                labels={'salary': 'Salary Offer (INR)'}
            )
            fig_sal.add_vline(x=avg_salary, line_dash="dash", line_color="#EF4444", annotation_text=f"Mean: ₹{avg_salary:,.0f}")
            st.plotly_chart(fig_sal, use_container_width=True)
        else:
            st.info("No placed candidates match the selected filters.")

    st.markdown("---")
    st.subheader("Academic Scores Correlation Matrix")
    corr_cols = ['ssc_p', 'hsc_p', 'degree_p', 'etest_p', 'mba_p', 'Placed_Flag']
    corr_matrix = filtered_df[corr_cols].corr()
    labels = ['10th %', '12th %', 'Degree %', 'E-Test %', 'MBA %', 'Placed Flag']
    
    fig_corr = px.imshow(
        corr_matrix,
        x=labels, y=labels,
        color_continuous_scale='Blues',
        text_auto='.2f',
        title="Pearson Correlation Heatmap"
    )
    st.plotly_chart(fig_corr, use_container_width=True)

# -----------------------------------------------------------------------------
# TAB 2: LIVE SQL CONSOLE
# -----------------------------------------------------------------------------
with tab2:
    st.subheader("💻 Interactive SQL Query Engine (`placement.db`)")
    st.markdown("Run real analytical SQL queries live against the SQLite database instance.")
    
    preset_queries = {
        "1. Overall Placement Summary": """
SELECT 
    COUNT(*) AS total_students,
    SUM(Placed_Flag) AS total_placed,
    COUNT(*) - SUM(Placed_Flag) AS total_unplaced,
    ROUND(AVG(Placed_Flag) * 100, 2) AS placement_rate_pct
FROM students;""",
        "2. Placement Rate by Specialisation": """
SELECT 
    specialisation,
    COUNT(*) AS total_students,
    SUM(Placed_Flag) AS placed_students,
    ROUND(AVG(Placed_Flag) * 100, 2) AS placement_rate_pct
FROM students
GROUP BY specialisation
ORDER BY placement_rate_pct DESC;""",
        "3. Window Function - MBA Rank within Specialisation": """
SELECT 
    student_id,
    gender,
    specialisation,
    mba_p,
    status,
    salary,
    RANK() OVER (PARTITION BY specialisation ORDER BY mba_p DESC) AS rank_within_spec
FROM students
ORDER BY specialisation, rank_within_spec
LIMIT 15;""",
        "4. CTE - Academic Stage Score Averages": """
WITH AcademicAverages AS (
    SELECT 
        status,
        COUNT(*) AS student_count,
        ROUND(AVG(ssc_p), 2) AS avg_ssc_p,
        ROUND(AVG(hsc_p), 2) AS avg_hsc_p,
        ROUND(AVG(degree_p), 2) AS avg_degree_p,
        ROUND(AVG(mba_p), 2) AS avg_mba_p
    FROM students
    GROUP BY status
)
SELECT * FROM AcademicAverages;""",
        "5. Placement Rate by Work Experience": """
SELECT 
    workex,
    COUNT(*) AS total_students,
    SUM(Placed_Flag) AS placed_students,
    ROUND(AVG(Placed_Flag) * 100, 2) AS placement_rate_pct
FROM students
GROUP BY workex;""",
        "6. Top 10 Highest Salary Offers": """
SELECT 
    student_id, gender, specialisation, workex, degree_t, salary
FROM students
WHERE status = 'Placed'
ORDER BY salary DESC
LIMIT 10;"""
    }
    
    query_choice = st.selectbox("Select Pre-built SQL Query:", list(preset_queries.keys()))
    user_sql = st.text_area("SQL Editor", value=preset_queries[query_choice], height=180)
    
    if st.button("▶ Run SQL Query", type="primary"):
        try:
            result_df = pd.read_sql_query(user_sql, conn)
            st.success(f"Query executed successfully! ({len(result_df)} rows returned)")
            st.dataframe(result_df, use_container_width=True)
        except Exception as e:
            st.error(f"SQL Execution Error: {e}")

# -----------------------------------------------------------------------------
# TAB 3: DATA EXPLORER
# -----------------------------------------------------------------------------
with tab3:
    st.subheader("📋 Candidate Dataset Explorer")
    st.markdown(f"Displaying **{len(filtered_df)}** matching student records.")
    
    search_term = st.text_input("Search student records (by degree field, stream, etc.):", "")
    display_df = filtered_df.copy()
    if search_term:
        display_df = display_df[display_df.astype(str).apply(lambda x: x.str.contains(search_term, case=False)).any(axis=1)]
        
    st.dataframe(display_df, use_container_width=True)
    
    csv_data = display_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv_data,
        file_name="placement_filtered.csv",
        mime="text/csv"
    )

# -----------------------------------------------------------------------------
# TAB 4: EXECUTIVE INSIGHTS
# -----------------------------------------------------------------------------
with tab4:
    st.subheader("💡 Key Analytical Takeaways & Empirical Drivers")
    
    st.markdown("""
    ### 1. 💼 Work Experience is the Single Strongest Placement Predictor
    * Candidates with prior work experience achieved an **86.5% placement rate**, compared to **59.6%** for those without.
    * Having work experience boosts candidate recruitment probability by **+26.9 percentage points**.
    
    ### 2. 📈 Foundational Academics (10th/12th) Out-predict MBA Score
    * Placed candidates scored **+14.2% higher in 10th grade** (`ssc_p`: 71.7% vs 57.5%) and **+11.5% higher in 12th grade** (`hsc_p`: 69.9% vs 58.4%).
    * In contrast, the difference in MBA performance (`mba_p`) between placed and unplaced candidates was negligible (**62.6% vs 61.6%**, a delta of only **+1.0%**).
    * *Recruiter Behavior Insight*: Campus recruiters prioritize long-term consistent academic performance over post-graduate scores alone.
    
    ### 3. 🎯 Marketing & Finance Yields Higher ROI than Marketing & HR
    * **Mkt&Fin** specialisation achieved a **79.2% placement rate** and an average salary of **₹2,98,853**.
    * **Mkt&HR** achieved a **55.8% placement rate** and an average salary of **₹2,70,377**.
    * Finance specialisation yields **+23.4% higher placement likelihood** and **+10.5% higher average pay**.
    """)

st.markdown("---")
st.markdown("<p style='text-align: center; color: #64748B;'>Built by Kavya Thakar | Campus Placement Data Analytics Portfolio</p>", unsafe_allow_html=True)
