Unigram Perlexity: infinity
Bigram Perlexity: infinity
Smooth Perlexity: 5.3113700754119435

-Unigram and Bigram performed worst because the perlexity goes to infinity because of the unseen word probability
so the distribution of the model is unable to predict the test senteces.A low perplexity indicates the probability 
distribution is good at predicting the sample.

-Smoothing help the model's performance when evaluated the on this corpus because the data is small and smoothing 
gave the model a better distribution(perplexity) than without smoothing. The smoothing help with unseen word
to create a bigger parameter so the model can have lower perplexity.