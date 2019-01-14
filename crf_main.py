import torch
from torch.optim import SGD
from allennlp.data.dataset_readers import SequenceTaggingDatasetReader
from allennlp.data.vocabulary import Vocabulary
from allennlp.models import CrfTagger
from allennlp.modules.seq2seq_encoders import PytorchSeq2SeqWrapper
from allennlp.modules.text_field_embedders import BasicTextFieldEmbedder
from allennlp.modules.token_embedders import Embedding
from allennlp.data.iterators import BucketIterator
from allennlp.common import Params
from allennlp.training import Trainer


TRAIN_FILEPATH = "data/train.seqtags"
VALID_FILEPATH = "data/valid.seqtags"

EMBEDDING_DIM = 300
HIDDEN_DIM = 300
LEARNING_RATE = 1e-3
WEIGHT_DECAY = 1e-4
PATIENCE = 10
NUM_EPOCHS = 5

# Used to download 100dGloVe
GLOVE_EMBEDDINGS_URL = "(http://nlp.stanford.edu/data/glove.6B.zip)#glove.6B.300d.txt"


def main():
    reader = SequenceTaggingDatasetReader(token_delimiter="\t")
    training_dataset = reader.read(TRAIN_FILEPATH)
    validation_dataset = reader.read(VALID_FILEPATH)
    vocab = Vocabulary.from_instances(training_dataset + validation_dataset)

    params = Params(
        {"pretrained_file": GLOVE_EMBEDDINGS_URL, "embedding_dim": EMBEDDING_DIM}
    )
    token_embedding = Embedding.from_params(vocab, params)
    word_embeddings = BasicTextFieldEmbedder({"tokens": token_embedding})

    lstm = PytorchSeq2SeqWrapper(
        torch.nn.LSTM(EMBEDDING_DIM, HIDDEN_DIM, batch_first=True, bidirectional=True)
    )

    model = CrfTagger(vocab, text_field_embedder=word_embeddings, encoder=lstm)
    optimizer = SGD(model.parameters(), lr=LEARNING_RATE, weight_decay=WEIGHT_DECAY)

    iterator = BucketIterator(sorting_keys=[("tokens", "num_tokens")])
    iterator.index_with(vocab)

    trainer = Trainer(
        model=model,
        optimizer=optimizer,
        iterator=iterator,
        train_dataset=training_dataset,
        validation_dataset=validation_dataset,
        patience=PATIENCE,
        num_epochs=NUM_EPOCHS,
    )
    trainer.train()


if __name__ == "__main__":
    main()
