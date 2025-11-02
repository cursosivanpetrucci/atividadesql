# =========================================
# ATIVIDADE: RELACIONAMENTOS SQL + PYTHON
# =========================================
# App em Streamlit desenvolvido para prática
# Autor: Prof. Ivan Sanches
# =========================================

import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

# =========================================
# CONFIGURAÇÃO DA PÁGINA
# =========================================
st.set_page_config(
    page_title="Atividade SQL + Python",
    layout="wide",
    page_icon="📊"
)

st.title("📊 Atividade Prática — SQL, Relacionamentos e Análise de Dados")
st.markdown("""
**Objetivo:** Trabalhar com **duas tabelas relacionadas (produtos e vendas)**, 
gerando análises e gráficos a partir de consultas SQL e integração com Python.
""")

# =========================================
# CRIAÇÃO DO BANCO DE DADOS
# =========================================
con = sqlite3.connect(":memory:")
cur = con.cursor()

sql_script = """
DROP TABLE IF EXISTS vendas;
DROP TABLE IF EXISTS produtos;

CREATE TABLE produtos (
    id_produto INTEGER PRIMARY KEY,
    nome_produto TEXT,
    categoria TEXT,
    preco_unitario FLOAT
);

CREATE TABLE vendas (
    id_venda INTEGER PRIMARY KEY,
    id_produto INTEGER,
    quantidade INTEGER,
    data_venda DATE,
    desconto FLOAT,
    FOREIGN KEY (id_produto) REFERENCES produtos(id_produto)
);

INSERT INTO produtos (id_produto, nome_produto, categoria, preco_unitario) VALUES
(1, 'Notebook Dell', 'Informática', 3500.00),
(2, 'Mouse Logitech', 'Acessórios', 120.00),
(3, 'Monitor LG 24"', 'Informática', 950.00),
(4, 'Teclado Mecânico', 'Acessórios', 420.00),
(5, 'Headset Gamer', 'Acessórios', 480.00),
(6, 'Impressora HP', 'Periféricos', 800.00),
(7, 'Smartphone Samsung', 'Telefonia', 2900.00),
(8, 'Cabo HDMI 2m', 'Acessórios', 40.00),
(9, 'Webcam Logitech', 'Acessórios', 310.00),
(10, 'Roteador TP-Link', 'Redes', 250.00),
(11, 'SSD Kingston 480GB', 'Armazenamento', 380.00),
(12, 'HD Externo 1TB', 'Armazenamento', 420.00),
(13, 'Tablet Lenovo', 'Informática', 1300.00),
(14, 'Monitor Samsung 27"', 'Informática', NULL),
(15, 'Caixa de Som JBL', NULL, 550.00);

INSERT INTO vendas (id_venda, id_produto, quantidade, data_venda, desconto) VALUES
(1, 1, 3, '2025-10-01', 50.00),
(2, 2, 5, '2025-10-02', 0.00),
(3, 3, 2, '2025-10-03', NULL),
(4, 4, 1, '2025-10-04', 20.00),
(5, 5, 4, '2025-10-05', 15.00),
(6, 6, 2, '2025-10-06', 0.00),
(7, 7, 1, '2025-10-07', 200.00),
(8, 8, 10, '2025-10-08', NULL),
(9, 9, 3, '2025-10-09', 30.00),
(10, 10, 2, '2025-10-10', 10.00),
(11, 11, 5, '2025-10-11', 0.00),
(12, 12, 3, '2025-10-12', 25.00),
(13, 13, 1, '2025-10-13', 0.00),
(14, 14, 2, '2025-10-14', 50.00),
(15, 15, 6, '2025-10-15', NULL),
(16, 1, 1, '2025-10-16', 0.00),
(17, 3, 4, '2025-10-17', 30.00),
(18, 5, 2, '2025-10-18', NULL),
(19, 7, 2, '2025-10-19', 150.00),
(20, 8, NULL, '2025-10-20', 0.00),
(21, 9, 1, '2025-10-21', NULL),
(22, 10, 3, '2025-10-22', 0.00),
(23, 11, NULL, '2025-10-23', 20.00),
(24, 12, 2, '2025-10-24', 0.00),
(25, 13, 1, '2025-10-25', 10.00),
(26, 14, NULL, '2025-10-26', NULL),
(27, 15, 5, '2025-10-27', 0.00),
(28, NULL, 2, '2025-10-28', 0.00),
(29, 6, 1, '2025-10-29', 0.00),
(30, 2, 4, '2025-10-30', 10.00);
"""
cur.executescript(sql_script)

# =========================================
#  EXIBIR AS TABELAS ORIGINAIS
# =========================================
st.subheader("📋 Tabelas Originais")
col1, col2 = st.columns(2)

with col1:
    produtos = pd.read_sql_query("SELECT * FROM produtos", con)
    st.markdown("**Tabela: Produtos**")
    st.dataframe(produtos)

with col2:
    vendas = pd.read_sql_query("SELECT * FROM vendas", con)
    st.markdown("**Tabela: Vendas**")
    st.dataframe(vendas)

# =========================================
# CONSULTA COM RELACIONAMENTO
# =========================================
query = """
SELECT
    v.id_venda,
    p.nome_produto,
    p.categoria,
    v.quantidade,
    p.preco_unitario,
    v.desconto,
    v.data_venda,
    (v.quantidade * p.preco_unitario) - v.desconto AS valor_total
FROM vendas v
LEFT JOIN produtos p ON v.id_produto = p.id_produto;
"""
df = pd.read_sql_query(query, con)

st.subheader("🔗 Consulta Relacional com Coluna Calculada")
st.dataframe(df)

# =========================================
#  TRATAMENTO DE NULOS
# =========================================
st.subheader("🧹 Tratamento de Dados (valores nulos)")
df["categoria"].fillna("Sem Categoria", inplace=True)
df["quantidade"].fillna(0, inplace=True)
df["preco_unitario"].fillna(df["preco_unitario"].mean(), inplace=True)
df["desconto"].fillna(0, inplace=True)
df["valor_total"].fillna(0, inplace=True)

st.markdown("Valores nulos tratados com regras básicas. Veja o resultado:")
st.dataframe(df)

# =========================================
# 5️⃣ ANÁLISES E GRÁFICOS
# =========================================
st.subheader("📊 Análises e Visualizações")

# Faturamento por categoria
fat_categoria = df.groupby("categoria")["valor_total"].sum().reset_index()
fig1 = px.bar(fat_categoria, x="categoria", y="valor_total",color="categoria",
              title="💰 Faturamento por Categoria")

# Evolução temporal
fig2 = px.line(df, x="data_venda", y="valor_total",
               title="📈 Evolução do Faturamento Diário")

# Produtos mais vendidos
top_produtos = df.groupby("nome_produto")["valor_total"].sum().reset_index().sort_values(by="valor_total", ascending=False).head(10)
fig3 = px.bar(top_produtos, x="nome_produto", y="valor_total",
              title="🏆 Top 10 Produtos Mais Lucrativos")

st.plotly_chart(fig1, use_container_width=True)
st.plotly_chart(fig2, use_container_width=True)
st.plotly_chart(fig3, use_container_width=True)

# =========================================
# 6️⃣ INSTRUÇÕES PARA OS ALUNOS
# =========================================
st.markdown("---")
st.subheader("📘 Instruções da Atividade")

st.markdown("""
### Etapas sugeridas:
1. **Explore os dados** das tabelas `produtos` e `vendas`.
2. **Observe os relacionamentos** entre as tabelas.
3. **Analise a consulta SQL** que faz o JOIN e cria a coluna `valor_total`.
4. **Trate os valores nulos** de forma adequada.
5. **Gere novas análises e gráficos**, como:
   - Faturamento médio por categoria.
   - Produto com maior número de vendas.
   - Dias de pico de faturamento.
6. **Elabore conclusões** sobre os padrões identificados nos dados.

💡 **Desafio extra:** adicione novos filtros (por data ou categoria) e exporte o DataFrame final em CSV.
""")

st.markdown("---")
st.caption("Desenvolvido para fins educacionais — Curso de Análise com Python.")
