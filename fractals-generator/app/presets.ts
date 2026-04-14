export const PRESETS = {
  ifs: {
    fern: {
      label: 'Fern',
      matrices: [
        { a: 0, b: 0, c: 0, d: 0.16, e: 0, f: 0, p: 0.01 },
        { a: 0.85, b: 0.04, c: -0.04, d: 0.85, e: 0, f: 1.6, p: 0.85 },
        { a: 0.2, b: -0.26, c: 0.23, d: 0.22, e: 0, f: 1.6, p: 0.07 },
        { a: -0.15, b: 0.28, c: 0.26, d: 0.24, e: 0, f: 0.44, p: 0.07 },
      ],
      defaults: { iterations: 120000, density: 65, pointSize: 1.2, colorMode: 'matrix' },
    },
    weed: {
      label: 'Weed',
      matrices: [
        { a: 0.14, b: 0.01, c: 0, d: 0.51, e: -0.08, f: -1.31, p: 0.1 },
        { a: 0.43, b: 0.52, c: -0.45, d: 0.5, e: 1.49, f: -0.75, p: 0.35 },
        { a: 0.45, b: -0.49, c: 0.47, d: 0.47, e: -1.62, f: -0.74, p: 0.35 },
        { a: 0.49, b: 0, c: 0, d: 0.51, e: 0.02, f: 1.62, p: 0.2 },
      ],
      defaults: { iterations: 125000, density: 58, pointSize: 1.2, colorMode: 'emerald' },
    },
    radial1: {
      label: 'Radial 1',
      equation: 'radial',
      matrices: [
        { a: 0.6, b: 0.6, t: 0.4, e: 0, f: 0, p: 0.34 },
        { a: 0.6, b: 0.6, t: 2.4, e: 1.2, f: 0.1, p: 0.33 },
        { a: 0.6, b: 0.6, t: 4.2, e: 0.2, f: 1.1, p: 0.33 },
      ],
      defaults: { iterations: 120000, density: 70, pointSize: 1.1, colorMode: 'matrix' },
    },
  },
  lsystem: {
    pythagorasTree: {
      label: 'Pythagoras Tree',
      axiom: 'F',
      rules: { F: 'F[+F][-F]F' },
      defaults: { iterations: 6, distance: 4, angle: 45, lengthScale: 1, lineWidth: 1, lineColor: '#14532d' },
    },
    dragonCurve: {
      label: 'Dragon Curve',
      axiom: 'FX',
      rules: { X: 'X+YF+', Y: '-FX-Y' },
      defaults: { iterations: 12, distance: 6, angle: 90, lengthScale: 1, lineWidth: 1, lineColor: '#7c2d12' },
    },
    kochSnowflake: {
      label: 'Koch Snowflake',
      axiom: 'F--F--F',
      rules: { F: 'F+F--F+F' },
      defaults: { iterations: 5, distance: 4, angle: 60, lengthScale: 1, lineWidth: 1, lineColor: '#1d4ed8' },
    },
  },
  escapeTime: {
    mandelbrot: { label: 'Mandelbrot', type: 'mandelbrot', viewport: { minX: -2.4, maxX: 1, minY: -1.2, maxY: 1.2 }, defaults: { maxIterations: 300, bailout: 4, power: 2, cRe: -0.8, cIm: 0.156 } },
    juliaClassic: { label: 'Julia', type: 'julia', viewport: { minX: -1.7, maxX: 1.7, minY: -1.2, maxY: 1.2 }, defaults: { maxIterations: 300, bailout: 4, power: 2, cRe: -0.8, cIm: 0.156 } },
    burningShip: { label: 'Burning Ship', type: 'burning-ship', viewport: { minX: -2.2, maxX: 1.3, minY: -2, maxY: 0.7 }, defaults: { maxIterations: 300, bailout: 4, power: 2, cRe: 0, cIm: 0 } },
  },
  newton: {
    cubic: { label: 'Newton Cubic', type: 'newton-cubic', viewport: { minX: -2, maxX: 2, minY: -1.4, maxY: 1.4 }, defaults: { maxIterations: 40, epsilon: 0.000001 } },
    quartic: { label: 'Newton Quartic', type: 'newton-quartic', viewport: { minX: -2, maxX: 2, minY: -1.4, maxY: 1.4 }, defaults: { maxIterations: 40, epsilon: 0.000001 } },
  },
  attractor: {
    clifford: { label: 'Clifford', type: 'clifford', defaults: { iterations: 500000, discard: 1000, a: -1.7, b: 1.8, c: -1.9, d: -0.4 } },
    peterDeJong: { label: 'Peter de Jong', type: 'peter-de-jong', defaults: { iterations: 500000, discard: 1000, a: 2.01, b: -2.53, c: 1.61, d: -0.33 } },
    lorenz: { label: 'Lorenz', type: 'lorenz', defaults: { iterations: 500000, discard: 1200, a: 10, b: 28, c: 2.6666667, d: 0.005 } },
  },
  inversion: {
    apollonian: { label: 'Apollonian', type: 'apollonian-gasket', defaults: { depth: 8, minRadius: 0.003 } },
    kleinianClassic: { label: 'Kleinian Classic', type: 'kleinian-schottky', defaults: { depth: 8, minRadius: 0.003, iterations: 420000, discard: 140, circles: [{ x: -0.9, y: 0, r: 0.33 }, { x: -0.22, y: 0, r: 0.23 }, { x: 0.22, y: 0, r: 0.23 }, { x: 0.9, y: 0, r: 0.33 }], seed: { x: 0.02, y: 0.01 } } },
    kleinianNecklace: { label: 'Kleinian Necklace', type: 'kleinian-schottky', defaults: { depth: 8, minRadius: 0.003, iterations: 420000, discard: 140, circles: [{ x: -1.15, y: 0.04, r: 0.5 }, { x: -0.18, y: 0, r: 0.2 }, { x: 0.58, y: 0.4, r: 0.25 }, { x: 0.58, y: -0.4, r: 0.25 }], seed: { x: 0.06, y: -0.04 } } },
  },
} as const;
