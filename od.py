import minizinc
import pandas as pd
import time

# PARAMETERS
input_file = 'sus-preferences.xlsx'
output_file='assigned_sus-preferences.xlsx'
priority_column_name_identifier='prio'
num_iterations = 2 # change to how may times a bucket is "fillable"
buckets = [
  [1,10],
  [1,24],
  [1,20],
  [1,20],
]
assign_only_priorities = True
ignore_choice_grace=False
approximate_best_solution=True
choice_grace_points=[10,6,2] # adjust when adding more priorities!

num_buckets=len(buckets)
df = pd.read_excel(input_file)
num_prefs=df.loc[:, df.columns.str.contains(priority_column_name_identifier)].shape[1] #don't change!
num_sus=len(df.index) #don't change!
approximation_threshold = 0.05
optimal_grace_value = num_sus * num_iterations * ( sum(choice_grace_points) / len(choice_grace_points) )

# MINIZINC MODEL SETUP
## Create a MiniZinc model
model = minizinc.Model()
model.add_string(f"""
include "globals.mzn";

int: S = {num_sus};
int: B = {num_buckets};
int: I = {num_iterations};
int: P = {num_prefs};

set of int: Preferences = 1 .. P;
set of int: Buckets = 1 .. B;
set of int: BucketIterations = 1 .. I;
set of int: SuS = 1 .. S;

array[SuS, Preferences] of Buckets: choices;

array[Preferences] of int: choiceGracePoints;
var int: choiceGrace;

array[BucketIterations, SuS] of var Buckets: assignments;

array[Buckets, 1 .. 2] of int: bucketParams = array2d(Buckets, 1..2, {[elem for bucket in buckets for elem in bucket]});
""")

# CONSTRAINTS
## number of SuS per bucket according to [min,max] per bucket
model.add_string("""
constraint
  forall (bi in BucketIterations) (
    forall (b in Buckets) (
      let { var int: occ = sum([assignments[bi, s] == b | s in SuS]) } 
      in (occ >= bucketParams[b, 1]) /\ (occ <= bucketParams[b, 2])
    )
  );
""")

## if multiple iterations: each SuS is assigned only once per bucket
if (num_iterations > 1):
  model.add_string("""
    constraint
      forall (s in SuS) (
        alldifferent([assignments[bi, s] | bi in BucketIterations])
      );
  """) 

## each SuS must be assigned to one of his/her selected buckets
if (assign_only_priorities):
    model.add_string("""
    constraint
      forall (bi in BucketIterations, s in SuS) (
        exists(p in Preferences)(assignments[bi, s] == choices[s, p])
      );
    """)

## objective: gracePoints (weight could be adjusted)
if not ignore_choice_grace:
  model.add_string("""
    constraint
      choiceGrace == sum([bool2int(assignments[bi, s] == choices[s, p]) * choiceGracePoints[p]
                    | bi in BucketIterations, s in SuS, p in Preferences]);
  """)

## objective: approximate best solution
  if approximate_best_solution:
    model.add_string(f"""
      constraint choiceGrace >= (1 - {approximation_threshold}) * {optimal_grace_value};
    """)

# SOLVE MZ INSTANCE
if ignore_choice_grace or approximate_best_solution:
  model.add_string('solve satisfy')
else:
  model.add_string('solve maximize choiceGrace')

inst = minizinc.Instance(minizinc.Solver.lookup("gecode"), model)

## assign priorities from excel to instance
inst['choices'] = df.loc[:, df.columns.str.contains(priority_column_name_identifier)].to_numpy()
inst['choiceGracePoints'] = choice_grace_points

start_time = time.time()
result = inst.solve()
print("Time taken:", time.time() - start_time)

## write output to new excel file
print(result)
for i in range(len(result['assignments'])):
  print("iteration: " + str(i + 1))
  df[f'ASSIGNED BUCKET (iteration {i + 1})'] = result['assignments'][i-1]
  print(df)

df.to_excel(output_file, index=False)