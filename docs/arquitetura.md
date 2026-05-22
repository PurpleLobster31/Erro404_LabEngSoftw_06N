# Arquitetura - MedTime (as-is)

O projeto e executado localmente via Docker Compose e, no deploy alvo, em uma unica instancia EC2 contendo frontend, backend e banco no mesmo host. O frontend consome a API via HTTP e o backend acessa o banco PostGIS para consultas geoespaciais.

```plantuml
@startuml
title Arquitetura - MedTime (as-is)

left to right direction

actor Paciente

cloud Internet

rectangle "AWS EC2 (Docker)" {
    component "Angular (Frontend)"
    component "FastAPI (Backend)"
    database "PostgreSQL + PostGIS"
}

Paciente --> Internet
Internet --> "Angular (Frontend)" : HTTPS
"Angular (Frontend)" --> "FastAPI (Backend)" : REST API
"FastAPI (Backend)" --> "PostgreSQL + PostGIS" : SQL + PostGIS

@enduml
```
