import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from IPython.display import Image, Markdown, display
from plotly.graph_objs import Figure
from plotly.subplots import make_subplots
from scipy import stats
from sklearn.model_selection import GridSearchCV
from statsmodels.stats.proportion import proportions_ztest
from typing import Any, Dict, Tuple


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


def hist_box_eda(
    df: pd.DataFrame,
    feature: str,
    x_title: str,
    sub_title: str,
    render_mode: str,
    title_mod: str = "",
    stat_print: bool = True,
    custom_low: float = 0.00,
    custom_high: float = 0.00,
    custom_flag: bool = False,
) -> None:
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
    hist = px.histogram(df, x=feature, nbins=50)
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
    print("\n", feature_description, "\n", sep="") if stat_print else None


def ttest_with_assumptions_check(df: pd.DataFrame, feature: str, target: str) -> None:
    """The function formulates hypotheses and conducts statistical tests
    for comparison of means of a feature's distributions for binary
    target's values:
        - checks distribution normality and variance homogeneity
        - conducts Student's t-test if variances are homogenous
        - conducts Welch's t-test if variances are not homogenous
        - outputs results of all tests.

    Parameters:
    df           Pandas datafrade with data
    feature      feature for which the tests will be conducted
    target       binary target feature for distinction of distributions

    Returns:
    None.
    """
    distribution_0 = df[df[target] == 0][feature]
    distribution_1 = df[df[target] == 1][feature]
    distributions = [distribution_0, distribution_1]

    for i, dist in enumerate(distributions):
        display(
            Markdown(
                f"""**Normality Test for "{feature}" where "{target}" = {i}:**  
        H₀: The distribution of "{feature}" for "{target}" = {i} is normal.  
        H₁: The distribution of "{feature}" for "{target}" = {i} is not normal."""
            )
        )

        shapiro = stats.shapiro(dist)
        display(
            Markdown(
                f"Shapiro-Wilk test statistic: {shapiro.statistic:.4f}, p-value: {shapiro.pvalue:.4e}"
            )
        )
        if shapiro.pvalue < 0.05:
            display(
                Markdown(
                    "**Conclusion:** `Reject` H₀. The distribution is `not normal`."
                )
            )
        else:
            display(
                Markdown(
                    "**Conclusion:** Fail to reject H₀. The distribution is normal."
                )
            )

    display(
        Markdown(
            f"""<br>**Homogeneity of Variances Test for "{feature}":**  
    H₀: The variances of "{feature}" for the two groups are equal.  
    H₁: The variances of "{feature}" for the two groups are not equal."""
        )
    )

    levene = stats.levene(distribution_0, distribution_1)
    display(
        Markdown(
            f"Levene's test statistic: {levene.statistic:.4f}, p-value: {levene.pvalue:.4e}"
        )
    )
    if levene.pvalue < 0.05:
        display(Markdown("**Conclusion:** `Reject` H₀. The variances are `not equal`."))
    else:
        display(Markdown("**Conclusion:** Fail to reject H₀. The variances are equal."))

    display(
        Markdown(
            f"""<br>**T-Test for Means of "{feature}":**  
    H₀: The means of "{feature}" for the two groups are equal.  
    H₁: The means of "{feature}" for the two groups are not equal."""
        )
    )

    t_stat, p_value = stats.ttest_ind(
        distribution_0, distribution_1, equal_var=(levene.pvalue >= 0.05)
    )
    display(Markdown(f"T-test statistic: {t_stat:.4f}, p-value: {p_value:.4e}"))
    if p_value < 0.05:
        display(
            Markdown(
                "**Conclusion:** `Reject` H₀. There is a `significant difference` in means."
            )
        )
    else:
        display(
            Markdown(
                "**Conclusion:** Fail to reject H₀. No significant difference in means."
            )
        )


def local_conversion_rate_scatter(
    df: pd.DataFrame,
    local_feature: str,
    x_title: str,
    target_feature: str,
    overall_conversion_rate: float,
    sub_title: str,
    render_mode: str,
) -> None:
    """The function creates and renders a scatterplot of local conversion rates
    of target feature per bin of a feature and adds a horizontal line of
    overall conversion rate for comparison.

    Parameters:
    df                       Pandas dataframe with data
    local_feature            name of feature to plot local conversion rates
    x_title                  title of x axis
    target_feature           name of target feature to calculate conversion rates
    overall_conversion_rate  calculated overall conversion rate
    sub_title                plot subtitle (e.g. "Fig.1")
    render_mode              method of rendering (interactive or static plot)

    Returns:
    None
    """
    local_conversion = (
        df.groupby(local_feature)[target_feature]
        .mean()
        .reset_index()
        .rename(columns={target_feature: "ConversionRate"})
    )

    fig = px.scatter(
        local_conversion,
        x=local_feature,
        y="ConversionRate",
    )

    fig.update_traces(marker=dict(size=8))

    fig_update(
        fig,
        f"Local Conversion Rates of {local_feature} vs Overall Conversion Rate",
        f"<i>{sub_title}</i>",
        x_title,
        "Conversion Rate",
        "",
        800,
        400,
    )

    fig.add_hline(
        y=overall_conversion_rate,
        line_dash="dash",
        line_color="green",
        annotation_text=f"Overall Conversion Rate: {overall_conversion_rate:.4f}",
        annotation_position="top right",
    )

    fig_px_render(fig, render_mode, sub_title.replace(".", ""))


def ztest_proportions_of_1(df: pd.DataFrame, feature: str, target: str) -> None:
    """
    Perform a Z-test for proportions of value 1 across two groups defined by a binary feature.

    Args:
        df (DataFrame): The dataset.
        feature (str): The binary feature to test ("Yes"/"No").
        target (str): The binary target variable for purchasing insurance (0/1).

    Returns:
        None. Displays results using Markdown.
    """
    group_yes = df[df[feature] == "Yes"]
    group_no = df[df[feature] == "No"]

    yes_1 = (group_yes[target] == 1).sum()
    no_1 = (group_no[target] == 1).sum()
    total_yes = len(group_yes)
    total_no = len(group_no)

    display(
        Markdown(
            f"""**Proportion Test for "{target}" = 1 proportions in "{feature}":**<br>
                H₀: The proportion of 1 in "{target}" is equal for "{feature}" = "Yes" and "{feature}" = "No".<br>
                H₁: The proportions are different."""
        )
    )

    count = np.array([yes_1, no_1])
    nobs = np.array([total_yes, total_no])
    z_stat, p_value = proportions_ztest(count, nobs)

    display(Markdown(f"Z-test statistic: {z_stat:.4f}, p-value: {p_value:.4e}"))

    if p_value < 0.05:
        display(
            Markdown(
                f"**Conclusion:** `Reject` H₀. There is a `significant difference` in the proportions between the two groups.<br><br>"
            )
        )
    else:
        display(
            Markdown(
                f"**Conclusion:** Fail to reject H₀. There is no significant difference in the proportions between the two groups.<br><br>"
            )
        )


def best_tuned_model(
    estimator_pipe: Any,
    param_grid: Dict[str, Any],
    cv: int,
    X_vars: pd.DataFrame,
    y_array: pd.Series,
    models_df: pd.DataFrame,
    model: str,
    tuned_models_dict: Dict[str, Any],
) -> Tuple[Dict[str, Any], pd.DataFrame]:
    """
    The function searches for best hyperparameters for a model and prints them out.
    Calculates best score for the minority class (PR AUC) and standard eviation of the score.
    Adds score and standar deviation to a dataframe for future reference.
    Adds the tuned best model to a dict for future use.

    Params:
    estimator_pipe    Estimator (model or pipeline) for tuning
    param_grid        Grid of hyper parameters to be tuned
    cv                Cross validation folds
    X_vars            Independent variables subset
    y_array           Target variable array
    models_df         DataFrame with list of models, their scores and std
    model             Reference name of a model
    tuned_models_dict Dict with tuned models

    Returns:
    tuned_models_dict Dict with tuned models appended with current model tuned
    models_df         DataFrame with models, their scores and std, appended with
                      relevant information

    """
    grid_search = GridSearchCV(
        estimator=estimator_pipe,
        param_grid=param_grid,
        cv=cv,
        n_jobs=-1,
        verbose=1,
        scoring="average_precision",
    )

    grid_search.fit(X_vars, y_array)

    print("Best hyperparameters:", grid_search.best_params_)
    print("Best score:", grid_search.best_score_.round(6))

    std_test_scores = grid_search.cv_results_["std_test_score"]
    best_index = grid_search.best_index_

    print("Best score STD:", std_test_scores[best_index].round(6))

    models_df.loc[
        models_df["Model"] == model, ["Tuned Best Mean", "Tuned Best STD"]
    ] = [grid_search.best_score_.round(6), std_test_scores[best_index].round(6)]

    tuned_models_dict[model] = grid_search.best_estimator_

    return tuned_models_dict, models_df
