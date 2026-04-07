# -*- coding: utf-8 -*-




"""
Created on Mon Apr  6 14:02:07 2026

@author: gustavo.araujo
"""

# =============================================================================
# Importando Bibliotecas
# =============================================================================

from dash import html, dcc, Dash, Input, Output, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import gdown

# =============================================================================
# Dados
# =============================================================================

# Cole o ID do seu arquivo aqui
FILE_ID = '14GwVAdntetbw_H07TS8qAKpCTWDdCXtT'

# Baixa o arquivo localmente na primeira execução
gdown.download(f'https://drive.google.com/uc?id={FILE_ID}', 'infra_final.csv', quiet=False)


infra = pd.read_csv('infra_final.csv', sep=',')

total_por_produto = infra.groupby(['macro_produto', 'Ano', 'cenario'])['toneladas'].sum().reset_index()
total_por_produto['milhoes_de_toneladas'] = (total_por_produto['toneladas'] / 1000000).round(2)

total_por_produto = total_por_produto.rename(columns={
    'macro_produto':        'Produtos',
    'milhoes_de_toneladas': 'Milhões de Toneladas'
})

total_por_produto['Produtos'] = total_por_produto['Produtos'].replace({
    'Embalagens plásticas, botijões para gás, pallets de madeira e garrafas de vidro': 'Embalagens e Recipientes'
})

total_por_produto = total_por_produto.assign(
    cenario=lambda x: x['cenario'].map({
        'base':          'Base',
        'transformador': 'Otimista'
    })
)

dados_finais = infra.copy()
dados_finais['milhoes_ton'] = (dados_finais['toneladas'] / 1000000).round(2)
dados_finais['cenario'] = dados_finais['cenario'].map({
    'base':          'Base',
    'transformador': 'Otimista'
})

resumo = total_por_produto.groupby(['Ano', 'cenario'])['Milhões de Toneladas'].sum().reset_index()

total_base_2030     = resumo.loc[(resumo['Ano']==2030) & (resumo['cenario']=='Base'),     'Milhões de Toneladas'].values[0]
total_base_2050     = resumo.loc[(resumo['Ano']==2050) & (resumo['cenario']=='Base'),     'Milhões de Toneladas'].values[0]
total_otimista_2030 = resumo.loc[(resumo['Ano']==2030) & (resumo['cenario']=='Otimista'), 'Milhões de Toneladas'].values[0]
total_otimista_2050 = resumo.loc[(resumo['Ano']==2050) & (resumo['cenario']=='Otimista'), 'Milhões de Toneladas'].values[0]

cresc_base     = ((total_base_2050     - total_base_2030)     / total_base_2030)     * 100
cresc_otimista = ((total_otimista_2050 - total_otimista_2030) / total_otimista_2030) * 100

n = 20
cagr_base     = ((total_base_2050     / total_base_2030)     ** (1/n) - 1) * 100
cagr_otimista = ((total_otimista_2050 / total_otimista_2030) ** (1/n) - 1) * 100

# =============================================================================
# Desenvolvimento do Dashboard
# =============================================================================

app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

app.layout = html.Div([

    dcc.Store(id='gatilho-inicial', data=1),

    # Cabeçalho
    dbc.Row([
        html.H1("Projeções de crescimento 2030-50",
                className="text-center my-4",
                style={"color": "white"}),
    ], style={"backgroundColor": "#1a1a1a", "padding": "20px"}),

    # 1ª Linha
    dbc.Row([

        # 1ª Coluna — Barra Lateral
        dbc.Col([
            html.P("Projeções econômicas de produtos e logística", className="text-center my-4"),
            html.P(['Dados retirados do PIT', html.Br(), 'Cenários de 2030 e 2050'],
                   className="text-center mb-4"),

            html.Hr(style={"borderColor": "#444"}),

            html.Div([
                html.P("📦 Cenário Base", style={"fontWeight": "bold", "color": "#4f98a3", "marginBottom": "8px"}),
                html.Div([html.Small("Total 2030", style={"color": "#888"}),
                          html.P(f"{total_base_2030:,.0f} Mi. Ton.", style={"color": "white", "margin": "0"})
                          ], style={"marginBottom": "8px"}),
                html.Div([html.Small("Total 2050", style={"color": "#888"}),
                          html.P(f"{total_base_2050:,.0f} Mi. Ton.", style={"color": "white", "margin": "0"})
                          ], style={"marginBottom": "8px"}),
                html.Div([html.Small("Crescimento 2030→2050", style={"color": "#888"}),
                          html.P(f"+{cresc_base:.1f}%", style={"color": "#4fd1a3", "margin": "0", "fontSize": "1.1rem", "fontWeight": "bold"})
                          ], style={"marginBottom": "8px"}),
                html.Div([html.Small("CAGR (ao ano)", style={"color": "#888"}),
                          html.P(f"{cagr_base:.2f}% a.a.", style={"color": "#4fd1a3", "margin": "0", "fontSize": "1.1rem", "fontWeight": "bold"})
                          ]),
            ], style={"backgroundColor": "#1e2a2a", "padding": "12px", "borderRadius": "8px", "marginBottom": "12px"}),

            html.Div([
                html.P("🚀 Cenário Otimista", style={"fontWeight": "bold", "color": "#e8af34", "marginBottom": "8px"}),
                html.Div([html.Small("Total 2030", style={"color": "#888"}),
                          html.P(f"{total_otimista_2030:,.0f} Mi. Ton.", style={"color": "white", "margin": "0"})
                          ], style={"marginBottom": "8px"}),
                html.Div([html.Small("Total 2050", style={"color": "#888"}),
                          html.P(f"{total_otimista_2050:,.0f} Mi. Ton.", style={"color": "white", "margin": "0"})
                          ], style={"marginBottom": "8px"}),
                html.Div([html.Small("Crescimento 2030→2050", style={"color": "#888"}),
                          html.P(f"+{cresc_otimista:.1f}%", style={"color": "#f5d78e", "margin": "0", "fontSize": "1.1rem", "fontWeight": "bold"})
                          ], style={"marginBottom": "8px"}),
                html.Div([html.Small("CAGR (ao ano)", style={"color": "#888"}),
                          html.P(f"{cagr_otimista:.2f}% a.a.", style={"color": "#f5d78e", "margin": "0", "fontSize": "1.1rem", "fontWeight": "bold"})
                          ]),
            ], style={"backgroundColor": "#2a2510", "padding": "12px", "borderRadius": "8px"}),

        ], style={"backgroundColor": "#1a1a1a", "padding": "20px"}, width=2),

        # 2ª Coluna — Gráfico + Botão Download
        dbc.Col([
            html.Div([
                html.Button(
                    "⬇ Exportar CSV",
                    id='btn-download',
                    style={
                        'backgroundColor': '#4f98a3',
                        'color': 'white',
                        'border': 'none',
                        'padding': '8px 16px',
                        'borderRadius': '6px',
                        'cursor': 'pointer',
                        'marginBottom': '10px'
                    }
                ),
                dcc.Download(id='download-csv')  # ✅ componente invisível de download
            ]),
            html.Div(id='espaco-grafico')
        ], style={"backgroundColor": "black", "padding": "20px"}, width=6),

        # 3ª Coluna — Heatmap
        dbc.Col([
            html.P("Matriz de Fluxo Origem × Destino", className="text-center my-4"),
            html.Label("Cenário:", style={"color": "white"}),
            dcc.Dropdown(
                id='filtro-cenario-matriz',
                options=[
                    {'label': 'Base',     'value': 'Base'},
                    {'label': 'Otimista', 'value': 'Otimista'}
                ],
                value='Base',
                clearable=False,
                style={'color': 'black'}
            ),
            html.Br(),
            html.Div(id='espaco-matriz')
        ], style={"backgroundColor": "#1a1a1a", "padding": "20px"}, width=4),

    ]),

    # ✅ 2ª Linha — Gráfico de Linha
    dbc.Row([
        dbc.Col([
            html.Div(id='espaco-linha')
        ], style={"backgroundColor": "black", "padding": "20px"}, width=12)
    ])
])

# ============================================================
# Callback 1 — Gráfico de Barras
# ============================================================

@app.callback(
    Output('espaco-grafico', 'children'),
    Input('gatilho-inicial', 'data')
)
def atualizar_grafico(dummy):

    top_produtos = (
        total_por_produto.groupby('Produtos')['Milhões de Toneladas']
        .sum()
        .nlargest(10)
        .index
    )
    df_top_10 = total_por_produto[total_por_produto['Produtos'].isin(top_produtos)]

    ordem = (
        df_top_10.groupby('Produtos')['Milhões de Toneladas']
        .sum()
        .sort_values(ascending=False)
        .index.tolist()
    )

    # ✅ '<br>' correto para quebra de linha
    ordem_display = [p.replace(' ', '<br>', 2) for p in ordem]

    base_2030     = df_top_10[(df_top_10['Ano'] == 2030) & (df_top_10['cenario'] == 'Base')]
    otimista_2030 = df_top_10[(df_top_10['Ano'] == 2030) & (df_top_10['cenario'] == 'Otimista')]
    base_2050     = df_top_10[(df_top_10['Ano'] == 2050) & (df_top_10['cenario'] == 'Base')]
    otimista_2050 = df_top_10[(df_top_10['Ano'] == 2050) & (df_top_10['cenario'] == 'Otimista')]

    merged_2030 = base_2030.merge(otimista_2030, on='Produtos', suffixes=('_base', '_otim'))
    merged_2050 = base_2050.merge(otimista_2050, on='Produtos', suffixes=('_base', '_otim'))

    merged_2030['diff'] = merged_2030['Milhões de Toneladas_otim'] - merged_2030['Milhões de Toneladas_base']
    merged_2050['diff'] = merged_2050['Milhões de Toneladas_otim'] - merged_2050['Milhões de Toneladas_base']

    fig = go.Figure()

    # ✅ hovertemplate personalizado em todos os 4 traces
    fig.add_trace(go.Bar(
        name='Base 2030',
        x=merged_2030['Produtos'],
        y=merged_2030['Milhões de Toneladas_base'],
        offsetgroup='2030',
        marker_color='#4f98a3',
        hovertemplate='<b>%{x}</b><br>Base 2030: %{y:.1f} Mi.Ton<extra></extra>'
    ))

    fig.add_trace(go.Bar(
        name='Otimista 2030',
        x=merged_2030['Produtos'],
        y=merged_2030['diff'],
        base=merged_2030['Milhões de Toneladas_base'].values,
        offsetgroup='2030',
        marker_color='#a3d4d8',
        customdata=merged_2030['Milhões de Toneladas_otim'].values,
        hovertemplate='<b>%{x}</b><br>Otimista 2030: %{customdata:.1f} Mi.Ton<extra></extra>'
    ))

    fig.add_trace(go.Bar(
        name='Base 2050',
        x=merged_2050['Produtos'],
        y=merged_2050['Milhões de Toneladas_base'],
        offsetgroup='2050',
        marker_color='#e8af34',
        hovertemplate='<b>%{x}</b><br>Base 2050: %{y:.1f} Mi.Ton<extra></extra>'
    ))

    fig.add_trace(go.Bar(
        name='Otimista 2050',
        x=merged_2050['Produtos'],
        y=merged_2050['diff'],
        base=merged_2050['Milhões de Toneladas_base'].values,
        offsetgroup='2050',
        marker_color='#f5d78e',
        customdata=merged_2050['Milhões de Toneladas_otim'].values,
        hovertemplate='<b>%{x}</b><br>Otimista 2050: %{customdata:.1f} Mi.Ton<extra></extra>'
    ))

    fig.update_layout(
        barmode='overlay',
        template='plotly_dark',
        title='Top 10 Produtos — 2030 vs 2050',
        legend_title_text='Legenda',
        margin=dict(l=10, r=10, t=40, b=10),
        height=500,
        xaxis=dict(
            categoryorder='array',
            categoryarray=ordem,
            ticktext=ordem_display,
            tickvals=ordem,
            tickangle=0
        )
    )

    return dcc.Graph(figure=fig)

# ============================================================
# Callback 2 — Heatmap
# ============================================================

@app.callback(
    Output('espaco-matriz', 'children'),
    Input('filtro-cenario-matriz', 'value')
)
def atualizar_matriz(cenario_selecionado):

    df       = dados_finais[dados_finais['cenario'] == cenario_selecionado]
    dados_ano = df[df['Ano'] == 2030]

    matriz = pd.pivot_table(
        dados_ano, values='milhoes_ton',
        index='regiao_origem', columns='regiao_destino',
        aggfunc='sum', fill_value=0
    ).round(2)

    fig = px.imshow(
        matriz,
        text_auto=True,
        aspect='auto',
        color_continuous_scale='Teal',
        template='plotly_dark',
        title=f'Fluxo Origem × Destino — {cenario_selecionado}',
        labels={'x': 'Destino', 'y': 'Origem', 'color': 'Milhões de Ton.'}
    )

    fig.update_layout(
        margin=dict(l=10, r=10, t=40, b=10),
        height=380,
        coloraxis_colorbar=dict(title='Mi. Ton.')
    )

    return dcc.Graph(figure=fig)

# ============================================================
# Callback 3 — Download CSV  
# ============================================================

@app.callback(
    Output('download-csv', 'data'),
    Input('btn-download', 'n_clicks'),
    prevent_initial_call=True
)
def exportar_csv(n_clicks):
    return dcc.send_data_frame(
        total_por_produto.to_csv,
        filename='projecoes_infra_2030_2050.csv',
        index=False
    )

# ============================================================
# Callback 4 — Gráfico de Linha  
# ============================================================

@app.callback(
    Output('espaco-linha', 'children'),
    Input('gatilho-inicial', 'data')
)
def atualizar_linha(dummy):

    evolucao = (
        total_por_produto
        .groupby(['Ano', 'cenario'])['Milhões de Toneladas']
        .sum()
        .reset_index()
    )

    fig = px.line(
        evolucao,
        x='Ano',
        y='Milhões de Toneladas',
        color='cenario',
        markers=True,
        template='plotly_dark',
        title='Evolução Total da Carga — 2030 vs 2050',
        labels={'cenario': 'Cenário'},
        color_discrete_map={
            'Base':     '#4f98a3',
            'Otimista': '#e8af34'
        }
    )

    fig.update_traces(line=dict(width=3), marker=dict(size=10))

    fig.update_layout(
        xaxis=dict(tickvals=[2030, 2050], ticktext=['2030', '2050']),
        height=300,
        margin=dict(l=10, r=10, t=40, b=10)
    )

    return dcc.Graph(figure=fig)

# ============================================================
# Run
# ============================================================

if __name__ == '__main__':
    app.run(debug=True)