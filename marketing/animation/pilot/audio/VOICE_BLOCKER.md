# Castingstatus

Den første leveransen manglet dialog. Dette er løst med sju lokalt genererte, lisensierte Kokoro-opptak i tre ulike stemmer, brukt i ferdig film og karakterprøver. Ingen betalt API eller eSpeak-stemme er brukt. Originalrapporten er bevart i `../qa/history/M1_initial_casting.txt`.

Valg og naturlige opptaksvarigheter er dokumentert i `voice/auditions.json`. `speed=1.0` for alle replikker; klippeplanen er retimet etter lyden. Se `README.md` for stems og lisenser.

Uavhengig menneskelig godkjenning av profesjonelt stemmespill og fonemsynk er **NOT TESTED**. Dette blir ikke fremstilt som utført mobil-/seer-QA.

Valgfri ny syntese: isolert Python-venv med `requirements-voice.lock.txt`; modellene fra `https://github.com/thewh1teagle/kokoro-onnx/releases/tag/model-files-v1.1`, SHA-256 mot manifestet, så `python audio/generate_auditions.py /sti/til/modellmappe`. Film/prosjekt kan brukes uten denne installasjonen; alle WAV-er er vedlagt.
