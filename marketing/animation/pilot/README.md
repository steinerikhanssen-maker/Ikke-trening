# The Ugly Tree – karakterprøver for issue #4

**Arbeidsleveranse. Kvalitetsporten er ikke bestått. Ingen fullfilm eller publiseringsklar master er levert.**

Denne grenen er isolert fra WordPress-pluginen. Den inneholder tre redigerbare Blender-prosjekter, tre bevegelsesprøver og sju lokale stemmeauditions og faktiske kontrollresultater. Kildene er rekonstruert fra de 14 delene på main med korrekt SHA-256. Originale storyboardbilder brukes aldri som filmbilder.

Åpne [review.html](review.html) lokalt for å spille av prøvene. MP4-ene i `previews/` er **540×960, 30 fps og to sekunder**. NIM og treet har AAC-lyd med stemmeauditions; Alex er en stum bevegelsesprøve; dette er prøveformat, ikke formatet til den bestilte 1080×1920-sluttfilmen. Prosjektene er konfigurert til 1080×1920 og har alle NIM-teksturer og brukte stemmestems pakket inn.

| Prøve | Redigerbart prosjekt | Innhold og begrensning |
|---|---|---|
| NIM_acting.mp4 | edit/NIM_PROOF.blend | Ekte flerlags beinrigg, armgest, uttrykksbytte, bevisst blink og antenneetterklang. Lokal «Perfect»-audition; endelig leppesynk ikke godkjent. |
| Alex_walk.mp4 | edit/Alex_PROOF.blend | Originale mesh-/kurvelag bundet til kropp, armer og ben. Sittende posering, oppreisning og steg. Enkel konseptkunst, kontakt/telefon krever videre arbeid. |
| Tree_reveal.mp4 | edit/Tree_PROOF.blend | Sammenhengende barkmesh med shape keys for knuter/bryn og talebevegelse. Ingen separat munnflate. Lokal «I can hear you»-audition. Materiale/uttrykk krever kunstnerisk viderearbeid. |

Den opprinnelige NIM-kunsten er bevart som fullkanvas SVG og PNG under `assets/nim_rig/`. Alex, treet og miljøene er redigerbar, proseduralt tegnet kunst i `blender/build_proofs.py` og de lagrede `.blend`-filene. Dette er ikke godkjent erstatning for konseptreferansens profesjonelle tegnestil.

## M1-revisjon 14. oktober, videreført på eksisterende gren

`blender/refine_characters.py` videreutvikler de eksisterende Alex-/treriggene.
NIM-prosjektet, videoen og kildekunsten er uendret. Alex beholder nå telefonen
under oppreisning/steg; avlegging på puten er utsatt, ikke løst. Eget håndledd,
fingergrep, kles-/ansiktsdetaljer og per-frame benløsning er lagt til. Treet har
kontinuerlig prosedural bark, større øyne, asymmetriske bryn og et vedvarende
reaksjonsuttrykk. Ingen bildegenerator eller innlimte storyboardbilder er brukt.

Gjeldende vurdering: `qa/REVISION_M1.txt`. Den opprinnelige TESTRAPPORT-teksten
nedenfor revisjonsmerknaden beholdes som historikk. M1 er fortsatt FAIL.

Kontaktmåling etter bygging:

```bash
blender -b marketing/animation/pilot/edit/Alex_PROOF.blend --python marketing/animation/pilot/blender/check_contacts.py -- marketing/animation/pilot/qa/contact-checks.json
```

## Reproduser

Faktisk kjørt versjon: **Blender 4.3.2**, Cycles CPU; **FFmpeg 7.1.5**. Python-standardbibliotek er nok. Ingen betalt API, abonnement, nytt GPU-miljø eller produksjonssystem brukes.

Fra repoets rot:

```bash
python3 marketing/animation/source-archive/rebuild_archive.py
python3 marketing/animation/pilot/verify_bundle.py
bash marketing/animation/pilot/blender/render_proofs.sh
```

Skriptet bygger ekte rigger, renderer alle 60 bilder i hver prøve, pakker H.264 og åpner prosjektene igjen i faktisk Blender. Proof-rendering bruker 50 prosent av prosjektoppløsningen. Rå PNG-sekvenser, verbose rendererlogger og Blender-backup er utelatt fra Git; sammendragsloggene beholder alle 180 faktiske lagrede bilder. Git-tracked MP4/prosjektfiler trenger ingen ny rendering for gjennomgang.

Blender utenfor skymiljøet: åpne en `edit/*_PROOF.blend`, velg armaturen i Pose Mode og rediger nøkler/mesh/kurver. Tree har redigerbare shape keys på `TREE_CONTINUOUS_BARK_SKIN`. NIMs teksturer er pakket; SVG-masterne er også vedlagt. Tekst ligger som egne redigerbare tekstobjekter. Kameraet er statisk; figurene animeres.

EEVEE kunne ikke opprette en grafikkontekst i dette miljøet. Cycles fungerer. Den installerte Blender-byggen mangler OpenImageDenoise; den funksjonen er derfor slått av. Blender 4.5 LTS/5.x er ikke testet.

Valgfri browser-QA bruker Node og `@playwright/test` 1.56.1 med systemets Chromium 154.0.8037.57. Kjør HTTP-serveren fra repoets rot i én terminal, og QA i en annen:

```bash
python3 -m http.server 8090 --bind 127.0.0.1 --directory marketing/animation/pilot
```

```bash
npm install --prefix /tmp/gnf-animation-browser --ignore-scripts --no-audit --no-fund @playwright/test@1.56.1
NODE_PATH=/tmp/gnf-animation-browser/node_modules node marketing/animation/pilot/qa/browser_playback.cjs
```

`GNF_CHROMIUM_PATH` kan settes til en annen lokal Chromium-fil; standard er `/usr/bin/chromium`. Testen måler faktisk dekodet avspilling, ikke menneskelig lytting eller fysisk mobiltest.

## Kvalitetsport og videre arbeid

Les [qa/TESTRAPPORT.txt](qa/TESTRAPPORT.txt) og [audio/VOICE_BLOCKER.md](audio/VOICE_BLOCKER.md). Tekniske PASS er ikke kreativ godkjenning. M2 holdes igjen etter oppdragets regel om tre beståtte karakterprøver. De sju shottene, manus og undertekstreferansen er bevart i `brief/` for senere regiarbeid; de er **ikke** fremstilt som ferdig klippet timeline.

Nødvendige neste produksjonstrinn er bedre Alex-/trekunst og kontaktposering, godkjente naturlige stemmer, lydstyrte ansiktsnøkler, visuelt godkjente M1-prøver og deretter de sju shottene. Mobilavspilling med og uten lyd og forståelsestest på fem personer må gjennomføres før publisering. Ingen automatisk merge eller TikTok-publisering.
