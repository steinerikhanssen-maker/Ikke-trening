# Lydkilder for arbeidsleveransen

`voice/` har sju lokale, nevralgenererte castingauditions, tre ulike stemmer, ingen taleakselerering. Filproveniens, lisenskilde, kontrollsummer og varigheter står i `voice/auditions.json`. Disse er ikke godkjent profesjonell dialog. Se `VOICE_BLOCKER.md`.

`sfx/` har seks originale syntetiske effekter: UI-ping, fotsteg, dørlås, barkknirk, telefonvibrasjon og kort merkesignal. Ingen eksterne opptak, samplebiblioteker eller kommersiell musikk brukes. Signalene og tilfeldighetsfrøet kan redigeres i `generate_sfx.py`; opprinnelse, peak og kontrollsummer står i `sfx/manifest.json`. De er foreslåtte effektstems, ikke en godkjent sluttmiks.

Proof-videoene bruker kun den aktuelle castingreplikken, med 0,5 sekunders innledende stillhet. SFX og de øvrige replikkene er separate, ikke en ferdig 12-sekunders miks. Ingen musikk er lagt til. Bruk de faktiske WAV-opptakene når shots og undertekster senere retimes.
