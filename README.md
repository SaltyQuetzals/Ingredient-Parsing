# Ingredient Parsing

A while ago, I stumbled upon a [fantastic write-up](https://open.blogs.nytimes.com/2015/04/09/extracting-structured-data-from-recipes-using-conditional-random-fields/) 
from the New York Times about structured predictions using conditional random
fields (CRFs). However, if you look at when the article was released, you'll
notice it was released in 2015. At the time of writing, that's over 3 years ago.
NLP has come a long way since then, with the advent of LSTMs, word embeddings,
and sequence-to-sequence modelling. I firmly believe that the use of recurrent
neural networks can improve upon the overall ability of the tagger.

## Reproduction

The computer I'm currently using to train my model has an Intel Core i5 processor and a NVIDIA GEFORCE GTX 1070 GPU. Training 

### Experiment Data

I've included the data I used to train my model, which can be found in the `data` folder.

In addition, the original New York Times CSV file that I partitioned into my datasets can be found there as well.

All files ending in `.tags` are CRF++-formatted files, all ending in `.seqtags` are formatted in AllenNLP [`SequenceTaggingDatasetReader`](https://allenai.github.io/allennlp-docs/api/allennlp.data.dataset_readers.sequence_tagging.html)-requested format. These are used as the input to my model.

### Generating Your Own Data

If you want to run the experiment with a different dataset, simply remove everything from the `data` directory except for `nyt-ingredients-snapshot-2015.csv`,
and type:

```bash
./create_data.sh
```

### Training the BiLSTM-CRF Yourself

Due to the nature of LSTMs, training this model on a CPU will take a while. If you're okay with the wait, go ahead and train away! Otherwise, I'd recommend using a GPU for training, or [loading the pre-built model from an archive](https://allenai.github.io/allennlp-docs/api/allennlp.predictors.html#allennlp.predictors.predictor.Predictor.from_archive).

To train the model (assuming you have [AllenNLP installed](https://github.com/allenai/allennlp)), simply type

```bash
allennlp train config.jsonnet -s <your desired serialization folder here>
```

### Training the CRF

Assumptions:

- You have Docker installed
- You are okay with waiting a bit for the CRF to train (like an hour) on your CPU (no GPU options available)
- You have the dataset provided or have [generated your own data](#generating-your-own-data).

If, for whatever reason, you'd like to train the CRF, you can do so by typing:

```bash
./evaluate_crf.sh
```

This script will create two files in `data/crf_results`, `results.txt`, and `test.tags`.

In `results.txt`, you'll notice that the input looks something like...

```
# 0.391376
1	I1	L12	NoCAP	NoPAREN	B-QTY/0.989924
cup	I2	L12	NoCAP	NoPAREN	B-UNIT/0.960915
carrot	I3	L12	NoCAP	NoPAREN	B-NAME/0.959627
juice	I4	L12	NoCAP	NoPAREN	I-NAME/0.951555
```

Any line prefixed with a `#` sign must be removed, and everything after (and including) the `/` character should also be removed.
After processing, the file should look more like:

```
1	I1	L12	NoCAP	NoPAREN	B-QTY
cup	I2	L12	NoCAP	NoPAREN	B-UNIT
carrot	I3	L12	NoCAP	NoPAREN	B-NAME
juice	I4	L12	NoCAP	NoPAREN	I-NAME
```

This can be done with a couple solid find-and-replace operations, so I'll leave that up to you.

## Goals

### Beat the NYT

Conditional random fields are _surprisingly_ effective at tagging these
sentences. I want to beat the NYT's model, and not by just a little, but by a significant margin.

### Learn RNNs

I'm tired of just blindly bumbling around when using deep learning. I want to
build something, and know _why_ I built it. Up until now, it's been mostly
trial-and-error. I'd like to be able to at least justify my system architecture
and learn a little more about the space of sequence tagging.

## Thought Process

For more about my decision-making process, check out [PROCESS.md](PROCESS.md).
