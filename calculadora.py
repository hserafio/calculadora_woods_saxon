import streamlit as st
import numpy as np

st.set_page_config(
    page_title="Woods-Saxon | SIICUSP", 
    layout="centered"
)

@st.cache_data
def load_parameters(filepath):
    try:
        return np.load(filepath)
    except FileNotFoundError:
        return None

coeficientes = load_parameters('best_params_18.npy')

# ==========================================
# BARRA LATERAL (MENU ESQUERDO)
# ==========================================
with st.sidebar:
    st.title("Painel de Controle")
    st.write("Defina a energia incidente do projétil para atualizar os parâmetros em tempo real.")
    
    energy = st.number_input(
        "Energia do Projétil (MeV):", 
        min_value=1.0, 
        max_value=50.0, 
        value=10.0, 
        step=0.1,
        format="%.1f",
        help="Insira o valor da energia de colisão no referencial do laboratório."
    )
    
    st.markdown("---")
    st.markdown("**Projeto de Iniciação Científica**")
    st.markdown("*34º SIICUSP - IFUSP*")

# ==========================================
# TELA PRINCIPAL
# ==========================================
st.title("Calculadora Woods-Saxon")
st.subheader("Sistema: $^4\mathrm{He} + ^{\mathrm{nat}}\mathrm{Zr}$")

st.markdown("""
Esta ferramenta interativa permite calcular os parâmetros do potencial óptico de Woods-Saxon para o sistema de colisão $^4\mathrm{He} + ^{\mathrm{nat}}\mathrm{Zr}$. 

Insira a energia desejada no painel ao lado para obter os valores resultantes da nossa otimização baseada em dados experimentais.
""")

st.write("---")

if coeficientes is None:
    st.error("Erro: Não foi possível encontrar o arquivo 'best_params_18.npy'. Verifique se ele está na mesma pasta do código.")
else:
    ws_params = [
        coeficientes[i] + (energy * coeficientes[i+1]) + ((energy**2) * coeficientes[i+2])
        for i in range(0, 18, 3)
    ]
    
    st.success(f"Parâmetros calculados para a energia de {energy:.1f} MeV.")

    col_real, col_imag = st.columns(2)
        
    with col_real:
        with st.container(border=True):
            st.markdown("**Potencial Real (V)**")
            st.metric("Profundidade V_0", f"{ws_params[0]:.3f} MeV")
            st.metric("Raio r_v",        f"{ws_params[1]:.3f} fm")
            st.metric("Difusividade a_v",f"{ws_params[2]:.3f} fm")

    with col_imag:
        with st.container(border=True):
            st.markdown("**Potencial Imaginário (W)**")
            st.metric("Profundidade W_0", f"{ws_params[3]:.3f} MeV")
            st.metric("Raio r_w",        f"{ws_params[4]:.3f} fm")
            st.metric("Difusividade a_w",f"{ws_params[5]:.3f} fm")

# ==========================================
# METODOLOGIA
# ==========================================
st.write("") 
with st.expander("Como essa conta é feita? (Metodologia)"):
    st.markdown("""
    O procedimento consistiu no levantamento e na análise de dados experimentais disponíveis na literatura (via banco de dados internacional **EXFOR**), com o objetivo de estabelecer a dependência energética dos parâmetros do potencial óptico de Woods-Saxon. 
    
    Foram considerados dados na faixa de **15 a 40 MeV**, utilizando a seguinte parametrização quadrática:
    """)
    
    st.latex(r"""
    (V, r_v, a_v, W, r_w, a_w) = (1, E, E^2)\mathbf{M_p}
    """)
    
    st.markdown("""
    Onde $\mathbf{M_P}$ é a matriz que contém os coeficientes dos polinômios ajustados. A otimização foi realizada por meio de algoritmos implementados em Python (utilizando a biblioteca `pymoo`), tendo como função objetivo a minimização do **qui-quadrado**:
    """)
    
    st.latex(r"""
    \chi_{\mathrm{Total}}^2 =
    \sum_i
    \frac{\left(d\sigma/d\Omega_i^{\mathrm{exp}}-d\sigma/d\Omega_i^{\mathrm{teo}}\right)^2}
    {\sigma_i^2}
    """)
    
    st.markdown("""
    O somatório é realizado sobre todos os pontos experimentais de seção de choque diferencial incluídos nas distribuições angulares selecionadas. As variáveis $d\sigma/d\Omega_i^{\mathrm{exp}}$ e $d\sigma/d\Omega_i^{\mathrm{teo}}$ representam as seções de choque diferenciais angulares experimentais e teóricas, enquanto $\sigma_i$ corresponde à incerteza experimental associada a cada ponto.
    """)

# ==========================================
# DADOS E REFERÊNCIAS
# ==========================================
with st.expander("Referências e Dados Experimentais"):
    st.markdown("### Conjuntos de Dados Utilizados")
    
    # Tabela formatada em Markdown nativo
    st.markdown("""
    | Sistema | Energia (MeV) | Nº de dados | Referência |
    | :--- | :--- | :--- | :--- |
    | $^4$He + $^{90}$Zr | 15.0 | 30 | B. D. Watson [1] |
    | $^4$He + $^{90}$Zr | 31.0 | 52 | E. J. Martens [2] |
    | $^4$He + $^{90}$Zr | 21.0, 23.4 e 25.0 | 154 | M. Wit [3] |
    | $^4$He + $^{90}$Zr | 40.0 | 46 | A. D. Duysebaev [4] |
    """)
    
    st.markdown("### Bibliografia")
    
    # Referências com DOIs transformados em links clicáveis
    st.markdown("""
    **[1]** B. D. Watson, D. Robson, D. D. Tolbert e R. H. Davis. "Resolution of Fixed-Geometry Optical-Model Ambiguities". *Phys. Rev. C* 4.6 (1971), pp. 2240–2249. [DOI: 10.1103/PhysRevC.4.2240](https://doi.org/10.1103/PhysRevC.4.2240)
    
    **[2]** E. J. Martens e A. M. Bernstein. "The 90Zr and 92Mo($\\alpha, \\alpha$') reactions at 31 MeV". *Nuclear Physics A* 117.2 (1968), pp. 241–272. [DOI: 10.1016/0375-9474(68)90842-7](https://doi.org/10.1016/0375-9474(68)90842-7)
    
    **[3]** M. Wit, J. Schiele, K. A. Eberhard e J. P. Schiffer. "Back-angle elastic alpha scattering from 89Y and 90,91,94Zr". *Phys. Rev. C* 12.5 (1975), pp. 1447–1451. [DOI: 10.1103/PhysRevC.12.1447](https://doi.org/10.1103/PhysRevC.12.1447)
    
    **[4]** A. D. Duysebaev, K. A. Kuterbekov, I. N. Kuchtina, B. M. Sadykov, L. I. Slusarenko, V. V. Tokarevsky e S. A. Fayans. "Structure of the 90,94Zr nuclei: Global analysis of data on the elastic and inelastic scattering of alpha particles and on the total cross sections for the reactions induced by their interaction with these nuclei". *Physics of Atomic Nuclei* 66.4 (2003), pp. 599–611. [DOI: 10.1134/1.1568811](https://doi.org/10.1134/1.1568811)
    """)