def prefilter_items(data):
    # Уберем самые популярные товары (их и так купят)
    popularity = data.groupby('item_id')['user_id'].nunique().reset_index() / data['user_id'].nunique()
    popularity.rename(columns={'user_id': 'share_unique_users'}, inplace=True)
    
    top_popular = popularity[popularity['share_unique_users'] > 0.5].item_id.tolist()
    data = data[~data['item_id'].isin(top_popular)]
    
    # Уберем самые НЕ популярные товары (их и так НЕ купят)
    top_notpopular = popularity[popularity['share_unique_users'] < 0.01].item_id.tolist()
    data = data[~data['item_id'].isin(top_notpopular)]
    return data
    
def postfilter_items(user_id, recommednations):
    pass
    
def get_similar_items_recommendation(user, model, N=5):
    """Рекомендуем товары, похожие на топ-N купленных юзером товаров"""
    recs = model.similar_items(itemid_to_id[user], N=N)
    all_recs= [id_to_itemid[rec[0]] for rec in recs]
    return  all_recs 

def get_similar_users_recommendation(user, model, N=5):
    """Рекомендуем топ-N товаров, среди купленных похожими юзерами"""
    try:
        res = [id_to_itemid[rec[0]] for rec in model.recommend(userid=userid_to_id[user], 
                                        user_items=csr_matrix(user_item_matrix).tocsr(),   # на вход user-item matrix
                                        N=N, 
                                        filter_already_liked_items=False, 
                                        #filter_items=[itemid_to_id[999999]],  # !!! have already deleted in def prefilter_items
                                        recalculate_user=True)]
    except KeyError: 
        res = None

    return res
