import importlib
mods=['pandas','numpy','scipy','sklearn','streamlit','matplotlib','seaborn','plotly']
for m in mods:
    try:
        mod=importlib.import_module(m)
        print(m, getattr(mod,'__version__','v?'))
    except Exception as e:
        print(m, 'ERROR:', e)
