from __future__ import annotations
from typing import Any

GRAPH_FIELD_SEP = "<SEP>"

PROMPTS: dict[str, Any] = {}


PROMPTS["DEFAULT_LANGUAGE"] = "Portuguese"  

PROMPTS["DEFAULT_TUPLE_DELIMITER"] = "<|>"
PROMPTS["DEFAULT_RECORD_DELIMITER"] = "##"
PROMPTS["DEFAULT_COMPLETION_DELIMITER"] = "<|COMPLETE|>"


PROMPTS["DEFAULT_ENTITY_TYPES"] = ["organization", "person", "geo", "event", "category", "decision"]  

PROMPTS["DEFAULT_USER_PROMPT"] = "n/a"

PROMPTS["entity_extraction"] = """---Objetivo---
Dado um documento de texto que é potencialmente relevante para esta atividade e uma lista de tipos de entidade, identifique todas as entidades desses tipos do texto e todos os relacionamentos entre as entidades identificadas.
Use {language} como idioma de saída.

---Etapas---
1. Identifique todas as entidades. Para cada entidade identificada, extraia as seguintes informações:
- entity_name: Nome da entidade, use o mesmo idioma do texto de entrada. Se em inglês, capitalize o nome.
- entity_type: Um dos seguintes tipos: [{entity_types}]
- entity_description: Descrição abrangente dos atributos e atividades da entidade
Formate cada entidade como ("entity"{tuple_delimiter}<entity_name>{tuple_delimiter}<entity_type>{tuple_delimiter}<entity_description>)

2. Das entidades identificadas na etapa 1, identifique todos os pares de (source_entity, target_entity) que estão *claramente relacionados* entre si.
Para cada par de entidades relacionadas, extraia as seguintes informações:
- source_entity: nome da entidade de origem, conforme identificado na etapa 1
- target_entity: nome da entidade de destino, conforme identificado na etapa 1
- relationship_description: explicação de por que você acha que a entidade de origem e a entidade de destino estão relacionadas entre si
- relationship_strength: uma pontuação numérica indicando a força do relacionamento entre a entidade de origem e a entidade de destino
- relationship_keywords: uma ou mais palavras-chave de alto nível que resumem a natureza geral do relacionamento, focando em conceitos ou temas em vez de detalhes específicos
Formate cada relacionamento como ("relationship"{tuple_delimiter}<source_entity>{tuple_delimiter}<target_entity>{tuple_delimiter}<relationship_description>{tuple_delimiter}<relationship_keywords>{tuple_delimiter}<relationship_strength>)

3. Identifique palavras-chave de alto nível que resumem os principais conceitos, temas ou tópicos de todo o texto. Estas devem capturar as ideias gerais presentes no documento.
Formate as palavras-chave de nível de conteúdo como ("content_keywords"{tuple_delimiter}<high_level_keywords>)

4. Retorne a saída em {language} como uma lista única de todas as entidades e relacionamentos identificados nas etapas 1 e 2. Use **{record_delimiter}** como delimitador de lista.

5. Quando terminar, produza {completion_delimiter}

######################
---Exemplos---
######################
{examples}

#############################
---Dados Reais---
######################
Entity_types: [{entity_types}]
Texto:
{input_text}
######################
Saída:"""

PROMPTS["entity_extraction_examples"] = [
    """Exemplo 1:

Entity_types: [person, technology, mission, organization, location]
Texto:
```
enquanto Alex cerrou o maxilar, o zumbido de frustração opaco contra o pano de fundo da certeza autoritária de Taylor. Era essa corrente subterrânea competitiva que o mantinha alerta, a sensação de que o compromisso compartilhado dele e de Jordan com a descoberta era uma rebelião não dita contra a visão estreita de controle e ordem de Cruz.

Então Taylor fez algo inesperado. Eles pararam ao lado de Jordan e, por um momento, observaram o dispositivo com algo parecido com reverência. "Se essa tecnologia puder ser entendida..." Taylor disse, com a voz mais baixa, "Poderia mudar o jogo para nós. Para todos nós."

A rejeição subjacente anterior pareceu vacilar, substituída por um vislumbre de respeito relutante pela gravidade do que estava em suas mãos. Jordan olhou para cima, e por um batimento cardíaco fugaz, seus olhos se encontraram com os de Taylor, um confronto silencioso de vontades suavizando-se em uma trégua desconfortável.

Foi uma pequena transformação, quase imperceptível, mas que Alex notou com um aceno interno. Todos eles foram trazidos aqui por caminhos diferentes
```

Saída:
("entity"{tuple_delimiter}"Alex"{tuple_delimiter}"person"{tuple_delimiter}"Alex é um personagem que experimenta frustração e é observador das dinâmicas entre outros personagens."){record_delimiter}
("entity"{tuple_delimiter}"Taylor"{tuple_delimiter}"person"{tuple_delimiter}"Taylor é retratado com certeza autoritária e mostra um momento de reverência em relação a um dispositivo, indicando uma mudança de perspectiva."){record_delimiter}
("entity"{tuple_delimiter}"Jordan"{tuple_delimiter}"person"{tuple_delimiter}"Jordan compartilha um compromisso com a descoberta e tem uma interação significativa com Taylor sobre um dispositivo."){record_delimiter}
("entity"{tuple_delimiter}"Cruz"{tuple_delimiter}"person"{tuple_delimiter}"Cruz está associado a uma visão de controle e ordem, influenciando a dinâmica entre outros personagens."){record_delimiter}
("entity"{tuple_delimiter}"O Dispositivo"{tuple_delimiter}"technology"{tuple_delimiter}"O Dispositivo é central para a história, com implicações potencialmente revolucionárias, e é reverenciado por Taylor."){record_delimiter}
("relationship"{tuple_delimiter}"Alex"{tuple_delimiter}"Taylor"{tuple_delimiter}"Alex é afetado pela certeza autoritária de Taylor e observa mudanças na atitude de Taylor em relação ao dispositivo."{tuple_delimiter}"dinâmica de poder, mudança de perspectiva"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"Alex"{tuple_delimiter}"Jordan"{tuple_delimiter}"Alex e Jordan compartilham um compromisso com a descoberta, que contrasta com a visão de Cruz."{tuple_delimiter}"objetivos compartilhados, rebelião"{tuple_delimiter}6){record_delimiter}
("relationship"{tuple_delimiter}"Taylor"{tuple_delimiter}"Jordan"{tuple_delimiter}"Taylor e Jordan interagem diretamente sobre o dispositivo, levando a um momento de respeito mútuo e uma trégua desconfortável."{tuple_delimiter}"resolução de conflito, respeito mútuo"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Jordan"{tuple_delimiter}"Cruz"{tuple_delimiter}"O compromisso de Jordan com a descoberta está em rebelião contra a visão de controle e ordem de Cruz."{tuple_delimiter}"conflito ideológico, rebelião"{tuple_delimiter}5){record_delimiter}
("relationship"{tuple_delimiter}"Taylor"{tuple_delimiter}"O Dispositivo"{tuple_delimiter}"Taylor mostra reverência em relação ao dispositivo, indicando sua importância e impacto potencial."{tuple_delimiter}"reverência, significância tecnológica"{tuple_delimiter}9){record_delimiter}
("content_keywords"{tuple_delimiter}"dinâmica de poder, conflito ideológico, descoberta, rebelião"){completion_delimiter}
#############################""",
    """Exemplo 2:

Entity_types: [company, index, commodity, market_trend, economic_policy, biological]
Texto:
```
Os mercados de ações enfrentaram uma queda acentuada hoje, pois as gigantes da tecnologia viram declínios significativos, com o Índice Global de Tecnologia caindo 3,4% nas negociações do meio-dia. Analistas atribuem a venda às preocupações dos investidores sobre o aumento das taxas de juros e a incerteza regulatória.

Entre os mais atingidos, a Nexon Technologies viu suas ações despencarem 7,8% após relatar lucros trimestrais abaixo do esperado. Em contraste, a Omega Energy registrou um ganho modesto de 2,1%, impulsionado pelo aumento dos preços do petróleo.

Enquanto isso, os mercados de commodities refletiram um sentimento misto. Os futuros de ouro subiram 1,5%, atingindo US$ 2.080 por onça, à medida que os investidores buscavam ativos de refúgio seguro. Os preços do petróleo bruto continuaram sua alta, subindo para US$ 87,60 por barril, apoiados por restrições de oferta e forte demanda.

Especialistas financeiros estão observando atentamente o próximo movimento do Federal Reserve, à medida que cresce a especulação sobre possíveis aumentos de taxas. O próximo anúncio de política deve influenciar a confiança dos investidores e a estabilidade geral do mercado.
```

Saída:
("entity"{tuple_delimiter}"Índice Global de Tecnologia"{tuple_delimiter}"index"{tuple_delimiter}"O Índice Global de Tecnologia rastreia o desempenho das principais ações de tecnologia e experimentou um declínio de 3,4% hoje."){record_delimiter}
("entity"{tuple_delimiter}"Nexon Technologies"{tuple_delimiter}"company"{tuple_delimiter}"Nexon Technologies é uma empresa de tecnologia que viu suas ações caírem 7,8% após lucros decepcionantes."){record_delimiter}
("entity"{tuple_delimiter}"Omega Energy"{tuple_delimiter}"company"{tuple_delimiter}"Omega Energy é uma empresa de energia que ganhou 2,1% em valor de ações devido ao aumento dos preços do petróleo."){record_delimiter}
("entity"{tuple_delimiter}"Futuros de Ouro"{tuple_delimiter}"commodity"{tuple_delimiter}"Os futuros de ouro subiram 1,5%, indicando maior interesse dos investidores em ativos de refúgio seguro."){record_delimiter}
("entity"{tuple_delimiter}"Petróleo Bruto"{tuple_delimiter}"commodity"{tuple_delimiter}"Os preços do petróleo bruto subiram para US$ 87,60 por barril devido a restrições de oferta e forte demanda."){record_delimiter}
("entity"{tuple_delimiter}"Venda do Mercado"{tuple_delimiter}"market_trend"{tuple_delimiter}"Venda do mercado refere-se ao declínio significativo nos valores das ações devido às preocupações dos investidores sobre taxas de juros e regulamentações."){record_delimiter}
("entity"{tuple_delimiter}"Anúncio de Política do Federal Reserve"{tuple_delimiter}"economic_policy"{tuple_delimiter}"O próximo anúncio de política do Federal Reserve deve impactar a confiança dos investidores e a estabilidade do mercado."){record_delimiter}
("relationship"{tuple_delimiter}"Índice Global de Tecnologia"{tuple_delimiter}"Venda do Mercado"{tuple_delimiter}"O declínio no Índice Global de Tecnologia faz parte da venda mais ampla do mercado impulsionada pelas preocupações dos investidores."{tuple_delimiter}"desempenho do mercado, sentimento do investidor"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Nexon Technologies"{tuple_delimiter}"Índice Global de Tecnologia"{tuple_delimiter}"O declínio das ações da Nexon Technologies contribuiu para a queda geral no Índice Global de Tecnologia."{tuple_delimiter}"impacto da empresa, movimento do índice"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Futuros de Ouro"{tuple_delimiter}"Venda do Mercado"{tuple_delimiter}"Os preços do ouro subiram à medida que os investidores buscavam ativos de refúgio seguro durante a venda do mercado."{tuple_delimiter}"reação do mercado, investimento em refúgio seguro"{tuple_delimiter}10){record_delimiter}
("relationship"{tuple_delimiter}"Anúncio de Política do Federal Reserve"{tuple_delimiter}"Venda do Mercado"{tuple_delimiter}"A especulação sobre mudanças na política do Federal Reserve contribuiu para a volatilidade do mercado e a venda dos investidores."{tuple_delimiter}"impacto da taxa de juros, regulamentação financeira"{tuple_delimiter}7){record_delimiter}
("content_keywords"{tuple_delimiter}"queda do mercado, sentimento do investidor, commodities, Federal Reserve, desempenho das ações"){completion_delimiter}
#############################""",
    """Exemplo 3:

Entity_types: [economic_policy, athlete, event, location, record, organization, equipment]
Texto:
```
No Campeonato Mundial de Atletismo em Tóquio, Noah Carter quebrou o recorde de sprint de 100m usando spikes de fibra de carbono de última geração.
```

Saída:
("entity"{tuple_delimiter}"Campeonato Mundial de Atletismo"{tuple_delimiter}"event"{tuple_delimiter}"O Campeonato Mundial de Atletismo é uma competição esportiva global com os melhores atletas em atletismo."){record_delimiter}
("entity"{tuple_delimiter}"Tóquio"{tuple_delimiter}"location"{tuple_delimiter}"Tóquio é a cidade anfitriã do Campeonato Mundial de Atletismo."){record_delimiter}
("entity"{tuple_delimiter}"Noah Carter"{tuple_delimiter}"athlete"{tuple_delimiter}"Noah Carter é um velocista que estabeleceu um novo recorde no sprint de 100m no Campeonato Mundial de Atletismo."){record_delimiter}
("entity"{tuple_delimiter}"Recorde de Sprint de 100m"{tuple_delimiter}"record"{tuple_delimiter}"O recorde de sprint de 100m é uma referência no atletismo, recentemente quebrado por Noah Carter."){record_delimiter}
("entity"{tuple_delimiter}"Spikes de Fibra de Carbono"{tuple_delimiter}"equipment"{tuple_delimiter}"Spikes de fibra de carbono são sapatos de corrida avançados que fornecem velocidade e tração aprimoradas."){record_delimiter}
("entity"{tuple_delimiter}"Federação Mundial de Atletismo"{tuple_delimiter}"organization"{tuple_delimiter}"A Federação Mundial de Atletismo é o órgão regulador que supervisiona o Campeonato Mundial de Atletismo e validações de recordes."){record_delimiter}
("relationship"{tuple_delimiter}"Campeonato Mundial de Atletismo"{tuple_delimiter}"Tóquio"{tuple_delimiter}"O Campeonato Mundial de Atletismo está sendo realizado em Tóquio."{tuple_delimiter}"localização do evento, competição internacional"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Noah Carter"{tuple_delimiter}"Recorde de Sprint de 100m"{tuple_delimiter}"Noah Carter estabeleceu um novo recorde de sprint de 100m no campeonato."{tuple_delimiter}"conquista do atleta, quebra de recorde"{tuple_delimiter}10){record_delimiter}
("relationship"{tuple_delimiter}"Noah Carter"{tuple_delimiter}"Spikes de Fibra de Carbono"{tuple_delimiter}"Noah Carter usou spikes de fibra de carbono para melhorar o desempenho durante a corrida."{tuple_delimiter}"equipamento atlético, aumento de desempenho"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"Federação Mundial de Atletismo"{tuple_delimiter}"Recorde de Sprint de 100m"{tuple_delimiter}"A Federação Mundial de Atletismo é responsável por validar e reconhecer novos recordes de sprint."{tuple_delimiter}"regulamentação esportiva, certificação de recorde"{tuple_delimiter}9){record_delimiter}
("content_keywords"{tuple_delimiter}"atletismo, velocidade, quebra de recorde, tecnologia esportiva, competição"){completion_delimiter}
#############################""",

    """Exemplo 4:

Entity_types: [organization, person, decision, event, geo]
Texto:
```
O Conselho de Administração da TechCorp reuniu-se na sede em São Paulo para deliberar sobre a proposta de expansão internacional. Após três horas de debate intenso, o presidente João Silva anunciou a decisão unânime de aprovar o investimento de R$ 200 milhões para abrir filiais na Ásia. 

A decisão foi baseada no relatório apresentado pela diretora financeira Maria Santos, que demonstrou um potencial de retorno de 35% em três anos. A implementação será liderada pelo diretor de operações Carlos Ferreira, que já iniciou o processo de seleção de equipes locais.

Paralelamente, o conselho também decidiu suspender temporariamente o projeto de automação da fábrica de Campinas, redirecionando esses recursos para a expansão internacional. Esta decisão gerou reações mistas entre os acionistas presentes na reunião.
```

Saída:
("entity"{tuple_delimiter}"TechCorp"{tuple_delimiter}"organization"{tuple_delimiter}"TechCorp é uma empresa cujo Conselho de Administração tomou decisões importantes sobre expansão internacional e projetos internos."){record_delimiter}
("entity"{tuple_delimiter}"Conselho de Administração da TechCorp"{tuple_delimiter}"organization"{tuple_delimiter}"O Conselho de Administração é o órgão decisório da TechCorp responsável por aprovar investimentos estratégicos."){record_delimiter}
("entity"{tuple_delimiter}"João Silva"{tuple_delimiter}"person"{tuple_delimiter}"João Silva é o presidente do Conselho de Administração da TechCorp que anunciou as decisões tomadas."){record_delimiter}
("entity"{tuple_delimiter}"Maria Santos"{tuple_delimiter}"person"{tuple_delimiter}"Maria Santos é a diretora financeira da TechCorp que apresentou o relatório que fundamentou a decisão de expansão."){record_delimiter}
("entity"{tuple_delimiter}"Carlos Ferreira"{tuple_delimiter}"person"{tuple_delimiter}"Carlos Ferreira é o diretor de operações da TechCorp responsável por implementar a expansão internacional."){record_delimiter}
("entity"{tuple_delimiter}"São Paulo"{tuple_delimiter}"geo"{tuple_delimiter}"São Paulo é a cidade onde está localizada a sede da TechCorp e onde ocorreu a reunião do conselho."){record_delimiter}
("entity"{tuple_delimiter}"Campinas"{tuple_delimiter}"geo"{tuple_delimiter}"Campinas é a cidade onde está localizada a fábrica da TechCorp cujo projeto de automação foi suspenso."){record_delimiter}
("entity"{tuple_delimiter}"Aprovação de Investimento para Expansão Asiática"{tuple_delimiter}"decision"{tuple_delimiter}"Decisão unânime do conselho de aprovar R$ 200 milhões para abrir filiais na Ásia, baseada em potencial de retorno de 35% em três anos."){record_delimiter}
("entity"{tuple_delimiter}"Suspensão do Projeto de Automação"{tuple_delimiter}"decision"{tuple_delimiter}"Decisão de suspender temporariamente o projeto de automação da fábrica de Campinas para redirecionar recursos à expansão internacional."){record_delimiter}
("entity"{tuple_delimiter}"Reunião do Conselho de Administração"{tuple_delimiter}"event"{tuple_delimiter}"Reunião realizada na sede da TechCorp onde foram tomadas decisões estratégicas sobre investimentos e projetos."){record_delimiter}
("relationship"{tuple_delimiter}"Conselho de Administração da TechCorp"{tuple_delimiter}"Aprovação de Investimento para Expansão Asiática"{tuple_delimiter}"O Conselho tomou a decisão unânime de aprovar o investimento para expansão."{tuple_delimiter}"decisão estratégica, aprovação de investimento"{tuple_delimiter}10){record_delimiter}
("relationship"{tuple_delimiter}"Maria Santos"{tuple_delimiter}"Aprovação de Investimento para Expansão Asiática"{tuple_delimiter}"O relatório de Maria Santos fundamentou a decisão de expansão com dados de potencial retorno."{tuple_delimiter}"fundamentação decisória, análise financeira"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"João Silva"{tuple_delimiter}"Aprovação de Investimento para Expansão Asiática"{tuple_delimiter}"João Silva anunciou oficialmente a decisão de expansão como presidente do conselho."{tuple_delimiter}"anúncio oficial, liderança executiva"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Carlos Ferreira"{tuple_delimiter}"Aprovação de Investimento para Expansão Asiática"{tuple_delimiter}"Carlos Ferreira foi designado para implementar a decisão de expansão internacional."{tuple_delimiter}"implementação de decisão, responsabilidade operacional"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Conselho de Administração da TechCorp"{tuple_delimiter}"Suspensão do Projeto de Automação"{tuple_delimiter}"O Conselho decidiu suspender o projeto para redirecionar recursos."{tuple_delimiter}"realocação de recursos, decisão estratégica"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Aprovação de Investimento para Expansão Asiática"{tuple_delimiter}"Suspensão do Projeto de Automação"{tuple_delimiter}"A suspensão do projeto foi necessária para viabilizar recursos para a expansão."{tuple_delimiter}"trade-off estratégico, realocação de investimento"{tuple_delimiter}7){record_delimiter}
("content_keywords"{tuple_delimiter}"decisão corporativa, expansão internacional, investimento estratégico, governança corporativa"){completion_delimiter}
#############################"""  
]

PROMPTS[
    "summarize_entity_descriptions"
] = """Você é um assistente útil responsável por gerar um resumo abrangente dos dados fornecidos abaixo.
Dadas uma ou duas entidades e uma lista de descrições, todas relacionadas à mesma entidade ou grupo de entidades.
Por favor, concatene todas elas em uma única descrição abrangente. Certifique-se de incluir informações coletadas de todas as descrições.
Se as descrições fornecidas forem contraditórias, resolva as contradições e forneça um resumo único e coerente.
Certifique-se de que esteja escrito em terceira pessoa e inclua os nomes das entidades para que tenhamos o contexto completo.
Use {language} como idioma de saída.

#######
---Dados---
Entidades: {entity_name}
Lista de Descrições: {description_list}
#######
Saída:
"""

PROMPTS["entity_continue_extraction"] = """
MUITAS entidades e relacionamentos foram perdidos na última extração.

---Lembre-se das Etapas---

1. Identifique todas as entidades. Para cada entidade identificada, extraia as seguintes informações:
- entity_name: Nome da entidade, use o mesmo idioma do texto de entrada. Se em inglês, capitalize o nome.
- entity_type: Um dos seguintes tipos: [{entity_types}]
- entity_description: Descrição abrangente dos atributos e atividades da entidade
Formate cada entidade como ("entity"{tuple_delimiter}<entity_name>{tuple_delimiter}<entity_type>{tuple_delimiter}<entity_description>)

2. Das entidades identificadas na etapa 1, identifique todos os pares de (source_entity, target_entity) que estão *claramente relacionados* entre si.
Para cada par de entidades relacionadas, extraia as seguintes informações:
- source_entity: nome da entidade de origem, conforme identificado na etapa 1
- target_entity: nome da entidade de destino, conforme identificado na etapa 1
- relationship_description: explicação de por que você acha que a entidade de origem e a entidade de destino estão relacionadas entre si
- relationship_strength: uma pontuação numérica indicando a força do relacionamento entre a entidade de origem e a entidade de destino
- relationship_keywords: uma ou mais palavras-chave de alto nível que resumem a natureza geral do relacionamento, focando em conceitos ou temas em vez de detalhes específicos
Formate cada relacionamento como ("relationship"{tuple_delimiter}<source_entity>{tuple_delimiter}<target_entity>{tuple_delimiter}<relationship_description>{tuple_delimiter}<relationship_keywords>{tuple_delimiter}<relationship_strength>)

3. Identifique palavras-chave de alto nível que resumem os principais conceitos, temas ou tópicos de todo o texto. Estas devem capturar as ideias gerais presentes no documento.
Formate as palavras-chave de nível de conteúdo como ("content_keywords"{tuple_delimiter}<high_level_keywords>)

4. Retorne a saída em {language} como uma lista única de todas as entidades e relacionamentos identificados nas etapas 1 e 2. Use **{record_delimiter}** como delimitador de lista.

5. Quando terminar, produza {completion_delimiter}

---Saída---

Adicione-os abaixo usando o mesmo formato:\n
""".strip()

PROMPTS["entity_if_loop_extraction"] = """
---Objetivo---'

Parece que algumas entidades ainda podem ter sido perdidas.

---Saída---

Responda APENAS com `SIM` OU `NÃO` se ainda há entidades que precisam ser adicionadas.
""".strip()

PROMPTS["fail_response"] = (
    "Desculpe, não consigo fornecer uma resposta para essa pergunta.[sem-contexto]"
)

PROMPTS["rag_response"] = """---Função---

Você é um assistente útil respondendo a consultas do usuário sobre o Grafo de Conhecimento e Fragmentos de Documentos fornecidos em formato JSON abaixo.


---Objetivo---

Gere uma resposta concisa baseada na Base de Conhecimento e siga as Regras de Resposta, considerando tanto o histórico da conversa quanto a consulta atual. Resuma todas as informações na Base de Conhecimento fornecida, incorporando conhecimento geral relevante à Base de Conhecimento. Não inclua informações não fornecidas pela Base de Conhecimento.

Ao lidar com relacionamentos com timestamps:
1. Cada relacionamento tem um timestamp "created_at" indicando quando adquirimos esse conhecimento
2. Ao encontrar relacionamentos conflitantes, considere tanto o conteúdo semântico quanto o timestamp
3. Não prefira automaticamente os relacionamentos criados mais recentemente - use julgamento baseado no contexto
4. Para consultas específicas de tempo, priorize informações temporais no conteúdo antes de considerar timestamps de criação

---Histórico da Conversa---
{history}

---Grafo de Conhecimento e Fragmentos de Documentos---
{context_data}

---Regras de Resposta---

- Formato e comprimento alvo: {response_type}
- Use formatação markdown com cabeçalhos de seção apropriados
- Por favor, responda no mesmo idioma da pergunta do usuário.
- Garanta que a resposta mantenha continuidade com o histórico da conversa.
- Liste até 5 fontes de referência mais importantes no final sob a seção "Referências". Indicando claramente se cada fonte é do Grafo de Conhecimento (KG) ou Fragmentos de Documentos (DC), e inclua o caminho do arquivo se disponível, no seguinte formato: [KG/DC] caminho_do_arquivo
- Se você não souber a resposta, apenas diga isso.
- Não invente nada. Não inclua informações não fornecidas pela Base de Conhecimento.
- Prompt adicional do usuário: {user_prompt}

Resposta:"""

PROMPTS["keywords_extraction"] = """---Função---

Você é um assistente útil encarregado de identificar palavras-chave de alto nível e baixo nível na consulta do usuário e no histórico da conversa.

---Objetivo---

Dada a consulta e o histórico da conversa, liste palavras-chave de alto nível e baixo nível. Palavras-chave de alto nível focam em conceitos ou temas gerais, enquanto palavras-chave de baixo nível focam em entidades específicas, detalhes ou termos concretos.

---Instruções---

- Considere tanto a consulta atual quanto o histórico relevante da conversa ao extrair palavras-chave
- Produza as palavras-chave em formato JSON, será analisado por um parser JSON, não adicione nenhum conteúdo extra na saída
- O JSON deve ter duas chaves:
  - "high_level_keywords" para conceitos ou temas gerais
  - "low_level_keywords" para entidades específicas ou detalhes

######################
---Exemplos---
######################
{examples}

#############################
---Dados Reais---
######################
Histórico da Conversa:
{history}

Consulta Atual: {query}
######################
A `Saída` deve ser texto legível, não caracteres unicode. Mantenha o mesmo idioma da `Consulta`.
Saída:

"""

PROMPTS["keywords_extraction_examples"] = [
    """Exemplo 1:

Consulta: "Como o comércio internacional influencia a estabilidade econômica global?"
################
Saída:
{
  "high_level_keywords": ["Comércio internacional", "Estabilidade econômica global", "Impacto econômico"],
  "low_level_keywords": ["Acordos comerciais", "Tarifas", "Câmbio", "Importações", "Exportações"]
}
#############################""",
    """Exemplo 2:

Consulta: "Quais são as consequências ambientais do desmatamento na biodiversidade?"
################
Saída:
{
  "high_level_keywords": ["Consequências ambientais", "Desmatamento", "Perda de biodiversidade"],
  "low_level_keywords": ["Extinção de espécies", "Destruição de habitat", "Emissões de carbono", "Floresta tropical", "Ecossistema"]
}
#############################""",
    """Exemplo 3:

Consulta: "Qual é o papel da educação na redução da pobreza?"
################
Saída:
{
  "high_level_keywords": ["Educação", "Redução da pobreza", "Desenvolvimento socioeconômico"],
  "low_level_keywords": ["Acesso escolar", "Taxas de alfabetização", "Treinamento profissional", "Desigualdade de renda"]
}
#############################""",
]

PROMPTS["naive_rag_response"] = """---Função---

Você é um assistente útil respondendo a consultas do usuário sobre Fragmentos de Documentos fornecidos em formato JSON abaixo.

---Objetivo---

Gere uma resposta concisa baseada nos Fragmentos de Documentos e siga as Regras de Resposta, considerando tanto o histórico da conversa quanto a consulta atual. Resuma todas as informações nos Fragmentos de Documentos fornecidos, incorporando conhecimento geral relevante aos Fragmentos de Documentos. Não inclua informações não fornecidas pelos Fragmentos de Documentos.

Ao lidar com conteúdo com timestamps:
1. Cada parte do conteúdo tem um timestamp "created_at" indicando quando adquirimos esse conhecimento
2. Ao encontrar informações conflitantes, considere tanto o conteúdo quanto o timestamp
3. Não prefira automaticamente o conteúdo mais recente - use julgamento baseado no contexto
4. Para consultas específicas de tempo, priorize informações temporais no conteúdo antes de considerar timestamps de criação

---Histórico da Conversa---
{history}

---Fragmentos de Documentos(DC)---
{content_data}

---Regras de Resposta---

- Formato e comprimento alvo: {response_type}
- Use formatação markdown com cabeçalhos de seção apropriados
- Por favor, responda no mesmo idioma da pergunta do usuário.
- Garanta que a resposta mantenha continuidade com o histórico da conversa.
- Liste até 5 fontes de referência mais importantes no final sob a seção "Referências". Indicando claramente cada fonte dos Fragmentos de Documentos(DC), e inclua o caminho do arquivo se disponível, no seguinte formato: [DC] caminho_do_arquivo
- Se você não souber a resposta, apenas diga isso.
- Não inclua informações não fornecidas pelos Fragmentos de Documentos.
- Prompt adicional do usuário: {user_prompt}

Resposta:"""

# TODO: deprecated
PROMPTS[
    "similarity_check"
] = """Por favor, analise a similaridade entre estas duas perguntas:

Pergunta 1: {original_prompt}
Pergunta 2: {cached_prompt}

Por favor, avalie se essas duas perguntas são semanticamente similares e se a resposta à Pergunta 2 pode ser usada para responder à Pergunta 1, forneça uma pontuação de similaridade entre 0 e 1 diretamente.

Critérios de pontuação de similaridade:
0: Completamente não relacionadas ou a resposta não pode ser reutilizada, incluindo mas não limitado a:
   - As perguntas têm tópicos diferentes
   - Os locais mencionados nas perguntas são diferentes
   - Os tempos mencionados nas perguntas são diferentes
   - Os indivíduos específicos mencionados nas perguntas são diferentes
   - Os eventos específicos mencionados nas perguntas são diferentes
   - As informações de fundo nas perguntas são diferentes
   - As condições-chave nas perguntas são diferentes
1: Idênticas e a resposta pode ser reutilizada diretamente
0.5: Parcialmente relacionadas e a resposta precisa de modificação para ser usada
Retorne apenas um número entre 0-1, sem nenhum conteúdo adicional.
"""