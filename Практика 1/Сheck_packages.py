import subprocess

packages = dict(
    a=dict(depends=[["b"],["c"],["z"]], conflcts=[]),
    b=dict(depends=[["d"]], conflcts=[]),
    c=dict(depends=[["d","e"],["f","g"]], conflcts=[]),
    d=dict(depends=[], conflcts=["e"]),
    e=dict(depends=[], conflcts=[]),
    f=dict(depends=[], conflcts=[]),
    g=dict(depends=[], conflcts=[]),
    y=dict(depends=[["z"]], conflcts=[]),
    z=dict(depends=[], conflcts=[])
)

def depend(x, ys):
    ys = " ".join(["%d" % y for y in ys])
    return "-%d %s" % (x, ys)

def conflict(x, y):
     return "-%d %d" % (x, y)

def build_cnf(packages, installed):
    idx = dict((v, i + 1) for i, v in enumerate(packages)) 
    clauses = []
    for n in packages:
        i = idx[n]
        p = packages[n]
        if p["depends"]:
            for d in p["depends"]:
                clauses.append(depend(i, [idx[x] for x in d]) + " 0")
        if p["conflcts"]:
            for c in p["conflcts"]:
                clauses.append(conflict(i, idx[c]) + " 0")
    for n in installed:
        clauses.append("%d 0" % idx[n])
    return "\n".join(["p cnf %d %d" % (len(packages),len(clauses))] + clauses)

cnf = build_cnf(packages, ["b", "c"])
with open("packages.txt", "w") as f:
    f.write(cnf)

subprocess.run(["minisat/minisat", "packages.cnf", "result.txt"])

