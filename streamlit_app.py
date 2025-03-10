import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Tratamento Antimicrobiano - Protocolos Brasileiros", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título e descrição
st.title("Tratamento Antimicrobiano - Protocolos Brasileiros")
st.markdown("Guia de tratamento para infecções em pacientes hospitalizados baseado em protocolos de hospitais brasileiros de referência")

# Dados da tabela
data = {
    "Foco Infeccioso": [
        "Pneumonia", 
        "Infecções do Trato Urinário", 
        "Infecções de Pele e Partes Moles",
        "Infecções Intra-abdominais", 
        "Sepse e Choque Séptico", 
        "Profilaxia Cirúrgica",
        "Meningite", 
        "Infecções de Corrente Sanguínea e Endocardites"
    ],
    "Tratamento para Infecção Comunitária (Hospitalizado)": [
        """**Paciente internado não-UTI:**
- Ceftriaxona 1-2g IV 1x/dia + Azitromicina 500mg IV/VO 1x/dia OU
- Levofloxacino 750mg IV/VO 1x/dia

**Paciente em UTI (PAC grave):**
- Ceftriaxona 2g IV 1x/dia + Claritromicina 500mg IV 12/12h OU
- Ampicilina-sulbactam 3g IV 6/6h + Azitromicina 500mg IV 1x/dia

**Se fatores de risco para S. aureus:**
- Adicionar Oxacilina 2g IV 4/4h OU Vancomicina 15-20mg/kg IV 12/12h""",
        
        """**ITU complicada hospitalizada:**
- Ceftriaxona 1-2g IV 1x/dia OU
- Ciprofloxacino 400mg IV 12/12h OU
- Ampicilina-sulbactam 3g IV 6/6h

**Pielonefrite (sem fatores de risco para MDR):**
- Ceftriaxona 1g IV 1x/dia OU
- Ciprofloxacino 400mg IV 12/12h""",
        
        """**Celulite/erisipela complicada:**
- Oxacilina 2g IV 4/4h OU
- Cefazolina 2g IV 8/8h OU
- Clindamicina 600mg IV 8/8h (se alergia a beta-lactâmicos)

**Se suspeita de MRSA comunitário:**
- Vancomicina 15-20mg/kg IV 12/12h OU
- Sulfametoxazol-trimetoprima 800/160mg IV 8/8h

**Infecções necrotizantes:**
- Ampicilina-sulbactam 3g IV 6/6h + Clindamicina 900mg IV 8/8h""",
        
        """**Comunitária não grave:**
- Ampicilina-sulbactam 3g IV 6/6h OU
- Ceftriaxona 2g IV 1x/dia + Metronidazol 500mg IV 8/8h

**Comunitária grave ou peritonite:**
- Cefepima 2g IV 8/8h + Metronidazol 500mg IV 8/8h OU
- Ertapenem 1g IV 1x/dia

**Pancreatite necro-hemorrágica:** 
- Ciprofloxacino 400mg IV 12/12h + Metronidazol 500mg IV 8/8h OU
- Piperacilina-tazobactam 4,5g IV 6/6h""",
        
        """**Origem comunitária sem foco definido:**
- Ceftriaxona 2g IV 1x/dia + Azitromicina 500mg IV 1x/dia OU
- Ampicilina-sulbactam 3g IV 6/6h

**Se suspeita de foco abdominal:**
- Cefepima 2g IV 8/8h + Metronidazol 500mg IV 8/8h OU
- Ertapenem 1g IV 1x/dia

**Se suspeita de meningite:**
- Ceftriaxona 2g IV 12/12h + Vancomicina 15-20mg/kg IV 12/12h + Ampicilina 2g IV 4/4h (>50 anos)""",
        
        """**Cirurgias limpas:**
- Cefazolina 2g IV dose única (até 3 doses em 24h)
- Para pacientes >120kg: 3g IV

**Cirurgias hepatobiliares:**
- Cefazolina 2g IV OU
- Ampicilina-sulbactam 3g IV

**Cirurgias colorretais:**
- Cefazolina 2g IV + Metronidazol 500mg IV OU
- Ampicilina-sulbactam 3g IV""",
        
        """**Meningite bacteriana comunitária:**
- Ceftriaxona 2g IV 12/12h + Vancomicina 15-20mg/kg IV 12/12h
- Adicionar Ampicilina 2g IV 4/4h (>50 anos)
- Dexametasona 0,15mg/kg IV 6/6h por 2-4 dias (iniciar antes ou com ATB)

**Meningite viral:**
- Tratamento de suporte

**Se suspeita de HSV:**
- Aciclovir 10mg/kg IV 8/8h""",
        
        """**Bacteremia comunitária:**
- Oxacilina 2g IV 4/4h (se suspeita de S. aureus) OU
- Ceftriaxona 2g IV 1x/dia (se suspeita de gram-negativos)

**Endocardite comunitária (S. viridans):**
- Penicilina G 4 milhões UI IV 4/4h + Gentamicina 3mg/kg/dia IV 1x/dia

**Endocardite comunitária (S. aureus não MRSA):**
- Oxacilina 2g IV 4/4h (+/- Gentamicina 3mg/kg/dia)

**Endocardite comunitária (Enterococcus):**
- Ampicilina 2g IV 4/4h + Gentamicina 3mg/kg/dia IV 1x/dia"""
    ],
    "Tratamento para Infecção com Risco de Patógeno Hospitalar": [
        """**Pneumonia hospitalar (<5 dias de internação):**
- Cefepima 2g IV 8/8h OU
- Piperacilina-tazobactam 4,5g IV 6/6h

**Pneumonia hospitalar (≥5 dias ou UTI):**
- Piperacilina-tazobactam 4,5g IV 6/6h + Amicacina 15-20mg/kg IV 1x/dia OU
- Meropenem 1g IV 8/8h + Vancomicina 15-20mg/kg IV 12/12h

**Se suspeita de MRSA:**
- Adicionar Vancomicina 15-20mg/kg IV 12/12h OU
- Linezolida 600mg IV 12/12h

**Se PAV tardia ou risco para multirresistentes:**
- Meropenem 1g IV 8/8h + Polimixina B 25.000UI/kg/dia IV dividida 12/12h""",
        
        """**ITU relacionada à assistência:**
- Cefepima 2g IV 8/8h OU
- Piperacilina-tazobactam 4,5g IV 6/6h

**ITU com fatores de risco para ESBL:**
- Meropenem 1g IV 8/8h OU
- Imipenem 500mg IV 6/6h

**Se presença de sonda vesical ou procedimento urológico:**
- Considerar cobertura para Enterococcus com Ampicilina 2g IV 6/6h OU
- Vancomicina 15-20mg/kg IV 12/12h (se risco de resistência)

**Se suspeita de candidúria invasiva:**
- Adicionar Fluconazol 400mg IV/VO 1x/dia""",
        
        """**Infecções hospitalares:**
- Vancomicina 15-20mg/kg IV 12/12h + Cefepima 2g IV 8/8h OU
- Vancomicina 15-20mg/kg IV 12/12h + Piperacilina-tazobactam 4,5g IV 6/6h

**Fasceíte necrotizante:**
- Meropenem 1g IV 8/8h + Vancomicina 15-20mg/kg IV 12/12h + Clindamicina 900mg IV 8/8h

**Infecções em ferida operatória:**
- Vancomicina 15-20mg/kg IV 12/12h + Cefepima 2g IV 8/8h + Metronidazol 500mg IV 8/8h

**Infecções em pé diabético graves:**
- Piperacilina-tazobactam 4,5g IV 6/6h + Vancomicina 15-20mg/kg IV 12/12h""",
        
        """**Infecção intra-abdominal nosocomial:**
- Piperacilina-tazobactam 4,5g IV 6/6h OU
- Meropenem 1g IV 8/8h

**Se risco de Enterococcus resistente:**
- Adicionar Vancomicina 15-20mg/kg IV 12/12h

**Se risco de Candida:**
- Adicionar Fluconazol 800mg IV dose de ataque, depois 400mg IV 1x/dia OU
- Anidulafungina 200mg IV dose de ataque, depois 100mg IV 1x/dia

**Peritonite terciária ou pós-operatória:**
- Meropenem 1g IV 8/8h + Vancomicina 15-20mg/kg IV 12/12h +/- Antifúngico""",
        
        """**Sepse/choque nosocomial:**
- Meropenem 1g IV 8/8h + Vancomicina 15-20mg/kg IV 12/12h (dose ataque 25-30mg/kg) OU
- Piperacilina-tazobactam 4,5g IV 6/6h + Vancomicina 15-20mg/kg IV 12/12h + Amicacina 15-20mg/kg IV 1x/dia

**Se fatores de risco para KPC ou multirresistentes:**
- Polimixina B 25.000UI/kg/dia IV dividida 12/12h + Vancomicina 15-20mg/kg IV 12/12h

**Se fatores de risco para candidemia invasiva:**
- Adicionar Anidulafungina 200mg IV dose de ataque, depois 100mg IV 1x/dia OU
- Micafungina 100mg IV 1x/dia""",
        
        """**Profilaxia em pacientes hospitalizados:**
- Mesmos antimicrobianos da profilaxia comunitária
- Se hospitalização prolongada: considerar Cefuroxima 1,5g IV
- Se colonização conhecida por MRSA: Vancomicina 15mg/kg IV

**Cirurgias de emergência com contaminação:**
- Ampliar espectro para Piperacilina-tazobactam 4,5g IV ou Ertapenem 1g IV

**Reoperação recente ou implante de prótese:**
- Vancomicina 15mg/kg IV + Cefepima 2g IV

**Importante:** Redosagem para cirurgias >3h ou sangramento >1,5L""",
        
        """**Meningite pós-neurocirurgia/derivação:**
- Vancomicina 15-20mg/kg IV 12/12h + Cefepima 2g IV 8/8h OU
- Vancomicina 15-20mg/kg IV 12/12h + Meropenem 2g IV 8/8h

**Se risco de Acinetobacter ou P. aeruginosa:**
- Polimixina B IV 25.000UI/kg/dia +/- Polimixina B intratecal (10.000 UI/dia)

**Meningite fúngica:**
- Anfotericina B lipossomal 5mg/kg/dia IV +/- Fluconazol intratecal OU
- Voriconazol 6mg/kg IV 12/12h no 1º dia, depois 4mg/kg IV 12/12h""",
        
        """**ICS relacionada a cateter:**
- Vancomicina 15-20mg/kg IV 12/12h + Cefepima 2g IV 8/8h OU
- Vancomicina 15-20mg/kg IV 12/12h + Amicacina 15-20mg/kg IV 1x/dia

**Endocardite hospitalar:**
- Vancomicina 15-20mg/kg IV 12/12h (MRSA) OU
- Daptomicina 8-10mg/kg IV 1x/dia (se CMI para vancomicina >1)

**Endocardite em prótese valvar:**
- Vancomicina 15-20mg/kg IV 12/12h + Gentamicina 3mg/kg/dia IV 1x/dia + Rifampicina 300-450mg VO 12/12h

**Candidemia:**
- Equinocandina (Anidulafungina 200mg IV, depois 100mg IV 1x/dia OU
- Micafungina 100mg IV 1x/dia)"""
    ]
}

# Lista de notas importantes
notas_importantes = [
    "**Ajuste de doses:** Todas as doses devem ser ajustadas conforme a função renal e hepática do paciente. O ajuste é particularmente importante para vancomicina, aminoglicosídeos e carbapenêmicos.",
    
    "**Posologia para pacientes obesos:** Em pacientes com obesidade (IMC>30), considerar ajuste de dose para antibióticos hidrofílicos.",
    
    "**Culturas:** Sempre coletar 2 pares de hemoculturas de sítios diferentes, urocultura, e culturas do foco suspeito antes do início da antibioticoterapia, sem atrasar o início do tratamento em casos graves.",
    
    "**Descalonamento:** Após resultados microbiológicos (48-72h), ajustar o tratamento para o espectro mais estreito possível, seguindo o antibiograma.",
    
    "**Fatores de risco para patógenos multirresistentes no Brasil:**\n- Hospitalização prévia nos últimos 90 dias\n- Antibioticoterapia nos últimos 90 dias (especialmente quinolonas e cefalosporinas)\n- Institucionalização (ILPI)\n- Hemodiálise\n- Imunossupressão\n- Tempo de internação atual >5 dias\n- Internação em UTI >3 dias\n- Colonização conhecida por bactéria multirresistente\n- Procedimentos invasivos (CVC, SVD, VM)\n- Alta prevalência local de ESBL, KPC ou outros mecanismos de resistência",
    
    "**Monitoramento terapêutico:**\n- Vancomicina: Dosar nível sérico (meta: vale 15-20mg/L, AUC/MIC >400)\n- Aminoglicosídeos: Considerar dose única diária e monitorar função renal\n- Polimixina B: Monitorar função renal diariamente",
    
    "**Duração de tratamento:**\n- Pneumonia: 5-7 dias (comunitária não complicada), 7-10 dias (nosocomial)\n- ITU: 5-7 dias (cistite), 10-14 dias (pielonefrite)\n- Bacteremia: 14 dias (gram-negativos), 14-28 dias (S. aureus)\n- Endocardite: 4-6 semanas\n- Infecções intra-abdominais: 4-7 dias após controle do foco",
    
    "**Programa de Stewardship:**\n- Reavaliação do antimicrobiano em 48-72h\n- Revisão de dose, via de administração e duração\n- Checagem de interações medicamentosas\n- Discussão multidisciplinar com CCIH/Infectologia em casos complexos"
]

# Lista de fontes
fontes = [
    "Protocolos do Hospital Albert Einstein",
    "Diretrizes do Hospital Sírio-Libanês",
    "Protocolos da Sociedade Brasileira de Infectologia",
    "Guia de Antimicrobianos do Hospital das Clínicas FMUSP",
    "Diretrizes da ANVISA para prevenção de IRAS"
]

# Criando DataFrame
df = pd.DataFrame(data)

# Configurações da barra lateral
st.sidebar.title("Filtros")

# Filtro por foco
focos_infecciosos = ["Todos"] + list(df["Foco Infeccioso"])
foco_selecionado = st.sidebar.selectbox("Selecione o foco infeccioso:", focos_infecciosos)

# Opção para mostrar notas
mostrar_notas = st.sidebar.checkbox("Mostrar notas importantes", value=False)

# Mostrar fontes
mostrar_fontes = st.sidebar.checkbox("Mostrar fontes", value=False)

# Seleção de tema de cores
tema_cores = st.sidebar.selectbox(
    "Escolha o tema de cores:",
    ["Padrão", "Azul-claro", "Verde-hospital", "Alto contraste"]
)

# Aplicar temas de cores (CSS personalizado)
if tema_cores == "Azul-claro":
    st.markdown("""
    <style>
    .main, .stApp {background-color: #f0f5ff;}
    .stDataFrame {background-color: white !important;}
    h1, h2, h3 {color: #0047AB !important;}
    </style>
    """, unsafe_allow_html=True)
elif tema_cores == "Verde-hospital":
    st.markdown("""
    <style>
    .main, .stApp {background-color: #f0fff5;}
    .stDataFrame {background-color: white !important;}
    h1, h2, h3 {color: #1e7145 !important;}
    </style>
    """, unsafe_allow_html=True)
elif tema_cores == "Alto contraste":
    st.markdown("""
    <style>
    .main, .stApp {background-color: white;}
    .stDataFrame {background-color: white !important;}
    h1, h2, h3 {color: black !important;}
    </style>
    """, unsafe_allow_html=True)

# Download de PDF
st.sidebar.markdown("---")
st.sidebar.subheader("Download")
st.sidebar.markdown("Baixe a tabela completa em PDF (funcionalidade a ser implementada)")
if st.sidebar.button("Gerar PDF"):
    st.sidebar.info("Recurso será disponibilizado na próxima versão.")

# Créditos
st.sidebar.markdown("---")
st.sidebar.info("Desenvolvido para uso médico. Sempre consulte protocolos institucionais e avalie cada paciente individualmente.")
st.sidebar.caption("© 2025 - v1.0")

# Filtrar a tabela conforme seleção
if foco_selecionado != "Todos":
    df_filtrada = df[df["Foco Infeccioso"] == foco_selecionado]
else:
    df_filtrada = df

# Exibir tabela
st.dataframe(
    df_filtrada, 
    use_container_width=True,
    hide_index=True,
    height=500 if foco_selecionado == "Todos" else 300
)

# Mostrar notas importantes se checkbox ativado
if mostrar_notas:
    st.markdown("---")
    st.subheader("Notas Importantes")
    
    # Dividir notas em colunas para melhor visualização
    col1, col2 = st.columns(2)
    
    # Distribuir as notas entre as colunas
    for i, nota in enumerate(notas_importantes):
        if i < len(notas_importantes) // 2:
            with col1:
                st.markdown(nota)
                st.markdown("---")
        else:
            with col2:
                st.markdown(nota)
                st.markdown("---")

# Mostrar fontes se checkbox ativado
if mostrar_fontes:
    st.markdown("---")
    st.subheader("Fontes")
    
    for fonte in fontes:
        st.markdown(f"- {fonte}")

# Adicionar uma seção de busca rápida por antibiótico
st.markdown("---")
st.subheader("Busca rápida por antimicrobiano")

# Input de busca
termo_busca = st.text_input("Digite o nome do antimicrobiano:", placeholder="Ex: vancomicina, meropenem...")

# Executar busca se termo foi digitado
if termo_busca:
    # Converter para minúsculas para busca insensível a maiúsculas
    termo_lower = termo_busca.lower()
    
    # Buscar nas colunas relevantes
    resultados = []
    
    for index, row in df.iterrows():
        if (termo_lower in row["Tratamento para Infecção Comunitária (Hospitalizado)"].lower() or 
            termo_lower in row["Tratamento para Infecção com Risco de Patógeno Hospitalar"].lower()):
            resultados.append(row)
    
    # Exibir resultados da busca
    if resultados:
        st.success(f"Encontrado em {len(resultados)} focos infecciosos:")
        st.dataframe(pd.DataFrame(resultados), use_container_width=True, hide_index=True)
    else:
        st.warning(f"Nenhum resultado encontrado para '{termo_busca}'.")

# Adicionar uma seção de calculadora de dose
st.markdown("---")
st.subheader("Calculadora de doses")

col1, col2, col3 = st.columns(3)

with col1:
    peso = st.number_input("Peso do paciente (kg)", min_value=0.0, value=70.0, step=0.1)
    
with col2:
    antibiotico = st.selectbox(
        "Selecione o antimicrobiano:",
        [
            "Vancomicina", 
            "Amicacina", 
            "Gentamicina", 
            "Polimixina B",
            "Meropenem"
        ]
    )
    
with col3:
    clearance = st.number_input("Clearance de creatinina (mL/min)", min_value=0, value=90, step=1)

if st.button("Calcular dose"):
    if antibiotico == "Vancomicina":
        if clearance >= 60:
            dose_ataque = round(25 * peso, 0)
            dose_manutencao = round(15 * peso, 0)
            st.info(f"Dose de ataque: {dose_ataque} mg IV\nDose de manutenção: {dose_manutencao} mg IV a cada 12h\nConsiderar ajuste com base em níveis séricos.")
        elif clearance >= 30 and clearance < 60:
            dose_ataque = round(25 * peso, 0)
            dose_manutencao = round(10 * peso, 0)
            st.info(f"Dose de ataque: {dose_ataque} mg IV\nDose de manutenção: {dose_manutencao} mg IV a cada 12-24h\nMonitorar nível sérico.")
        else:
            st.warning("Paciente com disfunção renal grave - Consultar farmácia clínica ou nefrologista para dosagem individualizada.")
            
    elif antibiotico == "Amicacina":
        if clearance >= 60:
            dose = round(15 * peso, 0)
            st.info(f"Dose: {dose} mg IV uma vez ao dia\nMonitorar função renal.")
        else:
            st.warning("Paciente com disfunção renal - Considerar ajuste de dose ou intervalo prolongado. Consultar farmácia clínica.")
            
    elif antibiotico == "Gentamicina":
        if clearance >= 60:
            dose = round(3 * peso, 0)
            st.info(f"Dose: {dose} mg IV uma vez ao dia (dose única diária)\nAlternativamente: {dose/3:.1f} mg IV a cada 8h\nMonitorar função renal.")
        else:
            st.warning("Paciente com disfunção renal - Considerar ajuste de dose ou intervalo prolongado. Consultar farmácia clínica.")
            
    elif antibiotico == "Polimixina B":
        if clearance >= 30:
            dose_diaria = round(25000 * peso / 1000000, 2)
            dose_por_aplicacao = round(dose_diaria / 2, 2)
            st.info(f"Dose diária: {dose_diaria} milhões UI IV, dividida em 2 aplicações\nDose por aplicação: {dose_por_aplicacao} milhões UI IV a cada 12h\nMonitorar função renal diariamente.")
        else:
            st.warning("Paciente com disfunção renal grave - Considerar redução de dose. Consultar farmácia clínica ou nefrologista.")
            
    elif antibiotico == "Meropenem":
        if clearance >= 50:
            st.info("Dose: 1g IV a cada 8h\nPara infecções graves como meningite: 2g IV a cada 8h")
        elif clearance >= 25 and clearance < 50:
            st.info("Dose: 1g IV a cada 12h")
        elif clearance >= 10 and clearance < 25:
            st.info("Dose: 500mg IV a cada 12h")
        else:
            st.warning("Paciente com disfunção renal grave - Dose: 500mg IV a cada 24h\nConsultar farmácia clínica.")

# Aviso final
st.markdown("---")
st.caption("Este aplicativo é apenas uma ferramenta de referência. As condutas devem ser adaptadas ao perfil epidemiológico local e às características individuais do paciente.")