# 🔧 Diagramas Técnicos del Sistema SoftSkillsVision

## 📊 Diagrama de Arquitectura de Componentes

```mermaid
graph TB
    subgraph "Frontend Layer"
        A[Angular App] --> B[Components]
        B --> C[Services]
        C --> D[Models]
    end
    
    subgraph "API Gateway"
        E[FastAPI Router] --> F[Endpoints]
        F --> G[Authentication]
    end
    
    subgraph "Business Logic Layer"
        H[Face Video Recognition] --> I[MediaPipe Detector]
        H --> J[FER Detector]
        K[Drive Utils] --> L[Google Drive API]
    end
    
    subgraph "Data Layer"
        M[SQL Server] --> N[Candidates Table]
        M --> O[Emotions Table]
        M --> P[Jobs Table]
        Q[Google Drive] --> R[Video Files]
    end
    
    subgraph "External Services"
        S[MediaPipe Models]
        T[FER Models]
        U[Google Cloud]
    end
    
    A --> E
    E --> H
    H --> M
    H --> Q
    I --> S
    J --> T
    L --> U
```

## 🔄 Diagrama de Secuencia - Procesamiento de Video

```mermaid
sequenceDiagram
    participant U as Usuario
    participant F as Frontend
    participant A as API
    participant P as Processor
    participant M as MediaPipe
    participant E as FER
    participant D as Database
    
    U->>F: Selecciona video
    F->>A: POST /procesar-video
    A->>P: process_video()
    P->>P: Validar archivo
    P->>M: Inicializar detector
    P->>E: Inicializar detector
    
    loop Para cada frame
        P->>M: detect_landmarks()
        M-->>P: landmarks
        P->>E: detect_emotion()
        E-->>P: emotion + score
        P->>P: Anotar frame
    end
    
    P->>P: Calcular promedios
    P->>D: Guardar resultados
    D-->>P: Confirmación
    P-->>A: Resultados
    A-->>F: JSON Response
    F-->>U: Mostrar resultados
```

## 🗄️ Diagrama de Base de Datos

```mermaid
erDiagram
    CANDIDATOS {
        int id PK
        string nombre
        string email
        string telefono
        string video_url
        datetime fecha_registro
        datetime fecha_evaluacion
    }
    
    CARGOS {
        int id PK
        string nombre
        string descripcion
        string requisitos
        datetime fecha_creacion
    }
    
    EMOCIONES {
        int id PK
        string nombre
        string descripcion
        string codigo
    }
    
    HABILIDADES_BLANDAS {
        int id PK
        string nombre
        string descripcion
        int cargo_id FK
    }
    
    PUNTUACIONES_EMOCIONES {
        int id PK
        int candidato_id FK
        int emocion_id FK
        float puntuacion
        datetime timestamp
    }
    
    RANGOS_EMOCIONES_CARGO {
        int id PK
        int cargo_id FK
        int emocion_id FK
        float rango_minimo
        float rango_maximo
    }
    
    EVALUACIONES {
        int id PK
        int candidato_id FK
        int cargo_id FK
        string resultado
        float puntuacion_total
        datetime fecha_evaluacion
    }
    
    CANDIDATOS ||--o{ PUNTUACIONES_EMOCIONES : tiene
    EMOCIONES ||--o{ PUNTUACIONES_EMOCIONES : mide
    CARGOS ||--o{ HABILIDADES_BLANDAS : requiere
    CARGOS ||--o{ RANGOS_EMOCIONES_CARGO : define
    EMOCIONES ||--o{ RANGOS_EMOCIONES_CARGO : especifica
    CANDIDATOS ||--o{ EVALUACIONES : evaluado
    CARGOS ||--o{ EVALUACIONES : para
```

## 🌐 Diagrama de Red y Comunicación

```mermaid
graph LR
    subgraph "Cliente"
        A[Navegador Web]
    end
    
    subgraph "Servidor de Aplicación"
        B[Angular Dev Server<br/>:4200]
        C[FastAPI Server<br/>:8000]
        D[Spring Boot Server<br/>:8080]
    end
    
    subgraph "Servicios Externos"
        E[Google Drive API]
        F[MediaPipe Models]
        G[FER Models]
    end
    
    subgraph "Base de Datos"
        H[SQL Server<br/>:1433]
    end
    
    subgraph "Almacenamiento"
        I[Google Drive<br/>Videos]
        J[Local Storage<br/>Temp Videos]
    end
    
    A --> B
    B --> C
    B --> D
    C --> E
    C --> F
    C --> G
    C --> J
    D --> H
    E --> I
```

## 🔐 Diagrama de Seguridad y Autenticación

```mermaid
flowchart TD
    A[Usuario] --> B[Login Form]
    B --> C{Validar Credenciales}
    C -->|Válido| D[Generar JWT Token]
    C -->|Inválido| E[Error de Autenticación]
    
    D --> F[Almacenar Token]
    F --> G[Redirigir a Dashboard]
    
    G --> H[Request con Token]
    H --> I{Validar Token}
    I -->|Válido| J[Procesar Request]
    I -->|Inválido| K[Error 401]
    
    J --> L{Verificar Permisos}
    L -->|Autorizado| M[Ejecutar Acción]
    L -->|No Autorizado| N[Error 403]
    
    M --> O[Respuesta]
    O --> P[Actualizar UI]
    
    E --> Q[Mostrar Error]
    K --> Q
    N --> Q
```

## 📈 Diagrama de Flujo de Datos

```mermaid
flowchart LR
    subgraph "Entrada"
        A[Video de Entrevista]
        B[Configuración de Cargo]
    end
    
    subgraph "Procesamiento"
        C[Extracción de Frames]
        D[Detección de Landmarks]
        E[Detección de Emociones]
        F[Cálculo de Promedios]
    end
    
    subgraph "Análisis"
        G[Comparación con Rangos]
        H[Evaluación de Soft Skills]
        I[Generación de Score]
    end
    
    subgraph "Salida"
        J[Reporte de Emociones]
        K[Evaluación Final]
        L[Recomendaciones]
    end
    
    A --> C
    C --> D
    C --> E
    D --> F
    E --> F
    F --> G
    B --> G
    G --> H
    H --> I
    I --> J
    I --> K
    I --> L
```

## 🚀 Diagrama de Despliegue

```mermaid
graph TB
    subgraph "Desarrollo"
        A[Developer Machine]
        B[Git Repository]
        C[Local Database]
    end
    
    subgraph "Testing"
        D[Test Server]
        E[Test Database]
        F[Test Google Drive]
    end
    
    subgraph "Producción"
        G[Production Server]
        H[Production Database]
        I[Production Google Drive]
        J[Load Balancer]
    end
    
    subgraph "Monitoreo"
        K[Logs]
        L[Metrics]
        M[Alerts]
    end
    
    A --> B
    B --> D
    D --> G
    G --> J
    J --> H
    J --> I
    G --> K
    K --> L
    L --> M
```

## 🔄 Diagrama de Estados - Proceso de Evaluación

```mermaid
stateDiagram-v2
    [*] --> VideoCargado
    VideoCargado --> ValidandoArchivo
    ValidandoArchivo --> ArchivoValido : Archivo OK
    ValidandoArchivo --> ErrorArchivo : Archivo Inválido
    
    ArchivoValido --> InicializandoDetectores
    InicializandoDetectores --> ProcesandoFrames
    ProcesandoFrames --> DetectandoLandmarks
    DetectandoLandmarks --> DetectandoEmociones
    DetectandoEmociones --> AnotandoFrame
    AnotandoFrame --> ProcesandoFrames : Más Frames
    AnotandoFrame --> CalculandoPromedios : Fin de Frames
    
    CalculandoPromedios --> EvaluandoSoftSkills
    EvaluandoSoftSkills --> GenerandoReporte
    GenerandoReporte --> GuardandoResultados
    GuardandoResultados --> [*]
    
    ErrorArchivo --> [*]
```

## 📊 Diagrama de Métricas y Monitoreo

```mermaid
graph LR
    subgraph "Aplicación"
        A[FastAPI App]
        B[Angular App]
        C[Spring Boot App]
    end
    
    subgraph "Métricas"
        D[Response Time]
        E[Error Rate]
        F[Throughput]
        G[CPU Usage]
        H[Memory Usage]
    end
    
    subgraph "Logs"
        I[Application Logs]
        J[Error Logs]
        K[Access Logs]
    end
    
    subgraph "Alertas"
        L[High Error Rate]
        M[Slow Response]
        N[High CPU Usage]
        O[Low Memory]
    end
    
    A --> D
    A --> E
    A --> F
    B --> G
    C --> H
    
    A --> I
    B --> J
    C --> K
    
    D --> M
    E --> L
    G --> N
    H --> O
```

## 🎯 Diagrama de Casos de Uso Detallado

```mermaid
graph TD
    subgraph "Actores"
        A[Reclutador]
        B[Administrador]
        C[Sistema]
    end
    
    subgraph "Casos de Uso"
        D[Procesar Video]
        E[Gestionar Candidatos]
        F[Configurar Cargos]
        G[Generar Reportes]
        H[Evaluar Soft Skills]
    end
    
    subgraph "Sistemas Externos"
        I[Google Drive]
        J[MediaPipe]
        K[FER]
    end
    
    A --> D
    A --> E
    A --> G
    A --> H
    B --> F
    B --> G
    
    D --> I
    D --> J
    D --> K
    E --> C
    F --> C
    G --> C
    H --> C
```

---

## 📋 Resumen de Diagramas

1. **Arquitectura de Componentes**: Muestra la estructura general del sistema
2. **Secuencia**: Detalla el flujo de procesamiento de videos
3. **Base de Datos**: Estructura de datos y relaciones
4. **Red y Comunicación**: Conectividad entre servicios
5. **Seguridad**: Flujo de autenticación y autorización
6. **Flujo de Datos**: Transformación de datos en el sistema
7. **Despliegue**: Arquitectura de infraestructura
8. **Estados**: Estados del proceso de evaluación
9. **Métricas**: Monitoreo y observabilidad
10. **Casos de Uso**: Interacciones de usuarios con el sistema

Estos diagramas proporcionan una visión completa y técnica del sistema SoftSkillsVision, facilitando la comprensión, mantenimiento y evolución del mismo.
