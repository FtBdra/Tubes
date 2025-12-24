import streamlit as st
import time
import tracemalloc
import re
import matplotlib.pyplot as plt

def normalize(text):
    return re.sub(r'[^a-z0-9]', '', text.lower())

def is_palindrome_iterative(text):
    left, right = 0, len(text) - 1
    while left < right:
        if text[left] != text[right]:
            return False
        left += 1
        right -= 1
    return True

def is_palindrome_recursive(text, left, right):
    if left >= right:
        return True
    if text[left] != text[right]:
        return False
    return is_palindrome_recursive(text, left + 1, right - 1)

def analyze_algorithm(func, *args):
    tracemalloc.start()
    start = time.perf_counter()
    result = func(*args)
    end = time.perf_counter()
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return result, end - start, peak / 1024

st.set_page_config(page_title="Analisis Palindrom", layout="centered")
st.title("Analisis Kompleksitas Algoritma Palindrom")

text = st.text_area("Masukkan Kalimat")

if st.button("Analisis"):
    if text.strip() == "":
        st.warning("Input tidak boleh kosong")
    else:
        clean = normalize(text)

        it_res, it_time, it_mem = analyze_algorithm(
            is_palindrome_iterative, clean
        )

        rec_res, rec_time, rec_mem = analyze_algorithm(
            is_palindrome_recursive, clean, 0, len(clean) - 1
        )

        st.subheader("Hasil Verifikasi")
        col1, col2 = st.columns(2)
        with col1:
            st.write("Iteratif")
            st.write("Palindrom:", it_res)
            st.write("Waktu Eksekusi:", f"{it_time:.6f} detik")
            st.write("Memori Maks:", f"{it_mem:.2f} KB")
        with col2:
            st.write("Rekursif")
            st.write("Palindrom:", rec_res)
            st.write("Waktu Eksekusi:", f"{rec_time:.6f} detik")
            st.write("Memori Maks:", f"{rec_mem:.2f} KB")

        
        st.subheader("Perbandingan Waktu Eksekusi")
        fig1, ax1 = plt.subplots()
        ax1.bar(["Iteratif", "Rekursif"], [it_time, rec_time])
        ax1.set_ylabel("Waktu (detik)")
        ax1.set_ylim(bottom=0)
        st.pyplot(fig1)

        st.subheader("Perbandingan Penggunaan Memori")
        fig2, ax2 = plt.subplots()
        ax2.bar(["Iteratif", "Rekursif"], [it_mem, rec_mem])
        ax2.set_ylabel("Memori (KB)")
        ax2.set_ylim(bottom=0)
        st.pyplot(fig2)

st.markdown("---")
st.markdown("## Analisis Teoritis")

st.markdown("""
**Algoritma Iteratif**
- Kompleksitas waktu: **O(n)**
- Kompleksitas memori: **O(1)**
- Lebih efisien untuk input besar

**Algoritma Rekursif**
- Kompleksitas waktu: **O(n)**
- Kompleksitas memori: **O(n)** (call stack)
- Lebih elegan namun berisiko stack overflow

### Kesimpulan:
**Iteratif lebih unggul dalam efisiensi memori**,  
**Rekursif unggul dari sisi keterbacaan kode**.
""")
