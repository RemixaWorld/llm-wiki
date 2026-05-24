---
domain: levelup.gitconnected.com
fetch_date: '2026-05-18T12:54:27.870693'
status: ok
url: https://levelup.gitconnected.com/ai-just-made-data-compression-algorithms-multi-folds-better-than-ever-da09092ff9fd
---

# AI Just Made Data Compression Algorithms Multiple Times Better Than Ever

## A deep dive into the ‘LMCompress’ algorithm that outperforms all traditional algorithms available today, supercharging data compression like never before.

[ ![Dr. Ashish Bamania](https://miro.medium.com/v2/resize:fill:64:64/1*5R3sTJ1KZkaD9s6XmBNsQA@2x.jpeg) ](<https://bamania-ashish.medium.com/?source=post_page---byline--da09092ff9fd--------------------------------------->)

[Dr. Ashish Bamania](<https://bamania-ashish.medium.com/?source=post_page---byline--da09092ff9fd--------------------------------------->)

9 min read

·

May 20, 2025

\--

Listen

Share

More

Image generated using Google ImageFX

A massive [403 million terabytes of data](<https://www.digitalsilk.com/digital-trends/how-much-data-is-generated-per-day/>) is generated on the internet every day.

Given this rate, the global data pool is [estimated to grow to 163 zettabytes](<https://www.seagate.com/files/www-content/our-story/trends/files/Seagate-WP-DataAge2025-March-2017.pdf>) (one billion terabytes) by 2025.

Press enter or click to view image in full size

Plot obtained from [Seagate’s report based on IDC’s Data Age 2025 study](<https://www.seagate.com/files/www-content/our-story/trends/files/Seagate-WP-DataAge2025-March-2017.pdf>)

Although the rate of data creation is exponential, the data compression methods available to us are hitting their limits.

_Can AI help us solve it?_

The answer is yes!

A [recent research paper published in Nature Machine Intelligence](<https://www.nature.com/articles/s42256-025-01033-7>) has proposed a new compression algorithm called **_LMCompress_ , **which uses LLMs to compress data.

This algorithm is so effective that it **doubles** the lossless compression ratios of [JPEG-XL](<https://en.wikipedia.org/wiki/JPEG_XL>) for images, [FLAC](<https://en.wikipedia.org/wiki/FLAC>) for audio, and [H.264](<https://en.wikipedia.org/wiki/Advanced_Video_Coding>) for videos, and **quadruples** the compression ratio of [bz2](<https://en.wikipedia.org/wiki/Bzip2>) for texts.

_This isn’t an episode of_[ _Silicon Valley_](<https://en.wikipedia.org/wiki/Silicon_Valley_\(TV_series\)>) _; it is actually happening!_

Here is a story where we deep dive into how this algorithm works to supercharge data compression like never before.

Let’s begin!

_Btw, my latest book called “_** _LLMs In 100 Images_** _” is now out. It is a collection of 100 visuals that describe the most important concepts you need to master LLMs today._

_Grab your copy at a_** _special early bird discount_** _using the link below:_

## [LLMs In 100 ImagesTired of AI explanations that sound like rocket science? I've got you covered!bamaniaashish.gumroad.com](<https://bamaniaashish.gumroad.com/l/llmbook/EARLYBIRD?source=post_page-----da09092ff9fd--------------------------------------->)

## But First, How Do We Currently Compress Data?

There are two types of Data compression methods:

* **Lossless** : These methods can compress and perfectly decompress/ reconstruct data without any loss
* **Lossy** : These methods lose some data during compression to reach a higher data compression ratio

For those new to this term, the [data compression ratio](<https://en.wikipedia.org/wiki/Data_compression_ratio>) measures the relative reduction in data size when using a data compression method/ algorithm.

_A higher data compression ratio means better compression._

There are multiple lossless data compression methods available to us today, with some popular ones being:

* [PNG](<https://en.wikipedia.org/wiki/PNG>) for images
* [FLAC](<https://en.wikipedia.org/wiki/FLAC>)**** for audio
* [DEFLATE](<https://en.wikipedia.org/wiki/Deflate>) for general files, including text and executables
* Lossless [H.264](<https://en.wikipedia.org/wiki/Advanced_Video_Coding>)/ [H.265](<https://en.wikipedia.org/wiki/High_Efficiency_Video_Coding>) for videos

Similarly, the following methods are available for lossy compression:

* [JPEG](<https://en.wikipedia.org/wiki/JPEG>) for images
* [MP3](<https://en.wikipedia.org/wiki/MP3>) for audio
* [MPEG-4](<https://en.wikipedia.org/wiki/MPEG-4>) for videos

(_There are no standard lossy compression methods for files containing text and executables, because data loss is never preferred for these._)

Most compression methods we use today are based on ideas proposed by [Claude Shannon](<https://en.wikipedia.org/wiki/Claude_Shannon>) in [his foundational work](<https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf>) on [Information theory](<https://en.wikipedia.org/wiki/Information_theory>).

Shannon introduced the concept of [**Entropy**(also called **Shannon entropy**)](<https://en.wikipedia.org/wiki/Entropy_\(information_theory\)>), which measures the average amount of uncertainty in a message/ data.

Lower entropy means more predictability, and the more predictable the data is, the more it can be compressed.

Also, this entropy determines a minimum size beyond which data cannot be [compressed without losing information](<https://en.wikipedia.org/wiki/Shannon%27s_source_coding_theorem>).

This is what lies at the foundation of our modern-day data compression methods.

Although these methods have been very effective, we have reached their limits after 80 years of research since they were first proposed.

_Can we do better?_

## Understanding Is Compression

Answer this question for me — What comes to your mind when you see this number `3.1415929` ?

Right, it’s pi (`π`).

How about when you try to remember a person?

You don’t memorise every facial detail of theirs, rather their key features like ‘bushy eyebrows’, ‘big nose’, or ‘bald with glasses’.

What your brain is doing here is **naturally compressing all the information by understanding it.**

And this is what LLMs do as well when they are trained on a large amount of data.

They compress the data within its parameters, and the better an LLM understands the data, the better it can compress it.

Based on this insight, researchers propose their new compression method called **_LMCompress_** that works as follows.

First, the given data is broken down into a sequence of tokens using a tokenizer.

Then, this token sequence is fed into an LLM, which outputs the predictive probability distribution for each token (i.e. how likely each possible next token is, given the previous ones).

Finally, based on these predictive distributions, the data is losslessly compressed using a technique called [**Arithmetic coding**](<https://en.wikipedia.org/wiki/Arithmetic_coding>), which efficiently encodes it into a single precise fraction between 0 and 1.

Press enter or click to view image in full size

An overview of the steps in the _LMCompress_ compression method

Different tokenisation methods and LLMs are used to better understand different data types and improve this method's performance.

Let’s learn how.

### Image Compression

The [image-GPT (iGPT) model](<https://cdn.openai.com/papers/Generative_Pretraining_from_Pixels_V2.pdf>) from OpenAI is used for lossless image compression.

This is an autoregressive large vision model based on the Transformer architecture that predicts the next pixel in a 1D sequence representing an image.

To start, an image is flattened from a 2D grid to a 1D sequence of pixels.

Next, this pixel sequence is input into iGPT, which outputs the probability of each next pixel.

These probabilities are then encoded using Arithmetic coding.

Since the entire pixel sequence might not fit iGPT’s limited context window, it is divided into non-overlapping sub-sequences that are input into the model to be compressed independently.

Press enter or click to view image in full size

Overview of the Image compression method using iGPT (Image obtained from research paper titled ‘[Generative Pretraining from Pixels](<https://cdn.openai.com/papers/Generative_Pretraining_from_Pixels_V2.pdf>)’)

### Lossless Video Compression

Since existing open-source large video models don’t output probabilities, the iGPT model is used for the lossless video compression task as well.

Since a video is fundamentally a sequence of frames (images), each frame is individually compressed using iGPT in the same way as described for images.

### Lossy Video Compression

Lossy compression is popularly acceptable for videos to reduce file size.

Lossy video compression algorithms such as [DCVC](<https://github.com/microsoft/DCVC>) and [H.26X](<https://en.wikipedia.org/wiki/Category:H.26x>) work by removing the redundant information within a frame (_intra-frame redundancies_) and between frames (_inter-frame redundancies_) of a video.

A technique called [**Generative Compression**](<https://arxiv.org/abs/1703.01467>) has recently been introduced in research that not only removes redundant information but can also generate details back during decompression using different AI models ([GANs](<https://arxiv.org/abs/1703.01467>)/ [Diffusion models](<https://arxiv.org/abs/2209.06950>)).

Press enter or click to view image in full size

Traditional versus Generative compression (Image obtained from ArXiv research paper titled ‘[Generative Compression](<https://arxiv.org/abs/1703.01467>)’)

Borrowing from this method, the researchers start by compressing a given video using [DCVC (Deep Contextual Video Compression)](<https://github.com/microsoft/DCVC>), followed by applying a [DDPM Diffusion model](<https://arxiv.org/abs/2006.11239>) on the compressed output.

This diffusion model generates/ recovers the details that may have been lost during the initial DCVC compression.

The reconstruction process iteratively improves by minimizing the squared error difference between each frame generated by the diffusion model and the DCVC-decoded frame.

### Audio Compression

For lossless audio compression, a given audio file is treated as a sequence of frames, where each frame uses a constant number of bytes to represent the amplitude information at a specific time point in the audio.

These bytes are converted into an ASCII character, converting the audio into a string of characters.

An LLM ([LLaMA3–8B](<https://huggingface.co/meta-llama/Meta-Llama-3-8B>)) is then [LoRA fine-tuned](<https://arxiv.org/abs/2106.09685>) on this ‘audio-as-string’ data to autoregressively predict the next token probabilities.

These probabilities are then encoded using Arithmetic coding.

Since the entire audio sequence might not fit the LLM’s limited context window, long audio sequences are split into smaller chunks, and each chunk is compressed separately.

### Text Compression

LLMs [naturally compress text](<https://arxiv.org/abs/2309.10668>), but their compression capabilities can be further improved when the text to be compressed belongs to a specific domain.

This is achieved by [LoRA fine-tuning](<https://arxiv.org/abs/2106.09685>) an LLM ([LLaMA3–8B](<https://huggingface.co/meta-llama/Meta-Llama-3-8B>)) on domain-specific text datasets as follows:

* [MeDAL](<https://arxiv.org/abs/2012.13978>): a dataset consisting of [PubMed](<https://pubmed.ncbi.nlm.nih.gov/>) medical abstracts
* [Pile of Law](<https://arxiv.org/abs/2207.00220>): a dataset consisting of legal and administrative texts

This makes the LLM better ‘ _understand_ ’ (and therefore better compress) the text belonging to a particular domain by learning the domain-specific characteristics.

Once fine-tuned, the LLM predicts the next-token probabilities for given text.

These probabilities are then encoded using Arithmetic coding.

Again, text is split into smaller chunks and input to the LLM due on its limited context window, compressing the overall text, chunk by chunk.

## But Is ‘**LMCompress’ Really That Impressive?**

### Performance On Image Compression

_LMCompress_ is tested on two well-known image datasets:

* [ILSVRC 2017](<https://arxiv.org/abs/1409.0575>) (ImageNet Large Scale Visual Recognition Challenge)
* [CLIC 2019 Professional](<https://clic2025.compression.cc/>) (Challenge on Learned Image Compression)

**The results show that it outperforms all the baselines on both datasets, achieving more than double the compression ratio of the best traditional methods.**

Press enter or click to view image in full size

Compression ratios achieved with LMCompress vs. traditional image compression algorithms. ‘[Chinchilla](<https://en.wikipedia.org/wiki/Chinchilla_\(language_model\)>)’ represents the compression ratio when this LLM (trained purely on text) is used for image compression.

Press enter or click to view image in full size

Plot representing the image compression ratios achieved by different lossless methods on two image datasets

### Performance On Video Compression

_LMCompress_ is evaluated on test video clips from [Xiph.org](<https://xiph.org/>).

These video clips either contain:

* Static scenes: where consecutive frames change slightly or do not change at all (e.g. classroom recordings), or
* Dynamic scenes: where consecutive frames change drastically (e.g. action movies)

The results are again impressive, with _LMCompress_ outperforming the baselines on both video types.

**It improves compression ratio by over 20% on static scenes and at least 50% on dynamic scenes compared to baselines.**

Press enter or click to view image in full size

Plot representing the video compression ratios achieved by different lossless methods on test videos with static and dynamic scenes

Next, CIPR SIF Sequences from [Xiph.org](<https://xiph.org/>) are used to evaluate its performance on lossy compression.

**The results show that _LMCompress_ more than doubles the compression ratio compared to DCVC and DCVC-FM.**

It achieves this while maintaining or even improving [Peak signal-to-noise ratio (PSNR) ](<https://en.wikipedia.org/wiki/Peak_signal-to-noise_ratio>)(which measures distortion) and [Fréchet inception distance (FID)](<https://en.wikipedia.org/wiki/Fr%C3%A9chet_inception_distance>) (which measures perceptual quality).

Press enter or click to view image in full size

Compression ratio and other video compression quality metrics achieved with LMCompress vs. traditional lossy video compression algorithms. Low [BPP (bits per pixel)](<https://en.wikipedia.org/wiki/Color_depth>) indicate more compression, which, alongside low FID and high PSNR, indicates better video compression quality.

### Performance On Audio Compression

_LMCompress_ is tested on two audio datasets containing English speech from audiobooks:

* [LibriSpeech](<https://www.tensorflow.org/datasets/catalog/librispeech>)
* [LJSpeech](<https://www.tensorflow.org/datasets/catalog/ljspeech>)

Results show that **all LLM-based methods (including _LMCompress)_ outperform FLAC by 25 to 94%.**

Specifically, **_LMCompress_ further improves upon the other LLM-based methods** (using non-fine-tuned LLaMA3–8B and [Chinchilla](<https://en.wikipedia.org/wiki/Chinchilla_\(language_model\)>)) **by an** **additional 28% to 55%**.

Another interesting finding is that even though _LMCompress_ is only fine-tuned on LibriSpeech, it still performs much better on LJSpeech, compressing it 55% better than the original, non-fine-tuned LLaMA3–8B model.

Press enter or click to view image in full size

Compression ratios achieved with LMCompress and other LLM-based methods vs. FLAC

### Performance On Text Compression

When tested on the datasets [MeDAL](<https://arxiv.org/abs/2012.13978>) (from the medical domain) and [Pile of Law](<https://arxiv.org/abs/2207.00220>) (from the law domain), _LMCompress_ is again found to outperform all other baselines.

It is so good that **its compression ratio on either dataset is as much as three times that of the best traditional methods.**

When compared to the non-fine-tuned LLaMA3–8B (used for compression [based on a prior research paper](<https://arxiv.org/abs/2308.06942>)), _LMCompress_ improves the compression ratio by 8.5% on MeDAL and by 38.4% on Pile of Law.

Press enter or click to view image in full size

Plot representing the text compression ratios achieved by LMCompress vs. other methods on two domain-specific text datasets

** _LMCompress_ achieves higher compression ratios across text, audio, image, and video than all traditional baselines and raw LLM-based algorithms.**

These results are really remarkable and open up new opportunities to build better communication and data storage systems for the future.

_What are your thoughts on it? Let me know in the comments below._

## Further Reading

*  _Research paper titled ‘Lossless data compression by large models’ (_[_published in ArXiv_](<https://arxiv.org/abs/2407.07723v3>) _and_[ _Nature Machine Intelligence_](<https://www.nature.com/articles/s42256-025-01033-7>) _)_
* [_Code available for the ‘Lossless data compression by large models’ paper on Code Ocean_](<https://codeocean.com/capsule/4957991/tree/v2>)
* [ _An overview of Arithmetic Coding on ‘The Hitchhiker’s Guide to Compression’ blog_](<https://go-compression.github.io/algorithms/arithmetic/>)
* [ _Research paper titled ‘Language Modeling Is Compression’ published in ArXiv_](<https://arxiv.org/abs/2309.10668>)
* [ _Research paper titled ‘Approximating Human-Like Few-shot Learning with GPT-based Compression’ published in ArXiv_](<https://arxiv.org/abs/2308.06942>)

## Source Of Images

All images are obtained from the [original research paper](<https://arxiv.org/abs/2407.07723v3>) unless stated otherwise.

[**_Subscribe to ‘Into AI’ — a newsletter where I help you explore the best and latest in Artificial Intelligence from the ground up by dissecting the original research papers._**](<https://intoai.pub/>)

Press enter or click to view image in full size
