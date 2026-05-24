# Flash Attention and Fused LayerNorm

Flash Attention is an IO-aware exact attention algorithm that reduces memory reads/writes between GPU HBM and SRAM by using tiling. It achieves 2-4x wall-clock speedup on common model sizes. Flash Attention 2 further reduces non-matmul FLOPs and optimizes work partitioning across GPU thread blocks.

Fused LayerNorm is a technique that fuses layer normalization operations into a single GPU kernel, reducing memory round-trips. It is commonly used alongside Flash Attention in transformer training pipelines to maximize GPU utilization.
