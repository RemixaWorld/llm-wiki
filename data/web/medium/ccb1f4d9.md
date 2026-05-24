---
domain: pub.towardsai.net
fetch_date: '2026-05-18T12:46:43.517277'
status: ok
url: https://pub.towardsai.net/explainable-ai-for-clip-the-architecture-explanation-and-its-application-for-segment-anything-b78ad5f05bb6
---

# Explainable AI for CLIP: The Architecture Explanation and its Application for Segment Anything

## A detailed explanation of the effective activation map visualization technique for CLIP and its application for Segment Anything

[ ![Yuki Shizuya](https://miro.medium.com/v2/resize:fill:64:64/1*XWF3sGAFbGgVo49OSKZUcw.jpeg) ](<https://medium.com/@ichigo.v.gen12?source=post_page---byline--b78ad5f05bb6--------------------------------------->)

[Yuki Shizuya](<https://medium.com/@ichigo.v.gen12?source=post_page---byline--b78ad5f05bb6--------------------------------------->)

10 min read

·

Aug 13, 2024

\--

Listen

Share

More

Press enter or click to view image in full size

The activation map corresponding to the target class adapted from [1]

Explainability is one of the crucial topics for AI models. Recent complicated AI tends to be a black box algorithm, making it difficult for humans to understand why the AI delivers those results. Recently, I read a paper, “CLIP Surgery for Better Explainability with Enhancement in Open-Vocabulary Tasks” [1], mainly about the explainable technique for CLIP. Although this paper shows the great explainability of CLIP, few blogs explain it. Thus, I will introduce the architecture of CLIP_Surgery and its application in this blog.

### Table of Contents

1. Quickly recap about CLIP
2. Explanation of CLIP Surgery algorithm
3. Application: Checking capability for real-world data and Points provider for Segment Anything

### 1\. Quickly recap about CLIP

CLIP is one of the game-changing AIs developed by OpenAI [2]. Thanks to its unique architecture, it is capable of zero-shot image classification. The architecture is shown below.

Press enter or click to view image in full size

CLIP architecture image adapted from [2]

CLIP has image and text encoders to create image and text embeddings. The training data is image and text pairs, such as a dog image with the text “The photo of a dog.” It utilizes contrastive pre-training to align the image and text embeddings if the image and text are a pair but not if they are not a pair. To understand intuitively, let’s consider the following example. In this example, we use three image and text pairs (_N = 3_ on the above original figure).

Press enter or click to view image in full size

The illustration of the contrastive pre-training from the author

The dimension of the output embedding from image and text encoders is always (1, 512) for each image and text. For this example, we have image and text embeddings with dimensions of (3, 512) for each. Using the cosine similarity of embeddings, we can calculate the similarity matrix, like the matrix in the above figure. In contrastive pre-training, CLIP utilizes this similarity matrix to align the matched pairs (= the diagonal elements) to get similar, but the other pairs(= the other elements) get dissimilar. To be concrete, the pseudo-code procedure from the paper [2] is shown as follows:

``` # image_encoder - ResNet or Vision Transformer# text_encoder - CBOW or Text Transformer# I[n, h, w, c] - minibatch of aligned images# T[n, l] - minibatch of aligned texts# W_i[d_i, d_e] - learned proj of image to embed# W_t[d_t, d_e] - learned proj of text to embed# t - learned temperature parameter# extract feature representations of each modalityI_f = image_encoder(I) #[n, d_i]T_f = text_encoder(T) #[n, d_t]# joint multimodal embedding [n, d_e]I_e = l2_normalize(np.dot(I_f, W_i), axis=1)T_e = l2_normalize(np.dot(T_f, W_t), axis=1)# scaled pairwise cosine similarities [n, n]logits = np.dot(I_e, T_e.T) * np.exp(t)# symmetric loss functionlabels = np.arange(n)loss_i = cross_entropy_loss(logits, labels, axis=0)loss_t = cross_entropy_loss(logits, labels, axis=1)loss = (loss_i + loss_t)/2 ```

After calculating the cosine similarity of the image and text embeddings, they apply cross-entropy loss so that the diagonal elements in the similarity matrix get to one, and the other elements do zero. The authors call this calculation a contrastive loss. CLIP is trained by only this contrastive loss.

For the zero-shot classification, the procedure is as follows. Firstly, we input the _n_ candidate texts and get embeddings with a dimension of (n, 512). Next, we calculate the similarities between the target image embedding and the candidate text embeddings. Finally, we can choose the most similar candidate as a class. Isn’t it so simple?

The procedure is simple and intuitive, but we need to train CLIP by millions of image and text pairs and hundreds of GPUs. From the original paper, they used a very large minibatch size of 32,768 and took 18 days to train on 592 V100 GPUs. Thus, many companies use this model as a foundation model and not train it from scratch.

### 2\. Explanation of CLIP Surgery algorithm

CLIP Surgery has been developed mainly to enhance the explainability of CLIP results. Surprisingly, CLIP Surgery can visualize the activation map corresponding to the label without any additional training. Because of its good activation map visualization, this technique can be applied to the Segmentation Anything, which is the foundation model for the segmentation task. I will introduce the application in a later section.

The authors thoroughly inspected the attention layers to achieve good explainability without training. Please see the figure below.

Press enter or click to view image in full size

CLIP Surgery architecture adapted from the paper [1]

The left part shows the original CLIP’s attention layer, while the right part shows the CLIP Surgery’s attention layer. They clarify that query-key self-attention activates the opposite semantic region corresponding to the label. On the other hand, the value-value self-attention can focus only on the semantic region. What does it mean? The figure below shows the activation map visualization of query-key self-attention and value-value self-attention.

Press enter or click to view image in full size

Activation map visualization of query-key attention and value-value attention adapted from the paper [1]

As you can see, the query key self-attention visualizes irrelevant region in addition to the target label region. Conversely, the value-value self-attention can focus on the corresponding target label region. Based on the experiments, the query-key self-attention may cause the feature map to be confused. Note that this fact is heuristic and hasn’t been derived by mathematical theorem.

Furthermore, they realized the activation map has redundant features across all labels. Please see the figure below.

CLIP activation maps for some labels adapted from the paper [1]

As you can see, the redundant region appears in the same location across the labels. Thus, they came up with the idea that they could remove the redundant features by removing the common activated region in all labels.

How did they achieve it? To be concrete, the official implementation is as follows.

``` # weights to restrain influence of obvious classes on others# (batch_size, 1, 512) @ (the number of labels, 512).T = (batch_size, 1, the number of labels)prob = image_features[:, :1, :] @ text_features.t()# prob has (batch_size, 1, the number of labels)prob = (prob * 2).softmax(-1)# w has (batch_size, 1, the number of labels)w = prob / prob.mean(-1, keepdim=True)# element-wise multiplied features# b is batch_size# n_t is the number of labels# n_i is the number of tokens (=197)# c is the feature dimension (=512)b, n_t, n_i, c = image_features.shape[0], text_features.shape[0], image_features.shape[1], image_features.shape[2]# feats has (batch_size, n_i, n_t, c)feats = image_features.reshape(b, n_i, 1, c) * text_features.reshape(1, 1, n_t, c)feats *= w.reshape(1, 1, n_t, 1)# redundant_feats has (batch_size, n_i, n_t, c)redundant_feats = feats.mean(2, keepdim=True) # along cls dimfeats = feats - redundant_feats# sum the element-wise multiplied features as cosine similarity# similarity has (batch_size, n_i, n_t)similarity = feats.sum(-1) ```

For better clarification, I added the dimension size transitions for each calculation in the code. Now, let’s figure out it step by step.

The first block calculates the weight vector to keep each class’s influence equal. Firstly, we extract the class token from an image embedding. In the transformer architecture, the class token is the first in the token dimension. Note that the class token is supposed to have information about all other tokens (If you are not familiar with Vision Transformer, you can refer to this blog [5]). Then, we calculate the cosine similarity and get the similarity matrix. Next, we convert the values of the similarity matrix to the probability along the label dimension and obtain the weight matrix.

In the second block, we calculate the feature matrix except for the redundant features. Firstly, we calculate the element-wise feature matrix of image and text embeddings. Intuitively, the activated region across the labels will have higher values in this map, as shown in the above figure. Thus, we can get the redundant features from the feature matrix by counting the mean across the labels. After subtracting the redundant features from the original feature matrix, we can obtain the pure feature matrix.

In the last block, we get the similarity matrix by summating of the feature matrix along the feature dimension.

For the feature map visualization, we need to normalize, reshape and interpolate the similarity matrix to the input image size (you can check the implementation using the attached code later) as postprocessing. The following picture shows the result of CLIP Surgery.

Press enter or click to view image in full size

CLIP Surgery activation map adapted from [1]

As you can see, it can capture the semantic region corresponding to the label. You can feel how powerful this visualization is.

We’ve seen the detailed algorithm of CLIP Surgery so far. In the last section, we will check its capability for real-world data and its application.

### 3\. Application: Checking capability for real-world data and Points provider for Segment Anything

In the last section, I will guide you through the application of CLIP Surgery for real-world data and Segment Anything (SAM). Let’s dive into them !

**Environment setup**

As the first step, you need to set an environment. I used ubuntu20.04, cuda11.7, and Python3.10 environment. Firstly, I create the virtual environment using conda.

```python conda create --name sam python==3.10 -yconda activate samconda install pip## optional: To avoid install libraries on the local environment, ## check the which pip will be used to store librarieswhich pip# I use /opt/conda/envs/sam/bin/pip in my enviornment. ```

Next, you need to install Pytorch and torchvision following [the official instruction](<https://pytorch.org/get-started/locally/#linux-anaconda>). You can install the version corresponding to your environment. For example, the command below is my case.

``` conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia ```

Then, you need to install the SAM repository and the model weight using the commands below.

```python pip install git+https://github.com/facebookresearch/segment-anything.gitwget https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth ```

You also need to install the CLIP Surgery repository.

``` git clone https://github.com/xmed-lab/CLIP_Surgery.git ```

Finally, you need to install several packages. You can install them via pip in the format of “pip install <library>.”

``` tqdm==4.66.5ftfy==6.2.3matplotlibopencv-pythonregex ```

Now, you have completed the environment setup.

**CLIP Surgery capability for Flickr30k dataset**

Firstly, I want to check the capability of CLIP Surgery for real-world data using Flickr30k dataset [4]. Therefore, I will compare the CLIP and the CLIP Surgery activation maps. I will attach the code used later. The figures below are the result of the comparison.

Press enter or click to view image in full size

The comparison between CLIP and CLIP Surgery activation maps

As you can see, the vanilla CLIP cannot detect objects precisely, but CLIP Surgery can detect objects corresponding to the label when objects exist. However, CLIP Surgery still has a problem when objects don’t exist, such as cat and plant. One of the reasons for this problem is min-max normalization in the postprocessing. When only irrelevant regions are in the activation map, min-max normalization may enhance the difference in their values. To fix this problem, we can simply add a threshold before min-max normalization. In the Flickr dataset case, the relevant region value threshold is more than 0.1, as checked by the histogram of the similarity maps. The results are shown below.

Press enter or click to view image in full size

The comparison between CLIP and CLIP Surgery activation maps after modification

Thanks to the threshold, we can remove the irrelevant regions. The threshold may be changed according to the dataset; thus, we should check and find the value using the histogram.

**Points provider for Segment Anything**

CLIP Surgery can be applied to the points provider for Segment Anything because of the preciseness of activation map visualization. For your information, SAM is one of the segmentation foundation models developed by Meta in 2023. The figure below shows the architecture.

Press enter or click to view image in full size

Segment Anything architecture adapted from the paper [3]

The segmentation capability of SAM is incredible. However, it is not trained by the segmentation dataset with labels, so we need to feed some points, bounding boxes or masks when we want to specify objects. As you can guess, these kinds of annotations are time-consuming. Here, CLIP Surgery helps us find the points automatically. Let’s see how to combine CLIP Surgery and SAM in the practical implementation.

To produce points for SAM, we downsample the activation map and sort the values to select the relevant region. In the official implementation, they use an activation map with the dimension of (7 x 7) to find the most relevant region. There is also a problem when the target object doesn’t exist, so I slightly modified the original implementation to add a threshold. The results are shown below.

Press enter or click to view image in full size

The results of the extracting points from CLIP Surgery given text

The orange points refer to the points related to the label, while the blue points represent the negative points of the label. As you can see, it can detect target label coordinates with decent accuracy. Note that the point’s accuracy comes from the CLIP capability. Therefore, it cannot be provided with target points accurately if CLIP doesn’t understand the target. I will attach a Jupyter notebook used in this application.

This is the end of this blog. Thank you for taking the time to read my blog!

### References

[1] Li, Y., Wang, H., et.al., [CLIP Surgery for Better Explainability with Enhancement in Open-Vocabulary Tasks](<https://arxiv.org/pdf/2304.05653>), _Arxiv_

[2] Radford, A., Kim, J., et.al., [Learning Transferable Visual Models From Natural Language Supervision](<https://arxiv.org/pdf/2103.00020>), _Arxiv_

[3] Kirillov, A., Ravi, N., Mintun, E., Mao, H., et.al., [Segment Anything](<https://arxiv.org/pdf/2304.02643>), _Arxiv_

[4] <https://www.kaggle.com/datasets/hsankesara/flickr-image-dataset>

[5] Callis, S., [Vision Transformers, Explained](<https://towardsdatascience.com/vision-transformers-explained-a9d07147e4c8>), Towards Data Science
