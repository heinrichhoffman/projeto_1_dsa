import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns    
from datetime import datetime, timedelta  

# Mini Projeto 1 DSA - Análise Exploratória de Dados    

data_set = 'vendas_finais.csv'

df_vendas = pd.read_csv(data_set)

df_vendas.describe()
df_vendas.info()

#ID_Pedido, Data_Pedido, Nome_Produto, Categoria, Preco_Unitario, Quantidade, ID_Cliente, Cidade, Estado 

df_vendas['Data_Pedido'] = pd.to_datetime(df_vendas['Data_Pedido'])



# Primeiro objetivo = Descobrir o faturamento e  quais são os produtos mais vendidos


df_vendas['Faturamento'] = df_vendas['Preco_Unitario'] * df_vendas['Quantidade']   

mais_vendidos = df_vendas.groupby('Nome_Produto')['Faturamento'].sum().sort_values(ascending=True)

sns.set_style("whitegrid")

plt.figure(figsize = (12, 7))

mais_vendidos.plot(kind = 'barh', color = 'skyblue')

plt.title('Top 10 Produtos Mais Vendidos por Faturamento', fontsize = 16)
plt.xlabel('Faturamento Total (R$)', fontsize = 12)
plt.ylabel('Produto', fontsize = 12)

plt.tight_layout()
plt.savefig('1_top_produtos.png', dpi=300, bbox_inches='tight') # Salva a imagem
plt.show()

# Primeiro objetivo OK 

# Segundo objetivo = Analisar o comportamento de vendas ao longo do tempo (Faturamento mensal)


df_vendas['Mes'] = df_vendas['Data_Pedido'].dt.to_period('M')

faturamento_mensal = df_vendas.groupby('Mes')['Faturamento'].sum()
faturamento_mensal.index = faturamento_mensal.index.strftime('%Y-%m')

plt.figure(figsize = (12, 6))

plt.plot(faturamento_mensal.index, faturamento_mensal.values, 
         marker = 'o', linestyle = '-', color = 'green', linewidth = 2, label = 'Faturamento')

plt.fill_between(faturamento_mensal.index, faturamento_mensal.values, color = 'green', alpha = 0.2)

plt.title('Evolução do Faturamento Mensal', fontsize = 16, fontweight = 'bold')
plt.xlabel('Mês', fontsize = 12)
plt.ylabel('Faturamento (R$)', fontsize = 12)

plt.xticks(rotation = 45)
plt.grid(True, which = 'both', linestyle = '--', linewidth = 0.5, alpha = 0.7)
plt.ylim(0, faturamento_mensal.max() * 1.1)

plt.tight_layout()
plt.savefig('2_evolucao_mensal.png', dpi=300, bbox_inches='tight') # Salva a imagem
plt.show()

# Segundo objetivo OK   

# Terceiro objetivo = Analisar a distribuição geográfica das vendas (Faturamento por Estado)

faturamento_estado = df_vendas.groupby('Estado')['Faturamento'].sum().sort_values(ascending=False).reset_index()

plt.figure(figsize=(12, 7))
sns.set_style("white")

ax = sns.barplot(
    data=faturamento_estado, 
    x='Estado', 
    y='Faturamento', 
    palette='Blues_d', 
    hue='Estado', 
    legend=False
)

plt.title('Faturamento Total por Estado', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Estado', fontsize=12)
plt.ylabel('Faturamento (R$)', fontsize=12)

for p in ax.patches:
    height = p.get_height()
    ax.annotate(f'R$ {height:,.2f}',
                (p.get_x() + p.get_width() / 2., height),
                ha='center', va='bottom',
                xytext=(0, 5),
                textcoords='offset points',
                fontsize=10)

sns.despine(left=True)
plt.yticks([])
plt.tight_layout()
plt.savefig('3_faturamento_por_estado.png', dpi=300, bbox_inches='tight') # Salva a imagem
plt.show()

# terceiro objetivo OK

# Quarto objetivo = Faturamento por categoria de produto

faturamento_categoria = df_vendas.groupby('Categoria')['Faturamento'].sum().sort_values(ascending=False).reset_index()

plt.figure(figsize=(12, 7))

ax2 = sns.barplot(
    data=faturamento_categoria,
    x='Categoria',
    y='Faturamento',
    palette='viridis',
    hue='Categoria',
    legend=False
)

plt.title('Faturamento Por Categoria', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Categoria', fontsize=12)
plt.ylabel('Faturamento (R$)', fontsize=12)

for p in ax2.patches:
    height = p.get_height()
    ax2.annotate(f'R$ {height/1000:.1f}K',
                (p.get_x() + p.get_width() / 2., height),
                ha='center', va='bottom',
                xytext=(0, 5),
                textcoords='offset points',
                fontsize=11,
                fontweight='bold')

sns.despine(left=True)
plt.yticks([])
plt.tight_layout()
plt.savefig('4_faturamento_por_categoria.png', dpi=300, bbox_inches='tight') # Salva a imagem
plt.show()