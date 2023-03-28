---
layout: post
title: HAAC: A Hardware-Software Co-Design to Accelerate Garbled Circuits
date: 2023-03-28
author: Jianqiao Mo
tags: [Conference Paper]
comments: true
toc: true
pinned: false
---
Link: [https://arxiv.org/abs/2211.13324](https://arxiv.org/abs/2211.13324)

**Authors:** Jianqiao Mo, Jayanth Gopinath, Brandon Reagen

**Abstract:**
Privacy and security have rapidly emerged as priorities in system design. 
One powerful solution for providing both is privacy-preserving computation, where functions are computed directly on encrypted data and control can be provided over how data is used. 
Garbled circuits (GCs) are a PPC technology that provide both confidential computing and control over how data is used. 
The challenge is that they incur significant performance overheads compared to plaintext. 
This paper proposes a novel garbled circuit accelerator and compiler, named HAAC, to mitigate performance overheads and make privacy-preserving computation more practical. 
HAAC is a hardware-software co-design. 
GCs are exemplars of co-design as programs are completely known at compile time, i.e., all dependence, memory accesses, and control flow are fixed. 
The design philosophy of HAAC is to keep hardware simple and efficient, maximizing area devoted to our proposed custom execution units and other circuits essential for high performance (e.g., on-chip storage). 
The compiler can leverage its program understanding to realize hardware's performance potential by generating effective instruction schedules, data layouts, and orchestrating off-chip events. 
In taking this approach we can achieve ASIC performance/efficiency without sacrificing generality. 
Insights of our approach include how co-design enables expressing arbitrary GC programs as streams, which simplifies hardware and enables complete memory-compute decoupling, and the development of a scratchpad that captures data reuse by tracking program execution, eliminating the need for costly hardware managed caches and tagging logic. 
We evaluate HAAC with VIP-Bench and achieve a speedup of 608× in 4.3mm<sup>2</sup> of area.

    

**Accepted in:** 
[2023 Proceedings of the 50th Annual International Symposium on Computer Architecture (ISCA)](https://www.iscaconf.org/isca2023/program/) 


**Date of Conference:** June 17–21, 2023