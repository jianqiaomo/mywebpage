---
layout: post
title: HAAC - A Hardware-Software Co-Design to Accelerate Garbled Circuits
date: Mar-28-2023
author: Jianqiao Mo
tags: [Paper]
comments: true
toc: false
pinned: false
---
_2023 ISCA Paper_

**Accepted to**:
[2023 International Symposium on Computer Architecture (ISCA)](https://www.iscaconf.org/isca2023/program/) 

**Date of Conference**: June 19, 2023

**Authors**: Jianqiao Mo*, Jayanth Gopinath, Brandon Reagen

**Abstract**:
Privacy and security have rapidly emerged as priorities in system design. One powerful solution for providing both is privacy-preserving computation, where functions are computed directly on encrypted data and control can be provided over how data is used. Garbled circuits (GCs) are a PPC technology that provide both confidential computing and control over how data is used. The challenge is that they incur significant performance overheads compared to plaintext. This paper proposes a novel garbled circuits accelerator and compiler, named HAAC, to mitigate performance overheads and make privacy-preserving computation more practical. HAAC is a hardware-software co-design. GCs are exemplars of co-design as programs are completely known at compile time, i.e., all dependence, memory accesses, and control flow are fixed. The design philosophy of HAAC is to keep hardware simple and efficient, maximizing area devoted to our proposed custom execution units and other circuits essential for high performance (e.g., on-chip storage). The compiler can leverage its program understanding to realize hardware's performance potential by generating effective instruction schedules, data layouts, and orchestrating off-chip events. In taking this approach we can achieve ASIC performance/efficiency without sacrificing generality. Insights of our approach include how co-design enables expressing arbitrary GCs programs as streams, which simplifies hardware and enables complete memory-compute decoupling, and the development of a scratchpad that captures data reuse by tracking program execution, eliminating the need for costly hardware managed caches and tagging logic. We evaluate HAAC with VIP-Bench and achieve an average speedup of 589× with DDR4 (2,627× with HBM2) in 4.3mm<sup>2</sup> of area.

**Paper Link**: [https://dl.acm.org/doi/abs/10.1145/3579371.3589045](https://dl.acm.org/doi/abs/10.1145/3579371.3589045) or [arxiv](https://arxiv.org/abs/2211.13324).

**Our ISCA 2023 Lightning Talks**:
<iframe width="560" height="315" src="https://www.youtube.com/embed/ZIQovAHcN2w" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
