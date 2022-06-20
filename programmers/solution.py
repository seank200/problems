import progress

def solution(infos, queries):
    results = []
    
    langs = dict.fromkeys(('cpp', 'java', 'python', '-'))
    jobs  = dict.fromkeys(('backend', 'frontend', '-'))
    exps  = dict.fromkeys(('junior', 'senior', '-'))
    foods = dict.fromkeys(('chicken', 'pizza', '-'))
    
    for k in langs:
        langs[k] = set()
    
    for j in jobs:
        jobs[j] = set()
    
    for e in exps:
        exps[e] = set()
    
    for f in foods:
        foods[f] = set()
    
    for i, info in enumerate(infos):
        infos[i] = info.split(" ")
        infos[i][4] = int(infos[i][4])
    
    for i, query in enumerate(queries):
        queries[i] = query.split(" and ")
        queries[i] = queries[i][:-1] + queries[i][3].split(" ")
        queries[i][4] = int(queries[i][4])
        
    infos.sort(reverse=True, key=lambda x: x[4])
    
    for i, info in enumerate(infos):
        lang, job, exp, food, score = info
        langs[lang].add(i)
        jobs[job].add(i)
        exps[exp].add(i)
        foods[food].add(i)
    
    all_idx = set([i for i in range(len(infos))])
    langs['-'] = all_idx
    jobs['-']  = all_idx
    exps['-']  = all_idx
    foods['-'] = all_idx
    
    progress.progress_start(total=len(queries))
    for i, query in enumerate(queries):
        if i % 200 == 0:
            progress.progress(i)

        lang, job, exp, food, score = query
        
        inters = langs[lang]
        if job != '-':
            inters = inters & jobs[job]
        if exp != '-':
            inters = inters & exps[exp]
        if food != '-':
            inters = inters & foods[food]
        
        matches = 0
        for idx in sorted(inters):
            if infos[idx][4] >= score:
                matches += 1
            else:
                break
        
        results.append(matches)
        
    return results