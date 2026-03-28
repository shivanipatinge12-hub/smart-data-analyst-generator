import pandas as pd
def get_best_model(results):
    best_model = max(results, key=results.get)
    best_score = results[best_model]
    return best_model, best_score
def results_to_df(results):
    df = pd.DataFrame(list(results.items()), columns=["Model", "Score"])
    return df
def sort_results(results):
    sorted_results = dict(sorted(results.items(), key=lambda x: x[1], reverse=True))
    return sorted_results