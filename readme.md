# Optimized Distribution

> [Python script](./od.py) to optimaly distribute SuS into buckets, according to their preferences.

## Parameters
- `input_file` – .xlsx-file used as input (headers: "SuS-Nr", "priority 1", "priority 2", "priority 3")
- `output_file` – .xlsx output file
- `priority_column_name_identifier` – string to identify excel-columns containing preferences (used with `str.contains()`) (depends on your `inputFile`)
- `num_iterations` – total numer of picks per SuS (use this when picking for several iterations of the same buckets, e.g. Q1, Q2, Q3, Q4)
- `buckets` – Array Item for each bucket with `[min,max]` amount of students per bucket
- `assign_only_priorities` – only assign SuS to bucket that they chose (default=True)
- `ignore_choice_grace` – Remove "weight" from priorities. Assigned buckets still meet all other constraints!
- `choice_grace_points` – Used as "weight" to measure *fulfilment of preference*, default=[10,6,2] (adjust when adding more priorities!)
- `approximate_best_solution` – time safing measure. The presented solution satisfies all constraints but may not be optimal. default=True

### How To

**Initial Setup:**
1. Install requirements: `pip install -r requirements`
2. Change parameters where needed. (See [[## Parameterse]])
3. Run script: `python od.py`

**Change the number of priorities:**
1. Use an input-file with additional priorities.
2. change the parameter `choiceGracePoints` accordingly (add/remove or change weights)

**Use custom column headers in your xlsx-file:**
- Change the parameter `priorityColumnNames` accordingly (the script uses `contains()` to identify "preference-columns")


## Dependencies
- [python3](https://www.python.org/download/releases/3.0/)
- [pandas](https://pypi.org/project/pandas/)
- [MiniZinc](https://www.minizinc.org/doc-2.5.5/en/installation.html#)

# Disclaimer
Free Use: do whatever to suit your needs :)
Execute any script optained on this repo with caution!