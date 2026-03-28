import streamlit as st
import pandas as pd
import plotly.express as px
from module.data_loader import load_data
from module.cleaning import clean_data
from module.modeling import train_models
from module.evaluation import get_best_model, results_to_df
from module.visualization import generate_plot
from db import get_engine
st.set_page_config(page_title="Smart Data Analyst Tool", layout="wide")
st.title("🧠 Smart Data Analyst Tool")
engine = get_engine()
TABLE_NAME = "uploaded_data"
file = st.file_uploader("📂 Upload CSV file", type=["csv"])
if file:
    df = load_data(file)
    if df is None:
        st.error("Error loading file")
        st.stop()
    try:
        df.to_sql(TABLE_NAME, engine, if_exists="replace", index=False)
        st.success("✅ Data saved to SQLite database")
    except Exception as e:
        st.error(f"Database save error: {e}")
        st.stop()
    try:
        df = pd.read_sql(f"SELECT * FROM {TABLE_NAME}", engine)
    except Exception as e:
        st.error(f"Database read error: {e}")
        st.stop()
    st.session_state.df = df
    tab1, tab2, tab3, tab4 = st.tabs([
        "📂 Data Loading",
        "🧹 Data Cleaning",
        "📊 Visualization",
        "🤖 Machine Learning"
    ])
    with tab1:
        df = st.session_state.get("df")
        st.subheader("📂 Data from Database")
        st.dataframe(df, use_container_width=True)
        st.write("Shape:", df.shape)
        st.write("Missing Values:")
        st.write(df.isnull().sum())
        csv_raw = df.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Download Raw Data", csv_raw, "raw_data.csv", "text/csv")
    with tab2:
        df = st.session_state.get("df")
        st.subheader("🧹 Data Cleaning")
        if st.button("Clean Data"):
            df_cleaned, report = clean_data(df)
            st.session_state.df = df_cleaned
            st.session_state.cleaned_df = df_cleaned
            st.session_state.report = report
            try:
                df_cleaned.to_sql("cleaned_data", engine, if_exists="replace", index=False)
                st.success("Cleaned data saved to DB ✅")
            except Exception as e:
                st.warning(f"Could not save cleaned data: {e}")
        if "report" in st.session_state:
            st.subheader("📊 Cleaning Report")
            st.json(st.session_state.report)
        if "cleaned_df" in st.session_state:
            st.dataframe(st.session_state.cleaned_df, use_container_width=True)
            csv_clean = st.session_state.cleaned_df.to_csv(index=False).encode('utf-8')
            st.download_button("⬇️ Download Cleaned Data", csv_clean, "cleaned_data.csv", "text/csv")
    with tab3:
        df = st.session_state.get("df")
        st.subheader("📊 Visualization")
        num_cols = df.select_dtypes(include=['int64', 'float64']).columns
        plot_type = st.selectbox(
            "Choose Plot",
            ["Histogram", "KDE Plot", "Bar Chart", "Scatter", "Box Plot", "Heatmap", "Correlation"]
        )
        col, x, y = None, None, None
        if plot_type in ["Histogram", "KDE Plot", "Box Plot"]:
            col = st.selectbox("Select Numeric Column", num_cols)
        elif plot_type == "Bar Chart":
            col = st.selectbox("Select Column", df.columns)
        elif plot_type == "Scatter":
            x = st.selectbox("X axis (numeric)", num_cols)
            y = st.selectbox("Y axis (numeric)", num_cols)
        result = generate_plot(df, plot_type, column=col, x=x, y=y)
        if isinstance(result, str):
            st.warning(result)
        elif result:
            st.plotly_chart(result, use_container_width=True)
    with tab4:
        df = st.session_state.get("df")
        st.subheader("🤖 Machine Learning")
        target = st.selectbox("🎯 Select Target Column", df.columns)
        if st.button("Run Models"):
            X = df.drop(columns=[target])
            y = df[target]
            X = pd.get_dummies(X, drop_first=True)
            if y.dtype == "object":
                y = y.fillna("missing")
                y = pd.factorize(y)[0]
            results = train_models(X, y)
            if not results:
                st.error("No models could be trained")
                st.stop()
            results_df = results_to_df(results)
            st.subheader("📊 Model Performance")
            st.dataframe(results_df)
            fig = px.bar(results_df, x="Model", y="Score", title="Model Comparison")
            st.plotly_chart(fig, use_container_width=True)
            csv_results = results_df.to_csv(index=False).encode('utf-8')
            st.download_button("⬇️ Download Model Results", csv_results, "model_results.csv", "text/csv")
            try:
                best_model, best_score = get_best_model(results)
                st.success(f"🏆 Best Model: {best_model}")
                st.info(f"Score: {best_score}")
            except:
                st.warning("Could not determine best model due to errors")
st.markdown("---")
st.markdown("🚀 Built with Streamlit | Smart Data Analyst Tool")