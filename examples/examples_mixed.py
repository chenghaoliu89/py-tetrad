import os
import sys

BASE_DIR = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(BASE_DIR)

import jpype
import jpype.imports

# os.environ["JAVA_HOME"] = "/usr/libexec/java_home"
jpype.startJVM(classpath=[f"{BASE_DIR}/tetrad-gui-7.2.2-launch.jar"])

import pandas as pd
import pytetrad.translate as tr

import java.util as util
import edu.cmu.tetrad.search as ts


df = pd.read_csv(f"{BASE_DIR}/examples/resources/auto-mpg.data.mixed.max.3.categories.txt", sep="\t")
df = df.astype({col: "float64" for col in df.columns if col != "origin"})

data = tr.data_frame_to_tetrad_data(df)
print(data)

variables = data.getVariables()

score = ts.DegenerateGaussianScore(data)
score.setPenaltyDiscount(2)
score.setStructurePrior(0)

test = ts.IndTestDegenerateGaussianLRT(data)
test.setAlpha(0.01)

print("\nfGES\n")
fges = ts.Fges(score)
fges_graph = fges.search()

# print("\nBOSS\n")
# boss = ts.Boss(score)
# boss.setUseDataOrder(False)
# boss.setNumStarts(5)
# boss.bestOrder(variables)
# boss_graph = boss.getGraph(True)

print("\nGRaSP\n")
grasp = ts.Grasp(test, score)
grasp.setOrdered(False)
grasp.setUseDataOrder(False)
grasp.setNumStarts(5)
grasp.bestOrder(variables)
grasp_graph = grasp.getGraph(True)

# print(fges_graph)
# print(boss_graph)
# print(grasp_graph)

print(tr.tetrad_graph_to_pcalg(fges_graph))
# print(tr.tetrad_graph_to_pcalg(boss_graph))
print(tr.tetrad_graph_to_pcalg(grasp_graph))

print(tr.tetrad_graph_to_causal_learn(fges_graph))
# print(tr.tetrad_graph_to_causal_learn(boss_graph))
# print(tr.tetrad_graph_to_causal_learn(grasp_graph))
