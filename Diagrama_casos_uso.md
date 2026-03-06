# Casos de Uso

| Nome | Descrição | 
| :--- | :---: | 
| UC001 - Verificar Tempo em Pronto Atendimento | O usuário verifica os hospitais relevantes e o tempo de atendimento em cada |
| UC002 - Visualizar Mapa de Hospitais | O usuário visualiza o mapa de hospitais da cidade |
| UC003 - Visualizar Especialidades | O usuário visualiza para cada unidade de atendimento o tempo de espera com base na especialidade desejada | 
| UC004 - Registrar evento de atendimento | O usuário registra o momento de entrada na unidade, a hora da triagem e a hora do atendimento com o especialista | 
| UC005 - Avaliar atendimento | O usuário avalia o atendimento da unidade | 
| UC006 - Cadastrar dados médicos | O usuário salva seus dados médicos |
| UC007 - Favoritar Hospitais | O usuário favorita os hospitais para priorizar visualização |
| UC008 - Pesquisar Hospitais | O usuário pesquisa hospitais por nome |


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