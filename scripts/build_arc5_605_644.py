"""Sequential adaptation of novel chapters 32–34, pages 605–644."""
import json
from pathlib import Path

# number, title, time, location, cast, visual beat, speaker:text pairs, composition
ROWS = [
 (605,"Os mapas em silêncio","Dia 464 · anoitecer","arquivo-escola","ordelia,eda","Ordelia and Eda spread the returned coastal maps on the familiar oak archive table; the west shelves remain locked.","Ordelia:Marque a haste como observação, não como prova.|Eda:E a leitura três marcas acima?","map-table"),
 (606,"Permissão para observar","Dia 465 · manhã","sala-elementos","oru,runa","Recovering Oru sits beside the south door of the square elemental classroom; Runa enters with healing brow cut and bruised left arm.","Oru:Hoje você observa antes de praticar.|Runa:Quero aprender quando devo parar.","door-and-teacher"),
 (607,"Um pires e um fio","Dia 465 · manhã","sala-elementos","oru,runa","On the familiar square classroom table stand one saucer of actual water, wet cotton thread and a small wooden piece; the brazier is closed and western sand box sealed.","Oru:Somente a água presente pode conduzir o impulso.|Runa:Então mostre o limite.","table-detail"),
 (608,"Dois dedos de distância","Dia 465 · manhã","sala-elementos","runa,oru","Runa guides the little wooden piece two finger widths along a wetted cotton thread while Oru watches from his chair; no levitating objects.","Runa:Moveu só enquanto o fio estava úmido.|Oru:Exatamente.","water-thread"),
 (609,"Quando o fio se rompe","Dia 465 · manhã","sala-elementos","runa,oru","The thin wet thread breaks; the piece stops on the square table, while Runa holds her injured left arm close, Oru intervening calmly.","Oru:Chega. A dor também é uma medida.|Runa:Eu queria tentar mais uma vez.","stopped-motion"),
 (610,"Perguntas no banco público","Dia 465 · manhã","sala-elementos","liria,oru","Suspended Líria watches Oru's lesson from the public rear bench with her brass-chained notebook closed over one knee; two dark tight braids and chin scar remain visible.","Líria:Quanta água custa deslocar esse peso?","observer-panel"),
 (611,"O último curativo","Dia 465 · tarde","enfermaria-leste","runa,curandeira","The school healer removes Runa's last brow dressing in the established east infirmary; healed small brow cut and left-arm bruise still visible.","Curandeira:Escada pode. Esforço, ainda não.|Runa:Vou respeitar isso.","infirmary-close"),
 (612,"Um degrau abaixo","Dia 465 · tarde","escada-biblioteca","ilyan,runa","Ilyan carries Runa's books on the library stairs while Runa climbs independently a step ahead, both visibly adults with natural anatomy.","Runa:Posso subir sem apoio.|Ilyan:Eu levo apenas os livros.","stair-diagonal"),
 (613,"A mesa liberada","Dia 465 · tarde","galeria-biblioteca","ordelia,ilyan,runa","Ordelia unlocks the upper copying table of the library gallery, while the western archive's barred gate stays shut in the same room.","Ordelia:A mesa de cópias está livre. O arquivo oeste continua fechado.|Ilyan:Usaremos as séries registradas.","gallery-wide"),
 (614,"Vento do norte","Dia 465 · tarde","galeria-biblioteca","runa,ilyan","At the upper gallery copying table, Runa compares two real water-level charts from Beren and Adra; Ilyan aligns the north-wind dates with a wooden ruler.","Runa:O atraso cresce com vento do norte.|Ilyan:Há uma derivação antes da eclusa.","chart-two-shot"),
 (615,"A linha que falta","Dia 465 · tarde","galeria-biblioteca","ilyan,runa","Ilyan draws a dotted uncertainty along the physically mapped canal rather than inventing an exact outlet; Runa checks the open source sheets.","Ilyan:Ainda não sabemos onde ela entra.|Runa:Escreva isso no mapa.","uncertain-map"),
 (616,"Carta de Pedra-Mansa","Dia 466 · manhã","patio-central","ilyan,mensageiro","An ordinary courier hands Ilyan a sealed letter from Pedra-Mansa beside the round central courtyard pool; Nima is absent, no magical apparition.","Mensageiro:Chegou pela estrada de ontem.|Ilyan:É de Pedra-Mansa.","letter-arrival"),
 (617,"A pergunta de Nima","Dia 466 · manhã","mesa-patio","ilyan,runa","At a quiet courtyard table Ilyan openly shows Nima's handwritten letter to Runa; only the two are physically present.","Ilyan:Ela perguntou pelo seu braço.|Runa:Posso responder com você?","letter-two-shot"),
 (618,"Duas caligrafias","Dia 466 · manhã","mesa-patio","runa,ilyan","Runa writes one honest line about her recovery; Ilyan adds the coastal measurements and asks about the eight-toothed wheel, two distinct scripts on one paper.","Runa:Vou agradecer sem fingir que já estou bem.|Ilyan:E perguntar pela roda que Nima conhece.","writing-close"),
 (619,"Para o correio de amanhã","Dia 466 · meio-dia","posto-correio","ilyan,runa","Ilyan and Runa seal the reply at a staffed medieval courier counter; it will leave on the next day's ordinary cart.","Ilyan:Segue na carroça de amanhã.|Runa:Ela saberá que lemos juntos.","mail-counter"),
 (620,"Saída ao sul","Dia 466 · tarde","patio-leste","sere,caio,ilyan","Sere sets a safe evacuation drill in the established east training yard; Caio guides two groups toward its south exit while Ilyan guards the rear with blunt sword.","Sere:Caio, conduza as duas turmas.|Caio:Ilyan cobre os últimos.","training-wide"),
 (621,"Quem ainda falta","Dia 466 · tarde","patio-leste","ilyan,runa","From behind the practice fence, Runa observes Ilyan checking the last students before leaving the retreat line; no injured or duplicated extras.","Runa:Você conta quem ainda não saiu.|Ilyan:É o único número que importa agora.","fence-observation"),
 (622,"Nome de Mira","Dia 466 · entardecer","patio-central","ilyan,runa","After drill at the round courtyard pool, Ilyan remembers his missing mother Mira without visual apparition; Runa remains beside him quietly.","Ilyan:Mira teria entendido esse mapa.|Runa:Podemos ficar aqui um pouco.","quiet-pool"),
 (623,"A peça numerada","Dia 467 · manhã","arquivo-escola","beren,ordelia","Licensed mason Beren presents a removed wooden intake piece numbered with its pre-removal drawing; Ordelia enters both into the archive evidence ledger.","Beren:Há desgaste antigo e lasca recente. Não sei quando surgiu.|Ordelia:As testemunhas verão os dois lados.","evidence-table"),
 (624,"A mensagem do inspetor","Dia 467 · manhã","arquivo-escola","eda,ordelia","Eda reads Maelor's delivered written demand not to halt station works while Ordelia keeps the numbered evidence secure; Maelor is not physically there.","Eda:Segurança e transparência são condições da obra.|Ordelia:Vou anexar sua resposta.","document-exchange"),
 (625,"Só a cópia pública","Dia 467 · tarde","sala-publica-arquivo","liria,ordelia","Suspended Líria requests inspection of the wooden piece, but Ordelia provides only its public measured drawing at the supervised archive counter.","Líria:Posso comparar a curvatura?|Ordelia:A cópia, sim. O objeto, não.","archive-counter"),
 (626,"A escuta da pedra","Dia 467 · tarde","sala-publica-arquivo","liria,oru","Under Oru's supervision, Líria presses two fingertips against a separate chipped test stone, sensing the direction of an existing crack; the wooden evidence remains untouched across the room.","Líria:Madeira não responde. Preciso da soleira mineral.","stone-close"),
 (627,"Uma proposta não absolve","Dia 467 · tarde","arquivo-escola","liria,ordelia","Líria proposes a licensed examination of the stone sill to Ordelia, presenting written method; the archive keeper records it without lifting suspension.","Ordelia:Registro a proposta. Sua sanção permanece.|Líria:Eu sei.","proposal-facing"),
 (628,"O custo de odiar","Dia 467 · entardecer","sala-elementos","oru,runa","Runa consults the public proposal in the elemental classroom while seated Oru asks her to consider a useful measurement from someone she resents.","Oru:Preferiria uma medição falsa?|Runa:Não. Ainda estou com raiva.","teacher-dialogue"),
 (629,"Três perguntas","Dia 467 · entardecer","sala-elementos","runa,oru","Under Oru's supervision Runa guides existing water from a saucer through a short wetted thread and stops before the source is spent; no floating mass.","Runa:De onde vem, por onde passa, onde termina.|Oru:Agora você controla a saída.","method-three-beats"),
 (630,"A palavra cedo demais","Dia 467 · crepúsculo","patio-central","ilyan,runa","By the courtyard's round reflecting pool, Ilyan confesses his love before measuring the word; Runa listens with tenderness and complicated fresh hurt.","Ilyan:Eu a amo. Isso não me autoriza a ferir Líria.|Runa:Repita quando não for resposta a uma ferida.","pool-emotional"),
 (631,"Escolher ficar","Dia 467 · noite","quarto-cedro","ilyan,runa","In Ilyan's established cedar room, his blunt sword rests by the chest, a lamp glows; Runa chooses to stay and the adults exchange a gentle kiss, fully clothed, respecting her sore rib.","Ilyan:Você pode ficar ou voltar sem se explicar.|Runa:Hoje eu escolho ficar.","cedar-room"),
 (632,"Luz pela janela norte","Dia 468 · manhã","quarto-cedro","runa,ilyan","Morning light from the same north window falls on Ilyan and Runa seated fully clothed with bread; her healing brow and bruise remain, affectionate but thoughtful.","Runa:Confiará que eu escolha meus limites?|Ilyan:Sim, mesmo quando for difícil.","morning-room"),
 (633,"Cadeiras a mais","Dia 469 · manhã","sala-conselho","ordelia,eda,talin","Ordelia opens the House council chamber with extra chairs for canal workers and shore delegates; familiar long oak table and west map mural, Talin attends only to report for guardians.","Ordelia:Cada margem terá voz nesta mesa.|Talin:Eu observo e relato, não autorizo por todos.","council-establish"),
 (634,"Quem pode falar","Dia 469 · manhã","sala-conselho","ordelia,runa,liria,ilyan","Runa sits as level-series author, Líria on witness bench under suspension, Ilyan stands by door carrying records without vote; Ordelia calls for firsthand measurements.","Ordelia:Separaremos medida de boato.|Runa:Começo pelo atraso do fluxo.","council-roles"),
 (635,"A soleira em disputa","Dia 469 · manhã","sala-conselho","runa,liria,eda","Across the council oak table Runa marks delayed water flow and Líria indicates the mineral sill on a separate drawing; Eda points to the endangered low street.","Runa:Sem leituras simultâneas, a rua baixa sofre.|Líria:A pedra precisa de exame.","disputed-maps"),
 (636,"Anexos autenticados","Dia 469 · pausa","sala-conselho","mensageiro,ordelia","A municipal courier arrives through the council doorway with certified account copies from two offices, counted by Ordelia before anyone reads them.","Mensageiro:Duas repartições, duas cópias seladas.|Ordelia:Registre a chegada antes de abrir.","accounts-arrival"),
 (637,"O dinheiro das medidas","Dia 469 · pausa","sala-conselho","ordelia,eda","Ordelia and Eda read account lines linking salt company payments to Maelor's office and reimbursement of a school sluice scholarship, with no attribution of sabotage.","Eda:A mesma sociedade financiou as duas frentes.|Ordelia:Conflito de interesse. Ainda não prova fraude.","ledger-comparison"),
 (638,"A bolsa de Líria","Dia 469 · tarde","sala-conselho","liria","Líria recognizes the number of her winter scholarship among account copies, her face conflicted; two braids and chin scar visible, no other person at her side.","Líria:Minha bolsa veio desse fundo?","private-reaction"),
 (639,"O caderno de corrente","Dia 469 · tarde","quarto-liria","liria","In her own modest school room Líria compares dates in her notebook fastened by brass chain to a copied funding seal, looking for a later correction.","Líria:Esta correção chegou depois de mim.","notebook-night"),
 (640,"Pedido formal","Dia 469 · tarde","sala-publica-arquivo","liria,ordelia","Líria submits a supervised public archive consultation request to Ordelia, holding her own original notebook page; barred west archive stays closed.","Líria:Peço horário para conferir a remessa.|Ordelia:Na sala pública, com testemunha.","public-request"),
 (641,"A ordem de gabinete","Dia 469 · tarde","sala-publica-arquivo","liria,escriva-municipal","Municipal clerk at public archive counter shows Líria a dispatch list proving the two-palm elevation change came from an aide of Maelor, not a signed field survey.","Escrivã municipal:A ordem saiu do gabinete.|Líria:Não de uma leitura de campo.","dispatch-ledger"),
 (642,"Dois palmos","Dia 469 · tarde","sala-publica-arquivo","liria,escriva-municipal","Líria sketches the dated two-palm correction under clerk supervision; original remains in ledger and lacks affected community signature.","Líria:Onde está a assinatura da margem?|Escrivã municipal:Não há nesta folha.","sketch-evidence"),
 (643,"Desenho entregue","Dia 469 · fim de tarde","galeria-biblioteca","liria,runa","Líria presents a witnessed copy to Runa in upper library gallery, keeping formal distance and distinct recognizable faces; Ilyan is not between them.","Líria:Esta cópia tem número e testemunhas.|Runa:Vou conferir a origem.","tense-handoff"),
 (644,"A palavra difícil","Dia 469 · fim de tarde","galeria-biblioteca","runa,liria","Runa verifies paper, date and ink against the public index; she thanks Líria quietly but refuses to imply reconciliation after the assault.","Runa:Obrigada pela cópia. O perdão ainda não veio.|Líria:Não pedi que viesse.","restrained-two-shot"),
]

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reader/medieval/arc5-605-644.json"
CHAPTERS = [
    {"title": "Pele, promessa, manhã", "start": 605, "end": 632},
    {"title": "A escola divide-se", "start": 633, "end": 644},
]

def line(part, index):
    speaker, text = part.split(":", 1)
    x = 5 if index == 0 else 57
    target_x = 24 if index == 0 else 76
    return {"speaker": speaker, "text": text, "balloon": {"x": x, "y": 2, "w": 38, "target_x": target_x, "target_y": 28}}

pages = []
for number, title, time, place, cast, scene, dialogue, layout in ROWS:
    pages.append({"number": number, "title": title, "time": time, "place": place,
                  "layout": layout, "cast": cast.split(","), "novel_chapter": 32 if number == 605 else (33 if number <= 632 else 34),
                  "scene": scene, "lines": [line(p, i) for i, p in enumerate(dialogue.split("|"))]})

# These two generated drawings already contain empty, speaker-pointing
# outlines. Place accessible DOM lettering INSIDE each outline rather than
# stacking another balloon over it.
embedded = {
    607: [(8, 7, 35), (60, 7, 33)],
    609: [(9, 10, 32), (62, 10, 31)],
}
for page in pages:
    for speech, (x, y, width) in zip(page["lines"], embedded.get(page["number"], [])):
        speech["balloon"].update({"x": x, "y": y, "w": width, "embedded": True})

# Place speech immediately above its actual speaker in pages whose first
# panel is an empty establishing view. Keep the tails short and off faces.
placements = {
    610: [(5, 15, 38, 18, 32)],
    614: [(5, 21, 38, 24, 36), (57, 21, 38, 73, 36)],
    616: [(5, 25, 38, 22, 43), (57, 25, 38, 77, 42)],
    617: [(5, 16, 38, 24, 34), (57, 16, 38, 75, 36)],
    620: [(5, 15, 38, 26, 34), (57, 15, 38, 65, 38)],
    621: [(57, 17, 38, 76, 40), (5, 26, 38, 40, 41)],
    624: [(57, 19, 38, 76, 39), (5, 25, 38, 25, 39)],
    625: [(5, 22, 38, 23, 37), (57, 22, 38, 76, 36)],
    626: [(5, 22, 38, 24, 38)],
    630: [(5, 18, 38, 24, 37), (57, 18, 38, 76, 38)],
    631: [(57, 19, 38, 52, 43), (5, 27, 38, 29, 43)],
    632: [(57, 2, 38, 73, 33), (5, 12, 38, 29, 33)],
    633: [(5, 23, 38, 20, 38), (57, 23, 38, 79, 40)],
    634: [(5, 2, 38, 22, 17), (43, 9, 38, 55, 26)],
    635: [(4, 11, 36, 18, 34), (43, 11, 36, 51, 34)],
    636: [(5, 20, 38, 30, 40), (57, 20, 38, 74, 40)],
    637: [(57, 5, 38, 76, 35), (5, 14, 38, 24, 36)],
    638: [(5, 12, 38, 23, 29)],
    639: [(25, 7, 40, 50, 24)],
    640: [(5, 19, 38, 22, 36), (57, 19, 38, 75, 36)],
    641: [(5, 20, 38, 24, 37), (57, 20, 38, 73, 38)],
    644: [(28, 33, 38, 43, 50), (57, 68, 38, 78, 83)],
}
for page in pages:
    for speech, (x, y, width, target_x, target_y) in zip(page["lines"], placements.get(page["number"], [])):
        speech["balloon"].update({"x": x, "y": y, "w": width, "target_x": target_x, "target_y": target_y})

assert [p["number"] for p in pages] == list(range(605, 645))
OUT.write_text(json.dumps({"chapters": CHAPTERS, "pages": pages}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(OUT, len(pages))
