import streamlit as st
import random
import graphviz

st.title("🎯 Fun Tournament Bracket Generator - Badminton Doubles")

# Input nama peserta
st.subheader("Input Nama Peserta")
participants = st.text_area("Masukkan nama peserta (pisahkan dengan koma)", height=150)

if st.button("Proses Turnamen"):
    if participants:
        names = [name.strip() for name in participants.split(',') if name.strip()]
        total_players = len(names)

        if total_players < 4:
            st.warning("Minimal 4 peserta untuk membuat turnamen.")
        elif total_players % 2 != 0:
            st.warning("Jumlah peserta harus genap! Silakan tambahkan atau hapus nama peserta untuk melanjutkan.")
        else:
            # Acak nama-nama peserta
            random.shuffle(names)

            # Membentuk pasangan tim
            teams = [(names[i], names[i+1]) for i in range(0, len(names), 2)]

            st.subheader("Hasil Pasangan Tim:")
            for i, team in enumerate(teams):
                st.write(f"Tim {i+1}: {team[0]} & {team[1]}")

            # Visualisasi bracket menggunakan Graphviz
            def draw_bracket_graphviz(teams):
                dot = graphviz.Digraph()
                dot.attr(rankdir='LR')  # Left to Right orientation

                # Menampilkan tim di awal bracket
                team_labels = [f"{a} & {b}" for a, b in teams]

                match_counter = 1
                current_level = team_labels
                round_num = 1

                # Membuat jalur pertandingan antar babak
                while len(current_level) > 1:
                    next_level = []  # Untuk babak berikutnya
                    for i in range(0, len(current_level), 2):
                        match_id = f"R{round_num}_M{match_counter}"
                        if i + 1 < len(current_level):  # Jika memiliki lawan
                            dot.node(match_id, f"Match {match_counter}")
                            dot.edge(current_level[i], match_id)
                            dot.edge(current_level[i + 1], match_id)
                        else:  # Jika tidak ada lawan (bye), masukkan tim langsung
                            dot.node(current_level[i])
                            dot.edge(current_level[i], match_id)
                        next_level.append(match_id)
                        match_counter += 1
                    current_level = next_level
                    round_num += 1

                return dot

            st.subheader("Visual Bracket (Graphviz)")
            dot = draw_bracket_graphviz(teams)
            st.graphviz_chart(dot)
    else:
        st.warning("Silakan masukkan nama peserta terlebih dahulu!")

# Menambahkan informasi kredit di sidebar
st.sidebar.title("Tentang Aplikasi")
st.sidebar.info("Aplikasi ini dibuat oleh **Zikri Wahyuzi** untuk membantu menyusun turnamen badminton double. © 2025")