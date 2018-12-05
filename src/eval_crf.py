import matplotlib.pyplot as plt
import numpy as np
import itertools
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.preprocessing import OneHotEncoder

from open_seq_data import TAG_MAP, read_crf_file


def to_categorical(category):
    categorical_vector = [0] * 9
    categorical_vector[category] = 1
    return categorical_vector


def concat_predictions(tags):
    results = []
    for taglist in tags:
        for tag in taglist:
            results.append(to_categorical(tag))
    return results


def plot_confusion_matrix(
    cm, classes, normalize=False, title="Confusion matrix", cmap=plt.cm.Blues
):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype("float") / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print("Confusion matrix, without normalization")

    print(cm)

    plt.imshow(cm, interpolation="nearest", cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = ".2f" if normalize else "d"
    thresh = cm.max() / 2.0
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(
            j,
            i,
            format(cm[i, j], fmt),
            horizontalalignment="center",
            color="white" if cm[i, j] > thresh else "black",
        )

    plt.ylabel("True label")
    plt.xlabel("Predicted label")
    plt.tight_layout()


def main():
    _, pred_tags = zip(*read_crf_file("../results.txt"))
    _, actual_tags = zip(*read_crf_file("../test_truths.txt"))

    pred_results = np.array(concat_predictions(pred_tags))
    actual_results = np.array(concat_predictions(actual_tags))
    print(f"Accuracy: {accuracy_score(pred_results, actual_results)*100}%")

    print(
        classification_report(pred_results, actual_results, target_names=TAG_MAP.keys())
    )
    conf = confusion_matrix(pred_results.argmax(axis=1), actual_results.argmax(axis=1))
    plot_confusion_matrix(conf, classes=TAG_MAP.keys())
    plt.show()


if __name__ == "__main__":
    main()
