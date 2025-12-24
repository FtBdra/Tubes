import streamlit as st
import time
import tracemalloc
import re

def normalize(text):
    return re.sub(r'[^a-z0-9]', '', text.lower())

def is_palindrome_iterative(text):
    left = 0
    right = len(text) - 1

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
    start_time = time.perf_counter()
    result = func(*args)
    end_time = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "result": result,
        "time": end_time - start_time,
        "memory": peak / 1024  # KB
    }

st.set_page_config(page_title="Analisis Palindrom", layout="centered")

st.title("Analisis Kompleksitas Algoritma Palindrom")
st.subheader("Perbandingan Iteratif vs Rekursif")

input_text = st.text_area(
    "Masukkan kalimat:",
    placeholder="Contoh: Kasur ini rusak"
)

if st.button("Analisis"):
    if input_text.strip() == "":
        st.warning("Masukkan kalimat terlebih dahulu.")
    else:
        clean_text = normalize(input_text)
        # Analisis Iteratif
        iterative = analyze_algorithm(
            is_palindrome_iterative, clean_text
        )
        # Analisis Rekursif
        recursive = analyze_algorithm(
            is_palindrome_recursive, clean_text, 0, len(clean_text) - 1
        )

        st.markdown("##Hasil Verifikasi")
        col1, col2 = st.columns(2)

        with col1:
            st.success("Iteratif")
            st.write("Palindrom:", iterative["result"])
            st.write("Waktu Eksekusi:", f"{iterative['time']:.6f} detik")
            st.write("Memori Maks:", f"{iterative['memory']:.2f} KB")

        with col2:
            st.success("Rekursif")
            st.write("Palindrom:", recursive["result"])
            st.write("Waktu Eksekusi:", f"{recursive['time']:.6f} detik")
            st.write("Memori Maks:", f"{recursive['memory']:.2f} KB")
            
        st.markdown("## Perbandingan Kompleksitas")
        st.bar_chart({
            "Iteratif": [iterative["time"], iterative["memory"]],
            "Rekursif": [recursive["time"], recursive["memory"]]
        }, horizontal=False)
        st.caption("Baris 1: Waktu Eksekusi | Baris 2: Penggunaan Memori (KB)")

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
