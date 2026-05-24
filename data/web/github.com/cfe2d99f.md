---
domain: github.com
fetch_date: '2026-05-18T12:35:30.112079'
status: ok
url: https://github.com/philterd/phileas
---

- For an open source API-based redaction app built on Phileas, please see Philter.

Phileas is a Java library to deidentify and redact PII, PHI, and other sensitive information from text. Given text or documents (PDF), Phileas analyzes the text searching for sensitive information such as persons' names, ages, addresses, and many other types of information. Phileas is highly configurable through its settings and policies.

When sensitive information is identified, Phileas can manipulate the sensitive information in a variety of ways. The information can be replaced, encrypted, anonymized, and more. The user chooses how to manipulate each type of sensitive information. We refer to each of these methods in whole as "redaction."

Information can be redacted based on the content of the information and other attributes. For example, only certain persons' names, only zip codes meeting some qualification, or IP addresses that match a given pattern.

For Phileas' documentation, please see https://philterd.github.io/phileas/.

This is the *primary* Phileas repository, but it has been ported to a few other languages. Functionality between this Java version and the versions for other languages will differ. Some features available here are not (yet) available in the ports, and there may be features in the ports that are not available in the Java version. Refer to the documentation for each port for more information.

Development will likely focus on the Java version since it powers Philter and other applications.

- Phileas (Python) - https://github.com/philterd/phileas-python (docs)
- Phileas (.NET) - https://github.com/philterd/phileas-net (docs)
- Phileas (Go) - https://github.com/philterd/go-phileas

- Phileas can identify and redact over 30 types of sensitive information (see list below).
- Phileas can evaluate conditions when redacting (only zip codes with population less than some value, only ages > 30, only when sentiment is a certain value, etc.).
- Phileas can perform sentiment and offensiveness classification.
- Phileas can redact, encrypt, and anonymize sensitive information.
- Phileas can replace persons names with random names, dates with similar but random dates, etc.
- Phileas can disambiguate types of sensitive information (i.e. SSN vs. phone number).
- Phileas can deidentify text consistently ("John Smith" is replaced consistently in certain documents).
- Phileas can shift dates or replace dates with approximate representations (i.e. "3 months ago").
- Phileas uses policies to define what sensitive information to find and how to redact it.

This list might be outdated. Please check the individual filter classes for details.

- Person's Names - Multiple methods, e.g. NER, dictionary, census data
- Physician Names
- First Names
- Surnames

- Medical Conditions

- Ages
- Bank Account Numbers
- Bitcoin Addresses
- Credit Cards
- Currency (USD)
- Dates (in addition to birthdates and deathdates)
- (US) Driver's License Numbers
- Email Addresses
- IBAN Codes
- IP Addresses (IPv4 and IPv6)
- MAC Addresses
- (US) Passport Numbers
- Phone Numbers
- Phone Number Extensions
- Sections (of a document)
- SSNs and TINs
- Tracking Numbers (UPS / FedEx / USPS)
- URLs
- VINs
- Zip Codes

- Cities
- Counties
- Hospitals
- States
- State Abbreviations

- Dictionary
- Identifier

After cloning, run `git lfs pull`

to download models needed for unit tests. Phileas can then be built with `mvn clean install`

.

Phileas snapshots and releases as of version 2.12.1 are available in Maven Central. Previous versions were in the Philterd repository.

Add the Phileas dependency to your project:

```
<dependency>
<groupId>ai.philterd</groupId>
<artifactId>phileas</artifactId>
<version>3.0.0</version>
</dependency>
```


Create a `FilterService`

, using a `PhileasConfiguration`

, and call `filter()`

on the service:

```
Properties properties = new Properties();
PhileasConfiguration phileasConfiguration = new PhileasConfiguration(properties);
PlainTextFilterService filterService = new PlainTextFilterService(phileasConfiguration);
FilterResponse response = filterService.filter(policies, context, text);
```


The `policies`

is a list of `Policy`

classes. (See below for more about Policies.) Lastly, we specify that the data is plain text.

The `response`

contains information about the identified sensitive information along with the filtered text.

The PhileasFilterServiceTest and EndToEndTests test classes have examples of how to configure Phileas and filter text.

Create a `FilterService`

, using a `PhileasConfiguration`

, and call `filter()`

on the service:

```
PhileasConfiguration phileasConfiguration = ConfigFactory.create(PhileasConfiguration.class);
PdfFilterService filterService = new PdfFilterService(phileasConfiguration);
BinaryDocumentFilterResponse response = filterService.filter(policies, context, body, MimeType.APPLICATION_PDF, MimeType.IMAGE_JPEG);
```


The `policies`

is a list of `Policy`

classes which are created by deserializing a policy from JSON. (See below for more about Policies.) The `body`

is the text you are filtering. Lastly, we specify that the data is plain text.

The `response`

contains a zip file of the images generated by redacting the PDF document.

A policy is an instance of a `Policy`

class that tells Phileas the types of sensitive information to identify, and what to do with the sensitive information when found. A policy describes the entire filtering process, from what filters to apply, terms to ignore, to everything in between. Phileas can apply one or more policies when `filter()`

is called. The list of policies will be applied in order as they were added to the list.

For examples on creating a policy, look at EndToEndTestsHelper. The PhileasFilterServiceTest and EndToEndTests test classes have examples of how to configure Phileas and filter text.

Policies can be de/serialized to JSON. Here is a basic (but valid) policy that identifies and redacts ages:

```
{
"name": "default",
"ignored": [],
"identifiers": {
"age": {
"ageFilterStrategies": [{
"strategy": "REDACT",
"redactionFormat": "{{{REDACTED-%t}}}"
}]
}
}
}
```


There is a long list of `identifiers`

that can be applied, and each identifier has several possible `strategy`

values. In this case, when a age is found, it is redacted by being replaced with the text `{{{REDACTED-age}}}`

. The `%t`

is a placeholder for the type of filter. In this case, it is the literal text `age`

.

Phileas is the underlying core of Philter, a turnkey text redaction engine which is built on top of Phileas and provides an API for redacting text. Philter runs entirely within your cloud and never transmits data outside your cloud. Custom AI models are available for domains like healthcare, legal, and news.

- Philter on the AWS Marketplace
- Philter on the Google Cloud Marketplace
- Philter on the Azure Marketplace
- On-prem deployments by contacting us at https://www.philterd.ai/.

As of Phileas 2.2.1, Phileas is licensed under the Apache License, version 2.0. Previous versions were under a proprietary license.

Copyright 2024-2026 Philterd, LLC.

Copyright 2018-2023 Mountain Fog, Inc.
