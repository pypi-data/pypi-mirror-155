import pandas as pd
import seaborn as sns
import numpy as np
from sklearn import metrics
import matplotlib.pyplot as plt
from ds_utils.metrics import plot_confusion_matrix as _plot_confusion_matrix, visualize_accuracy_grouped_by_probability
from . import xproblem, xpd


def plot_feature_importances(folds, title=''):
    df = xproblem.calc_feature_importances(folds, flat=True)
    if df is None:
        return

    fis = df.groupby('feature_name')['feature_importance'].mean()
    df = xpd.x_sort_on_lookup(df, 'feature_name', fis, ascending=True)
    sns.catplot(data=df, y='feature_name', x='feature_importance')
    plt.xlim([0, None])
    if title:
        plt.title(title)

    plt.tight_layout()
    plt.show()

    return


def plot_roc_curve(y_true, y_score, title=''):
    auc = metrics.roc_auc_score(y_true, y_score)
    fper, tper, thresholds = metrics.roc_curve(y_true, y_score)
    plt.plot(fper, tper, color='orange', label='ROC')
    plt.plot([0, 1], [0, 1], color='darkblue', linestyle='--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')

    title2 = f'ROC Curve (AUC={auc:.3f})'
    if title:
        title2 = f"{title}: {title2}"

    plt.title(title2)
    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_confusion_matrix(y_true, y_pred, labels=None, title=''):
    y_true = pd.Series(y_true)
    counts = sorted([(l, c) for l, c in y_true.value_counts().items()])
    counts_str = ", ".join([f"{l}={c}" for l, c in counts])

    labels = labels or sorted(y_true.unique())

    _plot_confusion_matrix(y_true, y_pred, labels=labels)

    title2 = f"Counts: {counts_str} (total={len(y_true)})"
    if title:
        title2 = f"{title}: {title2}"

    plt.title(title2)

    plt.tight_layout()
    plt.show()


def plot_model_scores(y_true, y_score, bins=25, title=''):
    """
    Useful of comparing model scores for the different targets
    """

    df = pd.DataFrame({'Target': y_true, 'Model Score': y_score})
    sns.histplot(data=df, x='Model Score', hue='Target', element="step", common_norm=False, stat='percent', bins=bins)

    title2 = 'Histogram of model scores'
    if title:
        title2 = f"{title}: {title2}"

    plt.title(title2)
    plt.tight_layout()
    plt.show()


def plot_score_comparison(scores: dict, key_label='Dataset', score_label='Model Score', bins=25, title=''):
    """
    Useful for comparing the scores of various datasets:
    > plot_score_comparison({'train': train_scores, 'test': test_scores, 'blind': blind_scores)
    """

    rows = []
    for k, scores in scores.items():
        for score in scores:
            rows.append({key_label: k, score_label: score})

    df = pd.DataFrame(rows)
    sns.histplot(data=df, x=score_label, hue=key_label, element="step", common_norm=False, stat='percent', bins=bins)

    title2 = f'Histogram of model scores per {key_label}'
    if title:
        title2 = f"{title}: {title2}"

    plt.title(title2)
    plt.tight_layout()
    plt.show()


def plot_model_scores_ratios(y_true, y_score, bins=25, ratio_of=1):
    df = pd.DataFrame({'target': y_true, 'score': y_score})
    s_min = y_score.min()
    s_max = y_score.max()
    s_range = s_max - s_min
    borders = np.linspace(s_min, s_max+s_range*.0001, bins+1)

    rows = []
    for s_start, s_end in zip(borders[:-1], borders[1:]):
        s_mid = (s_start + s_end) / 2
        df_g = df[(df.score >= s_start) & (df.score < s_end)]
        if len(df_g) == 0:
            continue

        r = (df_g.target == ratio_of).sum() / len(df_g)
        rows.append({'s_start': df_g.score.min(), 's_end': df_g.score.max(), 'ratio': r})

    df_rows = pd.DataFrame(rows)

    for row in df_rows.itertuples():
        plt.plot([row.s_start, row.s_end], [row.ratio, row.ratio], color='black')

    plt.title('Histogram of model scores')
    plt.tight_layout()
    plt.show()


def plot_corr_heatmap(df, title='Correlation Heatmap', fontsize=12, pad=12, cmap='BrBG', figsize=(15,15)):
    """
    Credits: https://medium.com/@szabo.bibor/how-to-create-a-seaborn-correlation-heatmap-in-python-834c0686b88e
    """

    plt.subplots(figsize=figsize)
    df_corr = df.corr()
    mask = np.triu(np.ones_like(df_corr, dtype=np.bool))

    hm = sns.heatmap(df_corr, vmin=-1, vmax=1, annot=True, cmap=cmap, mask=mask)
    hm.set_title(title, fontdict={'fontsize': fontsize}, pad=pad)
    plt.tight_layout()
    plt.show()


def plot_pie(vals, title=''):
    vals = pd.Series(vals)
    counts = vals.value_counts()

    plt.figure(figsize=(6, 6))
    plt.pie(counts.values, labels=counts.index.values, autopct='%1.1f%%', shadow=False, startangle=0)

    if title:
        plt.title(title)

    plt.tight_layout()
    plt.show()


def plot_counts(df, on):
    counts = df[on].value_counts()
    counts = counts.sort_values(ascending=False)
    plt.title(f"Counts on {on}")
    plt.scatter(np.arange(len(counts)), counts.values, s=2)
    plt.ylabel('counts')
    plt.xlabel(f"{on} sorted by counts")
    plt.tight_layout()
    plt.show()
