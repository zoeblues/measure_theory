# Teoria miary — powtórka do kolokwium

Interaktywna aplikacja pomaga powtórzyć rodziny zbiorów, algebry, σ-algebry, topologie i zbiory borelowskie.

## Pobranie i uruchomienie

Wymagania: Git, Python 3.14+ i [`uv`](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/zoeblues/measure_theory.git
cd measure_theory
uv sync
uv run streamlit run app.py
```

Streamlit wyświetli adres aplikacji w terminalu (zwykle <http://localhost:8501>).

## Jak się uczyć

1. Na **Mapie i laboratorium** prześledź zależności między rodzinami zbiorów.
2. W laboratorium wybierz rodzinę podzbiorów i najpierw samodzielnie oceń, czy jest algebrą, σ-algebrą lub topologią. Potem porównaj odpowiedź z wynikiem i sprawdź wygenerowaną σ-algebrę.
3. Powtórz **definicje i wzory**, a następnie przejrzyj **daty historyczne**.
4. Na koniec odpowiedz z pamięci: czym różni się topologia od σ-algebry? Co oznacza σ(F)? Jak powstaje σ-algebra borelowska?