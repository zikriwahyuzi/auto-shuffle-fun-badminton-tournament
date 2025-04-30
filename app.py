import streamlit as st
import random
import graphviz

st.markdown("<h1 style='text-align: center; color: purple;'>🏸🏆 Fun Badminton Tournament Generator</h1>", unsafe_allow_html=True)

# Pilihan kategori
st.subheader("Pilih Kategori")
category = st.selectbox("Kategori Turnamen", ["Double", "Single"])

# Input nama peserta
st.subheader("Input Nama Peserta")
participants = st.text_area("Masukkan nama peserta (pisahkan dengan koma)", height=150)

if st.button("Proses Turnamen"):
    if participants:
        names = [name.strip() for name in participants.split(',') if name.strip()]
        total_players = len(names)

        if total_players < (4 if category == "Double" else 2):
            st.warning(f"Minimal {4 if category == 'Double' else 2} peserta untuk membuat turnamen.")
        elif category == "Double" and total_players % 2 != 0:
            st.warning("Jumlah peserta untuk kategori Double harus genap! Silakan tambahkan atau hapus nama peserta.")
        else:
            # Acak nama-nama peserta
            random.shuffle(names)

            if category == "Double":
                # Membentuk pasangan tim untuk kategori double
                teams = [(names[i], names[i+1]) for i in range(0, len(names), 2)]
                st.subheader("Hasil Pasangan Tim:")
                for i, team in enumerate(teams):
                    st.write(f"Tim {i+1}: {team[0]} & {team[1]}")

                def draw_bracket_graphviz(teams):
                    dot = graphviz.Digraph()
                    dot.attr(rankdir='LR')

                    team_labels = [f"{a} & {b}" for a, b in teams]
                    match_counter = 1
                    current_level = team_labels
                    round_num = 1

                    while len(current_level) > 1:
                        next_level = []
                        for i in range(0, len(current_level), 2):
                            match_id = f"R{round_num}_M{match_counter}"
                            if i + 1 < len(current_level):
                                dot.node(match_id, f"Match {match_counter}")
                                dot.edge(current_level[i], match_id)
                                dot.edge(current_level[i + 1], match_id)
                            else:
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
                # Untuk kategori single
                st.subheader("Hasil Pengundian Lawan:")
                for i, name in enumerate(names):
                    st.write(f"Peserta {i+1}: {name}")

                def draw_bracket_graphviz(players):
                    dot = graphviz.Digraph()
                    dot.attr(rankdir='LR')

                    match_counter = 1
                    current_level = players
                    round_num = 1

                    while len(current_level) > 1:
                        next_level = []
                        for i in range(0, len(current_level), 2):
                            match_id = f"R{round_num}_M{match_counter}"
                            if i + 1 < len(current_level):
                                dot.node(match_id, f"Match {match_counter}")
                                dot.edge(current_level[i], match_id)
                                dot.edge(current_level[i + 1], match_id)
                            else:
                                dot.node(current_level[i])
                                dot.edge(current_level[i], match_id)
                            next_level.append(match_id)
                            match_counter += 1
                        current_level = next_level
                        round_num += 1

                    return dot

                st.subheader("Visual Bracket (Graphviz)")
                dot = draw_bracket_graphviz(names)
                st.graphviz_chart(dot)

    else:
        st.warning("Silakan masukkan nama peserta terlebih dahulu!")

# Menambahkan informasi kredit di sidebar
st.sidebar.title("Tentang Aplikasi")
st.sidebar.info("""
Selamat datang di aplikasi turnamen badminton!🎉
- Pilih kategori turnamen (Double atau Single).
- Masukkan nama peserta.
- Klik tombol proses turnamen

_**'Kalau kita mau jadi juara, kita harus bisa mengalahkan diri sendiri dulu. Jangan pernah puas dengan apa yang sudah kita capai.'**_ - Taufik Hidayat
""")

st.sidebar.info("Aplikasi ini dibuat oleh **Zikri Wahyuzi** untuk membantu menyusun turnamen fun badminton. © 2025")
