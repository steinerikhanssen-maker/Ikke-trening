
import 'package:flutter/material.dart';

void main() => runApp(const Viamo());
const green = Color(0xff145641);
const ink = Color(0xff172b23);
const muted = Color(0xff738276);
const orange = Color(0xffd96843);
const cream = Color(0xfff7f8f4);
const line = Color(0xffe3e9e2);

class Place {
  const Place(this.id, this.city, this.name, this.note);
  final String id, city, name, note;
}
const places = <Place>[
  Place('bo1','Bologna','Mercato delle Erbe','Matmarked og små spisesteder i sentrum'),
  Place('bo2','Bologna','Piazza Maggiore','Historisk torg og møteplass'),
  Place('bo3','Bologna','Portici di Bologna','Søyleganger og gangveier gjennom byen'),
  Place('na1','Napoli','Quartieri Spagnoli','Byområde med tett gateliv'),
  Place('na2','Napoli','Lungomare','Promenade langs sjøen'),
  Place('sa1','Santa Marinella','Stranden','Strandområde nær sentrum'),
  Place('sa2','Santa Marinella','Santa Marinella stasjon','Togstasjon'),
];

class Post {
  Post(this.id,this.city,this.author,this.type,this.title,this.text,{this.placeId,this.photo, List<String>? replies})
      : replies = replies ?? [];
  final int id;
  final String city, author, type, title, text;
  final String? placeId, photo;
  final List<String> replies;
}

class Viamo extends StatelessWidget {
  const Viamo({super.key});
  @override Widget build(BuildContext context) => MaterialApp(
    debugShowCheckedModeBanner:false,
    title:'Viamo Social – Flutter',
    theme:ThemeData(
      useMaterial3:true, scaffoldBackgroundColor:cream,
      colorScheme:ColorScheme.fromSeed(seedColor:green, surface:cream),
      textTheme:const TextTheme(headlineLarge:TextStyle(fontSize:29,fontWeight:FontWeight.w800,letterSpacing:-1.1,color:ink),
        titleLarge:TextStyle(fontSize:20,fontWeight:FontWeight.w800,letterSpacing:-.5,color:ink)),
      inputDecorationTheme:InputDecorationTheme(filled:true,fillColor:Colors.white,
        border:OutlineInputBorder(borderSide:const BorderSide(color:line),borderRadius:BorderRadius.circular(14)),
        enabledBorder:OutlineInputBorder(borderSide:const BorderSide(color:line),borderRadius:BorderRadius.circular(14))),
    ),
    home:const SocialHome(),
  );
}

class SocialHome extends StatefulWidget {
 const SocialHome({super.key});
 @override State<SocialHome> createState()=>_SocialHomeState();
}
class _SocialHomeState extends State<SocialHome> {
 String city='Bologna',tab='Strøm',filter='Alt',query='';
 int nextId=100;
 final liked=<int>{}, saved=<int>{}, expanded=<int>{};
 final plan=<String>{};
 final posts=<Post>[
   Post(1,'Bologna','Mari','Spørsmål','Hvor spiser vi en god, enkel lunsj i Bologna?',
       'Vi har bare én dag. Hva anbefaler dere som har vært der selv?',placeId:'bo1',
       replies:['Elin (eksempel): Se gjerne på tilbudet ved Mercato delle Erbe.']),
   Post(2,'Bologna','Jonas','Erfaring','En dag til fots i Bologna – hvilke steder ville du lagt til?',
       'Jeg ville startet på Piazza Maggiore. Er det noe man absolutt bør få med seg?',placeId:'bo2',
       photo:'https://images.unsplash.com/photo-1533105079780-92b9be482077?w=1100&q=80',
       replies:['Tone (eksempel): Se på de historiske søylegangene.']),
   Post(3,'Bologna','Fellesskapet','Guide','Bologna – en tur satt sammen av folks tips',
       'Samtalene kan bli en guide. Åpne steder og legg dem til i din egen dag.',placeId:'bo3'),
   Post(4,'Napoli','Elin','Spørsmål','Hvor kan vi gå en fin tur langs sjøen?',
       'Vi vil kombinere en spasertur med middag.',placeId:'na2'),
   Post(5,'Napoli','Thomas','Erfaring','Hva er ditt beste tips for Quartieri Spagnoli?',
       'Del gjerne et sted eller en opplevelse som var verdt besøket.',placeId:'na1'),
   Post(6,'Santa Marinella','Anna','Spørsmål','Hvilken del av stranden er best for en rolig dag?',
       'Vi kommer med tog og vil helst gå til stranden.',placeId:'sa1'),
   Post(7,'Santa Marinella','Fellesskapet','Guide','Fra toget til stranden',
       'Samle stedene og reisendes erfaringer i en enkel dagsplan.',placeId:'sa2'),
 ];
 Place? place(String? id) {
   for(final p in places){if(p.id==id)return p;}
   return null;
 }
 List<Post> get matches => posts.where((p){
   if(p.city!=city)return false;
   if(tab=='Lagret' && !saved.contains(p.id))return false;
   if(filter!='Alt' && p.type!=filter)return false;
   final q=query.trim().toLowerCase();
   return q.isEmpty || (p.title+' '+p.text+' '+(place(p.placeId)?.name??'')).toLowerCase().contains(q);
 }).toList();

 @override Widget build(BuildContext context){
   final width=MediaQuery.sizeOf(context).width;
   final desktop=width>=1040, roomy=width>=700;
   return Scaffold(
     body:SafeArea(child:Column(children:[
       Container(color:Colors.white,padding:EdgeInsets.symmetric(horizontal:roomy?24:14,vertical:11),
         child:Row(children:[
           const Text('viamo',style:TextStyle(color:green,fontSize:29,fontWeight:FontWeight.w900,letterSpacing:-1.8)),
           if(roomy)...[const SizedBox(width:12),const Text('Italia gjennom mennesker',style:TextStyle(color:muted,fontSize:12))],
           const Spacer(),
           Container(padding:const EdgeInsets.only(left:8),decoration:BoxDecoration(color:cream,borderRadius:BorderRadius.circular(10)),
             child:Row(children:[
               const Icon(Icons.place_outlined,size:17,color:green),
               SizedBox(width:roomy?175:140,child:DropdownButtonHideUnderline(child:DropdownButton<String>(isExpanded:true,value:city,
                 style:const TextStyle(color:ink,fontSize:12,fontWeight:FontWeight.w700),
                 items:['Bologna','Napoli','Santa Marinella'].map((v)=>DropdownMenuItem(value:v,child:Text(v))).toList(),
                 onChanged:(v)=>setState((){city=v??city;filter='Alt';query='';})))),
             ])),
           if(roomy)...[const SizedBox(width:9),const Tooltip(message:'Eksempelinnhold',child:Icon(Icons.science_outlined,color:muted))],
         ])),
       const Divider(height:1,color:line),
       Expanded(child:desktop?Row(crossAxisAlignment:CrossAxisAlignment.start,children:[
         SizedBox(width:205,child:_navigation()),
         const VerticalDivider(width:1,color:line),
         Expanded(child:Center(child:ConstrainedBox(constraints:const BoxConstraints(maxWidth:670),child:_content()))),
         SizedBox(width:272,child:_sidebar()),
       ]):_content()),
     ])),
     bottomNavigationBar:desktop?null:NavigationBar(
       height:64,backgroundColor:Colors.white,indicatorColor:const Color(0xffdfefe4),
       selectedIndex:['Strøm','Steder','Lagret','Min dag'].indexOf(tab),
       onDestinationSelected:(i)=>setState((){tab=['Strøm','Steder','Lagret','Min dag'][i];query='';filter='Alt';}),
       destinations:const [
         NavigationDestination(icon:Icon(Icons.dynamic_feed_outlined),label:'Strøm'),
         NavigationDestination(icon:Icon(Icons.explore_outlined),label:'Steder'),
         NavigationDestination(icon:Icon(Icons.bookmark_outline),label:'Lagret'),
         NavigationDestination(icon:Icon(Icons.route_outlined),label:'Min dag'),
       ],
     ),
     floatingActionButton:tab=='Min dag'?null:FloatingActionButton(
       backgroundColor:orange,foregroundColor:Colors.white,onPressed:()=>_compose(),child:const Icon(Icons.add)),
   );
 }
 Widget _navigation()=>Container(color:Colors.white,padding:const EdgeInsets.all(12),child:Column(children:[
   const SizedBox(height:17),
   ...['Strøm','Steder','Lagret','Min dag'].map((t)=>Padding(padding:const EdgeInsets.only(bottom:6),
     child:ListTile(
       selected:tab==t,selectedTileColor:const Color(0xffe8f2ea),shape:RoundedRectangleBorder(borderRadius:BorderRadius.circular(12)),
       leading:Icon(t=='Strøm'?Icons.dynamic_feed_outlined:t=='Steder'?Icons.place_outlined:t=='Lagret'?Icons.bookmark_outline:Icons.route_outlined,
         color:tab==t?green:muted),
       title:Text(t,style:const TextStyle(fontSize:13,fontWeight:FontWeight.w700)),
       onTap:()=>setState((){tab=t;query='';filter='Alt';}),
     ))),
   const Spacer(),
   const Padding(padding:EdgeInsets.all(10),child:Text('Flutter-demo. Fiktive profiler og eksempelinnhold. Ingen data publiseres.',style:TextStyle(color:muted,fontSize:11,height:1.5))),
 ]));
 Widget _content()=>ListView(padding:const EdgeInsets.fromLTRB(16,23,16,95),children:[
   if(tab=='Strøm')...[
     const Text('FELLESSKAPET',style:TextStyle(color:orange,fontSize:11,fontWeight:FontWeight.w900,letterSpacing:1.2)),
     const SizedBox(height:8),
     Text('Italia, slik folk opplever det.',style:Theme.of(context).textTheme.headlineLarge),
     const SizedBox(height:8),
     const Text('Spørsmål, erfaringer, bilder og guider. Alt hører til stedene det handler om.',style:TextStyle(color:muted,fontSize:13,height:1.5)),
     const SizedBox(height:19),
     _composerCard(),const SizedBox(height:14),
     TextField(decoration:const InputDecoration(hintText:'Søk i mennesker, spørsmål og steder',prefixIcon:Icon(Icons.search,color:green)),
       onChanged:(v)=>setState(()=>query=v)),
     const SizedBox(height:12),
     SingleChildScrollView(scrollDirection:Axis.horizontal,child:Row(children:['Alt','Spørsmål','Erfaring','Bilde','Guide'].map((f)=>
       Padding(padding:const EdgeInsets.only(right:7),child:ChoiceChip(label:Text(f),selected:filter==f,
         selectedColor:const Color(0xffdfeee3),backgroundColor:Colors.white,
         onSelected:(_)=>setState(()=>filter=f)))).toList())),
     const SizedBox(height:17),
     Row(children:[Expanded(child:Text('Fra folk i '+city,style:Theme.of(context).textTheme.titleLarge)),
       const Text('DEMO',style:TextStyle(color:muted,fontSize:10,fontWeight:FontWeight.w800))]),
     const SizedBox(height:12),
     if(matches.isEmpty)_empty('Ingen treff i eksempeldataene.'),
     ...matches.map(_postCard),
   ]else if(tab=='Steder')...[
     Text('Steder i '+city,style:Theme.of(context).textTheme.headlineLarge),
     const SizedBox(height:9),
     const Text('Samme sted forbinder samtaler, erfaringer og turer.',style:TextStyle(color:muted)),
     const SizedBox(height:22),
     ...places.where((p)=>p.city==city).map(_placeCard),
   ]else if(tab=='Lagret')...[
     Text('Lagret',style:Theme.of(context).textTheme.headlineLarge),
     const SizedBox(height:10),
     if(matches.isEmpty)_empty('Lagre innlegg fra strømmen for å finne dem igjen.'),
     ...matches.map(_postCard),
   ]else...[
     Text('Min dag i '+city,style:Theme.of(context).textTheme.headlineLarge),
     const SizedBox(height:10),
     const Text('Steder du har tatt med videre fra samtalene.',style:TextStyle(color:muted)),
     const SizedBox(height:18),
     if(!plan.any((id)=>place(id)?.city==city))_empty('Åpne et sted og trykk Legg til i min dag.'),
     ...plan.where((id)=>place(id)?.city==city).map((id)=>_placeCard(place(id)!)),
   ],
 ]);
 Widget _composerCard()=>Container(padding:const EdgeInsets.all(14),
   decoration:BoxDecoration(color:Colors.white,border:Border.all(color:line),borderRadius:BorderRadius.circular(17)),
   child:Column(children:[
     Row(children:[_avatar('DU'),const SizedBox(width:10),Expanded(child:InkWell(
       onTap:()=>_compose(),borderRadius:BorderRadius.circular(12),
       child:Container(padding:const EdgeInsets.all(14),decoration:BoxDecoration(color:cream,borderRadius:BorderRadius.circular(12)),
         child:Text('Hva vil du dele fra '+city+'?',style:const TextStyle(fontSize:12,color:muted)))))]),
     const SizedBox(height:12),
     Wrap(spacing:8,runSpacing:5,alignment:WrapAlignment.spaceEvenly,children:[
       TextButton.icon(onPressed:()=>_compose(kind:'Spørsmål'),icon:const Icon(Icons.help_outline,size:18),label:const Text('Spørsmål')),
       TextButton.icon(onPressed:()=>_compose(kind:'Erfaring'),icon:const Icon(Icons.auto_awesome_outlined,size:18),label:const Text('Erfaring')),
       TextButton.icon(onPressed:()=>_compose(kind:'Bilde'),icon:const Icon(Icons.photo_camera_outlined,size:18),label:const Text('Bilde')),
     ]),
   ]));
 Widget _avatar(String name)=>CircleAvatar(radius:20,backgroundColor:const Color(0xfff4e2d3),
   child:Text(name,style:const TextStyle(color:Color(0xff986548),fontSize:12,fontWeight:FontWeight.w800)));
 Widget _postCard(Post p){
   final location=place(p.placeId), opened=expanded.contains(p.id);
   return Container(margin:const EdgeInsets.only(bottom:13),padding:const EdgeInsets.all(15),
     decoration:BoxDecoration(color:Colors.white,border:Border.all(color:line),borderRadius:BorderRadius.circular(18)),
     child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[
       Row(children:[
         _avatar(p.author.substring(0,1)),
         const SizedBox(width:10),
         Expanded(child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[
           Text(p.author,style:const TextStyle(color:ink,fontSize:13,fontWeight:FontWeight.w800)),
           Text(p.city+' · Eksempel',style:const TextStyle(color:muted,fontSize:10)),
         ])),
         Container(padding:const EdgeInsets.symmetric(horizontal:10,vertical:6),
           decoration:BoxDecoration(color:p.type=='Spørsmål'?const Color(0xffffefdf):const Color(0xffe7f2eb),
             borderRadius:BorderRadius.circular(30)),
           child:Text(p.type,style:TextStyle(fontSize:10,fontWeight:FontWeight.w800,
             color:p.type=='Spørsmål'?const Color(0xffa56a31):green))),
       ]),
       const SizedBox(height:14),
       Text(p.title,style:const TextStyle(color:ink,fontSize:18,fontWeight:FontWeight.w800,height:1.3,letterSpacing:-.35)),
       const SizedBox(height:8),
       Text(p.text,style:const TextStyle(color:ink,fontSize:13,height:1.5)),
       if(location!=null)...[
         const SizedBox(height:11),
         OutlinedButton.icon(onPressed:()=>_openPlace(location),icon:const Icon(Icons.place_outlined,size:17),
           label:Text(location.name+'  ›',style:const TextStyle(fontSize:12,fontWeight:FontWeight.w700)),
           style:OutlinedButton.styleFrom(foregroundColor:green,backgroundColor:const Color(0xfff0f6f1),side:BorderSide.none)),
       ],
       if(p.photo!=null)...[
         const SizedBox(height:10),
         ClipRRect(borderRadius:BorderRadius.circular(12),child:SizedBox(height:195,width:double.infinity,
           child:Image.network(p.photo!,fit:BoxFit.cover,errorBuilder:(c,e,s)=>const ColoredBox(
             color:Color(0xffe0eee3),child:Center(child:Icon(Icons.landscape_outlined,color:green,size:54)))))),
         const SizedBox(height:5),
         const Text('Illustrasjonsfoto, ikke dokumentasjon av stedet.',style:TextStyle(color:muted,fontSize:10)),
       ],
       const SizedBox(height:10),const Divider(color:line,height:1),
       Wrap(spacing:3,children:[
         TextButton.icon(onPressed:()=>setState(()=>liked.contains(p.id)?liked.remove(p.id):liked.add(p.id)),
           icon:Icon(liked.contains(p.id)?Icons.favorite:Icons.favorite_outline,size:18),
           label:Text(liked.contains(p.id)?'Likt':'Liker')),
         TextButton.icon(onPressed:()=>setState(()=>opened?expanded.remove(p.id):expanded.add(p.id)),
           icon:const Icon(Icons.chat_bubble_outline,size:17),label:Text('Svar ('+p.replies.length.toString()+')')),
         TextButton.icon(onPressed:()=>setState(()=>saved.contains(p.id)?saved.remove(p.id):saved.add(p.id)),
           icon:Icon(saved.contains(p.id)?Icons.bookmark:Icons.bookmark_outline,size:17),
           label:Text(saved.contains(p.id)?'Lagret':'Lagre')),
       ]),
       if(opened)Container(width:double.infinity,padding:const EdgeInsets.all(13),
         decoration:BoxDecoration(color:cream,borderRadius:BorderRadius.circular(11)),
         child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[
           if(p.replies.isEmpty)const Text('Ingen svar ennå.',style:TextStyle(color:muted,fontSize:12)),
           ...p.replies.map((r)=>Padding(padding:const EdgeInsets.only(bottom:11),
             child:Text(r,style:const TextStyle(fontSize:12,color:ink,height:1.4)))),
           TextButton.icon(onPressed:()=>_reply(p),icon:const Icon(Icons.edit_outlined,size:16),label:const Text('Skriv svar')),
         ])),
     ]));
 }
 Widget _placeCard(Place p)=>Container(margin:const EdgeInsets.only(bottom:11),
   decoration:BoxDecoration(color:Colors.white,border:Border.all(color:line),borderRadius:BorderRadius.circular(16)),
   child:ListTile(contentPadding:const EdgeInsets.symmetric(horizontal:12,vertical:7),
     leading:const CircleAvatar(backgroundColor:Color(0xffe2eee5),child:Icon(Icons.place_outlined,color:green)),
     title:Text(p.name,style:const TextStyle(color:ink,fontWeight:FontWeight.w800)),
     subtitle:Text(p.note,style:const TextStyle(color:muted,fontSize:12)),
     trailing:tab=='Min dag'?IconButton(icon:const Icon(Icons.remove_circle_outline,color:orange),
       onPressed:()=>setState(()=>plan.remove(p.id))):const Icon(Icons.chevron_right,color:green),
     onTap:()=>_openPlace(p)));
 Widget _empty(String msg)=>Container(padding:const EdgeInsets.all(24),
   decoration:BoxDecoration(color:Colors.white,border:Border.all(color:line),borderRadius:BorderRadius.circular(15)),
   child:Text(msg,textAlign:TextAlign.center,style:const TextStyle(color:muted,height:1.5)));
 Widget _sidebar()=>Container(color:Colors.white,padding:const EdgeInsets.all(16),child:ListView(children:[
   const SizedBox(height:15),
   const Text('SNAKKES OM I OMRÅDET',style:TextStyle(color:orange,fontSize:10,fontWeight:FontWeight.w900,letterSpacing:1)),
   const SizedBox(height:9),
   Text('Steder i '+city,style:Theme.of(context).textTheme.titleLarge),
   const SizedBox(height:14),
   ...places.where((p)=>p.city==city).map((p)=>Padding(padding:const EdgeInsets.only(bottom:8),
     child:ListTile(tileColor:cream,shape:RoundedRectangleBorder(borderRadius:BorderRadius.circular(12)),
       leading:const Icon(Icons.place_outlined,color:green),title:Text(p.name,style:const TextStyle(fontSize:12,fontWeight:FontWeight.w700)),
       onTap:()=>_openPlace(p)))),
   const SizedBox(height:22),
   const Text('ÉN SAMMENHENG',style:TextStyle(color:orange,fontSize:10,fontWeight:FontWeight.w900,letterSpacing:1)),
   const SizedBox(height:7),
   const Text('Innlegg → sted → samtale → din dag',style:TextStyle(color:ink,fontSize:15,fontWeight:FontWeight.w800)),
   const SizedBox(height:7),
   const Text('Alle delene bruker den samme stedsidentiteten, ikke parallelle seksjoner.',
     style:TextStyle(color:muted,fontSize:12,height:1.5)),
   const SizedBox(height:20),
   const Text('Lokal prototype. Ingen innlegg er publisert på Viamo.',
     style:TextStyle(color:muted,fontSize:11,height:1.5)),
 ]));
 void _openPlace(Place p){
   final related=posts.where((x)=>x.placeId==p.id).toList();
   showModalBottomSheet<void>(context:context,isScrollControlled:true,showDragHandle:true,
     backgroundColor:cream,builder:(ctx)=>SafeArea(child:ConstrainedBox(
       constraints:BoxConstraints(maxHeight:MediaQuery.sizeOf(ctx).height*.83),
       child:ListView(shrinkWrap:true,padding:const EdgeInsets.fromLTRB(22,2,22,30),children:[
         const Text('STED OG FELLESSKAP',style:TextStyle(color:orange,fontSize:10,fontWeight:FontWeight.w900)),
         const SizedBox(height:7),
         Text(p.name,style:Theme.of(ctx).textTheme.headlineLarge),
         const SizedBox(height:8),Text(p.note,style:const TextStyle(color:ink)),
         const SizedBox(height:14),
         FilledButton.icon(style:FilledButton.styleFrom(backgroundColor:green),
           onPressed:(){setState(()=>plan.add(p.id));Navigator.pop(ctx);},
           icon:Icon(plan.contains(p.id)?Icons.check:Icons.add),
           label:Text(plan.contains(p.id)?'I min dag':'Legg til i min dag')),
         OutlinedButton.icon(onPressed:(){Navigator.pop(ctx);_compose(kind:'Spørsmål',placeId:p.id);},
           icon:const Icon(Icons.chat_outlined),label:const Text('Spør om stedet')),
         const SizedBox(height:19),
         Text('Samtaler knyttet til stedet',style:Theme.of(ctx).textTheme.titleLarge),
         const SizedBox(height:11),
         if(related.isEmpty)const Text('Ingen demoinnlegg ennå.'),
         ...related.map((x)=>ListTile(contentPadding:EdgeInsets.zero,
           leading:const Icon(Icons.forum_outlined,color:green),
           title:Text(x.title,style:const TextStyle(fontSize:13,fontWeight:FontWeight.w700)),
           subtitle:Text(x.type),
           onTap:(){Navigator.pop(ctx);setState((){tab='Strøm';filter='Alt';query='';expanded.add(x.id);});})),
         const SizedBox(height:13),
         const Text('Dette er eksempelinnhold, ikke publiserte menneskelige erfaringer.',
           style:TextStyle(color:muted,fontSize:11)),
       ]))));
 }
 Future<void> _reply(Post p) async{
   final controller=TextEditingController();
   final value=await showDialog<String>(context:context,builder:(ctx)=>AlertDialog(
     title:const Text('Skriv et svar'),
     content:TextField(controller:controller,maxLines:4,maxLength:400,
       decoration:const InputDecoration(hintText:'Del en konkret erfaring')),
     actions:[TextButton(onPressed:()=>Navigator.pop(ctx),child:const Text('Avbryt')),
       FilledButton(onPressed:()=>Navigator.pop(ctx,controller.text.trim()),child:const Text('Legg til'))]));
   controller.dispose();
   if(!mounted||value==null||value.isEmpty)return;
   setState((){p.replies.add('Du: '+value);expanded.add(p.id);});
 }
 Future<void> _compose({String kind='Erfaring',String? placeId})async{
   final headline=TextEditingController(),body=TextEditingController();
   var type=kind;String? placeChoice=placeId??'';
   await showModalBottomSheet<void>(context:context,isScrollControlled:true,showDragHandle:true,
     backgroundColor:cream,builder:(ctx)=>StatefulBuilder(builder:(ctx,update)=>Padding(
       padding:EdgeInsets.fromLTRB(18,0,18,MediaQuery.viewInsetsOf(ctx).bottom+24),
       child:SingleChildScrollView(child:Column(mainAxisSize:MainAxisSize.min,crossAxisAlignment:CrossAxisAlignment.start,children:[
         Text('Del med '+city,style:Theme.of(ctx).textTheme.headlineLarge),
         const Text('Kun i demonstrasjonen. Ingen ekte publisering.',style:TextStyle(color:muted,fontSize:12)),
         const SizedBox(height:12),
         Wrap(spacing:6,children:['Spørsmål','Erfaring','Bilde','Guide'].map((k)=>ChoiceChip(
           label:Text(k),selected:type==k,onSelected:(_)=>update(()=>type=k))).toList()),
         const SizedBox(height:12),
         TextField(controller:headline,maxLength:130,decoration:const InputDecoration(labelText:'Overskrift eller spørsmål')),
         const SizedBox(height:9),
         TextField(controller:body,maxLength:600,maxLines:3,decoration:const InputDecoration(labelText:'Din erfaring eller mer informasjon')),
         const SizedBox(height:9),
         DropdownButtonFormField<String>(value:placeChoice,decoration:const InputDecoration(labelText:'Knytt til sted'),
           items:[const DropdownMenuItem(value:'',child:Text('Hele området')),
             ...places.where((p)=>p.city==city).map((p)=>DropdownMenuItem(value:p.id,child:Text(p.name)))],
           onChanged:(v)=>update(()=>placeChoice=v)),
         const SizedBox(height:15),
         SizedBox(width:double.infinity,child:FilledButton.icon(
           style:FilledButton.styleFrom(backgroundColor:green,padding:const EdgeInsets.all(14)),
           icon:const Icon(Icons.send_outlined),label:const Text('Legg til i demo'),
           onPressed:(){
             if(headline.text.trim().isEmpty)return;
             setState((){
               posts.insert(0,Post(nextId++,city,'Du',type,headline.text.trim(),body.text.trim(),
                 placeId:placeChoice==''?null:placeChoice));
               tab='Strøm';filter='Alt';query='';
             });
             Navigator.pop(ctx);
           })),
       ])))));
   headline.dispose();body.dispose();
 }
}
