import re
from itertools import combinations
from pathlib import Path

import streamlit as st

# ---------------------------------------------------------------------------
# Konfiguracja strony
# ---------------------------------------------------------------------------
st.set_page_config(page_title="Rodziny Zbiorów – Infografika Interaktywna", layout="wide")

st.markdown(
    """
<style>
    .block-container { padding-top: 2rem; padding-bottom: 3rem; }
    .card-blue {
        background-color: #f0f4f8; border-left: 6px solid #1e3a8a;
        padding: 15px; border-radius: 8px; margin-bottom: 10px; color: #1e293b;
    }
    .card-orange {
        background-color: #fff7ed; border-left: 6px solid #ea580c;
        padding: 15px; border-radius: 8px; margin-bottom: 10px; color: #1e293b;
    }
    .card-purple {
        background-color: #f5f3ff; border-left: 6px solid #7c3aed;
        padding: 15px; border-radius: 8px; margin-bottom: 10px; color: #1e293b;
    }
</style>
""",
    unsafe_allow_html=True,
)

BASE_DIR = Path(__file__).parent

DOMYSLNE_WZORY = """
Topologia:
Rodzinę $\\mathcal{O}$ podzbiorów zbioru $X$ nazywamy **topologią w zbiorze $X$**, jeżeli:
1. $\\emptyset \\in \\mathcal{O},\\ X \\in \\mathcal{O}$,
2. $V_i \\in \\mathcal{O},\\ i = 1, 2, \\dots, n \\implies V_1 \\cap V_2 \\cap \\dots \\cap V_n \\in \\mathcal{O}$,
3. $\\{V_\\alpha\\}$ – dowolna rodzina zbiorów w $\\mathcal{O} \\implies \\bigcup_\\alpha V_\\alpha \\in \\mathcal{O}$.

Przestrzeń $X$ z topologią $\\mathcal{O}$, a formalnie parę $(X, \\tau)$, nazywamy **przestrzenią topologiczną**, a elementy rodziny $\\mathcal{O}$ – **zbiorami otwartymi w $X$**.
---
Algebra:
Rodzinę $\\mathcal{M} \\subset 2^X$ podzbiorów przestrzeni $X$ nazywamy **algebrą** (ciałem zbiorów), gdy:
1. $X \\in \\mathcal{M}$,
2. $A \\in \\mathcal{M} \\Rightarrow A' \\in \\mathcal{M}$,
3. $A, B \\in \\mathcal{M} \\Rightarrow A \\cup B \\in \\mathcal{M}$.

Z powyższych warunków wynika zamkniętość na różnicę, skończone sumy i skończone przekroje.
---
Sigma-algebra:
Rodzinę $\\mathcal{M} \\subset 2^X$ podzbiorów przestrzeni $X$ nazywamy **$\\sigma$-algebrą** (lub **$\\sigma$-ciałem**), gdy:
1. $X \\in \\mathcal{M}$,
2. $A \\in \\mathcal{M} \\Rightarrow A' \\in \\mathcal{M}$,
3. $A_n \\in \\mathcal{M},\\ n = 1, 2, 3, \\dots \\Rightarrow \\bigcup_{n=1}^\\infty A_n \\in \\mathcal{M}$.

Z prawa De Morgana wynika także zamkniętość na przeliczalne przekroje.
---
Zbiór potęgowy:
Jeżeli $X$ jest przestrzenią, to możemy zdefiniować maksymalną rodzinę jego podzbiorów:
$$2^X := \\{A : A \\subset X\\}.$$
$2^X$ nazywamy **zbiorem potęgowym**. Jeżeli $|X| = n$, to $2^X$ składa się z $2^n$ podzbiorów przestrzeni $X$.
---
Sigma-algebra generowana:
Niech $\\mathcal{M} \\subset 2^X$ będzie rodziną podzbiorów $X$. Rodzinę
$$\\bigcap \\{\\mathcal{A} : \\mathcal{M} \\subset \\mathcal{A},\\ \\mathcal{A} - \\sigma\\text{-algebra}\\}$$
nazywamy **$\\sigma$-algebrą generowaną przez rodzinę $\\mathcal{M}$**. Będziemy ją oznaczać $\\sigma(\\mathcal{M})$ lub $\\mathcal{M}^*$.

Własności:
1. jeśli $\\mathcal{M}$ jest $\\sigma$-algebrą, to $\\mathcal{M}^* = \\mathcal{M}$,
2. $(\\mathcal{F}^*)^* = \\mathcal{F}^*$,
3. jeśli $\\mathcal{F}_1 \\subset \\mathcal{F}_2 \\subset 2^X$, to $\\mathcal{F}_1^* \\subset \\mathcal{F}_2^*$.
---
Przestrzeń mierzalna:
Jeżeli $\\mathcal{M} \\subset 2^X$ jest $\\sigma$-algebrą, to parę $(X, \\mathcal{M})$ nazywamy **przestrzenią mierzalną**, a elementy $\\mathcal{M}$ – **zbiorami mierzalnymi**.
---
Zbiory borelowskie:
Załóżmy, że $(X, \\mathcal{O}_X)$ jest przestrzenią topologiczną. Istnieje najmniejsza $\\sigma$-algebra $\\mathcal{B}_X$ w $X$ taka, że każdy otwarty podzbiór przestrzeni $X$ należy do $\\mathcal{B}_X$.

Elementy rodziny $\\mathcal{B}_X$ nazywamy **zbiorami borelowskimi w $X$**, tzn.
$$\\mathcal{O}_X^* = \\mathcal{B}_X.$$
---
Rozszerzony zbiór liczb rzeczywistych:
Rozszerzony zbiór liczb rzeczywistych ma postać:
$$\\overline{\\mathbb{R}} = [-\\infty, +\\infty] = \\mathbb{R} \\cup \\{-\\infty, +\\infty\\}.$$
Naturalne uporządkowanie zachowuje porządek na $\\mathbb{R}$, przy czym $-\\infty < x < +\\infty$ dla każdego $x \\in \\mathbb{R}$.
"""


def read_optional(filename: str):
    """Czyta plik obok app.py; zwraca None, jeśli go brak."""
    path = BASE_DIR / filename
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8")


def latex_for_streamlit(text: str) -> str:
    """Zamienia \\( ... \\) na $...$ oraz \\[ ... \\] na $$...$$."""
    text = re.sub(r"\\\[(.+?)\\\]", lambda m: "$$" + m.group(1).strip() + "$$", text, flags=re.DOTALL)
    text = re.sub(r"\\\((.+?)\\\)", lambda m: "$" + m.group(1).strip() + "$", text, flags=re.DOTALL)
    return text


# ---------------------------------------------------------------------------
# Nawigacja
# ---------------------------------------------------------------------------
widok = st.sidebar.radio(
    "Wybierz sekcję",
    [
        "Wszystkie sekcje",
        "Mapa i laboratorium",
        "Wzory i definicje",
        "Daty historyczne",
        "Kawiarnia Szkocka",
    ],
)
pokaz_mape = widok in ("Wszystkie sekcje", "Mapa i laboratorium")
pokaz_wzory = widok in ("Wszystkie sekcje", "Wzory i definicje")
pokaz_daty = widok in ("Wszystkie sekcje", "Daty historyczne")
pokaz_kawiarnie = widok in ("Wszystkie sekcje", "Kawiarnia Szkocka")

# ---------------------------------------------------------------------------
# Nagłówek
# ---------------------------------------------------------------------------
st.title("Architektura Rodzin Zbiorów")
st.markdown(
    "**Interaktywne powtórzenie graficzne:** od zbioru potęgowego $2^X$ "
    "po zbiory borelowskie $\\mathcal{B}_X = \\mathcal{O}_X^*$."
)
st.divider()

# ---------------------------------------------------------------------------
# SEKCJA 1 i 2: mapa + laboratorium
# ---------------------------------------------------------------------------
if pokaz_mape:
    col_map, col_table = st.columns([1.1, 1.2], gap="large")

    with col_map:
        st.subheader("Mapa zależności")
        graph = """
    digraph G {
        rankdir=TB;
        bgcolor="transparent";
        nodesep=0.55;
        ranksep=0.75;
        splines=true;

        node [shape=box, style="rounded,filled", fontname="Helvetica", fontsize=15,
              margin="0.3,0.18", penwidth=2];
        edge [color="#64748b", penwidth=1.8, fontname="Helvetica", fontsize=13,
              fontcolor="#334155", arrowsize=0.9];

        PX  [label="Zbiór potęgowy 2^X\\nwszystkie podzbiory X",
             fillcolor="#e2e8f0", color="#475569"];

        subgraph cluster_mierzalnosc {
            label="Świat mierzalności"; labeljust=l;
            fontname="Helvetica-Bold"; fontsize=14; fontcolor="#1e40af";
            style="rounded,dashed"; color="#93c5fd";

            ALG [label="Algebra M\\ndopełnienia A' + sumy skończone",
                 fillcolor="#dbeafe", color="#1d4ed8"];
            SIG [label="σ-algebra M\\ndopełnienia A' + sumy przeliczalne",
                 fillcolor="#bfdbfe", color="#1e40af"];
            GEN [label="σ-algebra generowana σ(M) lub M*\\nnajmniejsza σ-algebra zawierająca M",
                 fillcolor="#e0e7ff", color="#4338ca"];
        }

        subgraph cluster_bliskosc {
            label="Świat otwartości"; labeljust=l;
            fontname="Helvetica-Bold"; fontsize=14; fontcolor="#c2410c";
            style="rounded,dashed"; color="#fdba74";

            TOP [label="Topologia O (lub τ)\\nsumy dowolne + przekroje skończone",
                 fillcolor="#ffedd5", color="#c2410c"];
        }

        BOR [label="Zbiory borelowskie B_X = O_X*\\npomost między światami",
             fillcolor="#ede9fe", color="#6d28d9", fontsize=16];

        PX  -> ALG [label="  domknięcie na\\l  dopełnienia i sumy skończone\\l"];
        PX  -> TOP [label="  domknięcie na\\l  sumy dowolne i przekroje skończone\\l"];
        ALG -> SIG [label="  sumy przeliczalne\\l"];
        SIG -> GEN [label="  generowanie z rodziny M\\l"];
        TOP -> GEN [label="  M = O\\l  (rodzina generująca to topologia)\\l",
                    color="#ea580c", fontcolor="#c2410c"];
        GEN -> BOR [label="  O = O_X\\l  (topologia w przestrzeni X)\\l",
                    color="#7c3aed", fontcolor="#6d28d9"];
    }
    """
        st.graphviz_chart(graph, use_container_width=True)

    with col_table:
        st.subheader("⚖️ Podobieństwa i różnice (wspólny warunek: $\\emptyset, X \\in \\mathcal{F}$)")
        st.markdown(
            """
| Rodzina $\\mathcal{F} \\subset 2^X$ | Dopełnienia ($A'$) | Sumy ($\\bigcup$) | Przekroje ($\\bigcap$) |
| :--- | :---: | :---: | :---: |
| **Zbiór potęgowy $2^X$** | ✅ TAK | Dowolne | Dowolne |
| **Algebra $\\mathcal{M}$** | ✅ TAK | **Skończone** | Skończone |
| **$\\sigma$-algebra $\\mathcal{M}$** | ✅ TAK | **Przeliczalne** | Przeliczalne |
| **Topologia $\\mathcal{O}$** | ❌ **NIE** (w ogólności) | **Dowolne** | **Skończone** |
"""
        )

    st.divider()

    # --- Laboratorium na X = {1,2,3} ---
    st.subheader("🧪 Laboratorium: zbadaj rodzinę podzbiorów $X = \\{1, 2, 3\\}$")
    st.caption(
        "Zaznacz podzbiory tworzące rodzinę $\\mathcal{M} \\subset 2^X$ "
        "— aplikacja sprawdzi aksjomaty i wyznaczy $\\sigma(\\mathcal{M}) = \\mathcal{M}^*$."
    )

    X = frozenset({1, 2, 3})
    all_subsets = [frozenset(c) for r in range(len(X) + 1) for c in combinations(sorted(X), r)]

    def fmt(s):
        return "∅" if len(s) == 0 else "{" + ",".join(map(str, sorted(s))) + "}"

    subset_map = {fmt(s): s for s in all_subsets}

    col_sel, col_res = st.columns([1.2, 1])

    with col_sel:
        selected_labels = st.multiselect(
            "Wybierz elementy rodziny M (domyślnie: topologia, która nie jest algebrą):",
            options=list(subset_map.keys()),
            default=["∅", "{1}", "{1,2}", "{1,2,3}"],
        )
        M = {subset_map[lbl] for lbl in selected_labels}

    has_empty_and_X = (frozenset() in M) and (X in M)
    closed_comp = all((X - A) in M for A in M)
    closed_union = all((A | B) in M for A in M for B in M)
    closed_inter = all((A & B) in M for A in M for B in M)

    is_algebra = has_empty_and_X and closed_comp and closed_union
    is_topology = has_empty_and_X and closed_union and closed_inter
    is_sigma = is_algebra

    sigma_M = set(M) | {frozenset(), X}
    changed = True
    while changed:
        new_sets = set()
        for A in sigma_M:
            new_sets.add(X - A)
            for B in sigma_M:
                new_sets.add(A | B)
        if new_sets.issubset(sigma_M):
            changed = False
        else:
            sigma_M |= new_sets

    with col_res:
        st.markdown("**Werdykt algorytmu:**")
        c1, c2, c3 = st.columns(3)
        c1.metric("Algebra?", "TAK ✅" if is_algebra else "NIE ❌")
        c2.metric("σ-algebra?", "TAK ✅" if is_sigma else "NIE ❌")
        c3.metric("Topologia?", "TAK ✅" if is_topology else "NIE ❌")
        st.caption("Dla skończonego X każda algebra jest σ-algebrą (Zadanie 1.5).")

        st.info(
            f"**Wygenerowana $\\sigma(\\mathcal{{M}}) = \\mathcal{{M}}^*$** (liczba zbiorów = {len(sigma_M)}):  \n"
            + ", ".join(sorted((fmt(s) for s in sigma_M), key=lambda x: (len(x), x)))
        )

    st.divider()

# ---------------------------------------------------------------------------
# SEKCJA 3: daty z daty.md
# ---------------------------------------------------------------------------
if pokaz_daty:
    st.subheader("⏳ Kamienie milowe teorii miary i topologii")

    dates_text = read_optional("daty.md")
    if dates_text is None:
        st.warning("Nie znaleziono pliku `daty.md` obok `app.py`.")
    else:
        dates_text = latex_for_streamlit(dates_text)
        events = []
        for match in re.finditer(
            r"^###\s+(.+?)\n(?P<body>.*?)(?=^###\s+|\Z)",
            dates_text,
            flags=re.MULTILINE | re.DOTALL,
        ):
            events.append((match.group(1).strip(), match.group("body").strip()))

        for heading, body in events:
            st.markdown(f"### {heading}")
            st.markdown(body)

    st.divider()

# ---------------------------------------------------------------------------
# SEKCJA 4: wzory (zawsze zgodne ze skryptem)
# ---------------------------------------------------------------------------
if pokaz_wzory:
    st.subheader("🧾 Najważniejsze definicje i wzory")
    tresc_latex = DOMYSLNE_WZORY
    bloki = [b.strip() for b in tresc_latex.split("---") if b.strip()]

    card_styles = []
    for i in range(len(bloki)):
        hue = round(360 * i / len(bloki))
        card_styles.append(
            f"""
            .st-key-formula-card-{i} {{
                background-color: hsl({hue}, 75%, 94%);
                border: 1px solid hsl({hue}, 50%, 84%);
                border-radius: 0.75rem;
                padding: 1rem;
                color: #1e293b;
            }}
            """
        )
    st.markdown(
        f"<style>{''.join(card_styles)}</style>",
        unsafe_allow_html=True,
    )

    kolumny = st.columns(2, gap="large")
    for i, blok in enumerate(bloki):
        with kolumny[i % 2]:
            with st.container(border=True, key=f"formula-card-{i}"):
                lines = blok.splitlines()
                title = lines[0].strip().rstrip(":")
                body = "\n".join(lines[1:]).strip()
                st.markdown(f"**{title.replace('_', ' ').capitalize()}**")
                st.markdown(body if body else lines[0])
    st.divider()

# ---------------------------------------------------------------------------
# SEKCJA 5: Kawiarnia Szkocka / szkoła lwowska
# ---------------------------------------------------------------------------
if pokaz_kawiarnie:
    st.subheader("☕ Kawiarnia Szkocka i lwowska szkoła matematyczna")
    st.markdown(
        """
Lwowska szkoła matematyczna (lata 20. i 30. XX w., skupiona wokół Stefana Banacha i Hugona Steinhausa)
jest najbardziej znana z **analizy funkcjonalnej**, ale wniosła też ważny wkład do teorii mnogości,
topologii, teorii miary i całki oraz rachunku prawdopodobieństwa. Teoria miary i całki rozwijała się
równolegle w innych ośrodkach (m.in. w Warszawie wokół *Fundamenta Mathematicae*, założonych w 1920 r.).

Czasopismo *Studia Mathematica* założyli w 1929 r. Banach i Steinhaus; publikowano w nim głównie prace
z analizy funkcjonalnej i pokrewnych działów. Matematycy spotykali się w **Kawiarni Szkockiej**, gdzie od
1935 r. prowadzono **Księgę Szkocką** — zeszyt z problemami (ponad 190 wpisów, ostatnie z 1941 r.),
wydany później w tłumaczeniu angielskim pod redakcją R. D. Mauldina.
"""
    )

    st.markdown("### Kluczowe postacie i ich wkład")
    osoby = [
        (
            "Stefan Banach (1892–1945)",
            "Twórca nowoczesnej analizy funkcjonalnej (przestrzenie Banacha, *Théorie des opérations "
            "linéaires*, 1932). W pracy *Sur le problème de la mesure* (1923) wykazał istnienie skończenie "
            "addytywnej, niezmienniczej miary na wszystkich ograniczonych podzbiorach prostej i płaszczyzny. "
            "Z Alfredem Tarskim (warszawianinem) opublikował w 1924 r. paradoks Banacha–Tarskiego "
            "(wymaga aksjomatu wyboru, działa w ℝ³ i wyżej). Z Kuratowskim (1929) badał uogólnienia problemu miary.",
        ),
        (
            "Hugo Steinhaus (1887–1972)",
            "Współzałożyciel szkoły lwowskiej. Twierdzenie Banacha–Steinhausa (1927), twierdzenie Steinhausa "
            "o sumie zbiorów o dodatniej mierze, prace o szeregach losowych i podstawach rachunku "
            "prawdopodobieństwa opartych na mierze (1923, 1930) — jeden z prekursorów ujęcia Kołmogorowa (1933). "
        
        ),
        (
            "Stanisław Ulam (1909–1984)",
            "W pracy *Zur Masstheorie in der allgemeinen Mengenlehre* (1930) zapoczątkował badania nad "
            "**kardynałami mierzalnymi** (miara przeliczalnie addytywna na zbiorach nieprzeliczalnych); "
            "pokazał m.in., że na ω₁ nie ma nietrywialnej σ-addytywnej miary znikającej na punktach "
            "(macierze Ulama). Później pracował w USA (Monte Carlo, Projekt Manhattan).",
        ),
        (
            "Stanisław Saks (1897–1942)",
            "Związany głównie z Warszawą, współpracował ze Lwowem (twierdzenie Banacha–Saksa, 1930). "
            "Jego monografia *Théorie de l'intégrale* (1933; wyd. ang. *Theory of the Integral*, 1937) "
            "stała się klasycznym podręcznikiem teorii miary i całki.",
        ),
        (
            "Juliusz Schauder (1899–1943) i Stanisław Mazur (1905–1981)",
            "Schauder: baza Schaudera, twierdzenie o punkcie stałym (1930), metoda Leraya–Schaudera dla "
            "równań różniczkowych. Mazur: twierdzenie Mazura–Ulama (1932), algebry Banacha, gra Banacha–Mazura "
            "i problem bazy (rozwiązany negatywnie przez Enfla w 1972 r.). Ich główny wkład to analiza "
            "funkcjonalna, a nie sama teoria miary.",
        ),
    ]
    kolumny_osob = st.columns(2)
    for i, (osoba, opis) in enumerate(osoby):
        with kolumny_osob[i % 2]:
            with st.container(border=True):
                st.markdown(f"**{osoba}**")
                st.markdown(opis)