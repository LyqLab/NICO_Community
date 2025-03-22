

# Agent Sales: I Should build cognition of my Customers!

<p align="center" width="100%">
<img src="map1.png" alt="NICO Supermarket" style="width: 80%; min-width: 300px; display: block; margin: auto;">
</p>

A virtual supermarket is embedded into a town comprising 12 LLM-driven agents. This allows the observation of the dynamic interaction and mental evolution process between consumer-type and seller-type agents. Based on continuously adjusted cognition, the agents with different identities will achieve behaviours such as dynamic scheduling, environmental perception and exploration, conversation content control, sales and purchase decision-making.

<p align="center" width="100%">
<img src="NICO.mp4" alt="NICO Supermarket" style="width: 80%; min-width: 300px; display: block; margin: auto;">
</p>

### Step 0. Deployment Generative Agents and Llama2

Our work is based on `Generative Agents`, so be sure to deploy and debug this project first, and then add our designs to it to improve it.

In order to reduce the cost of using LLM, we use Llama2 to replace part of the GPT-3.5. Deploy llama2 to the server side and call it through flask. The client-side code can be referenced in our `client_llama2\gpt_structure.py`.


### Step 1. Add town files

The subfolders and files in the folder `the_ville` correspond to the directories in the `generative agents` project: `environment\frontend_server\static_dirs\assets`. Replace or add the above related files.


### Step 2. Add character files

Put `base_NICO_community_n12` in the `storage` folder

Christopher Lee: Hawks Steakhouse owner
Elizabeth Lee: Lough Pub owner
Ava Lee: Adamas Gym instructor
James Lee: NICO Supermarket Salesman 
Michael Smith: Western Bank president
Emily Smith: Capybara Bakery owner
Isabella Smith: Lough Pub bartender
Andrew Taylor: NICO Supermarket manager
David Taylor: Game programmer
Charlotte Moore: NICO Supermarket Salesman 
Daniel Wilson: NICO Supermarket Salesman 
Sophia Thompson: July Hotel Manager

### Step 3. Add the mind module to the `persona` directory 

includes 4 main files:
mind_self.py
mind4others_memory.py
mind4things_memory.py
mind4town_memory.py

### Step 4. Add the cognition related prompt to the `prompt_template` directory

includes 10 pompt files in v4_mind folder:
decide_to_buy_v3
decide_to_talk_v3
impact4RTD_event
something_to_buy_v3
update_cognition4thing_event
update_cognition4town_event
update_mind4other_event
update_mind4self_event
update_needs4other_event
update_needs4self_event


### We will publish the complete project once this article has been accepted



