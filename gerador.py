import streamlit as st
import pandas as pd
from faker import Faker
import random

fake = Faker("pt_BR")

st.title("Gerador de Bases - Ivan ")

# Escolhas iniciais
area = st.selectbox("Escolha o tema:", ["Alunos", "Saúde"])
qtd = st.slider("Quantas linhas quer gerar?", min_value=10, max_value=1000, step=10, value=10)

st.markdown("---")
st.subheader("Campos personalizados")

# Quantos campos personalizados o usuário quer adicionar
num_campos = st.number_input("Quantos campos adicionais deseja criar?", min_value=0, step=1)

# Lista que armazenará as definições dos novos campos
novos_campos = []

for i in range(num_campos):
    st.markdown(f"**Campo {i+1}**")
    nome = st.text_input(f"Nome do campo {i+1}", key=f"nome_{i}")
    tipo = st.radio(
        f"Tipo de geração do campo {i+1}",
        ["Números aleatórios", "Lista de valores"],
        key=f"tipo_{i}",
        horizontal=True
    )

    if tipo == "Números aleatórios":
        min_val = st.number_input(f"Valor mínimo do campo {nome}", value=0, key=f"min_{i}")
        max_val = st.number_input(f"Valor máximo do campo {nome}", value=10, key=f"max_{i}")
        novos_campos.append({
            "nome": nome,
            "tipo": "numerico",
            "min": min_val,
            "max": max_val
        })

    else:
        lista = st.text_area(
            f"Digite os valores possíveis (separe por vírgula)",
            key=f"lista_{i}"
        )
        valores = [x.strip() for x in lista.split(",") if x.strip()]
        novos_campos.append({
            "nome": nome,
            "tipo": "lista",
            "valores": valores
        })

st.markdown("---")

# Função geradora
def gerar_dados(area, qtd, novos_campos):
    dados = []

    for _ in range(qtd):
        if area == "Alunos":
            linha = {
                "Data": fake.date_this_year(),
                "Alunos": fake.name(),
                "Nota": round(random.uniform(1, 10), 1),
                "Disciplina": random.choice(["Historia", "Fisica", "Geografia"])
            }
        elif area == "Saúde":
            linha = {
                "Data": fake.date_this_year(),
                "Paciente": fake.name(),
                "Especialidade": random.choice(["Pediatria", "Otorrino", "Cardiologia"]),
                "Convênio": random.choice(["Particular", "Empresa", "SUS"])
            }

        # Adiciona os campos personalizados
        for campo in novos_campos:
            if campo["tipo"] == "numerico":
                linha[campo["nome"]] = round(random.uniform(campo["min"], campo["max"]),0)
            elif campo["tipo"] == "lista" and campo["valores"]:
                linha[campo["nome"]] = random.choice(campo["valores"])
            else:
                linha[campo["nome"]] = None

        dados.append(linha)

    return pd.DataFrame(dados)

# Botão para gerar
if st.button("Gerar Dados"):
    df = gerar_dados(area, qtd, novos_campos)
    df = df.sort_values(df.columns[1]).reset_index(drop=True)
    st.dataframe(df, hide_index=True)

    csv= df.to_csv(index=False).encode("utf-8")
    
    st.download_button(
        label="Baixar planilha",
        data=csv,
        file_name=f'dados_{area.lower()}.csv',
        mime="text/csv"
    )


