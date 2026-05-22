# Lista de Requisitos

## Requisitos Funcionais

| ID   | Requisito                       | Descricao                                                                                                                                  | Prioridade | Status |
| ---- | ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ | ---------- | ------ |
| RF01 | Verificar tempo de espera       | O sistema permite que o paciente visualize o tempo estimado de espera para atendimento em unidades de pronto atendimento.                  | Alta       | Implementado |
| RF02 | Visualizar mapa de hospitais    | O sistema apresenta um mapa com a localizacao das unidades de saude disponiveis.                                                           | Baixa      | Planejado |
| RF03 | Visualizar especialidades       | O sistema permite visualizar especialidades medicas disponiveis em cada unidade.                                                           | Media      | Planejado |
| RF04 | Registrar evento de atendimento | O sistema permite registrar entrada, triagem e atendimento medico em uma unidade, com validacao de raio.                                   | Alta       | Implementado |
| RF05 | Avaliar atendimento             | O sistema permite que o paciente avalie o atendimento recebido em uma unidade de saude.                                                    | Baixa      | Planejado |
| RF06 | Cadastrar dados medicos         | O sistema permite cadastro de dados medicos basicos do paciente.                                                                           | Baixa      | Planejado |
| RF07 | Favoritar hospitais             | O sistema permite favoritar unidades para priorizar visualizacao.                                                                          | Baixa      | Planejado (UI parcial) |
| RF08 | Pesquisar hospitais             | O sistema permite pesquisa textual de unidades por nome ou endereco na lista carregada.                                                    | Alta       | Implementado |
| RF09 | Atualizar dados de espera       | O sistema recalcula medias automaticamente com base nos atendimentos registrados (ultimos 5).                                               | Alta       | Implementado |

## Requisitos Nao Funcionais

| ID    | Requisito               | Descricao                                                                                                                       | Prioridade | Status |
| ----- | ----------------------- | ------------------------------------------------------------------------------------------------------------------------------- | ---------- | ------ |
| RNF01 | Disponibilidade         | O sistema deve estar disponivel 24 horas por dia, 7 dias por semana.                                                            | Alta       | Nao validado |
| RNF02 | Desempenho              | O tempo de resposta para consultas de hospitais e tempo de espera deve ser inferior a 5 segundos.                               | Media      | Nao validado |
| RNF03 | Escalabilidade          | O sistema deve suportar multiplos usuarios simultaneos sem degradacao significativa de desempenho.                              | Alta       | Nao validado |
| RNF04 | Seguranca               | Os dados dos usuarios devem ser protegidos utilizando autenticacao e criptografia adequadas.                                    | Media      | Planejado |
| RNF05 | Usabilidade             | A interface deve ser simples e intuitiva, permitindo que usuarios encontrem rapidamente informacoes sobre hospitais.            | Alta       | Implementado |
| RNF06 | Compatibilidade         | O sistema deve funcionar em navegadores modernos e dispositivos moveis.                                                         | Media      | Implementado |
| RNF07 | Integracao com API      | O sistema deve consumir uma API para obter e atualizar dados das unidades de saude e tempos de espera.                          | Alta       | Implementado |
| RNF08 | CI/CD                   | O projeto deve possuir pipeline de integracao continua e entrega continua.                                                      | Media      | Implementado |
| RNF09 | Infraestrutura em nuvem | O sistema deve ser implantado utilizando um servico de computacao em nuvem da AWS.                                              | Media      | Planejado |
| RNF10 | Testes                  | O sistema deve possuir testes automatizados para garantir a qualidade das funcionalidades principais.                           | Media      | Implementado |
