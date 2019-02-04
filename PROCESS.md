# Procedure

## Problem Identification

In order to do any kind of research about possible models, I needed to figure out what kind of problem I was tackling. The NYT called the problem they were modeling a "structured prediction" problem, but that category is too general. More specifically, this is a _sequence tagging_ problem. We've got a bunch of words, and we need to define what specifically each word represents in the context of the sentence. Take, for example:

| 3   | tablespoons | unsalted | butter |
| --- | ----------- | -------- | ------ |
| `?` | `?`         | `?`      | `?`    |

The problem is to figure out what each `?` is in the context of the sentence. The NYT decided what parts of the sentence they were looking for:

- `QUANTITY`
- `UNIT`
- `INGREDIENT NAME`
- `COMMENT`
- `OTHER`

So we just need to build something that can assign those labels to each `?`!

If you're curious, here's how these ought to be tagged.

| 3          | tablespoons | unsalted          | butter            |
| ---------- | ----------- | ----------------- | ----------------- |
| `QUANTITY` | `UNIT`      | `INGREDIENT NAME` | `INGREDIENT NAME` |

## Dataset Construction

The data was [provided by the New York Times](https://github.com/NYTimes/ingredient-phrase-tagger/blob/master/nyt-ingredients-snapshot-2015.csv). The first thing to do was to split the data into training, validation, and testing datasets. I chose to allocate 50 examples to the testing dataset,
and the remaining examples were split 80%/20% between training/validation.

| Subset     | # of Examples |
| ---------- | ------------- |
| Training   | 130000        |
| Validation | 48582         |
| Testing    | 481           |

## Baseline Verification

The first thing I wanted to do was check out the CRF that the NYT said got such high accuracy on the task. According to the NYT, they got 89% accuracy when training their model on 130,000 examples. I used the training and testing datasets above to automatically train and evaluate the model, and here are the results I got using scikit-learn's [`accuracy_score`](http://scikit-learn.org/stable/modules/generated/sklearn.metrics.accuracy_score.html#sklearn.metrics.accuracy_score) and [`classification_report`](http://scikit-learn.org/stable/modules/generated/sklearn.metrics.classification_report.html).

```Accuracy: 81.01623147494708%```

| TAG          | precision | recall | f1-score | support |
| ------------ | --------- | ------ | -------- | ------- |
| B-COMMENT    | 0.68      | 0.82   | 0.74     | 309     |
| B-NAME       | 0.85      | 0.86   | 0.86     | 499     |
| B-QTY        | 0.99      | 0.99   | 0.99     | 410     |
| B-RANGE_END  | 0.60      | 1.00   | 0.75     | 3       |
| B-UNIT       | 0.92      | 0.99   | 0.95     | 322     |
| I-COMMENT    | 0.72      | 0.87   | 0.78     | 529     |
| I-NAME       | 0.79      | 0.69   | 0.73     | 341     |
| OTHER        | 0.75      | 0.46   | 0.57     | 421     |
|              |           |        |          |         |
| micro avg    | 0.81      | 0.81   | 0.81     | 2834    |
| macro avg    | 0.79      | 0.83   | 0.80     | 2834    |
| weighted avg | 0.81      | 0.81   | 0.80     | 2834    |

As you can tell, the model I'm competing against doesn't achieve the 89% accuracy reported, but it's still quite strong.

However, since accuracy can be quite misleading when measuring the success of a classifier, I'd rather work with something a little more informative: F1 score.

Accuracy can be thrown off by class imbalances, whereas F1 can take those imbalances into account.

As a result, I'd like to judge the CRF produced by the NYT, not by its overall accuracy, but by the F1 score it achieves. I'll go ahead and pick the macro average: **Number to beat: 0.81 (81%)**

## Model Choice and Implementation

Unsurprisingly, conditional random fields (the model that achieved the results above) dominated the sequence tagging realm for quite a long time due to their great ability to capture the context of words. However, in recent years, deep learning has made great strides in POS-tagging.

One model that struck me was the use of a bidirectional LSTM CRF (BiLSTM-CRF) model. This model uses bidirectional LSTMs (which are excellent at capturing sequence data) to extract features from a sentence, much like the example above. It then feeds those features into the same model that the New York Times used. I felt like this model could be promising, so I decided to run with it.

### Embeddings

#### Word Embeddings

Word embeddings are a _fascinating_ topic for anybody who's interested. Simply put, word embeddings provide a way to mathematically represent the _meanings_ behind words. There's a ton of tutorials and explanations online done by people far smarter than I am, so I won't delve into all the examples everybody repeats.

I looked into using a couple of different types of pretrained word embeddings, thinking that they might give me an edge:

- [GloVe (Wikipedia 2014 + Gigaword)](https://nlp.stanford.edu/projects/glove/)
- [Fasttext](https://fasttext.cc/docs/en/english-vectors.html)

I didn't find they really helped much, so I just went with training my own embeddings.


#### Character Embeddings

Word embeddings are super cool, but tend to perform less well when you look at words that the embedding has never seen before.

For example, if the embeddings are trained on only the English language (meaning they only represent English words), how exactly are they supposed to
represent words from other languages that have never been seen before?

Character embeddings are a way to boost word embeddings to generalize for out-of-vocabulary data. What this means is that if my word embeddings don't recognize
a word, rather than giving up, they can try and "piece something together" from the characters of the word.  These kinds of embeddings have seen a lot of use
in domains like tweet analysis, where text isn't always properly written, abbreviations are used, etc.

I figured that since recipe lines were pretty short, I'd give character embeddings a shot, and I found that they helped a fair amount.


## Ending Results

Here are the results I got from my BiLSTM-CRF. The AllenNLP configuration file can be found in `config.json`

```Accuracy: 80.02842928216063%```

Remember, we're aiming for higher **macro F1 score**, rather than accuracy.

| TAG          | precision | recall | f1-score | support |
| ------------ | --------- | ------ | -------- | ------- |
| B-COMMENT    | 0.74      | 0.86   | 0.80     | 308     |
| B-NAME       | 0.86      | 0.85   | 0.85     | 489     |
| B-QTY        | 0.99      | 0.99   | 0.99     | 402     |
| B-RANGE_END  | 1.00      | 1.00   | 1.00     | 3       |
| B-UNIT       | 0.92      | 0.98   | 0.95     | 319     |
| I-COMMENT    | 0.77      | 0.74   | 0.75     | 529     |
| I-NAME       | 0.57      | 0.73   | 0.64     | 338     |
| OTHER        | 0.78      | 0.51   | 0.62     | 426     |
|              |           |        |          |         |
| micro avg    | 0.80      | 0.80   | 0.80     | 2814    |
| macro avg    | 0.83      | 0.83   | 0.83     | 2814    |
| weighted avg | 0.81      | 0.80   | 0.80     | 2814    |

The macro average F1 score is a full 3% higher than the CRF alone, which means this model achieves the goal I'm looking for!

Let's look at some examples:

| 17      | pinches  | of      | kosher   | salt     |
| ------- | -------- | ------- | -------- | -------- |
| `B-QTY` | `B-UNIT` | `OTHER` | `B-NAME` | `I-NAME` |

| A       | small   | dash     | of      | paprika  |
| ------- | ------- | -------- | ------- | -------- |
| `OTHER` | `OTHER` | `B-UNIT` | `OTHER` | `B-NAME` |

| 1       | liter    | of      | milk     |
| ------- | -------- | ------- | -------- |
| `B-QTY` | `B-UNIT` | `OTHER` | `B-NAME` |

| 1/2     | teaspoon | of      | horseradish |
| ------- | -------- | ------- | ----------- |
| `B-QTY` | `B-UNIT` | `OTHER` | `B-NAME`    |