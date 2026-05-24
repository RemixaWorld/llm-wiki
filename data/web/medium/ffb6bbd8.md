---
domain: levelup.gitconnected.com
fetch_date: '2026-05-18T12:52:50.948920'
status: ok
url: https://levelup.gitconnected.com/how-to-train-your-pytorch-models-much-faster-14737c8c9770
---

# How To Train Your PyTorch Models (Much) Faster

## Tips and tricks I learnt while working with the best in the industry

[ ![Sahib Dhanjal](https://miro.medium.com/v2/resize:fill:64:64/1*N6hNlag3KYYZEGPSd4Clzw.jpeg) ](<https://sahibdhanjal.medium.com/?source=post_page---byline--14737c8c9770--------------------------------------->)

[Sahib Dhanjal](<https://sahibdhanjal.medium.com/?source=post_page---byline--14737c8c9770--------------------------------------->)

8 min read

·

Feb 10, 2025

\--

Listen

Share

More

My articles are free to read for everyone. If you don’t have a Medium subscription, read this article by [following this link](</how-to-train-your-pytorch-models-much-faster-14737c8c9770?sk=7c6ded73b9c50bd00752f9dc3496e65f>).

Press enter or click to view image in full size

Generated with Dall-E

Training deep learning models can sometimes feel like watching paint dry. Sometimes iterations are so slow that you find yourself banging your head against the keyboard, frustrated as you watch each epoch crawl by on your terminal. And that’s when you wonder:

> Is there a better way to do this?

Well, fret not! I’m back with another article sharing some tips/tricks making your deep learning workflow much more agile. I’ll share straightforward and clever coding tweaks that help you harness your computational resources more effectively. We’ll also dive into a host of industry-tested tips, tricks and tweaks that can extract every bit of performance from your hardware, so you can focus less on waiting and more on faster iterations.

## 1\. Enable Automatic Mixed Precision Training

If your GPU supports mixed precision training (think [AMD](<https://rocm.blogs.amd.com/artificial-intelligence/automatic-mixed-precision/README.html>)/[NVidia](<https://developer.nvidia.com/automatic-mixed-precision>) GPUs), PyTorch makes it incredibly easy and straightforward to enable it in your training schedule. Mixed precision training uses a mix of 16-bit and 32-bit numbers so you use less memory and get faster computations. Using these can provide significant speedups without having to rewrite your whole training loop.

Press enter or click to view image in full size

Source — [Sebastian Raschka’s Blog](<https://sebastianraschka.com/images/blog/2023/pytorch-faster/mixed-precision.png>)

You can easily enable it with `torch.cuda.amp.autocast()`. A simple snippet on usage can be:

```python import torchimport torch.nn as nnimport torch.optim as optim# define model, optimizer and criterion# define scaler using amp (Automatic Mixed Precision)scaler = torch.cuda.amp.GradScaler() # load inputs and labels with dataloaderfor inputs, labels in dataloader: inputs = inputs.cuda(non_blocking=True) labels = labels.cuda(non_blocking=True) optimizer.zero_grad() # enable mixed precision training with the scaler with torch.cuda.amp.autocast(): outputs = model(inputs) loss = criterion(outputs, targets) scaler.scale(loss).backward() scaler.step(optimizer) scaler.update() ```

## 2\. Find and Fix Bottlenecks

Like in all code, it is extremely imperative to profile your code to see where it is slow so that you can optimize it. PyTorch’s built-in [profiler](<https://pytorch.org/tutorials/recipes/recipes/profiler_recipe.html>) helps you spot the slower parts. Getting started is pretty easy:

```python import torch.profilerwith torch.profiler.profile( schedule=torch.profiler.schedule(wait=1, warmup=1, active=3), on_trace_ready=torch.profiler.tensorboard_trace_handler('./log'), record_shapes=True, with_stack=True) as prof: for inputs, targets in dataloader: outputs = model(inputs) loss = criterion(outputs, targets) loss.backward() optimizer.step() optimizer.zero_grad() prof.step() ```

With this, you can easily pinpoint the bottlenecks in your PyTorch code.

## 3\. Speed Up Your DataLoader

Sometimes, data loading itself bogs the whole training process down by a lot. Ensuring you’re using the right settings in PyTorch’s `DataLoader` can easily shave a few minutes off your training time by reducing the idle times between batches. For example specifying `num_workers` enables asynchronous data loading and copying. A solid example of some of the main settings would be:

```python from torch.utils.data import DataLoaderdataloader = DataLoader( dataset, batch_size=64, shuffle=True, num_workers=4, # Use as many workers as your CPU cores allow pin_memory=True, # Speeds up data transfer to the GPU prefetch_factor=2 # Preload batches (only after PyTorch v1.8.0)) ```

## 4\. Enable Static Compilation

[PyTorch 2.0](<https://pytorch.org/tutorials/intermediate/torch_compile_tutorial.html>) brought the feature `torch.compile` that transforms your dynamic model code into a highly optimized static version using a Just-In-Time (jit) model. This simple one-liner can incredibly cut down training overhead by a lot. Using it is as simple as wrapping your model up as follows:

```python import torchmodel = torch.compile(model, "max-autotune")# ormodel = torch.compile(model, "reduce-overhead") ```

## 5\. Scale Up With Distributed Training

For larger models or huge datasets, one GPU is seldom enough. Advances in distributed training helps you take advantage of multiple GPUs or even multiple machines on a network cutting your training time by orders of magnitude. There are 2 main approaches on how PyTorch support this:

### 5.1) Data Parallelism on a Single Machine

If you have more than one GPU, you can use `torch.nn.DataParallel` to split data between them:

```python import torch.nn as nnmodel = nn.Linear(100, 10)# Automatically split your data across available GPUsmodel = nn.DataParallel(model)model = model.cuda() ```

### 5.2) Serious Scaling using Distributed Data Parallel**(DDP)**

For multi-GPU or multi-node setups with multiple systems on a singular network, `DistributedDataParallel` (DDP) minimizes communication overhead for better performance:

```python import torch.distributed as distfrom torch.nn.parallel import DistributedDataParallel as DDP# Initialize the distributed environment# Make sure you set up your environment variables correctlydist.init_process_group(backend='nccl')model = nn.Linear(100, 10).cuda()model = DDP(model) ```

### 5.3) Leverage Gradient Accumulation

If you’re an independent researcher, I’m pretty sure you’re limited by GPU memory. One common way you can simulate larger batch sizes is by [accumulating gradients](<https://youtu.be/p4ZZq0736Po?t=487>) over several steps:

``` accumulation_steps = 4for i, (inputs, targets) in enumerate(dataloader): inputs, targets = inputs.cuda(non_blocking=True), targets.cuda(non_blocking=True) outputs = model(inputs) loss = criterion(outputs, targets) / accumulation_steps loss.backward() if (i + 1) % accumulation_steps == 0: optimizer.step() optimizer.zero_grad() ```

Implementation of this logic is pretty straightforward as can be seen above. Gradually updating your parameters this way makes it possible to get the benefits of a larger batch size without needing extra memory.

## 6\. Use Task-Specialized Libraries

This is for you if you’re really deep into deep learning (pun intended 😛) and are a serious researcher in academia/industry. Some of the specialized libraries you can use are:

### 6.1) PyTorch Lightning

Press enter or click to view image in full size

[Lightning.ai](<https://lightning.ai/>) Website

Lightning helps you clean up your boilerplate code and easily plug in optimizations. It also makes switching to distributed training or mixed precision a breeze. For example, the [Lightning Trainer](<https://lightning.ai/docs/pytorch/stable/common/trainer.html>) handles the entire training loop, including [40+ details](<https://lightning.ai/docs/pytorch/stable/common/trainer.html#trainer-flags>) for you. This includes automatically enabling/disabling grads, enabling better orchestration of multi-GPU training by putting batches and computations on the correct devices amongst a variety of other optimizations. Once your PyTorch code is organized into a `LightningModule`, the trainer can be invoked as simply as:

```python import pytorch_lightning as plimport torch.nn.functional as Fclass LitModel(pl.LightningModule): def __init__(self): super().__init__() self.layer = nn.Linear(100, 10) def forward(self, x): return self.layer(x) def training_step(self, batch, batch_idx): x, y = batch y_hat = self(x) loss = F.mse_loss(y_hat, y) return loss def configure_optimizers(self): return torch.optim.SGD(self.parameters(), lr=0.01)trainer = pl.Trainer(gpus=2, precision=16, accelerator='ddp')trainer.fit(LitModel(), dataloader) ```

A quick introduction and walkthrough can be found [here](<https://lightning.ai/docs/pytorch/stable/starter/introduction.html>).

### 6.2) NVIDIA Apex

If you’re specifically using Nvidia GPUs on your cluster, [Apex](<https://github.com/NVIDIA/apex>) is great for mixed precision and distributed training on them. It gives you more control over performance optimizations. Loading and using it is simply:

```python from apex import ampmodel, optimizer = amp.initialize(model, optimizer, opt_level="O1") ```

### 6.3) MicroSoft DeepSpeed

Press enter or click to view image in full size

Image Credits — [DeepSpeed](<https://www.microsoft.com/en-us/research/project/deepspeed/>)

For very large models, DeepSpeed is Microsoft’s answer to extreme performance during training. It uses smart techniques like ZeRO to reduce memory overhead and boost performance.

## 7\. Model Specific Optimizations

While you can improve your infrastructure as much as you like, there is also some merit in looking into optimizing your models. Not every task is the same, but sometimes a few fine-tuned tweaks can work wonders. Without going into too much detail, here are some approaches we can use to make our training much faster:

### 7.1) Fine-Tune Pretrained Models

Starting with a pretrained model and then fine-tuning instead of training from scratch can save you lots of time.

### 7.2) Reduce Model Size Using Pruning and Quantization

Pruning and Quantization is a very active field of research in the deep learning community. Several off-the-shelf algorithms do exist to achieve both tasks. PyTorch even provides its own library for quantization which can be used as follows:

```python import torch.quantizationmodel.qconfig = torch.quantization.get_default_qconfig('fbgemm')torch.quantization.prepare(model, inplace=True)# Calibrate with your datafor inputs, _ in calibration_dataloader: model(inputs)torch.quantization.convert(model, inplace=True) ```

### 7.3) Keep an Eye on Your Training Progress

Monitoring your model’s performance is key to understanding if your optimizations are working. If the loss is diverging after only a couple of epochs, more likely than not, the training is going to fail. Always use tools like [TensorBoard](<https://pytorch.org/tutorials/recipes/recipes/tensorboard_with_pytorch.html>) to visualize metrics in real time. Regular monitoring can help you catch any slowdowns early and tweak your methods accordingly.

### 7.4) Miscellaneous Best Practices

While they do deserve their own section, here’s a quick list of code tweaks that you can make to enable faster training:

* Disable gradient calculation for validation of inference
* Fuse Operations by using the `torch.compile` decorator
* Utilize OpenMP and NUMA Controls
* Use `.as_tensor()` instead of `.tensor()`
* Set gradients to `None` rather than `0`
* Use gradient clipping
* Turn off bias before the `BatchNorm` layer
* Turn off gradient computation during validation

I’ve intentionally listed only a few here. I you want a full blown list on why each works, consider checking out PyTorch’s [official blog](<https://pytorch.org/tutorials/recipes/recipes/tuning_guide.html>) on tuning.

## 8\. cuDNN and GPU Tweaks

This one, again, is for the ones using Nvidia GPUs. A few tweaks which can often go a long way are:

### 8.1) Enable cuDNN Auto-Tuner

If your input sizes are constant, setting

``` torch.backends.cudnn.benchmark = True ```

lets cuDNN run a short benchmark and choose the most efficient kernel for your hardware.

### 8.2) **Disable Deterministic Mode**

If reproducibility isn’t crucial, you might achieve a slight speed bump by setting

``` torch.backends.cudnn.deterministic = False ```

### 8.3) Use Non-Blocking Transfers

When moving data to the GPU, pass `non_blocking=True` (as shown in the mixed precision example) to allow for asynchronous transfers.

## Summary

As previously stated, every model is different, and techniques that can be used to train them more efficiently are different as well. If there’s just one thing I’d like you to take away from this article, it will be this —

> It’s not about buying beefy hardware, but more about writing smart code and fine-tuning every part of your pipeline to achieve significant speed ups.

While this list isn’t an exhaustive, it walks you through some of the various techniques which experts in the field use to train models (**_much_**) faster than your average Joe. If you too, have been exposed to techniques which you use on a daily basis, I’d be glad if you’d post them in the comments. In the end, the more you share, the more you learn! ;)

**Enjoyed this post?** Help me share this knowledge with others by clapping, and sharing your thoughts. You can follow me on [**Medium**](<https://sahibdhanjal.medium.com/>) / [**LinkedIn**](<https://www.linkedin.com/in/sahibdhanjal/>) for more insights on C++, Python, Robotics and Trading algorithms.
