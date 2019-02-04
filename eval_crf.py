from sklearn.metrics import classification_report, accuracy_score


def read_tags(filepath: str):
    tags = []
    with open(filepath) as f:
        examples = f.read().split("\n\n")
        for example in examples:
            for line in example.split("\n"):
                if line.strip():
                    *_, tag = line.split()
                    tags.append(tag)
    return tags


true_tags = read_tags("data/crf_results/test.tags")
pred_tags = read_tags("data/crf_results/results.txt")
print(f"Accuracy: {accuracy_score(true_tags, pred_tags) * 100}%")
print(classification_report(true_tags, pred_tags))

