import pandas as pd
import xarray as xr


def transfer_cluster_annot(prev_cluster,
                           cur_cluster,
                           confident=0.9,
                           less_confident=0.5,
                           null_name=''):
    """
    Transfer cluster annotation from previous clustering annotation to new clustering assignments.

    Parameters
    ----------
    prev_cluster
        Previous clustering annotation.
    cur_cluster
        Current unannotated clustering assignments.
    confident
        Confidence threshold for directly transferring annotation.
    less_confident
        Confidence threshold for transferring annotation with a ratio suffix,
        this is for the convenience of manual review.
    null_name
        Name for the null cluster where overlapping with prev_cluster is < less_confident.

    Returns
    -------
    Dictionary of cluster annotation map to cur_cluster categories.
    """

    if isinstance(prev_cluster, xr.DataArray):
        prev_cluster = prev_cluster.to_pandas()

    if isinstance(cur_cluster, xr.DataArray):
        cur_cluster = cur_cluster.to_pandas()

    prev_cluster = prev_cluster.reindex(cur_cluster.index)
    prev_cluster.fillna(null_name, inplace=True)

    table = pd.DataFrame({'cur': cur_cluster, 'prev': prev_cluster})
    counts = table.value_counts().unstack().fillna(0).astype(int)
    ratio = counts / counts.sum(axis=1).values[:, None]

    cluster_map = {}
    for cur, row in ratio.iterrows():
        max_ratio = row.max()
        max_cluster = row.index[row.argmax()]
        if max_ratio > confident:
            cluster_map[cur] = max_cluster
        elif max_ratio > less_confident:
            cluster_map[cur] = max_cluster + f'_{int(max_ratio * 100)}'
        else:
            cluster_map[cur] = null_name
    return cluster_map
