import marimo

__generated_with = "0.19.4"
app = marimo.App(
    width="medium",
    app_title="Capacity Management",
    layout_file="layouts/capacity.slides.json",
    css_file="d3.css",
)


@app.cell(hide_code=True)
def _():
    # Import required libraries
    import marimo as mo
    import altair as alt
    import polars as pl
    import numpy as np
    import math
    import warnings
    warnings.filterwarnings("ignore", message=".*narwhals.*is_pandas_dataframe.*")
    return alt, math, mo, np, pl


@app.cell(hide_code=True)
def _(mo):
    # Slide classes for consistent presentation layout
    from dataclasses import dataclass
    from typing import Optional as _Optional
    import html as _html

    # Slide constants
    SLIDE_WIDTH = 1280
    SLIDE_HEIGHT = 720
    GAP = 24
    PADDING_X = 24
    PADDING_Y = 16
    TITLE_FONT_SIZE = 28
    FOOTER_FONT_SIZE = 12

    @dataclass
    class Slide:
        title: str
        chair: str
        course: str
        presenter: str
        logo_url: _Optional[str]
        page_number: int
        layout_type: str = "side-by-side"
        subtitle: _Optional[str] = None
        content1: _Optional[mo.core.MIME] = None
        content2: _Optional[mo.core.MIME] = None

        def _header(self) -> mo.core.MIME:
            safe_title = _html.escape(self.title)
            return mo.Html(
                f"""
                <div class="slide-header">
                  <div class="slide-title" style="font-size: {TITLE_FONT_SIZE}px; font-weight: 700; line-height: 1.2; margin: 0;">{safe_title}</div>
                  <div class="slide-hr" style="height: 1px; background: #E5E7EB; margin: 8px 0;"></div>
                </div>
                """
            )

        def _footer(self) -> mo.core.MIME:
            safe_page = _html.escape(str(self.page_number))
            safe_chair = _html.escape(self.chair)
            left_html = f"Page {safe_page} &nbsp;&nbsp;|&nbsp;&nbsp; {safe_chair}"
            center_img = (
                f'<img class="slide-logo" src="{_html.escape(self.logo_url)}" alt="logo" style="display: block; max-height: 28px; max-width: 160px; margin: 0 auto; object-fit: contain;">'
                if self.logo_url else "&nbsp;"
            )
            return mo.Html(
                f"""
                <div class="slide-footer">
                  <div class="slide-hr" style="height: 1px; background: #E5E7EB; margin: 8px 0;"></div>
                  <div class="slide-footer-row" style="display: grid; grid-template-columns: 1fr auto 1fr; align-items: center;">
                    <div class="slide-footer-left" style="font-size: {FOOTER_FONT_SIZE}px; color: #6B7280; white-space: nowrap;">{left_html}</div>
                    <div class="slide-footer-center">{center_img}</div>
                    <div class="slide-footer-right">&nbsp;</div>
                  </div>
                </div>
                """
            )

        def _title_layout(self) -> mo.core.MIME:
            safe_title = _html.escape(self.title)
            sub = f'<div class="title-slide-sub" style="font-size: 40px; margin: 0 0 16px 0; color: #374151;">{_html.escape(self.subtitle)}</div>' if self.subtitle else ""
            body = mo.Html(
                f"""
                <div class="slide-body title-center" style="flex: 1 1 auto; min-height: 0; display: flex; align-items: center; justify-content: center; height: 100%;">
                  <div class="title-stack" style="text-align: center;">
                    <div class="title-slide-title" style="font-size: 50px; font-weight: 800; margin: 0 0 8px 0;">{safe_title}</div>
                    {sub}
                    <div class="title-slide-meta" style="font-size: 30px; color: #6B7280;">{_html.escape(self.course)}</div>
                    <div class="title-slide-meta" style="font-size: 22px; color: #6B7280;">{_html.escape(self.presenter)}</div>
                  </div>
                </div>
                """
            )
            return mo.Html(
                f"""
                <div class="slide" style="width: {SLIDE_WIDTH}px; height: {SLIDE_HEIGHT}px; min-width: {SLIDE_WIDTH}px; min-height: {SLIDE_HEIGHT}px; max-width: {SLIDE_WIDTH}px; max-height: {SLIDE_HEIGHT}px; box-sizing: border-box; background: #ffffff; padding: {PADDING_Y}px {PADDING_X}px; display: flex; flex-direction: column; border-radius: 6px; box-shadow: 0 0 0 1px #f3f4f6; overflow: hidden; page-break-after: always; break-after: page;">
                  {self._header()}
                  {body}
                  {self._footer()}
                </div>
                """
            )

        def _one_column_layout(self) -> mo.core.MIME:
            content = mo.md(self.content1) if isinstance(self.content1, str) else (self.content1 or mo.md(""))
            content_wrapped = mo.vstack([content], gap=0).style({"gap": "0", "margin": "0", "padding": "0"})
            body = mo.Html(
                f"""
                <div class="slide-body" style="flex: 1 1 auto; min-height: 0; display: flex; flex-direction: column;">
                    <div class="slide-col tight-md" style="min-height: 0; overflow: auto; padding-right: 2px;">
                        <style>
                            ul, ol {{ margin-top: -0.2em !important; }}
                            .slide-col.tight-md .paragraph {{ margin-block: 0 !important; margin: 0 0 4px 0 !important; font-size: 19px !important; }}
                            .slide-col.tight-md span.paragraph {{ margin-block: 0 !important; margin: 0 0 4px 0 !important; font-size: 19px !important; }}
                            li {{ font-size: 19px !important; }}
                            li * {{ font-size: 19px !important; }}
                            /* Table styling */
                            table {{ font-size: 14px !important; width: auto !important; max-width: 100% !important; }}
                            th, td {{ font-size: 14px !important; padding: 4px 8px !important; }}
                            thead {{ font-size: 14px !important; }}
                            /* Code block styling */
                            pre {{ font-size: 12px !important; padding: 6px 10px !important; margin: 4px 0 !important; max-width: 100% !important; overflow-x: auto !important; }}
                            code {{ font-size: 12px !important; }}
                            pre code {{ font-size: 12px !important; }}
                        </style>
                        {content_wrapped}
                    </div>
                </div>
                """
            )
            return mo.Html(
                f"""
                <div class="slide" style="width: {SLIDE_WIDTH}px; height: {SLIDE_HEIGHT}px; min-width: {SLIDE_WIDTH}px; min-height: {SLIDE_HEIGHT}px; max-width: {SLIDE_WIDTH}px; max-height: {SLIDE_HEIGHT}px; box-sizing: border-box; background: #ffffff; padding: {PADDING_Y}px {PADDING_X}px; display: flex; flex-direction: column; border-radius: 6px; box-shadow: 0 0 0 1px #f3f4f6; overflow: hidden; page-break-after: always; break-after: page;">
                  {self._header()}
                  {body}
                  {self._footer()}
                </div>
                """
            )

        def _side_by_side_layout(self) -> mo.core.MIME:
            left_content = mo.md(self.content1) if isinstance(self.content1, str) else (self.content1 or mo.md(""))
            right_content = mo.md(self.content2) if isinstance(self.content2, str) else (self.content2 or mo.md(""))
            left = mo.vstack([left_content], gap=0).style({"gap": "0", "margin": "0", "padding": "0"})
            right = mo.vstack([right_content], gap=0).style({"gap": "0", "margin": "0", "padding": "0"})
            body = mo.Html(
                f"""
                <div class="slide-body" style="flex: 1 1 auto; min-height: 0; display: flex; flex-direction: column;">
                    <style>
                        ul, ol {{ margin-top: -0.2em !important; }}
                        .slide-col.tight-md .paragraph {{ margin-block: 0 !important; margin: 0 0 4px 0 !important; font-size: 19px !important; }}
                        .slide-col.tight-md span.paragraph {{ margin-block: 0 !important; margin: 0 0 4px 0 !important; font-size: 19px !important; }}
                        li {{ font-size: 19px !important; }}
                        li * {{ font-size: 19px !important; }}
                        /* Table styling */
                        table {{ font-size: 14px !important; width: auto !important; max-width: 100% !important; }}
                        th, td {{ font-size: 14px !important; padding: 4px 8px !important; }}
                        thead {{ font-size: 14px !important; }}
                        /* Code block styling */
                        pre {{ font-size: 12px !important; padding: 6px 10px !important; margin: 4px 0 !important; max-width: 100% !important; overflow-x: auto !important; }}
                        code {{ font-size: 12px !important; }}
                        pre code {{ font-size: 12px !important; }}
                    </style>
                    <div class="slide-cols" style="display: grid; grid-template-columns: 1fr 1fr; gap: {GAP}px; height: 100%; min-height: 0;">
                        <div class="slide-col tight-md" style="min-height: 0; overflow: auto; padding-right: 2px;">
                            {left}
                        </div>
                        <div class="slide-col tight-md" style="min-height: 0; overflow: auto; padding-right: 2px;">
                            {right}
                        </div>
                    </div>
                </div>
                """
            )
            return mo.Html(
                f"""
                <div class="slide" style="width: {SLIDE_WIDTH}px; height: {SLIDE_HEIGHT}px; min-width: {SLIDE_WIDTH}px; min-height: {SLIDE_HEIGHT}px; max-width: {SLIDE_WIDTH}px; max-height: {SLIDE_HEIGHT}px; box-sizing: border-box; background: #ffffff; padding: {PADDING_Y}px {PADDING_X}px; display: flex; flex-direction: column; border-radius: 6px; box-shadow: 0 0 0 1px #f3f4f6; overflow: hidden; page-break-after: always; break-after: page;">
                  {self._header()}
                  {body}
                  {self._footer()}
                </div>
                """
            )

        def _section_layout(self) -> mo.core.MIME:
            """Section/agenda separator slide with large centered section title and optional agenda."""
            safe_title = _html.escape(self.title)
            # subtitle contains the section number (e.g., "Section 1")
            section_label = f'<div style="font-size: 20px; font-weight: 600; color: #6B7280; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 12px;">{_html.escape(self.subtitle)}</div>' if self.subtitle else ""
            # content1 contains optional agenda/description
            agenda_content = ""
            if self.content1:
                agenda_html = mo.md(self.content1) if isinstance(self.content1, str) else self.content1
                agenda_content = f'<div style="margin-top: 32px; font-size: 18px; color: #4B5563; max-width: 600px; text-align: center;">{agenda_html}</div>'

            body = mo.Html(
                f"""
                <div class="slide-body section-center" style="flex: 1 1 auto; min-height: 0; display: flex; align-items: center; justify-content: center; height: 100%;">
                  <div style="text-align: center;">
                    {section_label}
                    <div style="font-size: 42px; font-weight: 700; color: #111827; margin: 0;">{safe_title}</div>
                    {agenda_content}
                  </div>
                </div>
                """
            )
            return mo.Html(
                f"""
                <div class="slide" style="width: {SLIDE_WIDTH}px; height: {SLIDE_HEIGHT}px; min-width: {SLIDE_WIDTH}px; min-height: {SLIDE_HEIGHT}px; max-width: {SLIDE_WIDTH}px; max-height: {SLIDE_HEIGHT}px; box-sizing: border-box; background: #ffffff; padding: {PADDING_Y}px {PADDING_X}px; display: flex; flex-direction: column; border-radius: 6px; box-shadow: 0 0 0 1px #f3f4f6; overflow: hidden; page-break-after: always; break-after: page;">
                  {body}
                  {self._footer()}
                </div>
                """
            )

        def render(self) -> mo.core.MIME:
            if self.layout_type == "title":
                return self._title_layout()
            elif self.layout_type == "section":
                return self._section_layout()
            elif self.layout_type == "1-column":
                return self._one_column_layout()
            return self._side_by_side_layout()

    class SlideCreator:
        def __init__(self, chair: str, course: str, presenter: str, logo_url: _Optional[str] = None):
            self.chair = chair
            self.course = course
            self.presenter = presenter
            self.logo_url = logo_url
            self._page_counter = 0

        def styles(self) -> mo.core.MIME:
            return mo.Html(
                f"""
                <style>
                  :root {{
                    --slide-w: {SLIDE_WIDTH}px;
                    --slide-h: {SLIDE_HEIGHT}px;
                    --gap: {GAP}px;
                    --pad-x: {PADDING_X}px;
                    --pad-y: {PADDING_Y}px;
                    --title-size: {TITLE_FONT_SIZE}px;
                    --footer-size: {FOOTER_FONT_SIZE}px;
                    --border-color: #E5E7EB;
                    --text-muted: #6B7280;
                    --bg: #ffffff;
                  }}
                  div.slide, .slide {{
                    width: var(--slide-w) !important;
                    height: var(--slide-h) !important;
                    min-width: var(--slide-w) !important;
                    min-height: var(--slide-h) !important;
                    max-width: var(--slide-w) !important;
                    max-height: var(--slide-h) !important;
                    box-sizing: border-box !important;
                    background: var(--bg) !important;
                    padding: var(--pad-y) var(--pad-x) !important;
                    display: flex !important;
                    flex-direction: column !important;
                    border-radius: 6px;
                    box-shadow: 0 0 0 1px #f3f4f6;
                    overflow: hidden !important;
                  }}
                  div.slide-title, .slide-title {{
                    font-size: var(--title-size) !important;
                    font-weight: 700 !important;
                    line-height: 1.2 !important;
                    margin: 0 !important;
                  }}
                  div.slide-hr, .slide-hr {{
                    height: 1px !important;
                    background: var(--border-color) !important;
                    margin: 8px 0 !important;
                  }}
                  div.slide-body, .slide-body {{
                    flex: 1 1 auto !important;
                    min-height: 0 !important;
                    display: flex !important;
                    flex-direction: column !important;
                  }}
                  div.slide-cols, .slide-cols {{
                    display: grid !important;
                    grid-template-columns: 1fr 1fr !important;
                    gap: var(--gap) !important;
                    height: 100% !important;
                    min-height: 0 !important;
                  }}
                  div.slide-col, .slide-col {{
                    min-height: 0 !important;
                    overflow: auto !important;
                    padding-right: 2px !important;
                  }}
                  div.slide-footer div.slide-footer-row, .slide-footer .slide-footer-row {{
                    display: grid !important;
                    grid-template-columns: 1fr auto 1fr !important;
                    align-items: center !important;
                  }}
                  div.slide-footer-left, .slide-footer-left {{
                    font-size: var(--footer-size) !important;
                    color: var(--text-muted) !important;
                    white-space: nowrap !important;
                  }}
                  img.slide-logo, .slide-logo {{
                    display: block !important;
                    max-height: 28px !important;
                    max-width: 160px !important;
                    margin: 0 auto !important;
                    object-fit: contain !important;
                  }}
                  div.title-center, .title-center {{
                    display: flex !important;
                    align-items: center !important;
                    justify-content: center !important;
                    height: 100% !important;
                  }}
                  div.title-stack, .title-stack {{
                    text-align: center !important;
                  }}
                  div.title-slide-title, .title-slide-title {{
                    font-size: 40px !important;
                    font-weight: 800 !important;
                    margin: 0 0 8px 0 !important;
                  }}
                  div.title-slide-sub, .title-slide-sub {{
                    font-size: 20px !important;
                    margin: 0 0 16px 0 !important;
                    color: #374151 !important;
                  }}
                  div.title-slide-meta, .title-slide-meta {{
                    font-size: 16px !important;
                    color: var(--text-muted) !important;
                  }}
                  .tight-md p {{ margin: 0 0 4px 0 !important; }}
                  .tight-md .paragraph {{ margin-block: 0 !important; margin: 0 0 4px 0 !important; display: block !important; font-size: 19px !important; }}
                  .tight-md span.paragraph {{ margin-block: 0 !important; margin: 0 0 4px 0 !important; display: block !important; font-size: 19px !important; }}
                  ul, ol {{ margin-top: -0.2em !important; margin-bottom: 6px !important; margin-left: 1.25em !important; margin-right: 0 !important; }}
                  .tight-md li {{ margin: 2px 0 !important; font-size: 19px !important; }}
                  li {{ font-size: 19px !important; }}
                  li * {{ font-size: 19px !important; }}
                  .tight-md h1, .tight-md h2, .tight-md h3, .tight-md h4 {{ margin: 0 0 6px 0 !important; }}

                  /* Table styling for slides */
                  .slide table, .slide-col table {{
                    font-size: 14px !important;
                    width: auto !important;
                    max-width: 100% !important;
                    border-collapse: collapse !important;
                  }}
                  .slide th, .slide td, .slide-col th, .slide-col td {{
                    font-size: 14px !important;
                    padding: 4px 8px !important;
                    white-space: nowrap !important;
                  }}
                  .slide thead, .slide-col thead {{
                    font-size: 14px !important;
                  }}

                  /* Code block styling for slides */
                  .slide pre, .slide-col pre {{
                    font-size: 13px !important;
                    padding: 8px 12px !important;
                    margin: 4px 0 !important;
                    max-width: 100% !important;
                    overflow-x: auto !important;
                    white-space: pre !important;
                    box-sizing: border-box !important;
                  }}
                  .slide code, .slide-col code {{
                    font-size: 13px !important;
                  }}
                  .slide pre code, .slide-col pre code {{
                    font-size: 13px !important;
                    white-space: pre !important;
                  }}

                  /* Math display equations - consistent sizing across all views */
                  .katex-display,
                  .katex {{
                    font-size: 22px !important;
                  }}
                  .katex-display {{
                    margin: 0.5em 0 !important;
                  }}
                </style>
                """
            )

        def create_slide(self, title: str, layout_type: str = "side-by-side", page_number: _Optional[int] = None) -> Slide:
            if page_number is None:
                self._page_counter += 1
                page_number = self._page_counter
            return Slide(
                title=title,
                chair=self.chair,
                course=self.course,
                presenter=self.presenter,
                logo_url=self.logo_url,
                page_number=page_number,
                layout_type=layout_type,
            )

        def create_title_slide(self, title: str, subtitle: _Optional[str] = None, page_number: _Optional[int] = None) -> Slide:
            slide = self.create_slide(title, layout_type="title", page_number=page_number)
            slide.subtitle = subtitle
            return slide
    return (SlideCreator,)


@app.cell(hide_code=True)
def _():
    # Course metadata
    lehrstuhl = "Chair of Logistics and Quantitative Methods"
    vorlesung = "Operations Management"
    presenter = "Nikolai Stein"
    return lehrstuhl, presenter, vorlesung


@app.cell(hide_code=True)
def _(SlideCreator, lehrstuhl, presenter, vorlesung):
    # Initialize slide creator
    sc = SlideCreator(lehrstuhl, vorlesung, presenter)
    return (sc,)


@app.cell(hide_code=True)
def _(sc):
    # Title slide
    title_slide = sc.create_title_slide(
        "Capacity Management",
        subtitle="Staffing, Queues, and Trade-offs",
        page_number=1
    )
    sc.styles()
    title_slide.render()
    return


@app.cell(hide_code=True)
def _(sc):
    # Section 1 separator
    section_1 = sc.create_slide(
        "The Capacity Challenge",
        layout_type="section",
        page_number=2
    )
    section_1.subtitle = "Section 1"
    section_1.content1 = "Why do queues form? And why does it matter?"
    section_1.render()
    return


@app.cell(hide_code=True)
def _(mo, sc):
    # Slide 1.1 — Two pictures, one problem: congestion vs idle capacity
    slide_1_1 = sc.create_slide(
        "Two pictures, one problem",
        layout_type="side-by-side",
        page_number=3
    )

    IMG_PATH = "public/images"

    slide_1_1.content1 = mo.vstack([
        mo.image(f"{IMG_PATH}/pharmacy_busy.png", height=500),
        mo.md("**Flu season**")
    ], align="center")

    slide_1_1.content2 = mo.vstack([
        mo.image(f"{IMG_PATH}/pharmacy_empty.png", height=500),
        mo.md("**Quiet afternoon**")
    ], align="center")

    slide_1_1.render()
    return


@app.cell(hide_code=True)
def _(mo, sc):
    # Slide 1.1b — Discussion prompt
    slide_1_1b = sc.create_slide(
        "Both settings lead to costs of mismatched capacity",
        layout_type="side-by-side",
        page_number=4
    )

    slide_1_1b.content1 = mo.md(
        """
        **Busy pharmacy (left picture)**

        - Lost time, frustration
        - Potential walkouts (lost sales)
        - Staff stressed, errors more likely

        **Cost:** Customer waiting time + service quality risk
        """
    )

    slide_1_1b.content2 = mo.md(
        """
        **Empty pharmacy (right picture)**

        - Staff idle, no customers to serve
        - Labor cost with no output
        - Fixed costs still running

        **Cost:** Wasted capacity (labor + overhead)
        """
    )

    slide_1_1b.render()
    return


@app.cell(hide_code=True)
def _(mo, sc):
    # Slide 1.2 — The question for today
    slide_1_2 = sc.create_slide(
        "The question for today",
        layout_type="1-column",
        page_number=5
    )

    slide_1_2.content1 = mo.md(
        r"""
        **How do we choose capacity and configuration to hit a service promise at reasonable cost?**

        **The core trade-off:**
        - Too little capacity → customers wait, service suffers
        - Too much capacity → money wasted on idle resources

        **What we'll learn today:**
        1. The basic queueing model and its key metrics (λ, μ, s, ρ, L, W)
        2. What drives waiting — and why high utilization is dangerous
        3. Design levers: pooling and reducing variability
        4. How to make staffing decisions for time-varying demand

        **Our setting:** Pharmacy operations — staffing counters to serve customers
        """
    )

    slide_1_2.render()
    return


@app.cell
def _(sc):
    # Section 2 separator
    section_2 = sc.create_slide(
        "Queueing Fundamentals",
        layout_type="section",
        page_number=6
    )
    section_2.subtitle = "Section 2"
    section_2.content1 = "The building blocks: arrivals, service, utilization, and performance"
    section_2.render()
    return


@app.cell(hide_code=True)
def _(mo, sc):
    # Slide 2.1 — The basic queueing model (All variables defined here!)
    slide_2_1 = sc.create_slide(
        "The basic queueing model",
        layout_type="1-column",
        page_number=7
    )

    # Queue flow diagram using mermaid with larger size
    queue_flow = mo.mermaid(
        """
        %%{init: {'theme': 'neutral', 'themeVariables': {'fontSize': '18px'}}}%%
        flowchart LR
            A["Arrivals (λ)"] --> B["Queue"]
            B --> C["Servers (s)"]
            C --> D["Departures"]
        """
    ).style({"min-width": "600px"})

    slide_2_1.content1 = mo.vstack([
        queue_flow,
        mo.md(
            r"""
    **We can describe a simple queueing system using three parameters:**

    - **Arrival rate — $\lambda$ (lambda):** Average number of customers arriving per hour (demand intensity)

    - **Service rate — $\mu$ (mu):** Average number of customers one server can handle per hour (server speed)

    - **Servers — $s$:** Number of parallel servers (total capacity)

    **Example: Pharmacy counter**
    - On average, $\lambda = 8$ customers arrive per hour
    - One server can handle $\mu = 10$ customers per hour on average
    - We have $s = 1$ server (counter)
            """
        )
    ])

    slide_2_1.render()
    return


@app.cell(hide_code=True)
def _(mo, sc):
    # Slide 2.2 — Measuring queue performance
    slide_2_2 = sc.create_slide(
        "Measuring queue performance",
        layout_type="side-by-side",
        page_number=8
    )

    slide_2_2.content1 = mo.md(
        r"""
        **What do we want to know about a queue?**

        From the **system perspective:**
        - **Capacity** — Maximum customers we can serve per hour
        - **Utilization ($\rho$)** — How busy are the servers?

        From the **customer perspective:**
        - **$W$** — Average time in the system (waiting + service)
        - **$W_q$** — Average time waiting in the queue

        From the **manager perspective:**
        - **$L$** — Average number of customers in the system
        - **$L_q$** — Average number of customers waiting in the queue
        """
    )

    slide_2_2.content2 = mo.md(
        r"""
        **These metrics are connected!**

        If we know some of them, we can calculate the others.

        The key relationships:
        - Capacity depends on $s$ and $\mu$
        - Utilization depends on $\lambda$, $s$, and $\mu$
        - $L$, $W$, $L_q$, $W_q$ are all related through **Little's Law**
        """
    )

    slide_2_2.render()
    return


@app.cell(hide_code=True)
def _(mo, sc):
    # Slide 2.3 — Capacity and utilization
    slide_2_3 = sc.create_slide(
        "Capacity and utilization",
        layout_type="1-column",
        page_number=9
    )

    slide_2_3.content1 = mo.md(
        r"""
    **Capacity** — Maximum throughput rate if all servers are busy
    - Formula: $\text{Capacity} = s \times \mu$
    - Example: 1 server × 10 customers/hour = 10 customers/hour capacity
    - Example: 2 servers × 10 customers/hour = 20 customers/hour capacity

    **Utilization ($\rho$)** — Fraction of time servers are busy on average
    - Formula: $\rho = \frac{\lambda}{s \times \mu} = \frac{\text{demand}}{\text{capacity}}$
    - Example: $\lambda = 8$, $\mu = 10$, $s = 1$ → $\rho = \frac{8}{10} = 80\%$
    - Interpretation: The server is busy 80% of the time
        """
    )

    slide_2_3.render()
    return


@app.cell(hide_code=True)
def _(mo, sc):
    # Slide 2.4 — Little's Law
    slide_2_4 = sc.create_slide(
        "Little's Law",
        layout_type="side-by-side",
        page_number=10
    )

    slide_2_4.content1 = mo.md(
        r"""
        **The most important formula in queueing:**

        \[
        L = \lambda \cdot W
        \]

        - **$L$** = Average number of customers in the system
        - **$\lambda$** = Arrival rate (customers per hour)
        - **$W$** = Average time in the system (hours)

        **Intuition:** If customers arrive at rate $\lambda$ and each stays $W$ time, then on average $L = \lambda W$ are present.

        **Example:** $\lambda = 8$ customers/hour, $W = 15$ minutes

        \[
        L = 8 \times \frac{15}{60} = 8 \times 0.25 = 2 \text{ customers}
        \]

        On average, 2 customers are in the system.
        """
    )

    slide_2_4.content2 = mo.md(
        r"""
        **Also works for the queue only:**

        \[
        L_q = \lambda \cdot W_q
        \]

        If average wait is $W_q = 9$ minutes:

        \[
        L_q = 8 \times \frac{9}{60} = 1.2 \text{ customers waiting}
        \]

        **Why it's powerful:**
        - Works for *any* stable queue
        - No assumptions about distributions needed
        """
    )

    slide_2_4.render()
    return


@app.cell(hide_code=True)
def _(mo, sc):
    # Slide 2.5 — Kendall notation
    slide_2_5 = sc.create_slide(
        "Classifying queues: Kendall notation",
        layout_type="side-by-side",
        page_number=11
    )

    slide_2_5.content1 = mo.md(
        r"""
        **Little's Law works for any queue.** But to calculate $W$ or $L$ directly, we need to know the distributions of arrivals and service times.

        **Kendall notation** classifies queues as **A/S/s**:

        - **A** — Arrival process distribution
        - **S** — Service time distribution
        - **s** — Number of servers

        **Common symbols:**
        - **M** = Markovian (exponential/Poisson)
        - **D** = Deterministic (constant)
        - **G** = General (any distribution)
        """
    )

    slide_2_5.content2 = mo.md(
        r"""
        **Examples:**

        | Notation | Meaning |
        |----------|---------|
        | M/M/1 | Poisson arrivals, exponential service, 1 server |
        | M/M/s | Poisson arrivals, exponential service, s servers |
        | M/D/1 | Poisson arrivals, constant service time, 1 server |
        | M/G/1 | Poisson arrivals, general service, 1 server |

        **We'll focus on M/M/1 and M/M/s** — the most common models with closed-form solutions.
        """
    )

    slide_2_5.render()
    return


@app.cell(hide_code=True)
def _(mo):
    # Sliders for slide 2.6 — M/M/1 interactive explorer
    mm1_lambda = mo.ui.slider(1, 15, value=8, label="λ (arrivals/hr)", step=1)
    mm1_mu = mo.ui.slider(5, 20, value=10, label="μ (service rate/hr)", step=1)
    return mm1_lambda, mm1_mu


@app.cell(hide_code=True)
def _(mm1_lambda, mm1_mu, mo, sc):
    # Slide 2.6 — M/M/1 formulas with interactive explorer
    slide_2_6 = sc.create_slide(
        "M/M/1: Queue metrics from steady-state solution",
        layout_type="side-by-side",
        page_number=12
    )

    slide_2_6.content1 = mo.md(
        r"""
        **For M/M/1**, we can solve for the steady-state probabilities and derive:

        | Metric | Formula |
        |--------|---------|
        | Utilization | $\rho = \frac{\lambda}{\mu}$ |
        | Avg. time in system | $W = \frac{1}{\mu - \lambda}$ |
        | Avg. queue time | $W_q = \frac{\rho}{\mu - \lambda}$ |
        | Avg. in system | $L = \frac{\rho}{1 - \rho}$ |
        | Avg. in queue | $L_q = \frac{\rho^2}{1 - \rho}$ |
        """
    )

    # Calculate M/M/1 metrics
    _lam = mm1_lambda.value
    _mu = mm1_mu.value
    _rho = _lam / _mu  # Always show utilization, even if > 100%
    _stable = _lam < _mu

    if _stable:
        _W_min = (1 / (_mu - _lam)) * 60
        _Wq_min = (_rho / (_mu - _lam)) * 60
        _L = _rho / (1 - _rho)
        _Lq = (_rho ** 2) / (1 - _rho)
        _W_str = f"{_W_min:.1f} min"
        _Wq_str = f"{_Wq_min:.1f} min"
        _L_str = f"{_L:.1f}"
        _Lq_str = f"{_Lq:.1f}"
    else:
        _W_str = "∞"
        _Wq_str = "∞"
        _L_str = "∞"
        _Lq_str = "∞"

    # Little's Law check: L = λW
    if _stable:
        _W_hours = 1 / (_mu - _lam)  # W in hours
        _L_from_littles = _lam * _W_hours
        _littles_check = f"**Little's Law check:** L = λ × W = {_lam} × {_W_hours:.3f} = {_L_from_littles:.1f} ✓"
    else:
        _littles_check = "**Little's Law check:** Not applicable (unstable)"

    slide_2_6.content2 = mo.vstack([
        mo.md("**Try it yourself:**"),
        mm1_lambda,
        mm1_mu,
        mo.md(f"""
    | Metric | Value |
    |--------|-------|
    | ρ (utilization) | {_rho:.0%} |
    | W (time in system) | {_W_str} |
    | Wq (queue time) | {_Wq_str} |
    | L (avg in system) | {_L_str} |
    | Lq (avg in queue) | {_Lq_str} |
        """),
        mo.md(_littles_check),
    ])

    slide_2_6.render()
    return


@app.cell(hide_code=True)
def _(mo):
    # Sliders for Slide 2.7 — Stability (M/M/1 context: s=1)
    stability_lambda = mo.ui.slider(5, 20, value=8, label="λ (arrivals/hr)", step=1)
    stability_mu = mo.ui.slider(5, 20, value=10, label="μ (service rate/hr)", step=1)
    return stability_lambda, stability_mu


@app.cell(hide_code=True)
def _(mo, sc, stability_lambda, stability_mu):
    # Slide 2.7 — Stability: When do queues explode?
    slide_2_7 = sc.create_slide(
        "Stability: when do queues explode?",
        layout_type="side-by-side",
        page_number=13
    )

    slide_2_7.content1 = mo.md(
        r"""
        **The stability condition**

        For a queue to be stable (not grow forever):

        $$\lambda < \mu$$

        Or equivalently:

        $$\rho < 1$$

        **If violated:** Customers arrive faster than they can be served. The queue grows without bound.

        **Key insight:** Stability tells us *if* a system can cope in the long run, but not *how well* it performs.

        Even in stable systems, customers may wait a very long time.
        """
    )

    # Interactive stability check (M/M/1: s=1)
    _rho = stability_lambda.value / stability_mu.value if stability_mu.value > 0 else float('inf')
    _stable = stability_lambda.value < stability_mu.value

    slide_2_7.content2 = mo.vstack([
        mo.md("**Interactive stability check (single server)**"),
        stability_lambda,
        stability_mu,
        mo.md(f"**Utilization:** ρ = λ/μ = {stability_lambda.value}/{stability_mu.value} = {_rho:.2f}"),
        mo.callout(
            mo.md("**STABLE** — Queue will not explode") if _stable
            else mo.md("**UNSTABLE** — Queue will grow forever!"),
            kind="success" if _stable else "danger"
        )
    ])

    slide_2_7.render()
    return


@app.cell(hide_code=True)
def _(alt, mo, np, pl, sc):
    # Slide 2.8 — The nonlinearity insight
    slide_2_8 = sc.create_slide(
        "The nonlinearity insight",
        layout_type="side-by-side",
        page_number=14
    )

    # Create data for the nonlinearity plot with all metrics for tooltip
    _mu = 10  # customers per hour
    rho_values = np.linspace(0.01, 0.99, 100)
    L_values = rho_values / (1 - rho_values)  # M/M/1 formula for L
    Lq_values = rho_values**2 / (1 - rho_values)  # M/M/1 formula for Lq
    # Little's Law: W = L/λ, Wq = Lq/λ, where λ = ρ × μ
    W_values = L_values / (rho_values * _mu) * 60  # in minutes
    Wq_values = Lq_values / (rho_values * _mu) * 60  # in minutes

    df_nonlinear = pl.DataFrame({
        "rho": np.round(rho_values, 2),
        "L": np.round(L_values, 2),
        "Lq": np.round(Lq_values, 2),
        "W": np.round(W_values, 1),
        "Wq": np.round(Wq_values, 1)
    })

    nonlinear_chart = alt.Chart(df_nonlinear.to_pandas()).mark_line(strokeWidth=3, color="#2563eb").encode(
        x=alt.X("rho:Q", title="Utilization (ρ)", scale=alt.Scale(domain=[0, 1])),
        y=alt.Y("L:Q", title="Avg customers in system (L)", scale=alt.Scale(domain=[0, 30])),
        tooltip=[
            alt.Tooltip("rho:Q", title="ρ (utilization)", format=".0%"),
            alt.Tooltip("L:Q", title="L (avg in system)"),
            alt.Tooltip("W:Q", title="W (avg time, min)"),
            alt.Tooltip("Lq:Q", title="Lq (avg in queue)"),
            alt.Tooltip("Wq:Q", title="Wq (avg wait, min)"),
        ]
    ).properties(
        width=500,
        height=350,
        title="Performance degrades nonlinearly as ρ → 1"
    )

    # Add reference points
    ref_points = pl.DataFrame({
        "rho": [0.5, 0.8, 0.9, 0.95],
        "L": [1.0, 4.0, 9.0, 19.0],
        "label": ["ρ=0.5: L=1", "ρ=0.8: L=4", "ρ=0.9: L=9", "ρ=0.95: L=19"]
    })

    points = alt.Chart(ref_points.to_pandas()).mark_point(size=100, color="red", filled=True).encode(
        x="rho:Q",
        y="L:Q"
    )

    labels = alt.Chart(ref_points.to_pandas()).mark_text(align="right", dx=-10, fontSize=12).encode(
        x="rho:Q",
        y="L:Q",
        text="label:N"
    )

    slide_2_8.content1 = mo.vstack([
        mo.ui.altair_chart(nonlinear_chart + points + labels)
    ])

    slide_2_8.content2 = mo.md(
        r"""
        **Key managerial insight**

        Running at high utilization *seems* efficient but causes waiting to explode.

        | Utilization | Avg in system | Interpretation |
        |-------------|---------------|----------------|
        | 50% | 1 customer | Plenty of slack |
        | 80% | 4 customers | Getting busy |
        | 90% | 9 customers | Congested! |
        | 95% | 19 customers | Near crisis |

        **The trade-off:**
        - **High ρ** = efficient use of servers (low cost)
        - **Low ρ** = fast service (happy customers)
        """
    )

    slide_2_8.render()
    return


@app.cell
def _(sc):
    # Section 3 separator
    section_3 = sc.create_slide(
        "Design Levers",
        layout_type="section",
        page_number=15
    )
    section_3.subtitle = "Section 3"
    section_3.content1 = "Pooling, standardization, and the efficiency-responsiveness frontier"
    section_3.render()
    return


@app.cell
def _(mo):
    # Slider for Slide 3.1 — Trade-off explorer (ρ slider for smooth curve)
    tradeoff_rho = mo.ui.slider(0.1, 0.95, value=0.5, label="ρ (utilization)", step=0.05)
    return (tradeoff_rho,)


@app.cell(hide_code=True)
def _(alt, mo, np, pl, sc, tradeoff_rho):
    # Slide 3.1 — The efficiency-responsiveness trade-off
    slide_3_1 = sc.create_slide(
        "The efficiency-responsiveness trade-off",
        layout_type="side-by-side",
        page_number=16
    )

    slide_3_1.content1 = mo.md(
        r"""
        **The fundamental trade-off**

        We've seen that high utilization causes long waits. This creates a tension:

        - **Efficiency** (high ρ): Servers busy, low labor cost per customer
        - **Responsiveness** (low ρ): Short waits, happy customers
        - **You can't maximize both!**

        **Moving along the frontier**

        Adding capacity (more servers or faster service):
        - ↓ Utilization
        - ↓ Congestion
        - ↑ Cost
        """
    )

    # Interactive trade-off plot using L (avg in system) - same curve as slide 2.8
    _mu = 10  # customers per hour
    _rho_values = np.linspace(0.01, 0.99, 100)
    _L_values = _rho_values / (1 - _rho_values)  # M/M/1 formula for L
    _Lq_values = _rho_values**2 / (1 - _rho_values)  # M/M/1 formula for Lq
    _W_values = _L_values / (_rho_values * _mu) * 60  # in minutes
    _Wq_values = _Lq_values / (_rho_values * _mu) * 60  # in minutes

    df_curve = pl.DataFrame({
        "rho": np.round(_rho_values, 2),
        "L": np.round(_L_values, 2),
        "Lq": np.round(_Lq_values, 2),
        "W": np.round(_W_values, 1),
        "Wq": np.round(_Wq_values, 1)
    })

    # Current operating point from slider
    _current_rho = tradeoff_rho.value
    _current_L = _current_rho / (1 - _current_rho)

    df_point = pl.DataFrame({
        "rho": [_current_rho],
        "L": [_current_L],
        "label": [f"ρ={_current_rho:.0%}"]
    })

    # Create the chart - same style as slide 2.8
    frontier_line = alt.Chart(df_curve.to_pandas()).mark_line(
        strokeWidth=3, color="#2563eb"
    ).encode(
        x=alt.X("rho:Q", title="Utilization (ρ)", scale=alt.Scale(domain=[0, 1])),
        y=alt.Y("L:Q", title="Avg customers in system (L)", scale=alt.Scale(domain=[0, 30])),
        tooltip=[
            alt.Tooltip("rho:Q", title="ρ (utilization)", format=".0%"),
            alt.Tooltip("L:Q", title="L (avg in system)"),
            alt.Tooltip("W:Q", title="W (avg time, min)"),
            alt.Tooltip("Lq:Q", title="Lq (avg in queue)"),
            alt.Tooltip("Wq:Q", title="Wq (avg wait, min)"),
        ]
    )

    current_point = alt.Chart(df_point.to_pandas()).mark_point(
        size=200, color="red", filled=True
    ).encode(x="rho:Q", y="L:Q")

    point_label = alt.Chart(df_point.to_pandas()).mark_text(
        align="right", dx=-10, dy=-10, fontSize=14, fontWeight="bold"
    ).encode(x="rho:Q", y="L:Q", text="label:N")

    tradeoff_chart = (frontier_line + current_point + point_label).properties(
        width=450, height=350, title="Moving along the frontier"
    )

    slide_3_1.content2 = mo.vstack([
        tradeoff_rho,
        mo.ui.altair_chart(tradeoff_chart),
        mo.md(f"**Current:** ρ={_current_rho:.0%}, L={_current_L:.1f} customers")
    ])

    slide_3_1.render()
    return


@app.cell(hide_code=True)
def _(mo, sc):
    # Slide 3.2 — Two queue configurations (discussion)
    slide_3_2 = sc.create_slide(
        "Two ways to organize queues",
        layout_type="side-by-side",
        page_number=17
    )

    # Diagram: Separate queues (one queue per server) - vertical layout, bottom aligned
    separate_queue_diagram = mo.Html("""
    <div style="font-family: sans-serif; font-size: 14px; padding: 16px; background: #f8fafc; border-radius: 8px;">
        <div style="display: flex; justify-content: space-around; align-items: flex-end; gap: 8px;">
            <!-- Queue 1 -->
            <div style="display: flex; flex-direction: column; align-items: center; gap: 4px;">
                <div style="font-size: 20px;">👤</div>
                <div style="font-size: 20px;">👤</div>
                <div style="font-size: 20px;">👤</div>
                <div style="font-size: 20px;">👤</div>
                <div style="font-size: 18px; color: #64748b;">↓</div>
                <div style="background: #22c55e; color: white; padding: 8px 12px; border-radius: 4px; font-weight: bold; font-size: 12px;">Server 1</div>
            </div>
            <!-- Queue 2 -->
            <div style="display: flex; flex-direction: column; align-items: center; gap: 4px;">
                <div style="font-size: 20px;">👤</div>
                <div style="font-size: 20px;">👤</div>
                <div style="font-size: 18px; color: #64748b;">↓</div>
                <div style="background: #22c55e; color: white; padding: 8px 12px; border-radius: 4px; font-weight: bold; font-size: 12px;">Server 2</div>
            </div>
            <!-- Queue 3 -->
            <div style="display: flex; flex-direction: column; align-items: center; gap: 4px;">
                <div style="font-size: 20px;">👤</div>
                <div style="font-size: 20px;">👤</div>
                <div style="font-size: 20px;">👤</div>
                <div style="font-size: 20px;">👤</div>
                <div style="font-size: 20px;">👤</div>
                <div style="font-size: 20px;">👤</div>
                <div style="font-size: 18px; color: #64748b;">↓</div>
                <div style="background: #22c55e; color: white; padding: 8px 12px; border-radius: 4px; font-weight: bold; font-size: 12px;">Server 3</div>
            </div>
        </div>
    </div>
    """)

    # Diagram: Pooled queue (one queue, multiple servers) - vertical layout, 2 per row
    pooled_queue_diagram = mo.Html("""
    <div style="font-family: sans-serif; font-size: 14px; padding: 16px; background: #f8fafc; border-radius: 8px;">
        <div style="display: flex; flex-direction: column; align-items: center; gap: 4px;">
            <!-- Single queue - 2 people per row -->
            <div style="display: flex; gap: 8px;"><span style="font-size: 20px;">👤</span><span style="font-size: 20px;">👤</span></div>
            <div style="display: flex; gap: 8px;"><span style="font-size: 20px;">👤</span><span style="font-size: 20px;">👤</span></div>
            <div style="display: flex; gap: 8px;"><span style="font-size: 20px;">👤</span><span style="font-size: 20px;">👤</span></div>
            <div style="display: flex; gap: 8px;"><span style="font-size: 20px;">👤</span><span style="font-size: 20px;">👤</span></div>
            <div style="display: flex; gap: 8px;"><span style="font-size: 20px;">👤</span><span style="font-size: 20px;">👤</span></div>
            <div style="display: flex; gap: 8px;"><span style="font-size: 20px;">👤</span><span style="font-size: 20px;">👤</span></div>
            <div style="font-size: 18px; color: #64748b; margin: 8px 0;">↓ ↓ ↓</div>
            <!-- Servers -->
            <div style="display: flex; gap: 8px;">
                <div style="background: #22c55e; color: white; padding: 8px 12px; border-radius: 4px; font-weight: bold; font-size: 12px;">Server 1</div>
                <div style="background: #22c55e; color: white; padding: 8px 12px; border-radius: 4px; font-weight: bold; font-size: 12px;">Server 2</div>
                <div style="background: #22c55e; color: white; padding: 8px 12px; border-radius: 4px; font-weight: bold; font-size: 12px;">Server 3</div>
            </div>
        </div>
    </div>
    """)

    slide_3_2.content1 = mo.vstack([
        mo.md("**Option A: Separate queues**"),
        separate_queue_diagram,
        mo.md("*Each server has its own line*"),
    ], align="center")

    slide_3_2.content2 = mo.vstack([
        mo.md("**Option B: Pooled queue**"),
        pooled_queue_diagram,
        mo.md("*One line feeds all servers*"),
    ], align="center")

    slide_3_2.render()
    return


@app.cell
def _(mo):
    # Checkboxes for Slide 3.2b — Compare queue configurations
    show_separate = mo.ui.checkbox(value=True, label="Separate queues (s independent M/M/1)")
    show_pooled = mo.ui.checkbox(value=False, label="Pooled queue (M/M/s)")
    return show_pooled, show_separate


@app.cell(hide_code=True)
def _(alt, math, mo, np, pl, sc, show_pooled, show_separate):
    # Slide 3.2b — Interactive comparison: separate vs pooled queues
    slide_3_2b = sc.create_slide(
        "Comparing queue configurations",
        layout_type="side-by-side",
        page_number=18
    )

    # Fixed number of servers for comparison
    s = 3  # 3 servers in both configurations

    # Helper function: Erlang-C probability (probability of waiting in M/M/s)
    def erlang_c(s, rho):
        """Calculate Erlang-C probability for M/M/s queue."""
        if rho >= 1:
            return 1.0  # Unstable
        a = s * rho  # offered load
        # Calculate P0 (probability of empty system)
        sum_term = sum((a ** k) / math.factorial(k) for k in range(s))
        last_term = (a ** s) / (math.factorial(s) * (1 - rho))
        p0 = 1.0 / (sum_term + last_term)
        # Erlang-C = probability of waiting
        c = ((a ** s) / math.factorial(s)) * (1 / (1 - rho)) * p0
        return c

    # Calculate all metrics for both configurations across ρ values
    _rho_values = np.linspace(0.05, 0.95, 50)
    _mu = 10  # Service rate (customers/hour)

    def calc_separate_metrics(rho):
        """Calculate metrics for s independent M/M/1 queues."""
        # Each queue has utilization ρ
        L = s * rho / (1 - rho)
        Lq = s * (rho ** 2) / (1 - rho)
        # Total arrival rate λ = s × ρ × μ
        lam = s * rho * _mu
        W = L / lam * 60  # in minutes
        Wq = Lq / lam * 60  # in minutes
        return L, Lq, W, Wq

    def calc_pooled_metrics(rho):
        """Calculate metrics for M/M/s pooled queue."""
        c = erlang_c(s, rho)
        Lq = c * rho / (1 - rho)
        L = Lq + s * rho  # L = Lq + average number in service
        # Total arrival rate λ = s × ρ × μ
        lam = s * rho * _mu
        W = L / lam * 60  # in minutes
        Wq = Lq / lam * 60  # in minutes
        return L, Lq, W, Wq

    # Build dataframe for plotting with all metrics
    data_rows = []
    if show_separate.value:
        for rho in _rho_values:
            L, Lq, W, Wq = calc_separate_metrics(rho)
            data_rows.append({
                "rho": round(rho, 2), "L": round(L, 2), "Lq": round(Lq, 2),
                "W": round(W, 1), "Wq": round(Wq, 1), "System": "Separate queues"
            })
    if show_pooled.value:
        for rho in _rho_values:
            L, Lq, W, Wq = calc_pooled_metrics(rho)
            data_rows.append({
                "rho": round(rho, 2), "L": round(L, 2), "Lq": round(Lq, 2),
                "W": round(W, 1), "Wq": round(Wq, 1), "System": "Pooled queue"
            })

    if data_rows:
        df_compare = pl.DataFrame(data_rows)

        comparison_chart = alt.Chart(df_compare.to_pandas()).mark_line(strokeWidth=3).encode(
            x=alt.X("rho:Q", title="Utilization (ρ)", scale=alt.Scale(domain=[0, 1])),
            y=alt.Y("L:Q", title="Avg customers in system (L)", scale=alt.Scale(domain=[0, 30])),
            color=alt.Color("System:N",
                scale=alt.Scale(
                    domain=["Separate queues", "Pooled queue"],
                    range=["#dc2626", "#2563eb"]  # Red for separate, Blue for pooled
                ),
                legend=alt.Legend(orient="bottom", title=None)
            ),
            strokeDash=alt.StrokeDash("System:N",
                scale=alt.Scale(
                    domain=["Separate queues", "Pooled queue"],
                    range=[[1, 0], [1, 0]]  # Solid lines for both
                ),
                legend=None  # Hide duplicate legend for strokeDash
            ),
            tooltip=[
                alt.Tooltip("rho:Q", title="ρ (utilization)", format=".0%"),
                alt.Tooltip("L:Q", title="L (avg in system)"),
                alt.Tooltip("W:Q", title="W (avg time, min)"),
                alt.Tooltip("Lq:Q", title="Lq (avg in queue)"),
                alt.Tooltip("Wq:Q", title="Wq (avg wait, min)"),
            ]
        ).properties(width=450, height=300, title=f"Separate vs Pooled queues (s = {s} servers)")

        chart_display = mo.ui.altair_chart(comparison_chart)
    else:
        chart_display = mo.md("*Select at least one system to display*")

    intro_text = mo.md(
        f"""
        **Same resources, different organization**

        Both systems have:
        - **{s} servers** total
        - Same arrival rate λ
        - Same service rate μ per server
        - Same utilization ρ = λ/(s·μ)

        **The only difference:** How queues are organized.
        """
    )

    math_content = mo.md(
        r"""
        *Separate queues* (s independent M/M/1):

        $$L = s \cdot \frac{\rho}{1-\rho}$$

        *Pooled queue* (M/M/s) uses the **Erlang-C formula**:

        $$L_q = C(s,\rho) \cdot \frac{\rho}{1-\rho}, \quad L = L_q + s\rho$$

        The Erlang-C term $C(s,\rho)$ is the probability of waiting.
        """
    )

    more_math_content = mo.md(
        r"""
        **The Erlang-C formula** $C(s,\rho)$ — probability that an arriving customer must wait:

        $$C(s,\rho) = \frac{\frac{(s\rho)^s}{s!} \cdot \frac{1}{1-\rho}}{\sum_{k=0}^{s-1} \frac{(s\rho)^k}{k!} + \frac{(s\rho)^s}{s!} \cdot \frac{1}{1-\rho}}$$
        """
    )

    slide_3_2b.content1 = mo.vstack([
        intro_text,
        mo.accordion({"The math": math_content, "More math (Erlang-C formula)": more_math_content})
    ])

    slide_3_2b.content2 = mo.vstack([
        mo.hstack([show_separate, show_pooled], justify="start", gap=2),
        chart_display,
        mo.accordion({"Insight": mo.md("Pooling **shifts the frontier** — same utilization, fewer customers waiting. This is a *design choice*, not a staffing decision!")})
    ])

    slide_3_2b.render()
    return


@app.cell(hide_code=True)
def _(mo, sc):
    # Slide 3.3 — Three service environments (visual comparison)
    slide_3_3 = sc.create_slide(
        "Three service environments",
        layout_type="1-column",
        page_number=19
    )

    # Visual diagrams showing service time distributions (fixed width for consistency)
    deterministic_diagram = mo.Html("""
    <div style="text-align: center; padding: 12px; background: #f0fdf4; border-radius: 8px; border: 2px solid #22c55e; width: 280px;">
        <div style="font-weight: bold; color: #166534; margin-bottom: 8px;">Standardized Process</div>
        <div style="font-size: 12px; color: #666; margin-bottom: 8px;">e.g., Self-checkout kiosk, automated pickup</div>
        <div style="display: flex; justify-content: center; align-items: flex-end; gap: 4px; height: 60px;">
            <div style="width: 20px; height: 40px; background: #22c55e;"></div>
            <div style="width: 20px; height: 40px; background: #22c55e;"></div>
            <div style="width: 20px; height: 40px; background: #22c55e;"></div>
            <div style="width: 20px; height: 40px; background: #22c55e;"></div>
            <div style="width: 20px; height: 40px; background: #22c55e;"></div>
            <div style="width: 20px; height: 40px; background: #22c55e;"></div>
        </div>
        <div style="font-size: 11px; color: #666; margin-top: 4px;">Every customer: exactly 6 min</div>
        <div style="font-weight: bold; color: #166534; margin-top: 4px;">CV = 0</div>
    </div>
    """)

    standard_diagram = mo.Html("""
    <div style="text-align: center; padding: 12px; background: #fefce8; border-radius: 8px; border: 2px solid #eab308; width: 280px;">
        <div style="font-weight: bold; color: #854d0e; margin-bottom: 8px;">Typical Service</div>
        <div style="font-size: 12px; color: #666; margin-bottom: 8px;">e.g., Regular pharmacy counter</div>
        <div style="display: flex; justify-content: center; align-items: flex-end; gap: 4px; height: 60px;">
            <div style="width: 20px; height: 25px; background: #eab308;"></div>
            <div style="width: 20px; height: 50px; background: #eab308;"></div>
            <div style="width: 20px; height: 35px; background: #eab308;"></div>
            <div style="width: 20px; height: 55px; background: #eab308;"></div>
            <div style="width: 20px; height: 30px; background: #eab308;"></div>
            <div style="width: 20px; height: 45px; background: #eab308;"></div>
        </div>
        <div style="font-size: 11px; color: #666; margin-top: 4px;">Average 6 min, moderate variation</div>
        <div style="font-weight: bold; color: #854d0e; margin-top: 4px;">CV = 1</div>
    </div>
    """)

    high_var_diagram = mo.Html("""
    <div style="text-align: center; padding: 12px; background: #fef2f2; border-radius: 8px; border: 2px solid #dc2626; width: 280px;">
        <div style="font-weight: bold; color: #991b1b; margin-bottom: 8px;">Unpredictable Service</div>
        <div style="font-size: 12px; color: #666; margin-bottom: 8px;">e.g., Mixed quick pickups + complex cases</div>
        <div style="display: flex; justify-content: center; align-items: flex-end; gap: 4px; height: 60px;">
            <div style="width: 20px; height: 10px; background: #dc2626;"></div>
            <div style="width: 20px; height: 60px; background: #dc2626;"></div>
            <div style="width: 20px; height: 15px; background: #dc2626;"></div>
            <div style="width: 20px; height: 55px; background: #dc2626;"></div>
            <div style="width: 20px; height: 8px; background: #dc2626;"></div>
            <div style="width: 20px; height: 50px; background: #dc2626;"></div>
        </div>
        <div style="font-size: 11px; color: #666; margin-top: 4px;">Average 6 min, but 1 min to 15 min range</div>
        <div style="font-weight: bold; color: #991b1b; margin-top: 4px;">CV = 1.5</div>
    </div>
    """)

    slide_3_3.content1 = mo.vstack([
        mo.md("""
        **Same average service time, different variability**

        All three environments have **mean service time = 6 minutes**. But the spread differs dramatically.

        **Coefficient of Variation (CV)** = standard deviation / mean
        """),
        mo.hstack([deterministic_diagram, standard_diagram, high_var_diagram], justify="space-around", gap=2),
    ])

    slide_3_3.render()
    return


@app.cell(hide_code=True)
def _(mo):
    # Checkboxes for Slide 3.3b — Compare variability settings
    show_cv_0 = mo.ui.checkbox(value=False, label="CV = 0 (deterministic)")
    show_cv_1 = mo.ui.checkbox(value=True, label="CV = 1 (standard)")
    show_cv_15 = mo.ui.checkbox(value=False, label="CV = 1.5 (high variability)")
    return show_cv_0, show_cv_1, show_cv_15


@app.cell(hide_code=True)
def _(alt, mo, np, pl, sc, show_cv_0, show_cv_1, show_cv_15):
    # Slide 3.3b — Variability explorer (interactive comparison)
    slide_3_3b = sc.create_slide(
        "Comparing variability levels",
        layout_type="side-by-side",
        page_number=20
    )

    # Calculate L for different CV values
    # Using: L = ρ + (ρ²/(1-ρ)) × ((CVa² + CVs²)/2)
    # Assuming CVa = 1 (Poisson arrivals), varying CVs
    rho_vals = np.linspace(0.05, 0.95, 50)
    cv_a = 1  # Fixed arrival variability (Poisson)

    def calc_L(rho, cv_s):
        """Calculate L using Kingman-based approximation."""
        variability_factor = (cv_a**2 + cv_s**2) / 2
        Lq = (rho**2 / (1 - rho)) * variability_factor
        return Lq + rho

    # Build data for plotting with all metrics for tooltip
    # Using Little's Law: W = L/λ, and λ = ρ × μ, with μ = 10/hour
    _mu = 10  # customers per hour

    def calc_all_metrics(rho, cv_s):
        """Calculate L, Lq, W, Wq using Kingman-based approximation."""
        variability_factor = (cv_a**2 + cv_s**2) / 2
        Lq = (rho**2 / (1 - rho)) * variability_factor
        L = Lq + rho
        # Little's Law: W = L/λ, Wq = Lq/λ, where λ = ρ × μ
        lam = rho * _mu
        W = L / lam * 60  # in minutes
        Wq = Lq / lam * 60  # in minutes
        return L, Lq, W, Wq

    var_data_rows = []
    if show_cv_0.value:
        for _rho in rho_vals:
            _L, _Lq, _W, _Wq = calc_all_metrics(_rho, 0)
            var_data_rows.append({"rho": round(_rho, 2), "L": round(_L, 2), "Lq": round(_Lq, 2),
                                  "W": round(_W, 1), "Wq": round(_Wq, 1), "Setting": "CV = 0 (deterministic)"})
    if show_cv_1.value:
        for _rho in rho_vals:
            _L, _Lq, _W, _Wq = calc_all_metrics(_rho, 1)
            var_data_rows.append({"rho": round(_rho, 2), "L": round(_L, 2), "Lq": round(_Lq, 2),
                                  "W": round(_W, 1), "Wq": round(_Wq, 1), "Setting": "CV = 1 (standard)"})
    if show_cv_15.value:
        for _rho in rho_vals:
            _L, _Lq, _W, _Wq = calc_all_metrics(_rho, 1.5)
            var_data_rows.append({"rho": round(_rho, 2), "L": round(_L, 2), "Lq": round(_Lq, 2),
                                  "W": round(_W, 1), "Wq": round(_Wq, 1), "Setting": "CV = 1.5 (high var)"})

    if var_data_rows:
        df_var = pl.DataFrame(var_data_rows)

        var_chart = alt.Chart(df_var.to_pandas()).mark_line(strokeWidth=3).encode(
            x=alt.X("rho:Q", title="Utilization (ρ)", scale=alt.Scale(domain=[0, 1])),
            y=alt.Y("L:Q", title="Avg customers in system (L)", scale=alt.Scale(domain=[0, 30])),
            color=alt.Color("Setting:N",
                scale=alt.Scale(
                    domain=["CV = 0 (deterministic)", "CV = 1 (standard)", "CV = 1.5 (high var)"],
                    range=["#22c55e", "#eab308", "#dc2626"]
                ),
                legend=alt.Legend(orient="bottom", title=None)
            ),
            tooltip=[
                alt.Tooltip("rho:Q", title="ρ (utilization)", format=".0%"),
                alt.Tooltip("L:Q", title="L (avg in system)"),
                alt.Tooltip("W:Q", title="W (avg time, min)"),
                alt.Tooltip("Lq:Q", title="Lq (avg in queue)"),
                alt.Tooltip("Wq:Q", title="Wq (avg wait, min)"),
            ]
        ).properties(width=450, height=300, title="Impact of service time variability")

        var_chart_display = mo.ui.altair_chart(var_chart)
    else:
        var_chart_display = mo.md("*Select at least one setting to display*")

    # Math content in accordion
    var_math_content = mo.md(
        r"""
        **Approximation for L with variability:**

        $$L \approx \rho + \frac{\rho^2}{1-\rho} \cdot \frac{CV_a^2 + CV_s^2}{2}$$

        Where:
        - $CV_a$ = coefficient of variation of arrivals (= 1 for Poisson)
        - $CV_s$ = coefficient of variation of service times

        For $CV_a = CV_s = 1$: this simplifies to $L = \frac{\rho}{1-\rho}$ (the M/M/1 formula).
        """
    )

    slide_3_3b.content1 = mo.vstack([
        mo.md(
            """
            **Same utilization, different variability**

            All settings have:
            - Same arrival rate λ
            - Same average service rate μ
            - Same utilization ρ

            **The only difference:** Service time variability (CVs)

            **Practical ways to reduce variability:**
            - Standardize processes
            - Triage customers by complexity
            - Self-service for simple cases
            - Training to reduce skill gaps
            """
        ),
        mo.accordion({"The math (Kingman approximation)": var_math_content})
    ])

    slide_3_3b.content2 = mo.vstack([
        mo.hstack([show_cv_0, show_cv_1, show_cv_15], justify="start", gap=2),
        var_chart_display,
        mo.accordion({"Insight": mo.md("Reducing variability **shifts the frontier** — less waiting at any utilization level!")})
    ])

    slide_3_3b.render()
    return


@app.cell(hide_code=True)
def _(mo, sc):
    # Slide 3.4 — Summary: Move along vs shift the frontier
    slide_3_4 = sc.create_slide(
        "Summary: move along vs shift the frontier",
        layout_type="side-by-side",
        page_number=21
    )

    slide_3_4.content1 = mo.md(
        """
        **Two ways to improve service:**

        **1. Move along the frontier** (cost ↔ service trade-off)
        - Add more staff → less waiting, more cost
        - Remove staff → more waiting, less cost
        - You're trading money for service quality

        **2. Shift the frontier** (better for same cost)
        - Pool queues → less waiting, same staff
        - Reduce variability → less waiting, same staff
        - Improve process → faster service, same staff

        **The first is a decision; the second is an improvement.**
        """
    )

    slide_3_4.content2 = mo.md(
        """
        **Frontier shifts in practice:**

        | Action | Effect |
        |--------|--------|
        | Pool separate lines | Less waiting for free |
        | Appointment scheduling | Smoother arrivals |
        | Standardize service process | Less service variability |
        | Self-service for simple tasks | Faster effective μ |

        **Key insight:**
        Before adding staff (expensive), ask:
        - Can we pool resources?
        - Can we reduce variability?
        - Can we simplify the process?
        """
    )

    slide_3_4.render()
    return


@app.cell
def _(sc):
    # Section 4 separator
    section_4 = sc.create_slide(
        "From Theory to Practice",
        layout_type="section",
        page_number=22
    )
    section_4.subtitle = "Section 4"
    section_4.content1 = "Time-varying demand and staffing decisions"
    section_4.render()
    return


@app.cell(hide_code=True)
def _(mo, sc):
    # Slide 4.1 — Arrivals vary over the day (problem setup)
    slide_4_1 = sc.create_slide(
        "Arrivals vary over the day",
        layout_type="side-by-side",
        page_number=23
    )

    slide_4_1.content1 = mo.md(
        r"""
        **Customer arrivals are not constant**

        Typical pharmacy pattern:
        - **Morning peak:** prescriptions from overnight, early shoppers
        - **Midday lull:** lunch hours
        - **Afternoon peak:** after work, school pickups

        **The key insight:**

        Our arrival rate $\lambda$ changes throughout the day.
        This is **$\lambda(t)$** — arrivals vary by time.

        **Question for you:**

        *How should we staff for this pattern?*
        """
    )

    slide_4_1.content2 = mo.md(
        """
        **Example arrival pattern (customers/hour):**

        | Time | Normal Day | Flu Season |
        |------|------------|------------|
        | 8-9am | 20 | 30 |
        | 9-10am | 25 | 40 |
        | 10-11am | 20 | 35 |
        | 11am-12pm | 15 | 25 |
        | 12-1pm | 10 | 20 |
        | 1-2pm | 15 | 25 |
        | 2-3pm | 20 | 35 |
        | 3-4pm | 25 | 40 |
        | 4-5pm | 30 | 50 |
        | 5-6pm | 25 | 40 |
        """
    )

    slide_4_1.render()
    return


@app.cell(hide_code=True)
def _(mo):
    # Slider for Slide 4.2 — Constant staff level
    constant_staff_slider = mo.ui.slider(1, 5, value=1, label="Staff level (constant all day)", step=1)
    return (constant_staff_slider,)


@app.cell(hide_code=True)
def _(alt, constant_staff_slider, math, mo, pl, sc):
    # Slide 4.2 — Can constant staffing work? (Interactive failure experience)
    slide_4_2 = sc.create_slide(
        "Can constant staffing work?",
        layout_type="1-column",
        page_number=24
    )

    # Time block data (same λ(t) pattern from 4.1)
    _time_blocks = ["8-9", "9-10", "10-11", "11-12", "12-1", "1-2", "2-3", "3-4", "4-5", "5-6"]
    _arrival_rates = [20, 25, 20, 15, 10, 15, 20, 25, 30, 25]
    _mu_rate = 10  # Service rate per server (customers/hour)

    # Calculate utilization for each block with constant staffing
    _s = constant_staff_slider.value
    _utilizations = [arr / (_s * _mu_rate) for arr in _arrival_rates]

    # M/M/s queueing metrics calculation
    def _calc_mms_metrics(lam, mu, s):
        """Calculate M/M/s queueing metrics. Returns (rho, L, W, Lq, Wq) or None if unstable."""
        rho = lam / (s * mu)
        if rho >= 1:
            return (rho, None, None, None, None)  # Unstable

        # Erlang-C formula for P0
        sum_terms = sum((s * rho) ** n / math.factorial(n) for n in range(s))
        last_term = ((s * rho) ** s) / (math.factorial(s) * (1 - rho))
        P0 = 1 / (sum_terms + last_term)

        # Lq = P0 * (s*rho)^s * rho / (s! * (1-rho)^2)
        Lq = P0 * ((s * rho) ** s) * rho / (math.factorial(s) * (1 - rho) ** 2)
        L = Lq + lam / mu
        Wq = Lq / lam * 60  # Convert to minutes
        W = Wq + (1 / mu) * 60  # Convert to minutes
        return (rho, L, W, Lq, Wq)

    _metrics = [_calc_mms_metrics(arr, _mu_rate, _s) for arr in _arrival_rates]

    _df_util = pl.DataFrame({
        "Time": _time_blocks,
        "λ (arrivals/hr)": _arrival_rates,
        "Utilization": _utilizations,
        "ρ (%)": [f"{u*100:.0f}%" for u in _utilizations],
        "L (customers)": [f"{m[1]:.1f}" if m[1] is not None else "∞" for m in _metrics],
        "W (min)": [f"{m[2]:.1f}" if m[2] is not None else "∞" for m in _metrics],
        "Lq (waiting)": [f"{m[3]:.1f}" if m[3] is not None else "∞" for m in _metrics],
        "Wq (min)": [f"{m[4]:.1f}" if m[4] is not None else "∞" for m in _metrics],
        "Status": ["Unstable" if u >= 1 else ("High" if u >= 0.85 else "OK") for u in _utilizations]
    })

    _util_chart = alt.Chart(_df_util.to_pandas()).mark_bar().encode(
        x=alt.X("Time:N", sort=_time_blocks, title="Time Block"),
        y=alt.Y("Utilization:Q", title="Utilization (ρ)", scale=alt.Scale(domain=[0, 1.5])),
        color=alt.Color("Status:N",
            scale=alt.Scale(
                domain=["OK", "High", "Unstable"],
                range=["#22c55e", "#f59e0b", "#dc2626"]  # Green, Amber, Red
            ),
            legend=alt.Legend(title="Status", orient="right")
        ),
        tooltip=[
            alt.Tooltip("Time:N", title="Time"),
            alt.Tooltip("λ (arrivals/hr):Q", title="λ (arrivals/hr)"),
            alt.Tooltip("ρ (%):N", title="ρ"),
            alt.Tooltip("L (customers):N", title="L (in system)"),
            alt.Tooltip("W (min):N", title="W (total time)"),
            alt.Tooltip("Lq (waiting):N", title="Lq (in queue)"),
            alt.Tooltip("Wq (min):N", title="Wq (wait time)")
        ]
    ).properties(width=900, height=280, title=f"Utilization by hour with constant s = {_s}")

    # Add threshold lines
    _threshold_100 = alt.Chart(pl.DataFrame({"y": [1.0]}).to_pandas()).mark_rule(
        color="#dc2626", strokeDash=[5, 5], strokeWidth=2
    ).encode(y="y:Q")
    _threshold_85 = alt.Chart(pl.DataFrame({"y": [0.85]}).to_pandas()).mark_rule(
        color="#f59e0b", strokeDash=[3, 3], strokeWidth=1
    ).encode(y="y:Q")

    # Count issues
    _unstable_count = sum(1 for u in _utilizations if u >= 1)
    _high_count = sum(1 for u in _utilizations if 0.85 <= u < 1)
    _ok_count = sum(1 for u in _utilizations if u < 0.85)

    # Status message
    if _unstable_count > 0:
        _status_msg = f"⛔ **System unstable** in {_unstable_count} hour(s)"
    elif _high_count > 0:
        _status_msg = f"⚠️ High utilization in {_high_count} hour(s)"
    else:
        _status_msg = "✅ All hours under control"


    slide_4_2.content1 = mo.vstack([
        mo.hstack([constant_staff_slider, mo.md(f"Service rate μ = 10 customers/hour per server")], justify="start", gap=2),
        mo.ui.altair_chart(_util_chart + _threshold_100 + _threshold_85),
        mo.md(_status_msg)
    ], gap=0.5)

    slide_4_2.render()
    return


@app.cell(hide_code=True)
def _(mo, sc):
    # Slide 4.3 — The staffing lever: introducing s(t)
    slide_4_3 = sc.create_slide(
        "The staffing lever",
        layout_type="side-by-side",
        page_number=25
    )

    slide_4_3.content1 = mo.md(
        r"""
        **Solution: staffing that varies with demand**

        What if we could change staffing through the day?

        Introduce **$s(t)$** — staffing by time block:
        - Morning: $s_{\text{morning}}$ staff
        - Afternoon: $s_{\text{afternoon}}$ staff

        **Why blocks work:**
        - Demand patterns are predictable by hour
        - Staff can adjust at shift changes or breaks
        - Queues "reset" reasonably within an hour

        **The trade-off:**
        More staff → better service but higher cost
        """
    )

    slide_4_3.content2 = mo.md(
        r"""
        **Cost structure**

        | Parameter | Value |
        |-----------|-------|
        | Wage per hour | €25 |
        | Operating hours | 8am – 6pm |
        | Min staff | 1 |
        | Max staff | 5 |

        **Two-shift structure:**
        - Morning shift: 8am – 1pm (5 hours)
        - Afternoon shift: 1pm – 6pm (5 hours)

        **Daily labor cost:**

        $$\text{Cost} = 5 \times s_{\text{morning}} \times €25 + 5 \times s_{\text{afternoon}} \times €25$$

        *Example: 2 morning + 4 afternoon = €750/day*
        """
    )

    slide_4_3.render()
    return


@app.cell(hide_code=True)
def _(mo):
    # Sliders for Slide 4.4 — Two-shift staffing decision
    morning_staff_slider = mo.ui.slider(1, 5, value=1, label="Morning shift (8am-1pm)", step=1)
    afternoon_staff_slider = mo.ui.slider(1, 5, value=1, label="Afternoon shift (1pm-6pm)", step=1)
    return afternoon_staff_slider, morning_staff_slider


@app.cell(hide_code=True)
def _(afternoon_staff_slider, alt, math, mo, morning_staff_slider, pl, sc):
    # Slide 4.4 — Two-shift staffing decision (interactive exercise)
    slide_4_4 = sc.create_slide(
        "Two-shift staffing decision",
        layout_type="1-column",
        page_number=26
    )

    # Time block data
    _time_blocks = ["8-9", "9-10", "10-11", "11-12", "12-1", "1-2", "2-3", "3-4", "4-5", "5-6"]
    _arrival_rates = [20, 25, 20, 15, 10, 15, 20, 25, 30, 25]
    _mu_rate = 10  # Service rate per server

    # Morning blocks: 8-9, 9-10, 10-11, 11-12, 12-1 (indices 0-4)
    # Afternoon blocks: 1-2, 2-3, 3-4, 4-5, 5-6 (indices 5-9)
    _s_morning = morning_staff_slider.value
    _s_afternoon = afternoon_staff_slider.value

    _staffing = [_s_morning] * 5 + [_s_afternoon] * 5
    _utilizations = [arr / (s * _mu_rate) for arr, s in zip(_arrival_rates, _staffing)]

    # M/M/s queueing metrics calculation
    def _calc_mms_metrics(lam, mu, s):
        """Calculate M/M/s queueing metrics. Returns (rho, L, W, Lq, Wq) or None if unstable."""
        rho = lam / (s * mu)
        if rho >= 1:
            return (rho, None, None, None, None)  # Unstable

        # Erlang-C formula for P0
        sum_terms = sum((s * rho) ** n / math.factorial(n) for n in range(s))
        last_term = ((s * rho) ** s) / (math.factorial(s) * (1 - rho))
        P0 = 1 / (sum_terms + last_term)

        # Lq = P0 * (s*rho)^s * rho / (s! * (1-rho)^2)
        Lq = P0 * ((s * rho) ** s) * rho / (math.factorial(s) * (1 - rho) ** 2)
        L = Lq + lam / mu
        Wq = Lq / lam * 60  # Convert to minutes
        W = Wq + (1 / mu) * 60  # Convert to minutes
        return (rho, L, W, Lq, Wq)

    _metrics = [_calc_mms_metrics(arr, _mu_rate, s) for arr, s in zip(_arrival_rates, _staffing)]

    _df_util = pl.DataFrame({
        "Time": _time_blocks,
        "λ (arrivals/hr)": _arrival_rates,
        "Staff": _staffing,
        "Utilization": _utilizations,
        "ρ (%)": [f"{u*100:.0f}%" for u in _utilizations],
        "L (customers)": [f"{m[1]:.1f}" if m[1] is not None else "∞" for m in _metrics],
        "W (min)": [f"{m[2]:.1f}" if m[2] is not None else "∞" for m in _metrics],
        "Lq (waiting)": [f"{m[3]:.1f}" if m[3] is not None else "∞" for m in _metrics],
        "Wq (min)": [f"{m[4]:.1f}" if m[4] is not None else "∞" for m in _metrics],
        "Status": ["Unstable" if u >= 1 else ("High" if u >= 0.90 else "OK") for u in _utilizations],
        "Shift": ["Morning"] * 5 + ["Afternoon"] * 5
    })

    _util_chart = alt.Chart(_df_util.to_pandas()).mark_bar().encode(
        x=alt.X("Time:N", sort=_time_blocks, title="Time Block"),
        y=alt.Y("Utilization:Q", title="Utilization (ρ)", scale=alt.Scale(domain=[0, 1.5])),
        color=alt.Color("Status:N",
            scale=alt.Scale(
                domain=["OK", "High", "Unstable"],
                range=["#22c55e", "#f59e0b", "#dc2626"]
            ),
            legend=alt.Legend(title="Status", orient="right")
        ),
        tooltip=[
            alt.Tooltip("Time:N", title="Time"),
            alt.Tooltip("λ (arrivals/hr):Q", title="λ (arrivals/hr)"),
            alt.Tooltip("Staff:Q", title="Staff (s)"),
            alt.Tooltip("ρ (%):N", title="ρ"),
            alt.Tooltip("L (customers):N", title="L (in system)"),
            alt.Tooltip("W (min):N", title="W (total time)"),
            alt.Tooltip("Lq (waiting):N", title="Lq (in queue)"),
            alt.Tooltip("Wq (min):N", title="Wq (wait time)")
        ]
    ).properties(width=850, height=250)

    # Threshold lines
    _threshold_100 = alt.Chart(pl.DataFrame({"y": [1.0]}).to_pandas()).mark_rule(
        color="#dc2626", strokeDash=[5, 5], strokeWidth=2
    ).encode(y="y:Q")
    _threshold_90 = alt.Chart(pl.DataFrame({"y": [0.90]}).to_pandas()).mark_rule(
        color="#f59e0b", strokeDash=[3, 3], strokeWidth=1
    ).encode(y="y:Q")

    # Calculate cost and status
    _daily_cost = 5 * _s_morning * 25 + 5 * _s_afternoon * 25
    _hours_over_90 = sum(1 for u in _utilizations if u >= 0.90)
    _hours_unstable = sum(1 for u in _utilizations if u >= 1)

    if _hours_unstable > 0:
        _status_text = f"⛔ {_hours_unstable} hour(s) unstable (ρ ≥ 100%)"
        _status_color = "#dc2626"
    elif _hours_over_90 > 0:
        _status_text = f"⚠️ {_hours_over_90} hour(s) exceed 90% utilization"
        _status_color = "#f59e0b"
    else:
        _status_text = "✅ All hours OK (ρ < 90%)"
        _status_color = "#22c55e"

    _cost_box = mo.md(f"""
    **Daily Cost: €{_daily_cost}** &nbsp;&nbsp; | &nbsp;&nbsp;
    Morning: {_s_morning} × 5h × €25 = €{_s_morning * 5 * 25} &nbsp;&nbsp; | &nbsp;&nbsp;
    Afternoon: {_s_afternoon} × 5h × €25 = €{_s_afternoon * 5 * 25}
    """)

    _exercise_prompt = mo.callout(
        mo.md("**Exercise:** Find the lowest-cost staffing plan where no hour exceeds 90% utilization."),
        kind="info"
    )

    slide_4_4.content1 = mo.vstack([
        mo.hstack([morning_staff_slider, afternoon_staff_slider], justify="start", gap=2),
        mo.ui.altair_chart(_util_chart + _threshold_100 + _threshold_90),
        mo.hstack([_cost_box, mo.md(f"<span style='color:{_status_color}'>{_status_text}</span>")], justify="space-between"),
        _exercise_prompt
    ], gap=0.5)

    slide_4_4.render()
    return


@app.cell(hide_code=True)
def _(sc):
    # Section 5 separator
    section_5 = sc.create_slide(
        "Wrap-up",
        layout_type="section",
        page_number=27
    )
    section_5.subtitle = "Section 5"
    section_5.content1 = "Key takeaways and next steps"
    section_5.render()
    return


@app.cell(hide_code=True)
def _(mo, sc):
    # Slide 5.1 — Key takeaways
    slide_5_1 = sc.create_slide(
        "Key takeaways",
        layout_type="side-by-side",
        page_number=28
    )

    slide_5_1.content1 = mo.md(
        r"""
        **1. Utilization + variability → waiting (nonlinearly!)**
        - High ρ seems efficient but kills service
        - Variability amplifies the problem

        **2. Stability is necessary but not sufficient**
        - λ < s·μ keeps queues bounded
        - But ρ = 95% is still miserable

        **3. Pooling and standardization shift the frontier**
        - Better service for the same cost
        - Do this before adding staff
        """
    )

    slide_5_1.content2 = mo.md(
        r"""
        **4. Little's Law: L = λW**
        - Always works — universal sanity check
        - Use it to verify your analysis

        **5. Staffing must anticipate peaks**
        - Constant staffing rarely optimal
        - Match capacity to expected arrivals

        ---

        *Now you can explain both pharmacy pictures!*
        """
    )

    slide_5_1.render()
    return


@app.cell(hide_code=True)
def _(mo, sc):
    # Slide 5.2 — What's next: shaping demand
    slide_5_2 = sc.create_slide(
        "What's next: shaping demand",
        layout_type="1-column",
        page_number=29
    )

    slide_5_2.content1 = mo.md(
        """
        **If capacity is costly or slow to change... shape demand instead!**

        **Demand management levers:**
        - **Appointments:** Smooth arrivals, reduce variability
        - **Pickup windows:** Spread demand across time
        - **Prioritization:** Serve high-value first
        - **Pricing:** Off-peak discounts, peak surcharges
        - **Segmentation:** Fast lanes for simple transactions

        **This is the bridge to Revenue Management:**
        - Same capacity, different demand → different outcomes
        - Price/availability can be levers, not just staff
        """
    )

    slide_5_2.render()
    return


if __name__ == "__main__":
    app.run()
