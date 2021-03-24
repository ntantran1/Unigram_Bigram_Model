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


    #Create Dictionary
    unigram_table = dict()
    total_word = 0
    dictionary = dict()
    track = 0

    #Loop that loop through the number of sentences
    while track < train_num:
        sent_train.append(sent_temp[track])
        track = track +  1

    while track < sent_count:
        sent_test.append(sent_temp[track])
        track = track + 1

    #loop that loop thorugh a list of train sentences
    for i in sent_train:
        words = word_tokenize(i)
        for w in words:
            w = w.lower()

            if w in dictionary:
                dictionary[w] = dictionary[w] + 1
            else:
                dictionary[w] = 1
            total_word += 1


    #Find Probability for each word
    prob_file = open('unigram_probs.txt', 'w')
    for word,count in dictionary.items():
        prob_file.write('{0} = {1:.2f}\n'.format(word,float(count)/total_word))
        if word not in unigram_table:
            unigram_table[word] = float(count)/total_word
    prob_file.close()

    #Find the Probability of sentences
    eval_file = open('unigram_eval.txt', 'w')
    wordprob = 0
    for s in sent_test:
        words = word_tokenize(s)
        prob = 1
        for w in words :
            w = w.lower()
            if w in unigram_table:
                wordprob = unigram_table[w]
            else:
                wordprob = 0.00
            prob = prob * wordprob
            answer = str(round(prob, 10))
        eval_file.write(answer)
        sent_prob[s] = prob
        eval_file.write("\n")
    eval_file.close()

    #Calculate the perlexity for test sentences using unigram model
    l = []
    readme = open('Readme.txt', 'r')
    for line in readme:
        l.append(line)
    readme.close()


    readmeWrite = open('Readme.txt', 'w')


        
    p = 1
    perlexity = 0

    #Loop that loop through probability of the sentences
    for s in sent_prob:
        p = p * sent_prob[s]
    try:
        perlexity = (1/p) ** (1/len(sent_test))
        l[0] = ("Unigram Perlexity: " + str(perlexity) + "\n")
    except ZeroDivisionError:
        l[0] = ("Unigram Perlexity: infinity\n")
    for ele in l:
        readmeWrite.write(ele)
    readmeWrite.close()

except IOError:
    print('file not found')







