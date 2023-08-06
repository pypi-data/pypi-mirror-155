import pandas as pd
import scanpy as sc
import os
import scipy.io


def read_10X_multi(matrix_dir: str):
    r"""
    matrix_dir: downloaded from 10x website, containing matrix.mtx.gz, barcodes.tsv.gz and features.tsv.gz
    """
    mat_path = os.path.join(matrix_dir, "matrix.mtx.gz")
    mat = scipy.io.mmread(mat_path)

    features_path = os.path.join(matrix_dir, "features.tsv.gz")
    features = pd.read_table(features_path, header=None)
    features.columns = ['feature_id', 'feature_name', 'feature_type', 'chrom', 'chromStart', 'chromEnd']
    features.index = features.feature_id.values
    features = features.drop('feature_id', axis=1)
    
    barcodes_path = os.path.join(matrix_dir, "barcodes.tsv.gz")
    barcodes = pd.read_table(barcodes_path, header=None)
    barcodes.columns = ['barcode']
    barcodes.index = barcodes.barcode.values
    barcodes = barcodes.drop('barcode', axis=1)

    adata = sc.AnnData(X=mat.tocsr().transpose(), obs=barcodes, var=features)
    adata.obs.index = adata.obs.index.str[:-2]

    ad_r, ad_a = adata[:,adata.var.feature_type=='Gene Expression'], adata[:,adata.var.feature_type=='Peaks']

    ad_r.var = ad_r.var.rename(columns={'feature_name':'gene_name'}).drop('feature_type', axis=1)
    ad_a.var = ad_a.var.rename(columns={'feature_name':'peak'}).drop('feature_type', axis=1)

    return ad_r, ad_a


def make_gene_symbols_unique(adata: sc.AnnData) -> sc.AnnData:
    #TODO
    pass


def get_ncells_from_h5ad(h5ad_path: str) -> int:
    return len(sc.read(h5ad_path).obs)