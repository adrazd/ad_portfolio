from plotly.graph_objs import Figure
from IPython.display import Image, display


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
