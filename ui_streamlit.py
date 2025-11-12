
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from model_core import load_baseline, compute_allocation

st.set_page_config(page_title='Capacity Planner', layout='wide')

st.title('Production Capacity Planner')

rates, cal, demand_default = load_baseline()
months = cal['Month'].tolist()
lines = [c for c in rates.columns if c.startswith('Production Line')]

st.sidebar.header('Instructions')
st.sidebar.write('Edit the demand table and click Run Optimization to update results.')

st.subheader('Demand Input')
demand_edit = st.data_editor(demand_default, num_rows='dynamic', use_container_width=True, key='demand_editor')

run = st.button('Run Optimization')

if run:
    with st.spinner('Optimizing...'):
        alloc, util, fill_rates, meta = compute_allocation(demand_wide=demand_edit, rates_df=rates, calendar_df=cal)
    st.success('Done!')

    st.subheader('Fill Rate Heatmap')
    fr_piv = fill_rates.pivot(index='PRODUCT', columns='Month', values='Fill_Rate')
    fig, ax = plt.subplots(figsize=(12, 8))
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
    plt.style.use('default')
    plt.rcParams['font.family'] = ['Inter']
    plt.rcParams['font.sans-serif'] = ['Inter']
    ax.set_axisbelow(True)
    im0 = ax.imshow(fr_piv.values, cmap='Blues', vmin=0, vmax=1); cb0 = ax.figure.colorbar(im0, ax=ax); cb0.set_label('Fill Rate'); ax.set_xticks(range(fr_piv.shape[1])); ax.set_yticks(range(fr_piv.shape[0])); ax.set_xticklabels(fr_piv.columns, rotation=45, ha='right'); ax.set_yticklabels(fr_piv.index)
    ax.set_title('Fill Rates by Product and Month', pad=15, color='#171717', fontsize=20, fontweight='semibold')
    ax.set_xlabel('Month', labelpad=10, color='#171717', fontsize=16)
    ax.set_ylabel('Product', labelpad=10, color='#171717', fontsize=16)
    ax.tick_params(axis='both', colors='#171717', labelsize=14)
    for spine in ['top','right']:
        ax.spines[spine].set_visible(False)
    for spine in ['left','bottom']:
        ax.spines[spine].set_visible(True)
        ax.spines[spine].set_color('#171717')
    ax.grid(axis='y', color='#F3F4F6')
    st.pyplot(fig)

    st.subheader('Line Utilization Heatmap')
    util_piv = util.pivot(index='Line', columns='Month', values='Utilization')
    fig2, ax2 = plt.subplots(figsize=(12, 8))
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
    plt.style.use('default')
    plt.rcParams['font.family'] = ['Inter']
    plt.rcParams['font.sans-serif'] = ['Inter']
    ax2.set_axisbelow(True)
    im1 = ax2.imshow(util_piv.values, cmap='Blues', vmin=0, vmax=1); cb1 = ax2.figure.colorbar(im1, ax=ax2); cb1.set_label('Utilization'); ax2.set_xticks(range(util_piv.shape[1])); ax2.set_yticks(range(util_piv.shape[0])); ax2.set_xticklabels(util_piv.columns, rotation=45, ha='right'); ax2.set_yticklabels(util_piv.index)
    ax2.set_title('Line Utilization Heatmap', pad=15, color='#171717', fontsize=20, fontweight='semibold')
    ax2.set_xlabel('Month', labelpad=10, color='#171717', fontsize=16)
    ax2.set_ylabel('Production Line', labelpad=10, color='#171717', fontsize=16)
    ax2.tick_params(axis='both', colors='#171717', labelsize=14)
    for spine in ['top','right']:
        ax2.spines[spine].set_visible(False)
    for spine in ['left','bottom']:
        ax2.spines[spine].set_visible(True)
        ax2.spines[spine].set_color('#171717')
    ax2.grid(axis='y', color='#F3F4F6')
    st.pyplot(fig2)

    st.subheader('Allocations (head) and Downloads')
    st.dataframe(alloc.head(20), use_container_width=True)
    st.download_button('Download allocations CSV', data=alloc.to_csv(index=False).encode('utf-8'), file_name='allocations.csv', mime='text/csv')
    st.download_button('Download line utilization CSV', data=util.to_csv(index=False).encode('utf-8'), file_name='line_utilization.csv', mime='text/csv')
    st.download_button('Download fill rates CSV', data=fill_rates.to_csv(index=False).encode('utf-8'), file_name='fill_rates.csv', mime='text/csv')
else:
    st.info('Edit demand and click Run Optimization to see results.')
