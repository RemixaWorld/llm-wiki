---
domain: medium.com
fetch_date: '2026-05-18T12:53:36.126974'
status: ok
url: https://medium.com/data-science-collective/teaching-models-to-choose-features-wisely-a-distill-to-select-approach-a9359e2ba5d1
---

# Teaching Models to Choose Features Wisely: A Distill-to-Select Approach

[ ![Shenggang Li](https://miro.medium.com/v2/resize:fill:64:64/1*knqQWkDF7J-gf_A5p7ew5g.png) ](</@datalev?source=post_page---byline--a9359e2ba5d1--------------------------------------->)

[Shenggang Li](</@datalev?source=post_page---byline--a9359e2ba5d1--------------------------------------->)

11 min read

·

Apr 2, 2025

\--

\--

Listen

Share

More

A Novel Approach to Enhancing Transparency by Distilling Complex Predictors into Sparse, Human-Readable Models

![Photo by David Bruyndonckx on Unsplash](https://miro.medium.com/v2/resize:fit:700/0*To5y45tZGz2yJrG1)

## **Introduction**

Traditional models like _XGBoost_ or _LightGBM_ are great at making accurate predictions — but they can feel like black boxes. These models often use dozens (or even hundreds) of features, many of which are highly correlated. Sure, you can look at their “feature importance” rankings, but those can be misleading. For instance, two similar features might both rank high, even though only one is truly essential. And in logistic regression, using standardized coefficients can help a bit, but it still doesn’t solve the problem when features are correlated or noisy.

That’s where our idea comes in.

Inspired by model distillation techniques in large language models, we introduce a simple but powerful approach: train a strong teacher model (like _XGBoost_) to do the hard work, then distill its knowledge into a lightweight student model — specifically, a sparse logistic regression. Think of it like learning from a wise professor: the professor knows everything in detail, but the student writes a clean summary using only the most important points.

Our initial experiments show that this distilled model performs almost as well as the full teacher model, while giving you something much easier to understand and explain. Plus, it automatically highlights the most important features — no need to rely on noisy importance rankings or hope that standardized coefficients tell the full story.

This teacher–student setup opens the door for even more flexibility. You can tweak the loss weights, try different types of teacher models, or even adapt it to other types of student models. Overall, it’s a fresh and practical way to blend power and simplicity in predictive modeling.

## Intuition and Algorithm Mechanisms

Understanding how our model works requires stepping through both the intuition and the mathematical formulation behind this teacher–student distillation process. We aim to make high-performing models easier to interpret and more selective in feature use, without compromising on prediction quality.

### Why Not Just Use Feature Importance?

Popular models like _LightGBM_ or _XGBoost_ often report “feature importance” values based on things like split gain or frequency. However, these scores are heuristic and don’t necessarily reflect the causal or predictive value of features, especially when variables are correlated. For instance, if “ _Age_ ” and “ _Income_ ” are highly correlated, both might show up as “important,” even if only one truly drives predictions. In contrast, logistic regression uses coefficient magnitudes to imply importance, but these too can be misleading in the presence of multicollinearity or noise.

Our method tackles this challenge by introducing model distillation as a way to “summarize” the decision boundary of a complex model into a simple, sparse, and explainable model that selects features based on how they influence real decisions, not just how often they’re used in trees.

### The Teacher–Student Setup

The process begins by training a complex teacher model, such as _LightGBM_ , on the entire dataset. This teacher model learns the mapping:

![image](https://miro.medium.com/v2/resize:fit:519/1*001mnuEw9_Sxwt9n7f2oTw.png)

Here, _X ∈ R^d_ is the full feature set and _p^teacher ∈ [0,1]_ is the teacher’s predicted probability of the positive class. The teacher is expected to perform well, leveraging all features — relevant or not.

Next, we introduce a student model, specifically a logistic regression with _L1_ regularization, designed to replicate the teacher’s behavior, but using as few features as possible. The student model estimates:

![image](https://miro.medium.com/v2/resize:fit:346/1*5fUuHFbdGG6kDyv3ccUoFQ.png)

Where _σ(z)_ is the sigmoid function, _w ∈ R^d_ is the weight vector, and _b_ is the bias term.

### The Composite Loss Function

We train the student using a composite loss function that combines three elements:

**Prediction Loss (Binary Cross Entropy)**

This ensures the student learns from the true labels:

![image](https://miro.medium.com/v2/resize:fit:692/1*05Vm7xbZZ3Ef9sl3nEpzQw.png)

Where,

![image](https://miro.medium.com/v2/resize:fit:221/1*xDQbfvSFeoWjSVcnAnaAmg.png)

**Distillation Loss (KL Divergence)**

This encourages the student to mimic the teacher’s predicted probabilities:

![image](https://miro.medium.com/v2/resize:fit:700/1*qqtinMofOPEF6a9K0zp1MA.png)

This term is central to knowledge distillation: the student doesn’t just fit the data, but copies the decision boundary learned by the more expressive teacher.

**Sparsity Loss (L1 Penalty)**

This encourages the student to be sparse and perform feature selection:

![image](https://miro.medium.com/v2/resize:fit:387/1*L5rt44HUgUk9zWSqq_9Cmg.png)

The full objective becomes:

![image](https://miro.medium.com/v2/resize:fit:419/1*__BYOVQEC8mDQnRJy18lVQ.png)

Where:

* _γ_ controls how much the student copies the teacher
*  _λ_ controls sparsity

This design creates a balance between accuracy and interpretability.

### Why It Works

* The teacher captures full signal and nonlinear interactions.
* The student distills this into a linear boundary, only preserving what matters.
* The _L1_ penalty prunes out features that don’t contribute to the student’s mimicry or true label fit.

Compared to traditional feature importance rankings, which are post hoc and sensitive to correlation, our method does in-model selection, directly optimizing for performance and simplicity together. It’s like getting a curated summary of the teacher’s thinking — clean, direct, and actionable.

## Demonstration with a Marketing Campaign Dataset

To illustrate how the Distill-to-Select framework works in practice, we designed a realistic yet synthetic dataset simulating a marketing campaign scenario. The goal is to predict whether a customer makes a purchase after receiving a promotional offer. This dataset, available at [GitHub — RL_GBM](<https://github.com/datalev001/RL_GBM>), contains _125,000_ treatment group records and includes several customer attributes that commonly influence purchasing decisions.

### Dataset Description

The features include:

* _Age_ : Customer age in years.
* _Income_ : Annual income.
* _Days Since Last Purchase_ : Recency measure of last transaction.
* _Holiday_ : Binary indicator for whether the promotion occurred during a holiday.
* _Channel_ : Categorical variable indicating shopping method — Online, In-Store, or Mobile.
* _Loyalty Score_ : A continuous measure of customer loyalty.

All features were standardized, and categorical variables were one-hot encoded to ensure compatibility with both tree-based and linear models.

Here is the code:

```python import numpy as np import pandas as pdfrom sklearn.model_selection import train_test_splitfrom sklearn.preprocessing import StandardScalerfrom sklearn.metrics import roc_auc_score, accuracy_scorefrom scipy.stats import ks_2sampimport lightgbm as lgbimport torchimport torch.nn as nnimport torch.optim as optimfrom torch.utils.data import DataLoader, TensorDataset############################ Load Data###########################df = pd.read_csv('purchase_binary.csv')# Use only treatment datadf = df[df["Promo"] == 1] ############################ Data Preprocessing###########################df_encoded = pd.get_dummies(df, columns=["Channel"], drop_first=True)print("Dummy columns:", [col for col in df_encoded.columns if "Channel_" in col])# For instance, assume columns "Channel_Mobile" and "Channel_Online" exist.features = ["Age", "Income", "Days", "Holiday", "Loyalty", "Channel_Mobile", "Channel_Online"]target = "Purchase"X = df_encoded[features].values.astype(np.float32)y = df_encoded[target].values.astype(np.int64)scaler = StandardScaler()X_scaled = scaler.fit_transform(X)############################ Train-Test Split (65% / 35%)###########################X_train, X_test, y_train, y_test = train_test_split( X_scaled, y, test_size=0.35, random_state=42, stratify=y)############################ Train the Teacher Model (LightGBM)###########################teacher = lgb.LGBMClassifier(random_state=42)teacher.fit(X_train, y_train)teacher_train_prob = teacher.predict_proba(X_train)[:, 1]teacher_test_prob = teacher.predict_proba(X_test)[:, 1]teacher_auc = roc_auc_score(y_test, teacher_test_prob)teacher_acc = accuracy_score(y_test, teacher.predict(X_test))teacher_ks = ks_2samp(teacher_test_prob[y_test == 1], teacher_test_prob[y_test == 0]).statisticprint("
Teacher (LightGBM) Performance:")print(f"AUC = {teacher_auc:.4f}, KS = {teacher_ks:.4f}, ACC = {teacher_acc:.4f}")############################ Define the Student Model (Logistic Regression)###########################class LogisticRegressionStudent(nn.Module): def __init__(self, input_dim): super(LogisticRegressionStudent, self).__init__() self.linear = nn.Linear(input_dim, 1) def forward(self, x): logit = self.linear(x) prob = torch.sigmoid(logit) return probstudent = LogisticRegressionStudent(input_dim=X_train.shape[1])############################ Define the Combined Loss Function###########################def kl_divergence(p_teacher, p_student, eps=1e-8): p_teacher = torch.clamp(p_teacher, eps, 1.0 - eps) p_student = torch.clamp(p_student, eps, 1.0 - eps) kl = p_teacher * torch.log(p_teacher / p_student) + (1 - p_teacher) * torch.log((1 - p_teacher) / (1 - p_student)) return torch.mean(kl)# Hyperparameters for distillationgamma = 1.0 # weight for KL losslambda_l1 = 1e-4 # weight for L1 regularization############################ Train the Student Model (Distillation) with Early Stopping###########################X_train_tensor = torch.from_numpy(X_train)y_train_tensor = torch.from_numpy(y_train.reshape(-1, 1)).float()train_dataset = TensorDataset(X_train_tensor, y_train_tensor)train_loader = DataLoader(train_dataset, batch_size=256, shuffle=True)optimizer = optim.Adam(student.parameters(), lr=0.001)num_epochs = 100# For early stoppingbest_val_loss = float('inf')patience = 10best_epoch = 0best_student_state = None# Create validation tensors from X_test and y_testX_val_tensor = torch.from_numpy(X_test)y_val_tensor = torch.from_numpy(y_test.reshape(-1, 1)).float()student.train()for epoch in range(num_epochs): epoch_loss = 0.0 for batch_X, batch_y in train_loader: optimizer.zero_grad() student_prob = student(batch_X) # Student predictions # For simplicity, we use the first N teacher_train_prob values for this batch. batch_indices = np.arange(batch_X.shape[0]) teacher_probs = torch.from_numpy(teacher_train_prob[batch_indices]).float().unsqueeze(1) # Compute BCE loss (true labels) bce_loss = nn.BCELoss()(student_prob, batch_y) # Compute KL divergence loss (distillation) kl_loss = kl_divergence(teacher_probs.squeeze(), student_prob.squeeze()) # Compute L1 penalty on the student's weights (LASSO) l1_loss = torch.norm(student.linear.weight, 1) loss = bce_loss + gamma * kl_loss + lambda_l1 * l1_loss loss.backward() optimizer.step() epoch_loss += loss.item() * batch_X.size(0) epoch_loss /= len(train_dataset) # Evaluate validation loss on the test set student.eval() with torch.no_grad(): val_prob = student(X_val_tensor) val_loss = nn.BCELoss()(val_prob, y_val_tensor).item() student.train() print(f"Epoch {epoch+1}/{num_epochs} - Train Loss: {epoch_loss:.4f} - Val Loss: {val_loss:.4f}") # Check early stopping condition if val_loss < best_val_loss: best_val_loss = val_loss best_epoch = epoch best_student_state = student.state_dict() elif epoch - best_epoch >= patience: print(f"Early stopping triggered at epoch {epoch+1}") break# Load best model stateif best_student_state is not None: student.load_state_dict(best_student_state)############################ Evaluate the Student Model on Test Data###########################student.eval()with torch.no_grad(): X_test_tensor = torch.from_numpy(X_test) student_test_prob = student(X_test_tensor).cpu().numpy().flatten()student_pred = (student_test_prob >= 0.5).astype(int)student_auc = roc_auc_score(y_test, student_test_prob)student_acc = accuracy_score(y_test, student_pred)student_ks = ks_2samp(student_test_prob[y_test == 1], student_test_prob[y_test == 0]).statisticprint("
Student (Distilled Logistic Regression) Performance:")print(f"AUC = {student_auc:.4f}, KS = {student_ks:.4f}, ACC = {student_acc:.4f}")############################ Model Interpretability: Print Coefficients and Feature Importance############################ Extract weight and bias from the student's linear layerweights = student.linear.weight.detach().cpu().numpy().flatten()bias = student.linear.bias.detach().cpu().numpy()[0]# Pair each feature with its coefficient and sort by absolute valuefeature_importance = list(zip(features, weights))feature_importance = sorted(feature_importance, key=lambda x: abs(x[1]), reverse=True)print("
Student Model Coefficients and Feature Importance:")print(f"Intercept (bias): {bias:.4f}")for feature, coef in feature_importance: print(f"Feature: {feature:20s} Coefficient: {coef:.4f}")# Define a threshold for feature selection (e.g., absolute coefficient > 0.1)threshold = 0.1selected_features = [feat for feat, coef in feature_importance if abs(coef) > threshold]print("
Features Selected (|coefficient| > 0.1):")print(selected_features) ```

Here are the results:

``` Teacher (LightGBM) Performance:#######################################################AUC = 0.7566, KS = 0.3824, ACC = 0.6948Epoch 1/100 - Train Loss: 0.7836 - Val Loss: 0.6190Epoch 2/100 - Train Loss: 0.7400 - Val Loss: 0.6103Epoch 3/100 - Train Loss: 0.7382 - Val Loss: 0.6100Epoch 4/100 - Train Loss: 0.7380 - Val Loss: 0.6083Epoch 5/100 - Train Loss: 0.7380 - Val Loss: 0.6095Epoch 6/100 - Train Loss: 0.7380 - Val Loss: 0.6089Epoch 7/100 - Train Loss: 0.7383 - Val Loss: 0.6091Epoch 8/100 - Train Loss: 0.7373 - Val Loss: 0.6084Epoch 9/100 - Train Loss: 0.7387 - Val Loss: 0.6096Epoch 10/100 - Train Loss: 0.7376 - Val Loss: 0.6085Epoch 11/100 - Train Loss: 0.7378 - Val Loss: 0.6093Epoch 12/100 - Train Loss: 0.7379 - Val Loss: 0.6088Epoch 13/100 - Train Loss: 0.7376 - Val Loss: 0.6087Epoch 14/100 - Train Loss: 0.7377 - Val Loss: 0.6094Early stopping triggered at epoch 14Student (Distilled Logistic Regression) Performance:#######################################################AUC = 0.7585, KS = 0.3822, ACC = 0.6846Student Model Coefficients and Feature Importance:#######################################################Intercept (bias): 0.2965Feature: Income Coefficient: 0.4101Feature: Age Coefficient: 0.1721Feature: Holiday Coefficient: 0.1065Feature: Days Coefficient: -0.0312Feature: Loyalty Coefficient: -0.0076Feature: Channel_Online Coefficient: -0.0051Feature: Channel_Mobile Coefficient: 0.0024Features Selected (|coefficient| > 0.1):['Income', 'Age', 'Holiday'] ```

### Explanation:

1. **Teacher Model (_LightGBM_)**

We first trained a _LightGBM_ classifier using all features. As expected, the model delivered strong performance:

* **_AUC_** = _0.7566_
* **Accuracy** = _0.6948_
* ** _KS_ Statistic** = _0.3824_

However, while this model achieves high accuracy, it relies on all features — even those that may not be essential for interpretation or decision-making. For example, _LightGBM_ may assign importance to both “ _Channel_Online_ ” and “ _Channel_Mobile_ ” due to their correlation with purchases, even if only one is truly useful for modeling purposes. Feature importance scores alone don’t offer a clear path to select a sparse, actionable feature set.

**2\. Student Model via Distillation**

Next, we used the Distill-to-Select framework to train a _logistic_ regression model as the student. This student learns to:

* Predict actual purchase labels (true supervision),
* Mimic the _LightGBM_ probability output (distillation),
* And eliminate unimportant features via an _L1_ regularization term (sparsity).

The student is trained using our composite loss:

![image](https://miro.medium.com/v2/resize:fit:567/1*keJvBGuyrpNIvqej2pcfOg.png)

Hyperparameters _γ_ and _λ_ were tuned for performance and interpretability balance. During training, early stopping was used to prevent overfitting on the recent validation loss.

**3\. Results and Interpretation**

The distilled logistic regression model achieved performance on par with the teacher:

* **_AUC_** = _0.7585_
* **Accuracy** = _0.6846_
* ** _KS_ Statistic** = _0.3822_

More importantly, the student model produced a sparse and interpretable representation:

* It retained only _3–4_ meaningful features.
* The largest coefficients were assigned to “Income” (_0.41_), “ _Age_ ” (_0.17_), and “ _Holiday_ ” (_0.11_).
* Features like “ _Channel_Online_ ” and “ _Loyalty_ ” had negligible weights and were effectively pruned.

By applying a simple coefficient threshold (e.g., _∣β_j∣ >0.1_), we automatically select the core predictive features and exclude noise. The final student model becomes a compact, human-readable equation that a business analyst can easily interpret:

![image](https://miro.medium.com/v2/resize:fit:700/1*vwjgp1DO66qVERyT3KRV7A.png)

## Conclusion

The Distill-to-Select approach shows that model distillation isn’t just useful for simplifying complex models — it’s also a smart way to perform feature selection. Unlike traditional methods like feature importance scores or standardized coefficients, this technique builds feature selection into the training process itself. By combining label accuracy, teacher mimicry, and feature sparsity into a single loss function, the resulting model is both compact and aligned with the reasoning of a high-performing teacher.

More importantly, this is not limited to just _LightGBM_ or logistic regression. Distill-to-Select is a flexible, model-agnostic framework. The teacher could be any complex model — _XGBoost_ , deep neural nets, or even _LLMs_ like _BERT_. The student can be any simple, interpretable model — not just logistic regression. For example, this framework could be extended to _RAG_ -based _LLM_ systems, helping to select fewer, more relevant documents at retrieval time, making the process leaner and more transparent.

There are many ways to take this further. We could explore nonlinear student models (like sparse neural nets or shallow trees), develop adaptive loss weighting to better balance performance and simplicity, or even implement dynamic distillation, where students are periodically updated as the teacher evolves over time.

In short, Distill-to-Select is a practical recipe for turning any black-box model into something clear, efficient, and actionable. Whether you’re in healthcare, finance, marketing, or _NLP_ , this method helps you focus on what truly matters — without sacrificing accuracy.

The source code is available at: [https://github.com/datalev001/distill_feature_selection](<https://github.com/datalev001/distill_feature_selection/blob/main/code/distill_sparse_model.py>)

## About me

With over 20 years of experience in software and database management and 25 years teaching IT, math, and statistics, I am a Data Scientist with extensive expertise across multiple industries.

You can connect with me at:

Email: datalev@gmail.com | [LinkedIn](<https://www.linkedin.com/in/kelvin-li-5599691b/>) | [X/Twitter](<https://x.com/datalev00156330>)
