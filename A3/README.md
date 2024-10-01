# Assignment 3 - Probability, NLP and Computer Vision
## Part 1: Part-of-speech tagging
### Question
![image](https://github.com/user-attachments/assets/914a5bc9-0813-4c50-8baa-ad6ef6dce2fb)
![image](https://github.com/user-attachments/assets/f3e87683-2440-4f52-b351-c12db2b04c52)
![image](https://github.com/user-attachments/assets/b10143ef-04b6-43de-8ee0-6d00699298cc)

### Solution
(1) Formulation of problem: The basic problem here is part-of-speech tagging, where the goal is to mark each and every word in a sentence with the type/part of speech it is i.e. noun, verb etc. There can be sentences which are very complex, for instance, the Buffalo example which was given in the assignment beginning. To make such hefty tasks easy, we take advantage of statistical models, since this is a best example for NLP problem. Hence, we decided to use the Bayes simplified net approach. Along with that, to find the MAP (maximum a posteriori), we use the Viterbi method and then Gibbs sampling for estimating the best labels for each word.

(2) Program working strategy: To help us, we have been provided with data, which is thoroughly divided into 12 part-of-speech tags: ADJ (adjective), ADV (adverb), ADP (adposition), CONJ (conjunction), DET (determiner), NOUN, NUM (number), PRON (pronoun), PRT (particle), VERB, X (foreign word), and . (punctuation mark). The three various approaches to solve this as we discussed are - Bayesian Net (Simplified), Viterbi (for HMM - Hidden Markov Models) and Gibbs sampling for MCMC.

Naive Bayes:
We simply track the frequency of each word having a particular tag. We also track the tag frequency. Using these wordcounts, we calculate the word and tag probabilities in reference to the whole data corpus. The highest probability for a word is corresponding to the particular tag with the greatest probability. This is a Naive Bayes approach which doesn't consider previous tags, words or indices into consideration.

Viterbi for Hidden Markov Models:
Using pre-computed emission probabilities, initial probabilities are calculated. The transition/change probability corresponds to chance of change between states. A viterbi table is created with the words as columns and tags as rows. Following all forward steps calculation, max values and next values are generated. Finally, a backward propagation is done using the MAP value for terminal state until the whole sequence is recreated.

MCMC with Gibbs Sampling:
Gibbs sampling involves static values repititively, but for many times this gets computationally heavy. So the number of times to loop (epochs) is modified between the range of 125-200. The outputs are stored in a list of lists, using which we find the most frequent tag and append it to the final result.

(3) Further discussion:
We faced problems with MCMC since calculating emission for each state was very hectic. Also, the backward propagating in Viterbi took some time to understand in a technical coding approach.

Result accuracies: 
Bayes: the accuracy(words) is 93.92% and accuracy(sentences) is 47.45% for the big test file whereas accuracy(words) is 97.62%, accuracy(sentences) is 66.67% for the tiny test file.
Viterbi HMM: the accuracy(words) is 94.86% and accuracy(sentences) is 51.90% for the big test file whereas accuracy(words) is 97.62%, accuracy(sentences) is 66.67% for the tiny test file.
MCMC using sampling (Gibbs): the accuracy(words) is 93.92% and accuracy(sentences) is 47.45% for the big test file, whereas accuracy(words) is 97.62%, accuracy(sentences) is 66.67% for the tiny test file.

Assumptions: Tests done only for the 12 tags provided ; All approaches will run within 10 mins for the big test file.
Improvements: The MCMC using Gibbs sampling can be updated to perform a bit well, in terms of time complexity.

References for Part-1: 
https://stackoverflow.com/questions/268272/getting-key-with-maximum-value-in-dictionary
https://medium.com/data-science-in-your-pocket/pos-tagging-using-hidden-markov-models-hmm-viterbi-algorithm-in-nlp-mathematics-explained-d43ca89347c4
https://newbedev.com/np-random-choice-probabilities-do-not-sum-to-1
https://towardsdatascience.com/gibbs-sampling-8e4844560ae5
Prof Crandall's lecture and video codes

## Part 2: Reading text
### Question
![image](https://github.com/user-attachments/assets/2aded4dd-7d19-4b37-92d1-4ede57cbcc4a)
![image](https://github.com/user-attachments/assets/90664fcb-ff9e-4416-b784-47dd5f627c52)

### Solution
(1) Formulation of problem: We need to extract text from a noisy document image. Some pparticular letters may be critical to recognize. Hence, we use HMMs.

(2) Program working strategy: We were given one training image and 20 testing images, in a folder called test-images. The train image has no noise and has all characters and letters in it, whereas the testing images have noise in them. The approaches are Naive Bayes and Hidden Markov Model using Viterbi, just like part-1.
We maintain four counts:
MB: count of matched blanks ' ', MBS: count of mismatched blank and star, MSB; vice versa, MS : count of matched stars '*' 

In Bayes, We use Laplacean smoothing to smooth out the noise.
Viterbi is used to predict the most possible pattern with the help of the probabilities acquired from the train dataset.

(3) Further discussion:
The most challenging thing was tuning the noise properly.
Assumptions: Assuming the images have English words and lines/sentences, statistical approaches are used to solve dilemmas.

References for Part-2:
http://www.adeveloperdiary.com/data-science/machine-learning/implement-viterbi-algorithm-in-hidden-markov-model-using-python-and-r/
https://web.math.princeton.edu/~rvan/orf557/hmm080728.pdf
https://people.csail.mit.edu/billf/publications/Noise_Estimation_Single_Image.pdf
https://stackoverflow.com/questions/2440504/noise-estimation-noise-measurement-in-image
https://towardsdatascience.com/laplace-smoothing-in-na%C3%AFve-bayes-algorithm-9c237a8bdece?gi=226b8c1efb3b
