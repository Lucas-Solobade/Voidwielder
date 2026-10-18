"""Build the page-by-page adaptation of book chapter 32, Arcos sob chuva.

The source tuples are deliberately explicit: one beat per page, with place,
time, cast and the speaker named before the visual art is commissioned.
"""

import json
from pathlib import Path


ROWS = [
    # number, title, day/period, place, cast, visual action, dialogue, layout
    (555, "Três assinaturas", "Dia 460 · manhã", "arquivo-escola", "adra,eda,ilyan", "Adra places the coastal community's signed letter on Eda's oak desk; three signatures are visible as marks, not legible text.", "Adra:A Enseada permite medir a eclusa exterior.|Eda:Somente nesse corredor.", "wide-document"),
    (556, "A pedra de limite", "Dia 460 · manhã", "arquivo-escola", "eda,adra,ilyan", "Eda uses a wooden ruler to mark the municipal strip and the stone boundary of Ysra on a large map. The restricted north bank remains beyond the line.", "Eda:Sem licença das Faias, não cruzem esta pedra.|Ilyan:Entendi o limite.", "map-closeup"),
    (557, "Quem fica", "Dia 460 · manhã", "enfermaria-leste", "ilyan,runa", "Ilyan, travel bag in hand, informs resting Runa of the authorized mission; her bruised left arm is bandaged and she stays in the infirmary.", "Ilyan:Vou contar cada medida quando voltar.|Runa:Não posso ir com você desta vez.", "quiet-two-shot"),
    (558, "Sem atalhos", "Dia 460 · manhã", "patio-leste", "sere,ilyan,caio", "Sere sketches three routes in chalk on a board in the east training yard; Caio and Ilyan study it, archery fence behind.", "Sere:A rua baixa some primeiro na chuva.|Caio:Então a subida de pedra é a saída.", "route-board"),
    (559, "O aço sem fio", "Dia 460 · manhã", "patio-leste", "ilyan,sere", "Ilyan practices a blocking stance with Bram's short blunt training sword while Sere checks his footing, no one injured.", "Ilyan:Esta espada serve para conter uma retirada?|Sere:Sim. Não persiga o que recuar.", "practice-diagonal"),
    (560, "Flechas de contenção", "Dia 460 · manhã", "cerca-norte", "sere,caio", "Behind the safe north fence, Sere demonstrates an arrow at a hanging rope and Caio readies an arrow at a ground marker, not people.", "Sere:Primeiro desviar; só acertar se alguém for atacado.", "archery-split"),
    (561, "Peso da medida", "Dia 460 · meio-dia", "patio-leste", "adra,caio,ilyan", "Adra checks a brass survey tripod, coil of rope and medical kit. Caio realizes the equipment exceeds one ferry load.", "Adra:Faremos duas travessias.|Caio:O tripé pesa mais do que parece.", "equipment-detail"),
    (562, "Pelo portão sul", "Dia 460 · meio-dia", "portao-sul", "adra,sere,ilyan,caio", "The team departs the school through its south gate on foot, equipment counted, two coastal workers with them; Runa stays behind.", "Sere:Seis pessoas, três volumes. Vamos.", "departure-wide"),
    (563, "Valecobre a pé", "Dia 460 · tarde", "valecobre", "ilyan,caio,adra", "The group walks through Valecobre's market street toward the east quay; Ilyan carries the blunt sword, Caio carries survey rods.", "Ilyan:Seguimos a pé até o cais.|Caio:Além da rua dos oleiros.", "street-asymmetric"),
    (564, "Primeira barca", "Dia 460 · tarde", "cais-leste", "adra,caio", "At the east quay, Adra and Caio load the heavy tripod onto the first low wooden ferry; Sere and Ilyan wait ashore with remaining gear.", "Adra:Tripé e caixas comigo. Vocês vêm na segunda.", "ferry-overhead"),
    (565, "Segunda travessia", "Dia 460 · tarde", "barca-enseada", "sere,ilyan", "Ilyan and Sere ride the second ferry through grey water; the first ferry and its unloaded equipment are visible at the far bank.", "Sere:O vento virou para o norte.|Ilyan:E a chuva vem com ele.", "river-wide"),
    (566, "O corredor concedido", "Dia 460 · tarde", "estrada-enseada", "adra,sere,ilyan,caio", "After reuniting on the opposite bank, the team walks along the clearly marked public corridor to the outer sluice; no one crosses the Ysra boundary.", "Adra:Daqui em diante, somente pelo corredor marcado.", "path-depth"),
    (567, "A marca da ponte", "Dia 460 · fim de tarde", "ponte-enseada", "adra,ilyan", "Adra reads the water gauge at a stone bridge as rain darkens its stones; Ilyan records the reading on a notebook.", "Adra:A marca baixa já está perto.|Ilyan:Registrei a hora.", "bridge-gauge"),
    (568, "Aviso, não pânico", "Dia 460 · fim de tarde", "rua-baixa", "adra,caio", "A bell rings in the low street as Adra and Caio calmly knock on cottage doors and advise residents to carry medicine to high ground.", "Adra:Subam antes da próxima marca.|Caio:Há tempo para buscar os remédios.", "doorway-montage"),
    (569, "Seis pernas no capim", "Dia 460 · fim de tarde", "vala-enseada", "ilyan", "A dark mud-cutter emerges from grass by the ditch: crablike leather carapace scored with salt, six narrow legs and bone teeth. Ilyan spots it from a safe distance.", "Ilyan:Sere... há algo se movendo na vala.", "creature-reveal"),
    (570, "O saco da criança", "Dia 460 · fim de tarde", "rua-baixa", "ilyan", "A mud-cutter lunges toward a child's food sack; Ilyan steps between them, blunt short sword ready, child behind him.", "Ilyan:Para trás de mim!", "sudden-action"),
    (571, "A face do aço", "Dia 460 · fim de tarde", "rua-baixa", "ilyan", "Ilyan pushes the sack away with the flat of his blunt sword and strikes the mud-cutter's shell; its six legs remain distinct, no duplicate sword or arms.", "Ilyan:Largue!", "impact-close"),
    (572, "Linha de retirada", "Dia 460 · fim de tarde", "rua-baixa", "sere,caio,adra", "Sere positions Caio at a bend and a coastal archer atop the firm wall; Adra leads people uphill in a single safe line.", "Sere:Caio, conte a fila. Arcos para o chão à frente deles.", "tactical-wide"),
    (573, "Avô e neta", "Dia 460 · fim de tarde", "rua-baixa", "adra,ilyan", "Adra guides a child and grandfather toward high ground while Ilyan guards their ankles from approaching mud-cutters.", "Adra:Olhem para a subida. Um passo por vez.", "evacuation-close"),
    (574, "Dois ao mesmo tempo", "Dia 460 · fim de tarde", "rua-baixa", "ilyan,sere", "Two mud-cutters emerge together; Sere's arrow hits the joint of the first creature, while Ilyan turns toward the second.", "Sere:O segundo é seu!", "combat-diagonal"),
    (575, "A mordida na bota", "Dia 460 · fim de tarde", "rua-baixa", "ilyan", "One mud-cutter grips the leather of Ilyan's boot; his leg remains correctly attached and his blunt sword slides beneath the creature's belly.", "Ilyan:Solta a minha bota!", "combat-low-angle"),
    (576, "Não perseguir", "Dia 460 · fim de tarde", "rua-baixa", "sere,ilyan", "The creature tumbles back to the ditch; Sere gestures Ilyan back to the evacuation line instead of pursuing it.", "Sere:Volte à fila, Ilyan.|Ilyan:Já estou indo.", "retreat-two-shot"),
    (577, "A última casa", "Dia 460 · crepúsculo", "rua-baixa", "adra,ilyan,caio", "Water reaches the lower bridge mark; a family remains inside the last cottage, a father visible holding a tool chest.", "Adra:Pelo quintal alto, não pela calçada.|Caio:Falta uma casa!", "last-house-wide"),
    (578, "O bueiro cede", "Dia 460 · crepúsculo", "rua-baixa", "adra,ilyan", "Adra points at the sinking east sidewalk beside a storm drain; Ilyan takes the high garden path instead.", "Adra:A calçada leste está cedendo.|Ilyan:Então vamos pela pedra.", "route-obstacle"),
    (579, "Corda no poste", "Dia 460 · crepúsculo", "quintal-alto", "sere,ilyan,caio", "Sere ties a safety rope around a solid stone post and Ilyan's chest; Caio counts people at the safe entrance.", "Sere:Prenda acima das costelas.|Caio:Contarei cada saída.", "rope-detail"),
    (580, "A colher de madeira", "Dia 460 · crepúsculo", "quintal-alto", "ilyan,adra", "The family crosses the stone step one at a time; a child clutches a wooden spoon while the father carries the recovered tool chest.", "Ilyan:Primeiro a criança. Depois o avô.", "family-crossing"),
    (581, "A pedra afunda", "Dia 460 · crepúsculo", "quintal-alto", "ilyan,sere,caio", "After the last civilian crosses, the stone step collapses under Ilyan's foot; the rope arrests him as Sere and Caio haul it, sword remains tethered.", "Ilyan:Estou preso pela corda!|Sere:Puxem agora!", "rescue-angle"),
    (582, "A tira do punho", "Dia 460 · crepúsculo", "quintal-alto", "ilyan,caio", "Safe on high ground, Ilyan retrieves the blunt sword by its wrist strap and checks the intact rope; Caio steadies him.", "Ilyan:Sem essa corda, a água me levava.", "breath-close"),
    (583, "Tábuas do carrinho", "Dia 460 · noite", "dique-seguro", "sere,adra,caio", "The team dismantles boards from an abandoned cart to close a safe passage at the top of the dyke; every tool has a clear owner.", "Sere:Fechem a passagem. Os arcos nos darão tempo.", "barricade-build"),
    (584, "Martelo e arco", "Dia 460 · noite", "dique-seguro", "sere,ilyan", "Coastal blacksmith nails boards while Sere covers the barrier with a drawn bow; Ilyan braces the wood from the safe side.", "Sere:Segurem até prender!|Ilyan:Mais uma tábua aqui!", "split-action"),
    (585, "O corte de Caio", "Dia 460 · noite", "dique-seguro", "caio,ilyan", "A mud-cutter climbs the barrier and scratches Caio's forearm; Ilyan uses the blunt sword to knock its shell aside, no gore.", "Caio:Meu braço!|Ilyan:Afaste-se da borda!", "close-action"),
    (586, "Água limpa", "Dia 460 · noite", "dique-seguro", "caio,ilyan,adra", "After the animal is driven off, Ilyan washes Caio's muddy cut with clean carried water and soap while Adra offers a fresh bandage.", "Ilyan:Lodo no corte. Água limpa, sabão e atadura.", "medical-detail"),
    (587, "A senhora que faltava", "Dia 460 · noite", "posto-dique", "adra,caio,ilyan", "On the safe dyke, the team compares a household list with evacuees; two neighbors confirm an elderly woman stayed uphill with her daughter last night.", "Adra:Falta uma moradora na lista?|Caio:Na casa da filha, com duas testemunhas.", "counting-ledger"),
    (588, "A pressão lateral", "Dia 460 · noite", "posto-dique", "adra,sere,ilyan", "At a lanternlit observation post, Adra shows the outer sluice receiving pressure from a side channel drawn dry on the municipal map.", "Adra:Este braço não devia trazer água.|Sere:Vigias até amanhecer.", "sluice-night"),
    (589, "Duas séries", "Dia 460 · noite", "posto-dique", "adra,ilyan", "Adra aligns Beren's signed drawing from the school with fresh bridge readings, tracing two different times on parchment.", "Adra:A subida é parecida, mas chegou horas depois.", "measurement-close"),
    (590, "Não é uma porta só", "Dia 460 · noite", "posto-dique", "adra,sere,ilyan", "Two watercourses converge beneath the dyke in a cutaway-like illustration while the investigators compare the real flow from safety.", "Adra:Ainda não abriremos nada.|Ilyan:Pode haver duas entradas.", "water-diagram"),
    (591, "Leitura a cada sino", "Dia 461 · madrugada", "posto-dique", "sere,caio", "Sere sets watches by an iron bell and Caio writes the first overnight gauge reading, his forearm bandaged.", "Sere:Anotem a marca a cada sino. Céu claro não basta.", "night-watch"),
    (592, "O braço lavado", "Dia 461 · madrugada", "posto-dique", "ilyan,caio", "Under a dry lean-to Ilyan changes Caio's simple bandage and washes the cut again with carried clean water; quiet storm beyond.", "Ilyan:A notícia da escola chegou?|Caio:Chegou antes de nós.", "camp-conversation"),
    (593, "A diferença entre querer e fazer", "Dia 461 · madrugada", "posto-dique", "ilyan,caio", "Caio and Ilyan sit beside the safely sheathed blunt sword, speaking about anger and Runa while keeping watch.", "Caio:Você pretende enfrentar Líria?|Ilyan:Tive vontade. Não farei isso.", "quiet-night"),
    (594, "Uma carta comum", "Dia 461 · tarde", "enfermaria-leste", "runa", "A messenger delivers Ilyan's ordinary paper letter to Runa in the infirmary; the courier arrived on the first returning ferry.", "Runa:Ele escreveu as casas, não uma vitória.", "letter-window"),
    (595, "Escalas diferentes", "Dia 461 · tarde", "enfermaria-leste", "runa,beren", "Runa sits with healer's permission and compares Beren's plotted levels against an older Junco survey on a board; two visibly different scales.", "Runa:As curvas se parecem. As escalas, não.", "maps-overhead"),
    (596, "Descanso também é trabalho", "Dia 461 · noite", "enfermaria-leste", "runa", "Runa sets down the maps and lies back to rest, bruise on left arm and small brow wound still visible, rain at the pointed window.", "Runa:Uma hora de sono. Depois comparo de novo.", "infirmary-silence"),
    (597, "Permissão restrita", "Dia 462 · manhã", "posto-dique", "adra,sere", "A courier from the Faias arrives by land with a sealed restricted permit; Adra reads it beside Sere at the dry post.", "Adra:Vista da borda norte. Sem cavar nem tocar a junta.", "courier-arrival"),
    (598, "Pegadas maiores", "Dia 462 · manhã", "posto-dique", "talin,ilyan", "Talin, a red-haired pointed-eared elf with mustard cloak and cheek scar, arrives on foot and shows larger tracks near a hidden canal outlet to Ilyan.", "Ilyan:Essas pegadas são maiores?|Talin:Maiores que as dos cortadores. Não provam a pressão.", "tracks-detail"),
    (599, "Até o marco", "Dia 462 · manhã", "borda-norte", "talin,sere,adra,ilyan", "Talin leads Sere, Adra and Ilyan over wet rock to the permission boundary marker; all stay on the near side.", "Talin:Daqui observamos. Ninguém cruza.", "boundary-wide"),
    (600, "A haste torta", "Dia 462 · manhã", "borda-norte", "ilyan,talin", "Across the boundary, a sluice grille is visible with a repair wedge angled strangely; Ilyan recognizes its type but cannot touch or date it.", "Ilyan:Parece uma cunha de reparo.|Talin:Desenho a posição daqui.", "grille-telephoto"),
    (601, "Três marcas acima", "Dia 462 · manhã", "borda-norte", "sere,adra", "From a safe point Sere extends a graduated cord toward the water; Adra reads three marks above forecast as rain strengthens.", "Sere:Três marcas acima do previsto.|Adra:Registre e recolha o fio.", "measurement-rain"),
    (602, "Retirada sem prova falsa", "Dia 462 · tarde", "posto-dique", "adra,ilyan,talin", "The team returns on foot to the dyke with only sketches and timed notes; Adra corrects a rumor claiming Maelor set a trap.", "Adra:Uma haste vista à distância não prova autoria.", "post-debrief"),
    (603, "Volta à escola", "Dia 464 · tarde", "valecobre", "ilyan,sere,caio", "After the return ferry and walk through Valecobre, Ilyan reaches the school infirmary and asks the healer whether Runa may receive a visit.", "Ilyan:A curandeira liberou visitas?|Sere:Eu levo os registros ao arquivo.", "return-archway"),
    (604, "Lugar para a dúvida", "Dia 464 · tarde", "patio-central", "ilyan,runa", "In the school central courtyard by its round pool, Ilyan tells Runa of the child, rope, workers and uncertain tracks; Runa marks the permitted boundary on a map, small healed brow cut and left-arm bruise remain.", "Ilyan:Ainda não sabemos de onde vieram os cortadores.|Runa:Então vamos marcar só o que vimos.", "courtyard-conversation"),
]

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reader/medieval/arc5-555-604.json"
CHAPTERS = [
    {"title": "A licença e o caminho", "start": 555, "end": 566},
    {"title": "A rua baixa", "start": 567, "end": 582},
    {"title": "A vigília do dique", "start": 583, "end": 596},
    {"title": "O marco das Faias", "start": 597, "end": 604},
]


def make_line(part: str, side: int) -> dict:
    speaker, text = part.split(":", 1)
    if side == 0:
        box = {"x": 5, "y": 2, "w": 39, "target_x": 29, "target_y": 23}
    else:
        box = {"x": 56, "y": 2, "w": 39, "target_x": 72, "target_y": 23}
    if text.endswith("!"):
        box["kind"] = "shout"
    return {"speaker": speaker, "text": text, "balloon": box}


pages = []
for number, title, time, place, cast, scene, dialogue, layout in ROWS:
    lines = [make_line(part, i) for i, part in enumerate(dialogue.split("|"))]
    pages.append({
        "number": number, "title": title, "time": time, "place": place,
        "layout": layout, "cast": cast.split(","), "novel_chapter": 32,
        "scene": scene, "lines": lines,
    })

# Set the tails after inspecting the finished upper panels. The anchor is a
# visible speaker, never an inferred face in a later panel.
TAILS = {
    555: [(17, 26), (51, 27)],
    556: [(52, 30), (78, 30)],
    557: [(25, 31), (77, 39)],
    558: [(17, 26), (83, 26)],
    559: [(34, 36), (82, 38)],
    560: [(18, 28)],
    561: [(23, 27), (79, 27)],
    562: [(39, 28)],
    563: [(23, 27), (77, 28)],
    564: [(27, 28)],
    565: [(26, 28), (71, 28)],
    566: [(22, 30)],
    567: [(24, 30), (69, 30)],
    568: [(51, 28), (79, 28)],
    569: [(25, 24)],
    570: [(30, 30)],
    571: [(46, 30)],
    572: [(22, 28)],
    573: [(68, 28)],
    574: [(24, 27)],
    575: [(40, 28)],
    576: [(25, 30), (73, 28)],
    577: [(20, 28), (72, 28)],
    578: [(25, 30), (72, 29)],
    579: [(24, 30), (75, 30)],
    580: [(27, 29)],
    581: [(54, 29), (27, 29)],
    582: [(28, 28)],
    583: [(27, 28)],
    584: [(23, 28), (73, 28)],
    585: [(25, 30), (70, 30)],
    586: [(28, 30)],
    587: [(23, 30), (70, 30)],
    588: [(30, 29), (69, 29)],
    589: [(45, 28)],
    590: [(27, 29), (72, 29)],
    591: [(26, 29)],
    592: [(28, 31), (72, 30)],
    593: [(25, 19), (50, 20)],
    594: [(28, 29)],
    595: [(25, 29)],
    596: [(50, 29)],
    597: [(54, 28)],
    598: [(26, 28), (73, 28)],
    599: [(76, 28)],
    600: [(25, 28), (72, 28)],
    601: [(25, 28), (65, 28)],
    602: [(53, 28)],
    603: [(52, 27), (76, 27)],
    604: [(26, 28), (73, 28)],
}
for page in pages:
    for line, anchor in zip(page["lines"], TAILS.get(page["number"], [])):
        line["balloon"]["target_x"], line["balloon"]["target_y"] = anchor

BOXES = {
    566: [(71, 85, 28)],
    567: [(62, 4, 34), (5, 25, 35)],
    569: [(5, 25, 36)],
    573: [(55, 2, 39)],
    596: [(34, 2, 39)],
    597: [(41, 2, 39)],
    599: [(55, 2, 39)],
    602: [(34, 2, 39)],
    603: [(27, 10, 32), (64, 10, 32)],
    591: [(61, 2, 34)],
}
for page in pages:
    for line, box in zip(page["lines"], BOXES.get(page["number"], [])):
        line["balloon"]["x"], line["balloon"]["y"], line["balloon"]["w"] = box

TAILS.update({
    566: [(85, 76)],
    567: [(43, 17), (18, 14)],
    569: [(22, 14)],
    591: [(34, 14)],
})
for page in pages:
    for line, anchor in zip(page["lines"], TAILS.get(page["number"], [])):
        line["balloon"]["target_x"], line["balloon"]["target_y"] = anchor

assert [p["number"] for p in pages] == list(range(555, 605))
OUT.write_text(json.dumps({"chapters": CHAPTERS, "pages": pages}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(OUT, len(pages))
