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

| FIELD     | ACCURACY |
|-----------|----------|
| name      | 82.0%    |
| qty       | 81.4%    |
| range_end | 96.6%    |
| unit      | 91.8%    |
| comment   | 73.6%    |
| OVERALL   | 85.08%   |

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
