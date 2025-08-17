import streamlit as st
import pandas as pd

st.title("🥤 Pending Smoothie Orders")

# ✅ This uses your secrets.toml config
conn = st.connection("snowflake")

# Get pending orders
def get_pending_orders():
    with conn.session() as session:
        results = session.sql("SELECT id, ingredients, name_on_order FROM orders WHERE order_filled = FALSE").collect()
        return pd.DataFrame(results)

# Mark orders as filled
def mark_orders_filled(order_ids):
    if order_ids:
        id_list = ",".join(map(str, order_ids))
        with conn.session() as session:
            session.sql(f"UPDATE orders SET order_filled = TRUE WHERE id IN ({id_list})").collect()

df = get_pending_orders()

if df.empty:
    st.success("🎉 All smoothie orders are filled!")
else:
    st.dataframe(df, use_container_width=True)

    selected_ids = st.multiselect("✅ Select orders to mark as filled:", df["id"].tolist())

    if st.button("Mark Selected Orders as Filled"):
        mark_orders_filled(selected_ids)
        st.success("Marked as filled! Refreshing...")
        st.experimental_rerun()
