import streamlit as st
from streamlit_extras.stylable_container import stylable_container

primary_background = '#111111'
secondary_background = '#171717'
dark_text_color = '#171717'
light_text_color = '#E8E8E8'
color_1 = '#fc4778'
color_2 = '#3952f5'
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


