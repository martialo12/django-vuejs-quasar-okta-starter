# (frontend)

Cloud portal

## Install the dependencies
```bash
yarn
# or
npm install
```

### Start the app in development mode (hot-code reloading, error reporting, etc.)
```bash
quasar dev
```


### Lint the files
```bash
yarn lint
# or
npm run lint
```


### Format the files
```bash
yarn format
# or
npm run format
```



### Build the app for production
```bash
quasar build
```

### Customize the configuration
See [Configuring quasar.config.js](https://v2.quasar.dev/quasar-cli-vite/quasar-config-js).

```
graph LR
    A[Utilisateur] -->|Utilise| B(Frontend Quasar + Nginx)
    B -->|API Calls| C[Backend Django]
    C -->|Auth Request| D{Okta Authentification OAuth2}
    C -->|Database Queries| E[PostgreSQL]
    D -->|Auth Response| C
    C -->|Session Data| B
    B -.->|Servi via| F[Docker]
    C -.->|Conteneurisé par| F
    E -.->|Géré via| G[Docker Compose]

    classDef default fill:#f9f,stroke:#333,stroke-width:2px;
    classDef docker fill:#bbf,stroke:#f66,stroke-width:2px,stroke-dasharray: 5, 5;
    class B,F,G style fill:#bbf,stroke:#333,stroke-width:2px;
```