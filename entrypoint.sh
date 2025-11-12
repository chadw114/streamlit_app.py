#!/bin/sh
set -e
uvicorn api:app --host 0.0.0.0 --port 8000 &
streamlit run ui_streamlit.py --server.address 0.0.0.0 --server.port 8501
