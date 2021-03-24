try:

    from nltk import sent_tokenize
    # load data
    filename = "doyle_Bohemia.txt"
    file = open(filename, encoding="utf8")
    text = file.read()
    file.close()
    f = open('doyle_Bohemia_clean.txt', 'w')
    count = 0
    sent_count = 0
    sent_temp = []
    sent_test = []
    sent_train = []
    bigram_table = dict()
    sent_prob = dict()
    # split into sentences
    for i in sent_tokenize(text):
        if count > 1:
            from nltk.tokenize import word_tokenize
            tokens = word_tokenize(i)
            words = [word for word in tokens if word.isalpha()]
            sentence = " ".join(words)
            f.write(sentence)
            sent_temp.append(sentence)
            f.write("\n")
            sent_count += 1
        count += 1
    f.close()
    train_num = int(int(sent_count * (.8)))

    #Create Bigram Dictionary

    freq = {}
    bigram_dict = {}
    prev_word = ''
    freq = dict()
    track = 0

    #Loop that go through the total amount of train sentences
    while track < train_num:
        sent_train.append(sent_temp[track])
        track = track +  1

    while track < sent_count:
        sent_test.append(sent_temp[track])
        track = track + 1


    #Loop that loop through a list of train sentences
    for i in sent_train:
        words = word_tokenize(i)
        for word in words:
            word = word.lower()
            if prev_word not in bigram_dict:
                bigram_dict[prev_word] = dict()
                bigram_dict[prev_word][word] = 1

            else:
                if word in bigram_dict[prev_word]:
                    bigram_dict[prev_word][word] = bigram_dict[prev_word][word] + 1
                else:
                    bigram_dict[prev_word][word] = 1
            prev_word = word


    #Loop that loop throught a list train sentencs
    for i in sent_train:
        words = word_tokenize(i)
        for w in words:
            w = w.lower()

            if w in freq:
                freq[w] = freq[w] + 1
            else:
                freq[w] = 1



    c = 0
    #Loop that loop through a dictionary of all bigram words
    for e in bigram_dict:
        if e in freq:
            for word,count in bigram_dict[e].items():
                c = count
                while count > 0:
                    count = count -1
    prob_file = open('smooth_probs.txt', 'w')
    for e in bigram_dict:
        if e in freq:
            for word,count in bigram_dict[e].items():
                a = bigram_dict[e].get(word) + 0.1
                b = freq.get(e)+(0.1 *len(freq))
                #Smooth equation
                prob_file.write('{0} = {1:.2f}\n'.format("p(" + word + "|" + e + ") =", float(a / b)))
                s = e + " " + word
                #Add smooth for the non existence word
                if s not in bigram_table:
                    a = bigram_dict[e].get(word) + 0.1
                    b = freq.get(e)+(0.1 *len(freq))
                    bigram_table[s] = float(a/b)
    prob_file.close()

    #Prob of sentences using bigram
    eval_file = open('smoothed_eval.txt', 'w')
    wordprob = 0
    prev = ""
    wordprob = 0
    #Loop the list of test sentences
    for i in sent_test:
        words = word_tokenize(i)
        prob = 1
        for word in words:
            word = word.lower()
            s = prev + " " + word
            if prev == "":
                prev = word
            else:
                s = prev + " " + word
                if s in bigram_table:
                    wordprob = bigram_table[s]
                else:
                    if prev in  bigram_dict:
                        if word not in bigram_dict[prev]:
                            a = 0.1
                            b = freq.get(prev)+(0.1 *len(freq))
                            wordprob = float(a/b)
                        else:
                            a = bigram_dict[prev].get(word) + 0.1
                            b = freq.get(prev)+(0.1 *len(freq))
                            wordprob = float(a/b)
                    else:
                        b = 0.1 *len(freq)
                        a = 0.1
                        wordprob = float(a/b)
                        
                prob = prob * wordprob
                sent_prob[1] = prob
                answer = str(round(prob, 1000))
                prev = word
        eval_file.write(answer)
        eval_file.write("\n")
    eval_file.close()

    l = []
    readme = open('Readme.txt', 'r')
    for line in readme:
        l.append(line)
    readme.close()


    readmeWrite = open('Readme.txt', 'w')


    #Caculate the perlexity for smoothed bi gram     
    p = 1
    perlexity = 0
    for s in sent_prob:
        p = p * sent_prob[s]
    try:
        perlexity = (1/p) ** (1/len(sent_test))
        l[2] = ("Smooth Perlexity: " + str(perlexity) + "\n")
    except ZeroDivisionError:
        l[2] = ("Smooth Perlexity: infinity")
    for ele in l:
        readmeWrite.write(ele)
    readmeWrite.close()

except IOError:
    print('file not found')


