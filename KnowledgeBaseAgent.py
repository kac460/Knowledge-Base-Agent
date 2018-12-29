# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 18:20:48 2018

@author: Kevin
"""
import itertools
#import pdb

def indexOf(x, L):
    for i in range(len(L)):
        if(L[i]==x):
            return i
    print("Error: " + str(x) + "not found in " + str(L))
#input: l, a list of terminal symbols (corresponds to a sentence)
    #G, the grammar
    #r, list of nonterminals
#returns a 2D matrix M s.t. M[i][j]==rule_k iff rule_k was used
    #to generate right triangle below it
    #(see Wikipedia page on CYK algorithm)   
def printMatrix(M):
    s=""
    for i in range(len(M)):
        for j in range(len(M[i])):
            s+=str(M[i][j])+"\t"
        s+="\n"
    return s
def printList(L):
    s=""
    for i  in range(len(L)):
        s+=str(L[i]+"\t")
    return s
def cykparse(L, G, R):
    n=len(L)
    r=len(R)
    L.insert(0, "eX")
    R.insert(0, "eX")
    P=[]
    for i in range(n+1):
        P.append([])
        for j in range(n+1):
            P[i].append([])
            for k in range(r+1):
                P[i][j].append(False)
    for s in range(1,n+1):
        for v in range(1,r+1):
            #each key (LHS) points to a list of RHSs
            for i in range(len(G[R[v]])):
                if(L[s] in G[R[v]][i]):
                    #print("done")
                    P[1][s][v]=True
    LHSs=list(G.keys())
    for l in range(2,n+1):
        for s in range(1, n-l+1+1):
            for p in range(1, l-1+1):
                for LHS in LHSs:
                    for RHS in G[LHS]:
                        if(len(RHS)==2):
                            a=indexOf(LHS, R)
                            b=indexOf(RHS[0], R)
                            c=indexOf(RHS[1], R)
                            if P[p][s][b] and P[l-p][s+p][c]:
                            #if P[s][p][b] or P[s+p][l-p][c]:
                                #print("done")
                                P[l][s][a]=True
    M=[]
    for i in range(n+1):
        M.append([])
        for j in range(n+1):
            M[i].append([])
            for k in range(r+1):
                if(P[i][j][k]):
                    M[i][j].append(R[k])
    for row in M:
        row.pop(0)
    M.pop(0)
    L.pop(0)
    R.pop(0)
    return M 
def getNP(M, L):
    for i in reversed(range(len(M))):
        if('NP' in M[i][0]):
            return L[0:i+1]
def getEntity(NP, assignments):
    #lazy way of dealing with "the":
    if NP[0]=="the":
        NP[0]="a"
    s=listToString(NP)
    if(s in assignments["males"]):
        assignments["mostRecentMale"]=s
    elif s in assignments['females']:
        assignments["mostRecentFemale"]=s
    elif s=="he":
        s=assignments["mostRecentMale"]
        if s=="":
            print("Who's 'he'?")
            s=input()
            assignments["mostRecentMale"]=s
    elif s=="she":
        s=assignments["mostRecentFemale"]
        if s=="":
            print("Who's 'she'?")
            s=input()
            assignments["mostRecentFemale"]=s
    return s
def getVP(M, j ,L):
    #print(j)
    for i in reversed(range(len(M))):
        if('VP' in M[i][j]):
            return L[j:j+i+1]
def getVPs(M, j, L):
    VPs=[]
    '''
    for i in reversed(range(len(M))):
        if('VP' in M[i][j]):
            VPs.append(L[j:j+i+1])
    '''
    #get highest VP:
    for i in reversed(range(len(M))):
        if('VP' in M[i][j]):
            break
    #M[i][j] is now the highest VP location inthe matrix
    #get adjuncts/object:
    subphraseLocations=[]
    counter=1
    trans=False
    if j<len(M[0])-1:
        for r in reversed(range(len(M))):
            if 'NP' in M[r][j+1]:
                trans=True
                break
    if trans:
        subphraseLocations.append([j+1, j+1+r]) #location of object
    for c in range(j+1, len(M[0])):
        for r in range(i-counter+1):
            if(r<len(M) and c<len(M[0])):
                if('PP' in M[r][c]):
                    subphraseLocations.append([c, c+r])
    for length in range(len(subphraseLocations)+1):
        for subset in itertools.combinations(subphraseLocations, length):
            s=[]
            for elem in subset:
                P=L[elem[0]:elem[1]+1]
                P=listToString(P)
                #print(P)
                s.append(P)
            s.insert(0, L[j])
            #print("s=" + str(s))
            s=listToString(s)
            VPs.append(s)
    return VPs
def normalizedVP(VP):
    #print("normalizing " +str(VP))
    for i in range(len(VP)):
        if(VP[i]==' '):
            if(VP[i-1]=='s'):
                VP=VP[:i-1]+VP[i:]
            break
    if(i==len(VP)-1):
        if(VP[i]=='s'):
            VP=VP[:i]
    '''
    if(VP[0][len(VP[0])-1])=='s':
        #print('done')
        VP[0]=VP[0][:len(VP[0])-1]
    
    elif(VP[0]=="doesn't"):
        print()#negation
    '''
    #print("normalized: " + str(VP))
    return VP
def getProperty(VP):
    VP=listToString(VP)
    VP=normalizedVP(VP)
    return VP
def getProperties(VPs):
    props=[]
    for VP in VPs:
        VP=normalizedVP(VP)
        props.append(VP)
    return props
def listToString(L):
    s=""
    for e in L:
        s+=e+" "
    return s[:len(s)-1]

def checkConditionals(hypotheticals, world):
    keepChecking=True
    while keepChecking:
        keepChecking=False
        antecedents=list(hypotheticals.keys())
        knownProps=list(world.keys())
        for a in antecedents:
            newFacts=[]
            for consequence in hypotheticals[a]:
                anteEntity=a[0]
                anteProp=a[1]
                consEntity=consequence[0]
                consProp=consequence[1]
                if(anteProp in knownProps):
                    if anteEntity in world[anteProp]:
                        print("Because " + anteEntity + " has the property '" + anteProp + "', I know that " 
                              + consEntity + " has the property '" + consProp +"'")
                        if(consProp in knownProps):
                            world[consProp].add(consEntity)
                        else:
                            world[consProp]=set()
                            world["doesn't " + consProp]=set()
                            world[consProp].add(consEntity)
                        newFacts.append(consequence)
                        keepChecking=True
            for f in newFacts:
                hypotheticals[a].remove(f)
                
def checkContradictions(world):
    props=world.keys()
    for p in props:
        if "doesn't" not in p:
            entities=list(world[p])
            for e in entities:
                if e in world["doesn't "+p]:
                    print("Contradiction: " + e + " has the property " + p + " and the property doesn't " + p)
                    print("Does " + e + " " + p + " (yes/no)")
                    if "yes" in input():
                        world["doesn't " + p].remove(e)
                    else:
                        world[p].remove(e)
                    print("Okay.")
grammar = {
        'S'  :[('NP', 'VP')],
        'VP' :[('VP', 'PP'),('V',  'NP'),('Neg', 'VP'), ('eats',),('eat',),('run',),('runs',),('drinks',),('drink',), ('walk,'), ('walks',)],
        'PP' :[('P',  'NP')],
        'NP' :[('Det','N'),('she',), ('who',), ('jane',), ('fish',), ('john',), ('alex',), ('he',), ('kevin',), ('soda',)],
        'V'  :[('eats',),('eat',), ('drinks',),('drink',), ('throw',), ('throws',), ('likes',), ('like',)],
        'P'  :[('with',), ('on',), ('at',)],
        'N'  :[('fish',),('fork',), ('soda',)],
        'Det':[('a',), ('the',)],
        'Neg':[("doesn't",)]
        }
assignments = {
        "mostRecentFemale":"",
        "mostRecentMale":"",
        "males":["john", "joe", "kevin", "donald"],
        "females":["jane","jen","alex"]
        }
properties = {
        }
conditionals={
        }
nonterminals=list(grammar.keys())
print("")
print("To end the program, enter 'stop' (no quotation marks)")
print("")
print("Enter sentences/questions (one at a time) of one of these forms: ")
print("<NP> [doesn't/does not] <VP>[.]")
print("If <NP> [doesn't/does not] <VP>, then <NP> [doesn't/does not] <VP>[.]")
print("Does <NP> [doesn't/does not] <VP>?")
print("Who [doesn't/does not] <VP>?")
print("")
print("(note: [] indicates optionality. <> indicates necessity. / means 'or')")
    
while(True):
    checkContradictions(properties)
    knownProperties=list(properties.keys())
    s=input().lower()
    if s == "stop":
        break
    elif(s[len(s)-1]!='?'):
        if(s[len(s)-1]=='.' or s[len(s)-1]=='!'):
            s=s[:len(s)-1]
        L=s.split()
        for n in range(len(L)-1):
            if(L[n]=="does" and L[n+1]=="not"):
                L[n]="doesn't"
                L.pop(n+1)
            elif(L[n]=="do" and L[n+1]=="not"):
                L[n]="doesn't"
                L.pop(n+1)
            elif(L[n]=="don't"):
                L[n]="doesn't"
        if L[0]!="if":
            M=cykparse(L, grammar, nonterminals)
            print(printMatrix(M))
            if('S' not in M[len(M)-1][0]):
                print("I don't understand (sentence not in English fragment)")
            else:
                NP=getNP(M,L)
                j=len(NP)
                #VP=getVP(M,j,L)
                entity=getEntity(NP, assignments)
                print("entity: " + str(entity))
                #prop=getProperty(VP)
                VPs=getVPs(M, j, L)
                if("doesn't" not in VPs[0]):
                    #print("VPs: " + str(VPs))
                    props=getProperties(VPs)
                    print("properties: " + str(props))
                    for prop in props:
                        if prop in knownProperties:
                            properties[prop].add(entity)
                        else:
                            properties[prop]=set()
                            properties["doesn't "+prop]=set()
                            properties[prop].add(entity)
                else:
                    VP=getVP(M, j+1, L)
                    #print("VP: " + str(VP))
                    prop=getProperty(VP)
                    print("property: doesn't " +str(prop))
                    if prop in knownProperties:
                        properties["doesn't " + prop].add(entity)
                    else:
                         properties[prop]=set()
                         properties["doesn't "+prop]=set()
                         properties["doesn't "+prop].add(entity)
        else:
            #pdb.set_trace()
            antecedent=[]
            i=1
            #print("L= " +str(L))
            while(i<len(L) and L[i]!="then"):
                antecedent.append(L[i])
                i+=1
            print("antecedent:")
            print(str(antecedent))
            if antecedent[i-2][len(antecedent[i-2])-1]==',':
                antecedent[i-2]=antecedent[i-2][:len(antecedent[i-2])-1]
            if len(antecedent)==len(L):
                print("Conditional statements must be of the form 'If <sentence> then <sentence>'")
            else:
                consequent=L[i+1:len(L)]
                MA=cykparse(antecedent, grammar, nonterminals)
                print(printMatrix(MA))
                print("consequent:")
                print(str(consequent))
                MC=cykparse(consequent, grammar, nonterminals)
                print(printMatrix(MC))
                if ('S' not in MA[len(MA)-1][0]) or ('S' not in MC[len(MC)-1][0]):
                    print("I don't understand (sentence not in English fragment)")
                else:
                    anteNP=getNP(MA, antecedent)
                    antej=len(anteNP)
                    anteEntity=getEntity(anteNP, assignments)
                    print("antecedent entity: " + str(anteEntity))
                    anteVP=getVP(MA, antej, antecedent)
                    anteProp=getProperty(anteVP)
                    print("antecedent property: " + str(anteProp))
                    if (anteEntity, anteProp) not in list(conditionals.keys()):
                        conditionals[(anteEntity, anteProp)] = set()
                    consNP=getNP(MC, consequent)
                    consj=len(consNP)
                    consEntity=getEntity(consNP, assignments)
                    print("consequent entity: " + str(consEntity))
                    consVPs=getVPs(MC, consj, consequent)
                    if("doesn't" not in consVPs[0]):
                        #print("consVPs: " + str(consVPs))
                        consprops=getProperties(consVPs)
                        print("consequent properties " + str(consprops))
                        for consprop in consprops:
                            conditionals[(anteEntity, anteProp)].add((consEntity, consprop))
                    else:
                        consVP=getVP(MC, consj+1, consequent)
                        #print("consVP: " + str(consVP))
                        consprop=getProperty(consVP)
                        print("consequent property: doesn't " +str(consprop))
                        conditionals[(anteEntity, anteProp)].add((consEntity, "doesn't " + consprop))
                
    else:
        s=s[:len(s)-1]
        L=s.split()
        for n in range(len(L)-1):
            if(L[n]=="does" and L[n+1]=="not"):
                L[n]="doesn't"
                L.pop(n+1)
            elif(L[n]=="do" and L[n+1]=="not"):
                L[n]="doesn't"
                L.pop(n+1)
            elif(L[n]=="don't"):
                L[n]="doesn't"
        if(L[0]=='does'):
            L=L[1:]
            M=cykparse(L, grammar, nonterminals)
            if('S' not in M[len(M)-1][0]):
                print("I don't understand (sentence not in English fragment)")
            else:
                NP=getNP(M,L)
                j=len(NP)
                VP=getVP(M,j,L)
                entity=getEntity(NP, assignments)
                prop=getProperty(VP)
                if prop in knownProperties:
                    if entity in properties[prop]:
                        print("YES!")
                    elif entity in properties["doesn't "+prop]:
                        print("NO!")
                    else:
                        print("I'M NOT SURE!")
                else:
                    print("I don't know of anyone who does " + prop)
        elif(L[0]=='who'):
            M=cykparse(L, grammar, nonterminals)
            if('S' not in M[len(M)-1][0]):
                print("I don't understand (sentence not in English fragment)")
            else:
                NP=getNP(M,L)
                j=len(NP)
                VP=getVP(M,j,L)
                prop=getProperty(VP)
                print("property: "+str(prop))
                #print answers:
                if prop in knownProperties:
                    if len(properties[prop])>0:
                        st=""
                        for e in properties[prop]:
                            st+=e + ", "
                        st=st[:len(st)-2]
                        if len(properties[prop])>1:
                            for x in reversed(range(len(st))):
                                if(st[x]==' '):
                                    st=st[:x-1]+' and'+st[x:]
                                    break
                        print(st.upper())
                    else:
                        print("I don't know of anyone who does " + prop)
                else:
                    print("I don't know of anyone who does " + prop)
        else:
            print("Good question, but I'm not smart enough to know the answer :(")
            print("(Keep in mind I don't know how to deal with 'who' as an object!)")
    checkConditionals(conditionals, properties)
        
#print(VP)
#print(normalizedVP(VP))
#print(grammar[nonterminals[0]])
#print(grammar['S'])

