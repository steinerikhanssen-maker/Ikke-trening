# GymNotFound – The Ugly Tree

Én ferdig klippet 12-sekunders pilot med ekte Blender-karakterrigger, tre ulike engelske stemmer, lydmiks og undertekster. **Publisering er ikke utført.** Fysisk mobiltest, fem uavhengige seere og ekstern vurdering av stemmespill/leppesynk er ikke gjennomført; se den eksplisitte kvalitetsrapporten.

| Leveranse | Fil |
|---|---|
| H.264/AAC-film, 1080×1920, 30 fps, 12.00 s | `final/GymNotFound_S01E01_TikTok_FINAL.mp4` |
| Redigerbart prosjekt med sju shots og full tidslinje | `edit/GymNotFound_S01E01_FINAL.blend` |
| Tre native karakterprøver, to sekunder hver | `previews/NIM_acting.mp4`, `Alex_walk.mp4`, `Tree_reveal.mp4` |
| Forside | `final/GymNotFound_S01E01_COVER.png` |
| Dialog, effekter og miks | `audio/` |
| Engelske undertekster | `subtitles.srt` |
| Faktiske kontroller og kjente begrensninger | `qa/TESTRAPPORT.txt` |
| Komplett ZIP med kilde, film, lyd og QA | `dist/GymNotFound_S01E01_COMPLETE.zip` |

Åpne [review.html](review.html) lokalt for film og prøver. Historiske M1-rapporter ligger i `qa/history/`. De beskriver den første arbeidsleveransen, ikke den oppdaterte eksporten.

## Rediger prosjektet

Åpne `.blend` og velg scenen **GYMNOTFOUND_S01E01_EDIT**. Blender Video Sequencer har sju scene-klipp. Hvert shot inneholder separate karakter-, bakgrunns- og tekstobjekter. Kameraene står stille; rigger, kroppsdeler, uttrykk og barkmesh animeres.

NIMs originale fullkanvas PNG/SVG-kunst og pivoter er bevart. Figuren har beinrigg med armgest, bevisst blink, munnformer og antennebevegelse. Alex er samme voksne figur i fire shots, med vektede kroppsdeler, hånd-/telefonkontakt og føtter som står fast gjennom oppreisningen. Treet har ett sammenhengende barkmesh med animerte knuter, bryn og kjeve; munnen er en deformasjon og fargefure i barken.

Tidslinjens kanal 4 spiller den normaliserte miksen. Kanal 2 har de sju individuelle dialogstemmene og kanal 3 effektstemmen; disse er mutet for å unngå dobbel lyd. Mut kanal 4 og aktiver kanal 2/3 for egen miks. Individuelle originale SFX og alle dialog-WAV-er følger også med. Alle brukte bilder, fonter og lydstems er pakket og har relative referanser. Ingen TTS-modell eller betalt tjeneste trengs for å åpne prosjektet.

Dialogen beholder naturlig hastighet. Shot-planen er retimet rundt faktiske opptak; `edit/edit_timing.json` er gjeldende klippeplan, mens `brief/shot_plan.json` er originalbestillingen. Blender-tekstobjekter og `.srt` er redigerbare; teksten er ikke bakt inn i scenekunsten.

## Bygg på nytt

Faktisk kjørt: Blender **4.3.2**, FFmpeg **7.1.5**, vanlig Python. Fra repoets rot:

```bash
bash marketing/animation/pilot/blender/render_pilot.sh
```

Skriptet bygger kilder og tidslinje, lager lydmiks, renderer de tre prøvene og alle 360 native filmbilder, encoder MP4, verifiserer og pakker leveransen. Rendering bruker Cycles CPU som standard. EEVEE er også prøvd med en lokal virtuell X-skjerm, men er ikke en nødvendig avhengighet. Blender 4.5/5.x er ikke testet.

Primær kunst-/riggkilde er `blender/create_full_pilot.py` og `blender/lib/drawing.py`. `build_proofs.py`, `refine_characters.py`, `blender/check_contacts.py` og det opprinnelige `create_project.py` er tidligere arbeids-/startskript; de er ikke sluttfilmens kilde. Gjeldende kontakter og prosjektkontroller bruker skriptene i `qa/`. Rå bilder, verbose logger og Blender-backup er utelatt fra Git/ZIP. Sammendragslogger og kontrollsummer er vedlagt.

For å pakke de eksisterende sluttfilene uten ny rendering:

```bash
python3 marketing/animation/pilot/qa/package_handoff.py
```

Valgfri browser-QA bruker Node, `@playwright/test` 1.56.1 og system-Chromium 154. Start HTTP-server i én terminal:

```bash
python3 -m http.server 8090 --bind 127.0.0.1 --directory marketing/animation/pilot
```

I en annen terminal:

```bash
npm install --prefix /tmp/gnf-animation-browser --ignore-scripts --no-audit --no-fund @playwright/test@1.56.1
NODE_PATH=/tmp/gnf-animation-browser/node_modules node marketing/animation/pilot/qa/browser_playback.cjs
```

`GNF_CHROMIUM_PATH` kan peke på en annen lokal Chromium. Testen viser faktisk avspilling og dekoding; den erstatter ikke fysisk telefon eller menneskelig lytting.

## Kilder og kostnader

Den opprinnelige 69-filspakken er verifisert med SHA-256 `cdf2332a59d40e7ade8d5db839dba1f1d544ae3685449dd9f0cb5b0873283a6e`. Storyboardbilder brukes kun som referanse og aldri som filmbilder. Alex, tre og miljøer er egne redigerbare vector-/mesh-kilder. NIM følger originalen. Open Sans-lisens og MIT/Apache-lisenser for den lokale Kokoro-stemmekilden er vedlagt. SFX er egen signal-/støy-syntese uten eksterne opptak eller kommersiell musikk.

Ingen betalt API, abonnement, WordPress-endring, produksjonsinstallasjon, automatisk merge eller TikTok-publisering er utført.
