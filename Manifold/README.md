# Manifold Geometry for Generative AI

## Overview
This book builds intuition-first foundations for manifolds and geodesics, then develops Riemannian and information geometry tools that directly support modern generative AI (VAEs, GANs, diffusion, flows). You’ll learn how metrics, geodesics, curvature, Fisher information, natural gradients, and Bregman divergences unify geometry and training dynamics.

- Release PDF: see `release/` (use `make release`)
- Build locally: `make pdf` (outputs to `release/Manifold.pdf`)

## Target Audience
- ML/AI practitioners and researchers seeking geometric foundations for model design and training
- Students with basic math background wanting a concise path from manifolds to practical AI
- Readers who prefer visual intuition with clean, minimal formalism

## Prerequisites
- Linear algebra: vectors, matrices, eigenvalues/eigenvectors, PSD matrices
- Multivariable calculus: gradients, Jacobians, Hessians, Taylor expansion, arc length
- Light ODEs: initial value problems (for geodesic and transport ODEs)
- Probability/statistics: expectations, log-likelihood, score; Gaussian/Bernoulli
- Information theory: KL divergence (basics)
- Optimization: gradient descent, conditioning/preconditioning (natural gradient is introduced in-book)

No prior differential geometry required. Full geometric treatment is given in Chapter 9; information geometry in Chapter 10.

## Table of Contents (with brief notes and sources)
- Chapter 1: What is a Manifold? — Local flatness via charts; intuition and examples. (`chapters/01-What-is-a-Manifold.tex`)
- Chapter 2: 1D Manifold Examples — Lines and circles; arc length and basic geodesics. (`chapters/02-1D-Manifold-Examples.tex`)
- Chapter 3: 2D Manifold Examples — Planes, spheres, tori; local vs global geometry. (`chapters/03-2D-Manifold-Examples.tex`)
- Chapter 4: Why Not a Cone? — Counterexample clarifying manifold definition. (`chapters/04-Why-Not-a-Cone.tex`)
- Chapter 5: Geodesics Introduction — Shortest paths; variational view and intuition. (`chapters/05-Geodesics-Introduction.tex`)
- Chapter 6: Geodesics 1D–2D–Sphere — Worked geodesic equations and methods. (`chapters/06-Geodesics-1D-2D-Sphere.tex`)
- Chapter 7: Distance on Sphere — Practical formulas (e.g., haversine), edge cases. (`chapters/07-Distance-on-Sphere.tex`)
- Chapter 8: Open n-Ball — Local neighborhoods that define manifold structure. (`chapters/08-Open-n-Ball.tex`)
- Chapter 9: Riemannian Manifold — Tangent spaces, metric tensor, Levi-Civita, parallel transport, curvature; exp/log maps, geodesic deviation. (`chapters/09-Riemannian-Manifold.tex`)
- Chapter 10: Manifolds in Generative AI — Statistical/parameter manifolds, Fisher, natural gradient, Bregman, and links to VAEs/GANs/diffusion. (`chapters/10-Manifolds-in-Generative-AI.tex`)

## Build and Release
- Build: `make pdf` → `release/Manifold.pdf`
- Release: `make release` → `release/Manifold-Generative-AI.pdf`
- Clean: `make clean` (preserves `release/Manifold-Generative-AI.pdf`)

## Contact
- See `backmatter/contact.tex` for author contact.

## License
- Creative Commons Attribution 4.0 International (CC BY 4.0). See `backmatter/license.tex`.

## Conclusion
Geometry provides principled tools for understanding and training generative models. By unifying manifolds, metrics, and divergences with optimization, this book offers a compact path from intuition to practical, geometry-aware AI.


