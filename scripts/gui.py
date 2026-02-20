import streamlit as st
import sys
from pathlib import Path
import warnings

sys.path.append(str(Path(__file__).parent / "src"))

from etl.config import JOBS
from etl.orchestrator import clean_folder
from etl.merger import merge
from etl.strip_all import strip_all
from etl.special_characters import special_char
from etl.saver import save_cleaned_data
from etl.reset_view import reset_workbook_view
from etl.end_to_beg import end_to_beg
from etl.clearer import clear_all
from etl.writer import write_master

warnings.filterwarnings(
    "ignore",
    message="Workbook contains no default style*",
    category=UserWarning,
)

st.set_page_config(page_title="Auto Calc Pipeline")

st.title("Auto Calc Pipeline")
st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    folder_input = st.text_input("📁 Target Folder Path", placeholder="C:/Data/Project")
with col2:
    mode = st.selectbox("⚙️ Mode", options=["all", "not-all"], index=0)

if st.button("▶ Run Pipeline", type="primary", use_container_width=True):
    base_folder = Path(folder_input).resolve()
    
    if not base_folder.is_dir():
        st.error(f"Error: '{base_folder}' is not a valid directory.")
    else:
        master_path = base_folder / "Auto Calc.xlsx"
        
        # This creates the "Live Terminal" effect you wanted
        with st.status("Initializing ETL...", expanded=True) as status:
            
            st.write(f"Folder: `{base_folder.name}`")
            
            st.write("Cleaning and Merging...")
            cleaned = clean_folder(base_folder)
            cleaned = merge(cleaned)
            cleaned = strip_all(cleaned)
            cleaned = special_char(cleaned)
            
            st.write("Saving cleaned data...")
            save_cleaned_data(cleaned, base_folder)
            
            st.write("Resetting workbook view...")
            reset_workbook_view(master_path)
            
            if mode == "all":
                st.write("End -> Beg...")
                end_to_beg(str(master_path))
                st.write("Clearing...")
                clear_all(str(master_path), JOBS)
                st.write("Writing...")
                write_master(str(master_path), cleaned, JOBS, clear_first=False)
            else:
                st.write("Writing...")
                write_master(str(master_path), cleaned, JOBS, clear_first=True, suppress_warnings=True)
            
            status.update(label="✅ Pipeline Completed!", state="complete", expanded=False)
        
        st.success("Successfully updated 'Auto Calc.xlsx'")