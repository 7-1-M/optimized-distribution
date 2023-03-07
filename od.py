import minizinc
import pandas as pd

# PARAMETERS
inputFile = 'sus-preferences.xlsx'
outputFile='assigned_sus-preferences.xlsx'
priorityColumnNames='prio'
studentColumnName='SuS-Nr'
totalBuckets=4
bucketMin=4
bucketMax=100
assignOnlyPriorities=True
choiceGracePoints=[10,6,2] # adjust when adding more priorities!

df = pd.read_excel(inputFile)
totalPreferences=df.loc[:, df.columns.str.contains(priorityColumnNames)].shape[1] #don't change!
totalStudents=len(df.index) #don't change!

# MINIZINC MODEL SETUP
## Create a MiniZinc model
model = minizinc.Model()
model.add_string(f"""
int: S = {totalStudents};
int: B = {totalBuckets};
int: P = {totalPreferences};

set of int: Preferences = 1 .. P;
set of int: Buckets = 1 .. B;
set of int: SuS = 1 .. S;

array[SuS, Preferences] of Buckets: choices;

array[Preferences] of int: choiceGracePoints;
var int: choiceGrace;
""")

## Create assignments
model.add_string("""
array[SuS] of var Buckets: assignments;
""")

# CONSTRAINTS
## number of SuS per bucket according to consts "bucketMin" & "bucketMax"
model.add_string("""
constraint
  forall (b in Buckets) (
    let { var int: occ = sum([assignments[s] == b | s in SuS]) } 
    in (occ >= %i) /\ (occ <= %i)
  );
"""%(bucketMin,bucketMax))

## each SuS must be assigned to one of his/her selected buckets
if (assignOnlyPriorities):
    model.add_string("""
    constraint
    forall (s in SuS) (
        exists(p in Preferences)(assignments[s] == choices[s, p])
    );
    """)

## objective: gracePoints (weight could be adjusted)
model.add_string("""
constraint
  choiceGrace == sum([if assignments[s] == choices[s, p] then choiceGracePoints[p] else 0 endif 
                     | s in SuS, p in Preferences]);

""")

# SOLVE MZ INSTANCE
model.add_string('solve maximize choiceGrace')
gecode = minizinc.Solver.lookup("gecode")
inst = minizinc.Instance(gecode, model)

## assign priorities from excel to instance
inst['choices'] = df.loc[:, df.columns.str.contains(priorityColumnNames)].to_numpy()
inst['choiceGracePoints'] = choiceGracePoints

result = inst.solve()

## write output to new excel file
print(result)
df['ASSIGNED BUCKET'] = result['assignments']
df.to_excel(outputFile, index=False)