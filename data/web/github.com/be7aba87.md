---
domain: github.com
fetch_date: '2026-05-18T12:36:30.666074'
status: ok
url: https://github.com/richard-to/mesop-app-maker
---

| title | Mesop App Maker |
|---|---|
| emoji | 🏭 |
| colorFrom | yellow |
| colorTo | pink |
| sdk | docker |
| pinned | false |
| license | apache-2.0 |
| app_port | 8080 |

Editor to generate, edit, and view Mesop apps using LLMs.

The Mesop App Maker consists of two Mesop apps, the editor and the app runner.

The editor is the Mesop app that allows you to generate, edit, and view Mesop apps.

```
pip install -r requirements.txt
mesop main.py
```

The editor supports the following environment variables. These are mainly useful for local development where you don't want to keep entering your API Key and runner token after every reload.

```
GEMINI_API_KEY=you-gemini-api-key
MESOP_APP_MAKER_RUNNER_URL=https://example.com
MESOP_APP_MAKER_RUNNER_TOKEN=your-secret-token
MESOP_APP_MAKER_SHOW_HELP=0
```


You will need a Gemini API key to use the Mesop app generate functionality.

The runner has been moved to https://github.com/richard-to/mesop-app-runner.


The Mesop App Runner uses Docker to avoid potentially destructive code changes.

It can be started using these commands:

```
# In mesop-app-runner directory
docker stop mesop-app-runner;
docker rm mesop-app-runner;
docker build -t mesop-app-runner . && docker run --name mesop-app-runner \
-e MESOP_APP_RUNNER_TOKEN=your-secret-token \
-d -p 8080:8080 mesop-app-runner;
```

![Screenshot 2024-08-05 at 5 29 44 PM](https://private-user-images.githubusercontent.com/539889/355273284-d96afd8a-3c09-4d12-8749-00deddc7f8f5.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NzkwNzkyOTMsIm5iZiI6MTc3OTA3ODk5MywicGF0aCI6Ii81Mzk4ODkvMzU1MjczMjg0LWQ5NmFmZDhhLTNjMDktNGQxMi04NzQ5LTAwZGVkZGM3ZjhmNS5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjYwNTE4JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI2MDUxOFQwNDM2MzNaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT01NDA3MjY0YjE2M2Q1YmY0NjQ5YWRiYmQzNjI3NWU4NWM4NjAwNjA1ZjRmZmU5ODEyZDBlNmIyZDM1OWRmZTk2JlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCZyZXNwb25zZS1jb250ZW50LXR5cGU9aW1hZ2UlMkZwbmcifQ.Sf-MeS7epeTUjG3YgEiUM0ipXuDVAvT2GbKTpb0W5Sg)

![Screenshot 2024-08-05 at 5 31 35 PM](https://private-user-images.githubusercontent.com/539889/355273297-1a826d44-c87b-4c79-aeaf-29bc8da3b1c0.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NzkwNzkyOTMsIm5iZiI6MTc3OTA3ODk5MywicGF0aCI6Ii81Mzk4ODkvMzU1MjczMjk3LTFhODI2ZDQ0LWM4N2ItNGM3OS1hZWFmLTI5YmM4ZGEzYjFjMC5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjYwNTE4JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI2MDUxOFQwNDM2MzNaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT05NjcwZWU3MjEwYmM2MjgxMmM3YTM0MzJlYmYzZjllMzQ2N2I5MWQxZWY0NDFhYWIxMDhhNDE3ZTBiZWNlNWMyJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCZyZXNwb25zZS1jb250ZW50LXR5cGU9aW1hZ2UlMkZwbmcifQ.KvTk1O9LsSZCgbBxP5pqBP2qj-jWsDJVg8sj3nH2kg4)

If you want to test out the Mesop App Maker on Hugging Face, you will need to create your own instance of the Mesop App Runner.

You can do this by duplicating the Mesop App Runner on Hugging Face.

This can be done on the Mesop App Runner space like this:

Make sure to specify a `MESOP_APP_RUNNER_TOKEN`

. This can be any random characters. It is needed to ensure that only people
with the token can run Mesop code on your runner instance.

![Screenshot 2024-08-25 at 2 49 36 PM](https://private-user-images.githubusercontent.com/539889/361264811-4c6ce056-0898-4c10-8e6c-36d268a63108.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NzkwNzkyOTMsIm5iZiI6MTc3OTA3ODk5MywicGF0aCI6Ii81Mzk4ODkvMzYxMjY0ODExLTRjNmNlMDU2LTA4OTgtNGMxMC04ZTZjLTM2ZDI2OGE2MzEwOC5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjYwNTE4JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI2MDUxOFQwNDM2MzNaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT03OGY2Y2FkMzAzYWQ0ZWNhMTE0ODQ2ZTBiZjMxNDI2NWYzNzNlNDQ0OTE2OTU4NWJmNmIxNzJlMjY3Y2NjOTFmJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCZyZXNwb25zZS1jb250ZW50LXR5cGU9aW1hZ2UlMkZwbmcifQ.6_7hAyfUEW-skD-C6rqRqSVPW4Ro_HUfROCXz62c1ro)

The URL will be something like `https://<username>-<app-name>.hf.space`

.

You will need to provide this URL as the Runner URL on Mesop App Maker. You will also need to provide the runner token associated with your instance on Mesop App Maker.

![Screenshot 2024-08-25 at 4 22 32 PM](https://private-user-images.githubusercontent.com/539889/361265058-efa1ce04-4770-4927-89ab-6a65ed62b014.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NzkwNzkyOTMsIm5iZiI6MTc3OTA3ODk5MywicGF0aCI6Ii81Mzk4ODkvMzYxMjY1MDU4LWVmYTFjZTA0LTQ3NzAtNDkyNy04OWFiLTZhNjVlZDYyYjAxNC5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjYwNTE4JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI2MDUxOFQwNDM2MzNaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT1hOTMxMjcxYjYyNjljZmUzZTFiNGI4OTQxMDY3MWM2OGFiYzlhMDBlZmQxMWVlNWFhZDQ2NWQxZWI5YTc2MmNlJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCZyZXNwb25zZS1jb250ZW50LXR5cGU9aW1hZ2UlMkZwbmcifQ.WpjlrjOKhma3oVnyqHFS3bicHZR3vvQ8HPKyDEaD3WM)
