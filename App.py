import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv

# 1. Mengambil API Key dari file .env atau Environment Variable
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Konfigurasi Halaman Streamlit
st.set_page_config(page_title="Universal AI Translator", page_icon="🌐")

st.title("🌐 AI Universal Translator")
st.markdown("Terjemahkan teks apa pun ke berbagai bahasa dengan kekuatan AI.")

# Sidebar untuk pengaturan
with st.sidebar:
    st.header("Pengaturan")
    # Jika API Key tidak ada di .env, user bisa memasukkannya manual di UI
    if not api_key:
        api_key = st.text_input("Masukkan Google API Key:", type="password")
    
    target_lang = st.selectbox(
        "Pilih Bahasa Tujuan:",
        ["Inggris", "Jepang", "Korea", "Arab", "Prancis", "Jerman", "Mandarin", "Indonesia"]
    )
    
    tone = st.select_slider(
        "Gaya Bahasa:",
        options=["Sangat Formal", "Formal", "Santai", "Gaul"]
    )

# Area Input Teks
source_text = st.text_area("Masukkan teks yang ingin diterjemahkan:", placeholder="Contoh: Halo, apa kabar hari ini?")

if st.button("Terjemahkan Sekarang"):
    if not api_key:
        st.error("Waduh, API Key-nya belum ada nih. Masukkan dulu di sidebar ya!")
    elif source_text.strip() == "":
        st.warning("Teksnya kosong, apa yang mau diterjemahkan?")
    else:
        try:
            with st.spinner('Sedang menerjemahkan...'):
                # Inisialisasi Model AI (Google Gemini)
                llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=api_key)
                
                # Membuat Prompt yang dinamis
                template = """
                Kamu adalah penerjemah profesional yang ahli dalam berbagai bahasa.
                Tugasmu adalah menerjemahkan teks berikut ke dalam bahasa {bahasa_tujuan}.
                Gunakan gaya bahasa yang {gaya}.
                
                Teks: {teks_asal}
                
                Hasil Terjemahan:
                """
                
                prompt = ChatPromptTemplate.from_template(template)
                chain = prompt | llm
                
                # Eksekusi AI
                response = chain.invoke({
                    "bahasa_tujuan": target_lang,
                    "gaya": tone,
                    "teks_asal": source_text
                })
                
                # Tampilkan Hasil
                st.success("Selesai!")
                st.subheader(f"Hasil ({target_lang}):")
                st.write(response.content)
                
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")

st.divider()
st.caption("Dibuat dengan ❤️ menggunakan Streamlit & Gemini AI")
