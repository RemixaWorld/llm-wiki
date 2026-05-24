---
domain: pub.towardsai.net
fetch_date: '2026-05-18T12:52:41.826354'
status: ok
url: https://pub.towardsai.net/reinforcement-learning-driven-adaptive-model-selection-and-blending-for-supervised-learning-09f5dfda5426
---

# Reinforcement Learning-Driven Adaptive Model Selection and Blending for Supervised Learning

## Inspired by Deepseeker: Dynamically Choosing and Combining ML Models for Optimal Performance

[ ![Shenggang Li](https://miro.medium.com/v2/resize:fill:64:64/1*knqQWkDF7J-gf_A5p7ew5g.png) ](<https://medium.com/@datalev?source=post_page---byline--09f5dfda5426--------------------------------------->)

[Shenggang Li](<https://medium.com/@datalev?source=post_page---byline--09f5dfda5426--------------------------------------->)

17 min read

·

Feb 3, 2025

\--

Listen

Share

More

Press enter or click to view image in full size

Photo by [Agence Olloweb](<https://unsplash.com/@olloweb?utm_source=medium&utm_medium=referral>) on [Unsplash](<https://unsplash.com/?utm_source=medium&utm_medium=referral>)

## Introduction

Machine learning model selection has always been a challenge. Whether you’re predicting stock prices, diagnosing diseases, or optimizing marketing campaigns, the question remains: which model works best for my data? Traditionally, we rely on cross-validation to test multiple models — _XGBoost_ , _LGBM_ , Random Forest, etc. — and pick the best one based on validation performance. But what if different parts of the dataset require different models? Or what if blending multiple models dynamically could improve accuracy?

This idea hit me while reading about Deepseeker R1, an advanced large language model (_LLM_) that adapts dynamically to improve performance. Inspired by its reinforcement learning (_RL_)-based optimization, I wondered: can we apply a similar _RL_ -driven strategy to supervised learning? Instead of manually selecting a model, why not let reinforcement learning learn the best strategy for us?

Imagine an RL agent acting like a data scientist — analyzing dataset characteristics, testing different models, and learning which performs best. Even better, rather than just picking one model, it could blend models dynamically based on data patterns. For instance, in a financial dataset, _XGBoost_ might handle structured trends well, while _LGBM_ might capture interactions better. Our _RL_ system could switch between them intelligently or even combine them adaptively.

This paper proposes a novel Reinforcement Learning-Driven Model Selection and Blending framework. We frame the problem as a Markov Decision Process (_MDP_), where:

* The state represents dataset characteristics.
* The action is selecting or blending different _ML_ models.
* The reward is based on model performance.
* The policy is trained using _RL_ to find the best model selection strategy over time.

Unlike traditional approaches that apply a single best model across an entire dataset, this _RL_ -driven method learns to choose the best model per data segment, or even blend models dynamically. This approach can automate, optimize, and personalize machine learning pipelines — reducing human intervention while improving predictive performance.

By the end of this paper, we’ll see how reinforcement learning can transform model selection, making it adaptive, intelligent, and more efficient — just like a skilled data scientist who constantly learns and refines their choices.

## Methodology: Reinforcement Learning for Adaptive Model Selection in Supervised Learning

I will describe the adaptive selection and blending of machine learning models as a Markov Decision Process (_MDP_) defined by the tuple _(S, A, P, R, γ)_ , where:

* _S_ is the set of states, representing the current statistical summary of the dataset (e.g., mean and variance of features),
* _A_ is the set of actions, corresponding to selecting individual models _{XGB, LGBM, RF, DNN, Blend}_ ,
* _P(s′∣s, a)_ defines the transition probabilities from the current state sss to the next state _s′_ ,
* _R(s, a)_ is the immediate reward received after taking action _a_ in state sss,
* _γ ∈ [0,1]_ is the discount factor that weighs immediate rewards versus future.

The goal of the reinforcement learning agent is to learn an optimal policy _π∗(s)_ that maximizes the expected cumulative reward over time:

The reward _R(s, a)_ at time _t_ is defined as:

Where _AUC_ and _KS_ evaluate model prediction performance, and the penalty function balances model complexity (e.g., a higher penalty is applied to complex models like _DNN_ or blending strategies).

### State Representation and Actions

In many cases, the state sss is defined by feature-level summaries of the dataset, such as:

where _μ(X)_ are the mean and variance vectors of the feature set _X_. Actions _a_t_ ​ can either select an individual model (e.g., _XGB_) or a weighted blend of multiple model predictions:

where _w_i_ ​ are blending weights, and _y^i_ ​ are predicted probabilities from each model.

### Q-Learning and Model Evaluation

The heart of the reinforcement learning approach in this paper lies in solving the optimization problem of estimating the state-action value function _Q(s, a)_ , which represents the expected cumulative reward starting from state sss, taking action _a_ , and following a policy _π_. Here, the “state” sss is not just a generic concept — it encodes meaningful information about the data at hand, such as the statistical properties (mean, variance) of features, while the “action” _a_ corresponds to selecting a specific model (e.g., _XGBoost_ , _LightGBM_ , RandomForest, _DNN_ , or Blend) to make predictions.

The function _Q(s, a)_ can be written as:

, where _R(s, a)_ is the immediate reward from the model (based on _AUC + KS — Penalty_) after selecting action _a_ , and _γ_ is the discount factor that determines how much importance is given to future rewards. The goal of reinforcement learning is to maximize this cumulative reward by intelligently selecting models over time, and adapting as the data evolves.

### Multi-Armed Bandit Method: Quick Model Selection Without Complexity

The multi-armed bandit approach treats the problem as stateless and memoryless, where rewards are independent across episodes. In the context of this paper, each action _a_ is one of the candidate models (e.g., _XGBoost_ or _LightGBM_) or a blend of models. When action _a_ is taken, we observe an immediate reward _R(a)_ based on how well the selected model performs on metrics such as _AUC_ and _KS_.

The update rule for the _Q-value_ is

where,

is the learning rate, and _N(a)_ is inversely proportional to the number of times the model _a_ has been selected? The epsilon-greedy policy ensures a balance between exploring less-used models and exploiting the current best-performing one:

For example, in the earlier episodes, the bandit might explore _DNN_ or blended models, once it consistently observes _XGBoost_ achieving superior rewards (e.g., a high _AUC_ with minimal penalties), it will converge toward frequent exploitation of _XGBoost_. This approach works well when model performance does not depend heavily on the state of the data.

### Deep Q-Network (DQN) Approach: When State Transitions Matter

Unlike the multi-armed bandit, the _DQN_ approach generalizes the problem by considering state transitions and long-term rewards. In this paper, the state sss is defined by the statistical properties of the dataset (e.g., mean and variance of the features), which can change over time due to shifting data distributions. The agent’s task is to choose the optimal model for the current state sss while anticipating how future states and rewards may evolve.

Q-values are approximated using a deep neural network _Q(s, a; θ)_ , where _θ_ represents the network parameters. The update is performed by minimizing the temporal difference (_TD_) error:

Training the _DQN_ involves experience replay, where past state-action-reward transitions _(s, a, r, s′)_ are stored in a buffer and sampled randomly to stabilize training. This prevents overfitting to recent transitions and allows for better generalization across various states.

For example, suppose the current state _s_ reflects a noisy dataset with high feature correlations (multicollinearity), this generally makes simple models like RandomForest ineffective. The _DQN_ learns to avoid selecting RandomForest in this state and instead prioritize blending _XGBoost_ and DNN predictions, which generalize better under noisy conditions. As the state evolves — e.g., when noise levels decrease — the _DQN_ dynamically updates its policy to exploit simpler models again.

### Comparison: Exploration vs. Exploitation in Model Selection

Both approaches rely on the epsilon-greedy policy to explore models selected less frequently while exploiting the currently known best-performing model. However, the _DQN_ approach introduces a more sophisticated exploration mechanism through the generalization power of neural networks. In dynamic scenarios where feature distributions change over time (e.g., in streaming financial datasets), the _DQN_ learns to identify patterns across states and adjusts its model selection strategy accordingly.

### Example Illustration: Choosing Between XGBoost and Blended Models

Consider an evolving financial dataset where the task is to predict loan defaults. In the initial state, where features exhibit strong linear separability, _XGBoost_ may dominate due to its ability to handle tabular data efficiently. As the dataset transitions to a noisier state with overlapping features, a blended model combining _XGBoost_ and _DNN_ predictions may yield higher rewards due to its robustness. The agent continuously monitors the mean _AUC_ and _KS_ metrics from past decisions and updates its _Q-values_ to reflect these changing conditions.

* In the Multi-Armed Bandit: The agent may converge to frequent exploitation of _XGBoost_ based on early successes, missing opportunities when blended models perform better in noisy states.
* In the _DQN_ : The agent dynamically adjusts its selection by tracking state transitions, selecting blended models when noise increases, and reverting to XGBoost during clean data periods.

### Combining Both Approaches

The multi-armed bandit method provides a computationally efficient solution when rewards are independent and immediate, making it suitable for online model selection tasks.

Meanwhile, the _DQN_ approach excels in dynamic environments where rewards depend on evolving data distributions, such as time-series forecasting or financial modeling.

Combining these approaches, this paper offers a robust framework for adaptive model selection and blending across a wide range of supervised learning tasks.

## Data and Code Experiment

We begin by testing the Multi-Armed Bandit Method using the provided data and code, evaluating model selection performance through dynamic exploration and reward-based updates.

```python import numpy as npimport pandas as pdfrom sklearn.model_selection import train_test_splitfrom sklearn.metrics import roc_auc_scorefrom sklearn.ensemble import RandomForestClassifierfrom xgboost import XGBClassifierfrom lightgbm import LGBMClassifierimport torchimport torch.nn as nnimport torch.nn.functional as F# Read the dataset from CSVdata = pd.read_csv('rein_data_binary.csv')X = data.drop('label', axis=1)y = data['label']# ---------------------------------------------# 2) Metrics (AUC, KS)# ---------------------------------------------def calc_ks_score(y_true, y_prob): data = pd.DataFrame({'y_true': y_true, 'y_prob': y_prob}).sort_values('y_prob', ascending=False) data['cum_pos'] = (data['y_true'] == 1).cumsum() data['cum_neg'] = (data['y_true'] == 0).cumsum() total_pos = data['y_true'].sum() total_neg = (data['y_true'] == 0).sum() data['cum_pos_rate'] = data['cum_pos'] / total_pos data['cum_neg_rate'] = data['cum_neg'] / total_neg data['ks'] = data['cum_pos_rate'] - data['cum_neg_rate'] return data['ks'].max()# ---------------------------------------------# 3) PyTorch DNN Model# ---------------------------------------------class DNNModel(nn.Module): def __init__(self, input_dim=5): super(DNNModel, self).__init__() self.fc1 = nn.Linear(input_dim, 16) self.fc2 = nn.Linear(16, 8) self.out = nn.Linear(8, 1) def forward(self, x): x = F.relu(self.fc1(x)) x = F.relu(self.fc2(x)) x = torch.sigmoid(self.out(x)) return xdef train_eval_pytorch_dnn(X_train, y_train, X_val, y_val, epochs=5, batch_size=64, lr=1e-3, device='cpu'): model = DNNModel(input_dim=X_train.shape[1]).to(device) optimizer = torch.optim.Adam(model.parameters(), lr=lr) criterion = nn.BCELoss() X_train_t = torch.tensor(X_train, dtype=torch.float32).to(device) y_train_t = torch.tensor(y_train, dtype=torch.float32).view(-1, 1).to(device) X_val_t = torch.tensor(X_val, dtype=torch.float32).to(device) dataset_size = len(X_train_t) n_batches = (dataset_size // batch_size) + 1 for epoch in range(epochs): indices = torch.randperm(dataset_size) X_train_t = X_train_t[indices] y_train_t = y_train_t[indices] for i in range(n_batches): start_idx = i * batch_size end_idx = start_idx + batch_size if start_idx >= dataset_size: break x_batch = X_train_t[start_idx:end_idx] y_batch = y_train_t[start_idx:end_idx] preds = model(x_batch) loss = criterion(preds, y_batch) optimizer.zero_grad() loss.backward() optimizer.step() with torch.no_grad(): val_preds = model(X_val_t).cpu().numpy().ravel() auc = roc_auc_score(y_val, val_preds) ks = calc_ks_score(y_val, val_preds) return model, auc, ks, val_preds# ---------------------------------------------# 4) Helper: Train & Evaluate Various Models# ---------------------------------------------def train_eval_model(model_name, X_train, y_train, X_val, y_val, device='cpu'): if model_name == 'xgb': model = XGBClassifier(use_label_encoder=False, eval_metric='logloss') model.fit(X_train, y_train) y_prob = model.predict_proba(X_val)[:, 1] auc = roc_auc_score(y_val, y_prob) ks = calc_ks_score(y_val, y_prob) return model, auc, ks, y_prob elif model_name == 'lgbm': model = LGBMClassifier() model.fit(X_train, y_train) y_prob = model.predict_proba(X_val)[:, 1] auc = roc_auc_score(y_val, y_prob) ks = calc_ks_score(y_val, y_prob) return model, auc, ks, y_prob elif model_name == 'rf': model = RandomForestClassifier() model.fit(X_train, y_train) y_prob = model.predict_proba(X_val)[:, 1] auc = roc_auc_score(y_val, y_prob) ks = calc_ks_score(y_val, y_prob) return model, auc, ks, y_prob elif model_name == 'dnn': model, auc, ks, y_prob = train_eval_pytorch_dnn( X_train.values, y_train.values, X_val.values, y_val.values, device=device ) return model, auc, ks, y_prob else: raise ValueError(f"Unknown model name: {model_name}")# Continue with the rest of the code unchanged...# ---------------------------------------------# 5) Weighted Blending# ---------------------------------------------def blend_predictions(probs_list, weights=None): if weights is None: weights = [1.0 / len(probs_list)] * len(probs_list) final_prob = np.zeros_like(probs_list[0]) for w, p in zip(weights, probs_list): final_prob += w * p return final_probdef evaluate_action(action, X_train, X_val, y_train, y_val, device='cpu'): """ action: int from 0..4 => (xgb=0, lgbm=1, rf=2, dnn=3, blend=4) Returns: reward = (auc + ks) - penalty auc, ks """ model_names = ['xgb', 'lgbm', 'rf', 'dnn'] if action < 4: chosen_model = model_names[action] _, auc_val, ks_val, _ = train_eval_model(chosen_model, X_train, y_train, X_val, y_val, device=device) penalty = 0.05 if chosen_model == 'dnn' else 0.0 reward = (auc_val + ks_val) - penalty return reward, auc_val, ks_val else: # Blend probs_list = [] for m in model_names: _, auc_m, ks_m, p = train_eval_model(m, X_train, y_train, X_val, y_val, device=device) probs_list.append(p) final_prob = blend_predictions(probs_list) auc_blend = roc_auc_score(y_val, final_prob) ks_blend = calc_ks_score(y_val, final_prob) reward = (auc_blend + ks_blend) - 0.1 return reward, auc_blend, ks_blend# ---------------------------------------------# 6) A Simple Multi-Armed Bandit Approach# ---------------------------------------------def multi_armed_bandit_model_selection( n_episodes=50, n_actions=5, epsilon=0.06, device='cpu'): """ We have 5 actions (xgb=0, lgbm=1, rf=2, dnn=3, blend=4). For each 'episode': 1) Generate a dataset (X,y) with the chosen seed 2) Split into train/val 3) Epsilon-greedy select an action 4) Evaluate the chosen action => get reward 5) Update average reward (Q) for that action """ Q = np.zeros(n_actions, dtype=np.float32) counts = np.zeros(n_actions, dtype=int) # For storing raw AUC, KS, Reward each time an action is chosen action_auc_records = [[] for _ in range(n_actions)] action_ks_records = [[] for _ in range(n_actions)] action_reward_records = [[] for _ in range(n_actions)] action_history = [] reward_history = [] for episode in range(n_episodes): # Generate the data here seed = 1000 + episode X = data.drop('label', axis=1) # Features y = data['label'] # Labels # Split the data X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.3, random_state=123) # Epsilon-greedy action selection if np.random.rand() < epsilon: action = np.random.randint(n_actions) else: action = np.argmax(Q) # Evaluate chosen action => get (reward, auc, ks) reward, auc_val, ks_val = evaluate_action( action, X_train, X_val, y_train, y_val, device=device ) # Update Q (incremental mean) counts[action] += 1 Q[action] += (reward - Q[action]) / counts[action] # Store details action_history.append(action) reward_history.append(reward) action_auc_records[action].append(auc_val) action_ks_records[action].append(ks_val) action_reward_records[action].append(reward) print(f"Episode {episode+1}/{n_episodes}, " f"Action={action}, Reward={reward:.4f}, Updated Q={Q}") return Q, action_history, reward_history, action_auc_records, action_ks_records, action_reward_records# ---------------------------------------------# 7) Run the Bandit, then Interpret Results# ---------------------------------------------def run_bandit(): device = 'cuda' if torch.cuda.is_available() else 'cpu' print(f"Using device={device}") n_episodes = 50 n_actions = 5 epsilon = 0.05 ( Q, actions, rewards, auc_records, ks_records, reward_records ) = multi_armed_bandit_model_selection( n_episodes=n_episodes, n_actions=n_actions, epsilon=epsilon, device=device ) best_action = np.argmax(Q) model_names = ["XGB", "LightGBM", "RandomForest", "DNN", "Blend"] print("
========================================") print("Interpreting Your Current Results") print("========================================
") print("Final Q-values:", Q) print(f"Best action index: {best_action}") print(f"Best action is: {model_names[best_action]} with estimated Q = {Q[best_action]:.4f}
") print("Detailed AUC/KS/Reward by action:") print("--------------------------------------------------") for a in range(n_actions): if len(auc_records[a]) > 0: avg_auc = np.mean(auc_records[a]) avg_ks = np.mean(ks_records[a]) avg_reward = np.mean(reward_records[a]) print(f"Action {a} ({model_names[a]}): chosen {len(auc_records[a])} times") print(f" Mean AUC = {avg_auc:.4f}, Mean KS = {avg_ks:.4f}, Mean Reward = {avg_reward:.4f}
") else: print(f"Action {a} ({model_names[a]}): chosen 0 times
")if __name__ == "__main__": run_bandit() ```

### Interpretation of Results

The final _Q-values_ indicate the estimated performance of each model in terms of cumulative rewards. The results from the experiment reveal:

* Best action: _XGBoost_ with an average reward of _1.267_.
* Comparison: _XGBoost_ significantly outperformed other models due to its balance of prediction accuracy and robustness.

The detailed results provide insight into the trade-offs between different models:

The results suggest that:

* _XGBoost_ dominates the selection because of its consistently high _AUC_ and _KS_ scores.
* _DNN_ shows potential, as indicated by its relatively high _AUC_ and _KS_ in the one episode it was selected.
* Blend and other models were not frequently chosen, suggesting further experimentation with weights and feature representations might be needed.

The dominance of _XGBoost_ highlights its suitability for this particular data structure and reward mechanism. Further research could include:

1. Exploring dynamic penalty adjustment for complex models.
2. Extending the bandit framework to handle time-varying rewards.
3. Optimizing model blending strategies using reinforcement learning itself.

It shows that the Multi-Armed Bandit Method can efficiently find the best model based on the given evaluation criteria.

Next, let’s dive into testing the Deep Q-Network (_DQN_) approach. This will help us see how well it handles changing states and long-term rewards, compared to the simpler, stateless Multi-Armed Bandit Method we tested earlier.

```python import numpy as npimport pandas as pdfrom sklearn.model_selection import train_test_splitfrom sklearn.metrics import roc_auc_scorefrom sklearn.ensemble import RandomForestClassifierfrom xgboost import XGBClassifierfrom lightgbm import LGBMClassifierimport torchimport torch.nn as nnimport torch.nn.functional as F# Gymnasiumimport gymnasium as gymfrom gymnasium import spaces# Stable Baselines3from stable_baselines3 import DQNfrom stable_baselines3.common.vec_env import DummyVecEnv# For callbackfrom stable_baselines3.common.callbacks import BaseCallback# ---------------------------------------------# 1) Read data from CSV file# ---------------------------------------------data = pd.read_csv('rein_data_binary.csv')X = data.drop('label', axis=1) # Featuresy = data['label'] # Labels# ---------------------------------------------# 2) Metrics (AUC, KS)# ---------------------------------------------def calc_ks_score(y_true, y_prob): data = pd.DataFrame({'y_true': y_true, 'y_prob': y_prob}).sort_values('y_prob', ascending=False) data['cum_pos'] = (data['y_true'] == 1).cumsum() data['cum_neg'] = (data['y_true'] == 0).cumsum() total_pos = data['y_true'].sum() total_neg = (data['y_true'] == 0).sum() data['cum_pos_rate'] = data['cum_pos'] / total_pos data['cum_neg_rate'] = data['cum_neg'] / total_neg data['ks'] = data['cum_pos_rate'] - data['cum_neg_rate'] return data['ks'].max()# ---------------------------------------------# 3) PyTorch DNN# ---------------------------------------------class DNNModel(nn.Module): def __init__(self, input_dim=5): super(DNNModel, self).__init__() self.fc1 = nn.Linear(input_dim, 16) self.fc2 = nn.Linear(16, 8) self.out = nn.Linear(8, 1) def forward(self, x): x = F.relu(self.fc1(x)) x = F.relu(self.fc2(x)) x = torch.sigmoid(self.out(x)) return xdef train_eval_pytorch_dnn(X_train, y_train, X_val, y_val, epochs=5, batch_size=64, lr=1e-3, device='cpu'): model = DNNModel(input_dim=X_train.shape[1]).to(device) optimizer = torch.optim.Adam(model.parameters(), lr=lr) criterion = nn.BCELoss() X_train_t = torch.tensor(X_train, dtype=torch.float32).to(device) y_train_t = torch.tensor(y_train, dtype=torch.float32).view(-1, 1).to(device) X_val_t = torch.tensor(X_val, dtype=torch.float32).to(device) dataset_size = len(X_train_t) n_batches = (dataset_size // batch_size) + 1 for epoch in range(epochs): indices = torch.randperm(dataset_size) X_train_t = X_train_t[indices] y_train_t = y_train_t[indices] for i in range(n_batches): start_idx = i * batch_size end_idx = start_idx + batch_size if start_idx >= dataset_size: break x_batch = X_train_t[start_idx:end_idx] y_batch = y_train_t[start_idx:end_idx] preds = model(x_batch) loss = criterion(preds, y_batch) optimizer.zero_grad() loss.backward() optimizer.step() with torch.no_grad(): val_preds = model(X_val_t).cpu().numpy().ravel() auc = roc_auc_score(y_val, val_preds) ks = calc_ks_score(y_val, val_preds) return model, auc, ks, val_preds# ---------------------------------------------# 4) Train & Evaluate Helper# ---------------------------------------------def train_eval_model(model_name, X_train, y_train, X_val, y_val, device='cpu'): if model_name == 'xgb': model = XGBClassifier(use_label_encoder=False, eval_metric='logloss') model.fit(X_train, y_train) y_prob = model.predict_proba(X_val)[:, 1] auc = roc_auc_score(y_val, y_prob) ks = calc_ks_score(y_val, y_prob) return model, auc, ks, y_prob elif model_name == 'lgbm': model = LGBMClassifier() model.fit(X_train, y_train) y_prob = model.predict_proba(X_val)[:, 1] auc = roc_auc_score(y_val, y_prob) ks = calc_ks_score(y_val, y_prob) return model, auc, ks, y_prob elif model_name == 'rf': model = RandomForestClassifier() model.fit(X_train, y_train) y_prob = model.predict_proba(X_val)[:, 1] auc = roc_auc_score(y_val, y_prob) ks = calc_ks_score(y_val, y_prob) return model, auc, ks, y_prob elif model_name == 'dnn': model, auc, ks, y_prob = train_eval_pytorch_dnn( X_train.values, y_train.values, X_val.values, y_val.values, device=device ) return model, auc, ks, y_prob else: raise ValueError(f"Unknown model name: {model_name}")def blend_predictions(probs_list, weights=None): if weights is None: weights = [1.0 / len(probs_list)] * len(probs_list) final_prob = np.zeros_like(probs_list[0]) for w, p in zip(weights, probs_list): final_prob += w * p return final_prob# ---------------------------------------------# 5) Single-step Environment# ---------------------------------------------class ModelSelectionEnv(gym.Env): metadata = {"render_modes": ["human"]} def __init__(self, X, y, device='cpu'): super().__init__() self.device = device # Train/val split self.X_train, self.X_val, self.y_train, self.y_val = train_test_split( X, y, test_size=0.3, random_state=123 ) means = X.mean().values vars_ = X.var().values self.state = np.concatenate([means, vars_]) # observation # 5 discrete actions self.action_space = spaces.Discrete(5) self.observation_space = spaces.Box( low=-np.inf, high=np.inf, shape=(len(self.state),), dtype=np.float32 ) self.terminated = False def reset(self, seed=None, options=None): super().reset(seed=seed) self.terminated = False return self.state.astype(np.float32), {} def step(self, action): if self.terminated: return self.state.astype(np.float32), 0.0, True, False, {} model_names = ['xgb', 'lgbm', 'rf', 'dnn'] if action < 4: chosen_model = model_names[action] _, auc_v, ks_v, _ = train_eval_model( chosen_model, self.X_train, self.y_train, self.X_val, self.y_val, device=self.device ) penalty = 0.05 if chosen_model == 'dnn' else 0.0 reward = (auc_v + ks_v) - penalty info = { "action_name": chosen_model, "AUC": auc_v, "KS": ks_v, "Penalty": penalty } else: # Blend probs_list = [] for m in model_names: _, auc_m, ks_m, prob_m = train_eval_model( m, self.X_train, self.y_train, self.X_val, self.y_val, device=self.device ) probs_list.append(prob_m) final_prob = blend_predictions(probs_list) auc_v = roc_auc_score(self.y_val, final_prob) ks_v = calc_ks_score(self.y_val, final_prob) penalty = 0.1 reward = (auc_v + ks_v) - penalty info = { "action_name": "blend", "AUC": auc_v, "KS": ks_v, "Penalty": penalty } self.terminated = True return self.state.astype(np.float32), reward, True, False, info# ---------------------------------------------# 7) RL Training & Execution# ---------------------------------------------def run_rl_model_selection_pytorch(): device = 'cuda' if torch.cuda.is_available() else 'cpu' print(f"Using {device} device") # Create single-step Gymnasium environment env = ModelSelectionEnv(X, y, device=device) # Wrap with DummyVecEnv def make_env(): return env vec_env = DummyVecEnv([make_env]) # Create callback callback = BanditSummaryCallback() # Create DQN model = DQN( "MlpPolicy", vec_env, verbose=1, learning_rate=1e-3, buffer_size=10000, exploration_fraction=0.3, exploration_final_eps=0.02, tensorboard_log="./rl_tensorboard/" ) # Train with callback model.learn(total_timesteps=2000, callback=callback) # Evaluate final policy (one step) obs = vec_env.reset() action, _ = model.predict(obs, deterministic=True) obs, rewards, dones, infos = vec_env.step(action) final_reward = rewards[0] action_map = ["XGB", "LightGBM", "RandomForest", "DNN", "Blend"] print("
======================================") print(f"Final chosen action => {action[0]} ({action_map[action[0]]})") print(f"Final step reward => (AUC + KS - penalty) = {final_reward:.4f}") print("======================================
")if __name__ == "__main__": run_rl_model_selection_pytorch() ```

### Results and Interpretation

**Training Summary:**

* _2000_ episodes were run with exploration and exploitation driven by the epsilon-greedy policy.
* _Q-values_ reflect the estimated cumulative rewards for each model selection.

**Final Q-values:**

_[1.1442,1.1800,1.0847,1.0510,1.0684]_

**Best action** : _LightGBM_ with the highest _Q-value_ _1.1800_.

**Detailed performance:**

Press enter or click to view image in full size

**Final chosen action:**
_LightGBM_ (action index 1) consistently outperformed others on _AUC, KS_ , and reward. Given the data structure and evaluation metrics, its selection demonstrates robustness and reliability.

## Summary of Deepseeker Techniques for Reinforcement Learning in Adaptive Model Selection

I wrote this paper by drawing inspiration from Deepseeker Techniques to improve adaptive model selection:

**Reinforcement Learning without Supervised Fine-Tuning:** Deepseeker skips the need for large labeled datasets by using reinforcement learning (_RL_) to develop reasoning through trial-and-error.

I apply the RL agent dynamically learns the best model selection policy through exploration and feedback, without fine-tuning. Over time, it generalizes across new datasets or domains without retraining models, mimicking Deepseeker’s meta-learning. Example: The agent may learn to use XGBoost for structured data and _DNN_ for non-linear data, automatically adapting to changing conditions.

**Data-Driven Model Selection and Classification:** Deepseeker activates only the relevant model components based on the data context, making the process efficient and targeted. Similarly, the _RL_ agent uses dataset statistics (mean, variance, etc.) to classify data regions and match them with the best models.

For example, for structured regions, the agent may choose _XGBoost_ , while noisy, non-linear regions could trigger blended _DNN_ and _LGBM_ models. This dynamic mapping of states to actions prevents applying a single model globally and improves prediction accuracy.

**Partial Parameter Activation (Sparse Model Execution):** Instead of activating all parameters, Deepseeker selectively activates only those needed for the current task.

The same concept applies to dynamic model blending, activating only the most effective models or configurations based on the current state. Example: In a medical dataset, _XGBoost_ could be used for structured patient history, while _DNN_ handles complex genetic data, minimizing unnecessary computation and boosting efficiency.

**Chain-of-thought (CoT):** DeepSeek-R1-Zero uses chain-of-thought (CoT) reasoning to solve complex tasks by generating self-verifying and reflective chains of reasoning steps.

In this paper, the RL agent could potentially use CoT for adaptive model selection (not applied yet, but it’s a research direction worth exploring):

It starts with basic models like _XGBoost_ or _LightGBM_ , then switches or blends with complex models like _DNN_ if needed. After each action, it verifies performance (_AUC, KS_). If rewards are low, it reflects, adjusts blending, or picks a new model. With rolling feedback, it remembers past decisions to avoid repeating mistakes and explores blending ratios dynamically for continuous improvement.

## Final Thoughts

I have explored how reinforcement learning (_RL_) can power adaptive model selection and blending by treating it as a Markov Decision Process (_MDP_). The _RL_ agent intelligently navigates choices like _XGBoost_ , _LightGBM, DNN_ , or model blending, dynamically adapting to shifting data distributions. Using cumulative performance rewards (based on _AUC_ and _KS_) and penalizing inefficient choices, we can optimize the modeling process without relying on fixed assumptions.

I’m inspired by the reinforcement learning mechanism in Deepseeker NN (LLM), which adds domain-specific knowledge. This could help generalize across various tasks like automated trading, healthcare diagnostics, and predictive maintenance.

Challenges, such as computational overhead and exploration-exploitation balance, remain. However, future meta-learning and semi-supervised labeling could improve adaptability while reducing costs. Expanding to _RL_ -based hyperparameter tuning could make the system fully autonomous, choosing the optimal model and its configurations.

Finally, this paper sets the stage for next-generation AutoML systems, where reinforcement learning and large language models collaborate for smarter, scalable solutions in real-world applications.

The data and code can be accessed at <https://github.com/datalev001/RL_supLR/>.

## About me

With over 20 years of experience in software and database management and 25 years teaching IT, math, and statistics, I am a Data Scientist with extensive expertise across multiple industries.

You can connect with me at:

Email: datalev@gmail.com | [LinkedIn](<https://www.linkedin.com/in/kelvin-li-5599691b/>) | [X/Twitter](<https://x.com/datalev00156330>)
