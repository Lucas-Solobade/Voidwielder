"""Build the next sequential, book-aligned part of the sixth comic arc."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "reader/medieval/arc6-831-924.json"

# Use the location IDs already fixed by earlier pages whenever a scene returns
# to the same room or courtyard. Only genuinely new Entremeio sites get new IDs.
PLACE_ALIASES = {
    "arquivo-casa": "casa-arquivos",
    "patio-casa": "patio-central",
    "patio-praticas": "patio-treino",
    "enfermaria-casa": "enfermaria-leste",
    "sala-teorica": "sala-elementos",
    "balsa-enseada": "barca-enseada",
}

# Page | title | time | place | visible cast | art beat | speaker | speech | speaker | speech.
# A leading ! is a shout, ~ a thought, and _ a whisper. Each scene places the
# first speaking character on the left and the second on the right.
BEATS = """831|A cópia numerada|Dia 500 · manhã|arquivo-casa|runa,ordelia|Runa and Ordelia compare Hessa's numbered copy with a separate official rebuttal on the archive desk.|Runa|A cópia de Hessa já recebeu número.|Ordelia|E uma contestação. Vamos ler as duas inteiras.
832|O parecer emprestado|Dia 500 · manhã, depois|arquivo-casa|liria,ordelia|Líria points to her older basalt sample measurements in Maelor's paper while Ordelia checks the small signature of its actual author.|Líria|Medi uma amostra antiga. Nunca toquei a pedra do porto.|Ordelia|Seu nome encobre a conclusão de outra pessoa.
833|Rumores no mural|Dia 500 · meio-dia|patio-casa|caio,ilyan|Caio and Ilyan stand before a school notice board where students gossip without legible text; Ilyan looks troubled.|Caio|Já dizem que Runa inventou o risco.|Ilyan|O documento não diz isso. Vamos à leitura.
834|Leitura pública|Dia 500 · tarde|patio-praticas|ordelia,runa|Ordelia opens the courtyard hearing with two stone replicas on the distant worktable; Runa stands to her right.|Ordelia|Cada uma dirá o que mediu, não o que suspeita.|Runa|Começo pela régua que aparece no desenho.
835|Amostra não é margem|Dia 500 · tarde, minutos depois|patio-praticas|liria,runa|Líria left with two tight braids and chained notebook, Runa right with straight bangs and septum, compare a small dry basalt sample with a port drawing.|Líria|Minha medida veio desta amostra. Não da margem.|Runa|Concordo. Seu resultado não estabiliza a cunha.
836|A régua externa|Dia 500 · tarde, depois|patio-praticas|runa,liria|Runa points to the edge of Adra's drawing without touching Líria's dry sample; Líria studies the scale.|Runa|Esta régua é externa. Não prova quando a pedra se moveu.|Líria|Então precisamos medir lá, no lugar.
837|A ferida antiga|Dia 500 · tarde, logo depois|patio-praticas|liria,runa|Líria glares across the model table, Runa bristles, students out of focus far behind.|Líria|Você escolheu o risco mais dramático para ser necessária a Ilyan.|Runa|Não use o nome dele para diminuir meu trabalho.
838|Uma mão erguida|Dia 500 · tarde, imediato|patio-praticas|sere,ilyan|Sere gently raises a hand to stop Ilyan stepping forward; both watch the two women from the edge, no confrontation.|Sere|Ela precisa responder por si.|Ilyan|Eu sei. Só não aceito essa acusação.
839|Método contra orgulho|Dia 500 · tarde, em seguida|patio-praticas|runa,liria|Runa asks Líria directly over the table; Líria holds her chained notebook and meets her gaze.|Runa|Deixaria seu nome num parecer sem repetir a medida?|Líria|Aceito a vistoria. Com uma testemunha do fluxo.
840|O controle pedido|Dia 500 · tarde, continuidade|patio-praticas|liria,runa|Líria indicates a shallow water channel and dry replica; Runa restrains her anger.|Líria|Quero distinguir água conduzida da água que corre sozinha.|Runa|Controle, então. Não uma insinuação de fraude.
841|Duas réplicas|Dia 500 · tarde, preparação|patio-praticas|oru,ordelia|Oru, short elderly gnome with braided silver beard and copper glasses, proposes supervised replicas to Ordelia, who marks a chalk line.|Oru|Duas pedras, canal raso, fontes nomeadas.|Ordelia|Isto testa método. Não julga o porto.
842|A palavra de parada|Dia 500 · tarde, preparação|patio-praticas|ordelia,sere|Ordelia indicates the chalk boundary; Sere holds an empty safety zone while healer waits in background.|Ordelia|Ninguém dirige matéria contra um corpo. Ao meu cessa, param.|Sere|A plateia ficará atrás desta marca.
843|Antes da água|Dia 500 · tarde, antes do teste|patio-praticas|ilyan,runa|Ilyan and Runa speak quietly beside a closed clean water basin, behind the chalk line.|Ilyan|Não dispute cada murmúrio da plateia.|Runa|Não luto para ser amada por você.
844|A fissura seca|Dia 500 · tarde, início do teste|patio-praticas|liria,oru|Líria touches only dry replica and draws a fissure in notebook; Oru watches the chalk boundary.|Líria|A fratura segue para baixo. Anote antes da água.|Oru|Registrado. Agora a fonte pode abrir.
845|A fonte visível|Dia 500 · tarde, teste|patio-praticas|runa,liria|Runa guides a narrow thread from an already full basin over a replica, Líria marks a tiny deviation from opposite side.|Runa|Fio rente à pedra. Sem arrancar bloco.|Líria|Desvio mínimo, do lado seco.
846|Outra sombra|Dia 500 · tarde, segunda leitura|patio-praticas|runa,liria|Water from the same basin changes inclination slightly across replica while Líria compares shadows on stone, distant crowd remains safely back.|Runa|Mudo o ângulo. A sombra parece outra.|Líria|A fissura física pode continuar igual.
847|Além do cal|Dia 500 · tarde, segundos depois|patio-praticas|liria,runa|Líria steps across the chalk boundary toward wet model; Runa urgently points to pooled water near the mark.|Líria|Vou tocar a pedra e conferir.|Runa|Espere. Há água junto à marca!
848|Cessa|Dia 500 · tarde, imediato|patio-praticas|oru,liria|Oru orders stop from safe edge; Líria is just across chalk line, water flow has stopped, no magic active.|!Oru|Cessa! A água parou. Recue da mesa.|Líria|Só afastarei a mão dela da prova.
849|Pulso preso|Dia 500 · tarde, imediato|patio-praticas|liria,runa|Líria grips Runa's wet wrist to move it from model; Runa pulls back, one hand each clearly visible.|Líria|Tire a mão da réplica.|Runa|Solte meu pulso.
850|O empurrão|Dia 500 · tarde, imediato|patio-praticas|runa,liria|With no magic active, Runa frees her wrist and shoves Líria's shoulder; replica tilts precariously behind them.|Runa|Eu pedi que soltasse.|Líria|A pedra... cuidado!
851|Basalto no chão|Dia 500 · tarde, segundos depois|patio-praticas|liria,runa|Replica falls and cuts Líria's shin; a few basalt pieces scatter, Runa shocked and stationary.|Líria|Minha perna! Você me empurrou.|Runa|Eu vi. A curandeira está aqui.
852|O primeiro golpe|Dia 500 · tarde, imediato|patio-praticas|liria,runa|Líria rises furious and strikes the side of Runa's face once; Runa raises forearm against a second blow; restrained non-graphic comic action.|!Líria|Não encoste em mim outra vez!|Runa|Pare, Líria!
853|Junto ao poste|Dia 500 · tarde, segundos depois|patio-praticas|runa,liria|Runa shields herself and pushes Líria toward the chalk-line post to get past, both women upright and anatomically credible.|Runa|Quero sair daqui. Dê passagem.|Líria|Você ainda acha que manda!
854|A bacia tombada|Dia 500 · tarde, segundos depois|patio-praticas|liria,runa|Líria grabs Runa's coat, disarranging Runa's straight hair, as basin tips; Runa's palm touches its remaining water, no extra hands.|Líria|Olhe para mim quando eu falar!|Runa|Então largue o meu casaco.
855|Água ao nível das botas|Dia 500 · tarde, imediato|patio-praticas|runa,liria|Runa guides remaining basin water in a LOW ARC across ground; Líria slips, tearing sleeve on fallen stone; no magic from nowhere.|Runa|Só para afastá-la.|Líria|Meu braço... maldição.
856|Estilhaços e ar|Dia 500 · tarde, paralelo|patio-praticas|caio,sere|Caio sees loose shards and chooses not to use wind; Sere moves students back, both away from fighting women.|Caio|Vento espalharia as lascas.|Sere|Então abra espaço comigo.
857|Mesa pesada|Dia 500 · tarde, paralelo|patio-praticas|tovo,caio|Tovo with green-sage skin and small tusks drags heavy model table clear with ordinary strength; Caio helps before Tovo strains shoulder.|Tovo|Segure este lado. Meu ombro reclamou.|Caio|Estou com você. Devagar.
858|Ouça minha voz|Dia 500 · tarde, segundos depois|patio-praticas|ilyan,runa|Ilyan remains BESIDE Sere at chalk edge, calls to injured Runa who is farther ahead, not physically entering the blows. His blunt practice sword is FULLY SHEATHED, both hands EMPTY and visible; no approach with a blade.|Ilyan|Runa, você me ouve?|Runa|Ouço. Ela pegou uma pedra.
859|Pedra largada|Dia 500 · tarde, imediato|patio-praticas|ilyan,liria|Ilyan at the chalk edge holds one fallen fragment harmlessly in an open palm; Líria visibly releases a DIFFERENT small fragment she had just picked up. Sere remains immediately off frame controlling the gap. Ilyan's sword is sheathed; neither attacks the other.|Ilyan|Largue a pedra, Líria.|Líria|Já larguei. Afaste-se.
860|Desta vez, param|Dia 500 · tarde, fim da briga|patio-praticas|sere,ordelia|Sere places herself safely between the women; Ordelia orders stop, both women remain apart behind them.|!Sere|Cessa. Acabou.|Ordelia|Ninguém se aproxima até a curandeira chamar.
861|Feridas separadas|Dia 500 · tarde, depois|enfermaria-casa|curandeira,runa|After first examining Líria's shin, healer checks Runa's split lip and scratched forearm, with separate distant cot for Líria; clean compresses and simple care.|Curandeira|A canela dela não atingiu tendão. Seu lábio precisa de pontos.|Runa|A costela dói. Não vou tratar a ferida dela.
862|O que cada uma fez|Dia 501 · manhã|arquivo-casa|ordelia,liria|Ordelia interviews Líria at a separate table, documenting crossed line, wrist grip and strike without Runa present.|Ordelia|Registre cada gesto, inclusive o seu.|Líria|Cruzei a linha, segurei o pulso e a golpeei.
863|Ficar sem absolver|Dia 501 · tarde|enfermaria-casa|ilyan,runa|Ilyan seated beside Runa's cot, looks worried and honest; Runa's lip has two small stitches, her arm bandaged.|Ilyan|Vi a provocação. Também vi a pedra cair.|Runa|Admiti o empurrão à Ordelia. Só preciso que fique.
864|A correção assinada|Dia 501 · noite|arquivo-casa|liria,ordelia|Líria with bandaged shin copies her original sample measurements left-handed steadying paper; Ordelia receives dated correction.|Líria|Minhas medidas não provam estável a cunha do porto.|Ordelia|Publicarei a correção com seu nome.
865|Doze dias|Dia 502 · manhã|sala-conselho|ordelia,oru|Ordelia announces equal twelve-day elemental-practice suspension with distinct recorded infractions; Oru logs method measurements separately.|Ordelia|Doze dias sem prática elemental para as duas.|Oru|As medidas anteriores à briga continuam válidas.
866|Cuidar sem apressar|Dia 502 · tarde|enfermaria-casa|runa,curandeira|Runa uses CLEAN water beneath compress to wash her own forearm wound gently under healer supervision, no instant healing.|Runa|Eu estava tentando fechar a pele depressa.|Curandeira|Primeiro retire os grãos. Depois cubra.
867|Pedido antigo|Dia 503 · manhã|arquivo-casa|eda,ordelia|Eda brings municipal papers showing refused salt company claim and Mira's older request to consult port records, but no license to open chamber.|Eda|A escritura da margem foi recusada. Havia um pedido de Mira.|Ordelia|Referência à câmara. Não é licença de entrada.
868|A comunidade decide|Dia 503 · tarde|arquivo-casa|ysra,adra|Ysra speaks to Adra over marked map, explaining feeric residents must be warned before a visit; no route drawn.|Ysra|O outro lado é habitado. Preciso ouvir o conselho.|Adra|Ninguém atravessa só porque encontrou um nome.
869|Dia de curativos|Dia 504 · manhã|enfermaria-casa|runa,curandeira|Runa changes bandage and copies raw port readings while healer checks wound; college continues around them.|Runa|Copiei as leituras brutas. Falta comparar a hora.|Curandeira|E manter este curativo limpo.
870|Amostra ao perito|Dia 504 · tarde|arquivo-casa|liria,eda|Líria delivers old basalt sample measurements to Eda's municipal expert through proper custody, avoiding Runa.|Líria|A folha é minha. A conclusão do gabinete não.|Eda|A perita receberá as duas coisas separadas.
871|A pena e o aro|Dia 506 · manhã|patio-treino|caio,sere|Caio guides a feather through a ring without moving three cloth ribbons; Sere observes near clear stone arch.|Caio|A pena passou. As fitas ficaram.|Sere|Hoje você controlou o ar, não o aplauso.
872|Poeira contra pressa|Dia 507 · manhã|patio-treino|caio,tovo|Caio's next wind attempt accidentally scatters training dust; Tovo shields his kitchen basket and jokes gently.|Caio|Ontem acertei. Hoje espalhei poeira.|Tovo|Ótimo: ainda não me peça para secar sopa com vento.
873|Duas caixas|Dia 507 · tarde|cozinha-casa|tovo,teren|Tovo carries two kitchen boxes without amplified strength, Teren checks his recovering shoulder and stance.|Tovo|Cheguei à mesa sem forçar o ombro.|Teren|Isso é treino também.
874|Chama com fonte|Dia 508 · manhã|forja-leste|ilyan,teren|Ilyan guides a small flame from counted charcoal and oil inside Teren's covered iron pan; no fire from empty air.|Ilyan|Quando fico nervoso, a chama foge.|Teren|Combustível, ar e mão calma. Comece de novo.
875|Limpeza não é cura|Dia 508 · tarde|enfermaria-casa|runa,curandeira|Healer teaches Runa with clean basin and cloth, with no wounded person being touched without permission.|Curandeira|Pergunte antes de usar água no corpo de alguém.|Runa|E não chamarei limpeza de cicatrização.
876|Outra mesa|Dia 509 · manhã|sala-teorica|liria,runa|In theory classroom, Líria at left desk notices a calculation error on Runa's separate right desk; they maintain distance, no friendly chat.|Líria|O peso da ponte está no denominador errado.|Runa|Vou conferir. Não preciso que venha à minha mesa.
877|Cálculo corrigido|Dia 509 · tarde|sala-teorica|runa,liria|Runa corrects her own page while Líria keeps working apart; tension persists but report improves.|Runa|A conta estava errada. Corrigi a cópia oficial.|Líria|O porto não suporta orgulho mal calculado.
878|Consentimento inicial|Dia 510 · tarde|sala-conselho|eda,adra|Eda returns from Porto with initial Enseada consent while Adra lists transport, food and guaranteed return.|Eda|A Enseada aceita uma vistoria na borda.|Adra|As Faias ainda precisam responder.
879|Oito nomes|Dia 510 · tarde, depois|sala-conselho|ilyan,adra|Ilyan LEFT and Adra RIGHT study provisional provisions for eight confirmed travelers: Eda, Adra, Ilyan, Sere, Tovo, Caio, Beren and Eda's photographer. Runa and Líria are NOT yet cleared; their decisions on days 502–515 will bring the list to ten. No unreadable generated text on paper.|Ilyan|Oito nomes. Líria e Runa ficaram de fora?|Adra|Faltam as autorizações individuais das duas.
880|Depois dos doze dias|Dia 515 · manhã|arquivo-casa|ordelia,runa|Ordelia formally releases Runa to gradual practice after healer and Oru sign; bandages gone but faint healing marks remain.|Ordelia|Prática gradual liberada. Campo depende de nova escolha.|Runa|Entendo. A ferida não decide minha vaga.
881|A medida sob supervisão|Dia 515 · manhã, depois|arquivo-casa|liria,eda|Eda names Líria to inspect disputed mineral sample under supervision; Líria's shin remains tender, no reconciliation.|Eda|Sua medida antiga exige sua presença, sob supervisão.|Líria|Assino os limites. Não quero seu favor.
882|Duas assinaturas|Dia 515 · tarde|arquivo-casa|runa,adra|Runa signs separate permit for water-flow notes under Adra; Líria's form stays on a different desk.|Runa|Registro o fluxo; não tocarei nos pesos.|Adra|Escreva exatamente esse limite.
883|Sem centro|Dia 515 · noite|observatorio-casa|ilyan,runa|Ilyan and Runa speak in established observatory, emotionally close but wary after fight, city lights behind.|Ilyan|Pode recusar trabalhar perto dela.|Runa|O porto tem mais de um caminho. Nenhuma de nós é o centro.
884|O portão sul|Dia 516 · manhã|portao-sul|eda,adra|Eda and Adra check ten travelers at same south gate: Eda, Adra, Ilyan, Runa, Líria, Sere, Tovo, Caio, Beren and Eda's photographer. Laden wagon, coastal road visible; realistic departure, not instant travel.|Eda|Dez na lista, incluindo Beren e minha fotógrafa.|Adra|Hessa nos encontrará no porto.
885|A travessia novamente|Dia 516 · tarde|balsa-enseada|sere,tovo|Sere watches cargo on barge while Tovo counts water jars for ten, east bank receding gradually.|Tovo|Dez viajantes, água para a volta também.|Sere|Boa conta. Ninguém improvisará sede.
886|Noite de hospedaria|Dia 516 · noite|hospedaria-hessa|hessa,ilyan|Hessa receives travelers into already-established inhabited port inn, Ilyan pays and asks about next day's tide.|Hessa|Quartos e jantar preparados. Vazante ao amanhecer.|Ilyan|Então descansamos antes de pisar nas pedras.
887|Resposta das Faias|Dia 517 · manhã|cais-porto|talin,ysra|Female red-curly-haired Talin with freckles and cheek scar brings message; Ysra holds bark permission beside busy harbor.|Talin|As Faias permitem a trilha marcada, com dois guardiões.|Ysra|O conselho do Entremeio permite visita breve na vazante.
888|Termos repetidos|Dia 517 · manhã, depois|cais-porto|ysra,adra|Ysra reads three grooves in bark with elf guardian nearby; Adra repeats restrictions to team.|Ysra|Sem caça, coleta ou entrada no Fundo de Sal.|Adra|Vou repetir a cada viajante antes da passagem.
889|Uma hora de pedra|Dia 517 · vazante|camara-contrapesos|beren,liria|Beren tests wet outer masonry without touching damp counterweight; Líria reads accessible fracture by touch.|Beren|A base está úmida. Não movo este peso.|Líria|A face inferior perdeu apoio.
890|Fluxo sem condução|Dia 517 · vazante, minutos depois|camara-contrapesos|runa,adra|Runa measures stream speed with a small bowl rather than steering it, Adra notes time and place.|Runa|A água passa rápido por uma fresta que devia respirar.|Adra|Anoto: observação, sem condução mágica.
891|Tampão retirado|Dia 517 · vazante, depois|camara-contrapesos|ysra,talin|Ysra and female red-curly-haired Talin remove agreed vegetal plug as low tide exposes narrow passage, no portal flash; Neral is not yet met.|Ysra|Só agora a maré descobriu as pedras.|Talin|Passagem aberta por uma hora. Sigam o acordo.
892|Linha de retorno|Dia 517 · vazante, imediato|passagem-entre-margens|sere,talin|Sere ties return line to agreed stake; Talin tests stones with her staff, no one has crossed yet.|Sere|Linha presa à estaca aprovada.|Talin|Esta pedra aguenta. A próxima está lisa.
893|Pés na água|Dia 517 · vazante, travessia|passagem-entre-margens|ilyan,tovo|Ilyan and taller half-orc Tovo walk one by one through narrow wet passage, carrying lantern and bread, no teleport.|Ilyan|A manga prendeu na parede. Espere.|Tovo|Vou baixar a cabeça. Vejo sua lanterna.
894|A outra disposição|Dia 517 · vazante, do outro lado|entremeio-ponte|ysra,ilyan|Same sky but elongated water margin, suspended pools among roots and woven reed bridge to inhabited homes; Ysra guides Ilyan.|Ysra|É a mesma água, em outra disposição.|Ilyan|A casa de Hessa deveria estar atrás de nós.
895|Quem mora aqui|Dia 517 · manhã|entremeio-ponte|neral,adra|Neral introduces a lived-in Entremeio settlement of working elves, gnomes and tiny winged fadas; Adra listens respectfully.|Neral|Estas casas existiam antes da sua licença.|Adra|Nossa equipe ficará na trilha autorizada.
896|Dez passos, meia hora|Dia 517 · manhã, depois|entremeio-ponte|neral,caio|Neral shows Caio stone waymarks by bridge; unusual water geography with no magical city-hopping.|Neral|Dez passos lá podem custar meia hora na volta.|Caio|Então seguimos marcas e horário, não intuição.
897|O Fundo fechado|Dia 517 · manhã, depois|entremeio-muralha|neral,ilyan|Neral points to dark salt wall and the old human measuring towers attached to it in the distance; Ilyan sees the closed trail, no monster visible yet.|Neral|Fechamos a trilha de predadores há três gerações.|Ilyan|E essas torres humanas que levavam água?
898|Sulco de ferramenta|Dia 517 · perto do meio-dia|entremeio-ponte|liria,eda|Líria finds tool groove at bridge base; Eda's photographer records in situ without moving it.|Líria|Este peso foi retirado. Não é desgaste de estação.|Eda|Fotografem antes que alguém toque.
899|Frio sob o sal|Dia 517 · meio-dia|entremeio-muralha|runa,neral|Runa feels cold water rising beneath warm sun near salt wall; Neral sees recent copper wedge and loose salt-company tag.|Runa|Água fria sobe aqui. Minha bacia não a alcança.|Neral|Cabo e cunha recentes. A etiqueta é só um indício.
900|Unhas atrás da parede|Dia 517 · meio-dia, imediato|entremeio-muralha|sere,ilyan|Sere hears claws behind salt wall, commands retreat; Ilyan leaves loose copper tag on ground, chooses rear guard.|!Sere|Para a ponte. Agora.|Ilyan|A etiqueta fica. Volto com todos.
901|Raspa-frio|Dia 517 · meio-dia, segundos depois|entremeio-muralha|neral,tovo|First plated pale articulated cold-hunting creature emerges following Tovo's lantern. Neral scrapes her knee against a low stone as she steps back, a superficial injury distinct from Eda's later cut. She identifies the creature; no duplicate body parts.|Neral|Raspa-frio. Ela segue calor e minério.|Tovo|Então a minha lanterna a chamou.
902|Duas na fissura|Dia 517 · meio-dia, imediato|entremeio-muralha|sere,caio|Second cold creature appears behind first as path narrows with rising water; Sere controls retreat, Caio watches air flow.|Sere|Uma segunda. Não espalhe estilhaços com vento.|Caio|Vou tentar devolver o ar à fissura.
903|Ar que volta errado|Dia 517 · meio-dia, imediato|entremeio-muralha|caio,tovo|Caio's misdirected gust almost yanks lantern from Tovo; no superhuman control, both retreat safely.|Caio|Errei a direção. A lanterna quase caiu.|Tovo|Pare; a ponte precisa de luz.
904|Onde segurar|Dia 517 · meio-dia, simultâneo|entremeio-ponte|tovo,beren|Tovo props reed bridge base while Beren points to whole crossbeam not loose rushes; brief enhanced strength with visible strain.|Tovo|Nesta travessa inteira?|Beren|Sim. Só até Neral pôr a trava.
905|Passar a carga|Dia 517 · meio-dia, segundos depois|entremeio-ponte|tovo,beren|Tovo's shoulder aches, Beren and guardians accept load under the braced bridge; people cross in background.|Tovo|A trava entrou. Meu ombro não aguenta mais.|Beren|Passe para mim. Não banque a ponte sozinho.
906|Um jarro aberto|Dia 517 · meio-dia, paralelo|entremeio-muralha|runa,liria|Runa empties ONE clean jar into carved stone channel and guides glittering thread away from bridge; Líria reads movable salt plate nearby.|Runa|Posso desviar o brilho com esta água limpa.|Líria|A placa junto à sua mão pode cobrir a abertura.
907|Espada sem fio|Dia 517 · meio-dia, imediato|entremeio-muralha|ilyan,eda|One cold creature leaps toward Eda's knee; Ilyan intercepts with blunt iron-echo sword GUARD as wedge, protecting her, not lethal attack.|Ilyan|Atrás de mim, Eda!|Eda|A placa me cortou o joelho.
908|Óleo contado|Dia 517 · meio-dia, segundos depois|entremeio-muralha|ilyan,sere|Ilyan guides a brief thread of fire FROM Tovo's existing oil lantern across sword tip; wick dims as creature retreats to cold.|Ilyan|A chama vem da mecha. Está acabando.|Sere|Basta para fazê-la recuar. Volte.
909|Água com permissão|Dia 517 · meio-dia, depois|entremeio-ponte|runa,eda|Runa kneels at Eda's bleeding knee with remaining second clean jar and asks before washing, no instant healing.|Runa|Posso lavar o corte? Tenho água limpa.|Eda|Pode. Há grãos escuros na pele.
910|Não feche o corte|Dia 517 · meio-dia, continuidade|entremeio-ponte|runa,neral|After cleaning and covering Eda's cut on page 909, Runa washes the SEPARATE superficial scrape on Neral's knee from the retreat on page 901. Neral sends for local healer to examine Eda's more serious wound and her own knee.|Runa|Saiu o grão. O corte continua aberto.|Neral|A curandeira verá o meu e o de Eda.
911|Peso certo|Dia 517 · meio-dia, paralelo|entremeio-muralha|liria,beren|Líria guides Beren and two guardians with precise fracture direction as they lever a salt plate manually, no effortless magic.|Líria|Ergam pelo lado inteiro. A fratura corre à esquerda.|Beren|Alavanca firme. Mais um dedo de altura.
912|Medida suficiente|Dia 517 · meio-dia, segundos depois|entremeio-muralha|runa,liria|Runa observes flow and Líria holds palm on wall while plate settles over fissure; a THIRD raspa-frio is only HEARD scratching salt on the far side, not shown. They exchange necessary data only, eyes tense.|Runa|O fio frio diminuiu. A terceira arranha o sal.|Líria|A placa assentou. Não retire a alavanca ainda.
913|Tampão vivo|Dia 517 · tarde|entremeio-muralha|neral,ysra|Neral fixes vegetal plug in repaired opening, Ysra watches, no final structural victory claim.|Neral|Dura até o conselho decidir o reparo.|Ysra|Por hoje, a trilha fecha.
914|Exame da margem|Dia 517 · tarde, depois|entremeio-aldeia|iri,eda|IRI is the FEERIC VILLAGE HEALER, a distinct person from the House healer: adult, deep umber skin, dark eyes, long bark-black braids, two fine green twigs at temples, simple moss cloak. Iri examines Eda's cleaned knee in a modest inhabited village; no school healer present.|Iri|Limpar cedo ajudou. Exame de volta à Casa, ainda assim.|Eda|Registrarei os dois cuidados.
915|Pão de raiz|Dia 517 · tarde|entremeio-ponte|tovo,menina_gnoma|Small GNOME CHILD of the bridge offers root bread to Tovo, who shares dried soup; warm moment without exoticizing community.|Tovo|Trouxe sopa seca. Aposto que seu pão é melhor.|Menina gnoma|Trouxe pão da nossa ponte.
916|Sem milagre|Dia 517 · crepúsculo|entremeio-aldeia|ilyan,runa|Ilyan sits with tired Runa after care, she leans forehead on his shoulder; no sudden cure or public spectacle.|Ilyan|Você cuidou bem dela sem prometer milagre.|Runa|Isso basta por hoje.
917|À espera da vazante|Dia 518–522 · espera e manhã da saída|passagem-entre-margens|sere,talin,eda,neral|A clear TWO-PANEL sequential montage: four nights waiting with Entremeio hosts; on day 522 morning Neral explicitly permits Eda to pick up the loose copper tag from its marked spot by the salt wall, under witness; then Sere LEFT and female Talin RIGHT check return rope and wet stones at the next authorized low tide. Eda and Neral only in the small earlier inset, no dialogue; Sere and Talin are primary speakers in lower half.|Sere|Eda recolheu a etiqueta com licença. Linha firme.|Talin|Dia 522. Pedras molhadas; um passo de cada vez.
918|Nomes em casca|Dia 522 · manhã, antes da saída|entremeio-ponte|neral,ilyan|Still INSIDE the Entremeio and after the tag retrieval, Neral hands Ilyan a SMALL COPY of bark list of old chamber measurers with Pedra-Mansa and a familiar sign; no claim of proof.|Neral|É uma cópia. Há um sinal que talvez conheça.|Ilyan|Parece o do caderno de Mira. Ainda não prova nada.
919|Todos no mesmo lado|Dia 522 · manhã, depois|cais-porto|adra,ysra|Adra counts all returning travelers on Hessa's bank after wet passage; Ysra closes agreed access from this side, no missing crew.|Adra|Todos chegaram. Fechamos conforme o acordo.|Ysra|Avisarei a margem antes de qualquer retorno.
920|Cadeia de guarda|Dia 522 · tarde|hospedaria-hessa|eda,adra|At Hessa's inn Eda documents Neral's permission granted INSIDE before crossing to take copper tag; Beren's drawing and original tag separately logged.|Eda|Neral autorizou retirar a etiqueta lá dentro.|Adra|Anote o lugar, a hora e quem a encontrou.
921|Dois dias de volta|Dia 524 · tarde|balsa-enseada|eda,adra|Eda rests injured knee in Hessa's borrowed cart then on ferry; Adra ensures slow two-day return to Valecobre.|Eda|A estrada inteira de uma vez seria imprudente.|Adra|Chegaremos à Casa hoje, sem forçar sua perna.
922|O que não posso atestar|Dia 524 · noite|enfermaria-casa|runa,curandeira,eda|Runa LEFT and House healer RIGHT speak as the healer rechecks Eda's knee after travel; Eda is visibly resting on the cot in the lower center but does not speak. Runa records the initial rinse accurately.|Runa|Lavei cedo. Não posso atestar que estava curada.|Curandeira|Exato. Não há placa escondida; vigiaremos febre.
923|Três pilhas|Dia 525 · manhã|arquivo-casa|ordelia,runa|Ordelia and Runa compare tariff, community list and old municipal request in three separate stacks, no paper alone conclusive.|Ordelia|Um sinal parecido não é assinatura.|Runa|Tarifa, lista e pedido precisam se confirmar.
924|Um recibo na caixa|Dia 525 · tarde|arquivo-casa|hessa,ilyan|Hessa opens father's box of copper tariff plates and waxed envelopes; Ilyan sees receipt naming Mira de Pedra-Mansa after known disappearance, stunned, without yet treating it as final proof.|Hessa|Meu pai anotou: estojo de vidro para Mira de Pedra-Mansa.|Ilyan|A data é posterior à partida. Precisamos conferir o livro público."""


def parse_speaker(raw: str) -> tuple[str, str]:
    return (raw[1:], {"!": "shout", "~": "thought", "_": "whisper"}[raw[0]]) if raw and raw[0] in "!~_" else (raw, "normal")


def make_line(speaker: str, text: str, side: int, page_number: int) -> dict:
    name, kind = parse_speaker(speaker)
    x = 7 if side == 0 else 54
    target_x = 27 if side == 0 else 73
    y = 27 if len(text) <= 47 else 25
    target_y = 43
    # The first four generated compositions have closer faces. Their compact
    # balloons need a higher illustrated part of the room, with tails directed
    # toward the visible speaker rather than crossing eyes or hair.
    if page_number == 831:
        target_x = 30 if side == 0 else 61
    elif page_number == 832:
        y, target_y = 12, 26
        target_x = 40 if side == 0 else 70
    elif page_number in (833, 834, 835):
        y, target_y = 10, 26
    elif page_number == 852:
        # A face de Runa também aparece no quadro de detalhe à esquerda.
        y, target_y = (14, 38) if side == 0 else (22, 42)
    elif page_number == 861:
        # A curandeira está alta no quadro: reservar até o cabelo.
        y, target_y = 6, 24
    elif page_number in (862, 863):
        # Os rostos estão mais baixos; manter balões perto deles.
        y, target_y = 20, 34
    elif page_number == 917:
        # A página é uma montagem: Sere e Talin falam no quadro INFERIOR.
        # Evitar caudas atravessando os rostos de Talin e Tovo nos quadros
        # anteriores e apontar perto das duas falantes visíveis abaixo.
        y, target_y = 60, 70
    # Manual face-map pass over the actual generated paintings. The default
    # height band would cross hair, eyes or mouths on these pages; keep each
    # bubble in illustrated scenery immediately above the speaker instead.
    face_safe_positions = {
        837: (12, 22), 838: (8, 19), 839: (13, 23),
        841: (10, 24), 842: (11, 25), 843: (15, 29),
        844: (10, 23), 845: (15, 28), 846: (13, 28),
        847: (12, 28), 848: (10, 25), 849: (15, 32),
        850: (13, 28), 851: (8, 22), 853: (8, 23),
        854: (8, 22), 855: (6, 19), 856: (15, 31),
        857: (15, 30), 858: (14, 30), 859: (14, 30),
        860: (15, 30), 864: (19, 35), 865: (20, 36),
        866: (15, 31), 867: (16, 32), 868: (16, 32),
        869: (16, 31), 870: (18, 34), 912: (14, 28),
        913: (12, 27),
    }
    if page_number in face_safe_positions:
        y, target_y = face_safe_positions[page_number]
    if page_number == 917 and side == 1:
        # Talin está alguns pixels mais abaixo que Sere no quadro inferior.
        y, target_y = 63, 74
    if page_number == 915:
        # Tovo fala primeiro à esquerda; a menina responde à direita, próxima
        # do próprio retrato. Ambas as caudas ficam curtas e fora dos rostos.
        x, y, target_x, target_y = (
            (54, 48, 77, 65) if name == "Menina gnoma"
            else (7, 27, 27, 44)
        )
    # The painted portraits are deliberately below the lettering band. These
    # coordinates keep compact balloons above the hairline, not over faces.
    return {"speaker": name, "text": text, "balloon": {
        "x": x, "y": y,
        "w": 39, "target_x": target_x, "target_y": target_y, "kind": kind,
    }}


pages = []
for record in BEATS.splitlines():
    fields = record.split("|")
    if len(fields) != 10:
        raise ValueError(f"Expected 10 fields, got {len(fields)}: {record}")
    number, title, time, place, cast, scene, speaker_a, line_a, speaker_b, line_b = fields
    place = PLACE_ALIASES.get(place, place)
    chapter = 4 if int(number) <= 868 else 5 if int(number) <= 920 else 6
    pages.append({
        "number": int(number), "title": title, "time": time, "place": place,
        "cast": cast.split(","),
        "layout": ("environmental reveal with foreground" if int(number) % 7 == 0 else
                   "asymmetric comic panel with object inset" if int(number) % 4 == 0 else
                   "cinematic single scene with lower detail inset" if int(number) % 3 == 0 else
                   "varied full-page painted comic composition"),
        "scene": scene, "novel_volume": 2, "novel_chapter": chapter,
        "lines": [make_line(speaker_a, line_a, 0, int(number)), make_line(speaker_b, line_b, 1, int(number))],
    })

assert [p["number"] for p in pages] == list(range(831, 925))
DEST.write_text(json.dumps({
    "chapters": [
        {"title": "A segunda lâmina", "start": 831, "end": 868},
        {"title": "A margem de dentro", "start": 869, "end": 920},
        {"title": "A assinatura depois do inverno", "start": 921, "end": 924},
    ],
    "pages": pages,
}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Wrote {len(pages)} pages to {DEST}")
