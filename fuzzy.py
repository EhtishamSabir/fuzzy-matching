import pandas as pd
from thefuzz import fuzz


def remove_duplicates_inplace(Df, groupby=[], similarity_field='', similar_level=85):
    df = Df.copy(True)

    def check_simi(d):
        dupl_indexes = []
        for i in range(len(d.values)):
            for j in range(i + 1, len(d.values)):
                if fuzz.token_sort_ratio(d.values[i], d.values[j]) >= similar_level:
                    dupl_indexes.append((d.index[j], fuzz.token_sort_ratio(d.values[i], d.values[j])))

        return dupl_indexes

    indexes = df.groupby(groupby).apply(check_simi)
    print('duplicates found')
    scores = []
    for index_list in indexes:
        for index, score in index_list:
            try:
                df.drop(index, inplace=True)
                scores.append(score)
            except:
                print('index not found')

    return df, scores


if __name__ == '__main__':
    # file = input('excel/csv file name : ')
    file = "test.csv"
    Df = pd.read_csv(file, low_memory=False, encoding="utf")
    print('file read sucessfull')
    df, scores = remove_duplicates_inplace(Df, groupby=['RECIP_FIRST_NAME',"RECIP_LAST_NAME"], similar_level=60)
    print('duplicates removed')
    newdf = Df.drop(df.index)
    newdf["Duplicate Score"] = scores
    print('writing files')
    df.to_csv('refined.csv')
    newdf.to_csv('duplicated.csv')
