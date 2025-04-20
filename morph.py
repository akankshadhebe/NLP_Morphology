import streamlit as st
import pandas as pd

st.set_page_config(page_title="Morphology", layout="centered")

st.markdown("<h2 style='text-align: center; color: #0175C2;'>Morphology</h2>", unsafe_allow_html=True)

if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "edited_df" not in st.session_state:
    st.session_state.edited_df = None
if "selected_root" not in st.session_state:
    st.session_state.selected_root = None

root_word = st.selectbox("Select a Root Word", ["पानी", "रानी", "कुत्ता", "बिल्ली", "लड़का", "धोबी", "नारी"], index=2)

# Reset
if st.session_state.get("selected_root") and root_word != st.session_state.selected_root:
    st.session_state.submitted = False
    st.session_state.edited_df = None
    st.session_state.selected_root = None

# example table
example_table = pd.DataFrame({
    "Delete": ["आ", "आ", "आ", "आ"],
    "Add": ["आ", "ए", "ए", "ओं"],
    "Number": ["sing", "plu", "sing", "plu"],
    "Case": ["dr", "dr", "ob", "ob"]
})

# Answers
tables = {
    "पानी": pd.DataFrame({
        "Delete": ["ई", "ई", "ई", "ई"],
        "Add": ["आ", "ए", "ए", "ओं"],
        "Number": ["sing", "plu", "sing", "plu"],
        "Case": ["dr", "dr", "ob", "ob"]
    }),
    "रानी": pd.DataFrame({
        "Delete": ["ई", "ई", "ई", "ई"],
        "Add": ["ई", "इयाँ", "ई", "इयों"],
        "Number": ["sing", "plu", "sing", "plu"],
        "Case": ["dr", "dr", "ob", "ob"]
    }),
    "कुत्ता": pd.DataFrame({
        "Delete": ["आ", "आ", "आ", "आ"],
        "Add": ["आ", "ए", "ए", "ओं"],
        "Number": ["sing", "plu", "sing", "plu"],
        "Case": ["dr", "dr", "ob", "ob"]
    }),
    "बिल्ली": pd.DataFrame({
        "Delete": ["ई", "ई", "ई", "ई"],
        "Add": ["ई", "इयाँ", "ई", "इयों"],
        "Number": ["sing", "plu", "sing", "plu"],
        "Case": ["dr", "dr", "ob", "ob"]
    }),
    "लड़का": pd.DataFrame({
        "Delete": ["आ", "आ", "आ", "आ"],
        "Add": ["आ", "ए", "ए", "ओं"],
        "Number": ["sing", "plu", "sing", "plu"],
        "Case": ["dr", "dr", "ob", "ob"]
    }),
    "धोबी": pd.DataFrame({
        "Delete": ["ई", "ई", "ई", "ई"],
        "Add": ["आ", "ए", "ए", "ओं"],
        "Number": ["sing", "plu", "sing", "plu"],
        "Case": ["dr", "dr", "ob", "ob"]
    }),
    "नारी": pd.DataFrame({
        "Delete": ["ई", "ई", "ई", "ई"],
        "Add": ["ई", "इयाँ", "ई", "इयों"],
        "Number": ["sing", "plu", "sing", "plu"],
        "Case": ["dr", "dr", "ob", "ob"]
    })
}

morpheme_options = ["आ", "आओं", "आये", "इयाँ", "इयों", "ई", "ए", "ओं"]

st.markdown("### Fill the Add-Delete Table:")

with st.form("morph_form"):
    col1, col2 = st.columns([3, 2])

    with col1:
        st.write("**Your Input Table**")
        base_data = {
            "Delete": ["आ", "आ", "आ", "आ"],  # Default value is now "आ"
            "Add": ["आ", "आ", "आ", "आ"],  # Default value is now "आ"
            "Number": ["sing", "plu", "sing", "plu"],
            "Case": ["dr", "dr", "ob", "ob"]
        }
        user_df = pd.DataFrame(base_data)

        edited_df = st.data_editor(
            user_df,
            num_rows="fixed",
            column_config={
                "Delete": st.column_config.SelectboxColumn("Delete", options=morpheme_options),
                "Add": st.column_config.SelectboxColumn("Add", options=morpheme_options),
                "Number": st.column_config.TextColumn("Number", disabled=True),
                "Case": st.column_config.TextColumn("Case", disabled=True),
            },
            use_container_width=True
        )

    with col2:
        st.write(f"**For Example for कुत्ता:**")  # Always display "कुत्ता"
        st.dataframe(example_table, use_container_width=True)

    submitted = st.form_submit_button("Submit")

# Save
if submitted:
    st.session_state.submitted = True
    st.session_state.edited_df = edited_df
    st.session_state.selected_root = root_word

# Display results
if st.session_state.submitted:
    correct_table = tables.get(st.session_state.selected_root, example_table)
    result_df = st.session_state.edited_df.copy()
    all_correct = True

    for i in range(len(correct_table)):
        user_del = result_df.at[i, "Delete"]
        user_add = result_df.at[i, "Add"]
        corr_del = correct_table.at[i, "Delete"]
        corr_add = correct_table.at[i, "Add"]

        if user_del == corr_del and user_add == corr_add:
            result_df.at[i, "Case"] = "✅"
        else:
            result_df.at[i, "Case"] = "❌"
            all_correct = False

    st.markdown("### Result")
    st.dataframe(result_df, use_container_width=True)

    if all_correct:
        st.success("✅ All entries are correct!")
    else:
        st.warning("⚠️ Some entries are incorrect. Check the ❌ marks.")

    if st.button("Get Answer"):
        st.markdown(f"### ✅ Correct Table for: **{st.session_state.selected_root}**")
        st.dataframe(tables[st.session_state.selected_root], use_container_width=True)
