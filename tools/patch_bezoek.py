"""Patch: bezoek aan de showroom als grote CTA (in plaats van alleen proefvaart).
Toepassen als laatste (na patch_mobile.py)."""
import sys
p = sys.argv[1]
s = open(p, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: raise SystemExit('anchor %d != %d: %s' % (n, count, old[:90]))
    s = s.replace(old, new)
i = s.index('\nfunction pBezoek(id){'); j = s.index('\n', i + 5)
s = s[:i] + r"""
function pBezoek(id){var b=id&&boat(id);var wat=[['Rondkijken in de showroom','showroom'],['Een proefvaart maken','proefvaart'],['Kennismaken met Klop Premium Service™','service'],['Advies over inruil of financiering','advies']];
return'<section class="phead"><div class="wrap">'+lbl(b?'Proefvaart en bezoek':'Bezoek de showroom')+'<h1>'+(b?'Vaar de '+esc(b.naam)+'.':'Plan je bezoek aan de showroom.')+'</h1><p class="lead">'+(b?'Op het water, met een Vrijheidsvaarder erbij. Laat je gegevens achter en wij bellen je terug.':'Kom kijken, voelen en varen aan de Rivierdijk. Laat je gegevens achter en een Vrijheidsvaarder belt je terug om een moment af te spreken.')+'</p></div></section><section class="sec tight" style="padding-top:0"><div class="wrap two-col" style="align-items:start"><div class="formcard"><form id="bf"><div class="two"><div class="f"><label>Naam</label><input name="n" required></div><div class="f"><label>Telefoon</label><input name="t" type="tel" required></div></div><div class="f"><label>E-mail</label><input name="e" type="email" required></div><div class="f"><label>Wat wil je doen?</label><select name="w">'+wat.map(function(x){return'<option'+((b?x[1]==='proefvaart':x[1]==='showroom')?' selected':'')+'>'+x[0]+'</option>'}).join('')+'</select></div><div class="f"><label>Welke boot?</label><input name="b" value="'+(b?esc(b.naam):'')+'" placeholder="Of: ik weet het nog niet"></div><div class="f"><label>Voorkeursdag</label><select name="d"><option>Zo snel mogelijk</option><option>Doordeweeks</option><option>Zaterdag</option></select></div><div class="f"><label>Opmerking</label><textarea name="o" rows="3"></textarea></div><button class="btn solid" type="submit">'+(b?'Plan mijn proefvaart':'Plan mijn bezoek')+'</button></form></div><div>'+ph(b?'g16':'g12','',b?'Een boot op het water bij zonsopgang':'De showroom met boten achter glas aan het water')+'<p class="mut" style="margin-top:22px">'+CONTACT.adres+', '+CONTACT.plaats+'. Liever direct? Bel '+CONTACT.tel+' of app ons op '+CONTACT.wa+'.</p></div></div></section>'}""" + s[j:]
rep('<a class="sa" href="#/bezoek">Plan proefvaart</a>', '<a class="sa" href="#/bezoek">Plan bezoek</a>')
# showroompagina: grote CTA is het bezoek
rep("btn('Plan een bezoek of proefvaart','#/bezoek','solid')", "btn('Plan je bezoek','#/bezoek','solid')")
# hoofd-CTA in de kop en in de mobiele balk: altijd een bezoek aan de showroom
rep('<a class="btn cta" href="#/stel-samen">Configureer boot</a>', '<a class="btn cta" href="#/bezoek">Bezoek showroom</a>', 2)
rep('<a class="go" href="#/stel-samen"><span>Configureer boot</span></a>', '<a class="go" href="#/bezoek"><span>Bezoek showroom</span></a>')
open(p, 'w', encoding='utf-8').write(s)
print('ok: bezoek')
