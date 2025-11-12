
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import pandas as pd
from model_core import compute_allocation, load_baseline

app = FastAPI(title='Capacity Planner API')

class DemandItem(BaseModel):
    PRODUCT: str
    Month: str
    Demand_MT: float

class OptimizeRequest(BaseModel):
    demand: List[DemandItem]

@app.get('/schema')
async def schema():
    rates, cal, dem = load_baseline()
    products = rates['PRODUCT'].tolist()
    lines = [c for c in rates.columns if str(c).startswith('Production Line')]
    months = cal['Month'].tolist()
    return {'products': products, 'lines': lines, 'months': months, 'default_demand': dem.to_dict(orient='records')}

@app.post('/optimize')
async def optimize(req: OptimizeRequest):
    df = pd.DataFrame([d.dict() for d in req.demand])
    demand_wide = df.pivot_table(index='PRODUCT', columns='Month', values='Demand_MT', aggfunc='sum').fillna(0).reset_index()
    allocations, util, fill_rates, meta = compute_allocation(demand_wide=demand_wide)
    return {
        'allocations': allocations.to_dict(orient='records'),
        'line_utilization': util.to_dict(orient='records'),
        'fill_rates': fill_rates.to_dict(orient='records'),
        'meta': meta
    }
