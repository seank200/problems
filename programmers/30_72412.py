# https://programmers.co.kr/learn/courses/30/lessons/72412
# language, job, experience, food, score

def solution(info, query):
    answer = []
    
    h_info = dict()  # hashed info
    
    for l in ('cpp', 'java', 'python', '-'):
        for j in ('backend', 'frontend', '-'):
            for e in ('junior', 'senior', '-'):
                for f in ('chicken', 'pizza', '-'):
                    h_info[l+j+e+f] = list()
    
    for ii in info:
        lang, job, exp, food, score = ii.split(" ")
        
        for l in (lang, '-'):
            for j in (job, '-'):
                for e in (exp, '-'):
                    for f in (food, '-'):
                        h_info[l+j+e+f].append(int(score))
    
    for k in h_info:
        h_info[k].sort(reverse=True)
    
    for qq in query:
        lang, job, exp, food, q_score = qq.replace("and ", "").split(" ")
        
        q_key = lang + job + exp + food
        q_score = int(q_score)
        
        # binary search
        lo = 0
        hi = len(h_info[q_key]) - 1
        
        while lo <= hi:
            md = (lo + hi) // 2
            
            if h_info[q_key][md] < q_score:
                hi = md - 1
            else:
                lo = md + 1
        
        answer.append(lo)
    
    return answer