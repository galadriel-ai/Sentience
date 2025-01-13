# Galadriel JS SDK - Sentience

### Setup

```shell
npm install sentience-js
```

### Usage

Make LLM API call using OpenAI API spec and verify the signature:

```javascript
const OpenAI = require('openai');
const Sentience = require('sentience-js');

const client = new OpenAI({
    apiKey: process.env['GALADRIEL_API_KEY'], // This is the default and can be omitted
    baseURL: "https://api.galadriel.com/v1/verified",
});

async function main() {
    const chatCompletion = await client.chat.completions.create({
        messages: [{role: 'user', content: 'Say this is a test'}],
        model: 'gpt-4o',
    });

    const result = Sentience.verifySignature(chatCompletion)
    console.log("Signature is valid: " + result)
}

main();
```

Fetch all previous verified inference requests:

```javascript
const Sentience = require('sentience-js');

async function main() {
    const result = await Sentience.getHistory(process.env['GALADRIEL_API_KEY'])
    console.log(result)
}

main()
```

Fetch a single verified inference request by hash:

```javascript
const Sentience = require('sentience-js');

async function main() {
    const result = await Sentience.getByHash(
        process.env['GALADRIEL_API_KEY'],
        "5cff951d70ad5d4da7c12187331d98eabbf4023f7aeb547e949224ddd1420fc7"
    )
    console.log(result)
}

main()

```
