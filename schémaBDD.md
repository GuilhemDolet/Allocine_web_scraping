```mermaid
---
title: Allocine Scrapping BDD
---
erDiagram
    SERIES{
        integer serie_id PK
        string title
        string status
        float public_score
        float press_score
        string date_of_release
        integer seasons_nbr
        integer episodes_nbr
        string language
        string duration
        string synopsis
    }

    PEOPLE{
        integer people_id PK
        string name
    }


    MOVIES{
        integer movie_id PK
        string title
        float public_score
        float press_score
        string date_of_release
        string language
        string duration
        string synopsis
    }

   

    GENRE_BY_MOVIES{
        string genre PK
        string movie_id FK, PK
    }

    GENRE_BY_SERIES{
        string genre PK
        string serie_id FK, PK
    }

    COUNTRIES_BY_MOVIES{
        string countrie PK
        string movie_id FK, PK
    }

    COUNTRIES_BY_SERIES{
        string countrie PK
        string movie_id FK, PK
    }

    ASSOCIATED_ROLE_MOVIES{
        string people_id FK, PK
        string movie_id FK, PK
    }

    ASSOCIATED_ROLE_SERIES{
        string people_id FK, PK
        string serie_id FK, PK
    }

    ASSOCIATED_REALISATOR_BY_MOVIES{
        string people_id FK, PK
        string movie_id FK, PK
    }

    ASSOCIATED_REALISATOR_BY_SERIES{
        string people_id FK, PK
        string seerie_id FK, PK
    }


    MOVIES }o--o{ GENRE_BY_MOVIES : ""
    MOVIES }o--o{ COUNTRIES_BY_MOVIES : ""
    SERIES }o--o{ GENRE_BY_SERIES : ""
    SERIES }o--o{ COUNTRIES_BY_SERIES : ""
    PEOPLE }o--o{ MOVIES: "many_to_many"
    PEOPLE }o--o{ SERIES: "many_to_many"
    PEOPLE ||--o{ ASSOCIATED_ROLE_MOVIES : "one_to_any"
    MOVIES ||--o{ ASSOCIATED_ROLE_MOVIES : "one_to_any"
    PEOPLE ||--o{ ASSOCIATED_ROLE_SERIES : "one_to_any"
    SERIES ||--o{ ASSOCIATED_ROLE_SERIES : "one_to_any"
    PEOPLE ||--o{ ASSOCIATED_REALISATOR_BY_MOVIES : "one_to_any"
    MOVIES ||--o{ ASSOCIATED_REALISATOR_BY_MOVIES : "one_to_any"
    PEOPLE ||--o{ ASSOCIATED_REALISATOR_BY_SERIES : "one_to_any"
    SERIES ||--o{ ASSOCIATED_REALISATOR_BY_SERIES : "one_to_any"
