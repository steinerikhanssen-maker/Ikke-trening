# Forsknings- og teknologikilder – kontrollert 13.10.2026

## Faglig vurdering

**Gamification er verdt å prøve, men er ikke en dokumentert løsning for nettopp disse brukerne.** Nishi mfl. sin systematiske gjennomgang og metaanalyse av 36 randomiserte studier, 10 079 deltakere, fant cirka **489 ekstra skritt/dag** (95 % KI 64–914) sammenlignet med tilsvarende ikke-spillifiserte apper. Forskerne betegnet dette som en *triviell* økning i skritt relativt til sitt forhåndsvalgte terskelnivå. Studien ble publisert i 2024; PubMed-registreringen kan fremstå oppdatert i 2025. Ikke framstill denne effekten som stor eller spesifikk for maskot.

- https://pubmed.ncbi.nlm.nih.gov/39764571/
- https://pmc.ncbi.nlm.nih.gov/articles/PMC11701442/

BE ACTIVE var en randomisert studie med 1 062 voksne med høy kardiovaskulær risiko. Gamification med og uten økonomiske insentiver kunne øke antall skritt. Resultatene gir grunnlag for å undersøke spillmekanismer, **ikke** å overføre effekten direkte til vår app eller å love helserisikoreduksjon.

- https://pubmed.ncbi.nlm.nih.gov/38583084/

JMIR Serious Games 2026 kartla 53 RCT-er og 48 ulike gamification-elementer. Kartlegging er ikke et bevis på at NIM, kapitler eller samarbeid hver for seg fungerer.

- https://games.jmir.org/2026/1/e85804/

Motivasjon/atferd:

- COM-B: https://pmc.ncbi.nlm.nih.gov/articles/PMC3096582/
- NICE PH49 om individuell atferdsendring: https://www.nice.org.uk/guidance/ph49/chapter/recommendations
- Affective–Reflective Theory: https://link.springer.com/article/10.1007/s12662-017-0477-9
- Motiverende samtale, fysisk aktivitet, BMJ 2024: https://www.bmj.com/content/386/bmj-2023-078713
- Norske anbefalinger for fysisk aktivitet: https://www.helsedirektoratet.no/faglige-rad/fysisk-aktivitet-i-forebygging-og-behandling/voksne-og-eldre

## Integrert aktivitetsprinsipp: korte bevegelsesøkter knyttet til rutiner

- **Kort trening kan hjelpe, men er ikke det samme som et komplett program.** BJSM/PubMed, 11 RCT-er / 414 deltakere, betydelig heterogenitet og lav/svært lav sikkerhet for flere mål: https://pubmed.ncbi.nlm.nih.gov/41057224/
- **Fysisk funksjon i 2026:** 11 RCT-er / 472 personer; forbedring i sit-to-stand og enkelte kondisjonsmål: https://www.sciencedirect.com/science/article/pii/S1279770726000680
- **Alder og usikkerhet:** 21 RCT-er / 921 personer; i undergrupper med gjennomsnittsalder >50 år var VO₂maks-effekten ikke signifikant: https://pubmed.ncbi.nlm.nih.gov/42571752/
- **90 eldre, 12 ukers studie av styrke- og tai chi-snacking:** https://link.springer.com/article/10.14283/jfa.2024.32
- **Ankervaner og faste kontekstsignaler:** metaanalyse av 14 studier / 6 069 personer; rutine/tidspunkt var assosiert med fysisk aktivitet, men korrelasjoner er ikke kausal dokumentasjon for vårt produkt: https://pmc.ncbi.nlm.nih.gov/articles/PMC13467471/
- **NHS, trygg stol-til-stå og andre generelle hjemmeøvelser:** https://www.nhs.uk/live-well/exercise/strength-exercises/
- **NHS fallforebygging, trygg dusj/bad:** https://www.nhs.uk/conditions/falls/
- **Ikke lov fullverdig styrkeeffekt fra tre små øvelser:** Helsedirektoratet, all aktivitet teller, men anbefalinger om store muskelgrupper og progresjon gjelder fortsatt: https://www.helsedirektoratet.no/faglige-rad/fysisk-aktivitet-i-forebygging-og-behandling/voksne-og-eldre

## WordPress: primære tekniske kilder

- Hvilket ansvar tema vs plugin har: https://developer.wordpress.org/themes/getting-started/what-is-a-theme/
- Plugin-utvikling: https://developer.wordpress.org/plugins/intro/
- Appmal for utvalgt side: https://developer.wordpress.org/reference/hooks/template_include/
- Blokkregistrering via metadata: https://developer.wordpress.org/reference/functions/register_block_type/
- Shortcode API: https://developer.wordpress.org/apis/shortcode/
- REST-ruter og tilgangskontroll: https://developer.wordpress.org/rest-api/extending-the-rest-api/adding-custom-endpoints/
- Cookie-autentisering og REST nonce: https://developer.wordpress.org/rest-api/using-the-rest-api/authentication/
- Nonce erstatter ikke tilgangskontroll: https://developer.wordpress.org/apis/security/nonces/
- Validering: https://developer.wordpress.org/apis/security/data-validation/
- Sanitizing: https://developer.wordpress.org/apis/security/sanitizing/
- Escaping: https://developer.wordpress.org/apis/security/escaping/
- Opprette og oppgradere datatabeller: https://developer.wordpress.org/plugins/creating-tables-with-plugins/
- WP privacy hooks: https://developer.wordpress.org/plugins/privacy/privacy-related-options-hooks-and-capabilities/
- WordPress privacy erasure: https://developer.wordpress.org/plugins/privacy/adding-the-personal-data-eraser-to-your-plugin/
- WordPress anbefalte serverkrav: https://wordpress.org/about/requirements/

## Metode og forbehold

- Den eksisterende 4.1-demoen er inspisert programmatisk, og de medfølgende to Playwright-testene er kjørt igjen med OK. De tester utvalgte frontendflyter, **ikke** WordPress, langsiktig bruk eller reell helseeffekt.
- Forumfunn og tidligere samtaler er kvalitativ innsikt, ikke representative prevalenstall. Intervjuer med ekte personer og videre testing kreves for å dokumentere preferanser og endret aktivitet.
- Norsk personvernlov og GDPR må vurderes for en virkelig tjeneste; denne spesifikasjonen er ikke en juridisk godkjenning. Ingen sensitive helsedata skal samles unødvendig.