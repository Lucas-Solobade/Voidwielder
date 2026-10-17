"""Arc-four coda, planned from chapter 30 and the established page-502 state."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# title | time | place | layout | cast | visible action | first speaker/text | second speaker/text
BEATS = [
    ("Três condições", "Dia 454 · tarde", "casa-das-quatro-luas-conselho", "wide", "eda,adra", "Eda holds the numbered council minutes while Adra points to three distinct conditions on a blank route map; no signatures have been invented.", "Eda", "Sem convite dos guardiões, não passamos da pedra.", "Adra", "E ninguém publica a voz de um morador sem permissão."),
    ("O custo escrito", "Dia 454 · tarde", "casa-das-quatro-luas-conselho", "split", "tovo,ordelia", "Tovo and Ordelia compare food and ferry costs in the House expense ledger, seated on opposite sides of the oak council table.", "Tovo", "A balsa e a comida precisam entrar na conta.", "Ordelia", "Cada turno terá custo e responsável anotados."),
    ("Mãos para a tarefa", "Dia 454 · tarde", "casa-das-quatro-luas-conselho", "asymmetric", "ilyan,runa", "Ilyan indicates the east-forge shift on a timetable; Runa indicates supervised map-copy training on a separate sheet.", "Ilyan", "Posso assumir turnos na forja.", "Runa", "E eu ensino cópias sem tirar os originais do arquivo."),
    ("Resposta lacrada", "Dia 455 · manhã", "biblioteca-galeria", "stack", "ordelia,eda", "A real messenger has delivered Maelor's sealed preliminary reply; Ordelia opens it at the public archive desk with Eda present, documents in their hands.", "Ordelia", "A carta chegou hoje. Os anexos ainda não vieram.", "Eda", "Registro o recebimento e cobro os livros prometidos."),
    ("Três frases diferentes", "Dia 455 · manhã", "biblioteca-galeria", "wide", "runa,ilyan", "Runa lays three separate note cards by the archive desk: proven payment, denied personal interest, unknown final destination; Ilyan studies them.", "Runa", "Pagamento confirmado. Interesse negado. Destino desconhecido.", "Ilyan", "Não vou chamar a terceira frase de prova sobre Mira."),
    ("A linha que falta", "Dia 455 · tarde", "biblioteca-galeria", "split", "ilyan,eda", "Ilyan points at Mira's earlier dated plan while Eda marks the unanswered link between that plan and later sales in the public work ledger.", "Ilyan", "O mapa dela veio antes das compras.", "Eda", "Então precisamos do procurador e dos anexos; não de um palpite."),
    ("O caminho da ala oeste", "Dia 455 · anoitecer", "patio-central", "asymmetric", "runa,ilyan", "Runa and Ilyan walk physically from the central reflecting pool along the west limestone path toward the established dormitory building at sunset.", "Runa", "O dia acabou. Posso caminhar com você?", "Ilyan", "Até meu quarto. Queria ficar mais um pouco ao seu lado."),
    ("Uma escolha dita em voz alta", "Dia 455 · noite", "dormitorio-cedro", "wide", "ilyan,runa", "Inside Ilyan's established single dorm room: narrow bed under north window, cedar trunk and dull training sword beside it. Both adults stand apart at first, making room for an explicit mutual invitation.", "Ilyan", "Você quer ficar? Quero ter certeza.", "Runa", "Quero. E quero que me diga se algo não estiver bem."),
    ("Mais perto", "Dia 455 · noite", "dormitorio-cedro", "split", "runa,ilyan", "The two adults share an unhurried consensual kiss beside the cedar trunk; Ilyan's vest and Runa's outer coat are neatly folded on the trunk, both still wearing opaque medieval underlayers.", "Runa", "Agora não há ninguém nos interrompendo.", "Ilyan", "Então posso beijar você sem pressa?"),
    ("A lamparina baixa", "Dia 455 · noite", "dormitorio-cedro", "asymmetric", "runa,ilyan", "Warm lamplight: Ilyan and Runa embrace on the edge of the narrow bed, fully covered from shoulders downward by an ivory quilt, their faces close and anatomically natural; a smaller inset shows the lamp being lowered. No nudity or explicit act.", "Runa", "Fica comigo esta noite.", "Ilyan", "Fico. Se você também quiser, a cada passo."),
    ("Antes da manhã", "Dia 455 · noite", "dormitorio-cedro", "wide", "runa,ilyan", "Quiet aftermath of their consensual first night together: two adult silhouettes under one quilt below the north window, only faces and shoulders visible in soft moonlight; no graphic intimacy, one sleeping lamp on the table.", "Runa", "Ainda está acordado?", "Ilyan", "Estou. E estou feliz por estar aqui com você."),
    ("A luz do norte", "Dia 456 · manhã", "dormitorio-cedro", "stack", "runa,ilyan", "Morning in the same room and same bed: both young adults sit upright wrapped in the quilt, hair and fixed facial traits intact, looking toward the north window; sword remains safely beside the cedar trunk.", "Runa", "Bom dia. Não quero fingir que ontem não mudou nada.", "Ilyan", "Mudou. Mas nós ainda escolhemos o próximo passo."),
    ("Sem promessas fáceis", "Dia 456 · manhã", "dormitorio-cedro", "split", "runa,ilyan", "Now fully dressed in established clothes, Runa and Ilyan talk by the north window, with respectful space between them; her left-arm floral tattoo and silver septum visible.", "Runa", "Gosto de você. E do meu próprio trabalho.", "Ilyan", "Não vou pedir que abandone nenhum dos dois."),
    ("Dois turnos", "Dia 456 · manhã", "patio-central", "asymmetric", "ilyan,runa", "The two adults exit the west dormitory along the same limestone path; Ilyan turns toward the east forge, Runa toward the northeastern library, both visibly carrying their separate work tools.", "Ilyan", "Vou para a forja. Nos vemos na mesa de cópias?", "Runa", "Depois do meu turno. Sem atalhos no mapa."),
    ("A verificação", "Dia 456 · tarde", "casa-das-quatro-luas-conselho", "split", "eda,adra", "Eda shows Adra the numbered reply, blank space for its missing accounting attachments, and formal independent verification request at the oak council table.", "Eda", "Maelor negou lucro próprio. Ainda deve os anexos.", "Adra", "A ata distingue resposta e prova."),
    ("Cada margem responde", "Dia 456 · tarde", "casa-das-quatro-luas-conselho", "wide", "adra,ilyan", "Adra seals two ordinary messenger packets for the Enseada and the Faias on the council table; Ilyan stands by the unfinished western salt-mirror map, with no new road line inked.", "Adra", "As cartas pedem decisão às comunidades.", "Ilyan", "A estrada espera. Nenhuma margem será apagada por nós."),
]

SPEAKERS = {"ilyan": "Ilyan", "runa": "Runa", "eda": "Eda", "adra": "Adra", "tovo": "Tovo", "ordelia": "Ordelia"}
assert len(BEATS) == 16


def balloon(index):
    x = 4 if index == 0 else 55
    target_x = 26 if index == 0 else 76
    return {"x": x, "y": 10, "w": 40, "target_x": target_x, "target_y": 35}


pages = []
for number, beat in enumerate(BEATS, 503):
    title, time, place, layout, cast, scene, speaker_a, text_a, speaker_b, text_b = beat
    assert speaker_a in SPEAKERS.values() and speaker_b in SPEAKERS.values()
    ids = cast.split(",")
    assert {speaker_a, speaker_b}.issubset({SPEAKERS[i] for i in ids})
    pages.append({
        "number": number, "title": title, "time": time, "place": place,
        "layout": layout, "cast": ids, "scene": scene, "novel_chapter": 30,
        "lines": [
            {"speaker": speaker_a, "text": text_a, "balloon": balloon(0)},
            {"speaker": speaker_b, "text": text_b, "balloon": balloon(1)},
        ],
    })

# A silent kiss is stronger than speech laid over faces. Two generated pages
# include their own empty, correctly aimed bubbles; place accessible text
# inside those shapes instead of drawing duplicates or extra tails.
pages[511 - 503]["lines"] = []
pages[513 - 503]["narration"] = "Passaram a noite juntos. A porta guardou o que pertencia somente aos dois."
for page in pages:
    for line in page["lines"]:
        line["balloon"]["y"] = 4
for number, geometry in {
    515: ((7, 3, 31), (50, 3, 41)),
    517: ((13, 3, 28), (61, 3, 30)),
}.items():
    for line, (x, y, w) in zip(pages[number - 503]["lines"], geometry):
        line["balloon"].update(x=x, y=y, w=w, embedded=True)

path = ROOT / "reader/medieval/arc4-503-518.json"
path.write_text(json.dumps({"chapters": [{"title": "Cada margem responde", "start": 503, "end": 518}], "pages": pages}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(path)
