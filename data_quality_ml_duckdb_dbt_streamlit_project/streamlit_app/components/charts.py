import plotly.express as px


def line_chart(df, x, y, color=None, title=None):
    fig = px.line(df, x=x, y=y, color=color, title=title)
    fig.update_layout(margin=dict(l=10, r=10, t=40, b=10))
    return fig


def histogram(df, column, title=None):
    fig = px.histogram(df, x=column, nbins=30, title=title)
    fig.update_layout(margin=dict(l=10, r=10, t=40, b=10))
    return fig


def box_plot(df, y, x=None, title=None):
    fig = px.box(df, x=x, y=y, title=title)
    fig.update_layout(margin=dict(l=10, r=10, t=40, b=10))
    return fig


def scatter(df, x, y, color=None, title=None, size=None):
    fig = px.scatter(df, x=x, y=y, color=color, title=title, size=size)
    fig.update_layout(margin=dict(l=10, r=10, t=40, b=10))
    return fig


def heatmap(corr, title=None):
    fig = px.imshow(corr, text_auto=True, aspect="auto", title=title)
    fig.update_layout(margin=dict(l=10, r=10, t=40, b=10))
    return fig
