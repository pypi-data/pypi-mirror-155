def morfoAnaliz(inputW, root, OT, FEL):
        root_3 = list()
        yx = ''
        otstem = ''
        felstem = ''

        for x in inputW: 
            yx += x
            for r in root:
               if yx == r['stem']: 
                  if r['turkum'] == 'NOUN':
                        otstem = yx 
                  elif r['turkum'] == 'VERB':
                        felstem = yx
                        
        diffot = yx.replace(otstem, "")#get suffix ot
        difffel = yx.replace(felstem, "")#get suffix fel
        analizot = findOtSuffix(OT, diffot)      
        analizfel = findOtSuffix(FEL, difffel)      
        if len(otstem) > 0:
            root_3.append('Input:'+yx+'->Root word: '+otstem+"->Word Class: NOUN"+'->Suffix:'+diffot+"->Analyze:"+analizot)
        if len(felstem) > 0: 
            root_3.append('Input:'+yx+'->Root word: '+felstem+"->Word Class: VERB"+'->Suffix:'+difffel+"->Analyze:"+analizfel)    

        return root_3           
    
def findOtSuffix(suffix, inputsuffix):
        analizot = ''
        go =''
        model = ''
        analizot1= ''
        count = 0
        l = list()
        for gword in inputsuffix:
            inputsuffix1 = inputsuffix.replace(analizot1, "")
            if len(inputsuffix) == 0:
                break
            else:   
                analizot1 += AnalizSuffix(suffix, inputsuffix1)
                l.append(AnalizSuffix(suffix, inputsuffix1))
                while '' in l:
                    l.remove("")
                count+=1
        for x in l:
            analizot += x+"+"
            for o in suffix:
                if x == o['suffix']:
                    model += o['tegi']+"+"
        return analizot[:-1]+"->Modeli: "+model[:-1]   

def AnalizSuffix(suffix, inputsuffix):
        go = ''
        analizot = ''
        model = ''

        for x in inputsuffix:
            go += x
            for o in suffix:
                if go == o['suffix']: 
                   analizot = go
                   model = o['tegi']
        return analizot