# Deutschland energy lakehouse

SMARD publishes German electricity as awkward JSON time series. This repo turns one week of **load** and **onshore wind** into Delta tables a person can query.

Medallion:
- `bronze.smard_raw` — raw hours from JSON (big timestamps, nulls kept)
- `silver.electricity_hourly` — Berlin time, typed metrics, duplicates removed
- `gold.daily_energy_mix` — one row per day: load, wind, wind share of load (hours with no load dropped)

How to run: Databricks Free Edition, Git folder on this repo, notebook `notebooks/01_bronze`. Sample JSON lives in `data/sample/`.

Kurz: Aus SMARD-JSON werden drei Tabellen. Bronze ist roh, Silver ist geputzt, Gold ist der Tages-Report (Windanteil an der Last).