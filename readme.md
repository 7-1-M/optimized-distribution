# Optimized Distrubtion

> Python script to optimaly distribute SuS into buckets, according to their preferences.

## Parameters
- `inputFile` – .xlsx-file used as input
- `outputFile` – .xlsx output file
- `priorityColumnNames` – string to identify columns containing preferences (used in `str.contains()`) (depends on your inputFile)
- `studentColumnName` – string to identify columns containing the SuS number (depends on your inputFile)
- `totalBuckets` – Number of available buckets
- `bucketMin` – Minimum number of SuS per bucket
- `bucketMax` – Maximum number of SuS per bucket
- `assignOnlyPriorities` – only assign SuS to bucket that they chose (default=True)
- `choiceGracePoints` – Used as "weight" to measure *fulfilment of preference*, default=[10,6,2]


## Dependencies
- [python3](https://www.python.org/download/releases/3.0/)
- [pandas](https://pypi.org/project/pandas/)
- [MiniZinc](https://www.minizinc.org/doc-2.5.5/en/installation.html#)