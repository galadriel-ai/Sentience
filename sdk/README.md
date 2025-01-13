# Proof of Sentience SDK

This directory contains Python and Javascript SDKs for Proof of Sentience. These SDKs are an abstraction layer built for improved developer experience on top of Galadriel's [verified inference](/verified-inference/) architecture.

## Quickstart
To get started with building verifieable AI agents go to Proof of Sentience [SDK quickstart docs](https://docs.galadriel.com/for-agents-developers/quickstart).


## High Level Overview
1. Your AI Agent calls an LLM API for inference using the SDK.

2. Our back-end runs inside TEEs - fully encrypted hardware enclaves.

3. TEE back-end makes the calls to LLM APIs and returns the responses with verifiable proofs. 

4. We also provide an SDK to easily verify inferences and retrieve a list of previous messages to show as logs.

![](/assets/SDK.png)


