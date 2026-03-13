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
    boundary "Interface Paciente" as intcli
    participant Controller as cont
    database "Banco de dados" as bd
    
    alt Por caixa de pesquisa
        pac -> intcli: Seleciona a lista de unidades
        intcli -> cont: ListarUnidades()
        cont -> bd: Busca unidades da cidade
        bd --> cont: Unidades
        cont --> intcli: MostrarUnidades()
        pac -> intcli: Seleciona a unidade
        intcli -> cont: getTempo(Unidade)
        alt Se disponível
            cont --> intcli: Tempo
        else Senão
            cont --> intcli: Null
        end

    else Pelo mapa
        pac -> intcli: Clica em uma unidade
        intcli -> cont: getTempo(Unidade)
        alt Se disponível
            cont --> intcli: Tempo
        else Senão
            cont --> intcli: Null
        end
    end
@enduml
```

# Diagrama de Sequência do UC003
```plantuml
@startuml

    actor Paciente as pac
    boundary "Interface paciente" as int
    participant Controller as cont

    alt Por unidade
        cont -> int: listarUnidades()
        activate cont
        activate int
        pac -> int: Escolher unidade
        int -> cont: mostrarUnidade()
        cont --> int: Unidade
        deactivate int
        deactivate cont
        
    else Por filtro
    end



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
