"""Entfernt fremde Verweise aus dem Quelltext (laeuft im Bau, nicht im Betrieb)."""
import sys

fehler = []

# 1. Analysedienst: Zeilenblock von <Script bis zum schliessenden />
p = "apps/web/src/app/layout.tsx"
s = open(p, encoding="utf8").read()
if "cdn.databuddy.cc" in s:
    zeilen = s.splitlines(keepends=True)
    start = ende = None
    for i, z in enumerate(zeilen):
        if "cdn.databuddy.cc" in z:
            j = i
            while j > 0 and "<Script" not in zeilen[j]:
                j -= 1
            start = j
            k = i
            while k < len(zeilen) - 1 and "/>" not in zeilen[k]:
                k += 1
            ende = k
            break
    if start is None:
        fehler.append("Analysedienst: Block nicht gefunden")
    else:
        del zeilen[start:ende + 1]
        rest = "".join(zeilen)
        if "databuddy" in rest:
            fehler.append("Analysedienst blieb stehen")
        else:
            open(p, "w", encoding="utf8").write(rest)
            print("entfernt: Analysedienst cdn.databuddy.cc")
else:
    print("Hinweis: Analysedienst stand nicht mehr im Quelltext")

# 2. Laufzeitabfrage bei Google (Schriftauswahl im Editor)
g = "apps/web/src/fonts/google-fonts.ts"
t = open(g, encoding="utf8").read()
alte_zeile = 'const GOOGLE_FONTS_CSS = "https://fonts.googleapis.com/css2";'
if "fonts.googleapis.com" in t:
    if alte_zeile not in t:
        fehler.append("Google-Schriften: Zeile nicht gefunden")
    else:
        t2 = t.replace(alte_zeile, 'const GOOGLE_FONTS_CSS = "about:blank";')
        if "fonts.googleapis.com" in t2:
            fehler.append("Google-Schriften liessen sich nicht abschalten")
        else:
            open(g, "w", encoding="utf8").write(t2)
            print("abgeschaltet: fonts.googleapis.com")
else:
    print("Hinweis: Google-Schriften standen nicht mehr im Quelltext")

if fehler:
    print("FEHLER: " + "; ".join(fehler))
    sys.exit(1)
print("Bereinigung in Ordnung")
