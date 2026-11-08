# Content policy

This policy defines what may appear in public KFlowLabs posts and what must stay internal. When in doubt, exclude the material and ask the author to clear the exact excerpt.

## Public by default

- General engineering explanations and public upstream documentation.
- The author's own career history, including public employer names, unless a specific incident or customer is identifiable.
- Sanitized examples with placeholder hosts, IPs, phone numbers, tokens, and channel IDs.
- Historical observations clearly labeled as historical.
- Code sketches labeled as sketches when they were not freshly tested.

## Private or excluded unless the exact material is cleared

- Student, staff, customer, or end-user personal data.
- Contracts, fees, margins, sales pipeline, pricing, and commercial terms.
- Credentials, API tokens, private keys, session cookies, and internal hostnames.
- Private addresses, personal phone numbers, and unlisted contact details.
- Customer screenshots, production dashboards, order details, and incident timelines.
- Internal operating numbers, unless they are necessary for the explanation and explicitly approved.
- Security-control bypass details, even when obtained on authorized test devices. Describe the test environment and the boundary, not an exploit recipe.

## Authorization boundary

SMS, OTP, payment, and account tests must use organization-owned devices and accounts approved for testing. Do not describe or imply interception of another person's messages. Do not publish a tool that exposes an unauthenticated control endpoint.

## AX field notes

A new AX field note without verifiable facts remains a draft. Observations must say what was measured, on which environment, and at what time. Do not turn a demo into a customer case study. Do not claim a tool is installed, a gate ran, or a channel was published without a recorded result.

## Automation boundary

Do not run unattended scrapes of internal repositories or customer systems. Do not add network publishing scripts or assume legacy API tokens. Channel account access is handled separately by the site owner.

## Reviews

Before publication, check:

1. Names, numbers, and quotes against the fact ledger.
2. Screenshots and diagrams for identifiers.
3. Code for real credentials or internal endpoints.
4. Claims about redirects, canonicals, tool support, and measured results.
5. Whether the exact confidential material has explicit clearance.
