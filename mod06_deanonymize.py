import pandas as pd

def load_data(anonymized_path, auxiliary_path):
    """
    Load anonymized and auxiliary datasets.
    """
    anon = pd.read_csv(anonymized_path)
    aux = pd.read_csv(auxiliary_path)
    return anon, aux


def link_records(anon_df, aux_df):
    """
    Attempt to link anonymized records to auxiliary records
    using exact matching on quasi-identifiers.

    Returns a DataFrame with columns:
      anon_id, matched_name
    containing ONLY uniquely matched records.
    """
    identifiers = ["age", "gender", "zip3"]
    
    #count how often each combo appears in each dataset
    anon_counts = anon_df.groupby(identifiers).size()
    aux_counts = aux_df.groupby(identifiers).size()
    
    #keep combos that appear exactly once in both
    unique_anon = anon_df.merge(anon_counts[anon_counts == 1].reset_index()[identifiers], on=identifiers)
    unique_aux = aux_df.merge(aux_counts[aux_counts == 1].reset_index()[identifiers], on=identifiers)
    
    #match uniquely occuring combos
    matches = unique_anon.merge(unique_aux, on=identifiers)
    
    matches = matches[["anon_id", "name"]]
    return matches.rename(columns={"name": "matched_name"})
    #raise NotImplementedError


def deanonymization_rate(matches_df, anon_df):
    """
    Compute the fraction of anonymized records
    that were uniquely re-identified.
    """
    if len(anon_df) == 0:
        return 0.0
    return len(matches_df) / len(anon_df)
    #raise NotImplementedError
