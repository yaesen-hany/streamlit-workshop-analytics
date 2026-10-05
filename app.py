import streamlit as st 
import pandas as pd
st.set_page_config(page_title="My task13",page_icon="📊", layout="wide")
@st.cache_data
def load_data():
    df = pd.read_csv("training_center_data.csv")
    return df
def clean_data(df):
    df["date"] = pd.to_datetime(df["date"])
    df = df.drop_duplicates().reset_index(drop=True) 
    df["city"]= df["city"].ffill()
    df["cost"] = df["cost"].fillna(df["cost"].median())
    df["rating"] = df["rating"].fillna(df["rating"].median())
    df["learners"] = df["learners"].fillna(df["learners"].median())
    return df
df = pd.DataFrame(load_data())
dc=clean_data(df)   
st.title("Training Center Data Analysis")
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Overview", "Dataset Explorer", "Insights", "Feedback"])
if page == "Overview":
    st.image("photo.jpg")
    st.markdown("""
    Welcome to the central monitoring platform. This application allows program managers to:
    * Track learner enrollment across tech and business tracks.
    * Measure satisfaction scores and evaluate operational quality.
    * Audit operational costs per workshop and city.""")
    st.header("Data Overview before analysis")
    st.write(df)
    st.divider()
    st.header("Data Overview after cleaning")
    st.write(dc)
    st.header("Executive KPIs")
    total_learners = (dc["learners"].sum())
    avg_rating = round(dc["rating"].mean(), 2)
    total_cost = (dc["cost"].sum())
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Learners", f"{total_learners:,}")
    col2.metric("Average Rating", f"{avg_rating} / 5.0")
    col3.metric("Total Investment", f"${total_cost:,}")
    st.divider()
    st.header("Dataset Overview")
    sum_col1, sum_col2, sum_col3 = st.columns(3)
    sum_col1.write(f"**Total Records:** {len(dc)} workshops")
    sum_col2.write(f"**Active Tracks:** {dc.loc[dc['status'] == 'Ongoing', 'track'].nunique()} tracks")
    sum_col3.write(f"**Cities Covered:** {dc['city'].nunique()} locations")
    st.divider()
    st.subheader("Calculation Methodology")
    st.write("Average rating is calculated across all valid course reviews using:")
    st.latex(r"\text{Average Rating} = \frac{\text{Total Ratings}}{\text{Total Workshops}}")
    st.caption("CLI execution command:")
    st.code("streamlit run app.py")
elif page == "Dataset Explorer":
     st.header("Dataset Explorer")
     st.write("Explore the dataset with filters and visualizations.")
     st.subheader("Filter Controls")
     track_options = ["All"] + dc["track"].unique().tolist()
     selected_track = st.selectbox("Select Track:", track_options)
     city_options = ["All"] + dc["city"].unique().tolist()
     selected_city = st.selectbox("Select City:", city_options)
     status_options = ["All"] + dc["status"].unique().tolist()
     selected_status = st.selectbox("Select Status:", status_options)
     status_list = dc["status"].dropna().unique().tolist()
     min_d=dc["date"].min()
     max_d=dc["date"].max()
     selected_date_range = st.date_input("Select Date Range:", [min_d, max_d], min_value=min_d, max_value=max_d)
     min_c=int(dc["cost"].min())
     max_c=int(dc["cost"].max())
     max_cost_budget = st.slider(
            "Max Budget per Workshop:",
            min_value=min_c,
            max_value=max_c,
            value= max_c,
            step=10,
        )
     dff=dc.copy()
     if selected_track != "All":
        dff = dff[dff["track"] == selected_track]
     if selected_city != "All":
         dff = dff[dff["city"] == selected_city]
     if selected_status != "All":
            dff = dff[dff["status"] == selected_status]
     dff = dff[dff["cost"] <= max_cost_budget]
     if len(selected_date_range) == 2:
         start_date, end_date = selected_date_range
         dff = dff[(dff["date"] >= pd.to_datetime(start_date)) & (dff["date"] <= pd.to_datetime(end_date))]
     if dff.empty:
         st.warning("No records match the selected filters.")
     else:
         st.dataframe(dff)
         st.divider()
         st.table(dff["status"].value_counts())
         st.divider()
         st.data_editor(dff)     
elif page == "Insights":
    st.header("Insights & Analytics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Learners", f"{int(dc['learners'].sum()):}")
    col2.metric("Average Rating", f"{round(dc['rating'].mean(), 2)} / 5.0")
    col3.metric("Total Cost", f"${int(dc['cost'].sum()):,}")
    st.divider()
    st.subheader("Attendance Trend Over Time")
    trend = dc.groupby("date")["learners"].sum()
    st.line_chart(trend)
    st.divider()
    st.subheader("Learners Comparison")
    chart_by = st.radio("Group by:", ["track", "city", "status"], horizontal=True)
    bar_data = dc.groupby(chart_by)["learners"].sum()
    st.bar_chart(bar_data)
    st.divider()
    st.subheader("Analysis Answers")
    top_track = dc.groupby("track")["rating"].mean().idxmax()
    top_city = dc.groupby("city")["learners"].sum().idxmax()
    st.write(f"**Highest Rated Track:** {top_track}")
    st.write(f"**City with Most Learners:** {top_city}")
    st.write("**Attendance Over Time:** Displayed in the line chart above.")
    st.write("**Courses with Low Rating or High Cost:**")
    flagged = dc[(dc["rating"] < 4.0) | (dc["cost"] > dc["cost"].mean())]
    st.dataframe(flagged[["course", "rating", "cost", "track"]])
elif page == "Feedback":
    st.header("Feedback & Evaluation")
    if "feedback_history" not in st.session_state:
        st.session_state["feedback_history"] = []
    with st.form("feedback_form", clear_on_submit=True):
        name = st.text_input("Your Name:")
        score = st.slider("Rating (1-5):", 1, 5, 5)
        comment = st.text_area("Your Feedback:")
        submit = st.form_submit_button("Submit Feedback")
        if submit:
            if name and comment:
                st.session_state["feedback_history"].append(
                    {"Name": name, "Rating": score, "Comment": comment})
                st.success("Thank you! Feedback saved.")
            else:
                st.warning("Please fill in both name and feedback.")
    st.divider()
    st.subheader("Submitted Feedback")
    if st.session_state["feedback_history"]:
        st.dataframe(pd.DataFrame(st.session_state["feedback_history"]))
    else:
        st.write("No feedback submitted yet.")