---
domain: twitter.com
fetch_date: '2026-05-18T12:34:48.674207'
note_fallback: true
status: ok
url: https://twitter.com/svpino/status/1775154270708396215
---

# 判断训练集和验证集同分布的技巧

来源：https://twitter.com/svpino/status/1775154270708396215  
其他更多技巧课程：https://www.ml.school/  

I want to show you a clever trick you didn't know before.

Imagine you have six months' worth of data. You want to build a model, so you take the first five months to train it. Then, you use the last month to test it.

This is a common approach for building machine learning models.

Unfortunately, you may find out your model works well with the train data but sucks on the test data.

Overfitting is not weird. We've all been there. But often, the worst you can do is try and fix it before understanding why it’s happening.

Ask anyone about this, and they will give you their favorite step-by-step guide on regularizing a model. They will jump right in and try to fix overfitting. Don’t do this.

There's a different way. A better way.

Here is the question I want you to answer before you start racking your brain trying to fix a model:

Do your test and training data come from the same distribution?

When building a model, we assume the train and test come from the same place. Unfortunately, this is not always the case.

Here is where the trick I promised comes in:

1. Put your train and test set together.

2. Get rid of the target column.

3. Create a new binary feature, and set every sample from your train set to 0 and every sample from the test set to 1. This feature will be the new target.

Now, train a simple binary classification model on this new dataset. The goal of this model is to predict whether a sample comes from the train or the test split.

The intuition behind this idea is simple:

If all your data comes from the same distribution, this model won't work. But if the data comes from different distributions, the model will learn to separate it.

After you build a model, you can use the ROC-AUC to evaluate it. If the AUC is close to 0.5, your model can't separate the samples. This means your training and test data come from the same distribution. If the AUC is closer to 1.0, your model learned to differentiate the samples. Your training and test data come from different distributions.

This technique is called Adversarial Validation. It's a clever, fast way to determine whether two datasets come from the same source.

If your splits come from different distributions, you won't get anywhere. You can't out-train bad data.

But there's more!

You can also use Adversarial Validation to identify where the problem is coming from:

1. Compute the importance of each feature.

2. Remove the most important one from the data.

3. Rebuild the adversarial model.

4. Recompute the ROC-AUC again.

You can repeat this process until the ROC-AUC is close to 0.5 and the model can’t differentiate between training and test samples.

Adversarial Validation is especially useful in production applications to identify distribution shifts.

Low investment with a high return.
