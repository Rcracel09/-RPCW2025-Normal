import json
import rdflib
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, RDFS, XSD, OWL

# Função para criar um ID válido para URIs a partir de um nome
def create_id(name):
    return name.lower().replace(" ", "_").replace("-", "_").replace(".", "").replace(",", "")

# Carrega os datasets JSON
def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# Criação de indivíduos para Conceitos
def create_conceitos(g, conceitos_data, conceitos_dict, periodos_dict, aplicacoes_dict):
    SAPIENTIA = Namespace("http://www.sapientia.edu/ontology#")
    
    for conceito in conceitos_data["conceitos"]:
        nome = conceito["nome"]
        conceito_id = create_id(nome)
        conceito_uri = SAPIENTIA[f"conceito_{conceito_id}"]
        
        # Adiciona o conceito ao grafo
        g.add((conceito_uri, RDF.type, SAPIENTIA.Conceito))
        g.add((conceito_uri, SAPIENTIA.nome, Literal(nome, datatype=XSD.string)))
        
        # Armazena para referência posterior
        conceitos_dict[nome] = conceito_uri
        
        # Adiciona período histórico
        if "períodoHistórico" in conceito:
            periodo = conceito["períodoHistórico"]
            if periodo not in periodos_dict:
                periodo_id = create_id(periodo)
                periodo_uri = SAPIENTIA[f"periodo_{periodo_id}"]
                g.add((periodo_uri, RDF.type, SAPIENTIA.PeriodoHistorico))
                g.add((periodo_uri, SAPIENTIA.nome, Literal(periodo, datatype=XSD.string)))
                periodos_dict[periodo] = periodo_uri
            
            g.add((conceito_uri, SAPIENTIA.surgeEm, periodos_dict[periodo]))
        
        # Adiciona aplicações
        if "aplicações" in conceito:
            for aplicacao in conceito["aplicações"]:
                if aplicacao not in aplicacoes_dict:
                    aplicacao_id = create_id(aplicacao)
                    aplicacao_uri = SAPIENTIA[f"aplicacao_{aplicacao_id}"]
                    g.add((aplicacao_uri, RDF.type, SAPIENTIA.Aplicacao))
                    g.add((aplicacao_uri, SAPIENTIA.nome, Literal(aplicacao, datatype=XSD.string)))
                    aplicacoes_dict[aplicacao] = aplicacao_uri
                
                g.add((conceito_uri, SAPIENTIA.temAplicacaoEm, aplicacoes_dict[aplicacao]))
        
    # Adiciona relações entre conceitos
    for conceito in conceitos_data["conceitos"]:
        nome = conceito["nome"]
        if "conceitosRelacionados" in conceito:
            for relacionado in conceito["conceitosRelacionados"]:
                # Cria o conceito relacionado se ainda não existir
                if relacionado not in conceitos_dict:
                    relacionado_id = create_id(relacionado)
                    relacionado_uri = SAPIENTIA[f"conceito_{relacionado_id}"]
                    g.add((relacionado_uri, RDF.type, SAPIENTIA.Conceito))
                    g.add((relacionado_uri, SAPIENTIA.nome, Literal(relacionado, datatype=XSD.string)))
                    conceitos_dict[relacionado] = relacionado_uri
                
                g.add((conceitos_dict[nome], SAPIENTIA.estaRelacionadoCom, conceitos_dict[relacionado]))

# Criação de indivíduos para Disciplinas
def create_disciplinas(g, disciplinas_data, disciplinas_dict, tipos_conhecimento_dict, conceitos_dict):
    SAPIENTIA = Namespace("http://www.sapientia.edu/ontology#")
    
    for disciplina in disciplinas_data["disciplinas"]:
        nome = disciplina["nome"]
        disciplina_id = create_id(nome)
        disciplina_uri = SAPIENTIA[f"disciplina_{disciplina_id}"]
        
        # Adiciona a disciplina ao grafo
        g.add((disciplina_uri, RDF.type, SAPIENTIA.Disciplina))
        g.add((disciplina_uri, SAPIENTIA.nome, Literal(nome, datatype=XSD.string)))
        
        # Armazena para referência posterior
        disciplinas_dict[nome] = disciplina_uri
        
        # Adiciona tipos de conhecimento
        if "tiposDeConhecimento" in disciplina:
            for tipo in disciplina["tiposDeConhecimento"]:
                if tipo not in tipos_conhecimento_dict:
                    tipo_id = create_id(tipo)
                    tipo_uri = SAPIENTIA[f"tipo_{tipo_id}"]
                    g.add((tipo_uri, RDF.type, SAPIENTIA.TipoDeConhecimento))
                    g.add((tipo_uri, SAPIENTIA.nome, Literal(tipo, datatype=XSD.string)))
                    tipos_conhecimento_dict[tipo] = tipo_uri
                
                g.add((disciplina_uri, SAPIENTIA.pertenceA, tipos_conhecimento_dict[tipo]))
        
        # Adiciona conceitos estudados
        if "conceitos" in disciplina:
            for conceito in disciplina["conceitos"]:
                # Cria o conceito se ainda não existir
                if conceito not in conceitos_dict:
                    conceito_id = create_id(conceito)
                    conceito_uri = SAPIENTIA[f"conceito_{conceito_id}"]
                    g.add((conceito_uri, RDF.type, SAPIENTIA.Conceito))
                    g.add((conceito_uri, SAPIENTIA.nome, Literal(conceito, datatype=XSD.string)))
                    conceitos_dict[conceito] = conceito_uri
                
                # Usa a propriedade inversa: conceito eEstudadoEm disciplina
                g.add((conceitos_dict[conceito], SAPIENTIA.eEstudadoEm, disciplina_uri))

# Criação de indivíduos para Mestres
def create_mestres(g, mestres_data, mestres_dict, disciplinas_dict, periodos_dict):
    SAPIENTIA = Namespace("http://www.sapientia.edu/ontology#")
    
    for mestre in mestres_data["mestres"]:
        nome = mestre["nome"]
        mestre_id = create_id(nome)
        mestre_uri = SAPIENTIA[f"mestre_{mestre_id}"]
        
        # Adiciona o mestre ao grafo
        g.add((mestre_uri, RDF.type, SAPIENTIA.Mestre))
        g.add((mestre_uri, SAPIENTIA.nome, Literal(nome, datatype=XSD.string)))
        
        # Armazena para referência posterior
        mestres_dict[nome] = mestre_uri
        
        # Adiciona período histórico
        if "períodoHistórico" in mestre:
            periodo = mestre["períodoHistórico"]
            if periodo not in periodos_dict:
                periodo_id = create_id(periodo)
                periodo_uri = SAPIENTIA[f"periodo_{periodo_id}"]
                g.add((periodo_uri, RDF.type, SAPIENTIA.PeriodoHistorico))
                g.add((periodo_uri, SAPIENTIA.nome, Literal(periodo, datatype=XSD.string)))
                periodos_dict[periodo] = periodo_uri
            
            g.add((mestre_uri, SAPIENTIA.ensinouEm, periodos_dict[periodo]))
        
        # Adiciona disciplinas ensinadas
        if "disciplinas" in mestre:
            for disciplina in mestre["disciplinas"]:
                # Cria a disciplina se ainda não existir
                if disciplina not in disciplinas_dict:
                    disciplina_id = create_id(disciplina)
                    disciplina_uri = SAPIENTIA[f"disciplina_{disciplina_id}"]
                    g.add((disciplina_uri, RDF.type, SAPIENTIA.Disciplina))
                    g.add((disciplina_uri, SAPIENTIA.nome, Literal(disciplina, datatype=XSD.string)))
                    disciplinas_dict[disciplina] = disciplina_uri
                
                g.add((mestre_uri, SAPIENTIA.ensina, disciplinas_dict[disciplina]))

# Criação de indivíduos para Obras
def create_obras(g, obras_data, mestres_dict, conceitos_dict):
    SAPIENTIA = Namespace("http://www.sapientia.edu/ontology#")
    
    for obra in obras_data["obras"]:
        titulo = obra["titulo"]
        obra_id = create_id(titulo)
        obra_uri = SAPIENTIA[f"obra_{obra_id}"]
        
        # Adiciona a obra ao grafo
        g.add((obra_uri, RDF.type, SAPIENTIA.Obra))
        g.add((obra_uri, SAPIENTIA.titulo, Literal(titulo, datatype=XSD.string)))
        
        # Adiciona autor (mestre)
        if "autor" in obra:
            autor = obra["autor"]
            # Cria o mestre se ainda não existir
            if autor not in mestres_dict:
                autor_id = create_id(autor)
                autor_uri = SAPIENTIA[f"mestre_{autor_id}"]
                g.add((autor_uri, RDF.type, SAPIENTIA.Mestre))
                g.add((autor_uri, SAPIENTIA.nome, Literal(autor, datatype=XSD.string)))
                mestres_dict[autor] = autor_uri
            
            g.add((obra_uri, SAPIENTIA.foiEscritoPor, mestres_dict[autor]))
        
        # Adiciona conceitos explicados
        if "conceitos" in obra:
            for conceito in obra["conceitos"]:
                # Cria o conceito se ainda não existir
                if conceito not in conceitos_dict:
                    conceito_id = create_id(conceito)
                    conceito_uri = SAPIENTIA[f"conceito_{conceito_id}"]
                    g.add((conceito_uri, RDF.type, SAPIENTIA.Conceito))
                    g.add((conceito_uri, SAPIENTIA.nome, Literal(conceito, datatype=XSD.string)))
                    conceitos_dict[conceito] = conceito_uri
                
                g.add((obra_uri, SAPIENTIA.explica, conceitos_dict[conceito]))

# Criação de indivíduos para Aprendizes
def create_aprendizes(g, aprendizes_data, disciplinas_dict):
    SAPIENTIA = Namespace("http://www.sapientia.edu/ontology#")
    
    for aprendiz in aprendizes_data:
        nome = aprendiz["nome"]
        idade = aprendiz["idade"]
        aprendiz_id = create_id(nome)
        aprendiz_uri = SAPIENTIA[f"aprendiz_{aprendiz_id}"]
        
        # Adiciona o aprendiz ao grafo
        g.add((aprendiz_uri, RDF.type, SAPIENTIA.Aprendiz))
        g.add((aprendiz_uri, SAPIENTIA.nome, Literal(nome, datatype=XSD.string)))
        g.add((aprendiz_uri, SAPIENTIA.idade, Literal(idade, datatype=XSD.integer)))
        
        # Adiciona disciplinas aprendidas
        if "disciplinas" in aprendiz:
            for disciplina in aprendiz["disciplinas"]:
                # Cria a disciplina se ainda não existir
                if disciplina not in disciplinas_dict:
                    disciplina_id = create_id(disciplina)
                    disciplina_uri = SAPIENTIA[f"disciplina_{disciplina_id}"]
                    g.add((disciplina_uri, RDF.type, SAPIENTIA.Disciplina))
                    g.add((disciplina_uri, SAPIENTIA.nome, Literal(disciplina, datatype=XSD.string)))
                    disciplinas_dict[disciplina] = disciplina_uri
                
                g.add((aprendiz_uri, SAPIENTIA.aprende, disciplinas_dict[disciplina]))

# Função principal de povoamento
def populate_ontology():
    # Inicializa o grafo RDF
    g = Graph()
    
    # Carrega a ontologia base
    g.parse("sapientia_base.ttl", format="turtle")
    
    # Define namespaces
    SAPIENTIA = Namespace("http://www.sapientia.edu/ontology#")
    g.bind("sapientia", SAPIENTIA)
    
    # Carrega dados JSON
    conceitos_data = load_json("conceitos.json")
    disciplinas_data = load_json("disciplinas.json")
    mestres_data = load_json("mestres.json")
    obras_data = load_json("obras.json")
    aprendizes_data = load_json("pg57871.json")
    
    # Dicionários para rastrear entidades já criadas (evita duplicações)
    conceitos_dict = {}
    disciplinas_dict = {}
    mestres_dict = {}
    periodos_dict = {}
    aplicacoes_dict = {}
    tipos_conhecimento_dict = {}
    
    # Cria indivíduos e relações
    create_conceitos(g, conceitos_data, conceitos_dict, periodos_dict, aplicacoes_dict)
    create_disciplinas(g, disciplinas_data, disciplinas_dict, tipos_conhecimento_dict, conceitos_dict)
    create_mestres(g, mestres_data, mestres_dict, disciplinas_dict, periodos_dict)
    create_obras(g, obras_data, mestres_dict, conceitos_dict)
    create_aprendizes(g, aprendizes_data, disciplinas_dict)
    
    # Salva a ontologia povoada
    g.serialize(destination="sapientia_ind.ttl", format="turtle")

# Executa o script
if __name__ == "__main__":
    populate_ontology()