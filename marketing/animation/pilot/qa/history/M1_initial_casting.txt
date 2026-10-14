# Casting og stemmegodkjenning gjenstår

Originalpakken inneholder manus, men ingen stemmeopptak. Denne arbeidsleveransen har nå **sju lokale stemmeauditions** i tre ulike Kokoro-stemmer. Ingen betalt tjeneste, abonnement eller stemmekloning er brukt. NIM- og treprøven bruker henholdsvis «Perfect» og «I can hear you» fra disse auditions. Alex-prøven viser kroppsspill og er uten dialog.

| Rolle | Kandidat | Status |
|---|---|---|
| Alex | am_michael | Teknisk generert og kontrollert; skuespill/forståelighet NOT TESTED |
| NIM | af_heart | Teknisk generert og kontrollert; skuespill/forståelighet NOT TESTED |
| Tree | bm_george | Teknisk generert og kontrollert; gravitas/karakterspill NOT TESTED |

Modellkilden [kokoro-onnx](https://github.com/thewh1teagle/kokoro-onnx) oppgir MIT for programvaren og Apache-2.0 for Kokoro-modellen. Lisensene er vedlagt i `licenses/`. Release `model-files-v1.1`, eksakte modellkontrollsummer og filproveniens står i `voice/auditions.json`. ONNX-modellene er ikke lagt inn i Git. Phonemisering benytter eSpeak NG via biblioteket; **lyden syntetiseres av Kokoro-nevralmodellen**, ikke av eSpeak-stemmer.

De vedlagte WAV-filene er 24 kHz / 24-bit PCM, modellens opprinnelige rate. AAC i NIM-/treprøvene er resamplet til 48 kHz. Alle replikker er generert med `speed=1.0`. Naturlige replikkvarigheter avviker fra regiplanens edit-mål; planen må retimes før fullfilm. Det er ikke laget en ferdig 12-sekunders stemmemiks.

Dette er kandidater, ikke profesjonelt godkjent casting. Stemmespill, forståelighet og leppesynk må vurderes med faktisk lytting før M3 kan bestås. Treets kjevedeformasjon følger det faktiske lydsignalets energi. NIMs munnformer er nøkkelsatt til «Perfect» med energistyrt lukking. Dette beviser ikke presis fonem- eller skuespillersynk.

En alternativ gratis løsning er egne opptak av tre samtykkende voksne utøvere etter [castingbeskrivelsen](../brief/script_voice_en.txt). WAV, helst 48 kHz / 24-bit, uten musikk/romklang og med dokumenterte markedsføringsrettigheter. Ikke akselerer stemmen for å få den til å passe i 12 sekunder.

## Reproduser auditions, valgfritt

De vedlagte opptakene er nok til å bygge proof-prosjektene uten TTS-installasjon. For ny generering, bruk en isolert Python 3.12-venv og `requirements-voice.lock.txt`. Last ned `kokoro-v1.0.int8.onnx` og `voices-v1.0.bin` fra [modellreleasen](https://github.com/thewh1teagle/kokoro-onnx/releases/tag/model-files-v1.1); kontroller SHA-256 mot manifestet. Kjør:

```bash
python audio/generate_auditions.py /sti/til/modellmappe
```

Ingen nettverkstjeneste kalles under selve syntesen. Godkjente stemmer, lydstyrte uttrykk og en dokumentert miks kommer etter at den visuelle M1-porten er bestått.
