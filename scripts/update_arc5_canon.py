"""Record the chapter-32 route and fixed geography in the medieval canon."""

import json
from pathlib import Path

path = Path(__file__).resolve().parents[1] / "reader/medieval/canon.json"
canon = json.loads(path.read_text(encoding="utf-8"))
canon["school_map"].update({
    "patio-leste": "Pátio de treino a leste da piscina central, com tábua de rotas e acesso à cerca norte de arquearia. O grupo sai daqui pelo portão sul.",
    "cerca-norte": "Área de tiro segura atrás da cerca ao norte do pátio leste; alvos de corda e estacas ficam afastados da circulação.",
})
canon["places"].update({
    "cais-leste": "Cais a leste de Valecobre; barca comum para a margem da Enseada. O tripé pesado exige duas travessias para seis viajantes e equipamento.",
    "barca-enseada": "Barca baixa de madeira que atravessa a água entre o cais leste e a margem oposta, sem teleporte nem atalho.",
    "estrada-enseada": "Caminho público da margem da Enseada até o corredor concedido para vistoria da eclusa exterior.",
    "ponte-enseada": "Ponte de pedra junto à faixa baixa da Enseada, com marcas de nível. A marca baixa aciona aviso preventivo.",
    "rua-baixa": "Rua sazonal de casas junto à ponte da Enseada; a calçada leste afunda perto do bueiro durante a cheia. A saída segura sobe pelo quintal alto.",
    "vala-enseada": "Vala entre o capim e a rua baixa; abrigo natural dos cortadores de lodo deslocados pela cheia.",
    "quintal-alto": "Quintal de pedra acima da rua baixa. Poste sólido segura a corda de travessia; o degrau de pedra pode ceder depois da retirada da família.",
    "dique-seguro": "Topo firme do dique junto à Enseada. Uma barreira de tábuas de carrinho protege a fila; arcos operam sem apontar para moradores.",
    "posto-dique": "Abrigo de observação no alto do dique, com sino, lanterna, livro de horários e leitura de nível a cada sino.",
    "borda-norte": "Margem rochosa observável somente com licença das Faias e Talin presente. O marco de pedra proíbe cruzar, escavar ou tocar a junta antiga.",
})
timeline_entry = (
    "HQ, arco 5, dias 460–464: páginas 555–604 adaptam o capítulo 32. Adra traz consentimento da Enseada "
    "para medir a eclusa exterior e retirar moradores da faixa baixa; Eda limita a missão ao corredor autorizado. "
    "Runa repousa, Líria está suspensa. Sere, Ilyan, Caio, Adra e dois trabalhadores vão a pé pelo portão sul e "
    "Valecobre, cruzam em duas viagens de barca e chegam ao dique. Cortadores de lodo deslocados pela cheia "
    "ameaçam a retirada; Ilyan usa a espada sem fio como defesa e a corda evita sua queda. Caio recebe corte "
    "superficial que é lavado. Medições noturnas sugerem duas entradas de água. Talin traz licença restrita "
    "para observar a borda norte, sem tocar a junta. Voltam no dia 464 sem atribuir autoria à haste vista."
)
if timeline_entry not in canon["timeline"]:
    canon["timeline"].append(timeline_entry)
path.write_text(json.dumps(canon, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
