# Automatische controles (CI)

GitHub Actions voert bij een pull request, een push naar `main` en een handmatige
start de [CI-workflow](../.github/workflows/ci.yml) uit.

| Controle | Doel |
|---|---|
| Docker Compose | Configuratie inlezen met voorbeeldwaarden |
| Monitoring | Prometheus-configuratie, regels en bestaande Linux-unit-tests controleren |
| Nginx | Configuratiesyntaxis controleren met een tijdelijk certificaat |
| Documentatielinks | Lokale links naar bestanden en mappen controleren |
| Secrets | Git-historiek scannen en echte `.env`-bestanden weigeren |

## Resultaat bekijken

Open op GitHub de commit of pull request en kies **Checks**.
Bij een rode controle open je de log, pas je het betreffende bestand aan en voer je
de controle opnieuw uit. Een groene CI-run bevestigt deze repositorycontroles;
de workflow past niets aan op de VM.

De controles gebruiken voorbeeldconfiguratie en tijdelijke containers.
Plaats geen productiegegevens of private sleutels in de workflow.

## Lokaal controleren

Vanuit de repositoryroot:

```bash
docker compose --env-file infrastructure/docker/.env.example -f infrastructure/docker/docker-compose.yml config --quiet
```

De monitoring-/back-up-unit-tests vereisen Linux met Python 3 en Bash:

```bash
python3 -B -m unittest discover -s infrastructure/docker/monitoring/tests -v
```

Dit zijn technische codecontroles, geen aparte acceptatietestverplichting.
