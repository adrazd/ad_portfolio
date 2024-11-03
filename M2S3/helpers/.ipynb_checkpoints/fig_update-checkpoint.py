import plotly.express as px

def fig_update(
    fig,
    plot_title: str,
    plot_subtitle: str,
    x_title: str,
    y_title: str,
    legend_title: str = "Legend", 
    plot_width: int = 1000,
    plot_height: int = 400
):
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