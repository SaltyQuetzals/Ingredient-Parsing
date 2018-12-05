# Ingredient Parsing

A while ago, I stumbled upon a [fantastic write-up](https://open.blogs.nytimes.com/2015/04/09/extracting-structured-data-from-recipes-using-conditional-random-fields/) 
from the New York Times about structured predictions using conditional random
fields (CRFs). However, if you look at when the article was released, you'll
notice it was released in 2015. At the time of writing, that's over 3 years ago.
NLP has come a long way since then, with the advent of LSTMs, word embeddings,
and sequence-to-sequence modelling. I firmly believe that the use of recurrent
neural networks can improve upon the overall ability of the tagger.

## Goals

### Beat the NYT

Conditional random fields are _surprisingly_ effective at tagging these
sentences. I want to beat the NYT's model, and not by just a little, but by a
statistically-significant margin.

#### Stats to Beat

The below statistics were calculated by training a CRF model on the training
corpus (found in `train.csv`), and then evaluating it using the ingredient
sentences in `test.csv`.

|             | precision |   recall | f1-score |  support |
|-------------|-----------|----------|----------|----------|
|       OTHER |      0.32 |     0.62 |     0.42 |      216 |
|      B-NAME |      0.85 |     0.85 |     0.85 |      524 |
|      I-NAME |      0.71 |     0.72 |     0.71 |      392 |
|   B-COMMENT |      0.78 |     0.67 |     0.72 |      372 |
|   I-COMMENT |      0.85 |     0.68 |     0.75 |      708 |
| B-RANGE_END |      0.33 |     1.00 |     0.50 |        3 |
|      B-UNIT |      0.96 |     0.91 |     0.93 |      350 |
|      I-UNIT |      0.00 |     0.00 |     0.00 |        0 |
|       B-QTY |      0.97 |     0.97 |     0.97 |      421 |
|             |           |          |          |          |
|   micro avg |      0.78 |     0.78 |     0.78 |     2986 |
|   macro avg |      0.64 |     0.71 |     0.65 |     2986 |
|weighted avg |      0.81 |     0.78 |     0.79 |     2986 |
| samples avg |      0.78 |     0.78 |     0.78 |     2986 |

![Confusion Matrix](CRF_ConfusionMatrix.png)

These are pretty solid results, but I think that LSTMs can do better.

### Increase the dataset size

The NYT provided a nice dataset to start work with. However, there's definitely
still more data that can be incorporated, and can also help the model
generalize. Otherwise, it's going to overfit to just NYT recipes.

### Learn RNNs

I'm tired of just blindly bumbling around when using deep learning. I want to
build something, and know _why_ I built it. Up until now, it's been mostly
trial-and-error. I'd like to be able to at least justify my system architecture
and learn a little more about the space of part-of-speech tagging.
