import pandas as pd
import re
from collections import Counter
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import copy
from collections import deque
import itertools
import timeit

start = timeit.default_timer()

file_path = "Ashwin_sec_dataset_filtered.csv"
internal = pd.read_csv(file_path, delimiter=',', usecols=[1],encoding="cp1252").values

file_path = "Ashwin_external.csv"
external = pd.read_csv(file_path, delimiter=',', usecols=['Project reference','Project name'],encoding="cp1252").values

internal_column = list(internal[:,0])
external_column = list(external[:,1])

def findWholeWord(w,str):
    if re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search(str):
        return True
    return False
    
solar_internal = filter(lambda x: findWholeWord('solar',x),internal_column)
solar_external = filter(lambda x: findWholeWord('solar',x),external_column)

# solar_internal = internal_column
# solar_external = external_column
# for i in solar_internal:
#     print(i)

# determine most common words in a file
def commonwords(column):
    words = ' '.join(column).split()
    lower_words = [word.lower() for word in words]
    return Counter(lower_words)

# print(len(list(solar_internal))/5)
# print most common words in each file
# print(commonwords(solar_internal).most_common(11),"\n",commonwords(solar_external).most_common(11))

regex = r"^[^aeiuo]+$"
number_regex = r"\d"
remove_list = {'fund','us','co','i','ii','iii','vi','vii','corp','company','group','trust','term','solar','power','plant','project','commercial','loan','portfolio','refinancing','farm','financing','acquisition','park','water','wind'}
remove = '|'.join(remove_list)
states = {'ak': 'alaska','al': 'alabama','ar': 'arkansas','az': 'arizona','ca': 'california','co': 'colorado','ct': 'connecticut','dc': 'district of columbia','de': 'delaware','fl': 'florida','ga': 'georgia','gu': 'guam','hi': 'hawaii','ia': 'iowa','id': 'idaho','il': 'illinois','in': 'indiana','ks': 'kansas','ky': 'kentucky','la': 'louisiana','ma': 'massachusetts','md': 'maryland','me': 'maine','mi': 'michigan','mn': 'minnesota','mo': 'missouri','mp': 'northern mariana islands','ms': 'mississippi','mt': 'montana','na': 'national','nc': 'north carolina','nd': 'north dakota','ne': 'nebraska','nh': 'new hampshire','nj': 'new jersey','nm': 'new mexico','nv': 'nevada','ny': 'new york','oh': 'ohio','ok': 'oklahoma','or': 'oregon','pa': 'pennsylvania','pr': 'puerto rico','ri': 'rhode island','sc': 'south carolina','sd': 'south dakota','tn': 'tennessee','tx': 'texas','ut': 'utah','va': 'virginia','vi': 'virgin islands','vt': 'vermont','wa': 'washington','wi': 'wisconsin','wv': 'west virginia','wy': 'wyoming'}

test_dict = dict()

# solar_internal = ['Catalina']
for line in solar_internal:
    wordline = list()
    if len(line.split())>1:
        for word in itertools.islice(line.split() , 0, 2):
            lower_word = word.lower()
            if lower_word == 'shell' or lower_word == 'shell:' :
                continue
            if lower_word in remove_list and len(wordline) > 0:
                break
            elif lower_word in remove_list and len(wordline) == 0:
                continue
            if lower_word in states:
                wordline.append(states[lower_word])            
            else:
                wordline.append(lower_word)
            # print(len(wordline))
    else:
        wordline.append(line)
    if len(wordline) == 0:
        wordline.append(line)
    # print(line,'->', ' '.join(wordline))
    test_dict[' '.join(wordline)] = line
    
# print(list(external))

w = dict(list(external))
w = {k: v.lower() for k, v in w.items()}
w = {k: v for k, v in w.items() if findWholeWord('solar',v)}

#for dict
for key,value in test_dict.items():
    # print(y)
    example = copy.deepcopy(w)
    gua = process.extractBests(key,example,scorer=fuzz.partial_ratio,score_cutoff=90, limit=5)
    if gua:
        print(value,"->",key,":",gua)
        
# print(test_dict)
stop = timeit.default_timer()

print(stop - start)

