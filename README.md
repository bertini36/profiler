# profiler
The purpose of this project is to identify main topics in personal twitter 
timelines.

# Development environment

# Development environment

**1. System requirements**

- Install Docker and Docker compose

- Install Git

**2. Download code**

``https://github.com/bertini36/profiler``

**3. Set project variables**

- Create .env file

- Set environmental variables in .env using .env-sample model

**4. Create Docker containers**

- Generate image

``make build``

- Run mongo

``make runmongo``

# Possible commands

``make gettimelines timelines=Albert_Rivera,sanchezcastejon,Pablo_Iglesias_,pablocasado_``

# Next work

- Preprocessing textual data
- Find main topics of an user using Latent Dirichlet Allocation algorithm
- Show results using pyLDAvis
