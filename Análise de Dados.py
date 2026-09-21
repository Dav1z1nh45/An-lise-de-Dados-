import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(
    page_title="Minha Loja",
    page_icon="🛒",
    layout="wide"
)

# ====================== DADOS ======================
dados = {
    "restaurante": ["Pizza Bella", "Sushi House", "Burger King", "Doce Sabor", "Pizza Bella", 
                    "China in Box", "Sushi House", "Burger King", "Doce Sabor", "China in Box"],
    "categoria": ["Pizza", "Japonesa", "Hambúrguer", "Doces", "Pizza", 
                  "Chinesa", "Japonesa", "Hambúrguer", "Doces", "Chinesa"],
    "valor": [45.90, 60.00, 35.50, 25.00, 52.30, 40.00, 75.00, 38.90, 22.50, 48.00],
    "tempo_entrega": [35, 50, 20, 15, 40, 45, 55, 25, 18, 42],
    "avaliacao": [4.5, 4.8, 4.0, 4.2, 4.6, 3.9, 4.9, 4.1, 4.3, 4.0]
}

df = pd.DataFrame(dados)

# ====================== TÍTULO ======================
st.title("🛒 Minha Loja")
st.markdown("### Análise de Pedidos")

# ====================== FILTROS ======================
st.sidebar.title("Filtros")

categoria_escolhida = st.sidebar.selectbox(
    "Categoria",
    ["Todas"] + list(df["categoria"].unique()),
    key="categoria_selectbox"
)

valor_maximo = st.sidebar.slider(
    "Valor máximo do pedido R$:",
    min_value=float(df["valor"].min()),
    max_value=float(df["valor"].max()),
    value=float(df["valor"].max()),
    key="valor_maximo_slider"
)

# ====================== APLICANDO OS FILTROS ======================
df_filtrado = df[df["valor"] <= valor_maximo]

if categoria_escolhida != "Todas":
    df_filtrado = df_filtrado[df_filtrado["categoria"] == categoria_escolhida]

# ====================== MÉTRICAS ======================
col1, col2, col3 = st.columns(3)

faturamento_total = df_filtrado["valor"].sum()
avaliacao_media = df_filtrado["avaliacao"].mean() if len(df_filtrado) > 0 else 0
qtd = len(df_filtrado)

col1.metric("Faturamento total", f"R$ {faturamento_total:.2f}")
col2.metric("Avaliação média", f"{avaliacao_media:.1f} ⭐")
col3.metric("Pedidos encontrados", qtd)

st.divider()

# ====================== TABELA ======================
st.subheader("📋 Pedidos Filtrados")
st.dataframe(df_filtrado, use_container_width=True, hide_index=True)

st.divider()

# ====================== GRÁFICO VERTICAL ======================
st.subheader("📊 Valor total por restaurante")

if len(df_filtrado) > 0:
    valor_por_restaurante = df_filtrado.groupby("restaurante")["valor"].sum().sort_values(ascending=False)
    
    # Gráfico de barras vertical
    st.bar_chart(valor_por_restaurante, height=400)
else:
    st.warning("Nenhum pedido encontrado com os filtros selecionados.")