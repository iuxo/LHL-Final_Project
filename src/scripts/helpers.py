def get_file_contents(filename):
    """ Given a filename, return the contents of that file
    """
    try:
        with open(filename, 'r') as f:
            # It's assumed our file contains a single line,
            # with our API key
            return f.read().strip()
    except FileNotFoundError:
        print("'%s' file not found" % filename)

class DiffTransformer():

    # here you define the operation it should perform
    def transform(self, X, y=None, **fit_params):
        columns_to_drop = []
        for b_column, r_column in zip(X.columns[:11], X.columns[11:]):
            feature_name = b_column[5:]+"_diff"
            X[feature_name] = X[b_column] - X[r_column]
            columns_to_drop.append(b_column)
            columns_to_drop.append(r_column)
        return X.drop(columns_to_drop, axis = 1)

    # just return self
    def fit(self, X, y=None, **fit_params):
        return self