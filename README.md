
# Capacity Planner (Streamlit)

This is a Streamlit app for production capacity planning with a built-in optimization model.

## Run locally

```bash
pip install -r cap_planner_app/requirements.txt
streamlit run cap_planner_app/ui_streamlit.py
```

## Deploy on Streamlit Cloud

- Point Streamlit Cloud to this repo
- Set the app entrypoint to `cap_planner_app/ui_streamlit.py`
- Add secrets in App Settings -> Secrets if needed
