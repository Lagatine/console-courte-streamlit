
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime

def create_scaled_diagram(Fed, Hed, b, h, d1):
    fig, ax = plt.subplots(figsize=(6, 4))
    scale = 100  # pour convertir m → cm visuellement

    console_rect = plt.Rectangle((0, 0), b * scale, h * scale, fill=None, edgecolor='black', linewidth=2)
    ax.add_patch(console_rect)

    ax.annotate(f'b = {b} m', xy=(b * scale / 2, -5), ha='center')
    ax.annotate(f'h = {h} m', xy=(-5, h * scale / 2), va='center', rotation='vertical')

    ax.arrow(b * scale / 2, h * scale, 0, -20, head_width=5, head_length=5, fc='red', ec='red')
    ax.text(b * scale / 2 + 5, h * scale - 10, f"Fed = {Fed} kN", color='red', va='center')

    if Hed != 0:
        ax.arrow(b * scale, h * scale / 2, -20, 0, head_width=5, head_length=5, fc='blue', ec='blue')
        ax.text(b * scale - 25, h * scale / 2 + 5, f"Hed = {Hed} kN", color='blue')

    ax.hlines(d1 * scale, 0, b * scale, colors='gray', linestyles='dotted')
    ax.text(b * scale + 5, d1 * scale, f"d1 = {d1} m", color='gray', va='bottom')

    ax.set_xlim(-10, b * scale + 30)
    ax.set_ylim(-20, h * scale + 20)
    ax.set_aspect('equal')
    ax.axis('off')
    plt.tight_layout()
    return fig

st.set_page_config(page_title="Console courte en béton armé", layout="centered")
st.title("Calcul d'une console courte en béton armé")
st.markdown("Entrez les paramètres ci-dessous pour effectuer le calcul :")

with st.form("parametres_console"):
    col1, col2 = st.columns(2)

    with col1:
        Fed = st.number_input("Force verticale Fed (kN)", value=32.25)
        b = st.number_input("Largeur b (m)", value=1.0)
        d1 = st.number_input("Enrobage d1 (m)", value=0.05)
        fyk = st.number_input("Résistance acier fyk (MPa)", value=500)

    with col2:
        Hed = st.number_input("Force horizontale Hed (kN)", value=0.0)
        h = st.number_input("Hauteur totale h (m)", value=0.15)
        fck = st.number_input("Résistance béton fck (MPa)", value=20)

    submitted = st.form_submit_button("Lancer le calcul")

if submitted:
    st.subheader("Résultats")
    d = h - d1
    Md = Fed * d
    Rd_max = 0.9 * fck * b * d * d / 1.5

    st.write(f"**Bras de levier d** = {d:.3f} m")
    st.write(f"**Moment fléchissant Md** = {Md:.2f} kNm")
    st.write(f"**Résistance maximale Rd,max** ≈ {Rd_max:.2f} kNm")

    ok = "✅ Dimensionnement OK" if Md <= Rd_max else "❌ Dimensionnement NON vérifié"
    st.success(ok if Md <= Rd_max else ok)

    # Afficher le schéma
    st.subheader("Schéma de la console (mise à l'échelle)")
    fig = create_scaled_diagram(Fed, Hed, b, h, d1)
    st.pyplot(fig)

    # Export résultats
    st.subheader("Exporter les résultats")
    if st.button("📥 Télécharger en Excel"):
        result_df = pd.DataFrame({
            "Paramètre": ["Fed", "Hed", "b", "h", "d1", "fyk", "fck", "d", "Md", "Rd_max"],
            "Valeur": [Fed, Hed, b, h, d1, fyk, fck, d, Md, Rd_max],
            "Unité": ["kN", "kN", "m", "m", "m", "MPa", "MPa", "m", "kNm", "kNm"]
        })
        file_name = f"resultats_console_{datetime.date.today()}.xlsx"
        result_df.to_excel(file_name, index=False)
        st.download_button("Télécharger le fichier Excel", data=open(file_name, "rb"), file_name=file_name)
