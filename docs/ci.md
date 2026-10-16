# Automatische controles (CI)

De workflow staat in [`.github/workflows/ci.yml`](../.github/workflows/ci.yml).
GitHub voert vier controles uit bij elke pull request, bij een push naar `main`
en wanneer de workflow handmatig wordt gestart. Deze controles hebben geen
werkende Nextcloud of toegang tot de VM nodig.

| Check | Wat wordt gecontroleerd? | Wat bewijst dit nog niet? |
|---|---|---|
| Docker Compose | De Compose-configuratie kan met `.env.example` worden ingelezen. | Dat images beschikbaar zijn of de applicatie op de VM werkt. |
| Nginx configuration | `nginx -t` controleert de projectconfiguratie in een tijdelijke Nginx-container. | Bereikbaarheid van Nextcloud, TLS of de firewall op de VM. |
| Documentation links | Lychee controleert of lokale Markdown-links naar bestaande bestanden/mappen verwijzen. | Externe websites, inhoudelijke juistheid of Mermaid-weergave. |
| Secrets scan | Gitleaks scant de opgehaalde Git-historiek; een extra controle weigert lokale `.env`-bestanden. | Dat ieder mogelijk geheim herkenbaar is. |

De workflow gebruikt alleen leesrechten, bewaart geen checkout-credentials en
vraagt geen VM-wachtwoorden of extra GitHub-secrets. Containers voor de
controles krijgen geen netwerktoegang en lezen projectbestanden alleen-lezen.
Docker haalt de vastgelegde toolversies wel vooraf op van hun registries.
De workflow bevat geen deployment naar de VM.

De scan gebruikt [`.gitleaks.toml`](../.gitleaks.toml) met alle standaardregels.
Er is één beperkte uitzondering voor de letterlijke `<apppassword>`-placeholder
in het historische quotatestvoorbeeld `evidence/test-results/test-at-q1-quota.md`.
Andere wachtwoordwaarden en andere bestanden blijven onder de standaardscan vallen.

## Hoe gebruik je dit?

1. Werk op een eigen branch en open na publicatie een pull request.
2. Bekijk onder **Checks** de vier resultaten. Groen betekent dat de
   configuratiecontroles slagen, niet dat alle acceptatietests geslaagd zijn.
3. Bij rood: open de betreffende check en lees de foutmelding. Corrigeer de
   configuratie of link en push de correctie naar dezelfde branch.
4. Bij een gevonden echt geheim: trek het in of wijzig het wachtwoord. Alleen
   het bestand verwijderen is onvoldoende, omdat Gitleaks ook historiek scant.
   Verberg een echte vondst niet met een algemene uitzondering.
5. Laat de wijzigingen reviewen voordat ze worden samengevoegd.

Zolang deze bestanden niet op GitHub zijn gepubliceerd, draait daar nog geen
nieuwe CI-workflow. Een handmatige run via **Actions → CI → Run workflow** is
beschikbaar zodra de workflow op de standaardbranch staat en Actions is
ingeschakeld. Een eerste succesvolle run is nog nodig als uitvoeringsbewijs.

## Lokaal controleren

Vanaf de repositoryroot kan Compose ook zonder draaiende Docker-daemon worden
gevalideerd:

```bash
docker compose --env-file infrastructure/docker/.env.example -f infrastructure/docker/docker-compose.yml config --quiet
```

Met een draaiende Docker-daemon kun je de Nginx-, link- en Gitleaks-commando's
uit de workflow herhalen in Bash. De mounts gebruiken `$PWD` als repositoryroot.
Gebruik de voorbeeldwaarden; echte `.env`-bestanden zijn niet nodig voor CI.
De Nginx-container heeft opzettelijk geen TLS-certificaten van de VM. Als TLS
wordt toegevoegd, moet voor de syntaxiscontrole ook een tijdelijk testcertificaat
worden gemaakt en gemount; productiekeys horen nooit in de workflow.

## Mergen alleen als CI groen is

Een repositorybeheerder kan voor `main` een branch ruleset of branch protection
instellen. Selecteer na de eerste run deze checks als verplicht:

- Docker Compose
- Nginx configuration
- Documentation links
- Secrets scan

Dat is een GitHub-instelling; het toevoegen van de workflow stelt deze
bescherming niet automatisch in.

## Verificatie van deze eerste versie

Op 2026-10-16 zijn Compose-validatie, workflowcontrole met Actionlint, lokale
Markdown-links met Lychee en de Git-historiekscan met Gitleaks lokaal geslaagd.
De nieuwe bestanden zijn ook afzonderlijk op secrets gecontroleerd. De drie
vastgelegde containerimages zijn beschikbaar in hun registries.

De Docker-daemon draaide op de ontwikkelcomputer niet. De containeruitvoering,
inclusief `nginx -t`, is daarom nog niet lokaal getest. De eerste volledige
GitHub Actions-run moet dit nog bevestigen.

## Bronnen

- [GitHub Actions: checkout](https://github.com/actions/checkout)
- [Docker Compose: config](https://docs.docker.com/reference/cli/docker/compose/config/)
- [Nginx: command-line parameters](https://nginx.org/en/docs/switches.html)
- [Lychee](https://github.com/lycheeverse/lychee)
- [Gitleaks](https://github.com/gitleaks/gitleaks)
