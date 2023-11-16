import pandas as pd
import streamlit as st

# Ler o CSV
df = pd.read_csv("dataset/iron_players.csv")  # Use barras invertidas (/) em vez de barras normais (\) para caminhos de arquivos em Python

# Converter para Parquet
df.to_parquet("dataset/iron_players.parquet", engine='pyarrow')  # Adicione o nome do arquivo parquet


