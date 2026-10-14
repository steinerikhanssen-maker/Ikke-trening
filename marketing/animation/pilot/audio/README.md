# Filmens lyd

`GymNotFound_S01E01_DIALOGUE.wav`, `GymNotFound_S01E01_SFX.wav` og `GymNotFound_S01E01_MIX.wav` er separate 12-sekunders 48 kHz / 24-bit PCM-stems og normalisert miks. `build_mix.py` gjør resampling, cue-plassering og totrinns loudness-normalisering uten taleakselerering. Måling av den ferdige AAC-filen står i `../qa/media-checks.json`.

`voice/` har de sju opprinnelige dialog-WAV-ene. Filnavnene beholder `_AUDITION` fra genereringen, men disse valgte stemmene brukes faktisk i filmen: Alex `am_michael`, NIM `af_heart`, Tree `bm_george`. Proveniens, eksakte modell-/filkontrollsummer og naturlige varigheter står i `voice/auditions.json`. Modellens opprinnelige rate er 24 kHz; miks/AAC er 48 kHz.

Kokoro-programvaren har MIT-lisens, modellen Apache-2.0. Lisensene er vedlagt. Phonemisering benytter eSpeak NG; selve lyden kommer fra nevralmodellen Kokoro. Ingen eSpeak-robotstemme, kjent stemmeklone, betalt tjeneste eller abonnement er brukt. Ekstern menneskelig vurdering av casting/forståelighet er fortsatt NOT TESTED.

`sfx/` har seks egne signal-/støysynteser med kilde, seed, peak og kontrollsummer. Ingen eksterne opptak, samplebiblioteker eller kommersiell musikk er brukt. Fotsteget er plassert ved landingen i dørklippet; øvrige cues står i `../qa/mix-measurements.json`.

Blender-spor: kanal 4 spiller miksen; kanal 2 er individuell dialog og kanal 3 er effektstemmen, mutet som standard. For ny miks, mut kanal 4 og aktiver kanal 2/3. Alle stems og relative referanser er pakket inn i fullprosjektet. Ingen modellinstallasjon trengs for redigering.
