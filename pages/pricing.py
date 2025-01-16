import streamlit as st

def pricing_page():
    st.components.v1.html(
        html='''<script async src="https://js.stripe.com/v3/pricing-table.js"></script>
        <stripe-pricing-table pricing-table-id="prctbl_1QhhzHDjNID2hO5KdY8PhrUJ"
        publishable-key="pk_test_51QK6BRDjNID2hO5KX6S5w4J0oO3PFEL6TRZ9fkJzXdGPlgTwWk56DoDX6RZvVL8eWy2EMEugQ2ojG3AsQBST6IHH00T2LJFAU3">
        </stripe-pricing-table>
        ''', height=500, scrolling=True)


if __name__ == "__main__":
    pricing_page()
 