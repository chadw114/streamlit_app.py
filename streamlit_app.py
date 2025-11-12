import importlib, subprocess, sys
def ensure(pkg, mod=None):
    name = mod or pkg
    try:
        importlib.import_module(name)
    except Exception:
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])
        importlib.import_module(name)
ensure("matplotlib==3.8.4", "matplotlib")
ensure("pandas==2.2.2", "pandas")
ensure("numpy==1.26.4", "numpy")
import cap_planner_app.ui_streamlit
