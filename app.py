import streamlit as st
from itertools import combinations

# Konfiguracja strony (szeroki układ przypominający plakat/infografikę)
st.set_page_config(page_title="Rodziny Zbiorów – Infografika Interaktywna", layout="wide")

# Stylizacja CSS pod wygląd nowoczesnej infografiki + INTERAKTYWNA OŚ CZASU
st.markdown("""
<style>
    .block-container { padding-top: 2rem; padding-bottom: 3rem; }
    .card-blue {
        background-color: #f0f4f8; border-left: 6px solid #1e3a8a;
        padding: 15px; border-radius: 8px; margin-bottom: 10px;
    }
    .card-orange {
        background-color: #fff7ed; border-left: 6px solid #ea580c;
        padding: 15px; border-radius: 8px; margin-bottom: 10px;
    }
    .card-purple {
        background-color: #f5f3ff; border-left: 6px solid #7c3aed;
        padding: 15px; border-radius: 8px; margin-bottom: 10px;
    }

    /* --- STYLIZACJA INTERAKTYWNEJ OSI CZASU (HOVER TOOLTIPS) --- */
    .timeline-wrapper {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        position: relative;
        margin: 40px 10px 20px 10px;
        padding-top: 20px;
    }
    /* Pozioma linia łącząca punkty */
    .timeline-wrapper::before {
        content: '';
        position: absolute;
        top: 52px;
        left: 6%;
        right: 6%;
        height: 4px;
        background: linear-gradient(90deg, #1e3a8a, #7c3aed, #ea580c);
        border-radius: 2px;
        z-index: 1;
    }
    .timeline-item {
        position: relative;
        z-index: 2;
        width: 18%;
        text-align: center;
        cursor: pointer;
    }
    .timeline-icon {
        width: 64px;
        height: 64px;
        margin: 0 auto 12px auto;
        background: #ffffff;
        border: 4px solid #1e3a8a;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 28px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.08);
        transition: transform 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
    }
    .timeline-item:hover .timeline-icon {
        transform: scale(1.15);
        border-color: #7c3aed;
        box-shadow: 0 6px 18px rgba(124, 58, 237, 0.3);
    }
    .timeline-date {
        font-weight: 800;
        color: #1e3a8a;
        font-size: 15px;
        margin-bottom: 4px;
    }
    .timeline-title {
        font-weight: 600;
        color: #1e293b;
        font-size: 13.5px;
        line-height: 1.3;
    }
    /* Dymek wyskakujący po najechaniu */
    .timeline-tooltip {
        visibility: hidden;
        opacity: 0;
        width: 260px;
        background-color: #1e293b;
        color: #f8fafc;
        text-align: left;
        border-radius: 10px;
        padding: 14px;
        position: absolute;
        z-index: 99;
        bottom: 112%;
        left: 50%;
        transform: translateX(-50%) translateY(8px);
        transition: opacity 0.25s ease, transform 0.25s ease;
        box-shadow: 0 10px 25px rgba(0,0,0,0.25);
        font-size: 13px;
        line-height: 1.45;
        pointer-events: none;
    }
    .timeline-tooltip::after {
        content: "";
        position: absolute;
        top: 100%;
        left: 50%;
        margin-left: -7px;
        border-width: 7px;
        border-style: solid;
        border-color: #1e293b transparent transparent transparent;
    }
    .timeline-item:hover .timeline-tooltip {
        visibility: visible;
        opacity: 1;
        transform: translateX(-50%) translateY(0);
    }
</style>
""", unsafe_allow_html=True)

# --- NAGŁÓWEK ---
st.title("🧩 Architektura Rodzin Zbiorów")
st.markdown("**Interaktywne powtórzenie graficzne:** od zbioru potęgowego $\\mathcal{P}(X)$ po zbiory borelowskie $\\mathcal{B}(\\mathbb{R})$.")
st.divider()

# --- SEKCJA 1: GŁÓWNA MAPA RELACJI (GRAPHVIZ) + PORÓWNANIE ---
col_map, col_table = st.columns([1.1, 1.2], gap="large")

with col_map:
    st.subheader("🗺️ Mapa zależności (Od ogółu do szczegółu)")
    graph = """
    digraph G {
        rankdir=TB;
        bgcolor="transparent";
        node [shape=box, style="rounded,filled", fontname="Arial", fontsize=11, margin="0.15,0.1"];
        edge [color="#64748b", penwidth=1.5];

        PX [label="Zbiór potęgowy P(X)\\n(Wszystkie podzbiory X)", fillcolor="#e2e8f0", color="#475569"];
        ALG [label="Algebra A\\n(Dopełnienia + skończone sumy)", fillcolor="#dbeafe", color="#1d4ed8"];
        SIG [label="σ-algebra Σ\\n(Dopełnienia + przeliczalne sumy)", fillcolor="#bfdbfe", color="#1e40af"];
        TOP [label="Topologia T\\n(Dowolne sumy + skończone przekroje)", fillcolor="#ffedd5", color="#c2410c"];
        GEN [label="σ-algebra generowana σ(G)\\n(Najmniejsza σ-algebra zawierająca G)", fillcolor="#e0e7ff", color="#4338ca"];
        BOR [label="Zbiory borelowskie B(R)\\nσ(T_nat) — pomost między światami", fillcolor="#ede9fe", color="#6d28d9"];

        PX -> ALG [label=" ograniczenie operacji"];
        PX -> TOP [label=" rezygnacja z dopełnień"];
        ALG -> SIG [label=" przejście do nieskończoności"];
        SIG -> GEN [label=" generowanie z rodziny G"];
        TOP -> BOR [label=" wrzucenie do maszyny σ(·)"];
        GEN -> BOR [label=" G = zbiory otwarte"];
    }
    """
    st.graphviz_chart(graph, use_container_width=True)

with col_table:
    st.subheader("⚖️ Podobieństwa i różnice (Wspólny mianownik: $\\emptyset, X \\in \\mathcal{F}$)")
    
    st.markdown("""
    | Rodzina $\\mathcal{F} \\subseteq \\mathcal{P}(X)$ | Dopełnienia ($A^c$) | Sumy ($\\bigcup$) | Przekroje ($\\bigcap$) |
    | :--- | :---: | :---: | :---: |
    | **Zbiór potęgowy $\\mathcal{P}(X)$** | ✅ TAK | Dowolne | Dowolne |
    | **Algebra $\\mathcal{A}$** | ✅ TAK | **Skończone** ($\\bigcup_{i=1}^n$) | Skończone |
    | **$\\sigma$-algebra $\\Sigma$** | ✅ TAK | **Przeliczalne** ($\\bigcup_{n=1}^\\infty$) | Przeliczalne |
    | **Topologia $\\mathcal{T}$** | ❌ **NIE** | **Dowolne** ($\\bigcup_{i \\in I}$) | **Skończone** ($\\bigcap_{i=1}^n$) |
    """)

    st.markdown('<div class="card-blue"><b>Świat Mierzalności (Algebry i σ-algebry):</b><br>Kluczowa jest symetria względem dopełnień (<i>A ∈ Σ ⇒ A<sup>c</sup> ∈ Σ</i>). Dzięki prawom De Morgana zamkniętość na sumy automatycznie wymusza zamkniętość na przekroje.</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-orange"><b>Świat Bliskości (Topologie):</b><br>Dopełnienie zbioru otwartego jest zbiorem domkniętym (nie musi być otwarte!). Dlatego topologia wymaga osobnych aksjomatów dla sum i przekrojów.</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-purple"><b>Pomost — Zbiory Borelowskie 𝓑(ℝ):</b><br>Powstają przez wzięcie topologii naturalnej i domknięcie jej na dopełnienia oraz przeliczalne sumy: <i>𝓑(ℝ) = σ(𝓣<sub>nat</sub>)</i>.</div>', unsafe_allow_html=True)

st.divider()

# --- SEKCJA 2: INTERAKTYWNE LABORATORIUM NA X = {1, 2, 3} ---
st.subheader("🧪 Interaktywne laboratorium: Zbadaj rodzinę podzbiorów na $X = \\{1, 2, 3\\}$")
st.caption("Zaznacz podzbiory tworzące rodzinę $\\mathcal{F} \\subseteq \\mathcal{P}(X)$, a algorytm sprawdzi aksjomaty i wyznaczy $\\sigma(\\mathcal{F})$.")

X = frozenset({1, 2, 3})
all_subsets = [frozenset(c) for r in range(len(X) + 1) for c in combinations(X, r)]

def fmt(s):
    return "∅" if len(s) == 0 else "{" + ",".join(map(str, sorted(s))) + "}"

subset_map = {fmt(s): s for s in all_subsets}

col_sel, col_res = st.columns([1.2, 1])

with col_sel:
    selected_labels = st.multiselect(
        "Wybierz elementy rodziny F (domyślnie przykładowa topologia niesymetryczna):",
        options=list(subset_map.keys()),
        default=["∅", "{1}", "{1,2}", "{1,2,3}"]
    )
    F = {subset_map[lbl] for lbl in selected_labels}

has_empty_and_X = (frozenset() in F) and (X in F)
closed_comp = all((X - A) in F for A in F)
closed_union = all((A | B) in F for A in F for B in F)
closed_inter = all((A & B) in F for A in F for B in F)

is_algebra = has_empty_and_X and closed_comp and closed_union
is_topology = has_empty_and_X and closed_union and closed_inter

sigma_F = set(F) | {frozenset(), X}
changed = True
while changed:
    new_sets = set()
    for A in sigma_F:
        new_sets.add(X - A)
        for B in sigma_F:
            new_sets.add(A | B)
    if not new_sets.issubset(sigma_F):
        sigma_F |= new_sets
    else:
        changed = False

with col_res:
    st.markdown("**Werdykt algorytmu:**")
    c1, c2 = st.columns(2)
    c1.metric("Czy to Algebra / σ-algebra?", "TAK ✅" if is_algebra else "NIE ❌")
    c2.metric("Czy to Topologia?", "TAK ✅" if is_topology else "NIE ❌")
    
    st.info(f"**Wygenerowana $\\sigma(\\mathcal{{F}})$** (moc = {len(sigma_F)}):  \n" + 
            ", ".join(sorted([fmt(s) for s in sigma_F], key=lambda x: (len(x), x))))

st.divider()

# --- SEKCJA 3: KLUCZOWE TWIERDZENIA ---
st.subheader("📌 Kluczowe twierdzenia i fakty na egzamin")
col_t1, col_t2 = st.columns(2, gap="large")

with col_t1:
    st.markdown("""
    1. **Hierarchia:** Każda $\\sigma$-algebra jest algebrą, ale nie odwrotnie (np. rodzina zbiorów skończonych i koskończonych na $\\mathbb{N}$ jest algebrą, lecz nie $\\sigma$-algebrą).
    2. **Operacje na rodzinach:** Przekrój dowolnej liczby $\\sigma$-algebr (lub topologii) zawsze jest $\\sigma$-algebrą (topologią). **Suma dwóch $\\sigma$-algebr nie musi nią być!**
    """)

with col_t2:
    st.markdown("""
    3. **Równoważne generatory $\\mathcal{B}(\\mathbb{R})$:** Przedziały otwarte $(a,b)$, domknięte $[a,b]$ oraz półproste $(-\\infty, a]$ generują dokładnie tę samą $\\sigma$-algebrę borelowską.
    4. **Argument mocowy (Zbiór Vitalego):** $|\\mathcal{B}(\\mathbb{R})| = \\mathfrak{c} < 2^{\\mathfrak{c}} = |\\mathcal{P}(\\mathbb{R})|$, skąd wynika istnienie podzbiorów $\\mathbb{R}$, które nie są borelowskie.
    """)

st.divider()

# --- SEKCJA 4: INTERAKTYWNA OŚ CZASU (NAJEDŹ MYSZKĄ NA IKONKĘ) ---
st.subheader("⏳ Kamienie milowe teorii miary i topologii")
st.caption("💡 **Wskazówka:** Najedź kursorem myszy na dowolną ikonę na osi czasu, aby zobaczyć szczegóły odkrycia.")

timeline_html = """
<div class="timeline-wrapper">
    <div class="timeline-item">
        <div class="timeline-tooltip">
            <b>Georg Cantor (1874–1895)</b><br>
            Stworzył teorię mnogości i zdefiniował <b>zbiór potęgowy P(X)</b>. Udowodnił twierdzenie Cantora (|X| &lt; |P(X)|), pokazując hierarchię nieskończoności, bez której nie powstałaby współczesna teoria miary.
        </div>
        <div class="timeline-icon">∞</div>
        <div class="timeline-date">1874–1895</div>
        <div class="timeline-title">Zbiór potęgowy<br>i teoria mnogości</div>
    </div>

    <div class="timeline-item">
        <div class="timeline-tooltip">
            <b>Émile Borel (1898)</b><br>
            Wprowadził pojęcie <b>zbiorów borelowskich B(R)</b> w pracy <i>Leçons sur la théorie des fonctions</i>. Zauważył, że aby mierzyć skomplikowane podzbiory prostej, trzeba domknąć przedziały na przeliczalne sumy i dopełnienia.
        </div>
        <div class="timeline-icon">📏</div>
        <div class="timeline-date">1898</div>
        <div class="timeline-title">Narodziny zbiorów<br>borelowskich</div>
    </div>

    <div class="timeline-item">
        <div class="timeline-tooltip">
            <b>Henri Lebesgue (1901–1902)</b><br>
            Opracował <b>miarę i całkę Lebesgue'a</b>. Uzupełnił zbiory borelowskie o podzbiory zbiorów miary zero, ugruntowując centralną rolę <b>σ-algebr</b> jako dziedziny funkcji mierzalnych.
        </div>
        <div class="timeline-icon">∫</div>
        <div class="timeline-date">1901–1902</div>
        <div class="timeline-title">Miara i całka<br>Lebesgue'a</div>
    </div>

    <div class="timeline-item">
        <div class="timeline-tooltip">
            <b>Felix Hausdorff (1914)</b><br>
            W dziele <i>Grundzüge der Mengenlehre</i> podał aksjomatyczną definicję <b>przestrzeni topologicznej</b>. Oddzielił pojęcie bliskości i ciągłości (topologia) od mierzalności (σ-algebra).
        </div>
        <div class="timeline-icon">🍩</div>
        <div class="timeline-date">1914</div>
        <div class="timeline-title">Aksjomatyzacja<br>topologii</div>
    </div>

    <div class="timeline-item">
        <div class="timeline-tooltip">
            <b>Andriej Kołmogorow (1933)</b><br>
            Oparł cały rachunek prawdopodobieństwa na teorii miary, definiując przestrzeń probabilistyczną <b>(Ω, F, P)</b>, gdzie F to σ-algebra zdarzeń losowych, a P to miara unormowana (P(Ω)=1).
        </div>
        <div class="timeline-icon">🎲</div>
        <div class="timeline-date">1933</div>
        <div class="timeline-title">Prawdopodobieństwo<br>na σ-algebrach</div>
    </div>
</div>
"""
st.markdown(timeline_html, unsafe_allow_html=True)

# --- STOPKA: BIBLIOGRAFIA I OŚWIADCZENIE GENAI ---
st.divider()
st.caption("""
**Bibliografia:** R. Engelking, *Topologia ogólna*; P. Billingsley, *Prawdopodobieństwo i miara*; materiały wykładowe z przedmiotu.  
**Oświadczenie dotyczące GenAI:** Aplikacja interaktywna oraz schematy wizualne zostały przygotowane z wykorzystaniem narzędzia GenAI (Gemini) w zakresie struktury kodu Python/Streamlit. Wszystkie definicje matematyczne, twierdzenia oraz daty historyczne zostały zweryfikowane przez autorkę w literaturze przedmiotu.
""")