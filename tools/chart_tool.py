import os
import plotly.express as px
import plotly.graph_objects as go


class ChartTool:

    def __init__(self):
        self.output_dir = "charts"
        os.makedirs(self.output_dir, exist_ok=True)

    # ======================================================
    # Save Chart
    # ======================================================

    def _save(self, fig, filename):

        path = os.path.join(self.output_dir, filename)

        fig.write_html(path)

        return {
            "figure": fig,
            "path": path
        }

    # ======================================================
    # Bar Chart
    # ======================================================

    def bar_chart(self, df, x, y, title="Bar Chart"):

        fig = px.bar(
            df,
            x=x,
            y=y,
            title=title,
            text_auto=".2s"
        )

        return self._save(fig, "bar_chart.html")

    # ======================================================
    # Line Chart
    # ======================================================

    def line_chart(self, df, x, y, title="Line Chart"):

        fig = px.line(
            df,
            x=x,
            y=y,
            title=title,
            markers=True
        )

        return self._save(fig, "line_chart.html")

    # ======================================================
    # Pie Chart
    # ======================================================

    def pie_chart(self, df, names, values, title="Pie Chart"):

        fig = px.pie(
            df,
            names=names,
            values=values,
            title=title,
            hole=0.35
        )

        return self._save(fig, "pie_chart.html")

    # ======================================================
    # Scatter Plot
    # ======================================================

    def scatter_chart(self, df, x, y, title="Scatter Plot"):

        fig = px.scatter(
            df,
            x=x,
            y=y,
            title=title,
            trendline="ols"
        )

        return self._save(fig, "scatter_plot.html")

    # ======================================================
    # Histogram
    # ======================================================

    def histogram(self, df, x, title="Histogram"):

        fig = px.histogram(
            df,
            x=x,
            title=title
        )

        return self._save(fig, "histogram.html")

    # ======================================================
    # Box Plot
    # ======================================================

    def box_plot(self, df, x, y, title="Box Plot"):

        fig = px.box(
            df,
            x=x,
            y=y,
            title=title
        )

        return self._save(fig, "box_plot.html")

    # ======================================================
    # Heatmap
    # ======================================================

    def heatmap(self, correlation_df, title="Correlation Heatmap"):

        fig = px.imshow(
            correlation_df,
            text_auto=True,
            aspect="auto",
            title=title
        )

        return self._save(fig, "heatmap.html")

    # ======================================================
    # Treemap
    # ======================================================

    def treemap(self, df, path, values, title="Treemap"):

        fig = px.treemap(
            df,
            path=path,
            values=values,
            title=title
        )

        return self._save(fig, "treemap.html")

    # ======================================================
    # Sunburst
    # ======================================================

    def sunburst(self, df, path, values, title="Sunburst"):

        fig = px.sunburst(
            df,
            path=path,
            values=values,
            title=title
        )

        return self._save(fig, "sunburst.html")

    # ======================================================
    # Area Chart
    # ======================================================

    def area_chart(self, df, x, y, title="Area Chart"):

        fig = px.area(
            df,
            x=x,
            y=y,
            title=title
        )

        return self._save(fig, "area_chart.html")

    # ======================================================
    # Violin Plot
    # ======================================================

    def violin_plot(self, df, x, y, title="Violin Plot"):

        fig = px.violin(
            df,
            x=x,
            y=y,
            title=title,
            box=True
        )

        return self._save(fig, "violin_plot.html")

    # ======================================================
    # Waterfall
    # ======================================================

    def waterfall(self, labels, values, title="Waterfall"):

        fig = go.Figure(
            go.Waterfall(
                x=labels,
                y=values
            )
        )

        fig.update_layout(title=title)

        return self._save(fig, "waterfall.html")