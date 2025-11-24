Clone official subnet template: git clone https://github.com/opentensor/bittensor-subnet-template.git and copy/merge the above template/ and neurons/ into that template. 
GitHub

Install deps: python -m venv venv && source venv/bin/activate && pip install -r requirements.txt

Start your FastAPI agent (for agent-to-agent): uvicorn byte_alchemist.api:app --host 0.0.0.0 --port 8000

Test miner locally: echo '{"prompt":"write a function to add two numbers"}' | python neurons/miner.py

Create subnet on testnet via BTCLI: btcli subnet create --network test and save the netuid. 
docs.learnbittensor.org

Register validators/miners per the subnet template docs so they connect to your netuid
