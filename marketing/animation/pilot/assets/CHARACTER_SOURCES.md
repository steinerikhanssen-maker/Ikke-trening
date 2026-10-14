# Redigerbare kunstkilder

Primær kilde: `../blender/lib/drawing.py`, satt i scene av `../blender/create_full_pilot.py`.

NIM følger de opprinnelige fullkanvas PNG/SVG-filene i `nim_rig/`. `rig_manifest.json` gir pivoter; `layer_bounds.json` begrenser bare tom meshflate og beskjærer aldri kildefilene. Armatur, uttrykksvarianter, blink, munnformer og sekundærbevegelse er redigerbare i `../edit/NIM_PROOF.blend` og fullprosjektets shots. Armens overgang mot kroppen blandes med kroppens egen kildefarge når den går foran silhuetten.

Alex har én kanonisk figur i alle fire opptredener: voksen, mørk hettegenser, grå bukser, rufsete hår og trekvartansikt. Klær, skygger, hender/fingre, telefon, munn og øyne er separate vektede mesh-/kurvelag. Samme ansiktsgeometri kontrolleres i alle shots. Telefonkontakt og planted-fotkontakt er målt mot faktisk evaluert Blender-geometri, ikke bare mot ønskede posisjoner.

Treet har ett sammenhengende barkmesh med `Bark_Knots_Open`, `Offended_Bark_Brows` og `Bark_Jaw_Viseme`. Materialets furer sitter i samme UV/barkflate og følger deformasjonen. Øyeinteriør ligger bak barken fram til knutene åpnes. Ingen separat munnplate/hull eller svart sirkel brukes.

Miljøene består av egne redigerbare vegg-, gulv-, sofa-, lampe-, vindu-, park-, gjerde-, hus-, gren- og kronelag. Ingen storyboardpaneler eller stillfoto-pan brukes som filmbilder. Alle brukt bilder/fonter er pakket inn, men SVG-mastere og kildefonter er også vedlagt.
