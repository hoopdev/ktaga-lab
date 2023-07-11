import hvplot
import plotly.graph_objects as go


def hv2plotly(plot, layout=None, trace_info=None, renderer="jupyterlab"):
    hvplot.output(backend="plotly")
    fig_hv = hvplot.render(plot)
    fig = go.Figure(fig_hv)
    default_layout = dict(
        template="simple_white",
        font=dict(family="Arial, monospace", size=30, color="Black"),
        margin=dict(l=100, r=25, t=25, b=100),
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
    if trace_info is not None:
        fig.update_trace(trace_info)
    if renderer is not None:
        fig.show(renderer=renderer)
    return fig
