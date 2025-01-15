import streamlit as st
from streamlit_extras.stylable_container import stylable_container

primary_background = '#111111'
secondary_background = '#171717'
dark_text_color = '#171717'
light_text_color = '#E8E8E8'
color_1 = '#5A85F3' #Blue
color_2 = '#CDFFD8' #Green
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