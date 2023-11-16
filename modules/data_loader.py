import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

def load_player_data(filepath):
    df = pd.read_parquet(filepath)

    categorical_cols = ['player']  # Exemplo colunas categóricas
    numeric_cols = ['nota_aliado', 'nota_eixo']  # Colunas numéricas

    numeric_imputer = SimpleImputer(strategy='mean')

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse=False))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_imputer, numeric_cols),
            ('cat', categorical_transformer, categorical_cols)
        ])

    df_transformed = preprocessor.fit_transform(df)

    columns = numeric_cols + preprocessor.named_transformers_['cat']['onehot'].get_feature_names_out(categorical_cols).tolist()

    df_transformed = pd.DataFrame(df_transformed, columns=columns)

    return df_transformed
