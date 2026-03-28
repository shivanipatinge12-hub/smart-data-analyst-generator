import plotly.express as px
def get_column_types(df):
    num_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    cat_cols = df.select_dtypes(include=['object']).columns.tolist()
    return num_cols, cat_cols
def histogram(df, column):
    fig = px.histogram(
        df,
        x=column,
        title=f"Distribution of {column}"
    )
    return fig
def kde_plot(df, column):
    fig = px.histogram(
        df,
        x=column,
        histnorm="density",
        marginal="box",
        title=f"KDE Plot of {column}"
    )
    return fig
def bar_chart(df, column):
    count_df = df[column].value_counts().reset_index()
    count_df.columns = [column, "Count"]

    fig = px.bar(
        count_df,
        x=column,
        y="Count",
        title=f"Count of {column}"
    )
    return fig
def scatter_plot(df, x, y):
    fig = px.scatter(
        df,
        x=x,
        y=y,
        title=f"{x} vs {y}"
    )
    return fig
def box_plot(df, column):
    fig = px.box(
        df,
        y=column,
        title=f"Outliers in {column}"
    )
    return fig
def correlation_heatmap(df):
    num_df = df.select_dtypes(include=['int64', 'float64'])

    if num_df.shape[1] < 2:
        return None

    corr = num_df.corr()

    fig = px.imshow(
        corr,
        text_auto=True,
        title="Correlation Heatmap"
    )
    return fig
def heatmap(df):
    num_df = df.select_dtypes(include=['int64', 'float64'])

    if num_df.shape[1] < 2:
        return None

    corr = num_df.corr()

    fig = px.imshow(
        corr,
        text_auto=True,
        color_continuous_scale="RdBu",
        title="🔥 Heatmap"
    )
    return fig
def generate_plot(df, plot_type, column=None, x=None, y=None):
    num_cols, cat_cols = get_column_types(df)
    if plot_type == "Histogram":
        if column in num_cols:
            return histogram(df, column)
        else:
            return "Histogram works only for numeric columns"
    elif plot_type == "KDE Plot":   # ✅ NEW
        if column in num_cols:
            return kde_plot(df, column)
        else:
            return "KDE works only for numeric columns"
    elif plot_type == "Bar Chart":
        if column in cat_cols:
            return bar_chart(df, column)
        else:
            return "Bar chart works only for categorical columns"
    elif plot_type == "Scatter":
        if x in num_cols and y in num_cols:
            return scatter_plot(df, x, y)
        else:
            return "Scatter plot needs numeric columns"
    elif plot_type == "Box Plot":
        if column in num_cols:
            return box_plot(df, column)
        else:
            return "Box plot works only for numeric columns"
    elif plot_type == "Heatmap":
        fig = heatmap(df)
        if fig:
            return fig
        else:
            return "Not enough numeric columns"
    elif plot_type == "Correlation":
        fig = correlation_heatmap(df)
        if fig:
            return fig
        else:
            return "Not enough numeric columns for correlation"
    return None