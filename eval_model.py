from sklearn import metrics
from allennlp import models, predictors, data


def main():
    archive = models.load_archive("models/no_pretrained/model.tar.gz", cuda_device=0)
    predictor = predictors.SentenceTaggerPredictor.from_archive(archive)

    token_indexers = {
        "tokens": data.token_indexers.SingleIdTokenIndexer(lowercase_tokens=True),
        "token_characters": data.token_indexers.TokenCharactersIndexer(
            character_tokenizer=data.tokenizers.CharacterTokenizer(
                lowercase_characters=True
            )
        ),
    }
    reader = data.dataset_readers.SequenceTaggingDatasetReader(
        token_delimiter="\t", token_indexers=token_indexers
    )

    test_data = reader.read("data/test.seqtags")

    true_tags = []
    pred_tags = []
    for instance in test_data:
        try:
            prediction = predictor.predict_instance(instance)
            true_tags += list(instance.fields["tags"])
            pred_tags += prediction["tags"]
        except RuntimeError:
            pass
    print(f"Accuracy: {metrics.accuracy_score(true_tags, pred_tags)*100}%")
    print(metrics.classification_report(true_tags, pred_tags))


if __name__ == "__main__":
    main()
