# Problem Statement

Project ID: SYS-002
Project Path: 04_INITIATIVES/SYSTEM_PORTFOLIO/SYS-002_GMAIL_INTEGRATION

## Current Problem
- Gmail integration is already active, but the System Portfolio still represents it as a candidate "read-only" item rather than a governed active integration surface.

## Impact
- Without a canonical packet, the actual Gmail scope, including controlled label writes, audit requirements, and runtime limits, can drift away from the project layer.

## Why Now
- Gmail is already part of the live matter-admin operating surface, so governance needs to catch up to runtime reality before more behavior is layered onto it.
