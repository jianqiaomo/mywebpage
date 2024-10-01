---
layout: post
title: Towards Fast and Scalable Private Inference
date: 2023-07-30
author: Jianqiao Mo
tags: [Paper]
comments: true
toc: false
pinned: false
---
_2023 CF Paper_

**Appear in**:
[2023 ACM International Conference on Computing Frontiers (CF)](https://www.computingfrontiers.org/2023/) 

**Authors**: Jianqiao Mo, Karthik Garimella, Negar Neda, Austin Ebel, Brandon Reagen

**Abstract**:
Privacy and security have rapidly emerged as first order design constraints. Users now demand more protection over who can see their data (confidentiality) as well as how it is used (control). Here, existing cryptographic techniques for security fall short: they secure data when stored or communicated but must decrypt it for computation. Fortunately, a new paradigm of computing exists, which we refer to as privacy-preserving computation (PPC). Emerging PPC technologies can be leveraged for secure outsourced computation or to enable two parties to compute without revealing either users' secret data. Despite their phenomenal potential to revolutionize user protection in the digital age, the realization has been limited due to exorbitant computational, communication, and storage overheads.

This paper reviews recent efforts on addressing various PPC overheads using private inference (PI) in neural network as a motivating application. First, the problem and various technologies, including homomorphic encryption (HE), secret sharing (SS), garbled circuits (GCs), and oblivious transfer (OT), are introduced. Next, a characterization of their overheads when used to implement PI is covered. The characterization motivates the need for both GCs and HE accelerators. Then two solutions are presented: HAAC for accelerating GCs and RPU for accelerating HE. To conclude, results and effects are shown with a discussion on what future work is needed to overcome the remaining overheads of PI.

***

<div style="text-align: center;">
[<a href="https://dl.acm.org/doi/abs/10.1145/3587135.3592169">paper</a>]
</div>

***