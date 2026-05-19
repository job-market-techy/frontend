"""
Job Market Intelligence Platform - Streamlit Frontend
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import warnings
import plotly.express as px
import plotly.graph_objects as go
from typing import Tuple
from trial_new import JobMarketIntelligence


warnings.filterwarnings('ignore')

# ==================== KONFIGURASI ====================

st.set_page_config(
    page_title="Job Market Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CSS STYLING ====================

def load_css():
    st.markdown("""
        <style>
        /* MAIN HEADER - GRADASI ORANYE */
        .main-header {
            font-size: clamp(1.1rem, 4vw, 1.5rem);
            text-align: center;
            margin-bottom: 1rem;
            font-weight: bold;
        }
        
        .main-header .gradient-text {
            background: linear-gradient(135deg, #FF6B35 0%, #FF8C42 50%, #FFD166 100%);
            background-clip: text;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        /* SECTION HEADER - TEKS UTAMA */
        .section-header {
            font-size: 1.3rem;
            color: #ECECEC !important;
            margin-bottom: 0;
            font-weight: bold;
            text-align: center;
        }
        
        /* INFO BOX - CARD BACKGROUND */
        .info-box {
            background-color: #FF8C42;
            padding: 1rem;
            border-radius: 12px;
            margin: 0.5rem 0;
            color: #ECECEC !important;
            border-left: 5px solid #FF6B35;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.3);
        }
        .info-box * {
            color: #ECECEC !important;
        }
        
        /* INSIGHT BOX - CARD BACKGROUND */
        .insight-box {
            background-color: #2A2A2A;
            padding: 1rem;
            border-radius: 10px;
            margin: 1rem 0;
            color: #E9C46A !important;
            font-weight: bold;
            border-left: 5px solid #E9C46A;
        }
        .insight-box * {
            color: #E9C46A !important;
        }
        
        /* SKILL CARD - CARD BACKGROUND */
        .skill-card {
            background-color: #2A2A2A;
            padding: 0.8rem;
            border-radius: 10px;
            margin: 0.8rem 0;
            border-left: 4px solid #FF6B35;
            box-shadow: 0 2px 4px rgba(0,0,0,0.3);
            color: #ECECEC !important;
        }
        .skill-card * {
            color: #ECECEC !important;
        }
        
        /* HIGHLIGHT CARD - GRADASI ORANYE */
        .highlight-card {
            background: linear-gradient(135deg, #FF6B35 0%, #FF8C42 100%);
            padding: 1rem;
            border-radius: 12px;
            margin: 0.8rem 0;
            color: white;
            box-shadow: 0 4px 15px rgba(255,107,53,0.3);
        }
        .highlight-card h3, .highlight-card div {
            color:#2A2A2A !important;
        }
        
        /* BACKGROUND UTAMA */
        .stApp {
            background: #212121;
        }
        
        /* SIDEBAR - GRADASI ORANYE */
        [data-testid="stSidebar"] {
            background: linear-gradient(135deg, #FF6B35 0%, #FF8C42 50%, #FFD166 100%);
        }
        [data-testid="stSidebar"] * {
            color: #ECECEC !important;
        }
        
        /* HR LINE */
        hr {
            margin: 0.5rem 0;
            border-color: #444444;
        }
        
        /* ========== FORM PERSONAL RECOMMENDATIONS ========== */
        
        /* INPUT TEXT (Your current skills) */
        .stTextInput > div > div > input {
            background-color: #ECECEC !important;
            color: #ECECEC !important;
            border: 1px solid #FF6B35 !important;
            border-radius: 8px !important;
        }
        
        /* SELECTBOX (Career goal & Target country) */
        .stSelectbox > div > div {
            background-color: #ECECEC !important;
            border-radius: 8px !important;
        }
        
        .stSelectbox div[data-baseweb="select"] {
            background-color: #ECECEC !important;
            color: #ECECEC !important;
            border: 1px solid #FF6B35 !important;
            border-radius: 8px !important;
        }
        
        /* ICON PANAH SELECTBOX */
        .stSelectbox svg {
            fill: #ECECEC !important;
        }
        
        /* LABEL FORM */
        .stTextInput label, .stSelectbox label {
            color: #ECECEC !important;
            font-weight: 500 !important;
            margin-bottom: 0.25rem !important;
        }
        
        /* TOMBOL GET RECOMMENDATIONS */
        .stButton button {
            background-color: #FF6B35 !important;
            color: #ECECEC !important;
            border-radius: 8px !important;
            border: none !important;
            padding: 0.5rem 1rem !important;
            font-weight: bold !important;
        }
        
        .stButton button:hover {
            background-color: #E85D04 !important;
        }
        </style>
    """, unsafe_allow_html=True)

# ==================== BOX RENDERERS ====================

def render_title_box(title: str):
    st.markdown(f"""
    <div class="info-box">
        <div class="section-header">{title}</div>
    </div>
    """, unsafe_allow_html=True)

def render_insight_box(insight: str):
    st.markdown(f"""
    <div class="insight-box">
        💡 <strong>Insight:</strong> {insight}
    </div>
    """, unsafe_allow_html=True)

# ==================== GRAFIK FUNCTIONS (CHART_BACKGROUND = #2F2F2F) ====================

def plot_horizontal_job_titles(titles_df: pd.Series) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = ['#FF6B35', '#FF8C42', '#F4A261', '#E9C46A', '#6A9C89']
    bars = ax.barh(titles_df.index, titles_df.values, color=colors[:len(titles_df)], edgecolor='white', height=0.6)
    ax.set_xlabel('Number of Developers', fontsize=11, color='#ECECEC')
    ax.set_title('Top Job Titles', fontsize=14, fontweight='bold', color='#ECECEC', pad=15)
    ax.invert_yaxis()
    for bar, val in zip(bars, titles_df.values):
        ax.text(bar.get_width() + 100, bar.get_y() + bar.get_height()/2,
                f'{val:,}', va='center', fontsize=10, fontweight='bold', color='#ECECEC')
    ax.set_facecolor('#2F2F2F')
    fig.patch.set_facecolor('#2F2F2F')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_color('#ECECEC')
    ax.tick_params(colors='#ECECEC')
    return fig

def plot_skill_gaps(gaps_df: pd.DataFrame, skill_type: str) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(10, 6))
    x = range(len(gaps_df))
    width = 0.35
    bars1 = ax.bar([i - width/2 for i in x], gaps_df['have_count'], width,
                   label='Have (Current Users)', color='#E9C46A', edgecolor='white')
    bars2 = ax.bar([i + width/2 for i in x], gaps_df['want_count'], width,
                   label='Want (Learners)', color='#FF6B35', edgecolor='white')
    ax.set_xlabel('Skill', fontsize=11, color='#ECECEC')
    ax.set_ylabel('Number of Developers', fontsize=11, color='#ECECEC')
    ax.set_title(f'Top Skill Gaps - {skill_type.title()}', fontsize=14, fontweight='bold', color='#ECECEC', pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(gaps_df['skill'], rotation=45, ha='right', fontsize=10, color='#ECECEC')
    legend = ax.legend(loc='upper right', fontsize=10)
    for text in legend.get_texts():
        text.set_color('#ECECEC')
    legend.get_frame().set_facecolor('#2F2F2F')
    legend.get_frame().set_edgecolor('#ECECEC')
    for bar in bars1:
        height = bar.get_height()
        if height > 0:
            ax.annotate(f'{int(height)}', xy=(bar.get_x() + bar.get_width()/2, height),
                       xytext=(0, 3), textcoords="offset points", ha='center', fontsize=8, color='#ECECEC')
    for bar in bars2:
        height = bar.get_height()
        if height > 0:
            ax.annotate(f'{int(height)}', xy=(bar.get_x() + bar.get_width()/2, height),
                       xytext=(0, 3), textcoords="offset points", ha='center', fontsize=8, color='#ECECEC')
    ax.set_facecolor('#2F2F2F')
    fig.patch.set_facecolor('#2F2F2F')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color('#ECECEC')
    ax.spines['left'].set_color('#ECECEC')
    ax.tick_params(colors='#ECECEC')
    return fig


def plot_hiring_priorities(priorities: pd.Series) -> go.Figure:
    """Donut chart dengan persentase di dalam"""

    labels = priorities.index.tolist()
    values = priorities.values.tolist()
    colors = ['#FF6B35', '#FF8C42', '#F4A261', '#E9C46A', '#6A9C89', '#A0C4E2']

    # Buat donut chart
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.4,  # Lubang 40%
        marker=dict(colors=colors[:len(labels)]),
        textinfo='percent',  # Hanya persentase yang masuk DI DALAM
        textposition='inside',  # Posisi di dalam
        textfont=dict(color='white', size=14, weight='bold'),
        hoverinfo='label+value+percent',
        pull=[0.05 if i == 0 else 0 for i in range(len(labels))]
    )])

    # Update layout
    fig.update_layout(
        title=dict(
            text='Hiring Priorities',
            font=dict(color='#ECECEC', size=16),
            x=0.5
        ),
        paper_bgcolor='#2F2F2F',
        plot_bgcolor='#2F2F2F',
        showlegend=True,
        legend=dict(
            font=dict(color='#ECECEC'),
            bgcolor='#2F2F2F',
            x=1.05,
            y=0.5
        ),
        margin=dict(t=50, l=0, r=150, b=0),
        height=370,
        width=500
    )

    return fig

def plot_emerging_skill(selected_skill: str, demand_ratio: float, want_count: int, have_count: int) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(8, 4))
    categories = ['Have (Current Users)', 'Want (Learners)']
    values = [have_count, want_count]
    colors = ['#F4A261', '#FF6B35']
    bars = ax.bar(categories, values, color=colors, edgecolor='white', width=0.5)
    ax.set_ylabel('Number of Developers', fontsize=11, color='#ECECEC')
    ax.set_title(f'{selected_skill} - Demand Ratio: {demand_ratio}x', fontsize=13, fontweight='bold', color='#ECECEC')
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 50,
                f'{val:,}', ha='center', va='bottom', fontsize=10, fontweight='bold', color='#ECECEC')
    ax.set_facecolor('#2F2F2F')
    fig.patch.set_facecolor('#2F2F2F')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color('#ECECEC')
    ax.spines['left'].set_color('#ECECEC')
    ax.tick_params(colors='#ECECEC')
    return fig

# ==================== DATA LOADER ====================

@st.cache_resource
def load_data(csv_path: str = "cleaned_data.csv") -> JobMarketIntelligence:
    return JobMarketIntelligence(csv_path)

# ==================== SIDEBAR ====================

def render_sidebar(jmi: JobMarketIntelligence) -> Tuple[str, str, str]:
    with st.sidebar:
        st.image("download-removebg-preview.png", width=225)
        st.title("🎯 Navigation")
        page = st.radio(
            "Choose a section:",
            ["💡 Personal Recommendations", "🏠 Dashboard", "📈 Skill Analysis", "🎯 Skill Gaps",
             "🚀 Emerging Skills", "⭐ Hiring Priorities"]
        )
        st.divider()
        st.subheader("🔍 Filters")
        countries = ['All'] + sorted(jmi.df['country'].dropna().unique().tolist())
        selected_country = st.selectbox("Country", countries)
        skill_types = ['languages', 'frameworks', 'databases', 'platforms']
        selected_skill_type = st.selectbox("Skill Type", skill_types)
    return page, selected_country, selected_skill_type

# ==================== DASHBOARD PAGE ====================

def render_dashboard_page(jmi: JobMarketIntelligence, selected_country: str, selected_skill_type: str):
    st.markdown('<h1 class="main-header">📊 <span class="gradient-text">Job Market Intelligence Dashboard</span></h1>', unsafe_allow_html=True)

    # KEY METRICS
    st.markdown("""
    <div style="text-align: center; margin-bottom: 1rem;">
        <div class="section-header">📈 Key Metrics</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4, gap="medium")
    with col1:
        st.markdown(f"""
        <div style="background: #2A2A2A; padding: 1.2rem; border-radius: 16px; text-align: center; border-left: 4px solid #FF6B35;">
            <div style="font-size: 2.2rem;">👥</div>
            <div style="font-size: 1.8rem; font-weight: 700; color: #ECECEC;">{len(jmi.df):,}</div>
            <div style="font-size: 0.85rem; color: #ECECEC;">Total Developers</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div style="background: #2A2A2A; padding: 1.2rem; border-radius: 16px; text-align: center; border-left: 4px solid #06D6A0;">
            <div style="font-size: 2.2rem;">🌍</div>
            <div style="font-size: 1.8rem; font-weight: 700; color: #ECECEC;">{jmi.df['country'].nunique()}</div>
            <div style="font-size: 0.85rem; color: #ECECEC;">Countries</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        top_lang = jmi.get_top_skills('languages', 1).index[0]
        st.markdown(f"""
        <div style="background: #2A2A2A; padding: 1.2rem; border-radius: 16px; text-align: center; border-left: 4px solid #4361EE;">
            <div style="font-size: 2.2rem;">🏆</div>
            <div style="font-size: 1.5rem; font-weight: 700; color: #ECECEC;">{top_lang}</div>
            <div style="font-size: 0.85rem; color: #ECECEC;">Most Popular Language</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        total_skills = jmi.df['skills_languages'].dropna().str.split(';').explode().nunique()
        st.markdown(f"""
        <div style="background: #2A2A2A; padding: 1.2rem; border-radius: 16px; text-align: center; border-left: 4px solid #F72585;">
            <div style="font-size: 2.2rem;">💻</div>
            <div style="font-size: 1.8rem; font-weight: 700; color: #ECECEC;">{total_skills}</div>
            <div style="font-size: 0.85rem; color: #ECECEC;">Unique Skills</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # TOP JOB TITLES
    top_titles = jmi.get_top_job_titles(10)
    fig = plot_horizontal_job_titles(top_titles)
    st.pyplot(fig)
    plt.close()
    st.markdown("<hr>", unsafe_allow_html=True)

    # SKILL GAPS & HIRING PRIORITIES - SEJAJAR KANAN KIRI (TANPA JUDUL)
    col1, col2 = st.columns(2)

    with col1:
        gaps = jmi.get_skill_gap(selected_skill_type, 8)
        if len(gaps) > 0:
            fig = plot_skill_gaps(gaps, selected_skill_type)
            st.pyplot(fig)
            plt.close()
        else:
            st.info("No skill gaps found for this category")

    with col2:
        country_for_hiring = selected_country if selected_country != 'All' else None
        priorities = jmi.get_hiring_priorities(country_for_hiring)
        if not priorities.empty:
            fig = plot_hiring_priorities(priorities)
            st.plotly_chart(fig, use_container_width=True)  # ← Pakai st.plotly_chart
        else:
            st.warning("No hiring priority data available")
# ==================== SKILL ANALYSIS PAGE ====================

def render_skill_analysis_page(jmi: JobMarketIntelligence, selected_country: str, selected_skill_type: str):
    st.markdown('<h1 class="main-header">📈 <span class="gradient-text">Skill Analysis</span></h1>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        render_title_box("✅ Most Used Languages")
        if selected_country == 'All':
            skills = jmi.get_top_skills(selected_skill_type, 15)
        else:
            skills = jmi.get_skills_by_country(selected_country, selected_skill_type, 15)
        for i, (skill, count) in enumerate(skills.items(), 1):
            st.markdown(f'<div class="skill-card">{i}. {skill} — {count:,} developers</div>', unsafe_allow_html=True)
    with col2:
        render_title_box("🎯 Most Wanted Languages")
        if selected_country == 'All':
            want_skills = jmi.get_wanted_skills(selected_skill_type, 15)
        else:
            col_map = {'languages': 'wanted_languages', 'frameworks': 'wanted_frameworks', 'databases': 'wanted_databases', 'platforms': 'wanted_platforms'}
            country_data = jmi.df[jmi.df['country'] == selected_country]
            want_skills = (country_data[col_map[selected_skill_type]].dropna().str.split(';').explode().str.strip().str.title().value_counts().head(15))
        for i, (skill, count) in enumerate(want_skills.items(), 1):
            st.markdown(f'<div class="skill-card">{i}. {skill} — wanted by {count:,} developers</div>', unsafe_allow_html=True)

# ==================== SKILL GAPS PAGE ====================

def render_skill_gaps_page(jmi: JobMarketIntelligence, selected_country: str, selected_skill_type: str):
    st.markdown('<h1 class="main-header">🎯 <span class="gradient-text">Skill Gap Analysis</span></h1>', unsafe_allow_html=True)
    st.markdown('<div style="color: #ECECEC;">*Skills that are in high demand but low supply*</div>', unsafe_allow_html=True)
    gaps = jmi.get_skill_gap(selected_skill_type, 15)
    if len(gaps) > 0:
        for _, row in gaps.iterrows():
            st.markdown(f"""
            <div class="skill-card">
                <strong>{row['skill']}</strong><br>
                📊 Want: {row['want_count']:,} | ✅ Have: {row['have_count']:,} | 
                <span style="color:#FF6B35; font-weight:bold;">⚠️ Gap: {row['gap']:,}</span>
            </div>
            """, unsafe_allow_html=True)
        top_skill = gaps.iloc[0]['skill']
        render_insight_box(f"**{top_skill}** has the biggest gap with {gaps.iloc[0]['gap']:,} more developers wanting to learn it!")
    else:
        st.info("No skill gaps found")

# ==================== EMERGING SKILLS PAGE ====================

def render_emerging_skills_page(jmi: JobMarketIntelligence, selected_country: str, selected_skill_type: str):
    st.markdown('<h1 class="main-header">🚀 <span class="gradient-text">Emerging Skills</span></h1>', unsafe_allow_html=True)
    st.markdown('<div style="color: #ECECEC;">*Skills with highest demand ratio - Select a skill to see the graph*</div>', unsafe_allow_html=True)
    emerging = jmi.get_emerging_skills(selected_skill_type, 15)
    if len(emerging) > 0:
        col1, col2 = st.columns([1, 1])
        with col1:
            render_title_box("📋 Select a Skill")
            skill_options = emerging['skill'].tolist()
            selected_skill = st.selectbox("Choose a skill:", skill_options, label_visibility="collapsed")
            st.markdown("---")
            st.markdown('<div style="color: #ECECEC; font-weight: bold;">🔥 All Emerging Skills:</div>', unsafe_allow_html=True)
            for _, row in emerging.iterrows():
                ratio = row['demand_ratio']
                emoji = "🚀" if ratio >= 5 else "📈" if ratio >= 3 else "⭐"
                if selected_skill == row['skill']:
                    st.markdown(f'<div style="color: #FF6B35; font-weight: bold;">👉 {emoji} {row["skill"]} — {ratio}x 👈</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div style="color: #ECECEC;">{emoji} {row["skill"]} — {ratio}x</div>', unsafe_allow_html=True)
        with col2:
            if selected_skill:
                skill_data = emerging[emerging['skill'] == selected_skill].iloc[0]
                fig = plot_emerging_skill(selected_skill, skill_data['demand_ratio'], skill_data['want_count'], skill_data['have_count'])
                st.pyplot(fig)
                plt.close()
                st.markdown(f'<div class="insight-box">💡 <strong>Insight:</strong> {selected_skill} has <strong>{skill_data["demand_ratio"]}x</strong> more learners than users!</div>', unsafe_allow_html=True)
        top_skill = emerging.iloc[0]['skill']
        st.markdown(f'<div class="insight-box">🎯 <strong>Top Emerging Skill:</strong> {top_skill} has the highest demand ratio at {emerging.iloc[0]["demand_ratio"]}x!</div>', unsafe_allow_html=True)
    else:
        st.info("No emerging skills identified")

# ==================== HIRING PRIORITIES PAGE ====================

def render_hiring_priorities_page(jmi: JobMarketIntelligence, selected_country: str, selected_skill_type: str):
    st.markdown('<h1 class="main-header">⭐ <span class="gradient-text">Hiring Priorities</span></h1>', unsafe_allow_html=True)
    st.markdown('<div style="color: #ECECEC;">*What employers value most when hiring*</div>', unsafe_allow_html=True)
    country_for_hiring = selected_country if selected_country != 'All' else None
    priorities = jmi.get_hiring_priorities(country_for_hiring)
    if not priorities.empty:
        for name, pct in priorities.items():
            if name == list(priorities.keys())[0]:
                st.markdown(f'<div class="highlight-card"><h3 style="margin: 0;">⭐ {name}</h3><div style="font-size: 1.2rem;"><strong>{pct:.0f}%</strong> of recruiters find this important</div></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="skill-card"><strong>{name}</strong><br>{pct:.0f}% of recruiters find this important</div>', unsafe_allow_html=True)
        top_priority = list(priorities.keys())[0]
        render_insight_box(f"{top_priority} is what recruiters value most! ({priorities.iloc[0]:.0f}%)")
    else:
        st.warning("No hiring priority data available")

# ==================== PERSONAL RECOMMENDATIONS PAGE ====================

def render_personal_recommendations_page(jmi: JobMarketIntelligence, selected_country: str, selected_skill_type: str):
    st.markdown('<h1 class="main-header">💡 <span class="gradient-text">Personalized Skill Recommendations</span></h1>', unsafe_allow_html=True)
    countries = ['All'] + sorted(jmi.df['country'].dropna().unique().tolist())
    with st.form("user_profile"):
        col1, col2 = st.columns(2)
        with col1:
            current_skills = st.text_input("💻 Your current skills", placeholder="e.g., Python, SQL, JavaScript")
            career_goal = st.selectbox("🎯 Career goal", ["Data Scientist", "Web Developer", "DevOps Engineer", "Mobile Developer", "Machine Learning Engineer", "Other"])
        with col2:
            target_country = st.selectbox("🌍 Target country", countries[1:])
            if career_goal == "Other":
                career_goal = st.text_input("📝 Specify your target role")
        submitted = st.form_submit_button("🎯 Get Recommendations", use_container_width=True)
    if submitted and current_skills:
        skill_list = [s.strip() for s in current_skills.split(',')]
        with st.spinner("📊 Analyzing market data..."):
            try:
                recommendations = jmi.recommend_skills(skill_list, career_goal if career_goal != "Other" else None, target_country if target_country != "All" else None, n=10)
                if len(recommendations) > 0:
                    for i, (_, row) in enumerate(recommendations.iterrows(), 1):
                        score = row['demand_score']
                        if i == 1:
                            st.markdown(f'<div class="highlight-card"><h2>🏆 #{i}</h2><h1 style="font-size: 1.8rem; color: white;">{row["skill"]}</h1><div style="color: white;">🔥 Demand Score: <strong>{score}/10</strong></div><div style="color: white;">💡 {row["reasons"]}</div></div>', unsafe_allow_html=True)
                        elif i == 2:
                            st.markdown(f'<div class="highlight-card" style="background: linear-gradient(135deg, #FF8C42 0%, #FFA559 100%);"><h3 style="color: white;">🥈 #{i}</h3><h2 style="font-size: 1.7rem; color: white;">{row["skill"]}</h2><div style="color: white;">📈 Demand Score: <strong>{score}/10</strong></div><div style="color: white;">💡 {row["reasons"]}</div></div>', unsafe_allow_html=True)
                        elif i == 3:
                            st.markdown(f'<div class="highlight-card" style="background: linear-gradient(135deg, #F4A261 0%, #F6B17A 100%);"><h3 style="color: white;">🥉 #{i}</h3><h2 style="font-size: 1.7rem; color: white;">{row["skill"]}</h2><div style="color: white;">⭐ Demand Score: <strong>{score}/10</strong></div><div style="color: white;">💡 {row["reasons"]}</div></div>', unsafe_allow_html=True)
                        else:
                            st.markdown(f'<div class="skill-card"><strong>#{i} {row["skill"]}</strong> — Demand Score: {score}/10<br>💡 {row["reasons"]}</div>', unsafe_allow_html=True)
                    render_insight_box(f"Start with **{recommendations.iloc[0]['skill']}** — it has the highest demand score!")
                else:
                    st.info("📭 No recommendations found.")
            except AttributeError:
                st.error("❌ Method 'recommend_skills()' not found.")
            except Exception as e:
                st.error(f"❌ Error: {e}")
    elif submitted:
        st.warning("⚠️ Please enter your current skills first!")

# ==================== FOOTER ====================

def render_footer():
    st.divider()
    st.markdown("<p style='text-align: center; color: #ECECEC;'>📊 Job Market Intelligence Platform | Powered by Stack Overflow Survey Data</p>", unsafe_allow_html=True)

# ==================== MAIN APP ====================

def main():
    load_css()
    try:
        jmi = load_data("cleaned_data.csv")
    except FileNotFoundError:
        st.error("❌ File 'cleaned_data.csv' tidak ditemukan!")
        st.stop()
    page, selected_country, selected_skill_type = render_sidebar(jmi)
    if page == "🏠 Dashboard":
        render_dashboard_page(jmi, selected_country, selected_skill_type)
    elif page == "📈 Skill Analysis":
        render_skill_analysis_page(jmi, selected_country, selected_skill_type)
    elif page == "🎯 Skill Gaps":
        render_skill_gaps_page(jmi, selected_country, selected_skill_type)
    elif page == "🚀 Emerging Skills":
        render_emerging_skills_page(jmi, selected_country, selected_skill_type)
    elif page == "⭐ Hiring Priorities":
        render_hiring_priorities_page(jmi, selected_country, selected_skill_type)
    elif page == "💡 Personal Recommendations":
        render_personal_recommendations_page(jmi, selected_country, selected_skill_type)
    render_footer()

if __name__ == "__main__":
    main()