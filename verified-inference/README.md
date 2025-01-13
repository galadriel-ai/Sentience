# Verified Inference

Underlying TEE architecture that powers Proof of Sentience SDK.

## [Enclave](enclave)
Scripts to build and run the code in [Amazon Nitro Enclaves](https://aws.amazon.com/ec2/nitro/nitro-enclaves/).

## [Host](host)
A server which listens for HTTP request and forwards them to the API running inside the enclave.

## [Solana attestation contract](solana-attestation-contract)
Solana contract to which proofs of inference are posted.

## [Verify](verify)
Instructions and code for verifying the TEE.