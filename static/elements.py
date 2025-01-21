import streamlit as st
import altair as alt
from streamlit_extras.stylable_container import stylable_container
import pandas as pd

primary_background = '#111111'
secondary_background = '#171717'
dark_text_color = '#171717'
light_text_color = '#E8E8E8'
color_1 = '#fc4778' #Pink
color_2 = '#3952f5' #Purple
border_color = '#3c3c3c'
caption_color = '#878884'

def tile(key, height, border):
    border_style = f"1px solid {border_color};" if border else "none;"
    
    with stylable_container(
        key=key,
        css_styles=f'''
        {{
            background-color: {secondary_background};
            font-family: "Source Sans Pro", sans-serif;
            font-weight: 400;
            border-radius: 0.5rem;
            border: {border_style};
            padding: calc(1em - 1px);
            color: {light_text_color};
        }}
        '''
    ):
        return st.container(border=False, height=height)

def metric_tile(key, stat, value, height, border, tooltip):
    with tile(key, height, border):
        st.markdown(
            f"""
                <div style="line-height: 1.5;">
                    <p style="margin: 0; font-size: 0.9em; color: {caption_color};">{stat}</p>
                    <p style="margin: 0; font-size: 1.4em; font-weight: bold; color: {light_text_color};">{value}</p>
                </div>
                """,
            unsafe_allow_html=True, help=tooltip
        )

def gradient_tile(key: str, content: str):
    """
    A function to create an animated container with custom content.

    Args:
        key (str): The container's unique key.
        content (str): The HTML content to display inside the container.
    """
    css_styles = f'''
        .gradient-container {{
            position: relative;
            padding: 15px; /* Adjust padding as needed */
            margin-bottom: 17px; /* Add vertical spacing between containers */
            border-radius: 8px; /* Rounded corners */
            background-color: {secondary_background}; /* Inner container background */
            color: {light_text_color}; /* Text color */
            z-index: 1;
            width: 100%;
        }}

        @property --angle {{
            syntax: "<angle>";
            initial-value: 0deg;
            inherits: false;
        }}

        .gradient-container::after, .gradient-container::before {{
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            border-radius: 8px; /* Match the container's border-radius */
            padding: 1px; /* Border thickness */
            -webkit-mask: 
                linear-gradient(#fff 0 0) content-box, 
                linear-gradient(#fff 0 0);
            -webkit-mask-composite: destination-out;
            mask-composite: exclude;
            background-image: conic-gradient(from var(--angle), {color_1}, {color_2}, {color_1}); /* Smooth circular loop */
            z-index: -1; /* Place behind the content */
            animation: spin 3s linear infinite;
        }}

        @keyframes spin {{
            from {{
                --angle: 0deg;
            }}
            to {{
                --angle: 360deg;
            }}
        }}
    '''

    with stylable_container(key=key, css_styles=css_styles):
        with st.container():
            st.markdown(
                f"""
                <div class="gradient-container">{content}</div>
                """,
                unsafe_allow_html=True
            )

def line_chart(data, x, y, x_label, y_label, height=280, show_labels=True):
    """
    Generate a line chart with a gradient fill.
    
    Parameters:
        data (pd.DataFrame): The DataFrame containing the data to plot.
        x (str): The column name for the x-axis.
        y (str): The column name for the y-axis.
        x_label (str): The label for the x-axis.
        y_label (str): The label for the y-axis.
        height (int): The height of the chart. Default is 280.
        show_labels (bool): Show labels or not.
    
    Returns:
        alt.Chart: The Altair chart object.
    """
    # Ensure the x-axis column is interpreted as datetime
    data[x] = pd.to_datetime(data[x])
    
    # Configure axis labels based on show_labels parameter
    x_axis = alt.X(f'{x}:T', title=x_label if show_labels else None)
    y_axis = alt.Y(f'{y}:Q', title=y_label if show_labels else None)

    # Create the main line chart with a gradient fill
    chart = alt.Chart(data).mark_area(
        line={'color': '#E8E8E8'},  # Line color
        color=alt.Gradient(  # Gradient fill with specified opacity
            gradient='linear',
            stops=[
                alt.GradientStop(color='rgba(232, 232, 232, 0.5)', offset=0),
                alt.GradientStop(color='rgba(232, 232, 232, 0)', offset=1)
            ],
            x1=1, x2=1, y1=1, y2=0
        ),
        interpolate='monotone'  # Smooth the line


    ).encode(
        x=x_axis,  # Configure x-axis
        y=y_axis   # Configure y-axis
    ).properties(
        height=height,  # Set the height of the chart
        background=secondary_background,  # Background color
        padding={"top": 10, "bottom": 10, "left": 10, "right": 10}
    ).configure_axis(
        grid=False  # Remove grid lines
    ).configure_view(
        strokeWidth=0  # Remove borders around the chart
    )
    
    return st.altair_chart(chart, use_container_width=True)
