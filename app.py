import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv

# 1. Load API Key secara aman
load_dotenv()
# Streamlit Cloud menggunakan st.secrets, lokal menggunakan .env
api_key = os.getenv("GOOGLE_API_KEY") or st.secrets.get("GOOGLE_API_KEY")

st.set_page_config(page_title="AI Translator Pro", page_icon="🚀", layout="wide")

st.title("🚀 AI Universal Translator (Next-Gen)")
st.write("Menerjemahkan dengan model Gemini terbaru untuk hasil yang lebih natural.")

# Sidebar Pengaturan
with st.sidebar:
    st.header("⚙️ Konfigurasi")
    
    # Input API Key manual jika tidak terdeteksi di sistem
    if not api_key:
        api_key = st.text_input("Google API Key:", type="password", help="Dapatkan di Google AI Studio")
    
    # Pilihan Model (Menggunakan Gemini 2.0 Flash sebagai standar terbaru)
    model_choice = st.selectbox(
        "Pilih Otak AI:",
        ["gemini-2.0-flash", "gemini-1.5-pro", "gemini-3-flash-preview"]
    )
    
    target_lang = st.selectbox(
        "Bahasa Tujuan:",
        ["English", "Japanese", "Korean", "Indonesian", "Arabic", "French", "Spanish", "German"]
    )
    
    tone = st.select_slider(
        "Gaya Bahasa:",
        options=["Sangat Formal", "Profesional", "Santai", "Bahasa Gaul/Slang"]
    )

# UI Kolom Utama
col1, col2 = st.columns(2)

with col1:
    source_text = st.text_area("Teks Sumber:", placeholder="Ketik di sini...", height=250)

if st.button("Terjemahkan ✨", use_container_width=True):
    if not api_key:
        st.error("Masukkan API Key terlebih dahulu!")
    elif not source_text:
        st.warning("Teks sumber tidak boleh kosong.")
    else:
        try:
            with st.spinner('AI sedang berpikir...'):
                # Inisialisasi Model Terbaru
                llm = ChatGoogleGenerativeAI(
                    model=model_choice, 
                    google_api_key=api_key,
                    temperature=0.3 # Suhu rendah agar hasil terjemahan konsisten
                )
                
                # Prompt yang lebih advanced (System Instruction tersembunyi)
                template = """
                Anda adalah mesin penerjemah AI mutakhir. 
                Tugas Anda:
                1. Deteksi bahasa asal secara otomatis.
                2. Terjemahkan ke dalam bahasa {bahasa_tujuan} dengan sangat akurat.
                3. Gunakan nada bicara {gaya}.
                4. Jika ada istilah teknis atau budaya, berikan adaptasi yang paling natural, bukan kaku.
                
                Teks: {teks_asal}
                
                Hasil Terjemahan:
                """
                
                prompt = ChatPromptTemplate.from_template(template)
                chain = prompt | llm
                
                # Eksekusi
                result = chain.invoke({
                    "bahasa_tujuan": target_lang,
                    "gaya": tone,
                    "teks_asal": source_text
                })
                
                with col2:
                    st.success(f"Hasil Terjemahan ({target_lang}):")
                    st.info(result.content)
                    
        except Exception as e:
            st.error(f"Terjadi kendala teknis: {str(e)}")

st.divider()
st.caption("Tips: Gunakan Gemini 2.0 Flash untuk kecepatan kilat, atau 1.5 Pro untuk dokumen panjang.")
