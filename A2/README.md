# Assignment 2 - Games and Bayesian Classifiers
## Part 1: Raichu
### Question
![image](https://github.com/user-attachments/assets/30358c54-626f-42a4-89e0-02bd3adf36ec)
![image](https://github.com/user-attachments/assets/a4fe7ecd-4458-4f8e-93d6-ddeb2a7bb823)
![image](https://github.com/user-attachments/assets/212affa6-3b77-4235-a006-f0e461e33fdf)

### Solution
(1) Formulation of problem: Clearly, the problem in front of us is returning a best (supposed optimal) move, for the current player, given the current board state of the Raichu game. Many approaches can succeed in doing so, but my area of interest is exhaustive i.e. generating all moves for the given state, player and pieces (Pichu, Pikachu, Raichu) set. As I learnt through the course, IDS (Iterative Deepening) is favorable for exhaustive searches at various levels. The next node/state is first sent to a smallest function, which leads to a greatest function, leading in recursive depth increase. If the threshold is attained, we return the cost. Given the time factor (the fifth argument), best (or) optimal movs are searched until we run out of time.

(2) Program working strategy: The program is divided into the following functions - next move, cost calculation, goal state (while using the logic of the enhanced Minimax version i.e. alphabeta pruning, which prunes the unnecessary branches, not needed for the search anymore & also uses the small and large functions as bounds). As the game has a unique condition, there is also a special function called Upgrade to Raichu, where a Pichu or Pikachu when reaching the other extreme of the board, becomes fully powered Raichu, just like a pawn turns into its favorable piece (queen, rook, horse, bishop) upon reaching the final tile in chess. Raichus can jump over vulnerable opponent pieces (Vulnerable whites and blacks), in various lengths and directions, making it a bit complex to implement, hence leading to deeper searches. 

(3) Further discussion: 
	
  1. Assumptions: One of the very basic assumption is that the goal state set is attainable i.e. either of the pieces get totally eliminated, in contrary of a deadlock scenario. Another primary assumption/hope is that both players don't upgrade to Raichus in consecutive moves, since in a memory/performance perspective, that can make the search hefty.
  2. Simplifications: The solution can be further simplified if, maybe, instead of aplha beta pruning, a much better approach can be used (personally not sure).
  3. Design decisions: In a design perspective, the approach was to yield moves octa-directionally, that is to calculate (every possible) moves towards Up, Down, Left, Right and the four diagonal directions too.

References for Raichu:
Alpha beta pruning - https://www.youtube.com/watch?v=l-hh51ncgDI
IDS - https://www.geeksforgeeks.org/iterative-deepening-searchids-iterative-deepening-depth-first-searchiddfs/
https://www.ijcai.org/Proceedings/75/Papers/048.pdf

## Part 2: Truth be Told
### Question
![image](https://github.com/user-attachments/assets/5c40b333-6b69-437e-a58e-6cdeaa81ae7e)

### Solution
(1) Formulation of problem: In simple terms, the problem is spam classification, with spam being termed as "deceptive" and non-spam being termed as "truthful/genuine". So, in this given dataset(s) of reviews (user genrated), one is for training the Naive Bayes model and the other is ofr testing it to find out the accuracy. The reviews play a vital role since fake ones among the original ones might lead to customer dissatisfaction or potential lawsuits against the hotel for fraud or misleading information. So, the problem at hand is to "classify/categorize" such reviews, taken from the datasets containing reviews from 20 Chicago-based hotels.

(2) Program working strategy: The ideal approach for such problem would be to use a categorical, especially binary, classifier such as the Naive Bayes. This works by calculating the favorability ratios, also, probabilities or likeliness. After computing such a ratio, it compares it to an already set value/performance quantity. Thus come the concepts of prior and posterior probabilities into reference. So, there are functions such as loadfile (dataset loading), classifier (Naive Bayes using the concept of Laplacean smoothing i.e. adding a constant to the curve), chance (calculating the odds), delete (removing unnecessary marks and stops from the reviews), antecedent (returns the prior probability of the labels) and finally, the accuracy is obtained after the test dataset is gone through. Using Naive Bayes classifier, 85% accuracy was obtained.

(3) Further discussion: 
	
  1. Assumptions: Initially, it is assumed that "words" in the model are actually words, and then later on the stops are filtered. Also, the test dataset is assumed to contain "relevant" data i.e. actual reviews, but not just text.
	2. Improvements: If further operations such as preliminary lowercase conversions or context-appropriate filtering are applied, then the accuracy can be pumped up to 87-92%.

References for Truth be Told:
https://en.wikipedia.org/wiki/Naive_Bayes_spam_filtering
https://medium.com/analytics-vidhya/na%C3%AFve-bayes-algorithm-with-python-7b3aef57fb59
https://www.sciencedirect.com/topics/computer-science/laplacian-smoothing
