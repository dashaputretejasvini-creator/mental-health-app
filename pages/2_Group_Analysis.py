import streamlit as st
import plotly.express as px
import pandas as pd
import sys
import os

# Add parent folder to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.preprocess import load_and_clean_data

# ── PAGE CONFIG ──────────────────────────────────────
st.set_page_config(
    page_title="Group Analysis",
    page_icon="👥",
    layout="wide"
)

# ── LOAD DATA ────────────────────────────────────────
@st.cache_data
def load_data():
    return load_and_clean_data()

df = load_data()

# Split into separate dataframes
df_students = df[df['category'] == 'Student'].copy()
df_workers = df[df['category'] == 'Worker'].copy()

# ── TITLE ────────────────────────────────────────────
st.title("👥 Group Analysis")
st.markdown("Analysing students and workers separately for accurate insights")
st.markdown("---")

# ── TABS ─────────────────────────────────────────────
tab1, tab2 = st.tabs(["👨‍🎓 Students", "👷 Workers"])

# ════════════════════════════════════════════════════
# STUDENTS TAB
# ════════════════════════════════════════════════════
with tab1:
    st.header("👨‍🎓 Student Mental Health Analysis")
    st.markdown(f"Analysing **{len(df_students):,} students**")
    st.markdown("---")

    # ── STUDENT FILTERS ──────────────────────────────
    st.sidebar.title("👨‍🎓 Student Filters")
    student_age_groups = st.sidebar.multiselect(
        "Age Groups (Students)",
        options=df_students['age_group'].dropna().unique().tolist(),
        default=df_students['age_group'].dropna().unique().tolist(),
        key="student_age"
    )

    filtered_students = df_students.copy()
    if student_age_groups:
        filtered_students = filtered_students[
            filtered_students['age_group'].isin(student_age_groups)
        ]

    # ── STUDENT METRIC CARDS ─────────────────────────
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Students", f"{len(filtered_students):,}")
    with col2:
        depression_rate = round(
            filtered_students['depression'].mean() * 100, 1
        )
        st.metric("Depression Rate", f"{depression_rate}%")
    with col3:
        avg_sleep = round(filtered_students['sleep_hours'].mean(), 1)
        st.metric("Avg Sleep Hours", f"{avg_sleep}h")
    with col4:
        avg_stress = round(filtered_students['stress_level'].mean(), 1)
        st.metric("Avg Stress Level", f"{avg_stress}/10")

    st.markdown("---")

    # ── STUDENT ROW 1 ────────────────────────────────
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Depression Rate by Age Group")
        dep_age = filtered_students.groupby(
            'age_group'
        )['depression'].mean().reset_index()
        dep_age.columns = ['Age Group', 'Depression Rate %']
        dep_age['Depression Rate %'] = (
            dep_age['Depression Rate %'] * 100
        ).round(1)
        fig = px.bar(
            dep_age,
            x='Age Group',
            y='Depression Rate %',
            color='Depression Rate %',
            color_continuous_scale='RdYlGn_r',
            title='Which age group has highest depression?'
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Sleep Hours vs Depression")
        fig2 = px.box(
            filtered_students,
            x='depression',
            y='sleep_hours',
            color='depression',
            labels={'depression': 'Depressed (0=No, 1=Yes)'},
            color_discrete_map={0: '#10B981', 1: '#EF4444'},
            title='Do depressed students sleep less?'
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    # ── STUDENT ROW 2 ────────────────────────────────
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Stress Level Distribution")
        fig3 = px.histogram(
            filtered_students,
            x='stress_level',
            color='risk_level',
            color_discrete_map={
                'Low': '#10B981',
                'Medium': '#F59E0B',
                'High': '#EF4444'
            },
            barmode='overlay',
            title='How stressed are students?'
        )
        st.plotly_chart(fig3, use_container_width=True)

    with col2:
        st.subheader("Risk Level by Age Group")
        risk_age = filtered_students.groupby(
            ['age_group', 'risk_level']
        ).size().reset_index(name='count')

        total_per_group = risk_age.groupby(
            'age_group'
        )['count'].transform('sum')
        risk_age['percentage'] = (
            risk_age['count'] / total_per_group * 100
        ).round(1)

        fig4 = px.bar(
            risk_age,
            x='age_group',
            y='percentage',
            color='risk_level',
            barmode='stack',
            color_discrete_map={
                'Low': '#10B981',
                'Medium': '#F59E0B',
                'High': '#EF4444'
            },
            title='Risk level % per age group'
        )
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown("---")

    # ── STUDENT HEATMAP ───────────────────────────────
    st.subheader("Heatmap — Age Group vs Risk Level")
    heat = filtered_students.groupby(
        ['age_group', 'risk_level']
    ).size().reset_index(name='count')

    pivot = heat.pivot(
        index='age_group',
        columns='risk_level',
        values='count'
    ).fillna(0)

    fig5 = px.imshow(
        pivot,
        color_continuous_scale='RdYlGn_r',
        title='Student risk distribution across age groups'
    )
    st.plotly_chart(fig5, use_container_width=True)

    st.markdown("---")

    # ── STUDENT INSIGHTS ─────────────────────────────
    st.subheader("📌 Key Student Insights")
    most_depressed_age = filtered_students.groupby(
        'age_group'
    )['depression'].mean().idxmax()
    least_sleep_age = filtered_students.groupby(
        'age_group'
    )['sleep_hours'].mean().idxmin()
    avg_stress_students = round(
        filtered_students['stress_level'].mean(), 1
    )
    st.info(f"📍 Most depressed age group: **{most_depressed_age}**")
    st.info(f"😴 Least sleep age group: **{least_sleep_age}**")
    st.info(f"😰 Average stress level: **{avg_stress_students}/10**")
    st.info(f"🧠 Overall depression rate: **{depression_rate}%**")


# ════════════════════════════════════════════════════
# WORKERS TAB
# ════════════════════════════════════════════════════
with tab2:
    st.header("👷 Worker Mental Health Analysis")
    st.markdown(f"Analysing **{len(df_workers):,} workers**")
    st.markdown("---")

    # ── WORKER METRIC CARDS ──────────────────────────
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Workers", f"{len(df_workers):,}")
    with col2:
        disorder_rate = round(
            df_workers[
                df_workers['sleep_disorder'] != 'None'
            ].shape[0] / len(df_workers) * 100, 1
        )
        st.metric("Sleep Disorder %", f"{disorder_rate}%")
    with col3:
        avg_sleep_w = round(df_workers['sleep_hours'].mean(), 1)
        st.metric("Avg Sleep Hours", f"{avg_sleep_w}h")
    with col4:
        avg_stress_w = round(df_workers['stress_level'].mean(), 1)
        st.metric("Avg Stress Level", f"{avg_stress_w}/8")

    st.markdown("---")

    # ── WORKER ROW 1 ─────────────────────────────────
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Stress Level by Occupation")
        stress_occ = df_workers.groupby(
            'occupation'
        )['stress_level'].mean().reset_index()
        stress_occ.columns = ['Occupation', 'Avg Stress']
        stress_occ = stress_occ.sort_values(
            'Avg Stress', ascending=True
        )
        fig6 = px.bar(
            stress_occ,
            x='Avg Stress',
            y='Occupation',
            orientation='h',
            color='Avg Stress',
            color_continuous_scale='RdYlGn_r',
            title='Which occupation is most stressed?'
        )
        st.plotly_chart(fig6, use_container_width=True)

    with col2:
        st.subheader("Sleep Hours by Occupation")
        fig7 = px.box(
            df_workers,
            x='occupation',
            y='sleep_hours',
            color='occupation',
            title='Sleep hours across different jobs'
        )
        fig7.update_xaxes(tickangle=45)
        st.plotly_chart(fig7, use_container_width=True)

    st.markdown("---")

    # ── WORKER ROW 2 ─────────────────────────────────
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Sleep Disorder Distribution")
        disorder_counts = df_workers[
            'sleep_disorder'
        ].value_counts().reset_index()
        disorder_counts.columns = ['Sleep Disorder', 'Count']
        fig8 = px.pie(
            disorder_counts,
            names='Sleep Disorder',
            values='Count',
            color_discrete_sequence=[
                '#10B981', '#EF4444', '#F59E0B'
            ],
            title='How many workers have sleep disorders?'
        )
        st.plotly_chart(fig8, use_container_width=True)

    with col2:
        st.subheader("Physical Activity vs Stress")
        fig9 = px.scatter(
            df_workers,
            x='physical_activity',
            y='stress_level',
            color='sleep_disorder',
            size='sleep_hours',
            title='Does exercise reduce stress for workers?'
        )
        st.plotly_chart(fig9, use_container_width=True)

    st.markdown("---")

    # ── WORKER ROW 3 ─────────────────────────────────
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("BMI vs Sleep Hours")
        fig10 = px.box(
            df_workers,
            x='bmi',
            y='sleep_hours',
            color='bmi',
            title='Does BMI affect sleep hours?'
        )
        st.plotly_chart(fig10, use_container_width=True)

    with col2:
        st.subheader("Risk Level by Occupation")
        risk_occ = df_workers.groupby(
            ['occupation', 'risk_level']
        ).size().reset_index(name='count')

        total_per_occ = risk_occ.groupby(
            'occupation'
        )['count'].transform('sum')
        risk_occ['percentage'] = (
            risk_occ['count'] / total_per_occ * 100
        ).round(1)

        fig11 = px.bar(
            risk_occ,
            x='occupation',
            y='percentage',
            color='risk_level',
            barmode='stack',
            color_discrete_map={
                'Low': '#10B981',
                'Medium': '#F59E0B',
                'High': '#EF4444'
            },
            title='Risk level % per occupation'
        )
        fig11.update_xaxes(tickangle=45)
        st.plotly_chart(fig11, use_container_width=True)

    st.markdown("---")

    # ── WORKER INSIGHTS ───────────────────────────────
    st.subheader("📌 Key Worker Insights")
    most_stressed_job = df_workers.groupby(
        'occupation'
    )['stress_level'].mean().idxmax()
    least_sleep_job = df_workers.groupby(
        'occupation'
    )['sleep_hours'].mean().idxmin()
    most_disorder_job = df_workers.groupby(
        'occupation'
    )['depression'].mean().idxmax()

    st.info(f"😰 Most stressed occupation: **{most_stressed_job}**")
    st.info(f"😴 Least sleep occupation: **{least_sleep_job}**")
    st.info(f"⚠️ Highest risk occupation: **{most_disorder_job}**")
    st.info(f"🩺 Workers with sleep disorders: **{disorder_rate}%**")