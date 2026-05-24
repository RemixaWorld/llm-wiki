---
domain: github.com
fetch_date: '2026-05-18T12:35:48.584851'
status: ok
url: https://github.com/stanfordnlp/pyreft/blob/main/pyreft/interventions.py
---

-
Notifications
You must be signed in to change notification settings - Fork 134

## Expand file tree

/

Copy path# interventions.py

More file actions

219 lines (191 loc) · 8.26 KB

/

# interventions.py

## File metadata and controls

219 lines (191 loc) · 8.26 KB

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

24

25

26

27

28

29

30

31

32

33

34

35

36

37

38

39

40

41

42

43

44

45

46

47

48

49

50

51

52

53

54

55

56

57

58

59

60

61

62

63

64

65

66

67

68

69

70

71

72

73

74

75

76

77

78

79

80

81

82

83

84

85

86

87

88

89

90

91

92

93

94

95

96

97

98

99

100

101

102

103

104

105

106

107

108

109

110

111

112

113

114

115

116

117

118

119

120

121

122

123

124

125

126

127

128

129

130

131

132

133

134

135

136

137

138

139

140

141

142

143

144

145

146

147

148

149

150

151

152

153

154

155

156

157

158

159

160

161

162

163

164

165

166

167

168

169

170

171

172

173

174

175

176

177

178

179

180

181

182

183

184

185

186

187

188

189

190

191

192

193

194

195

196

197

198

199

200

201

202

203

204

205

206

207

208

209

210

211

212

213

214

215

216

217

218

import torch

from collections import OrderedDict

from pyvene import (

ConstantSourceIntervention,

SourcelessIntervention,

TrainableIntervention,

DistributedRepresentationIntervention,

)

from transformers.activations import ACT2FN

class LowRankRotateLayer(torch.nn.Module):

"""A linear transformation with orthogonal initialization."""

def __init__(self, n, m, init_orth=True):

super().__init__()

# n > m

self.weight = torch.nn.Parameter(torch.empty(n, m), requires_grad=True)

if init_orth:

torch.nn.init.orthogonal_(self.weight)

def forward(self, x):

return torch.matmul(x.to(self.weight.dtype), self.weight)

class LoreftIntervention(

SourcelessIntervention,

TrainableIntervention,

DistributedRepresentationIntervention

):

"""

LoReFT(h) = h + R^T(Wh + b − Rh)

"""

def __init__(self, **kwargs):

super().__init__(**kwargs, keep_last_dim=True)

rotate_layer = LowRankRotateLayer(

self.embed_dim, kwargs["low_rank_dimension"], init_orth=True)

self.rotate_layer = torch.nn.utils.parametrizations.orthogonal(rotate_layer)

self.learned_source = torch.nn.Linear(

self.embed_dim, kwargs["low_rank_dimension"]).to(

kwargs["dtype"] if "dtype" in kwargs else torch.bfloat16)

self.dropout = torch.nn.Dropout(kwargs["dropout"] if "dropout" in kwargs else 0.0)

self.act_fn = ACT2FN["linear"] if "act_fn" not in kwargs or kwargs["act_fn"] is None else ACT2FN[kwargs["act_fn"]]

def forward(

self, base, source=None, subspaces=None

):

rotated_base = self.rotate_layer(base)

output = base + torch.matmul(

(self.act_fn(self.learned_source(base)) - rotated_base), self.rotate_layer.weight.T

)

return self.dropout(output.to(base.dtype))

def state_dict(self, *args, **kwargs):

"""

Overwrite for data-efficiency.

"""

state_dict = OrderedDict()

for k, v in self.learned_source.state_dict().items():

state_dict[k] = v

state_dict["rotate_layer"] = self.rotate_layer.weight.data

return state_dict

def load_state_dict(self, state_dict, *args, **kwargs):

"""

Overwrite for data-efficiency.

"""

self.learned_source.load_state_dict(state_dict, strict=False)

# Caveat: without creating a new layer, it might not work (still not sure why)

# We have to recreate a layer, and load back the columns.

overload_w = state_dict["rotate_layer"].to(

self.learned_source.weight.device)

overload_w_width = overload_w.shape[-1]

rotate_layer = LowRankRotateLayer(

self.embed_dim, overload_w_width, init_orth=True).to(

self.learned_source.weight.device)

self.rotate_layer = torch.nn.utils.parametrizations.orthogonal(rotate_layer)

self.rotate_layer.parametrizations.weight[0].base[:,:overload_w_width] = overload_w

assert torch.allclose(self.rotate_layer.weight.data, overload_w.data) == True # we must match!

return

class NoreftIntervention(

SourcelessIntervention,

TrainableIntervention,

DistributedRepresentationIntervention

):

"""

NoReFT(h) = h + W2^T(W1h + b − W2h)

"""

def __init__(self, **kwargs):

super().__init__(**kwargs, keep_last_dim=True)

self.proj_layer = torch.nn.Linear(

self.embed_dim, kwargs["low_rank_dimension"], bias=kwargs["add_bias"]).to(

kwargs["dtype"] if "dtype" in kwargs else torch.bfloat16)

self.learned_source = torch.nn.Linear(

self.embed_dim, kwargs["low_rank_dimension"]).to(

kwargs["dtype"] if "dtype" in kwargs else torch.bfloat16)

self.dropout = torch.nn.Dropout(kwargs["dropout"] if "dropout" in kwargs else 0.0)

self.act_fn = ACT2FN["linear"] if "act_fn" not in kwargs or kwargs["act_fn"] is None else ACT2FN[kwargs["act_fn"]]

def forward(

self, base, source=None, subspaces=None

):

proj_base = self.proj_layer(base)

output = base + torch.matmul(

(self.act_fn(self.learned_source(base)) - proj_base), self.proj_layer.weight

)

return self.dropout(output.to(base.dtype))

class ConsreftIntervention(

SourcelessIntervention,

TrainableIntervention,

DistributedRepresentationIntervention

):

"""

ConsReFT(h) = h + R^T(b − Rh)

"""

def __init__(self, **kwargs):

super().__init__(**kwargs, keep_last_dim=True)

rotate_layer = LowRankRotateLayer(self.embed_dim, kwargs["low_rank_dimension"], init_orth=True)

self.rotate_layer = torch.nn.utils.parametrizations.orthogonal(rotate_layer)

self.learned_source = torch.nn.Parameter(

torch.rand(kwargs["low_rank_dimension"]), requires_grad=True)

def forward(

self, base, source=None, subspaces=None

):

rotated_base = self.rotate_layer(base)

output = base + torch.matmul(

(self.learned_source - rotated_base), self.rotate_layer.weight.T

)

return output.to(base.dtype)

class LobireftIntervention(

SourcelessIntervention,

TrainableIntervention,

DistributedRepresentationIntervention

):

"""

LobiReFT(h) = h + R^T(b)

"""

def __init__(self, **kwargs):

super().__init__(**kwargs, keep_last_dim=True)

rotate_layer = LowRankRotateLayer(self.embed_dim, kwargs["low_rank_dimension"], init_orth=True)

self.rotate_layer = torch.nn.utils.parametrizations.orthogonal(rotate_layer)

self.learned_source = torch.nn.Parameter(

torch.rand(kwargs["low_rank_dimension"]), requires_grad=True)

self.dropout = torch.nn.Dropout(kwargs["dropout"] if "dropout" in kwargs else 0.0)

def forward(

self, base, source=None, subspaces=None

):

output = base + torch.matmul(

self.learned_source, self.rotate_layer.weight.T

)

return self.dropout(output.to(base.dtype))

class DireftIntervention(

SourcelessIntervention,

TrainableIntervention,

DistributedRepresentationIntervention

):

"""

DiReFT(h) = h + R^T(Wh + b)

"""

def __init__(self, **kwargs):

super().__init__(**kwargs, keep_last_dim=True)

rotate_layer = LowRankRotateLayer(self.embed_dim, kwargs["low_rank_dimension"], init_orth=True)

self.rotate_layer = torch.nn.utils.parametrizations.orthogonal(rotate_layer)

self.learned_source = torch.nn.Linear(

self.embed_dim, kwargs["low_rank_dimension"]).to(

kwargs["dtype"] if "dtype" in kwargs else torch.bfloat16)

self.dropout = torch.nn.Dropout(kwargs["dropout"] if "dropout" in kwargs else 0.0)

self.act_fn = ACT2FN["linear"] if "act_fn" not in kwargs or kwargs["act_fn"] is None else ACT2FN[kwargs["act_fn"]]

def forward(

self, base, source=None, subspaces=None

):

cast_base = base.to(self.learned_source.weight.dtype)

output = base + torch.matmul(

(self.act_fn(self.learned_source(cast_base))).to(self.rotate_layer.weight.dtype), self.rotate_layer.weight.T

)

return self.dropout(output.to(base.dtype))

class NodireftIntervention(

SourcelessIntervention,

TrainableIntervention,

DistributedRepresentationIntervention

):

"""

NodiReFT(h) = h + W2^T(W1h + b)

"""

def __init__(self, **kwargs):

super().__init__(**kwargs, keep_last_dim=True)

self.proj_layer = torch.nn.Linear(

self.embed_dim, kwargs["low_rank_dimension"], bias=kwargs["add_bias"]).to(

kwargs["dtype"] if "dtype" in kwargs else torch.bfloat16)

self.learned_source = torch.nn.Linear(

self.embed_dim, kwargs["low_rank_dimension"]).to(

kwargs["dtype"] if "dtype" in kwargs else torch.bfloat16)

self.dropout = torch.nn.Dropout(kwargs["dropout"] if "dropout" in kwargs else 0.0)

self.act_fn = ACT2FN["linear"] if "act_fn" not in kwargs or kwargs["act_fn"] is None else ACT2FN[kwargs["act_fn"]]

def forward(

self, base, source=None, subspaces=None

):

output = base + torch.matmul(

self.act_fn(self.learned_source(base)), self.proj_layer.weight

)

return self.dropout(output.to(base.dtype))
