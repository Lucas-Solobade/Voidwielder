"""Storyboard for arc four, pages 451–502. Dialogue is intentionally primary."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# title || scene with physical action || speaker || speech || speaker || speech
BEATS = """
O preço do pomar||Ilyan points to the old and new sale prices in the municipal ledger; the female clerk keeps the original open on her desk.||Ilyan||O pomar caiu para menos da metade.||Escrivã||A venda e o aviso têm datas nesta folha.
Uma semana||Runa lays the official risk notice beside the sale entry, keeping both documents within the clerk's view.||Runa||O aviso chegou na semana da venda.||Ilyan||Isso levanta uma pergunta. Ainda não responde quem o enviou.
Escalas diferentes||Runa aligns three paper maps by their printed scale bars on the municipal table; Ilyan watches.||Runa||Se eu alinhar pelas bordas, a saída do rio some.||Ilyan||Então marca a escala antes de copiar a curva.
A oficina ausente||Runa points to the empty area on the new municipal plan where the old plan showed the oar workshop; Adra compares.||Runa||Na planta nova, deixaram esse espaço em branco.||Adra||A oficina da Enseada ficava exatamente aqui.
A vala permanente||Runa compares the older seasonal outlet and newer permanent ditch on two plans; Adra traces the path without touching the originals.||Runa||O curso sazonal virou vala permanente no papel.||Adra||E o aviso de risco chegou antes aos compradores.
Nome de sociedade||Ilyan reads the salt company's purchase document while the clerk turns an authorized page.||Ilyan||A compradora é uma sociedade de sal.||Escrivã||Copie o nome inteiro, não apenas a marca.
O mesmo procurador||Runa and Adra compare the signatures on the bridge finance contract and salt company purchase.||Runa||O selo reaparece aqui. Ainda não é culpa provada.||Adra||Mas o mesmo procurador assinou os dois contratos.
Uma folha numerada||The female municipal clerk stamps the page sequence while Ilyan writes the folio number in his notebook.||Escrivã||Fólio cento e doze. A cópia cita esta origem.||Ilyan||E o original permanece com vocês.
O prazo da mesa||The female municipal clerk closes the ledger gently at the scheduled end of consultation while Ilyan has one unfinished line.||Escrivã||O turno terminou. Há outra consulta agora.||Ilyan||Voltaremos amanhã para completar a transcrição.
No corredor||Eda joins Ilyan in the stone corridor outside the municipal archive, holding the registered petition.||Ilyan||Podem esconder a verdade enquanto esperamos.||Eda||Uma prova sem registro seria fácil de contestar.
O canto do selo||Runa shows Ilyan two copied seal impressions; one squared edge appears broken.||Runa||Veja este canto: a matriz não parece igual.||Ilyan||Ou a impressão saiu falha. Precisamos examinar a cera.
Pedido de exame||Eda submits a written request to the female clerk for two independent wax drawings.||Eda||Duas cópias independentes e exame da cera, por favor.||Escrivã||Registrarei o pedido. Nada sai desta sala sem recibo.
Caminho à margem||Adra and Runa walk a marked public road from Valecobre toward the old orchard and the dry outlet, carrying copied maps.||Adra||Hessa aceitou nos receber no pomar.||Runa||Vamos ouvir antes de completar o mapa.
Hessa do pomar||Hessa, a adult orc orchard worker, welcomes Adra at the orchard gate near trimmed trees.||Hessa||Vendi o pomar. A escolha foi minha.||Adra||Quero registrar por que a escolha pareceu necessária.
Duas colheitas||Hessa shows Ilyan bare branches and her brother's treatment receipt on a workbench.||Hessa||Foram duas colheitas ruins. Meu irmão precisava de tratamento.||Ilyan||Vou registrar as duas razões, sem reduzir sua decisão.
O preço inteiro||Hessa and Ilyan sit at the orchard table while he prepares a transcript.||Hessa||Anote também o preço que consegui.||Ilyan||Ninguém vai resumir você como alguém que não soube negociar.
O rio que não mostraram||Runa unfolds the old seasonal waterway map for Hessa; she recognizes the stream boundary.||Runa||Esta saída sazonal existia na planta antiga.||Hessa||Se a tivessem mostrado, eu teria negociado diferente.
Uma recusa||Adra speaks with an unnamed resident from the public roadside; the resident remains behind a half-door, face partly in shadow.||Moradora||Não quero meu nome numa acusação.||Adra||Entendo. Não publicaremos seu depoimento.
Casa habitada||Adra and Runa mark the refused family's occupied house on their field map without a name.||Adra||Ela recusou falar. A casa continua habitada.||Runa||E permanece no mapa, sem inventarmos testemunho.
Carta de Líria||At the Valecobre lodging, Runa opens a delayed ordinary letter from Liria; Ilyan reads beside her.||Runa||Líria enviou a análise da terra das Faias.||Ilyan||A amostra chegou com o método registrado?
Sedimento deslocado||Runa sketches Liria's sediment layers beside a small labeled soil sample; Ilyan studies the sketch.||Runa||Há água de montante onde a corrente natural não a deixaria.||Ilyan||Isso indica intervenção. Não quem a fez.
A ressalva de Oru||Adra and Runa read the second page of the analysis with Oru's signed methodological caution.||Adra||Oru confirmou o método, mas não a data.||Runa||Essa ressalva vai junto com a descoberta.
Resposta à rival||Runa writes a short thank-you and request for duplicate samples; Ilyan watches from the other side of the desk.||Ilyan||Você vai agradecer à Líria?||Runa||Pelo dado útil, sim. Nossa rivalidade não desapareceu.
A corrente de latão||Ilyan notices the brass-chain sketch on Liria's letter while Runa closes the folder.||Ilyan||Ela ainda prende o caderno àquela corrente.||Runa||Continua sendo ela. Isso me ajuda a confiar na autoria.
Segunda consulta||On the next morning, the clerk receives Eda at the municipal archive; Maelor arrives alone behind them.||Escrivã||A consulta de hoje está registrada.||Eda||E as comunidades receberão cópias do que for encontrado.
Obras antes das chuvas||Maelor politely faces Eda across the archive desk, dark green coat and copper square ring visible.||Maelor||O vale precisa da obra antes das próximas chuvas.||Eda||E precisa de um laudo que resista à leitura pública.
Quem morou ali||Maelor points at Runa's copied map while Adra steps forward from the group.||Maelor||Alguém daqui morou junto à saída do rio?||Adra||Eu morei. Durante anos.
O nome de Adra||Adra stands squarely before Maelor in the municipal room; he retreats a small step, without melodrama.||Adra||Adra da Enseada das Conchas. Anote meu nome.||Maelor||Seu conhecimento local ficará registrado.
O mapa e a pessoa||Runa and Eda confer by the archive window after Maelor's comment about seasonal occupation.||Runa||Ele tratou a moradia como erro de mapa.||Eda||A experiência de Adra é dado, não ruído.
Livro de remessas||The female clerk turns to a payment entry in the separate remittance ledger; Ilyan copies its folio number.||Escrivã||Aqui: pagamento do levantamento ao gabinete.||Ilyan||Quem assinou a entrega do trabalho?
Equipe de campo||Ilyan and Runa compare the fee against the described survey team on a copied sheet.||Ilyan||O valor cobriria uma equipe de medição.||Runa||Mas ainda não diz para onde foi cada moeda.
Recibo que falta||Eda and the female clerk inspect an empty receipt field in the municipal remittance index.||Eda||Não encontro o recibo de entrega.||Escrivã||Fica em outro livro. A consulta exige novo pedido.
Dez dias||Eda writes the formal request for independent accounting while Adra watches.||Eda||Peço verificação independente. O prazo é de dez dias.||Adra||Então levamos as cópias às comunidades enquanto esperamos.
Duas margens||Adra and Eda make two sealed copy packets on the archive table, one for each affected community.||Adra||Uma cópia vai à Enseada; outra, às Faias.||Eda||O protocolo terá dois destinatários.
Antes das compras||Ilyan points to the date on Mira's old plan beside Runa's note of the later purchases.||Ilyan||O mapa de minha mãe é anterior às vendas.||Runa||Isso separa a obra antiga das compras recentes.
Linha sem resposta||Ilyan leaves a blank line in his notebook while Runa puts down the map carefully.||Ilyan||Por que alteraram uma cópia do traçado dela?||Runa||Ainda não temos o elo. Deixe a pergunta aberta.
A régua devolvida||At their modest shared lodging, Runa returns Ilyan's brass ruler; door visibly ajar, Caio absent on outdoor cargo guard.||Runa||Você acha que a Casa vai se calar?||Ilyan||Temo que prefira parecer infalível.
Ficar um instante||Two-panel progression in the half-open lodging room: Ilyan and Runa agree to stay close, then share a consensual kiss in a small lower inset; both are adults, fully clothed.||Ilyan||Pode ficar mais um instante?||Runa||Posso. E quero.
Passos na escada||Runa and Ilyan step apart smiling as Caio's footsteps sound from the stair; no explicit content.||Runa||Caio voltou da ronda.||Ilyan||Então amanhã, café antes da consulta?
Café antes de tudo||Next morning at a small lodging breakfast table, Runa and Ilyan exchange a quiet smile over bread and maps.||Runa||Café primeiro. Depois, mais números.||Ilyan||Combinado. E eu carrego as cópias.
As cópias na Casa||At the House of Four Moons archive, Ordelia receives the registered packets from Adra.||Ordelia||Recebo as cópias, com origem e limite de uso.||Adra||Hessa ainda precisa conferir o próprio depoimento.
As duas palavras||Days later, Adra shows Ordelia Hessa's corrected transcript returned by ordinary messenger, two words visibly amended.||Adra||Ela trocou duas palavras que mudavam o sentido.||Ordelia||A versão corrigida substituirá a anterior no resumo.
Três colunas||Ordelia and Runa lay out a public provisional summary with three labeled columns, at the school's archive table.||Ordelia||Observado, hipótese, falta testar.||Runa||E nenhuma pista atravessa as colunas sem prova.
Crédito a Nima||Ilyan checks a line crediting Nima of Pedra-Mansa for the eight-tooth mechanism suggestion; Ordelia stamps the letter to be sent.||Ilyan||O mecanismo de oito dentes leva o nome de Nima.||Ordelia||A cópia seguirá a ela pelo correio comum.
O testemunho de Braka||Adra and Ilyan review the public summary of Braka's sluice testimony by the school's map wall.||Adra||Braka aceitou publicar o que viu na comporta.||Ilyan||Isso mostra um padrão, sem inventar um autor único.
A contestação||Eda and Runa read Maelor's formal objection to the provisional report; the stamped document is plainly a letter, not a person in the room.||Eda||Maelor contestou a publicação.||Runa||Mas não negou os números de registro.
Quem paga a estrada||Tovo and Ordelia inspect the House's travel ledger and open expenses at the council table.||Tovo||Outra viagem precisa de transporte e refeições. Quem paga?||Ordelia||Vamos propor turnos e treino de copistas, com custo anotado.
Notícia do espelho||Adra and Runa open Talin's delivered letter about a proposed cart road to the shallow salt mirror west of the Faias.||Adra||Querem abrir via de carroças até o espelho de sal.||Runa||Isso mudaria a saída sazonal outra vez.
Sem pedido aos guardiões||Adra and Eda compare the letter with the public register of permissions at the council table.||Adra||Ysra diz que não receberam pedido de passagem.||Eda||Sem consentimento, não há vistoria além da pedra.
O recibo esperado||On the tenth day, Eda and the clerk at the municipal desk inspect a newly obtained accounting receipt with two signatures and an unknown rubric.||Eda||Vejo duas assinaturas válidas e uma rubrica por identificar.||Escrivã||Vou registrar essa distinção no protocolo.
O conflito||Eda and Adra address the House council, displaying the accounting receipt and purchase record.||Eda||Há vínculo financeiro que exige investigação formal.||Adra||Não prova quem armou o cervo nem quem cortou o sino.
Uma estrada por desenhar||Ilyan and Runa stand by the House's map wall, looking toward the western salt mirror route with a blank line for Mira.||Ilyan||Quero respostas sobre Mira, mas não vou inventá-las.||Runa||Então escutamos quem vive na margem antes de desenhar a estrada.
""".strip().splitlines()

assert len(BEATS) == 52, len(BEATS)


def page_time(number):
    if number <= 459:
        return "Dia 442 · manhã"
    if number <= 462:
        return "Dia 442 · meio-dia"
    if number <= 469:
        return "Dia 442 · tarde"
    if number <= 474:
        return "Dia 442 · noite"
    if number <= 486:
        return "Dia 443 · consulta"
    if number <= 489:
        return "Dia 443 · noite"
    if number == 490:
        return "Dia 444 · manhã"
    if number == 491:
        return "Dia 444 · tarde"
    if number <= 494:
        return "Dia 447–449 · arquivo da Casa"
    if number <= 497:
        return "Dia 450 · conselho"
    if number <= 499:
        return "Dia 451 · notícias do oeste"
    if number == 500:
        return "Dia 453 · décimo dia"
    return "Dia 454 · conselho"


def page_place(number):
    if number <= 459 or 475 <= number <= 486 or number == 500:
        return "arquivo-municipal-valecobre"
    if number <= 462:
        return "corredor-arquivo-municipal"
    if number <= 469:
        return "pomar-canal-seco"
    if number <= 474 or number <= 490:
        return "hospedaria-valecobre"
    return "casa-das-quatro-luas"


SPEAKERS = {
    "Ilyan": "ilyan", "Runa": "runa", "Adra": "adra", "Eda": "eda",
    "Hessa": "hessa", "Maelor": "maelor", "Ordelia": "ordelia",
    "Tovo": "tovo", "Escrivã municipal": "escriva-municipal",
    "Escrivão municipal": "escrivao-municipal", "Moradora da margem": "moradora-pomar",
}


def balloon(layout, index):
    # Two character-led balloons; all coordinates refer to the whole page image.
    variants = {
        "split": ((4, 10, 40, 24, 34), (55, 10, 40, 76, 34)),
        "stack": ((4, 10, 42, 25, 34), (55, 10, 41, 77, 34)),
        "asymmetric": ((5, 10, 41, 26, 34), (54, 10, 41, 76, 34)),
        "wide": ((4, 10, 41, 25, 34), (55, 10, 40, 76, 34)),
    }
    x, y, w, tx, ty = variants[layout][index]
    return {"x": x, "y": y, "w": w, "target_x": tx, "target_y": ty}


pages = []
layouts = ("split", "stack", "asymmetric", "wide")
for number, row in enumerate(BEATS, 451):
    title, scene, speaker_a, text_a, speaker_b, text_b = row.split("||")
    display_names = {
        "Escrivã": "Escrivã municipal",
        "Escrivão": "Escrivão municipal",
        "Moradora": "Moradora da margem",
    }
    speaker_a = display_names.get(speaker_a, speaker_a)
    speaker_b = display_names.get(speaker_b, speaker_b)
    layout = layouts[(number - 451) % len(layouts)]
    pages.append({
        "number": number,
        "title": title,
        "time": page_time(number),
        "place": page_place(number),
        "layout": layout,
        "cast": list(dict.fromkeys((SPEAKERS[speaker_a], SPEAKERS[speaker_b]))),
        "scene": scene,
        "novel_chapter": 30,
        "lines": [
            {"speaker": speaker_a, "text": text_a, "balloon": balloon(layout, 0)},
            {"speaker": speaker_b, "text": text_b, "balloon": balloon(layout, 1)},
        ],
    })

# The first finished illustration was inspected at full size. Its clerk sits
# lower than Ilyan, so place each balloon in the actual empty architecture.
pages[0]["lines"][0]["balloon"] = {"x": 4, "y": 9, "w": 40, "target_x": 33, "target_y": 34}
pages[0]["lines"][1]["balloon"] = {"x": 55, "y": 10, "w": 40, "target_x": 79, "target_y": 41}
pages[1]["lines"][0]["balloon"] = {"x": 4, "y": 9, "w": 40, "target_x": 34, "target_y": 38}
pages[1]["lines"][1]["balloon"] = {"x": 55, "y": 9, "w": 40, "target_x": 72, "target_y": 37}
pages[2]["lines"][0]["balloon"] = {"x": 4, "y": 9, "w": 40, "target_x": 30, "target_y": 38}
pages[2]["lines"][1]["balloon"] = {"x": 55, "y": 9, "w": 40, "target_x": 72, "target_y": 38}
# The generated compositions put Runa on the left and Adra on the right.
for index in (3, 6):  # pages 454 and 457
    pages[index]["lines"][0]["balloon"] = {"x": 4, "y": 10, "w": 40, "target_x": 28, "target_y": 39}
    pages[index]["lines"][1]["balloon"] = {"x": 55, "y": 10, "w": 40, "target_x": 72, "target_y": 39}
# Page 456 has both speakers in the upper split scene.
pages[5]["lines"][1]["balloon"] = {"x": 55, "y": 10, "w": 40, "target_x": 77, "target_y": 42}
# Orchard closeups rise toward the top margin; lift the bubbles clear of hair.
for index in (16, 17):  # pages 467 and 468
    for line in pages[index]["lines"]:
        line["balloon"]["y"] = 5
# The late archive map and lodging illustrations reserve more room above the
# speakers. Keep the balloons close to the first visible faces without crossing
# a panel border or covering their hair.
for number in (485, 486):
    for line in pages[number - 451]["lines"]:
        line["balloon"]["y"] = 15
for number in (487, 488, 489):
    for line in pages[number - 451]["lines"]:
        line["balloon"]["y"] = 18
for number in range(490, 503):
    for line in pages[number - 451]["lines"]:
        line["balloon"]["y"] = 17

output = ROOT / "reader" / "medieval" / "arc4-451-502.json"
output.write_text(json.dumps({"chapters": [{"title": "O espelho de sal", "start": 450, "end": 502}], "pages": pages}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Wrote {len(pages)} pages to {output}")
