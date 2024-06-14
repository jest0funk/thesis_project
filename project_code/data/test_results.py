import pandas as pd


def resulting_table(model_selection):
    test_results = []
    for model_reference in (model_selection):
        test_result = pd.read_json(f'test_results/{model_reference}.json', typ='series')
        test_result = pd.DataFrame({'language': test_result.index,
                                    'accuracy': test_result.values,
                                    'model': model_reference})
        test_results.append(test_result)

    test_results_df = pd.concat(test_results).pivot(index = 'model', columns='language', values='accuracy')
    columns = test_results_df.columns.to_list()
    columns = [columns[1], columns[0]] + columns[2:]
    test_results_df = test_results_df[columns] * 100
    test_results_df['mean'] = test_results_df.mean(numeric_only=True, axis=1)
    return test_results_df


def resulting_plot(resulting_table):
    resulting_table.T.plot(figsize=(15, 8))