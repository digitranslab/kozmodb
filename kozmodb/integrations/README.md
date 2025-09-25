KozmoDB integrations are broadly categorized into two types:

1. Datasources

Datasources in KozmoDB refer to the different data storage and management systems that you can connect with KozmoDB. These include traditional databases as well as data accessible through APIs. There are few different types of Datasources:

* [Databases](https://docs.kozmodb.com/integrations/data-integrations/all-data-integrations)
* [Applications](https://docs.kozmodb.com/integrations/app-integrations/binance)
* [Vector Databases](https://docs.kozmodb.com/integrations/vector-db-integrations/chromadb)

2. AI-Engines

[AI-Engines](https://docs.kozmodb.com/ai-engines/overview) in KozmoDB are the core of our AI and ML capabilities. This category encompasses a diverse range of artificial intelligence and machine learning modeling options, including:

  * Generative AI: Unlock the potential of generative algorithms for innovative solutions.
  * Automated Machine Learning (Auto-ML): Simplify complex ML processes with automation, making AI more accessible. 


## Directory Overview

* `/handlers`: Contains code for each integration, organized by handler names.
* `/utilities`: Utilities for tasks like parsing dates, filtering SQL, and managing dependencies.
* `/libs`: Libraries used across various handlers.

## Contributing

If you're interested in contributing a new integration, please refer to our detailed `How To` guidelines:

* [Building a Database Handler](https://docs.kozmodb.com/contribute/data-handlers)
* [Building a Machine Learning Handler](https://docs.kozmodb.com/contribute/ml-handlers)
* [Building an Application Handler](https://docs.kozmodb.com/contribute/app-handlers)