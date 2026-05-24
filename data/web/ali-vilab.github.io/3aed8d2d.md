---
domain: ali-vilab.github.io
fetch_date: '2026-05-18T12:36:42.502311'
status: ok
url: https://ali-vilab.github.io/In-Context-LoRA-Page/
---

**
In-Context LoRA for Diffusion Transformers
**

Lianghua Huang
Wei Wang
Zhi-Fan Wu
Yupeng Shi
Huanzhang Dou
Chen Liang
Yutong Feng
Yu Liu
Jingren Zhou


Tongyi Lab

[Paper]
[BibTeX]
[Code]


**Prompt:**
*
“This set of ***four images** illustrates a young artist's creative process
in a bright and inspiring studio;
**[IMAGE1]** she stands before a large canvas, brush in hand, adding
vibrant colors to a partially completed painting,
**[IMAGE2]** she sits at a cluttered wooden table, sketching ideas in a
notebook with various art supplies scattered around,
**[IMAGE3]** she takes a moment to step back and observe her work, and
**[IMAGE4]** she experiments with different textures by mixing paints
directly on the palette, her focused expression showcasing her dedication to her craft.”

*
In-Context LoRA fine-tunes text-to-image models to ***generate image sets** with customizable
intrinsic relationships, optionally **conditioned on another set**, enabling adaptation to a wide
range of tasks.

## Abstract

Recent research [Huang et al., 2024] has explored
the use of diffusion transformers (DiTs) for **task-agnostic image generation** by simply
concatenating attention tokens across images. However, despite substantial computational resources, the fidelity
of the generated images remains suboptimal. In this study, we reevaluate and streamline this framework by
hypothesizing that **text-to-image DiTs inherently possess in-context generation
capabilities**, requiring only minimal tuning to activate them. Through diverse task experiments, we
qualitatively demonstrate that existing text-to-image DiTs can effectively perform in-context generation without
any tuning. Building on this insight, we propose a remarkably simple pipeline to leverage the in-context abilities
of DiTs: (1) concatenate images instead of tokens, (2) perform joint captioning of multiple images, and (3) apply
task-specific LoRA tuning using small datasets (*e.g.,* 20 ~ 100 samples) instead of full-parameter tuning
with large datasets. We name our models In-Context LoRA (IC-LoRA). This approach requires no modifications to the
original DiT models, only changes to the training data. Remarkably, our pipeline generates high-fidelity image
sets that better adhere to prompts. While task-specific in terms of tuning data, our framework remains
task-agnostic in architecture and pipeline, offering a powerful tool for the community and providing valuable
insights for further research on product-level task-agnostic generation systems. We release our code, data, and
models at here.

## Film Storyboard Generation

Each three-image sequence is generated simultaneously using In-Context LoRA. A **placeholder character name** uniquely
references the character’s identity across the images.


**Prompt:**
*
“In this adventurous three-image sequence, [IMAGE1] ***Ethan**, an intrepid
archaeologist with a rugged appearance, uncovers an ancient map in a sunlit desert dig site, his excitement
palpable as he brushes away the sand, [IMAGE2] transitioning to a bustling marketplace in a vibrant foreign city
where **Ethan** negotiates with local merchants and gathers essential
supplies for his quest, [IMAGE3] and finally, **Ethan** treks through a
dense, mist-covered jungle, the towering trees and exotic wildlife emphasizing the challenges and mysteries that
lie ahead on his journey.”


**Prompt:**
*
“In a vibrant festival, [IMAGE1] we find ***Leo**, a shy boy, standing at
the edge of a bustling carnival, eyes wide with awe at the colorful rides and laughter, [IMAGE2] transitioning
to him reluctantly trying a daring game, his friends cheering him on, [IMAGE3] culminating in a triumphant
moment as he wins a giant stuffed bear, his face beaming with pride as he holds it up for all to see.”


**Prompt:**
*
“In a captivating tale of resilience, [IMAGE1] we see ***Lena**, a
determined girl, planting seeds in a barren field, her face set with resolve, [IMAGE2] transitioning to her
nurturing the plants, watering them daily, her efforts slowly yielding results, [IMAGE3] culminating in a lush
garden bursting with life, **Lena** standing proudly amidst her creation,
symbolizing growth and perseverance.”


**Prompt:**
*
“In a warm portrayal of family dynamics, [IMAGE1] shows ***Liam** assisting
his little sister **Sophie** with her homework at the dining table, their
expressions serious yet playful, [IMAGE2] shifting to the living room, where **Sophie** triumphantly holds up her completed project, her eyes sparkling with
pride while **Liam** shares in her joy, [IMAGE3] concluding with both
siblings snuggled on the couch, engrossed in a movie, their laughter echoing through the cozy space.”


**Prompt:**
*
“In a tender exploration of first love, [IMAGE1] we see ***Jamie** nervously
arranging flowers in a park, glancing around as if waiting for someone special, [IMAGE2] transitioning to the
moment arrives, their eyes locking in a shy smile that speaks volumes, [IMAGE3] finally showing them
seated on a bench, sharing stories and laughter, surrounded by blooming blossoms, embodying the magic of young
romance.”


**Prompt:**
*
“In a heartwarming depiction of a community gathering, [IMAGE1] captures ***Ella** preparing colorful decorations for a local festival, her excitement
palpable, [IMAGE2] then shifts to her helping **Tom** set up a booth, their
teamwork highlighted by laughter and shared smiles, [IMAGE3] culminating with the festival in full swing,
**Ella** and **Tom** surrounded by
friends, their joy radiating against the festive backdrop.”

## Portrait Photography

Each set of four images is generated concurrently with In-Context LoRA, aiming to maintain consistent subject
identities across images within each set.


**Prompt:**
*
“This set of four images showcases a teenage girl with curly black hair wearing a stylish denim jacket, each
image highlighting her dynamic personality in urban settings; [IMAGE1] she is skateboarding down a
graffiti-covered alley, a confident smile on her face as she maneuvers around obstacles; [IMAGE2] she is seated
at a trendy café, typing on her laptop with focused determination, the bustling city life visible through the
large windows behind her; [IMAGE3] she stands on a rooftop at sunset, her hair blowing in the breeze as she
gazes thoughtfully over the city skyline; and [IMAGE4] she is laughing with friends at a vibrant street market,
colorful lights and stalls creating a lively atmosphere around her.”
*


**Prompt:**
*
“The set of four images highlights the playful energy of a young boy in a city playground. [IMAGE1] He climbs up
a jungle gym with a look of determination, his hands gripping the bars as he pulls himself up; [IMAGE2] he
swings high on a set of swings, his head thrown back in laughter as his feet touch the sky; [IMAGE3] a close-up
captures him mid-slide, his eyes wide with excitement as he descends down a bright yellow slide; [IMAGE4] he
races down a pathway lined with trees, his arms pumping with energy as he chases after a soccer ball, his face
alight with joy.”
*


**Prompt:**
*
“The set of four images showcases a young girl exploring a cozy kitchen setting with her mother, filled with
warmth and affection. [IMAGE1] She stands on a stool, her hands reaching into a bowl of cookie dough as her
mother smiles beside her; [IMAGE2] she’s caught mid-laugh, flour dusted across her cheeks as she playfully
tosses a bit of dough in the air; [IMAGE3] the scene focuses on her concentration as she carefully uses cookie
cutters, her tiny hands pressing down on the dough; [IMAGE4] she proudly holds up a finished tray of cookies,
her face beaming with joy and accomplishment.”
*


**Prompt:**
*
“This set of four images captures the serene moments of an elderly woman tending to her garden. [IMAGE1] She
kneels beside a bed of blooming flowers, her hands gently pruning a rose bush, the soft morning light
illuminating her silver hair; [IMAGE2] she stands with a watering can, her face calm and peaceful as she
nurtures her plants; [IMAGE3] a close-up reveals her content smile as she examines a budding flower in her hand,
a sense of pride and joy evident; [IMAGE4] she sits on a small bench, sipping tea with her garden behind her,
surrounded by the vibrant colors of her hard work.”
*


**Prompt:**
*
“This set of four images captures a lively day spent at a beach between a mother and her son, highlighting their
playful connection and shared joy; [IMAGE1] the boy runs towards the water, his arms wide open, with the mother
following behind, smiling as she watches him; [IMAGE2] they are knee-deep in the ocean, laughing as they splash
each other, the sunlight reflecting off the water; [IMAGE3] they sit on the sand, the boy intently building a
sandcastle while the mother assists, both focused and relaxed; [IMAGE4] the final image shows the two walking
along the shore at sunset, the mother’s arm draped protectively around her son’s shoulders, their footprints
trailing behind them in the sand.”
*

## Font Design

Each set of four images is generated concurrently with In-Context LoRA, aiming to achieve a consistent font style
across images within each set.


**Prompt:**
*
“The set of four images features a minimalist handwriting font for casual use. [IMAGE1] shows "Everyday" on a
coffee cup; [IMAGE2] displays "Notes" on a small journal; [IMAGE3] has "Live Simply" on a white pillow; [IMAGE4]
shows "Good Vibes" on a cozy blanket, perfect for lifestyle and home decor branding.”
*


**Prompt:**
*
“The set of four image displays a tech-inspired sans serif font in minimalist designs. [IMAGE1] features "Tech
Flow" in silver on a circuit board; [IMAGE2] shows "Future World" in neon on a digital background; [IMAGE3] has
"Virtual Space" in blue on a sleek black setting; [IMAGE4] displays "AI Vision" in holographic font, ideal for
technology branding.”
*


**Prompt:**
*
“The set of four images presents a stylized font for travel themes. [IMAGE1] displays "Wanderlust" over a
mountain scene; [IMAGE2] features "Explore" on a beach background; [IMAGE3] shows "Adventure" with a compass
illustration; [IMAGE4] has "Journey" on a vintage suitcase, perfect for travel branding.”
*


**Prompt:**
*
“The set of four images highlights a serif font with Victorian-style details. [IMAGE1] displays "Vintage Charm"
on an old book cover; [IMAGE2] shows "Elegance" on a dark lace background; [IMAGE3] features "Old Times" on a
vintage clock; [IMAGE4] presents "Antique" on an ornate mirror, perfect for historical themes.”
*


**Prompt:**
*
“The set of four images showcases a playful bubble font in a vibrant pop-art style. [IMAGE1] displays "Pop
Candy" in bright pink with a polka dot background; [IMAGE2] shows "Sweet Treat" in purple, surrounded by candy
illustrations; [IMAGE3] has "Yum!" in a mix of bright colors; [IMAGE4] shows "Delicious" against a striped
background, perfect for fun, kid-friendly products.”
*

## Home Decoration

Each set of four images is generated concurrently using In-Context LoRA, aiming to maintain a consistent
decorative style across images within each set.


**Prompt:**
*
“This set of four images captures a colorful, nature-inspired living space with touches of green and earthy
textures; [IMAGE1] features a cozy nook with a woven chair draped in green blankets, surrounded by potted plants
and botanical prints on the wall; [IMAGE2] highlights a rustic wooden shelf adorned with small planters,
candles, and woven baskets; [IMAGE3] displays a serene bedroom with a bed made up in white linens, a natural
wood nightstand, and a forest-themed mural; [IMAGE4] shows a close-up of a large plant pot with unique textures
beside a patterned area rug.”
*


**Prompt:**
*
“This vibrant set of four image captures a lively home decor scene filled with color and eclectic charm;
[IMAGE1] the first image showcases a cozy living area with pastel-colored walls, a soft blue sofa, wooden
storage units displaying colorful accents, and a unique layered pendant light, [IMAGE2] the second image
features a kitchen setup with open shelves holding assorted kitchenware, a wire grid for organizing mugs above a
white sink, and warm sunlight streaming onto the countertop, [IMAGE3] the third image highlights a bold art wall
with an array of colorful, abstract paintings above a sage green sofa adorned with bright cushions, and [IMAGE4]
the fourth image shows a cheerful dining nook with a blue table, vividly striped cushions, framed artwork on the
sunny yellow wall, and a distinctive green pendant lamp casting a soft glow over the space.”
*


**Prompt:**
*
“This set of four images showcases a rustic living room with warm wood tones and cozy decor elements; [IMAGE1]
features a large stone fireplace with wooden shelves filled with books and candles; [IMAGE2] shows a vintage
leather sofa draped in plaid blankets, complemented by a mix of textured cushions; [IMAGE3] displays a corner
with a wooden armchair beside a side table holding a steaming mug and a classic book; [IMAGE4] captures a cozy
reading nook with a window seat, a soft fur throw, and decorative logs stacked neatly.”
*


**Prompt:**
*
“This set of four images showcases a vibrant and cozy kitchen with eclectic decor and warm tones; [IMAGE1]
reveals a colorful countertop with an assortment of spices in glass jars, a vintage kettle, and potted herbs;
[IMAGE2] displays a kitchen island with high chairs, bright red cabinets, and a hanging pot rack; [IMAGE3] shows
an inviting breakfast nook with a patterned bench, floral cushions, and a small round table; [IMAGE4] highlights
a section of open shelving with eclectic dinnerware, vibrant mugs, and unique artwork, creating a warm and
lively ambiance.”
*

## PowerPoint Template Design

Each set of four images is generated concurrently with In-Context LoRA, aiming to create a cohesive and unified
presentation style across slides within each set.


**Prompt:**
*
“This set of four images showcases a rustic-themed PowerPoint template for a culinary workshop; [IMAGE1]
introduces "Farm to Table Cooking" in warm, earthy tones; [IMAGE2] organizes workshop sections like
"Ingredients," "Preparation," and "Serving"; [IMAGE3] displays ingredient lists for seasonal produce; [IMAGE4]
includes chef profiles with short bios.”
*


**Prompt:**
*
“The set of four images presents a PowerPoint template designed for a charity fundraiser; [IMAGE1] introduces
"Help Make a Difference" in large, bold text over a background of hands reaching out; [IMAGE2] lists causes like
“Education,” “Healthcare,” and “Water Access” with heart icons; [IMAGE3] displays donation statistics; [IMAGE4]
includes a call-to-action slide with links to donate and volunteer.”
*


**Prompt:**
*
“This set of four images presents a PowerPoint template for an art history class on surrealism; [IMAGE1] shows
“Exploring Surrealism” over a Dali-inspired background; [IMAGE2] lists iconic surrealist artists like “Dali,”
“Magritte,” and “Ernst”; [IMAGE3] includes a timeline of the surrealist movement; [IMAGE4] showcases famous
artworks with short interpretations.”
*


**Prompt:**
*
“This set of four images depicts a colorful and engaging PowerPoint template for a “Food Science” educational
presentation; [IMAGE1] features a cover slide with “Understanding Nutrition” in bold typography and vegetable
illustrations; [IMAGE2] presents topics like “Macronutrients,” “Vitamins,” and “Minerals”; [IMAGE3] includes a
pie chart displaying daily nutrient intake recommendations; [IMAGE4] shows recipe ideas with images and
nutritional benefits.”
*


**Prompt:**
*
“The set of four images displays a vibrant template for a fashion branding presentation; [IMAGE1] introduces the
title “New Collection 2024” with a runway-inspired background; [IMAGE2] lists fashion sections like
“Streetwear,” “Formal,” and “Accessories” with icons; [IMAGE3] includes a color palette guide for the season;
[IMAGE4] presents a trend forecast with illustrated outfit ideas.”
*

## Couple Profile Generation

Each image pair is generated concurrently with In-Context LoRA, aiming to maintain a consistent style and identity
features across both images in each set.


**Prompt:**
*“This pair of images features a couple as cartoon characters in medieval attire; [IMAGE1] shows a knight
with a plumed helmet and a determined look, holding a small shield, while [IMAGE2] displays a character
dressed as a princess with a crown, smiling as they hold a flower, both against a castle background.”*


**Prompt:**
*“The pair of images captures a whimsical depiction of a couple in cartoon dragon costumes; [IMAGE1] a
character in a green dragon onesie with pointed ears and a toothy smile peeks towards the right, while
[IMAGE2] shows a character in a purple dragon suit with matching horns, displaying a playful wink, both set
against a cloudy sky background.”*


**Prompt:**
*“This pair of images portrays a couple of cartoon cats in detective attire; [IMAGE1] a black cat in a
trench coat and fedora holds a magnifying glass and peers to the right, while [IMAGE2] a white cat with a
bow tie and matching hat raises an eyebrow in curiosity, creating a fun, noir-inspired scene against a dimly
lit background.”*


**Prompt:**
*“The pair of images depicts cartoon characters enjoying music together; [IMAGE1] features a character with
a spiky mohawk and wide headphones, bobbing their head with closed eyes, while [IMAGE2] presents a character
with a ponytail, holding a guitar and also wearing headphones, both set against a dark blue background with
musical notes scattered around.”*


**Prompt:**
*“The pair of images depicts a couple in a cartoon-style grocery shopping scene; [IMAGE1] one character
reaches for a snack on a high shelf with a playful grin, while [IMAGE2] the other character with wide eyes
and a towering cart of food holds a grocery list, all set in a colorful grocery aisle.”*


**Prompt:**
*“This pair of images capture a couple in a pillow fight; [IMAGE1] a character with tousled hair and a
mischievous grin winds up to swing a fluffy pillow, while [IMAGE2] another character, already hit with
feathers flying around them, has a playful look of shock, both in a cozy bedroom with fluffy bedding.”*

## Visual Identity Design

Each image pair is generated concurrently with In-Context LoRA, aiming to achieve a cohesive and consistent visual
identity across both images in each pair.


**Prompt:**
*“The pair of images highlights a logo and its real-world use for a rustic coffee brand; [IMAGE1] a
striking teal background showcases a logo with a stylized, perched bird in black and white, titled “Bluebird
Roast” in an elegant serif font, with a leafy branch detail underneath; [IMAGE2] this logo is applied to a
coffee mug sitting atop a woven coaster on a dark mahogany table, with a blurred background that emphasizes
the warm tones and classic aesthetic of the branding in a cozy setting.”*


**Prompt:**
*“The pair of images showcases the joyful identity of a produce brand, [IMAGE1] showing a smiling pineapple
graphic and the brand name “Fresh Tropic” in a fun, casual font on a light aqua background; while [IMAGE2]
translates the design onto a reusable shopping tote with the pineapple logo in black, held by a person in a
market setting, emphasizing the brand’s approachable and eco-friendly vibe.”*


**Prompt:**
*“This pair of images presents an artisan soap brand inspired by botanical elements. [IMAGE1] On a rich
sage green background, delicate gold-foil leaves and flower motifs intertwine around the brand name “Herbal
Haven” in an elegant, serif font, conveying a sophisticated, earthy aesthetic. [IMAGE2] The design is
applied to a set of organic soaps wrapped in handmade paper and twine, placed with real herbs and flowers on
a wooden board, radiating the brand’s commitment to natural beauty and luxury through a warm, inviting
setting.”*


**Prompt:**
*“This pair of images introduces a sophisticated confectionery brand identity blending elegance and whimsy.
[IMAGE1] The first image resents a whimsical, Art Nouveau-inspired design, featuring a pattern of golden
leaves intertwined with pastel-colored candy shapes on a deep plum background. The brand name "Golden
Garden" appears in a flowing, decorative font, surrounded by delicate floral filigree. [IMAGE2] The design
is applied to a set of artisanal chocolate boxes, displayed with gold-foil accents and delicate paper
flowers, conveying the brand’s high-end and enchanting quality through luxurious textures and intricate
details.”*


**Prompt:**
*“In this set of two images, a bold animal-themed logo is introduced and adapted to a lifestyle product;
[IMAGE1] a simplistic black logo featuring a bear face and the brand name “Bear Lane” on a sky blue
background; [IMAGE2] the design is printed on a gray gym bag and water bottle, with both items positioned on
a wooden gym bench.”*


**Prompt:**
*“In this set of two images, a modern mystical brand identity comes to life. [IMAGE1] Against a deep navy
background, intricate star and moon motifs in metallic silver and soft blush pink shimmer in various sizes,
creating a cosmic, dreamlike atmosphere. The brand name “Celestial Glow” is displayed in a sleek, geometric
font that radiates a mystical yet minimalist vibe. [IMAGE2] The design is adapted onto a glowing glass
misting bottle and a crystal-infused body lotion bottle, arranged on a soft, cloud-like velvet fabric with
crystals and candles, showing the brand’s ethereal charm in self-care products.”*

## Portrait Illustration

Each pair of images is generated with In-Context LoRA, aiming to maintain consistent identity, clothing,
expression, similar pose, and atmosphere between the ‘before’ and ‘after’ illustration versions. Instead of
directly replicating the original photo, the illustration enhances key features with added expressive emphasis.


**Prompt:**
*“This image pair presents a transformation from a realistic portrait to a playful illustration, capturing
both detail and artistic flair; [IMAGE1] the photograph shows a woman standing in a bustling marketplace,
wearing a wide-brimmed hat, a flowing bohemian dress, and a leather crossbody bag; [IMAGE2] the illustration
version exaggerates her accessories and features, with the bohemian dress depicted in vibrant patterns and
bold colors, while the background is simplified into abstract market stalls, giving the scene an animated
and lively feel.”*


**Prompt:**
*“The image pair highlights a transformation from a high-fashion portrait to an artistic interpretation,
capturing elegance in both styles; [IMAGE1] the photo shows a woman wearing a sleek black dress with lace
details, posing against a white studio backdrop, her hair styled in an intricate updo; [IMAGE2] the
illustration reimagines her as a stylized figure, with the lace details transformed into bold, intricate
patterns and her hair exaggerated into voluminous curls, while the background is simplified into a gradient
of soft, muted colors, enhancing the contrast between her formal attire and the artistic rendering.”*


**Prompt:**
*“The image pair showcases the transformation from reality to a stylized interpretation; [IMAGE1] the photo
shows a person with a topknot, wearing a cozy yellow sweater and plaid scarf, standing in front of a shop
window, while [IMAGE2] the illustrated version highlights the warm tones, adding playful, oversized shapes
and bright hues, creating an animated feel with a soft, inviting background.”*


**Prompt:**
*“The image pair illustrates a transformation from a candid photograph to a dynamic illustration, each
capturing distinct artistic qualities; [IMAGE1] the original photo features a man with a beard, wearing a
denim jacket over a graphic tee and black jeans, seated on a staircase with a skateboard beside him, while
[IMAGE2] the illustrated version amplifies his outfit with bold colors, adding stylized graffiti on the
steps and vibrant motion lines around the skateboard.”*


**Prompt:**
*“This image pair captures a transformation from a street-style photograph to a dynamic digital
illustration; [IMAGE1] the photo shows a person wearing a colorful windbreaker jacket, ripped jeans, and
white sneakers, walking along a busy city street with a skateboard tucked under their arm; [IMAGE2] the
illustration simplifies the background into bold, abstract shapes, while the figure’s outfit is brightened
with more vibrant colors and their pose is exaggerated, giving the image a sense of movement and energy that
contrasts with the stillness of the photograph.”*


**Prompt:**
*“The image pair contrasts a photographic portrait with its illustrated counterpart, showcasing an artistic
reinterpretation; [IMAGE1] the initial photo shows a woman with a high bun, dressed in a classic black
trench coat, holding a bright yellow umbrella, standing on a rainy street, while [IMAGE2] the illustration
accentuates her pose with exaggerated features, making the umbrella the focal point with vivid yellows and
reds, transforming the rain into playful, curving lines.”*

## Sandstorm Visual Effect

Each image pair is generated using In-Context LoRA, aiming to demonstrate strong consistency between the ‘before’
and ‘after’ sandstorm effect images.


**Prompt:**
*“This image pair showcases the transformation of a cyclist through a sandstorm visual effect; [IMAGE1]
features a cyclist in vibrant gear pedaling steadily on a clear, open road with a serene sky in the background,
highlighting focus and determination, [IMAGE2] transforms the scene as the cyclist becomes enveloped in a fierce
sandstorm, with sand particles swirling intensely around the bike and rider against a stormy, darkened backdrop,
emphasizing chaos and power.”*


**Prompt:**
*“The image pair illustrates the metamorphosis of a musician enhanced by a sandstorm effect; [IMAGE1] the first
image depicts a guitarist playing calmly on a minimalist stage with soft lighting, capturing the essence of
tranquility and artistry, [IMAGE2] the second image erupts into a dynamic sandstorm with sand and debris
swirling around the musician and instrument, set against a tumultuous background, conveying an intense and
electrifying performance.”*


**Prompt:**
*“This pair of images highlights a stunning transformation with a sandstorm visual effect, balancing calm and
intensity; [IMAGE1] features a man in a meditative pose, seated cross-legged in a black outfit against a white
backdrop, eyes closed, [IMAGE2] shows the man shrouded in a fierce explosion of swirling sand particles mixed
with streaks of electric light, against a deeper background, creating a captivating display of serenity
overtaken by chaos.”*

## Image-Conditional Generation

Examples of image-conditional generation using In-Context LoRA across multiple tasks with training-free SDEdit.

**Portrait Identity Transfer.**


**Font Style Transfer.**


**Application of Visual Identity.**


**Portrait to Illustration.**


**Failure case of Sandstorm Visual Effect Application.**


**Failure cases of Portrait Identity Transfer.**


We observe that SDEdit for In-Context LoRA tends to be unstable, often failing to preserve identity. Addressing this issue is left for future work.


## BibTex

` @article{lhhuang2024iclora,`

title={In-Context LoRA for Diffusion Transformers},

author={Huang, Lianghua and Wang, Wei and Wu, Zhi-Fan and Shi, Yupeng and Dou, Huanzhang and Liang, Chen and Feng, Yutong and Liu, Yu and Zhou, Jingren},

booktitle={arXiv preprint arxiv:2410.23775},

year={2024}

}
