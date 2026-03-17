# Casos de Uso

| Nome | Descrição | 
| :--- | :---: | 
| UC001 - Verificar Tempo em Pronto Atendimento | O usuário verifica os hospitais relevantes e o tempo de atendimento em cada |
| UC002 - Visualizar Mapa de Hospitais | O usuário visualiza o mapa da cidade com hospitais mais próximos |
| UC003 - Visualizar Especialidades | O usuário visualiza para cada unidade de atendimento o tempo de espera com base na especialidade desejada | 
| UC004 - Registrar evento de atendimento | O usuário registra o momento de entrada na unidade, a hora da triagem e a hora do atendimento com o especialista | 
| UC005 - Avaliar atendimento | O usuário avalia o atendimento da unidade | 
| UC006 - Cadastrar dados médicos | O usuário salva seus dados médicos |
| UC007 - Favoritar Hospitais | O usuário favorita os hospitais para priorizar visualização |
| UC008 - Pesquisar Hospitais | O usuário visualiza os hospitais da região em formato de lista e pode pesquisá-los por nome |


```plantuml
@startuml

left to right direction
title Modelo de Caso de Uso

Actor "Paciente" as pc
Actor "Equipe Técnica" as et

rectangle "HUB Médico" {
    pc -- (UC001 - Verificar Tempo em Pronto Atendimento)
    pc -- (UC002 - Visualizar Mapa de Hospitais)
    pc -- (UC003 - Visualizar Especialidades)
    pc -- (UC004 - Registrar evento de atendimento)
    pc -- (UC005 - Avaliar atendimento)
    pc -- (UC006 - Cadastrar dados médicos)
    pc -- (UC007 - Favoritar Hospitais)
    pc -- (UC008 - Pesquisar Hospitais)
}
@enduml
```
# Diagrama de sequência do UC001
```plantuml
@startuml

    actor Paciente as pac
    boundary "Interface Pesquisa" as intpes
    participant "Controller Pesquisa" as contpes
    boundary "Interface Mapa" as intmap
    participant "Controller Mapa" as contmap
    participant Unidades as un
    participant "Unidades Repositorio" as unre
    database "Banco de dados" as bd
    
    alt Por caixa de pesquisa
        contpes -> unre: listarUnidades()
        activate contpes
        activate unre
        unre -> bd: query
        activate bd
        bd --> unre: resultado
        deactivate bd
        unre -> un: listarUnidades(resultado)
        un --> unre: Unidades[ ]
        unre --> contpes: Unidades[ ]
        deactivate unre
        contpes -> intpes: listarUnidades(Unidades[ ])
        activate intpes
        contpes -> intpes: solicitarInformacoes()
        pac -> intpes: Informações da Unidade
        intpes --> contpes: informacoes
        contpes -> unre: getUnidade(informacoes)
        activate unre
        unre -> bd: query
        activate bd
        bd --> unre: resultado
        deactivate bd
        unre -> un: new Unidade(resultado)
        un --> unre: Unidade
        unre --> contpes: Unidade
        deactivate unre
        contpes --> intpes: mostrarUnidade(Unidade)
        deactivate intpes
        deactivate contpes
        

    else Pelo mapa
        contmap -> unre: listarUnidades(Localizacao)
        activate contmap
        activate unre
        unre -> bd: query
        activate bd
        bd --> unre: resultado
        deactivate bd
        unre --> contmap: Unidades[ ]
        deactivate unre 
        contmap -> intmap: mostrarMapa()
        activate intmap
        contmap -> intmap: espalharUnidades(Chunk,Unidades[])
        pac -> intmap: Seleciona a unidade
        intmap -> contmap: getTempo(Unidade)
        contmap -> contmap: getTempo(Unidade)
        contmap --> intmap: Tempo
        deactivate intmap
        deactivate contmap


    end
@enduml
```

# Diagrama de Sequência do UC004
```plantuml
@startuml

@enduml
```

# Diagrama de Classe de Domínio
```plantuml
@startuml

class Paciente {
    nome: String
    sobrenome: String
    dataNascimento: Date
    email: String
    senha: String
}

class Unidade {
    nome: String
    ' Rede pública ou privada
    tipo: String
    rede: Rede
    endereco: String
    numero: String
    complemento: String
    cep: String
    cidade: String
    estado: String
    telefone1: String
    telefone2: String
    especialidades: List<Especialidade>
    tempoMedio: double
}

class Atendimento {
    paciente: Paciente
    unidade: Unidade
    status: String
    especialidadeAtend: Especialidade
    horarioChegada: Date
    horarioTriagem: Date
    horarioAtendimento: Date
    horarioSaida: Date
}

class Especialidade {
    especialidade: String
    getEspecialidade()
}

class RedesMedicas {
    nome: String
    convenios: List<Convenio>
    unidades: List<Unidade>
}

class Convenio {
    nome: String
}

@enduml
```


# Escopo do Diagrama de Classe (apenas para salvar formatação)
Exemplo de uma aula do takase para alterar depois com as classes do nosso projeto


```plantuml
@startuml

hide circle

'skinparam classAttributeIconSize 0
'skinparam classFontStyle bold
'skinparam classFontSize 14
'skinparam classBackgroundColor LightBlue
'skinparam classStereotypeFontSize 12

class Cliente
class Chamado 
class HelpDesk 
class TimeSuporte 
class MembroSuporte 
class Funcionario

Cliente "1" -r- "*" Chamado : Reporta >
Chamado "*" -r- "1" HelpDesk : Registra >
Chamado "*" -d-- "0..1" TimeSuporte : Tratado por >
TimeSuporte o-r- "*" MembroSuporte : Tem membro >
MembroSuporte -u|> Funcionario
HelpDesk -d-|> Funcionario

@enduml
```
