# GymNotFound – animasjonspilot «The Ugly Tree» – produksjonsoppdrag

**Dato:** 2026-10-14. **Egen oppgave, helt isolert fra WordPress-pluginkoden i [issue #1](../../issues/1).**

## Beslutning og mål
Vi har produsert flere 12-sekunders prototyper, men kvaliteten ble for lav: Ken Burns/pan/zoom, harde lagkanter, dårlig tre-munn, stivt kroppsspråk og billige robotstemmer. **Ikke gjenta denne metoden.** Nå skal vi produsere én reell 2D/2.5D karakteranimert TikTok-pilot med høy visuell kvalitet og komisk timing. Første episode **«The Ugly Tree»**. Ingen ti-episoders sesong før piloten passerer kvalitetssjekk.

Format: **1080 × 1920, 9:16, 30 fps, 360 frames, 12 sekunder, engelsk lyd, H.264/AAC**. Ingen betalte tjenester eller API-er uten ny godkjenning.

## Kildepakke (viktig)

Det er laget en separat nedlastbar pakke **GymNotFound_Codex_Profesjonell_Animasjon.zip** i ChatGPT-samtalen. Den skal knyttes til Codex-jobben som vedlegg eller pakkes ut i Codex-arbeidsområdet. ZIP-en ligger **ikke i GitHub-repositoriet**.

Etter utpakking: les `START_HER_CODEX.txt` og `INSTRUKSJON_FOR_BRUKER.txt` i pakkeroten og deretter:
- `brief/shot_plan.json` / `brief/shotlist_30fps.csv` – konkret regiplan.
- `brief/character_bible_no.md` – NIM, Alex, tre og visuell kontinuitet.
- `brief/animation_direction_no.md` – bevegelses- og komisk regi.
- `brief/release_gate_no.md` – kvalitetsport.
- `assets/nim_rig/svg/`, `assets/nim_rig/png/`, `rig_manifest.json` – lagdelt SVG/PNG NIM.
- `blender/create_project.py` – Blender STARTSKRIPT. Syntakssjekket og asset-kontrollert utenfor Blender; **ikke kjørt/testet i Blender**.
- `assets/reference/` er **bare** visuell referanse. Ikke bruk gamle storyboardpaneler som filmbilder.

Hvis ZIP-en ikke er tilgjengelig i Codex-miljøet, må den legges ved; ikke hev at filene allerede er importert. Den originale NIM-illustrasjonen er også dokumentert i `reference/IKKE_TRENING_4_1_standalone.html`.

## Arbeidspakker – utføres i rekkefølge

### M0 – Bekreft fungerende pipeline
1. Kjør `python verify_bundle.py` fra pakkens rot. Det validerer filer, rigg-lag og frame-plan, **ikke animasjonskvalitet**.
2. Finn Blender-versjon og kjør `blender -b --python blender/create_project.py` i faktisk Blender-miljø. Rett nødvendig bpy-/alpha-kompatibilitet mot installert Blender. Noter faktisk testet versjon.
3. Lag en åpningsbar `.blend` og render testbilder som viser at NIM-lagene har riktig geometri, pivot og alfa. Ingen falsk «pass» på Blender uten kjøring.

### M1 – Tre korte karakterprøver, ikke fullfilm
1. NIM 1–2 s: «Perfect» med original silhuett, armer, ansikt, blink og bevisst timing.
2. Alex 1–2 s: ekte kroppslig vekt når han legger vekk telefonen, reiser seg og tar et steg. Ingen skyv av stillfoto.
3. Tre 1–2 s: øyne, bryn og barkmunn oppstår som DEFORMASJON AV BARKEN, med replikk «I can hear you». Ingen pålimt svart sirkel eller hull.
Lever `previews/NIM_acting.mp4`, `Alex_walk.mp4`, `Tree_reveal.mp4`, før fullfilm. Gjennomgå visuelt og rett avvik først.

### M2 – Regissér pilotens sju shots
Bruk `shot_plan.json`. Storyen er:
- Alex: «I hate exercise.»
- NIM: «Perfect. Find the ugliest tree.»
- Alex går ut, peker: «Found it.»
- Treet, etter pause: «I can hear you.»
- NIM: «You went outside. Gotcha.»
- Kort GymNotFound-merke og «Exercise by accident.»

Gjør dette som EN liten komedie, ikke forklarende lysbilder. Hvis dialogen sprenger 12 sekunder, kort ned skriptet med bevart setup/payoff, ikke skru opp stemmehastighet unaturlig. Ikke lokk med appbutikk-knapper før appen er lansert.

### M3 – Stemmer, lyd og tekst
Tre tydelig forskjellige, forståelige stemmer. Lokale eSpeak-stemmer fra forrige utkast er PLACEHOLDERS og må ikke godkjennes som proff. Bruk opptak eller godkjent, lisensiert kvalitets-TTS uten nye abonnementer. Hvis dette ikke kan skaffes, rapportér blokkering og lever bildematerialet/redigerbar timeline uten å kalle finalen publiseringsklar.
Originale/lisensierte SFX. Undertekster på egne redigerbare lag, TikTok safe zones; ingen tekst integrert i scenebakgrunn.

### M4 – Sluttfilm og full leveranse
- `final/GymNotFound_S01E01_TikTok_FINAL.mp4` (12.00s, 1080x1920, 30fps, H.264 + AAC).
- `edit/GymNotFound_S01E01_FINAL.blend`, alle teksturer/rigg-lag/relativlenker.
- `assets/` med NIM, Alex, tre og separerte bakgrunner, redigerbar kilde.
- `audio/` stems + miks, `subtitles.srt`, forsidebilde og minst tre korte proof-klipp.
- `qa/TESTRAPPORT.txt` med reelle PASS / FAIL / NOT TESTED.
- GitHub PR med kildeprosjekt. Ingen merge/publisering automatisk.

## Ikke godta («release gate»)
- Ken Burns/stillfoto-pan som «karakteranimasjon», limte kanter, unaturlig tre-munn, manglende kroppslig vekt.
- Ny maskot som ikke følger NIM-figuren, uryddig tekst og altfor høy lyd.
- Bare teknisk MP4-integritet uten kreativ/visuell kontroll og avspilling på mobil.
- Kommersielle lyder/musikk uten dokumentert rettighet.
- «Publiseringsklar» uten faktisk rigget karakteranimasjon og forståelig dialog.

## Arbeidsregler
Jobb på egen `marketing/pilot-animation`-gren, isolert fra appens WordPress-oppgave. Bruk gratis Blender Grease Pencil/rigging; eventuelt gratis DaVinci Resolve til etterarbeid eller Blender VSE/FFmpeg. Ikke la API- eller appbetaling aktiveres, og ikke start masseproduksjon.

Eksterne referanser (sjekket oktober 2026):
- Blender Grease Pencil: https://docs.blender.org/manual/en/5.0/grease_pencil/
- Blender command line: https://docs.blender.org/manual/en/5.0/advanced/command_line/ 
- DaVinci Resolve 21: https://www.blackmagicdesign.com/support
