#!/usr/bin/env node

const fs = require('node:fs/promises');
const path = require('node:path');
const { PNG } = require('pngjs');

const DEFAULT_WIDTH = 1280;
const DEFAULT_HEIGHT = 720;

const IFS_PRESETS = {
  fern: {
    label: 'Fern',
    matrices: [
      { a: 0, b: 0, c: 0, d: 0.16, e: 0, f: 0, p: 0.01 },
      { a: 0.85, b: 0.04, c: -0.04, d: 0.85, e: 0, f: 1.6, p: 0.85 },
      { a: 0.2, b: -0.26, c: 0.23, d: 0.22, e: 0, f: 1.6, p: 0.07 },
      { a: -0.15, b: 0.28, c: 0.26, d: 0.24, e: 0, f: 0.44, p: 0.07 },
    ],
    defaults: { iterations: 120000, density: 65, pointSize: 1 },
  },
  ifsTree: {
    label: 'IFS Tree',
    matrices: [
      { a: 0.05, b: 0, c: 0, d: 0.6, e: 0, f: 0, p: 0.2 },
      { a: 0.05, b: 0, c: 0, d: -0.5, e: 0, f: 1, p: 0.1 },
      { a: 0.46, b: -0.32, c: 0.39, d: 0.38, e: 0, f: 0.6, p: 0.4 },
      { a: 0.47, b: -0.15, c: 0.17, d: 0.42, e: 0, f: 1.1, p: 0.3 },
    ],
    defaults: { iterations: 120000, density: 72, pointSize: 1 },
  },
  weed: {
    label: 'Weed',
    matrices: [
      { a: 0.14, b: 0.01, c: 0, d: 0.51, e: -0.08, f: -1.31, p: 0.1 },
      { a: 0.43, b: 0.52, c: -0.45, d: 0.5, e: 1.49, f: -0.75, p: 0.35 },
      { a: 0.45, b: -0.49, c: 0.47, d: 0.47, e: -1.62, f: -0.74, p: 0.35 },
      { a: 0.49, b: 0, c: 0, d: 0.51, e: 0.02, f: 1.62, p: 0.2 },
    ],
    defaults: { iterations: 125000, density: 58, pointSize: 1 },
  },
  mapleLeaf: {
    label: 'Maple Leaf',
    matrices: [
      { a: 0.14, b: 0.01, c: 0, d: 0.51, e: -0.08, f: -1.31, p: 0.1 },
      { a: 0.43, b: 0.52, c: -0.45, d: 0.5, e: 1.49, f: -0.75, p: 0.35 },
      { a: 0.45, b: -0.49, c: 0.47, d: 0.47, e: -1.62, f: -0.74, p: 0.35 },
      { a: 0.49, b: 0, c: 0, d: 0.51, e: 0.02, f: 1.62, p: 0.2 },
    ],
    defaults: { iterations: 125000, density: 64, pointSize: 1 },
  },
  spiral: {
    label: 'Spiral',
    matrices: [
      { a: 0.787879, b: -0.424242, c: 0.242424, d: 0.859848, e: 1.758647, f: 1.408065, p: 0.9 },
      { a: -0.121212, b: 0.257576, c: 0.151515, d: 0.05303, e: -6.721654, f: 1.377236, p: 0.05 },
      { a: 0.181818, b: -0.136364, c: 0.090909, d: 0.181818, e: 6.086107, f: 1.568035, p: 0.05 },
    ],
    defaults: { iterations: 150000, density: 55, pointSize: 1 },
  },
  ifsPythagorasTree: {
    label: 'IFS Pythagoras Tree',
    matrices: [
      { a: 0.6, b: 0, c: 0, d: 0.6, e: 0, f: 0, p: 0.5 },
      { a: 0.5, b: -0.5, c: 0.5, d: 0.5, e: 0.6, f: 0.6, p: 0.25 },
      { a: 0.5, b: 0.5, c: -0.5, d: 0.5, e: 0.1, f: 0.6, p: 0.25 },
    ],
    defaults: { iterations: 100000, density: 130, pointSize: 1 },
  },
  radial1: {
    label: 'Radial 1',
    equation: 'radial',
    matrices: [
      { a: 0.6, b: 0.6, t: 0.4, e: 0, f: 0, p: 0.34 },
      { a: 0.6, b: 0.6, t: 2.4, e: 1.2, f: 0.1, p: 0.33 },
      { a: 0.6, b: 0.6, t: 4.2, e: 0.2, f: 1.1, p: 0.33 },
    ],
    defaults: { iterations: 120000, density: 70, pointSize: 1 },
  },
  radial2: {
    label: 'Radial 2',
    equation: 'radial',
    matrices: [
      { a: 0.52, b: 0.52, t: 0.8, e: 0.1, f: 0.1, p: 0.34 },
      { a: 0.52, b: 0.52, t: 2.9, e: 0.9, f: 0.2, p: 0.33 },
      { a: 0.52, b: 0.52, t: 4.7, e: 0.35, f: 1.0, p: 0.33 },
    ],
    defaults: { iterations: 120000, density: 76, pointSize: 1 },
  },
  radial3: {
    label: 'Radial 3',
    equation: 'radial',
    matrices: [
      { a: 0.5, b: 0.55, t: 1.2, e: 0.2, f: 0.05, p: 0.34 },
      { a: 0.5, b: 0.55, t: 3.4, e: 1.0, f: 0.25, p: 0.33 },
      { a: 0.5, b: 0.55, t: 5.5, e: 0.35, f: 1.05, p: 0.33 },
    ],
    defaults: { iterations: 120000, density: 80, pointSize: 1 },
  },
  sierpinskiTriangleIFS: {
    label: 'Sierpinski Triangle IFS',
    matrices: [
      { a: 0.5, b: 0, c: 0, d: 0.5, e: 0, f: 0, p: 0.33 },
      { a: 0.5, b: 0, c: 0, d: 0.5, e: 0.5, f: 0, p: 0.33 },
      { a: 0.5, b: 0, c: 0, d: 0.5, e: 0.25, f: 0.433, p: 0.34 },
    ],
    defaults: { iterations: 100000, density: 520, pointSize: 1 },
  },
  coral: {
    label: 'Coral',
    matrices: [
      { a: 0.307692, b: 0.531469, c: -0.461538, d: -0.293706, e: 5.401953, f: 8.655175, p: 0.4 },
      { a: 0.307692, b: -0.076923, c: 0.153846, d: -0.447552, e: -1.295248, f: 4.15299, p: 0.15 },
      { a: 0, b: 0.545455, c: 0.692308, d: -0.195804, e: -4.893637, f: 7.269794, p: 0.45 },
    ],
    defaults: { iterations: 145000, density: 44, pointSize: 1 },
  },
  fernDense: {
    label: 'Fern Dense',
    matrices: [
      { a: 0, b: 0, c: 0, d: 0.25, e: 0, f: -0.4, p: 0.02 },
      { a: 0.95, b: 0.005, c: -0.005, d: 0.93, e: -0.002, f: 0.5, p: 0.84 },
      { a: 0.035, b: -0.2, c: 0.16, d: 0.04, e: -0.09, f: 0.02, p: 0.07 },
      { a: -0.04, b: 0.2, c: 0.16, d: 0.04, e: 0.083, f: 0.12, p: 0.07 },
    ],
    defaults: { iterations: 180000, density: 62, pointSize: 1 },
  },
  shellSpiral: {
    label: 'Shell Spiral',
    equation: 'radial',
    matrices: [
      { a: 0.62, b: 0.62, t: 0.2, e: 0.1, f: 0, p: 0.5 },
      { a: 0.62, b: 0.62, t: 2.3, e: 0.9, f: 0.2, p: 0.25 },
      { a: 0.62, b: 0.62, t: 4.6, e: 0.35, f: 0.95, p: 0.25 },
    ],
    defaults: { iterations: 150000, density: 68, pointSize: 1 },
  },
  cantorDust: {
    label: 'Cantor Dust',
    matrices: [
      { a: 1 / 3, b: 0, c: 0, d: 1 / 3, e: 0, f: 0, p: 0.25 },
      { a: 1 / 3, b: 0, c: 0, d: 1 / 3, e: 2 / 3, f: 0, p: 0.25 },
      { a: 1 / 3, b: 0, c: 0, d: 1 / 3, e: 0, f: 2 / 3, p: 0.25 },
      { a: 1 / 3, b: 0, c: 0, d: 1 / 3, e: 2 / 3, f: 2 / 3, p: 0.25 },
    ],
    defaults: { iterations: 160000, density: 95, pointSize: 1 },
  },
  randomIfsGenerator: {
    label: 'Random IFS Generator',
    randomGenerator: { seed: 1337, count: 4 },
    defaults: { iterations: 170000, density: 64, pointSize: 1 },
  },
};

const LSYSTEM_PRESETS = {
  pythagorasTree: {
    label: 'Pythagoras Tree',
    axiom: 'F',
    rules: { F: 'F[+F][-F]F' },
    defaults: { iterations: 6, distance: 4, angle: 45, lengthScale: 1, lineWidth: 1, lineColor: '#14532d' },
  },
  lTree: {
    label: 'L Tree',
    axiom: 'X',
    rules: { X: 'F[+X]F[-X]+X', F: 'FF' },
    defaults: { iterations: 6, distance: 4.2, angle: 20, lengthScale: 1, lineWidth: 1, lineColor: '#166534' },
  },
  lTree2: {
    label: 'L Tree 2',
    axiom: 'X',
    rules: { X: 'F-[[X]+X]+F[+FX]-X', F: 'FF' },
    defaults: { iterations: 5, distance: 4.8, angle: 24, lengthScale: 1, lineWidth: 1.1, lineColor: '#15803d' },
  },
  seg32Curve: {
    label: '32 Segment Curve',
    axiom: 'F+F+F+F',
    rules: { F: 'F+F-F-FF+F+F-F' },
    defaults: { iterations: 3, distance: 3.2, angle: 90, lengthScale: 1, lineWidth: 1, lineColor: '#0f766e' },
  },
  boxFractal: {
    label: 'Box Fractal',
    axiom: 'F-F-F-F',
    rules: { F: 'F-F+F+FF-F-F+F' },
    defaults: { iterations: 3, distance: 4, angle: 90, lengthScale: 1, lineWidth: 1, lineColor: '#1d4ed8' },
  },
  dragonCurve: {
    label: 'Dragon Curve',
    axiom: 'FX',
    rules: { X: 'X+YF+', Y: '-FX-Y' },
    defaults: { iterations: 12, distance: 6, angle: 90, lengthScale: 1, lineWidth: 1, lineColor: '#7c2d12' },
  },
  twinDragonCurve: {
    label: 'Twin Dragon Curve',
    axiom: 'FX+FX+',
    rules: { X: 'X+YF+', Y: '-FX-Y' },
    defaults: { iterations: 10, distance: 5.5, angle: 90, lengthScale: 1, lineWidth: 1, lineColor: '#9a3412' },
  },
  threeDragonCurve: {
    label: 'Three Dragon Curve',
    axiom: 'FX+FX+FX',
    rules: { X: 'X+YF+', Y: '-FX-Y' },
    defaults: { iterations: 9, distance: 5.2, angle: 120, lengthScale: 1, lineWidth: 1, lineColor: '#92400e' },
  },
  terDragonCurve: {
    label: 'Ter Dragon Curve',
    axiom: 'F+F+F',
    rules: { F: 'F-F+F' },
    defaults: { iterations: 8, distance: 4.5, angle: 120, lengthScale: 1, lineWidth: 1, lineColor: '#b45309' },
  },
  levyCCurve: {
    label: 'Levy C Curve',
    axiom: 'F',
    rules: { F: '+F--F+' },
    defaults: { iterations: 12, distance: 6, angle: 45, lengthScale: 1, lineWidth: 1, lineColor: '#1e3a8a' },
  },
  hilbertsCurve: {
    label: 'Hilberts Curve',
    axiom: 'A',
    rules: { A: '-BF+AFA+FB-', B: '+AF-BFB-FA+' },
    defaults: { iterations: 6, distance: 6, angle: 90, lengthScale: 1, lineWidth: 1, lineColor: '#0c4a6e' },
  },
  hilbertCurve2: {
    label: 'Hilbert Curve II',
    axiom: 'LFL+F+LFL',
    rules: { L: '-RF+LFL+FR-', R: '+LF-RFR-FL+' },
    defaults: { iterations: 4, distance: 6, angle: 90, lengthScale: 1, lineWidth: 1, lineColor: '#075985' },
  },
  kochSnowflake: {
    label: 'Koch Snowflake',
    axiom: 'F--F--F',
    rules: { F: 'F+F--F+F' },
    defaults: { iterations: 5, distance: 4, angle: 60, lengthScale: 1, lineWidth: 1, lineColor: '#1d4ed8' },
  },
  peanoCurve: {
    label: 'Peano Curve',
    axiom: 'X',
    rules: { X: 'XFYFX+F+YFXFY-F-XFYFX', Y: 'YFXFY-F-XFYFX+F+YFXFY' },
    defaults: { iterations: 3, distance: 4.5, angle: 90, lengthScale: 1, lineWidth: 1, lineColor: '#0f766e' },
  },
  peanoGosperCurve: {
    label: 'Peano Gosper Curve',
    axiom: 'FX',
    rules: { X: 'X+YF++YF-FX--FXFX-YF+', Y: '-FX+YFYF++YF+FX--FX-Y' },
    defaults: { iterations: 4, distance: 4.2, angle: 60, lengthScale: 1, lineWidth: 1, lineColor: '#0f766e' },
  },
  quadraticKochIsland: {
    label: 'Quadratic Koch Island',
    axiom: 'F+F+F+F',
    rules: { F: 'F+F-F-FFF+F+F-F' },
    defaults: { iterations: 3, distance: 3.5, angle: 90, lengthScale: 1, lineWidth: 1, lineColor: '#047857' },
  },
  sierpinskiArrowhead: {
    label: 'Sierpinski Arrowhead',
    axiom: 'A',
    rules: { A: 'B-A-B', B: 'A+B+A' },
    defaults: { iterations: 8, distance: 6, angle: 60, lengthScale: 1, lineWidth: 1, lineColor: '#166534' },
  },
  sierpinskiCurve: {
    label: 'Sierpinski Curve',
    axiom: 'F--XF--F--XF',
    rules: { X: 'XF+F+XF--F--XF+F+X' },
    defaults: { iterations: 4, distance: 4, angle: 45, lengthScale: 1, lineWidth: 1, lineColor: '#14532d' },
  },
  siepinskiSieve: {
    label: 'Siepinski Sieve',
    axiom: 'FXF--FF--FF',
    rules: { X: '--FXF++FXF++FXF--' },
    defaults: { iterations: 6, distance: 4, angle: 60, lengthScale: 1, lineWidth: 1, lineColor: '#1e40af' },
  },
  quadraticSnowflake: {
    label: 'Quadratic Snowflake',
    axiom: 'F',
    rules: { F: 'F+F-F-F+F' },
    defaults: { iterations: 5, distance: 3.8, angle: 90, lengthScale: 1, lineWidth: 1, lineColor: '#1d4ed8' },
  },
  board: {
    label: 'Board',
    axiom: 'F+F+F+F',
    rules: { F: 'FF+F+F+F+FF' },
    defaults: { iterations: 3, distance: 2.8, angle: 90, lengthScale: 1, lineWidth: 1, lineColor: '#334155' },
  },
  cross: {
    label: 'Cross',
    axiom: 'F+F+F+F',
    rules: { F: 'F+F-F+F+F' },
    defaults: { iterations: 4, distance: 3, angle: 90, lengthScale: 1, lineWidth: 1, lineColor: '#374151' },
  },
  cross2: {
    label: 'Cross 2',
    axiom: 'F+F+F+F',
    rules: { F: 'F+F-F-F+F' },
    defaults: { iterations: 4, distance: 3, angle: 90, lengthScale: 1, lineWidth: 1, lineColor: '#1f2937' },
  },
  pentaplexity: {
    label: 'Pentaplexity',
    axiom: 'F++F++F++F++F',
    rules: { F: 'F++F++F+++++F-F++F' },
    defaults: { iterations: 3, distance: 3.6, angle: 36, lengthScale: 1, lineWidth: 1, lineColor: '#7c3aed' },
  },
  tiles: {
    label: 'Tiles',
    axiom: 'F+F+F+F',
    rules: { F: 'FF+F-F+F+FF' },
    defaults: { iterations: 3, distance: 3, angle: 90, lengthScale: 1, lineWidth: 1, lineColor: '#0369a1' },
  },
  rings: {
    label: 'Rings',
    axiom: 'F+F+F+F',
    rules: { F: 'F+F-F+F' },
    defaults: { iterations: 5, distance: 2.2, angle: 90, lengthScale: 1, lineWidth: 1, lineColor: '#0f766e' },
  },
  krishnaAnklets: {
    label: 'Krishna Anklets',
    axiom: 'X',
    rules: { X: 'XFX--XFX' },
    defaults: { iterations: 6, distance: 3, angle: 45, lengthScale: 1, lineWidth: 1, lineColor: '#9f1239' },
  },
  triangle: {
    label: 'Triangle',
    axiom: 'F-F-F',
    rules: { F: 'F-F+F' },
    defaults: { iterations: 7, distance: 4.5, angle: 120, lengthScale: 1, lineWidth: 1, lineColor: '#0f766e' },
  },
  quadraticGosper: {
    label: 'Quadratic Gosper',
    axiom: '-YF',
    rules: {
      X: 'XFX-YF-YF+FX+FXYF+YF-XFX-YF+FX+FXYFYF-',
      Y: '+FXFX-YF-YF+FX+FXYF-YF-XFXYFYF-',
    },
    defaults: { iterations: 3, distance: 4, angle: 90, lengthScale: 1, lineWidth: 1, lineColor: '#0c4a6e' },
  },
  crystal: {
    label: 'Crystal',
    axiom: 'F+F+F+F',
    rules: { F: 'FF+F++F+F' },
    defaults: { iterations: 4, distance: 2.7, angle: 90, lengthScale: 1, lineWidth: 1, lineColor: '#1d4ed8' },
  },
  mooreCurve: {
    label: 'Moore Curve',
    axiom: 'LFL+F+LFL',
    rules: { L: '-RF+LFL+FR-', R: '+LF-RFR-FL+' },
    defaults: { iterations: 5, distance: 5.3, angle: 90, lengthScale: 1, lineWidth: 1, lineColor: '#0369a1' },
  },
  fractalBush: {
    label: 'Fractal Bush',
    axiom: 'F',
    rules: { F: 'FF-[-F+F+F]+[+F-F-F]' },
    defaults: { iterations: 4, distance: 3.8, angle: 22.5, lengthScale: 1, lineWidth: 1, lineColor: '#166534' },
  },
  minkowskiSausage: {
    label: 'Minkowski Sausage',
    axiom: 'F',
    rules: { F: 'F+F-F-FF+F+F-F' },
    defaults: { iterations: 4, distance: 3.1, angle: 90, lengthScale: 1, lineWidth: 1, lineColor: '#0f766e' },
  },
  cesaroFractal: {
    label: 'Cesaro Fractal',
    axiom: 'F',
    rules: { F: 'F+F--F+F' },
    defaults: { iterations: 6, distance: 4.2, angle: 85, lengthScale: 1, lineWidth: 1, lineColor: '#1d4ed8' },
  },
  gosperIsland: {
    label: 'Gosper Island',
    axiom: 'FX',
    rules: { X: 'X+YF++YF-FX--FXFX-YF+', Y: '-FX+YFYF++YF+FX--FX-Y' },
    defaults: { iterations: 4, distance: 3.9, angle: 60, lengthScale: 1, lineWidth: 1, lineColor: '#0c4a6e' },
  },
  hexDragon: {
    label: 'Hex Dragon',
    axiom: 'FX',
    rules: { X: 'X+YF++YF-FX--FXFX-YF+', Y: '-FX+YFYF++YF+FX--FX-Y' },
    defaults: { iterations: 3, distance: 5, angle: 60, lengthScale: 1, lineWidth: 1, lineColor: '#7c2d12' },
  },
  sierpinskiCarpetPath: {
    label: 'Sierpinski Carpet Path',
    axiom: 'F+F+F+F',
    rules: { F: 'F+F-F-F-F+F+F+F-F' },
    defaults: { iterations: 3, distance: 2.8, angle: 90, lengthScale: 1, lineWidth: 1, lineColor: '#1f2937' },
  },
  stochasticPlants: {
    label: 'Stochastic Plants',
    axiom: 'F',
    rules: { F: 'F[+F]F[-F]F' },
    stochasticRules: {
      F: [
        { replacement: 'F[+F]F[-F]F', probability: 0.33 },
        { replacement: 'F[+F]F', probability: 0.33 },
        { replacement: 'F[-F]F', probability: 0.34 },
      ],
    },
    defaults: { iterations: 5, distance: 5, angle: 25, lengthScale: 0.93, lineWidth: 1, lineColor: '#166534' },
  },
  parametricWeeds: {
    label: 'Parametric Weeds',
    axiom: 'F',
    rules: { F: 'F[+F<][-F<]F<' },
    defaults: { iterations: 5, distance: 6, angle: 22.5, lengthScale: 0.84, lineWidth: 1, lineColor: '#15803d' },
  },
};

const ESCAPE_TIME_PRESETS = {
  mandelbrot: {
    label: 'Mandelbrot Set',
    family: 'escape-time',
    type: 'mandelbrot',
    viewport: { minX: -2.4, maxX: 1.0, minY: -1.2, maxY: 1.2 },
    maxIterations: 400,
    bailout: 4,
    power: 2,
  },
  juliaClassic: {
    label: 'Julia Set (c=-0.8+0.156i)',
    family: 'escape-time',
    type: 'julia',
    viewport: { minX: -1.7, maxX: 1.7, minY: -1.2, maxY: 1.2 },
    c: { re: -0.8, im: 0.156 },
    maxIterations: 400,
    bailout: 4,
    power: 2,
  },
  burningShip: {
    label: 'Burning Ship',
    family: 'escape-time',
    type: 'burning-ship',
    viewport: { minX: -2.2, maxX: 1.3, minY: -2.0, maxY: 0.7 },
    maxIterations: 400,
    bailout: 4,
  },
  multibrot: {
    label: 'Multibrot (d=3)',
    family: 'escape-time',
    type: 'mandelbrot',
    viewport: { minX: -2.2, maxX: 1.2, minY: -1.4, maxY: 1.4 },
    maxIterations: 420,
    bailout: 4,
    power: 3,
  },
};

const NEWTON_PRESETS = {
  newtonCubic: {
    label: 'Newton Fractal (z^3-1)',
    family: 'newton',
    type: 'newton-cubic',
    viewport: { minX: -2, maxX: 2, minY: -1.4, maxY: 1.4 },
    maxIterations: 40,
    epsilon: 1e-6,
  },
  newtonQuartic: {
    label: 'Newton Fractal (z^4-1)',
    family: 'newton',
    type: 'newton-quartic',
    viewport: { minX: -2, maxX: 2, minY: -1.4, maxY: 1.4 },
    maxIterations: 40,
    epsilon: 1e-6,
  },
};

const ATTRACTOR_PRESETS = {
  clifford: {
    label: 'Clifford Attractor',
    family: 'attractor',
    type: 'clifford',
    params: { a: -1.7, b: 1.8, c: -1.9, d: -0.4 },
    iterations: 800000,
    discard: 1000,
  },
  peterDeJong: {
    label: 'Peter de Jong Attractor',
    family: 'attractor',
    type: 'peter-de-jong',
    params: { a: 2.01, b: -2.53, c: 1.61, d: -0.33 },
    iterations: 800000,
    discard: 1000,
  },
  henon: {
    label: 'Henon Map',
    family: 'attractor',
    type: 'henon',
    params: { a: 1.4, b: 0.3 },
    iterations: 900000,
    discard: 1000,
  },
  ikeda: {
    label: 'Ikeda Map',
    family: 'attractor',
    type: 'ikeda',
    params: { u: 0.918 },
    iterations: 900000,
    discard: 1000,
  },
  hopalong: {
    label: 'Hopalong Attractor',
    family: 'attractor',
    type: 'hopalong',
    params: { a: 0.7, b: 0.9998, c: 0.2 },
    iterations: 900000,
    discard: 1000,
  },
  lorenz: {
    label: 'Lorenz Attractor (Projected)',
    family: 'attractor',
    type: 'lorenz',
    params: { sigma: 10, rho: 28, beta: 8 / 3, dt: 0.005 },
    iterations: 900000,
    discard: 1500,
  },
};

const INVERSION_PRESETS = {
  apollonianGasket: {
    label: 'Apollonian Gasket',
    family: 'inversion',
    type: 'apollonian-gasket',
    depth: 8,
    minRadius: 0.003,
  },
  kleinianSchottkyClassic: {
    label: 'Kleinian Group (Schottky Classic)',
    family: 'inversion',
    type: 'kleinian-schottky',
    style: 'denser-dust',
    iterations: 760000,
    discard: 180,
    seed: { x: 0.02, y: 0.01 },
    viewport: { minX: -1.4, maxX: 1.4, minY: -1.05, maxY: 1.05 },
    circles: [
      { x: -0.9, y: 0, r: 0.33 },
      { x: -0.22, y: 0, r: 0.23 },
      { x: 0.22, y: 0, r: 0.23 },
      { x: 0.9, y: 0, r: 0.33 },
    ],
  },
  kleinianSchottkyNecklace: {
    label: 'Kleinian Group (Schottky Necklace)',
    family: 'inversion',
    type: 'kleinian-schottky',
    style: 'chain-necklace',
    iterations: 620000,
    discard: 120,
    seed: { x: 0.06, y: -0.04 },
    viewport: { minX: -2.0, maxX: 2.0, minY: -1.25, maxY: 1.25 },
    circles: [
      { x: -1.15, y: 0.04, r: 0.5 },
      { x: -0.18, y: 0, r: 0.2 },
      { x: 0.58, y: 0.4, r: 0.25 },
      { x: 0.58, y: -0.4, r: 0.25 },
    ],
  },
  kleinianSchottkySymmetric: {
    label: 'Kleinian Group (Symmetric Limit Set)',
    family: 'inversion',
    type: 'kleinian-schottky',
    style: 'symmetric-limit-set',
    iterations: 700000,
    discard: 140,
    seed: { x: 0.01, y: 0.03 },
    viewport: { minX: -1.6, maxX: 1.6, minY: -1.2, maxY: 1.2 },
    circles: [
      { x: -0.86, y: 0.44, r: 0.34 },
      { x: -0.86, y: -0.44, r: 0.34 },
      { x: 0.86, y: 0.44, r: 0.34 },
      { x: 0.86, y: -0.44, r: 0.34 },
    ],
  },
};

function printHelp() {
  console.log([
    'Generate fractal artifacts for all default presets.',
    '',
    'Usage:',
    '  node scripts/generate-all-fractals.js [--width <px>] [--height <px>] [--size <WxH>] [--out <dir>]',
    '',
    'Examples:',
    '  node scripts/generate-all-fractals.js',
    '  node scripts/generate-all-fractals.js --size 1920x1080',
    '  node scripts/generate-all-fractals.js --width 800 --height 800 --out artifacts/custom',
  ].join('\n'));
}

function parseArgs(argv) {
  const options = {
    width: DEFAULT_WIDTH,
    height: DEFAULT_HEIGHT,
    outDir: path.resolve(process.cwd(), 'artifacts'),
  };

  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];

    if (arg === '--help' || arg === '-h') {
      options.help = true;
      return options;
    }

    if (arg === '--width') {
      options.width = Number(argv[i + 1]);
      i += 1;
      continue;
    }

    if (arg === '--height') {
      options.height = Number(argv[i + 1]);
      i += 1;
      continue;
    }

    if (arg === '--size') {
      const value = String(argv[i + 1] ?? '');
      i += 1;
      const [w, h] = value.toLowerCase().split('x').map(Number);
      options.width = w;
      options.height = h;
      continue;
    }

    if (arg === '--out') {
      options.outDir = path.resolve(process.cwd(), argv[i + 1]);
      i += 1;
      continue;
    }

    throw new Error(`Unknown argument: ${arg}`);
  }

  if (!Number.isFinite(options.width) || options.width <= 0) {
    throw new Error('Width must be a positive number');
  }

  if (!Number.isFinite(options.height) || options.height <= 0) {
    throw new Error('Height must be a positive number');
  }

  options.width = Math.round(options.width);
  options.height = Math.round(options.height);

  return options;
}

function slugify(input) {
  return input
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/(^-|-$)/g, '');
}

function createPng(width, height) {
  const png = new PNG({ width, height });
  png.data.fill(255);
  return png;
}

function setPixel(png, x, y, r, g, b, a = 255) {
  if (x < 0 || y < 0 || x >= png.width || y >= png.height) {
    return;
  }

  const idx = (png.width * y + x) << 2;
  png.data[idx] = r;
  png.data[idx + 1] = g;
  png.data[idx + 2] = b;
  png.data[idx + 3] = a;
}

function drawSquare(png, x, y, size, color) {
  const half = Math.floor(size / 2);
  for (let yy = y - half; yy <= y + half; yy += 1) {
    for (let xx = x - half; xx <= x + half; xx += 1) {
      setPixel(png, xx, yy, color[0], color[1], color[2]);
    }
  }
}

function drawLine(png, x0, y0, x1, y1, color, width = 1) {
  let x = x0;
  let y = y0;
  const dx = Math.abs(x1 - x0);
  const sx = x0 < x1 ? 1 : -1;
  const dy = -Math.abs(y1 - y0);
  const sy = y0 < y1 ? 1 : -1;
  let err = dx + dy;

  while (true) {
    drawSquare(png, x, y, width, color);
    if (x === x1 && y === y1) {
      break;
    }
    const e2 = 2 * err;
    if (e2 >= dy) {
      err += dy;
      x += sx;
    }
    if (e2 <= dx) {
      err += dx;
      y += sy;
    }
  }
}

function createTransform(bounds, width, height, padding = 24) {
  const [maxX, maxY, minX, minY] = bounds;
  const boundsW = Math.max(1, maxX - minX);
  const boundsH = Math.max(1, maxY - minY);

  const scaleX = (width - padding * 2) / boundsW;
  const scaleY = (height - padding * 2) / boundsH;
  const scale = Math.min(scaleX, scaleY);

  const offsetX = (width - boundsW * scale) / 2;
  const offsetY = (height - boundsH * scale) / 2;

  return (x, y) => {
    const px = Math.round((x - minX) * scale + offsetX);
    const py = Math.round(height - ((y - minY) * scale + offsetY));
    return [px, py];
  };
}

function matrixColor(index) {
  const palette = [
    [16, 185, 129],
    [5, 150, 105],
    [34, 197, 94],
    [20, 184, 166],
    [6, 182, 212],
    [59, 130, 246],
  ];
  return palette[Math.abs(index) % palette.length];
}

function lerp(a, b, t) {
  return a + (b - a) * t;
}

function seededRandom(seed) {
  let state = seed >>> 0;
  return () => {
    state = (1664525 * state + 1013904223) >>> 0;
    return state / 0x100000000;
  };
}

function buildRandomIfsMatrices(config = {}) {
  const count = Math.max(3, Math.min(6, Math.round(config.count ?? 4)));
  const random = seededRandom(config.seed ?? 1337);
  const matrices = [];
  const p = 1 / count;
  for (let i = 0; i < count; i += 1) {
    matrices.push({
      a: random() * 0.62 - 0.31,
      b: random() * 0.62 - 0.31,
      c: random() * 0.62 - 0.31,
      d: random() * 0.62 - 0.31,
      e: random() * 2 - 1,
      f: random() * 2 - 1,
      p,
    });
  }
  return matrices;
}

function gradientColor(t) {
  const stops = [
    [9, 10, 38],
    [45, 78, 140],
    [98, 187, 255],
    [255, 236, 130],
    [255, 140, 66],
  ];
  const clamped = Math.max(0, Math.min(1, t));
  const scaled = clamped * (stops.length - 1);
  const idx = Math.floor(scaled);
  const frac = scaled - idx;
  const c1 = stops[idx];
  const c2 = stops[Math.min(stops.length - 1, idx + 1)];
  return [
    Math.round(lerp(c1[0], c2[0], frac)),
    Math.round(lerp(c1[1], c2[1], frac)),
    Math.round(lerp(c1[2], c2[2], frac)),
  ];
}

function mapPixelToComplex(x, y, width, height, viewport) {
  const re = viewport.minX + (x / (width - 1)) * (viewport.maxX - viewport.minX);
  const im = viewport.maxY - (y / (height - 1)) * (viewport.maxY - viewport.minY);
  return [re, im];
}

function renderEscapeTime(preset, width, height) {
  const png = createPng(width, height);
  const maxIterations = preset.maxIterations;
  const bailout = preset.bailout ?? 4;
  const power = preset.power ?? 2;

  for (let y = 0; y < height; y += 1) {
    for (let x = 0; x < width; x += 1) {
      const [u, v] = mapPixelToComplex(x, y, width, height, preset.viewport);

      let zr;
      let zi;
      let cr;
      let ci;

      if (preset.type === 'julia') {
        zr = u;
        zi = v;
        cr = preset.c.re;
        ci = preset.c.im;
      } else {
        zr = 0;
        zi = 0;
        cr = u;
        ci = v;
      }

      let escaped = false;
      let iter = 0;

      for (; iter < maxIterations; iter += 1) {
        let ar = zr;
        let ai = zi;

        if (preset.type === 'burning-ship') {
          ar = Math.abs(ar);
          ai = Math.abs(ai);
        }

        let nextR;
        let nextI;
        if (power === 2) {
          nextR = ar * ar - ai * ai + cr;
          nextI = 2 * ar * ai + ci;
        } else {
          const mag = Math.sqrt(ar * ar + ai * ai);
          const angle = Math.atan2(ai, ar);
          const magPow = mag ** power;
          nextR = magPow * Math.cos(power * angle) + cr;
          nextI = magPow * Math.sin(power * angle) + ci;
        }

        zr = nextR;
        zi = nextI;

        if (zr * zr + zi * zi > bailout * bailout) {
          escaped = true;
          break;
        }
      }

      if (!escaped) {
        setPixel(png, x, y, 6, 7, 15, 255);
        continue;
      }

      const t = iter / maxIterations;
      const [r, g, b] = gradientColor(t);
      setPixel(png, x, y, r, g, b, 255);
    }
  }

  return {
    png,
    count: width * height,
  };
}

function closestRootIndex(zr, zi, roots) {
  let idx = 0;
  let best = Number.POSITIVE_INFINITY;
  for (let i = 0; i < roots.length; i += 1) {
    const dr = zr - roots[i][0];
    const di = zi - roots[i][1];
    const d2 = dr * dr + di * di;
    if (d2 < best) {
      best = d2;
      idx = i;
    }
  }
  return idx;
}

function renderNewton(preset, width, height) {
  const png = createPng(width, height);
  const maxIterations = preset.maxIterations;
  const epsilon = preset.epsilon;

  const roots = preset.type === 'newton-cubic'
    ? [[1, 0], [-0.5, Math.sqrt(3) / 2], [-0.5, -Math.sqrt(3) / 2]]
    : [[1, 0], [0, 1], [-1, 0], [0, -1]];

  const basePalette = [
    [239, 68, 68],
    [59, 130, 246],
    [34, 197, 94],
    [234, 179, 8],
  ];

  for (let y = 0; y < height; y += 1) {
    for (let x = 0; x < width; x += 1) {
      let [zr, zi] = mapPixelToComplex(x, y, width, height, preset.viewport);

      let iter = 0;
      for (; iter < maxIterations; iter += 1) {
        let fr;
        let fi;
        let dfr;
        let dfi;

        if (preset.type === 'newton-cubic') {
          // f(z)=z^3-1, f'(z)=3z^2
          const z2r = zr * zr - zi * zi;
          const z2i = 2 * zr * zi;
          const z3r = z2r * zr - z2i * zi;
          const z3i = z2r * zi + z2i * zr;
          fr = z3r - 1;
          fi = z3i;
          dfr = 3 * z2r;
          dfi = 3 * z2i;
        } else {
          // f(z)=z^4-1, f'(z)=4z^3
          const z2r = zr * zr - zi * zi;
          const z2i = 2 * zr * zi;
          const z3r = z2r * zr - z2i * zi;
          const z3i = z2r * zi + z2i * zr;
          const z4r = z2r * z2r - z2i * z2i;
          const z4i = 2 * z2r * z2i;
          fr = z4r - 1;
          fi = z4i;
          dfr = 4 * z3r;
          dfi = 4 * z3i;
        }

        const denom = dfr * dfr + dfi * dfi;
        if (denom < 1e-14) {
          break;
        }

        const qr = (fr * dfr + fi * dfi) / denom;
        const qi = (fi * dfr - fr * dfi) / denom;
        zr -= qr;
        zi -= qi;

        if (qr * qr + qi * qi < epsilon * epsilon) {
          break;
        }
      }

      const rootIndex = closestRootIndex(zr, zi, roots);
      const base = basePalette[rootIndex % basePalette.length];
      const shade = 0.35 + 0.65 * (1 - iter / maxIterations);
      setPixel(
        png,
        x,
        y,
        Math.round(base[0] * shade),
        Math.round(base[1] * shade),
        Math.round(base[2] * shade),
        255,
      );
    }
  }

  return {
    png,
    count: width * height,
  };
}

function iterateAttractorPoint(type, state, params) {
  const x = state.x;
  const y = state.y;
  const z = state.z ?? 0;
  if (type === 'clifford') {
    return {
      x: Math.sin(params.a * y) + params.c * Math.cos(params.a * x),
      y: Math.sin(params.b * x) + params.d * Math.cos(params.b * y),
      z,
    };
  }
  if (type === 'peter-de-jong') {
    return {
      x: Math.sin(params.a * y) - Math.cos(params.b * x),
      y: Math.sin(params.c * x) - Math.cos(params.d * y),
      z,
    };
  }
  if (type === 'henon') {
    return {
      x: 1 - params.a * x * x + y,
      y: params.b * x,
      z,
    };
  }
  if (type === 'ikeda') {
    const t = 0.4 - 6 / (1 + x * x + y * y);
    return {
      x: 1 + params.u * (x * Math.cos(t) - y * Math.sin(t)),
      y: params.u * (x * Math.sin(t) + y * Math.cos(t)),
      z,
    };
  }
  if (type === 'hopalong') {
    const sign = x < 0 ? -1 : 1;
    return {
      x: y - sign * Math.sqrt(Math.abs(params.b * x - params.c)),
      y: params.a - x,
      z,
    };
  }
  if (type === 'lorenz') {
    const dt = params.dt ?? 0.005;
    const nextX = x + params.sigma * (y - x) * dt;
    const nextY = y + (x * (params.rho - z) - y) * dt;
    const nextZ = z + (x * y - params.beta * z) * dt;
    return {
      x: nextX,
      y: nextY,
      z: nextZ,
    };
  }
  return { x, y, z };
}

function projectAttractorPoint(type, state) {
  if (type === 'lorenz') {
    return { px: state.x, py: state.z };
  }
  return { px: state.x, py: state.y };
}

function renderAttractor(preset, width, height) {
  const iterations = preset.iterations;
  const discard = preset.discard;
  const params = preset.params;

  let state = {
    x: preset.type === 'lorenz' ? 0.1 : 0,
    y: 0,
    z: 0,
  };

  let minX = Number.POSITIVE_INFINITY;
  let minY = Number.POSITIVE_INFINITY;
  let maxX = Number.NEGATIVE_INFINITY;
  let maxY = Number.NEGATIVE_INFINITY;

  for (let i = 0; i < iterations; i += 1) {
    state = iterateAttractorPoint(preset.type, state, params);
    if (i < discard) {
      continue;
    }
    const { px, py } = projectAttractorPoint(preset.type, state);
    minX = Math.min(minX, px);
    minY = Math.min(minY, py);
    maxX = Math.max(maxX, px);
    maxY = Math.max(maxY, py);
  }

  const hist = new Uint32Array(width * height);
  state = {
    x: preset.type === 'lorenz' ? 0.1 : 0,
    y: 0,
    z: 0,
  };
  const scaleX = (width - 1) / Math.max(1e-9, maxX - minX);
  const scaleY = (height - 1) / Math.max(1e-9, maxY - minY);
  let maxCount = 0;

  for (let i = 0; i < iterations; i += 1) {
    state = iterateAttractorPoint(preset.type, state, params);
    if (i < discard) {
      continue;
    }
    const { px: x, py: y } = projectAttractorPoint(preset.type, state);

    const px = Math.floor((x - minX) * scaleX);
    const py = Math.floor((maxY - y) * scaleY);
    if (px < 0 || py < 0 || px >= width || py >= height) {
      continue;
    }

    const idx = py * width + px;
    hist[idx] += 1;
    if (hist[idx] > maxCount) {
      maxCount = hist[idx];
    }
  }

  const png = createPng(width, height);
  for (let py = 0; py < height; py += 1) {
    for (let px = 0; px < width; px += 1) {
      const count = hist[py * width + px];
      if (count === 0) {
        continue;
      }
      const t = Math.log(count + 1) / Math.log(maxCount + 1);
      const [r, g, b] = gradientColor(t);
      setPixel(png, px, py, r, g, b, 255);
    }
  }

  return {
    png,
    count: iterations - discard,
  };
}

function drawCircle(png, cx, cy, r, color, lineWidth = 1) {
  const samples = Math.max(24, Math.round(2 * Math.PI * r));
  for (let w = 0; w < lineWidth; w += 1) {
    const radius = r - w;
    for (let i = 0; i < samples; i += 1) {
      const t = (i / samples) * Math.PI * 2;
      const x = Math.round(cx + radius * Math.cos(t));
      const y = Math.round(cy + radius * Math.sin(t));
      setPixel(png, x, y, color[0], color[1], color[2], 255);
    }
  }
}

function invertPoint(point, circle) {
  const dx = point.x - circle.x;
  const dy = point.y - circle.y;
  const d2 = dx * dx + dy * dy;
  if (d2 < 1e-14) {
    return null;
  }
  const scale = (circle.r * circle.r) / d2;
  return {
    x: circle.x + dx * scale,
    y: circle.y + dy * scale,
  };
}

function composeInversions(point, first, second) {
  const once = invertPoint(point, first);
  if (!once) {
    return null;
  }
  return invertPoint(once, second);
}

function renderApollonian(preset, width, height) {
  const circles = [];
  const seen = new Set();

  function keyForCircle(circle) {
    return `${Math.round(circle.k * 1e6)}:${Math.round(circle.x * 1e6)}:${Math.round(circle.y * 1e6)}`;
  }

  function addCircle(circle) {
    const key = keyForCircle(circle);
    if (seen.has(key)) {
      return false;
    }
    seen.add(key);
    circles.push(circle);
    return true;
  }

  const c1 = { k: -1, x: 0, y: 0 };
  const c2 = { k: 2, x: -0.5, y: 0 };
  const c3 = { k: 2, x: 0.5, y: 0 };
  const c4 = { k: 3, x: 0, y: 2 / 3 };
  [c1, c2, c3, c4].forEach(addCircle);

  function recurse(a, b, c, d, depth) {
    if (depth <= 0) {
      return;
    }

    const combos = [
      [b, c, d, a],
      [a, c, d, b],
      [a, b, d, c],
      [a, b, c, d],
    ];

    for (const [u, v, w, old] of combos) {
      const k = 2 * (u.k + v.k + w.k) - old.k;
      if (Math.abs(k) < 1e-9) {
        continue;
      }

      const x = (2 * (u.k * u.x + v.k * v.x + w.k * w.x) - old.k * old.x) / k;
      const y = (2 * (u.k * u.y + v.k * v.y + w.k * w.y) - old.k * old.y) / k;
      const r = Math.abs(1 / k);
      if (r < preset.minRadius) {
        continue;
      }

      const circle = { k, x, y };
      if (!addCircle(circle)) {
        continue;
      }
      recurse(u, v, w, circle, depth - 1);
    }
  }

  recurse(c1, c2, c3, c4, preset.depth);

  const png = createPng(width, height);
  const margin = 18;
  const scale = Math.min((width - margin * 2) / 2, (height - margin * 2) / 2);
  const cx = Math.round(width / 2);
  const cy = Math.round(height / 2);

  for (const c of circles) {
    const r = Math.abs(1 / c.k) * scale;
    const px = Math.round(cx + c.x * scale);
    const py = Math.round(cy - c.y * scale);
    drawCircle(png, px, py, r, [17, 24, 39], 1);
  }

  return {
    png,
    count: circles.length,
  };
}

function renderKleinianSchottky(preset, width, height) {
  const png = createPng(width, height);
  const iterations = Math.max(1000, Math.round(preset.iterations ?? 300000));
  const discard = Math.max(0, Math.round(preset.discard ?? 80));
  const circles = preset.circles;

  const generators = [
    (point) => composeInversions(point, circles[0], circles[1]),
    (point) => composeInversions(point, circles[1], circles[0]),
    (point) => composeInversions(point, circles[2], circles[3]),
    (point) => composeInversions(point, circles[3], circles[2]),
  ];
  const inverseGenerator = [1, 0, 3, 2];

  const points = [];
  let minX = Number.POSITIVE_INFINITY;
  let minY = Number.POSITIVE_INFINITY;
  let maxX = Number.NEGATIVE_INFINITY;
  let maxY = Number.NEGATIVE_INFINITY;

  let point = {
    x: preset.seed?.x ?? 0.02,
    y: preset.seed?.y ?? 0.01,
  };
  let previousGenerator = -1;

  for (let i = 0; i < iterations + discard; i += 1) {
    let generatorIndex = Math.floor(Math.random() * generators.length);
    if (previousGenerator >= 0) {
      while (generatorIndex === inverseGenerator[previousGenerator]) {
        generatorIndex = Math.floor(Math.random() * generators.length);
      }
    }

    const next = generators[generatorIndex](point);
    previousGenerator = generatorIndex;

    if (!next || !Number.isFinite(next.x) || !Number.isFinite(next.y)) {
      point = { x: 0.02, y: 0.02 };
      previousGenerator = -1;
      continue;
    }

    point = next;

    if (i < discard) {
      continue;
    }
    points.push([point.x, point.y]);
    minX = Math.min(minX, point.x);
    minY = Math.min(minY, point.y);
    maxX = Math.max(maxX, point.x);
    maxY = Math.max(maxY, point.y);
  }

  if (points.length === 0) {
    return { png, count: 0 };
  }

  const hist = new Uint32Array(width * height);
  let maxCount = 0;
  const pad = 0.03;
  const spanX = Math.max(1e-9, maxX - minX);
  const spanY = Math.max(1e-9, maxY - minY);
  const loX = minX - spanX * pad;
  const hiX = maxX + spanX * pad;
  const loY = minY - spanY * pad;
  const hiY = maxY + spanY * pad;

  for (let i = 0; i < points.length; i += 1) {
    const x = points[i][0];
    const y = points[i][1];
    const px = Math.floor(((x - loX) / (hiX - loX)) * (width - 1));
    const py = Math.floor(((hiY - y) / (hiY - loY)) * (height - 1));
    if (px < 0 || py < 0 || px >= width || py >= height) continue;
    const idx = py * width + px;
    hist[idx] += 1;
    if (hist[idx] > maxCount) maxCount = hist[idx];
  }

  for (let py = 0; py < height; py += 1) {
    for (let px = 0; px < width; px += 1) {
      const value = hist[py * width + px];
      if (value === 0) {
        continue;
      }
      const t = Math.log(value + 1) / Math.log(maxCount + 1);
      const [r, g, b] = gradientColor(t);
      setPixel(png, px, py, r, g, b, 255);
    }
  }

  return {
    png,
    count: points.length,
  };
}

function renderInversion(preset, width, height) {
  if (preset.type === 'apollonian-gasket') {
    return renderApollonian(preset, width, height);
  }
  if (preset.type === 'kleinian-schottky') {
    return renderKleinianSchottky(preset, width, height);
  }
  throw new Error(`Unsupported inversion preset type: ${preset.type}`);
}

function renderIFS(IFS, radial, preset, width, height) {
  const options = preset.defaults;
  const matrices = preset.randomGenerator
    ? buildRandomIfsMatrices(preset.randomGenerator)
    : preset.matrices;
  const fractal = new IFS({
    matrices,
    iterations: options.iterations,
    density: options.density,
    equation: preset.equation === 'radial' ? radial : undefined,
  });

  fractal.run();

  const png = createPng(width, height);
  const toPixel = createTransform(fractal.bounds, width, height, 20);
  const pointSize = Math.max(1, Math.round(options.pointSize ?? 1));

  for (let i = 0; i < fractal.points.length; i += 1) {
    const [x, y, { matrixNum }] = fractal.points[i];
    const [px, py] = toPixel(x, y);
    drawSquare(png, px, py, pointSize, matrixColor(matrixNum));
  }

  return {
    png,
    count: fractal.points.length,
  };
}

function renderLSystem(LSystem, preset, width, height) {
  const options = preset.defaults;
  const fractal = new LSystem({
    axiom: preset.axiom,
    rules: preset.rules,
    iterations: options.iterations,
    distance: options.distance,
    angle: options.angle,
    lengthScale: options.lengthScale,
  });

  fractal.run();

  const png = createPng(width, height);
  const toPixel = createTransform(fractal.bounds, width, height, 28);
  const lineColorHex = String(options.lineColor ?? '#0f172a').replace('#', '');
  const lineColor = [
    parseInt(lineColorHex.slice(0, 2), 16),
    parseInt(lineColorHex.slice(2, 4), 16),
    parseInt(lineColorHex.slice(4, 6), 16),
  ];
  const lineWidth = Math.max(1, Math.round(options.lineWidth ?? 1));

  let prev = null;
  for (let i = 0; i < fractal.points.length; i += 1) {
    const [x, y, meta] = fractal.points[i];
    const current = toPixel(x, y);

    if (!prev || !meta.paintable) {
      prev = current;
      continue;
    }

    drawLine(png, prev[0], prev[1], current[0], current[1], lineColor, lineWidth);
    prev = current;
  }

  return {
    png,
    count: fractal.points.length,
  };
}

async function writePng(filePath, png) {
  const data = PNG.sync.write(png);
  await fs.writeFile(filePath, data);
}

async function loadFractalClasses() {
  try {
    const ifsModule = require(path.resolve(__dirname, '../lib/ifs.js'));
    const lModule = require(path.resolve(__dirname, '../lib/l.js'));
    return {
      IFS: ifsModule.IFS,
      radial: ifsModule.radial,
      LSystem: lModule.LSystem,
    };
  } catch (error) {
    throw new Error(
      'Cannot load compiled fractal classes from lib/. Run "npm run build" first, then retry.\n' +
        String(error.message || error),
    );
  }
}

async function generateAll(options) {
  const { IFS, radial, LSystem } = await loadFractalClasses();

  const ifsDir = path.join(options.outDir, 'ifs');
  const lsysDir = path.join(options.outDir, 'lsystem');
  const escapeDir = path.join(options.outDir, 'escape-time');
  const attractorDir = path.join(options.outDir, 'attractors');
  const newtonDir = path.join(options.outDir, 'newton');
  const inversionDir = path.join(options.outDir, 'inversions');

  await fs.mkdir(ifsDir, { recursive: true });
  await fs.mkdir(lsysDir, { recursive: true });
  await fs.mkdir(escapeDir, { recursive: true });
  await fs.mkdir(attractorDir, { recursive: true });
  await fs.mkdir(newtonDir, { recursive: true });
  await fs.mkdir(inversionDir, { recursive: true });

  const summary = {
    generatedAt: new Date().toISOString(),
    size: { width: options.width, height: options.height },
    ifs: [],
    lsystem: [],
    escapeTime: [],
    attractors: [],
    newton: [],
    inversions: [],
  };

  for (const preset of Object.values(IFS_PRESETS)) {
    const outputName = `${slugify(preset.label)}.png`;
    const outputPath = path.join(ifsDir, outputName);

    const { png, count } = renderIFS(IFS, radial, preset, options.width, options.height);
    await writePng(outputPath, png);

    summary.ifs.push({
      name: preset.label,
      file: path.relative(options.outDir, outputPath),
      points: count,
    });

    console.log(`IFS: ${preset.label} -> ${outputPath}`);
  }

  for (const preset of Object.values(LSYSTEM_PRESETS)) {
    const outputName = `${slugify(preset.label)}.png`;
    const outputPath = path.join(lsysDir, outputName);

    const { png, count } = renderLSystem(LSystem, preset, options.width, options.height);
    await writePng(outputPath, png);

    summary.lsystem.push({
      name: preset.label,
      file: path.relative(options.outDir, outputPath),
      points: count,
    });

    console.log(`L-system: ${preset.label} -> ${outputPath}`);
  }

  for (const preset of Object.values(ESCAPE_TIME_PRESETS)) {
    const outputName = `${slugify(preset.label)}.png`;
    const outputPath = path.join(escapeDir, outputName);

    const { png, count } = renderEscapeTime(preset, options.width, options.height);
    await writePng(outputPath, png);

    summary.escapeTime.push({
      name: preset.label,
      file: path.relative(options.outDir, outputPath),
      points: count,
    });

    console.log(`Escape-time: ${preset.label} -> ${outputPath}`);
  }

  for (const preset of Object.values(NEWTON_PRESETS)) {
    const outputName = `${slugify(preset.label)}.png`;
    const outputPath = path.join(newtonDir, outputName);

    const { png, count } = renderNewton(preset, options.width, options.height);
    await writePng(outputPath, png);

    summary.newton.push({
      name: preset.label,
      file: path.relative(options.outDir, outputPath),
      points: count,
    });

    console.log(`Newton: ${preset.label} -> ${outputPath}`);
  }

  for (const preset of Object.values(ATTRACTOR_PRESETS)) {
    const outputName = `${slugify(preset.label)}.png`;
    const outputPath = path.join(attractorDir, outputName);

    const { png, count } = renderAttractor(preset, options.width, options.height);
    await writePng(outputPath, png);

    summary.attractors.push({
      name: preset.label,
      file: path.relative(options.outDir, outputPath),
      points: count,
    });

    console.log(`Attractor: ${preset.label} -> ${outputPath}`);
  }

  for (const preset of Object.values(INVERSION_PRESETS)) {
    const outputName = `${slugify(preset.label)}.png`;
    const outputPath = path.join(inversionDir, outputName);

    const { png, count } = renderInversion(preset, options.width, options.height);
    await writePng(outputPath, png);

    summary.inversions.push({
      name: preset.label,
      file: path.relative(options.outDir, outputPath),
      points: count,
    });

    console.log(`Inversion: ${preset.label} -> ${outputPath}`);
  }

  await fs.writeFile(path.join(options.outDir, 'index.json'), `${JSON.stringify(summary, null, 2)}\n`);

  console.log('Done.');
  console.log(`Artifacts directory: ${options.outDir}`);
  console.log(
    `Generated ${summary.ifs.length} IFS + ${summary.lsystem.length} L-system + ${summary.escapeTime.length} escape-time + ${summary.newton.length} Newton + ${summary.attractors.length} attractor + ${summary.inversions.length} inversion fractals.`,
  );
}

async function main() {
  try {
    const options = parseArgs(process.argv.slice(2));

    if (options.help) {
      printHelp();
      return;
    }

    await generateAll(options);
  } catch (error) {
    console.error(error.message || error);
    process.exitCode = 1;
  }
}

module.exports = {
  DEFAULT_WIDTH,
  DEFAULT_HEIGHT,
  IFS_PRESETS,
  LSYSTEM_PRESETS,
  ESCAPE_TIME_PRESETS,
  NEWTON_PRESETS,
  ATTRACTOR_PRESETS,
  INVERSION_PRESETS,
  slugify,
  generateAll,
};

if (require.main === module) {
  main();
}
