# LLM-Switcher 
<p> Dynamically switch between different LLM's if you reach a token limit, without stopping flow </p>

## Use Cases 

<p> Here are a few use cases where I found this useful </p>

- Writing Tools.. you might reach a token count on a writing tool and want to keep going. To ensure consistency, prompts exist that work to bring out similar results from each LLM without you having to change your existing flow that much 

- Code.. For codegen tools or companies this could be really useful. Right now I have claude-3-opus in cursor.sh but I would love to be able to switch between different models if the output is better witohut having to constantly add my API key. 


## Install 

```
pip install llm-switcher
```


## Disclaimer 

<p> This is for pure experimental purposes. If you find this useful or want to make it better feel free to open a PR </p>