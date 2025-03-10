import streamlit as st
import pandas as pd
import re

st.set_page_config(
    page_title="Tratamento Antimicrobiano - Protocolos do Complexo Hospitalar dos Estivadores", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Função para converter markdown para HTML
def md_to_html(md_text):
    html_text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', md_text)
    html_text = html_text.replace('\n', '<br>')
    return html_text

# Título e descrição
st.markdown("""
    <h1 style='text-align: center; color: #0047AB;'>Tratamento Antimicrobiano</h1>
    <h3 style='text-align: center; color: #4682B4; margin-bottom: 30px;'>Protocolos Complexo Hospitalar dos Estivadores</h3>
    <div style='text-align: center; padding: 0 50px; margin-bottom: 30px;'>
    Guia de tratamento para infecções em pacientes hospitalizados
    </div>
""", unsafe_allow_html=True)

# Dados da tabela - estrutura de dados simplificada
focos_infecciosos = [
    "Pneumonia", 
    "Infecções do Trato Urinário", 
    "Infecções de Pele e Partes Moles",
    "Infecções Intra-abdominais", 
    "Sepse e Choque Séptico", 
    "Profilaxia Cirúrgica",
    "Meningite", 
    "Infecções de Corrente Sanguínea e Endocardites",
    "Infecções em Gestantes",
    "Infecções em Puérperas",
    "Sepse Neonatal"
]

# Dicionário de tratamentos para cada foco
tratamentos = {
    "Pneumonia": {
        "comunitario": """**Paciente internado não-UTI:**
- Ceftriaxona 1-2g IV 1x/dia + Azitromicina 500mg IV/VO 1x/dia OU
- Levofloxacino 750mg IV/VO 1x/dia (se DPOC)

**Paciente em UTI (PAC grave):**
- Ceftriaxona 2g IV 1x/dia + Claritromicina 500mg IV 12/12h OU Azitromicina 500mg IV 1x/dia

**Se fatores de risco para S. aureus:**
- Adicionar Oxacilina 2g IV 4/4h OU Vancomicina 15-20mg/kg IV 12/12h""",
        
        "hospitalar": """**Pneumonia hospitalar (<5 dias de internação):**
- Cefepima 2g IV 8/8h OU
- Piperacilina-tazobactam 4,5g IV 6/6h

**Pneumonia hospitalar (≥5 dias ou UTI):**
- Piperacilina-tazobactam 4,5g IV 6/6h + Amicacina 15-20mg/kg IV 1x/dia OU
- Meropenem 1g IV 8/8h + Vancomicina 15-20mg/kg IV 12/12h

**Se suspeita de MRSA:**
- Adicionar Vancomicina 15-20mg/kg IV 12/12h OU
- Linezolida 600mg IV 12/12h

**Se PAV tardia ou risco para multirresistentes:**
- Meropenem 1g IV 8/8h + Polimixina B 25.000UI/kg/dia IV dividida 12/12h"""
    },
    
    "Infecções do Trato Urinário": {
        "comunitario": """**ITU complicada hospitalizada:**
- Ceftriaxona 1-2g IV 1x/dia OU
- Ciprofloxacino 400mg IV 12/12h OU
- Ampicilina-sulbactam 3g IV 6/6h

**Pielonefrite (sem fatores de risco para MDR):**
- Ceftriaxona 1g IV 1x/dia OU
- Ciprofloxacino 400mg IV 12/12h""",
        
        "hospitalar": """**ITU relacionada à assistência:**
- Cefepima 2g IV 8/8h OU
- Piperacilina-tazobactam 4,5g IV 6/6h

**ITU com fatores de risco para ESBL:**
- Meropenem 1g IV 8/8h OU
- Imipenem 500mg IV 6/6h

**Se presença de sonda vesical ou procedimento urológico:**
- Considerar cobertura para Enterococcus com Ampicilina 2g IV 6/6h OU
- Vancomicina 15-20mg/kg IV 12/12h (se risco de resistência)

**Se suspeita de candidúria invasiva:**
- Adicionar Fluconazol 400mg IV/VO 1x/dia"""
    },
    
    "Infecções de Pele e Partes Moles": {
        "comunitario": """**Celulite/erisipela complicada:**
- Oxacilina 2g IV 4/4h OU
- Cefazolina 2g IV 8/8h OU
- Clindamicina 600mg IV 8/8h (se alergia a beta-lactâmicos)

**Se suspeita de MRSA comunitário:**
- Vancomicina 15-20mg/kg IV 12/12h OU
- Sulfametoxazol-trimetoprima 800/160mg IV 8/8h

**Infecções necrotizantes:**
- Ampicilina-sulbactam 3g IV 6/6h + Clindamicina 900mg IV 8/8h""",
        
        "hospitalar": """**Infecções hospitalares:**
- Vancomicina 15-20mg/kg IV 12/12h + Cefepima 2g IV 8/8h OU
- Vancomicina 15-20mg/kg IV 12/12h + Piperacilina-tazobactam 4,5g IV 6/6h

**Fasceíte necrotizante:**
- Meropenem 1g IV 8/8h + Vancomicina 15-20mg/kg IV 12/12h + Clindamicina 900mg IV 8/8h

**Infecções em ferida operatória:**
- Vancomicina 15-20mg/kg IV 12/12h + Cefepima 2g IV 8/8h + Metronidazol 500mg IV 8/8h

**Infecções em pé diabético graves:**
- Piperacilina-tazobactam 4,5g IV 6/6h + Vancomicina 15-20mg/kg IV 12/12h"""
    },
    
    "Infecções Intra-abdominais": {
        "comunitario": """**Comunitária não grave:**
- Ampicilina-sulbactam 3g IV 6/6h OU
- Ceftriaxona 2g IV 1x/dia + Metronidazol 500mg IV 8/8h

**Comunitária grave ou peritonite:**
- Cefepima 2g IV 8/8h + Metronidazol 500mg IV 8/8h OU
- Ertapenem 1g IV 1x/dia

**Pancreatite necro-hemorrágica:** 
- Ciprofloxacino 400mg IV 12/12h + Metronidazol 500mg IV 8/8h OU
- Piperacilina-tazobactam 4,5g IV 6/6h""",
        
        "hospitalar": """**Infecção intra-abdominal nosocomial:**
- Piperacilina-tazobactam 4,5g IV 6/6h OU
- Meropenem 1g IV 8/8h

**Se risco de Enterococcus resistente:**
- Adicionar Vancomicina 15-20mg/kg IV 12/12h

**Se risco de Candida:**
- Adicionar Fluconazol 800mg IV dose de ataque, depois 400mg IV 1x/dia OU
- Anidulafungina 200mg IV dose de ataque, depois 100mg IV 1x/dia

**Peritonite terciária ou pós-operatória:**
- Meropenem 1g IV 8/8h + Vancomicina 15-20mg/kg IV 12/12h +/- Antifúngico"""
    },
    
    "Sepse e Choque Séptico": {
        "comunitario": """**Origem comunitária sem foco definido:**
- Ceftriaxona 2g IV 1x/dia + Azitromicina 500mg IV 1x/dia OU
- Ampicilina-sulbactam 3g IV 6/6h

**Se suspeita de foco abdominal:**
- Cefepima 2g IV 8/8h + Metronidazol 500mg IV 8/8h OU
- Ertapenem 1g IV 1x/dia

**Se suspeita de meningite:**
- Ceftriaxona 2g IV 12/12h + Vancomicina 15-20mg/kg IV 12/12h + Ampicilina 2g IV 4/4h (>50 anos)""",
        
        "hospitalar": """**Sepse/choque nosocomial:**
- Meropenem 1g IV 8/8h + Vancomicina 15-20mg/kg IV 12/12h (dose ataque 25-30mg/kg) OU
- Piperacilina-tazobactam 4,5g IV 6/6h + Vancomicina 15-20mg/kg IV 12/12h + Amicacina 15-20mg/kg IV 1x/dia

**Se fatores de risco para KPC ou multirresistentes:**
- Polimixina B 25.000UI/kg/dia IV dividida 12/12h + Vancomicina 15-20mg/kg IV 12/12h

**Se fatores de risco para candidemia invasiva:**
- Adicionar Anidulafungina 200mg IV dose de ataque, depois 100mg IV 1x/dia OU
- Micafungina 100mg IV 1x/dia"""
    },
    
    "Profilaxia Cirúrgica": {
        "comunitario": """**Cirurgias limpas:**
- Cefazolina 2g IV dose única (até 3 doses em 24h)
- Para pacientes >120kg: 3g IV

**Cirurgias hepatobiliares:**
- Cefazolina 2g IV OU
- Ampicilina-sulbactam 3g IV

**Cirurgias colorretais:**
- Cefazolina 2g IV + Metronidazol 500mg IV OU
- Ampicilina-sulbactam 3g IV""",
        
        "hospitalar": """**Profilaxia em pacientes hospitalizados:**
- Mesmos antimicrobianos da profilaxia comunitária
- Se hospitalização prolongada: considerar Cefuroxima 1,5g IV
- Se colonização conhecida por MRSA: Vancomicina 15mg/kg IV

**Cirurgias de emergência com contaminação:**
- Ampliar espectro para Piperacilina-tazobactam 4,5g IV ou Ertapenem 1g IV

**Reoperação recente ou implante de prótese:**
- Vancomicina 15mg/kg IV + Cefepima 2g IV

**Importante:** Redosagem para cirurgias >3h ou sangramento >1,5L"""
    },
    
    "Meningite": {
        "comunitario": """**Meningite bacteriana comunitária:**
- Ceftriaxona 2g IV 12/12h + Vancomicina 15-20mg/kg IV 12/12h
- Adicionar Ampicilina 2g IV 4/4h (>50 anos)
- Dexametasona 0,15mg/kg IV 6/6h por 2-4 dias (iniciar antes ou com ATB)

**Meningite viral:**
- Tratamento de suporte

**Se suspeita de HSV:**
- Aciclovir 10mg/kg IV 8/8h""",
        
        "hospitalar": """**Meningite pós-neurocirurgia/derivação:**
- Vancomicina 15-20mg/kg IV 12/12h + Cefepima 2g IV 8/8h OU
- Vancomicina 15-20mg/kg IV 12/12h + Meropenem 2g IV 8/8h

**Se risco de Acinetobacter ou P. aeruginosa:**
- Polimixina B IV 25.000UI/kg/dia +/- Polimixina B intratecal (10.000 UI/dia)

**Meningite fúngica:**
- Anfotericina B lipossomal 5mg/kg/dia IV +/- Fluconazol intratecal OU
- Voriconazol 6mg/kg IV 12/12h no 1º dia, depois 4mg/kg IV 12/12h"""
    },
    
    "Infecções de Corrente Sanguínea e Endocardites": {
        "comunitario": """**Bacteremia comunitária:**
- Oxacilina 2g IV 4/4h (se suspeita de S. aureus) OU
- Ceftriaxona 2g IV 1x/dia (se suspeita de gram-negativos)

**Endocardite comunitária (S. viridans):**
- Penicilina G 4 milhões UI IV 4/4h + Gentamicina 3mg/kg/dia IV 1x/dia

**Endocardite comunitária (S. aureus não MRSA):**
- Oxacilina 2g IV 4/4h (+/- Gentamicina 3mg/kg/dia)

**Endocardite comunitária (Enterococcus):**
- Ampicilina 2g IV 4/4h + Gentamicina 3mg/kg/dia IV 1x/dia""",
        
        "hospitalar": """**ICS relacionada a cateter:**
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
    },
    
    "Infecções em Gestantes": {
        "comunitario": """**ITU na gestação:**
- Nitrofurantoína 100mg VO 6/6h (contraindicada no final da gestação) OU
- Cefalexina 500mg VO 6/6h OU
- Amoxicilina-clavulanato 500/125mg VO 8/8h

**Pielonefrite na gestação:**
- Ceftriaxona 1-2g IV 1x/dia OU
- Ampicilina 2g IV 6/6h + Gentamicina 3-5mg/kg/dia IV 1x/dia

**Pneumonia na gestação:**
- Ampicilina-sulbactam 3g IV 6/6h OU
- Ceftriaxona 1-2g IV 1x/dia + Azitromicina 500mg IV/VO 1x/dia

**Antibióticos seguros na gestação:**
- Penicilinas, cefalosporinas, azitromicina, eritromicina (base)
- EVITAR: fluoroquinolonas, tetraciclinas, sulfonamidas (final da gestação)""",
        
        "hospitalar": """**ITU complicada na gestante hospitalizada:**
- Ceftriaxona 1g IV 1x/dia OU
- Ampicilina 2g IV 6/6h + Gentamicina 3-5mg/kg IV 1x/dia (dose única diária)

**Pneumonia hospitalar na gestante:**
- Cefepima 2g IV 8/8h OU
- Piperacilina-tazobactam 4,5g IV 6/6h

**Listeriose na gestação:**
- Ampicilina 2g IV 4/4h +/- Gentamicina 5mg/kg IV 1x/dia

**Corioamnionite:**
- Ampicilina 2g IV 6/6h + Gentamicina 5mg/kg IV 1x/dia + Metronidazol 500mg IV 8/8h OU
- Piperacilina-tazobactam 4,5g IV 6/6h"""
    },
    
    "Infecções em Puérperas": {
        "comunitario": """**Endometrite puerperal:**
- Ampicilina 2g IV 6/6h + Gentamicina 5mg/kg IV 1x/dia + Metronidazol 500mg IV 8/8h OU
- Clindamicina 900mg IV 8/8h + Gentamicina 5mg/kg IV 1x/dia

**Infecção de ferida operatória (cesariana):**
- Cefazolina 2g IV 8/8h OU
- Ampicilina-sulbactam 3g IV 6/6h

**Mastite puerperal não complicada:**
- Cefalexina 500mg VO 6/6h OU
- Dicloxacilina 500mg VO 6/6h

**Mastite puerperal complicada (abscesso):**
- Oxacilina 2g IV 4/4h OU
- Cefazolina 2g IV 8/8h""",
        
        "hospitalar": """**Endometrite pós-cesariana complicada:**
- Piperacilina-tazobactam 4,5g IV 6/6h OU
- Ertapenem 1g IV 1x/dia OU
- Imipenem 500mg IV 6/6h

**Infecção de ferida operatória complicada:**
- Vancomicina 15-20mg/kg IV 12/12h + Piperacilina-tazobactam 4,5g IV 6/6h OU
- Vancomicina 15-20mg/kg IV 12/12h + Cefepima 2g IV 8/8h + Metronidazol 500mg IV 8/8h

**Sepse puerperal grave:**
- Meropenem 1g IV 8/8h + Vancomicina 15-20mg/kg IV 12/12h +/- Clindamicina 900mg IV 8/8h OU
- Piperacilina-tazobactam 4,5g IV 6/6h + Vancomicina 15-20mg/kg IV 12/12h"""
    },
    
    "Sepse Neonatal": {
        "comunitario": """**Sepse neonatal precoce (<72h):**
- Ampicilina 50mg/kg/dose IV + Gentamicina 4mg/kg/dose IV 1x/dia OU
- Ampicilina 50mg/kg/dose IV + Cefotaxima 50mg/kg/dose IV 8/8h

**Sepse neonatal tardia (>72h):**
- Oxacilina 50mg/kg/dose IV 6/6h + Cefotaxima 50mg/kg/dose IV 8/8h OU
- Oxacilina 50mg/kg/dose IV 6/6h + Amicacina 15mg/kg/dose IV 1x/dia

**Sepse neonatal relacionada a cateter:**
- Vancomicina 15mg/kg/dose IV 8/8h (ajuste para função renal) + Cefotaxima 50mg/kg/dose IV 8/8h

**Meningite neonatal:**
- Ampicilina 100mg/kg/dose IV 8/8h + Cefotaxima 50mg/kg/dose IV 8/8h OU
- Ampicilina 100mg/kg/dose IV 8/8h + Gentamicina 4mg/kg/dose IV 1x/dia""",
        
        "hospitalar": """**Sepse neonatal tardia (hospitalar):**
- Vancomicina 15mg/kg/dose IV 8/8h + Cefepima 50mg/kg/dose IV 8/8h OU
- Vancomicina 15mg/kg/dose IV 8/8h + Meropenem 20mg/kg/dose IV 8/8h

**Sepse neonatal com foco abdominal:**
- Ampicilina 50mg/kg/dose IV 6/6h + Gentamicina 4mg/kg/dose IV 1x/dia + Metronidazol 7,5mg/kg/dose IV 8/8h OU
- Piperacilina-tazobactam 100mg/kg/dose IV 8/8h

**Infecções por Candida no neonato:**
- Anfotericina B lipossomal 3-5mg/kg/dia IV 1x/dia OU
- Micafungina 4-10mg/kg/dia IV 1x/dia (>1kg)

**Meningite neonatal hospitalar:**
- Vancomicina 15mg/kg/dose IV 8/8h + Meropenem 40mg/kg/dose IV 8/8h +/- Anfotericina B lipossomal"""
    }
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
    
    "**Considerações especiais para gestantes:**\n- FDA categorias B/C preferencialmente\n- Evitar tetraciclinas, fluoroquinolonas e sulfonamidas (último trimestre)\n- Aminoglicosídeos: monitorar função renal e níveis séricos quando possível\n- Ajustar doses conforme alterações fisiológicas da gestação",
    
    "**Considerações para neonatos:**\n- Ajuste de doses conforme peso e idade gestacional\n- Medir níveis séricos de vancomicina e aminoglicosídeos\n- Monitorar função renal diariamente durante o uso de nefrotóxicos\n- Considerar antibióticos com melhor penetração no SNC para meningites"
]

# Lista de fontes
fontes = [
    "Protocolos do Hospital Albert Einstein",
    "Diretrizes do Hospital Sírio-Libanês",
    "Protocolos da Sociedade Brasileira de Infectologia",
    "Guia de Antimicrobianos do Hospital das Clínicas FMUSP",
    "Diretrizes da ANVISA para prevenção de IRAS"
]

# Configurações da barra lateral
st.sidebar.title("Filtros")

# Filtro por foco
foco_selecionado = st.sidebar.selectbox("Selecione o foco infeccioso:", ["Todos"] + focos_infecciosos)

# Opção para mostrar notas
mostrar_notas = st.sidebar.checkbox("Mostrar notas importantes", value=False)
mostrar_fontes = st.sidebar.checkbox("Mostrar fontes", value=False)

# Créditos
st.sidebar.markdown("---")
st.sidebar.info("Desenvolvido para uso médico. Sempre consulte protocolos institucionais e avalie cada paciente individualmente.")
st.sidebar.caption("© 2025 - v1.0")

# Construir a tabela baseada na seleção
if foco_selecionado == "Todos":
    # Criar DataFrame para todos os focos
    data = []
    for foco in focos_infecciosos:
        data.append({
            "Foco Infeccioso": foco,
            "Tratamento para Infecção Comunitária (Hospitalizado)": md_to_html(tratamentos[foco]["comunitario"]),
            "Tratamento para Infecção com Risco de Patógeno Hospitalar": md_to_html(tratamentos[foco]["hospitalar"])
        })
    df = pd.DataFrame(data)
else:
    # Criar DataFrame para um único foco
    df = pd.DataFrame([{
        "Foco Infeccioso": foco_selecionado,
        "Tratamento para Infecção Comunitária (Hospitalizado)": md_to_html(tratamentos[foco_selecionado]["comunitario"]),
        "Tratamento para Infecção com Risco de Patógeno Hospitalar": md_to_html(tratamentos[foco_selecionado]["hospitalar"])
    }])

# Aplicar estilo à tabela
st.markdown("""
<style>
table {
    width: 100%;
    border-collapse: collapse;
}
th {
    background-color: #4682B4;
    color: white;
    padding: 12px;
    text-align: left;
    font-weight: bold;
}
td {
    padding: 12px;
    border: 1px solid #ddd;
    vertical-align: top;
}
tr:nth-child(even) {
    background-color: #f2f2f2;
}
</style>
""", unsafe_allow_html=True)

# Exibir tabela
st.write("## Tabela de Tratamento Antimicrobiano")
if foco_selecionado != "Todos":
    st.write(f"**Filtrado por:** {foco_selecionado}")

st.write(df.to_html(escape=False, index=False), unsafe_allow_html=True)

# Adicionar uma seção de busca rápida por antibiótico
st.markdown("---")
st.subheader("Busca Rápida por Antimicrobiano")

termo_busca = st.text_input("Digite o nome do antimicrobiano:", placeholder="Ex: vancomicina, meropenem...")

# Executar busca se termo foi digitado
if termo_busca:
    # Converter para minúsculas para busca insensível a maiúsculas
    termo_lower = termo_busca.lower()
    
    # Buscar nas colunas relevantes
    resultados = []
    
    for foco in focos_infecciosos:
        comunitario_lower = tratamentos[foco]["comunitario"].lower()