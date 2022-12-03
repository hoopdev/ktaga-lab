import hvplot
import plotly.graph_objects as go


def hv2plotly(plot, layout=None, renderer="jupyterlab"):
    hvplot.output(backend="plotly")
    fig_hv = hvplot.render(plot)
    fig = go.Figure(fig_hv)
    default_layout = dict(
        template="simple_white",
        font=dict(family="Arial, monospace", size=20, color="Black"),
        xaxis=dict(
            ticks="inside",
            mirror="all",
            showgrid=True,
        ),
        yaxis=dict(
            ticks="inside",
            mirror="all",
            showgrid=True,
        ),
    )
    fig.update_layout(default_layout)
    if layout is not None:
        fig.update_layout(layout)
    if renderer is not None:
        fig.show(renderer=renderer)
    return fig
