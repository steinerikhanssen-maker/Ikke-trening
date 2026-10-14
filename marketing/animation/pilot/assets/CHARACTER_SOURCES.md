# Redigerbare kunstkilder

NIM: originale fullkanvas PNG/SVG-filer i `nim_rig/`, pivoter i `rig_manifest.json`. `layer_bounds.json` begrenser kun tom meshflate i renderer; det beskjærer ikke filer eller flytter kildekoordinater. Beinrigg og uttrykk ligger i `../edit/NIM_PROOF.blend`.

Alex: egen konseptkunst som mesh- og kurvelag i `../edit/Alex_PROOF.blend`. `ALEX_BODY_ARMATURE` har rot, overkropp, hode, over-/underarmer, lår, legger og føtter. Navngitte klær, hender, ansikt og telefon kan redigeres uavhengig. Kunstgrunnlaget bygges av Alex-delen i `../blender/build_proofs.py`. Dette er en enkel arbeidsfigur, ikke godkjent profesjonell sluttkunst.

Tree: egen konseptkunst i `../edit/Tree_PROOF.blend`. `TREE_CONTINUOUS_BARK_SKIN` er én sammenhengende overflate med `Bark_folds_reveal` og `Bark_jaw_speech`. Munnens farge ligger i barkmeshens materialer; det finnes ikke en separat munnflate. Øyeinteriørene ligger bak barken til knutene åpnes. Videre kunstnerisk arbeid på bark/mimikk er nødvendig.

Bakgrunner: navngitte mesh-/kurveobjekter i de respektive prosjektfilene: stuevegg, gulv, sofa, skyggelag, parkhimmel, parkbakke og trekroner. Dette er separate redigerbare objekter, ikke et flatt storyboardbilde. Ingen av `assets/reference/*` er brukt som sluttbilder.

Alle karakterer/miljøer kan bygges fra den vedlagte Python-kilden i faktisk Blender. NIM-bilder og brukte voice WAV-stems er pakket i prosjektfilene og har relative referanser. Profesjonelt illustrerte Alex-/trelag følger ikke med originalpakken; de vedlagte egenbygde konseptlagene må fortsatt utvikles.
