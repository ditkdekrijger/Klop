"""Zet de u-vorm om naar de je-vorm in teksten (alleen tekst tussen tags en in JSON-strings).
Gebruik: python3 tools/je_vorm.py BESTAND [...]   (toont per bestand het aantal wijzigingen)"""
import re, sys
RULES = [
    (r'\bControleert u\b', 'Controleer je'), (r'\bWilt u\b', 'Wil je'), (r'\bmeldt u zich\b', 'meld je je'),
    (r'\bgebruikt u\b', 'gebruik je'), (r'\bKunt u\b', 'Kun je'), (r'\bHeeft u\b', 'Heb je'), (r'\bbent u\b', 'ben je'),
    (r'\bWij regelen het gedoe, u vaart\b', 'Wij regelen het gedoe, jij vaart'),
    (r'\bU vaart\b', 'Jij vaart'), (r'\bu vaart\b', 'jij vaart'),
    (r'\bwaarvoor u kocht: uw\b', 'waarvoor je hem kocht: je'),
    (r'\bUw\b', 'Je'), (r'\buw\b', 'je'), (r'\bUzelf\b', 'Jezelf'), (r'\buzelf\b', 'jezelf'),
    (r'\bU\b(?=\s+[a-z])', 'Je'), (r'(?<=[\s>(“"\'])u\b(?=[\s,.!?:;)”"\'<])', 'je'),
]
def conv(t):
    n = 0
    for a, b in RULES:
        t, k = re.subn(a, b, t); n += k
    return t, n
def fix(path):
    s = open(path, encoding='utf-8').read(); total = 0
    if path.endswith('.json'):
        def f(m):
            nonlocal total; t, k = conv(m.group(0)); total += k; return t
        s2 = re.sub(r'"(?:[^"\\]|\\.)*"', f, s)
    else:
        # alleen tekst tussen tags; script en style overslaan
        parts = re.split(r'(<script\b.*?</script>|<style\b.*?</style>|<[^>]+>)', s, flags=re.S)
        for i in range(0, len(parts), 2):
            parts[i], k = conv(parts[i]); total += k
        s2 = ''.join(parts)
    if total: open(path, 'w', encoding='utf-8').write(s2)
    return total
if __name__ == '__main__':
    for p in sys.argv[1:]:
        n = fix(p)
        if n: print(n, p)
