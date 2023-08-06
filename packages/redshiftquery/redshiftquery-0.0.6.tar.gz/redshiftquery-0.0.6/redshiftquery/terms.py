from redshiftquery import query as q 
import pandas as pd


def get_three_term_list():
    '''
    Used to generate a pandas DataFrame with terms in order
    No winter terms are included use the index of the DataFrame to do term 
    calculations rather than using the ID in the DataFrame
    '''
    
    return q.exquery("Select term, term_season, fiscal_year, time_strm, term_begin_dt from iss_sboyer9.terms where term_season <> 'Winter'")


def get_four_term_list() -> pd.DataFrame():
    '''
    Used to generate a pandas DataFrame with terms in order
    Winter terms are included use the index of the DataFrame to do term 
    calculations rather than using the ID in the DataFrame
    '''
    
    return q.exquery("Select term, term_season, fiscal_year, time_strm, term_begin_dt from iss_sboyer9.terms")

def get_last_n_terms(beginterm: str, n: int, gr4t: bool = False) -> []:
    if gr4t == True:
        termlist = get_four_term_list()
    else:
        termlist = get_three_term_list()
    return termlist.iloc[termlist.index[termlist['term']==beginterm][0] - n: termlist.index[termlist['term']==beginterm][0]]['term'].to_list()