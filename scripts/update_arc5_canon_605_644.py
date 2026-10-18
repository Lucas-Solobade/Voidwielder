"""Register the school return, places and limited evidence of pages 605–644."""
import json
from pathlib import Path

path = Path(__file__).resolve().parents[1] / "reader/medieval/canon.json"
canon = json.loads(path.read_text(encoding="utf-8"))
canon["characters"].update({
    "curandeira": {
        "name": "Curandeira", "role": "curandeira da enfermaria leste da Casa",
        "fixed_appearance": "Humana adulta de pele oliva clara, cabelo castanho-escuro preso em coque trançado e olhos castanhos.",
        "fixed_clothing": "Túnica escolar azul-escura com mangas de linho creme; sem insígnia de magia."
    },
    "mensageiro": {
        "name": "Mensageiro", "role": "entregador do correio comum de Valecobre",
        "fixed_appearance": "Humano adulto de pele morena clara, cabelo castanho curto e barba castanha curta.",
        "fixed_clothing": "Capa de viagem castanha e bolsa de couro para cartas; sem uniforme da Casa."
    },
})
canon["school_map"].update({
    "escada-biblioteca": "Escada interna de pedra que sobe da ala leste à galeria superior da biblioteca; Runa sobe por si, Ilyan carrega livros.",
    "galeria-biblioteca": "Galeria superior da biblioteca com mesa de cópias, estantes e portão do arquivo oeste trancado. A mesma mesa recebe séries e mapas.",
    "mesa-patio": "Mesa de pedra ao lado da piscina circular no pátio central; cartas chegam por mensageiro e seguem pelo correio comum.",
    "quarto-cedro": "Quarto individual de Ilyan na ala oeste: baú, lamparina, cama e janela voltada ao norte. A espada sem fio repousa junto ao baú durante a noite.",
    "sala-conselho": "Sala de conselho da Casa: mesa longa de carvalho no centro, mural de mapas na parede oeste, entrada com banco de depoentes; cadeiras extras para representantes.",
    "sala-publica-arquivo": "Sala de consulta pública supervisionada junto à galeria; balcão, lista de remessas e cópias autenticadas. Não dá acesso ao arquivo oeste.",
})
canon["places"].update({
    "posto-correio": "Balcão de correio comum em Valecobre; cartas seladas saem em carroça, nunca por transporte instantâneo."
})
entry = (
    "HQ, arco 5, dias 464–469: páginas 605–644 mostram Ordelia examinando mapas sem atribuir culpa; Runa recupera-se "
    "e treina impulso limitado à água existente sob supervisão de Oru. Líria observa suspensa, propõe exame da soleira "
    "sem ganhar absolvição. Carta de Nima chega por mensageiro de Pedra-Mansa; Ilyan e Runa respondem por correio. "
    "Sere e Caio treinam retirada; Beren entrega peça numerada com licença. Ilyan e Runa aprofundam a relação por "
    "escolha e cuidado. No conselho do dia 469, contas autenticadas ligam a sociedade de sal ao gabinete de Maelor "
    "e à bolsa de Líria, sem provar sabotagem. Líria consulta a cópia pública sob testemunha e entrega a Runa "
    "desenho de ordem que eleva a cota em dois palmos; a rivalidade e a sanção permanecem."
)
if entry not in canon["timeline"]:
    canon["timeline"].append(entry)
path.write_text(json.dumps(canon, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
