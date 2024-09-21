import time
import pandas as pd
import minizinc

# PARAMETERS
input_file = 'sus-preferences.xlsx'
output_file='assigned_sus-preferences.xlsx'
pref_header_identifier="pref"
atelier_header_identifier="\(at"
num_iterations = 3 # change to how may times a bucket is "fillable"
buckets = [
  [14,16],
  [14,16],
  [9,10], #Tüftelwerkstatt max.9

  [14,16],
  [14,16],
  [14,16],

  [14,16],
  [14,16],
  [14,16],
]

num_buckets=len(buckets)
df = pd.read_excel(input_file, header=3) # change the number of headers depending on your excel file

num_prefs=df.loc[:, df.columns.str.contains(pref_header_identifier)].shape[1] #don't change!
num_sus=len(df.index) #don't change!

print("SuS:", num_sus)
print("Preferences:", num_prefs)
print("Buckets:", num_buckets)
print("Iterations:", num_iterations)

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

## each SuS must not be assigned to one of his/her selected buckets
model.add_string("""
constraint
  forall (bi in BucketIterations, s in SuS) (
    not exists(p in Preferences)(assignments[bi, s] == choices[s, p])
  );
""")


# SOLVE MZ INSTANCE
model.add_string('solve satisfy')
inst = minizinc.Instance(minizinc.Solver.lookup("chuffed"), model)

## assign priorities from excel to instance
inst['choices'] = df.loc[:, df.columns.str.contains(pref_header_identifier)].to_numpy()

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