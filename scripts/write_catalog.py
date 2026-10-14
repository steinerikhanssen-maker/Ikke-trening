"""Curated bilingual content. This script does not generate activity text at runtime."""
import json
from pathlib import Path
cards=[]
def add(id,band,family,energy,outdoors,en,nb,contexts=None,place=None,cost='free'):
 cards.append(dict(id=id,time=band,family=family,energy=energy,outdoors=outdoors,contexts=contexts or ['anywhere'],cost=cost,place_category=place,instructions=False,reviewed=False,en=dict(zip(['title','description','step','nim'],en)),nb=dict(zip(['title','description','step','nim'],nb))))
add('doorstep',2,'fresh_air','low',True,
 ['A little air, no expedition','Step into a familiar, safe outdoor space. You can stay close and return whenever you like.','Choose a comfortable spot near the door.','No summit required. The doorstep counts as outside.'],
 ['Litt luft, ingen ekspedisjon','Gå ut på et kjent og trygt sted. Du kan holde deg nær og gå inn igjen når du vil.','Velg et behagelig sted ved døren.','Ingen fjelltopp kreves. Dørstokken er også utendørs.'])
add('new_view',2,'discovery','low',False,
 ['Give your view a change','Find a different window or a different room and notice what looks new from there.','Choose one familiar place to move to.','The scenery department has a modest budget.'],
 ['Bytt utsikt litt','Finn et annet vindu eller et annet rom, og legg merke til det du ser derfra.','Velg et kjent sted å gå til.','Utsiktsavdelingen jobber med et beskjedent budsjett.'])
add('three_colours',2,'discovery','low',False,
 ['Find three colours','Look for three different colours as you move around a familiar room or safe nearby space.','Start with a colour you rarely notice.','Colour research. Extremely unofficial.'],
 ['Finn tre farger','Se etter tre ulike farger mens du beveger deg i et kjent rom eller et trygt nærområde.','Begynn med en farge du sjelden legger merke til.','Fargeforskning. Svært uoffisielt.'])
add('sound_round',2,'discovery','low',False,
 ['Follow the quiet sounds','Take a small round in a familiar indoor space and notice the sounds that belong to it.','Pick a room with a clear, safe floor.','The fridge may apply for a solo.'],
 ['Lytt på en liten runde','Ta en liten runde på et kjent sted inne og legg merke til lydene som finnes der.','Velg et rom med fri og trygg gulvplass.','Kjøleskapet kan finne på å søke om en solo.'])
add('return_item',2,'practical','low',False,
 ['One thing, back where it belongs','Carry one light, easy object back to its place. Leave heavy or awkward things alone.','Pick something simple and nearby.','A very small relocation project.'],
 ['Én ting tilbake på plass','Bær en lett og enkel ting tilbake der den hører hjemme. La tunge og upraktiske ting være.','Velg noe enkelt som ligger i nærheten.','Et svært lite flytteprosjekt.'])
add('clear_corner',2,'practical','low',False,
 ['Make one small corner useful','Clear a little space on a table or shelf. No cleaning campaign, ladders or heavy lifting.','Choose a corner you can reach comfortably.','We are declining the full renovation.'],
 ['Gjør ett lite hjørne nyttig','Rydd litt plass på et bord eller en hylle. Ingen storvask, stiger eller tunge løft.','Velg et hjørne du når på en behagelig måte.','Vi takker nei til totalrenoveringen.'])
add('plant_visit',2,'home','low',False,
 ['Pay a plant a visit','If you have a plant, go and see whether it needs a little care. Otherwise, choose a different idea.','Visit one plant in an easy-to-reach place.','Botanical customer service is open.'],
 ['Besøk en plante','Har du en plante, gå bort og se om den trenger litt stell. Ellers kan du velge en annen idé.','Velg en plante som står lett tilgjengelig.','Botanisk kundeservice er åpen.'])
add('water_break',2,'practical','low',False,
 ['Take your water break somewhere else','If it suits you, fetch some water and enjoy it in a different familiar spot.','Choose an easy route with nothing in the way.','The glass is not a sports accessory.'],
 ['Ta vannpausen et annet sted','Hvis det passer, hent litt vann og nyt det på et annet kjent sted.','Velg en enkel vei med fri passasje.','Glasset er ikke sportsutstyr.'])
add('coffee_cue',2,'routine','low',False,
 ['While the coffee settles','After putting the coffee on, choose a small household task away from hot equipment.','Put down what you are holding, then choose one easy task.','Coffee has been promoted to assistant.'],
 ['Mens kaffen blir klar','Etter at kaffen er satt på, velg et lite gjøremål på trygg avstand fra varmt utstyr.','Legg fra deg det du holder, og velg én enkel ting.','Kaffen er forfremmet til assistent.'])
add('teeth_cue',2,'routine','low',False,
 ['After the toothbrush is put away','Use the end of toothbrushing as a cue for a short, familiar indoor round. Choose an ordinary household task if that suits you.','Hands free, dry floor, and a clear little route.','The toothbrush can retire for the evening.'],
 ['Når tannbørsten er lagt bort','La avsluttet tannpuss være signalet for en liten, kjent runde inne. Velg et vanlig hjemmeærend hvis det passer deg.','Frie hender, tørt gulv og en liten vei uten hindringer.','Tannbørsten kan ta kvelden.'])
add('sofa_cue',2,'routine','low',False,
 ['A different stop after the sofa','When you next leave the sofa, visit a comfortable spot in another room before doing your next thing.','Pick the spot now; no need to keep the app open.','The sofa remains on good terms with us.'],
 ['Et annet stopp etter sofaen','Neste gang du går fra sofaen, besøk et behagelig sted i et annet rom før du gjør det neste.','Velg stedet nå. Appen trenger ikke være åpen.','Vi er fortsatt på god fot med sofaen.'])
add('sky_glance',2,'nature','low',True,
 ['Check the sky yourself','From a familiar, safe outdoor spot, notice the light and clouds. Skip it if conditions do not suit you.','Choose a spot close enough to return easily.','A forecast by looking up. Radical.'],
 ['Se på himmelen selv','Fra et kjent og trygt sted ute, legg merke til lys og skyer. Velg noe annet hvis forholdene ikke passer.','Velg et sted du enkelt kan gå tilbake fra.','Værmelding ved å se opp. Radikalt.'])
add('familiar_round',15,'fresh_air','some',True,
 ['A familiar round, with fresh eyes','Choose a safe route you already know. Notice one detail you usually pass without seeing.','Decide where you want to turn back.','Same route, slightly different attention.'],
 ['En kjent runde med nye øyne','Velg en trygg vei du allerede kjenner. Legg merke til en detalj du vanligvis går forbi.','Bestem hvor du vil snu.','Samme vei, litt annen oppmerksomhet.'])
add('street_detail',15,'discovery','some',True,
 ['Find a detail on a nearby street','On a familiar public street, look for a pattern, doorway or sign you have not noticed. Stay where walking is safe.','Choose a known stretch, not an unknown shortcut.','The street has not been informed of this inspection.'],
 ['Finn en detalj i en gate nær deg','I en kjent, offentlig gate, se etter et mønster, en dør eller et skilt du ikke har lagt merke til. Velg trygg ferdsel.','Velg en kjent strekning, ikke en ukjent snarvei.','Gaten er ikke varslet om inspeksjonen.'],['urban','suburban'])
add('rural_detail',15,'nature','some',True,
 ['Notice what changes near home','Take a small outing on a familiar, safe public route. Look at the light, season or landscape without entering private land.','Choose a known route that suits today.','No café has been invented for this outing.'],
 ['Se hva som endrer seg nær hjemmet','Ta en liten tur på en kjent og trygg offentlig vei. Se på lyset, årstiden eller landskapet uten å gå inn på privat grunn.','Velg en kjent vei som passer i dag.','Ingen kafé er oppfunnet for denne turen.'],['rural','suburban'])
add('small_project',15,'practical','some',False,
 ['A tiny project with a finish line','Choose one useful home task with a clear end. Sorting a light drawer or putting things away can be enough.','Name one task, and leave the rest for another day.','The rest of the house has not been commissioned.'],
 ['Et lite prosjekt med en slutt','Velg ett nyttig gjøremål hjemme med en tydelig slutt. En lett skuff eller noen ting på plass kan være nok.','Velg én oppgave, og la resten vente.','Resten av huset er ikke bestilt.'])
add('room_reset',15,'home','low',False,
 ['Change one comfortable room detail','Move around the room to put away small things or adjust something easy to reach. Leave furniture and heavy objects alone.','Choose one small change you would enjoy.','Interior design, without the invoice.'],
 ['Endre én liten detalj i rommet','Gå rundt i rommet og legg bort småting eller juster noe som er lett å nå. La møbler og tunge ting stå.','Velg en liten endring du vil ha glede av.','Interiørdesign uten fakturaen.'])
add('music_task',15,'playful','low',False,
 ['Bring a little music to a small task','If you like, play your own music while doing an easy household task. No sound starts automatically here.','Choose the task first, then music if you want it.','No compulsory soundtrack. We have manners.'],
 ['Litt musikk til en liten oppgave','Spill gjerne din egen musikk mens du gjør et enkelt gjøremål. Ingen lyd starter automatisk her.','Velg oppgaven først, og musikk hvis du vil.','Ingen obligatorisk filmmusikk. Vi har folkeskikk.'])
add('lunch_cue',15,'routine','some',True,
 ['Give lunch a small follow-up','After lunch, choose a familiar, safe outing that fits your time. You can also switch to an indoor idea.','Choose a place to turn back before putting the phone away.','Lunch has declined to become a training plan.'],
 ['En liten fortsettelse etter lunsj','Etter lunsj kan du velge en kjent og trygg tur som passer tiden din. Du kan også bytte til en idé inne.','Velg hvor du vil snu før du legger bort mobilen.','Lunsjen takker nei til å bli en treningsplan.'])
add('message_visit',15,'connection','low',False,
 ['Ask about a small shared outing','Contact someone you know and suggest a relaxed, familiar activity. Sending the invitation is a plan, not completed movement.','Ask what would suit you both. You can also do it alone.','No matching tracksuits are required.'],
 ['Spør om en liten tur sammen','Kontakt noen du kjenner og foreslå en rolig, kjent aktivitet. Å sende invitasjonen er en plan, ikke gjennomført bevegelse.','Spør hva som passer dere begge. Du kan også gjøre det alene.','Like treningsdresser kreves ikke.'])
add('park_visit',15,'place','some',True,
 ['Look around {place}','This park appears in the place data. Choose a familiar, public approach and skip any area requiring payment or permission.','Check the map and conditions before deciding. Access and opening hours are not verified.','A real place. A reassuring feature.'],
 ['Se deg rundt ved {place}','Denne parken finnes i stedsdataene. Velg en kjent og offentlig tilkomst, og hopp over områder som krever betaling eller tillatelse.','Sjekk kart og forhold før du bestemmer deg. Adgang og åpningstider er ikke bekreftet.','Et virkelig sted. En betryggende funksjon.'],place='park')
add('library_visit',15,'place','some',True,
 ['Explore near {place}','The data lists this library. A small visit to the surrounding public area can be an idea; check separately before planning to go inside.','Opening hours, access and fees are not verified. You do not need to enter.','Books can wait. The map cannot promise opening hours.'],
 ['Utforsk området ved {place}','Dataene viser dette biblioteket. Et lite besøk i det offentlige området rundt kan være en idé. Sjekk separat før du planlegger å gå inn.','Åpningstider, adgang og priser er ikke bekreftet. Du trenger ikke gå inn.','Bøkene kan vente. Kartet lover ingen åpningstid.'],place='library')
add('cafe_optional',15,'place','some',True,
 ['Consider a stop near {place}','This café is a real provider result. Only choose it if possible spending suits you; buying something is never required by the app.','Check access, prices and opening hours yourself.','Coffee has not been added to the compulsory budget.'],
 ['Vurder et stopp ved {place}','Denne kafeen er et faktisk treff fra datakilden. Velg den bare hvis mulig pengebruk passer. Appen krever aldri et kjøp.','Sjekk adgang, priser og åpningstider selv.','Kaffe er ikke lagt til et obligatorisk budsjett.'],place='cafe',cost='maybe')
add('museum_optional',15,'place','some',True,
 ['Consider {place}','The provider lists this museum. Admission may cost money and opening hours are unknown here. Check before you make plans.','Choose another idea if you want to avoid possible fees.','Culture, with a small dose of fact-checking.'],
 ['Vurder {place}','Leverandøren viser dette museet. Det kan være inngangspenger, og åpningstidene er ukjente her. Sjekk før du planlegger et besøk.','Velg en annen idé hvis du vil unngå mulige kostnader.','Kultur med en liten dose faktasjekk.'],place='museum',cost='maybe')
add('unhurried_outing',30,'fresh_air','some',True,
 ['Leave room for an unhurried outing','Set aside some time for a familiar, safe route. There is no distance target and no promise about how far you will get.','Choose a comfortable turning point and adjust freely.','The finish line has taken the day off.'],
 ['Gi plass til en rolig tur','Sett av litt tid til en kjent og trygg vei. Ingen avstandsmål og ingen løfter om hvor langt du kommer.','Velg et behagelig sted å snu, og endre planen når du vil.','Målstreken har tatt fri.'])
add('known_nature',30,'nature','some',True,
 ['Return to nature you already know','If you know a safe, public place outdoors, spend a little time there. This idea does not claim a trail or destination exists nearby.','Use your own familiar option, or choose a home idea.','The forest is optional, not a system requirement.'],
 ['Tilbake til natur du kjenner','Kjenner du et trygt og offentlig sted ute, bruk gjerne litt tid der. Denne ideen påstår ikke at en sti eller destinasjon finnes i nærheten.','Bruk et kjent alternativ, eller velg en idé hjemme.','Skogen er valgfri, ikke et systemkrav.'],['rural','suburban','anywhere'])
add('neighbourhood_edges',30,'discovery','some',True,
 ['See a familiar neighbourhood differently','Explore a known public part of your neighbourhood. A new detail is enough; there is no need to search for an attraction.','Choose safe paths and stay away from private areas.','Ordinary places have not been ruled out.'],
 ['Se et kjent nabolag litt annerledes','Utforsk en kjent og offentlig del av nabolaget. En ny detalj er nok. Du trenger ikke lete etter en attraksjon.','Velg trygge veier og hold deg unna private områder.','Hverdagslige steder er ikke diskvalifisert.'])
add('home_finish',30,'practical','some',False,
 ['Finish one manageable home task','Choose a modest task you can do safely without heavy lifting, a ladder or special equipment. Stop when it suits you.','Define a small finish before you begin.','A full renovation remains outside the scope.'],
 ['Fullfør ett overkommelig gjøremål','Velg en liten oppgave du kan gjøre trygt uten tunge løft, stige eller spesialutstyr. Stopp når det passer.','Bestem en liten slutt før du begynner.','Totalrenovering er fortsatt utenfor omfanget.'])
add('shared_round',30,'connection','some',True,
 ['Make room for a shared round','If someone you know wants to join, choose a familiar, relaxed outing. Different pace and shorter plans are fine.','Ask what fits today, with no obligation to say yes.','Good company has no pace requirement.'],
 ['Gi plass til en tur sammen','Vil noen du kjenner bli med, velg en kjent og rolig tur. Ulikt tempo og kortere planer er helt greit.','Spør hva som passer i dag, uten plikt til å si ja.','Godt selskap har ingen tempokrav.'])
add('light_errand',30,'practical','some',True,
 ['Turn an existing errand into an outing','If a nearby task already needs doing, consider a safe, comfortable way to include a little movement. No extra purchase is needed.','Use an errand you actually have, not one invented by the app.','The shopping list has not been expanded.'],
 ['La et eksisterende ærend bli en tur','Har du allerede et gjøremål i nærheten, vurder en trygg og behagelig måte å få litt bevegelse inn i det. Ingen ekstra kjøp trengs.','Bruk et ærend du faktisk har, ikke et appen finner på.','Handlelisten er ikke utvidet.'])
add('photo_details',30,'discovery','some',True,
 ['Collect details without collecting things','On a familiar, safe public route, notice textures, colours or shapes. A photograph is optional, never uploaded by this app.','Leave people, private spaces and objects undisturbed.','The collection can live entirely in your memory.'],
 ['Samle inntrykk uten å samle ting','På en kjent og trygg offentlig vei, legg merke til teksturer, farger eller former. Bilder er valgfritt og lastes aldri opp av appen.','La mennesker, private områder og ting være i fred.','Samlingen kan bo helt i hukommelsen.'])
add('indoor_sort',30,'home','low',False,
 ['Make a little space indoors','Choose a few light things to sort or put away, moving between easy-to-reach places. Take breaks whenever you want.','Keep the task small enough to enjoy finishing.','Tidiness is not being entered in a competition.'],
 ['Lag litt plass inne','Velg noen lette ting å sortere eller legge på plass mellom steder som er lette å nå. Ta pause når du vil.','Hold oppgaven liten nok til at det er godt å bli ferdig.','Ryddighet er ikke meldt på en konkurranse.'])
add('music_home',30,'playful','some',False,
 ['An easy home task, at your own rhythm','Use music you already enjoy, if you want, while doing a simple task in a clear space. No choreography or prescribed exercise.','Choose a safe task and your own pace.','No auditions. Especially not from the laundry.'],
 ['Et enkelt gjøremål i din egen rytme','Bruk gjerne musikk du liker mens du gjør en enkel oppgave med fri gulvplass. Ingen koreografi eller foreskrevet trening.','Velg en trygg oppgave og ditt eget tempo.','Ingen opptaksprøve. Særlig ikke fra klesvasken.'])
add('look_back_route',30,'nature','high',True,
 ['Rediscover a route you used to like','If an old, familiar public route still suits current conditions, revisit it. A shorter version is just as legitimate.','Check that the route remains safe for you today.','Your old route has no attendance register.'],
 ['Gjenoppdag en vei du likte før','Passer en gammel og kjent offentlig vei til forholdene nå, besøk den igjen. En kortere variant er like grei.','Sjekk at veien fortsatt er trygg og passer for deg i dag.','Den gamle veien har ingen oppmøteliste.'])
add('viewpoint_visit',30,'place','some',True,
 ['Consider the view at {place}','This viewpoint is listed by the provider. It is an option only if a familiar, public approach and current conditions suit you.','Check access and transport yourself. The allotted time is not a travel-time estimate.','A view, without an invented hiking route.'],
 ['Vurder utsikten ved {place}','Dette utsiktspunktet finnes hos leverandøren. Det er et alternativ bare hvis kjent, offentlig tilkomst og forholdene nå passer.','Sjekk adgang og transport selv. Avsatt tid er ikke et anslag på reisetid.','En utsikt uten en oppfunnet turrute.'],place='viewpoint')
add('park_slow',30,'place','some',True,
 ['Take your time near {place}','The data lists this park. Explore a suitable public part at your pace; skip any place requiring payment or permission.','Use the map to check your options. No route or opening hours are verified here.','The park is real. The timetable is yours.'],
 ['Ta deg tid ved {place}','Dataene viser denne parken. Utforsk en passende offentlig del i ditt eget tempo. Hopp over steder som krever betaling eller tillatelse.','Bruk kartet til å se på alternativene. Ingen rute eller åpningstid er bekreftet her.','Parken er ekte. Tidsplanen er din.'],place='park')
assert len(cards)==36
Path('plugin/gymnotfound/content/activities.json').write_text(json.dumps(cards,ensure_ascii=False,indent=2)+'\n')
