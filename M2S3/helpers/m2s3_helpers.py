import pandas as pd
import plotly.express as px
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.graph_objs import Figure
from IPython.display import Image, Markdown, display
from plotly.subplots import make_subplots


def fig_px_render(fig_input: Figure, method: str, fig_name: str = "figure") -> None:
    """
    Render a Plotly figure based on the specified method.

    Parameters:
    - fig_input: Plotly Figure object to render.
    - method: The method of rendering ('export', 'github', or 'interactive').
    - name: Optional name for the saved image file (default is "figure").

    The function saves the figure as an image, displays the image,
    or shows the interactive figure based on the specified method.
    """

    image_file = f"images/{fig_name}.png"

    if method == "export":
        fig_input.write_image(image_file, engine="kaleido")
    elif method == "github":
        display(Image(image_file))
    elif method == "interactive":
        fig_input.show()


def fig_update(
    fig,
    plot_title: str,
    plot_subtitle: str,
    x_title: str,
    y_title: str,
    legend_title: str = "Legend",
    plot_width: int = 1000,
    plot_height: int = 400,
) -> Figure:
    """
    The function conveniently updates most of plots drawn by
    plotly.express with:

    Parameters:
    - fig: Plotly Figure object to update.
    - plot_title: Title of the plot.
    - plot_subtitle: Subtitle of the plot.
    - x_title: Title of the x-axis.
    - y_title: Title of the y-axis.
    - legend_title: Title for the legend (default is "Legend").
    - plot_width: width of the plot (default is 1000).
    - plot_height: height of the plot (default is 400).

    Returns:
    - Updated Plotly Figure object.
    """
    fig.update_layout(
        title_text=plot_title,
        title_x=0.5,
        title_font_size=20,
        annotations=[
            dict(
                text=plot_subtitle,
                xref="paper",
                yref="paper",
                x=0.5,
                y=-0.27,
                showarrow=False,
                font=dict(size=16, color="black"),
            )
        ],
        xaxis_title=x_title,
        yaxis_title=y_title,
        legend_title_text=legend_title,
        autosize=False,
        width=plot_width,
        height=plot_height,
    )
    return fig


def any_outliers_iqr(
    df: pd.DataFrame, col_name: str, print_flag: bool = True
) -> pd.DataFrame:
    """
    This function uses IQR method for identification of outliers in a column of DataFrame.

    Parameters:
    df          pd.DataFrame    The DataFrame where we are looking for outliers
    col_name    str             column of the DataFrame in which we are looking for outliers
    print_flag  bool            flag, indicating whether to print outlier information

    Returns:
    df_outliers pd.DataFrame    Prints text message for user if there are any top or bottom
                                outliers in the specified column. Returns a DataFrame with
                                all outliers from initial DataFrame.
    """
    df_outliers = pd.DataFrame()

    min_value = df[col_name].min()
    max_value = df[col_name].max()

    q1 = df[col_name].quantile(0.25)
    q3 = df[col_name].quantile(0.75)

    iqr = q3 - q1

    bottom_limit = round(q1 - 1.5 * iqr, 6)
    top_limit = round(q3 + 1.5 * iqr, 6)

    if bottom_limit <= min_value and top_limit >= max_value:
        print(f"There are no outliers in '{col_name}'.") if print_flag else None

    if bottom_limit > min_value:
        lower_rows = df[df[col_name] < bottom_limit]
        lower_count = lower_rows.shape[0]
        (
            print(
                f"There are {int(lower_count)} bottom outliers in '{col_name}' below {bottom_limit}"
            )
            if print_flag
            else None
        )
        df_outliers = pd.concat([df_outliers, lower_rows])

    if top_limit < max_value:
        upper_rows = df[df[col_name] > top_limit]
        upper_count = upper_rows.shape[0]
        (
            print(
                f"There are {int(upper_count)} top outliers in '{col_name}' above {top_limit}"
            )
            if print_flag
            else None
        )

        df_outliers = pd.concat([df_outliers, upper_rows])

    df_output = df_outliers.sort_values(by=col_name, ascending=False)

    return df_output


def hist_box_eda(
    df,
    feature,
    x_title,
    sub_title,
    render_mode,
    title_mod="",
    stat_print=True,
    custom_low=0.00,
    custom_high=0.00,
    custom_flag=False,
):
    """
    The function renders a plotly histogram and prints statistical summary of a feature

    Parameters:
    df           pandas dataframe
    feature      column in the dataframe
    x_title      title of x axis
    sub_title    plot subtitle (usually number of figure, e.g. Fig.11)
    render_mode  an argument passed to another function, switch for rendering plotly charts
                 interactively, export to .png or display static image
    title_mod    modification of plot title in case it needs to be modified
    stat_print   flag for statistical summary printing, default is 'True'
    custom_low   custom lower bound for box plot line, default is 0.00
    custom_high  custom upper bound for box plot line, default is 0.00
    custom_flag  boolean flag for adding custom lines, default is 'False'
    """
    hist = px.histogram(df, x=feature, nbins=30)
    box = px.box(df, x=feature, orientation="h")

    fig = make_subplots(
        rows=2, cols=1, shared_xaxes=True, row_heights=[0.9, 0.1], vertical_spacing=0.05
    )

    for trace in hist.data:
        fig.add_trace(trace, row=1, col=1)

    for trace in box.data:
        fig.add_trace(trace, row=2, col=1)

    if custom_flag:
        fig.add_vline(x=custom_low, line=dict(color="red"), row=2, col=1)
        fig.add_vline(x=custom_high, line=dict(color="red"), row=2, col=1)
        fig.add_trace(
            go.Scatter(
                x=[None],
                y=[custom_low],
                mode="lines",
                line=dict(color="red", dash="longdash"),
                name="typical levels",
                showlegend=True,
            )
        )

    fig.update_xaxes(title_text=x_title, row=2, col=1, title_standoff=0)

    fig_update(
        fig,
        f"Distribution of {feature.title() if feature != 'pH' else feature} {title_mod}",
        f"<i>{sub_title}</i>",
        "",
        "Count",
        "",
        800,
        400,
    )

    fig_px_render(fig, render_mode, sub_title.replace(".", ""))

    feature_description = pd.DataFrame(df[feature].describe()).round(3)
    print("\n", feature_description.T, "\n", sep="") if stat_print else None


def corr_bar(df, col):
    """
    The function prints a styled sorted correlation bar with strongest
    positive correlation on the left and strongest negative on the
    right
    """
    corr_col = pd.DataFrame(df[col])
    corr_col = corr_col.drop(col, axis=0)

    styled_df = (
        corr_col.sort_values(by=col, ascending=False)
        .T.style.background_gradient(cmap="coolwarm", axis=None)
        .format("{:.3f}")
        .set_table_attributes('style="width: 55%;"')
        .set_table_styles(
            [
                {
                    "selector": "th",
                    "props": [("white-space", "normal"), ("width", "50px")],
                },
                {"selector": "td", "props": [("width", "50px")]},
            ]
        )
    )

    html = styled_df.to_html()

    display(Markdown(html))
