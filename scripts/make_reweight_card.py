import json
import sys


def PrintBlock(pars, vals, index):
    res = []
    res.append('launch --rwgt_name=rw%.4i' % index)
    for par, val in zip(pars, vals):
        res.append('set %s %i %g' % (par['block'], par['index'], val))
    return res

par_to_rw_json = {}

with open(sys.argv[1]) as jsonfile:
    cfg = json.load(jsonfile)

pars = cfg['parameters']
defs = cfg['parameter_defaults']

for p in pars:
    for k in defs:
        if k not in p:
            p[k] = defs[k]
# print pars

output = ['change rwgt_dir rwgt']

initvals = [X['sm'] for X in pars]

current_i = 0
output.extend(PrintBlock(pars, initvals, current_i))
current_i += 1

#---Here making 2 reweights per parameters
for i in xrange(len(pars)):
    # reweight with value (--def-val + SM)/2
    for j in xrange(-int(sys.argv[2]), int(sys.argv[2])+1):
        if j==0:
            continue
        vals = list(initvals)
        vals[i] = (pars[i]['val'] + initvals[i]) / int(sys.argv[2]) * j
        output.extend(PrintBlock(pars, vals, current_i))        
        par_to_rw_json['rw%.4i'%current_i] = '%s %f' % (pars[i]['name'], vals[i])
        current_i += 1

# for i in xrange(len(pars)):
#     for j in xrange(i + 1, len(pars)):
#         # print i,j
#         vals = list(initvals)
#         vals[i] = pars[i]['val']
#         vals[j] = pars[j]['val']
#         output.extend(PrintBlock(pars, vals, current_i))
#         current_i += 1


if len(sys.argv) > 3:
    with open(sys.argv[3], 'w') as outfile:
            outfile.write('\n'.join(output))

with open(sys.argv[3][:-3]+'json', 'w') as outfile:
        outfile.write(json.dumps(par_to_rw_json, sort_keys=True, indent=4, separators=(',', ': ')))


print '>> Created %s with %i reweighting points' % (sys.argv[3], current_i)
