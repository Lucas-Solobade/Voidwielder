"""Close the sixth comic arc with the established last novel chapter."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "reader/medieval/arc6-925-940.json"

# Number | title | day | place | cast in left-to-right order | visual action |
# left speaker | line | right speaker | line. Each action follows volume II,
# chapter 6; the private receipt is not treated as independent proof.
BEATS = """925|A placa na mesa|Dia 525 · fim da tarde|casa-arquivos|hessa,ordelia|Hessa places the numbered copper tariff plate beside her father's private receipt; Ordelia writes its serial without stamping it authentic yet.|Hessa|Esta placa ficou guardada com o recibo.|Ordelia|A sequência deve aparecer em outro livro.
926|O livro da Enseada|Dia 526 · manhã|casa-arquivos|pim,hessa|Adult gnome Pim arrives from the Enseada carrying the independently kept public tariff ledger; Hessa watches him open the bound volume.|Pim|Trouxe o livro do conselho. Não saiu de lá antes de hoje.|Hessa|Procure a tarifa de meu pai pelo número.
927|Dois registros|Dia 526 · manhã, depois|casa-arquivos|ordelia,runa|Ordelia and Runa match serial and salt fee in the two separate records; a small visual inset shows Pim's rope-knot sketch made before seeing Mira's old drawing.|Ordelia|Número e valor conferem em livros de guarda diferente.|Runa|O nó também foi desenhado sem olhar o caderno.
928|A estação da casca|Dia 526 · meio-dia|casa-arquivos|neral,ysra|Neral and Ysra enter with the ORIGINAL bark strip and sealed glass case; Neral points to three seasonal marks beside an independent human calendar.|Neral|Esta marca é do inverno seguinte à partida dela.|Ysra|O conselho preservou a tira original.
929|Lacres e testemunhas|Dia 526 · meio-dia, depois|casa-arquivos|eda,ordelia|Eda and Ordelia log both seals and custody witnesses before opening the sealed glass case on the archive desk; others remain secondary, no one touches the letter yet.|Eda|Registre quem trouxe, quem recebeu e cada lacre.|Ordelia|Só abriremos diante das testemunhas.
930|A folha de Mira|Dia 526 · tarde|casa-arquivos|ilyan,runa|Ilyan and Runa witness the opened letter under a mundane oil lamp; the script is decorative and illegible, the glass case and broken old wax are visible.|Ilyan|É a letra dela. Ainda precisamos do resto.|Runa|A marca da forja aparece aqui, por dentro.
931|A dívida de água|Dia 526 · tarde, continuidade|casa-arquivos|adra,ilyan|Adra and Ilyan read the page explaining the old counterweights and inhabitants of both margins; a small inset shows salt wall and reed village, no new portal.|Adra|Ela não queria entregar a rota a um único gabinete.|Ilyan|Porque a passagem atravessa casas habitadas.
932|O que não prometeu|Dia 526 · tarde, continuidade|casa-arquivos|ilyan,ordelia|Ilyan reads his mother's final paragraph while Ordelia keeps the original letter on the table, weighing the grief rather than celebrating a solved disappearance.|Ilyan|Ela não prometeu voltar. Só pediu que eu soubesse por quê.|Ordelia|A folha prova uma data. Não o lugar dela hoje.
933|Um corredor inteiro|Dia 526 · entardecer|casa-arquivos|ilyan,runa|Ilyan has walked physically into the archive corridor to breathe; Runa joins only after he beckons and keeps respectful space.|Ilyan|Quero procurá-la. Também quero falar com meu pai.|Runa|Nenhuma das duas escolhas precisa ser hoje.
934|Quatro maneiras de falhar|Dia 526 · fim da tarde|sala-elementos|caio,tovo|Caio and Tovo give separate bridge testimony before Oru and a classroom diagram: redirected air failed; muscle surge hurt Tovo's shoulder; the teacher listens.|Caio|Inverti o ar e quase levei o frio à ponte.|Tovo|Segurei a travessa até o ombro mandar parar.
935|A fratura assinada|Dia 526 · noite|casa-arquivos|liria,runa|Líria places her own witnessed fracture sketch in the file, never falsifying it; she and Runa face each other with unresolved hostility and separate workspaces.|Líria|A fissura pode ceder se voltarmos depressa.|Runa|Avisarei Adra. Isso não muda o que houve entre nós.
936|A versão pública|Dia 527 · manhã|casa-conselho-enseada|eda,hessa|Eda presents a public summary with protected map annex; Hessa checks that her inhabited port is named and not presented as ruin; closed folder conceals exact route.|Eda|Publicaremos as provas, não a trilha protegida.|Hessa|Escreva Porto das Cinzas como povoado vivo.
937|Duas cartas|Dia 527 · tarde|casa-arquivos|ilyan,ordelia|Ilyan writes separate ordinary letters to Bram and Nima at the archive desk, with no magical delivery, while Ordelia seals only a certified public excerpt for his father.|Ilyan|Meu pai recebe a cópia autenticada. Nima, só o que posso contar.|Ordelia|As cartas seguirão pelo correio comum.
938|Uma mecha existente|Dia 528 · manhã|forja-leste|ilyan,oru|In the SAME red-brick east forge, Ilyan guides a tiny flame only from existing charcoal to a contained wick, then covers it; Oru watches, water bucket close by.|Ilyan|A chama veio do carvão. A mecha já se apaga.|Oru|Então feche a fonte antes de sair.
939|O aviso da margem|Dia 528 · tarde|casa-arquivos|adra,ordelia|Adra brings the Enseada council's physical written notice that the seam remains closed and watched; Ordelia pins class schedules under it, no secret travel order.|Adra|A costura continua fechada e vigiada.|Ordelia|As aulas retomam. A investigação também.
940|Um lugar sem trilha|Dia 528 · crepúsculo|observatorio-casa|ilyan,runa|Ilyan and Runa sit in the familiar observatory above lit school windows, two warm mugs beside a public map that names the port but leaves protected route blank; quiet arc-ending vista.|Ilyan|Ainda não sei se a perdoo. Mas sei o que perguntar.|Runa|Então começaremos pelas perguntas certas."""


def balloon(speaker: str, text: str, side: int) -> dict:
    return {
        "speaker": speaker,
        "text": text,
        "balloon": {
            "x": 7 if side == 0 else 54,
            "y": 30,
            "w": 39,
            "target_x": 28 if side == 0 else 73,
            "target_y": 47,
            "kind": "normal",
        },
    }


pages = []
for row in BEATS.splitlines():
    number, title, time, place, cast, scene, left, left_line, right, right_line = row.split("|")
    number = int(number)
    pages.append({
        "number": number,
        "title": title,
        "time": time,
        "place": place,
        "cast": cast.split(","),
        "layout": (
            "asymmetric comic panel with a small evidence inset" if number % 4 == 0 else
            "single wide environmental panel with two separated foreground figures" if number % 3 == 0 else
            "two unequal comic panels with a clear establishing view"
        ),
        "scene": scene,
        "novel_volume": 2,
        "novel_chapter": 6,
        "lines": [balloon(left, left_line, 0), balloon(right, right_line, 1)],
    })

assert [page["number"] for page in pages] == list(range(925, 941))
DEST.write_text(json.dumps({
    "chapters": [{"title": "A assinatura depois do inverno", "start": 925, "end": 940}],
    "pages": pages,
}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Wrote {len(pages)} pages to {DEST}")
