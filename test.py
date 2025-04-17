import pandas as pd
import json

# O teu JSON (podes carregar de ficheiro ou colar diretamente como abaixo)
data = [{"CTTG": 27.38272, "Average": 8.876435, "Maximum": 27.38272, "Minimum": 0.55203, "Indicator": "Total Performance"}, {"CTTG": 53.84873, "Average": 28.677241666, "Maximum": 53.84873, "Minimum": 15.03798, "Indicator": "Financial Performance"}, {"CTTG": 0.33704, "Average": 0.184555, "Maximum": 0.33704, "Minimum": 0.09477, "Indicator": "Market Performance"}, {"CTTG": 0.74, "Average": 0.749583333, "Maximum": 0.8175, "Minimum": 0.685, "Indicator": "Marketing Effectiveness"}, {"CTTG": 6.78823, "Average": 7.366581666, "Maximum": 8.75058, "Minimum": 5.17124, "Indicator": "Investment in Future"}, {"CTTG": 0.39628, "Average": 0.30715, "Maximum": 0.57334, "Minimum": 0.12692, "Indicator": "Wealth"}, {"CTTG": 0.79825, "Average": 0.812311666, "Maximum": 0.83702, "Minimum": 0.79234, "Indicator": "Human Resource Management"}, {"CTTG": 1.86787, "Average": 1.698288333, "Maximum": 2.42611, "Minimum": 0.81601, "Indicator": "Asset Management"}, {"CTTG": 0.64636, "Average": 0.594203333, "Maximum": 0.70577, "Minimum": 0.30984, "Indicator": "Manufacturing Productivity"}, {"CTTG": 0.78644, "Average": 0.770545, "Maximum": 1.0, "Minimum": 0.55461, "Indicator": "Financial Risk"}]

# Converte para DataFrame
df = pd.DataFrame(data)

# Mostra os dados
print(df)

# Exemplo de análise: ordenar por "CTTG"
print("\nOrdenado por CTTG:")
print(df.sort_values(by="CTTG", ascending=False))

# Exemplo de exportação para CSV
df.to_csv("metrics.csv", index=False)
