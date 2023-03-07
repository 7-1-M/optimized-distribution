# Optimized Distribution

> Python script to optimaly distribute SuS into buckets, according to their preferences.

## Parameters
- `inputFile` – .xlsx-file used as input (headers: "SuS-Nr", "priority 1", "priority 2", "priority 3")
- `outputFile` – .xlsx output file
- `priorityColumnNames` – string to identify excel-columns containing preferences (used with `str.contains()`) (depends on your `inputFile`)
- `studentColumnName` – string to identify columns containing the SuS number (depends on your inputFile)
- `totalBuckets` – Number of available buckets
- `bucketMin` – Minimum number of SuS per bucket
- `bucketMax` – Maximum number of SuS per bucket
- `assignOnlyPriorities` – only assign SuS to bucket that they chose (default=True)
- `choiceGracePoints` – Used as "weight" to measure *fulfilment of preference*, default=[10,6,2]

### How To

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