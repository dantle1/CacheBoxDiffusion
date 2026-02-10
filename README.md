# Learning Architectural Cache Simulator Behavior with Diffusion Models

Applications have memory access patterns with complex spatial and temporal relationships. Architectural simulators that evaluate these applications are highly sequential in nature, particularly for stateful components like caches. The memory access traces from these simulators can be represented as two-dimensional heatmap images. The behavior of a cache can be used as a filter on these heatmap images which can be learned with deep learning methods. We introduce a framework that employs a diffusion model to learn and replicate the filtering behavior of caches using memory access heatmaps. The model is trained on a large collection of memory access heatmaps to reconstruct new heatmaps and can generalize to new workloads and cache configurations. In addition, the framework utilizes preprocessing to normalize access intensities and augment training data to improve robustness. We evaluate the performance of the model on multiple different benchmarks to assess its ability to generalize across a diverse range of memory access traces.




[Master's Defense Presentation](https://docs.google.com/presentation/d/1xrbwvei8k1RAARulsScMPgVmGbp7Ew0N4S1a6-yEwNg/edit?slide=id.g4702670f3a_2_74#slide=id.g4702670f3a_2_74)
