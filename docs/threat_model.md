# Threat Model

LLM Prompt Injection Tester v1 focuses on defensive testing of prompt-injection risks.

## Assets Being Protected

This project simulates protection of:

- System instructions
- Developer instructions
- Hidden context
- Fake secrets
- Fake customer records
- Fake tool actions

## Threats Tested

The test cases cover:

- Ignoring previous instructions
- Revealing system prompts
- Pretending safety rules do not apply
- Extracting hidden context
- Overriding developer instructions
- Jailbreak roleplay attempts
- Simulated data exfiltration
- Simulated tool misuse
- Policy override attempts
- Prompt leaking attempts

## Out of Scope

This project does not test or provide:

- Real credential theft
- Malware
- Real exploit payloads
- Unauthorized system access
- Production red-team operations

## Defensive Purpose

The goal is to help developers understand how prompt-injection failures can appear and how to document them safely.
