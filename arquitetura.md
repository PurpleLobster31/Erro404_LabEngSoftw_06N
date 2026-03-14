# Arquitetura - MedTime

```
@startuml
title Arquitetura - MedTime

left to right direction

actor Paciente

cloud Internet

rectangle "AWS Cloud" {

    rectangle "Frontend Layer" {
        component "Angular (CloudFront)"
    }

    rectangle "Application Layer" {
        component "FastAPI (EC2)"
    }

    rectangle "Data Layer" {
        database "PostgreSQL (RDS)"
    }

}

Paciente --> Internet
Internet --> "Angular (CloudFront)" : HTTPS
"Angular (CloudFront)" --> "FastAPI (EC2)" : REST API
"FastAPI (EC2)" --> "PostgreSQL (RDS)" : SQL

@enduml
```
