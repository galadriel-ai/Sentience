//replace console.log with document.write to make the behavior visible
console.log = (m) => {
    document.write(`${m}<br>`)
}

import Sentience from '../sentience.min.js'

// TODO:
const GALADRIEL_API_KEY = "TODO"

function verifySignatures() {
    const EXAMPLE_VALID = {
        hash: '5cff951d70ad5d4da7c12187331d98eabbf4023f7aeb547e949224ddd1420fc7',
        public_key: '835cc0e84c2a5190561d7c2eaf10eb2597cbe7a71541084c5edea32b60bc5e68',
        signature: '819218f6ad5a8ec86091afc1dfbecc5d21384d62f1df0c649ab0c351e515e825fda72d124091418b3cc4a3be35b20dd471b8f8447a448712315b19ecaef34206',
    }

    const EXAMPLE_INVALID_HASH = {
        hash: '5cff951d70ad5d4da7c12187331d98eabbf4023f7aeb547e949224ddd1420fc8',
        public_key: '835cc0e84c2a5190561d7c2eaf10eb2597cbe7a71541084c5edea32b60bc5e68',
        signature: '819218f6ad5a8ec86091afc1dfbecc5d21384d62f1df0c649ab0c351e515e825fda72d124091418b3cc4a3be35b20dd471b8f8447a448712315b19ecaef34206',
    }
    console.log("Sentience.verifySignature(EXAMPLE_VALID):")
    console.log(Sentience.verifySignature(EXAMPLE_VALID));

    console.log("Sentience.verifySignature(EXAMPLE_INVALID_HASH):")
    console.log(Sentience.verifySignature(EXAMPLE_INVALID_HASH));
}


async function apiCalls() {
    console.log("\n\n==== Get History ====")
    const history = await Sentience.getHistory(GALADRIEL_API_KEY)
    document.body.insertAdjacentHTML('beforeend', `${JSON.stringify(history)}<br>`)
}

verifySignatures()
apiCalls()
    .catch(e => document.body.insertAdjacentHTML('beforeend', `${e}<br>`))