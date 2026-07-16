"""
EduPro Instructor Performance Dashboard
Professional Streamlit Application for Real-Time Performance Monitoring
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import os
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="EduPro Performance Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and cache data"""
    data_dir = r'c:\Users\SARAH\OneDrive\Instructor performance'
    teachers = pd.read_csv(os.path.join(data_dir, 'teachers_data.csv'))
    courses = pd.read_csv(os.path.join(data_dir, 'courses_data.csv'))
    transactions = pd.read_csv(os.path.join(data_dir, 'transactions_data.csv'))
    
    # Integrate data
    integrated = transactions.merge(teachers, on='TeacherID', how='left')
    integrated = integrated.merge(courses, on='CourseID', how='left')
    
    return teachers, courses, transactions, integrated

# Load data
teachers, courses, transactions, integrated = load_data()

# ============================================================================
# SIDEBAR - FILTERS
# ============================================================================
st.sidebar.title("🎛️ Dashboard Filters")
st.sidebar.markdown("---")

# Expertise Filter
selected_expertise = st.sidebar.multiselect(
    "Select Expertise Areas",
    options=sorted(teachers['Expertise'].unique()),
    default=sorted(teachers['Expertise'].unique())
)

# Course Category Filter
selected_category = st.sidebar.multiselect(
    "Select Course Categories",
    options=sorted(courses['CourseCategory'].unique()),
    default=sorted(courses['CourseCategory'].unique())
)

# Course Level Filter
selected_level = st.sidebar.multiselect(
    "Select Course Levels",
    options=sorted(courses['CourseLevel'].unique()),
    default=sorted(courses['CourseLevel'].unique())
)

# Rating Range Filter
rating_range = st.sidebar.slider(
    "Teacher Rating Range",
    min_value=2.0,
    max_value=5.0,
    value=(2.0, 5.0),
    step=0.1
)

# Experience Range Filter
exp_range = st.sidebar.slider(
    "Years of Experience",
    min_value=0,
    max_value=25,
    value=(0, 25),
    step=1
)

# Apply Filters
filtered_teachers = teachers[
    (teachers['Expertise'].isin(selected_expertise)) &
    (teachers['TeacherRating'] >= rating_range[0]) &
    (teachers['TeacherRating'] <= rating_range[1]) &
    (teachers['YearsOfExperience'] >= exp_range[0]) &
    (teachers['YearsOfExperience'] <= exp_range[1])
]

filtered_courses = courses[courses['CourseCategory'].isin(selected_category)]
filtered_courses = filtered_courses[filtered_courses['CourseLevel'].isin(selected_level)]

filtered_integrated = integrated[
    (integrated['Expertise'].isin(selected_expertise)) &
    (integrated['CourseCategory'].isin(selected_category)) &
    (integrated['CourseLevel'].isin(selected_level)) &
    (integrated['TeacherRating'] >= rating_range[0]) &
    (integrated['TeacherRating'] <= rating_range[1])
]

# ============================================================================
# MAIN DASHBOARD
# ============================================================================

# Header
col1, col2 = st.columns([3, 1])
with col1:
    st.title("📊 EduPro Performance Dashboard")
    st.markdown("### Comprehensive Instructor Performance & Course Quality Analysis")

with col2:
    st.metric("Last Updated", datetime.now().strftime("%Y-%m-%d %H:%M"))

st.markdown("---")

# ============================================================================
# SECTION 1: KPI CARDS
# ============================================================================
st.markdown("## Executive KPI Cards")

col1, col2, col3, col4, col5 = st.columns(5)

# KPI 1: Average Teacher Rating
with col1:
    avg_rating = filtered_teachers['TeacherRating'].mean()
    st.metric(
        "Avg Teacher Rating",
        f"{avg_rating:.2f}/5.0",
        delta=f"{(avg_rating - 4.0):.2f}" if avg_rating > 4.0 else None,
        delta_color="off"
    )

# KPI 2: Average Course Rating
with col2:
    avg_course_rating = filtered_integrated['CourseRating'].mean()
    st.metric(
        "Avg Course Rating",
        f"{avg_course_rating:.2f}/5.0",
        delta=f"{(avg_course_rating - 4.0):.2f}" if avg_course_rating > 4.0 else None
    )

# KPI 3: Total Enrollments
with col3:
    total_enrollments = filtered_integrated['EnrollmentCount'].sum()
    st.metric(
        "Total Enrollments",
        f"{total_enrollments:,}",
        delta=None
    )

# KPI 4: Number of Instructors
with col4:
    num_instructors = filtered_teachers['TeacherID'].nunique()
    st.metric(
        "Active Instructors",
        f"{num_instructors}",
        delta=None
    )

# KPI 5: Avg Experience
with col5:
    avg_experience = filtered_teachers['YearsOfExperience'].mean()
    st.metric(
        "Avg Experience",
        f"{avg_experience:.1f} years",
        delta=None
    )

st.markdown("---")

# ============================================================================
# SECTION 2: INSTRUCTOR LEADERBOARD
# ============================================================================
st.markdown("## 🏆 Instructor Leaderboard")

col1, col2 = st.columns(2)

# Top Performers by Rating
with col1:
    st.subheader("Top 10 by Rating")
    top_by_rating = filtered_teachers.nlargest(10, 'TeacherRating')[
        ['TeacherName', 'TeacherRating', 'Expertise', 'YearsOfExperience']
    ]
    top_by_rating.index = range(1, len(top_by_rating) + 1)
    st.dataframe(top_by_rating, width='stretch')

# Top by Enrollments
with col2:
    st.subheader("Top 10 by Enrollments")
    teacher_enrollments = filtered_integrated.groupby('TeacherID').agg({
        'EnrollmentCount': 'sum',
        'TeacherName': 'first',
        'TeacherRating': 'first'
    }).sort_values('EnrollmentCount', ascending=False).head(10)
    
    df_enroll = pd.DataFrame({
        'Instructor': teacher_enrollments['TeacherName'],
        'Total Enrollments': teacher_enrollments['EnrollmentCount'],
        'Rating': teacher_enrollments['TeacherRating']
    })
    df_enroll.index = range(1, len(df_enroll) + 1)
    st.dataframe(df_enroll, width='stretch')

st.markdown("---")

# ============================================================================
# SECTION 3: EXPERIENCE vs RATING ANALYSIS
# ============================================================================
st.markdown("## 📈 Experience vs Performance Analysis")

fig = px.scatter(
    filtered_teachers,
    x='YearsOfExperience',
    y='TeacherRating',
    size='Age',
    color='Expertise',
    hover_name='TeacherName',
    title='Instructor Experience vs Rating (bubble size = age)',
    labels={
        'YearsOfExperience': 'Years of Experience',
        'TeacherRating': 'Teacher Rating'
    }
)

fig.add_hline(y=filtered_teachers['TeacherRating'].mean(), 
              line_dash="dash", line_color="red", 
              annotation_text="Avg Rating", annotation_position="right")

st.plotly_chart(fig, width='stretch')

st.markdown("---")

# ============================================================================
# SECTION 4: COURSE QUALITY HEATMAP
# ============================================================================
st.markdown("## 🔥 Course Quality Heatmap")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Quality by Category")
    category_stats = filtered_integrated.groupby('CourseCategory').agg({
        'CourseRating': 'mean',
        'EnrollmentCount': 'sum'
    }).reset_index()
    
    fig_cat = go.Figure(data=go.Bar(
        x=category_stats['CourseCategory'],
        y=category_stats['CourseRating'],
        marker_color=category_stats['CourseRating'],
        marker_colorscale='RdYlGn',
        text=category_stats['CourseRating'].round(2),
        textposition='outside',
        marker_line_width=2
    ))
    fig_cat.update_layout(title='Average Rating by Category', height=400)
    st.plotly_chart(fig_cat, width='stretch')

with col2:
    st.subheader("Quality by Level")
    level_stats = filtered_integrated.groupby('CourseLevel').agg({
        'CourseRating': 'mean',
        'EnrollmentCount': 'sum'
    }).reset_index()
    
    fig_level = go.Figure(data=go.Bar(
        x=level_stats['CourseLevel'],
        y=level_stats['CourseRating'],
        marker_color=level_stats['CourseRating'],
        marker_colorscale='Viridis',
        text=level_stats['CourseRating'].round(2),
        textposition='outside',
        marker_line_width=2
    ))
    fig_level.update_layout(title='Average Rating by Level', height=400)
    st.plotly_chart(fig_level, width='stretch')

st.markdown("---")

# ============================================================================
# SECTION 5: EXPERTISE PERFORMANCE COMPARISON
# ============================================================================
st.markdown("## 💡 Expertise Performance Comparison")

expertise_stats = filtered_integrated.groupby('Expertise').agg({
    'TeacherRating': 'mean',
    'CourseRating': 'mean',
    'EnrollmentCount': 'sum'
}).sort_values('TeacherRating', ascending=False).reset_index()

fig_expertise = make_subplots(
    specs=[[{"secondary_y": True}]]
)

fig_expertise.add_trace(
    go.Bar(x=expertise_stats['Expertise'], y=expertise_stats['TeacherRating'],
           name='Teacher Rating', marker_color='lightblue'),
    secondary_y=False
)

fig_expertise.add_trace(
    go.Scatter(x=expertise_stats['Expertise'], y=expertise_stats['EnrollmentCount'],
               name='Total Enrollments', mode='lines+markers',
               line=dict(color='red', width=3)),
    secondary_y=True
)

fig_expertise.update_layout(
    title='Expertise Area Performance',
    xaxis_title='Expertise',
    yaxis_title='Average Rating',
    yaxis2_title='Total Enrollments',
    hovermode='x unified',
    height=500
)

st.plotly_chart(fig_expertise, width='stretch')

st.markdown("---")

# ============================================================================
# SECTION 6: ENROLLMENT ANALYSIS
# ============================================================================
st.markdown("## 👥 Enrollment Distribution Analysis")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Enrollment by Instructor Tier")
    
    filtered_integrated['Tier'] = pd.cut(
        filtered_integrated['TeacherRating'],
        bins=[0, 3.5, 4.49, 5.0],
        labels=['Low', 'Mid', 'High']
    )
    
    tier_enrollments = filtered_integrated.groupby('Tier')['EnrollmentCount'].sum().reset_index()
    
    fig_tier = px.pie(
        tier_enrollments,
        values='EnrollmentCount',
        names='Tier',
        title='Enrollment Distribution by Instructor Tier',
        color_discrete_map={'Low': '#ff6b6b', 'Mid': '#ffd93d', 'High': '#6bcf7f'}
    )
    st.plotly_chart(fig_tier, width='stretch')

with col2:
    st.subheader("Enrollment Trends")
    
    enrollment_stats = filtered_integrated.groupby('CourseLevel')['EnrollmentCount'].agg(['sum', 'mean', 'count']).reset_index()
    
    fig_trends = go.Figure()
    fig_trends.add_trace(go.Bar(
        x=enrollment_stats['CourseLevel'],
        y=enrollment_stats['sum'],
        name='Total Enrollments',
        marker_color='steelblue'
    ))
    fig_trends.update_layout(title='Total Enrollments by Course Level', height=400)
    st.plotly_chart(fig_trends, width='stretch')

st.markdown("---")

# ============================================================================
# SECTION 7: RECOMMENDATION ENGINE
# ============================================================================
st.markdown("## 💡 AI-Powered Recommendations")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🎯 Quick Wins")
    
    # Get insights
    low_performers = filtered_teachers[filtered_teachers['TeacherRating'] < 3.5]
    high_performers = filtered_teachers[filtered_teachers['TeacherRating'] >= 4.5]
    
    st.info(f"""
    **Top 3 Actionable Items:**
    
    1. 📈 **Performance Gap**: {len(low_performers)} instructors need support
    
    2. 🏆 **Best Practices**: Learn from {len(high_performers)} high performers
    
    3. 🎓 **Experience Factor**: Mentorship ROI could increase ratings by 0.5-1.0 points
    """)

with col2:
    st.subheader("⚠️ Risk Alerts")
    
    risks = []
    if len(low_performers) > 0:
        risks.append(f"• {len(low_performers)} at-risk instructors detected")
    
    declining_categories = filtered_integrated.groupby('CourseCategory')['CourseRating'].mean().sort_values().head(2)
    for cat, rating in declining_categories.items():
        if rating < 4.0:
            risks.append(f"• {cat} courses below benchmark (Rating: {rating:.2f})")
    
    if risks:
        st.warning("\n".join(risks))
    else:
        st.success("✓ All metrics within healthy ranges")

st.markdown("---")

# Footer
st.markdown("""
<div style='text-align: center; color: #666; margin-top: 50px; padding: 20px;'>
    <p>📊 EduPro Dashboard | Data-Driven Instructor Performance Analytics</p>
    <p>Powered by Streamlit & Plotly | Last Updated: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</p>
</div>
""", unsafe_allow_html=True)
