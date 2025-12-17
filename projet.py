# =====================================================
# PROJET STREAMLIT : Tableau de bord interactif AVC
# Version professionnelle avec boutons et tableau d'aperçu
# =====================================================

# -------------------- IMPORTS --------------------
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder

# Configuration graphique
sns.set(style="whitegrid")

# -------------------- CONFIGURATION PAGE --------------------
st.set_page_config(
    page_title="Analyse des facteurs de risque d'AVC",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------- TITRE ET DESCRIPTION --------------------
st.title("Analyse des facteurs de risque d'AVC 🧠")
st.markdown("""
**Contexte :**  
Les accidents vasculaires cérébraux (AVC) représentent un problème majeur de santé publique dans le monde, touchant des millions de personnes chaque année. Identifier les facteurs de risque permet de mieux prévenir ces incidents et de cibler les interventions médicales.
Ce tableau de bord interactif analyse les données des patients afin de mettre en évidence les facteurs de risque clés tels que l’âge, le BMI, le niveau de glucose, le sexe et le statut tabagique, et fournit des statistiques et insights pour soutenir la prise de décision médicale.
""")

# -------------------- CHARGEMENT DES DONNÉES --------------------
file_path = r"C:\Users\bouas\Downloads\data_projetpython\healthcare-dataset-stroke-data.csv"
df = pd.read_csv(file_path)

# -------------------- NETTOYAGE --------------------
df['bmi'].fillna(df['bmi'].median(), inplace=True)
df['smoking_status'].fillna('Unknown', inplace=True)

categorical_cols = ['gender', 'smoking_status', 'work_type', 'Residence_type', 'ever_married']
for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])

# Colonnes originales pour certaines visualisations
df['work_type_original'] = pd.read_csv(file_path)['work_type']
df['Residence_type_original'] = pd.read_csv(file_path)['Residence_type']

# -------------------- APERÇU DES DONNÉES --------------------
st.subheader("Aperçu du dataset")
st.dataframe(df, height=400)  # Affichage grand tableau avec scroll

# ==================== INTERFACE AVEC BOUTONS ====================
st.subheader("Choisissez le graphique à afficher :")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Outliers BMI"):
        Q1 = df['bmi'].quantile(0.25)
        Q3 = df['bmi'].quantile(0.75)
        IQR = Q3 - Q1
        outliers = df[(df['bmi'] < Q1 - 1.5 * IQR) | (df['bmi'] > Q3 + 1.5 * IQR)]
        st.write(f"Nombre d'outliers détectés : {outliers.shape[0]}")
        fig, ax = plt.subplots()
        sns.boxplot(x=df['bmi'], ax=ax, color='#66b3ff')
        ax.set_title("Boxplot du BMI")
        st.pyplot(fig)

with col2:
    if st.button("Nombre de patients : Stroke vs No Stroke 🧠​"):
        stroke_counts = df['stroke'].value_counts()
        fig, ax = plt.subplots(figsize=(6,5))
        ax.bar(['No Stroke','Stroke'], stroke_counts.values, color=['#66b3ff','#ff9999'])
        ax.set_ylabel("Nombre de patients")
        ax.set_title("Nombre de patients avec et sans AVC")
        st.pyplot(fig)

    if st.button("Âge vs AVC"):
        fig, ax = plt.subplots(figsize=(8,5))
        sns.boxplot(data=df, x='stroke', y='age', ax=ax, palette=['#66b3ff','#ff9999'])
        ax.set_xticklabels(['No Stroke','Stroke'])
        ax.set_title("Distribution de l'âge selon l'AVC")
        st.pyplot(fig)

with col3:
    if st.button("Glucose & BMI vs AVC 🩸​"):
        fig1, ax1 = plt.subplots()
        sns.boxplot(data=df, x='stroke', y='avg_glucose_level', ax=ax1, palette=['#66b3ff','#ff9999'])
        ax1.set_xticklabels(['No Stroke','Stroke'])
        ax1.set_title("Average Glucose Level vs Stroke")
        st.pyplot(fig1)

        fig2, ax2 = plt.subplots()
        sns.boxplot(data=df, x='stroke', y='bmi', ax=ax2, palette=['#66b3ff','#ff9999'])
        ax2.set_xticklabels(['No Stroke','Stroke'])
        ax2.set_title("BMI vs Stroke")
        st.pyplot(fig2)

# -------------------- AUTRES GRAPHIQUES --------------------
#st.subheader("Autres visualisations :")
col4, col5, col6 = st.columns(3)

with col4:
    if st.button("Smoking Status vs AVC 🚬"):
        mapping = {0:'Ancien fumeur', 1:'Jamais fumé', 2:'Fumeur', 3:'Inconnu'}
        df['smoking_status_label'] = df['smoking_status'].map(mapping)
        fig, ax = plt.subplots(figsize=(8,5))
        sns.countplot(data=df, x='smoking_status_label', hue='stroke', ax=ax, palette=['#66b3ff','#ff9999'])
        ax.set_title("Smoking Status vs AVC")
        st.pyplot(fig)

with col5:
    if st.button("Gender vs AVC 👩/👨"):
        # Création de la figure
        fig, ax = plt.subplots(figsize=(6,4))
        
        # Graphique countplot
        sns.countplot(data=df, x='gender', hue='stroke', ax=ax, palette=['#66b3ff','#ff9999'])
        
        # Labels lisibles
        ax.set_xticklabels(['Female','Male'])
        ax.set_title("Gender vs Stroke")
        ax.set_xlabel("Gender")
        ax.set_ylabel("Nombre de patients")
        ax.legend(title="AVC", labels=["No Stroke", "Stroke"])
        
        # Affichage dans Streamlit
        st.pyplot(fig)


with col6:
    if st.button("Ever Married vs AVC 💍"):
        # Création de la figure
        fig, ax = plt.subplots(figsize=(6,4))
        
        # Graphique countplot
        sns.countplot(data=df, x='ever_married', hue='stroke', ax=ax, palette=['#66b3ff','#ff9999'])
        
        # Labels lisibles
        ax.set_xticklabels(['No','Yes'])
        ax.set_title("Ever Married vs Stroke")
        ax.set_xlabel("Ever Married")
        ax.set_ylabel("Nombre de patients")
        ax.legend(title="AVC", labels=["No Stroke", "Stroke"])
        
        # Affichage dans Streamlit
        st.pyplot(fig)

# -------------------- Work Type --------------------
if st.button("Work Type vs AVC 🏢"):
    fig, ax = plt.subplots(figsize=(8,3))
    sns.countplot(data=df, x='work_type_original', hue='stroke', ax=ax, palette=['#66b3ff','#ff9999'])
    ax.set_title("Work Type vs Stroke")
    ax.set_xticklabels(df['work_type_original'].unique(), rotation=7)
    ax.legend(title="AVC", labels=["No Stroke", "Stroke"])
    st.pyplot(fig)

# -------------------- Residence Type --------------------
if st.button("Stroke vs Residence Type🏠"):
    stroke_residence = df[df['stroke']==1]['Residence_type_original'].value_counts()
    fig, ax = plt.subplots(figsize=(2,2))  # <-- Taille compacte mais lisible
    ax.pie(
        stroke_residence,
        labels=stroke_residence.index,
        autopct='%1.1f%%',
        startangle=20,
        colors=['#66b3ff','#ff9999'],
        textprops={'fontsize': 8}  # <-- Texte plus lisible
    )
    ax.set_title("Proportion des patients avec Stroke selon le type de résidence", fontsize=9)
    st.pyplot(fig)
# -------------------- KPIs --------------------

st.subheader("📊 Statistiques clés")

with st.container():
    # Première ligne de KPIs
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(
            f"""
            <div style="padding: 20px; border: 2px solid #66b3ff; border-radius: 10px; text-align: center; background-color: #f5f5f5; color: #0e1117;">
                <h3>Total Patients</h3>
                <p style="font-size: 24px; font-weight: bold;">{df.shape[0]}</p>
            </div>
            """, unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            f"""
            <div style="padding: 20px; border: 2px solid #ff9999; border-radius: 10px; text-align: center; background-color: #fef2f2; color: #0e1117;">
                <h3>Patients avec AVC</h3>
                <p style="font-size: 24px; font-weight: bold;">{df['stroke'].sum()}</p>
            </div>
            """, unsafe_allow_html=True
        )
    with col3:
        st.markdown(
            f"""
            <div style="padding: 20px; border: 2px solid #ffcc66; border-radius: 10px; text-align: center; background-color: #fff8e1; color: #0e1117;">
                <h3>Pourcentage AVC</h3>
                <p style="font-size: 24px; font-weight: bold;">{df['stroke'].mean()*100:.2f}%</p>
            </div>
            """, unsafe_allow_html=True
        )

    # Deuxième ligne de KPIs
    st.write("")  # petit espace entre les lignes
    col4, col5, col6 = st.columns(3)
    
    with col4:
        st.markdown(
            f"""
            <div style="padding: 20px; border: 2px solid #66b3ff; border-radius: 10px; text-align: center; background-color: #f5f5f5; color: #0e1117;">
                <h3>BMI moyen</h3>
                <p style="font-size: 24px; font-weight: bold;">{df['bmi'].mean():.2f}</p>
            </div>
            """, unsafe_allow_html=True
        )
    with col5:
        st.markdown(
            f"""
            <div style="padding: 20px; border: 2px solid #ff9999; border-radius: 10px; text-align: center; background-color: #fef2f2; color: #0e1117;">
                <h3>Glucose moyen</h3>
                <p style="font-size: 24px; font-weight: bold;">{df['avg_glucose_level'].mean():.2f}</p>
            </div>
            """, unsafe_allow_html=True
        )
    with col6:
        st.markdown(
            f"""
            <div style="padding: 20px; border: 2px solid #ffcc66; border-radius: 10px; text-align: center; background-color: #fff8e1; color: #0e1117;">
                <h3>Âge moyen</h3>
                <p style="font-size: 24px; font-weight: bold;">{df['age'].mean():.1f}</p>
            </div>
            """, unsafe_allow_html=True
        )


# -------------------- INSIGHTS --------------------
st.subheader("Insights et recommandations 🎯")
st.markdown("""
- Les AVC sont plus fréquents chez les patients de plus de 60 ans.  
- Les patients avec un BMI élevé et un glucose élevé ont un risque plus important.  
- Les fumeurs ont un risque plus élevé d'AVC.  
- La majorité des patients avec AVC vivent en zone urbaine.  
- Les hommes et les femmes sont à risque, mais la distribution peut varier selon l’âge et le mode de vie.
""")
  
