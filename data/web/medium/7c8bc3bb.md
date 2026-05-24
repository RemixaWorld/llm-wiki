---
domain: medium.com
fetch_date: '2026-05-18T12:46:59.676698'
status: ok
url: https://medium.com/@datadrifters/flux-lora-fine-tuning-guide-personalize-ai-image-models-on-minimal-data-for-custom-look-and-feel-240c37cae450
---

# Fine Tuning FLUX: Personalize AI Image Models on Minimal Data for Custom Look and Feel

[ ![Agent Native](https://miro.medium.com/v2/resize:fill:64:64/1*dt5tcaKMBhB6JboQ9lIEAA.jpeg) ](</?source=post_page---byline--240c37cae450--------------------------------------->)

[Agent Native](</?source=post_page---byline--240c37cae450--------------------------------------->)

11 min read

·

Aug 15, 2024

[](<https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fvote%2Fp%2F240c37cae450&operation=register&redirect=https%3A%2F%2Fagentnativedev.medium.com%2Fflux-lora-fine-tuning-guide-personalize-ai-image-models-on-minimal-data-for-custom-look-and-feel-240c37cae450&user=Agent+Native&userId=3dea44a5d468&source=---header_actions--240c37cae450---------------------clap_footer------------------>)

\--

[](<https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2F240c37cae450&operation=register&redirect=https%3A%2F%2Fagentnativedev.medium.com%2Fflux-lora-fine-tuning-guide-personalize-ai-image-models-on-minimal-data-for-custom-look-and-feel-240c37cae450&source=---header_actions--240c37cae450---------------------bookmark_footer------------------>)

[Listen](<https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3D240c37cae450&operation=register&redirect=https%3A%2F%2Fagentnativedev.medium.com%2Fflux-lora-fine-tuning-guide-personalize-ai-image-models-on-minimal-data-for-custom-look-and-feel-240c37cae450&source=---header_actions--240c37cae450---------------------post_audio_button------------------>)

Share

Black Forest Labs (alumni of Stability AI) launched FLUX.1, an open-sourced suite of AI image generation models that you can run locally.

FLUX models took socials by storm, because the largest one, FLUX.1 [pro], outperformed Stable Diffusion 3 Ultra, Midjourney v6.0, and DALL·E 3 HD.

Look at the benchmarks, absolutely crazy!

![image](https://miro.medium.com/v2/resize:fit:630/0*-UHPsb80ewO0uS5X.png)

There are 3 models:

* **Flux.1 [pro]:** Proprietary, API-based, $0.055/image.
* **Flux.1 [dev]:** 12B parameters, noncommercial use.
* **Flux.1 [schnell]:** 12B parameters, speed-optimized, Apache 2.0.

and all of them are based on hybrid multimodal transformer blocks:

* Parallel diffusion and parallel attention layers
* Scaled to 12B parameters
* Flow matching (consistently better performance than alternative diffusion-based methods in terms of both likelihood and sample quality)

There are lots of LoRAs and extensions released as you read this article, and people say it’s noticeably better than Midjourney, and my experience is also very… very promising!
