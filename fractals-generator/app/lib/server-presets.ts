type AnyRecord = Record<string, any>;

const scriptPresets = require('../../scripts/generate-all-fractals.js') as AnyRecord;

export function getAppPresets(): AnyRecord {
  const mod = scriptPresets;
  return {
    ifs: mapIfsPresets(mod.IFS_PRESETS || {}),
    lsystem: { ...(mod.LSYSTEM_PRESETS || {}) },
    escapeTime: mapWith(mod.ESCAPE_TIME_PRESETS || {}, mapEscapePreset),
    newton: normalizeNewtonKeys(mapWith(mod.NEWTON_PRESETS || {}, mapNewtonPreset)),
    attractor: mapWith(mod.ATTRACTOR_PRESETS || {}, mapAttractorPreset),
    inversion: normalizeInversionKeys(mapWith(mod.INVERSION_PRESETS || {}, mapInversionPreset)),
  };
}

function mapWith(input: AnyRecord, mapper: (v: any) => AnyRecord): AnyRecord {
  const out: AnyRecord = {};
  Object.entries(input).forEach(([key, value]) => {
    out[key] = mapper(value);
  });
  return out;
}

function mapIfsPresets(input: AnyRecord): AnyRecord {
  return mapWith(input, (value) => ({
    ...value,
    defaults: {
      ...value.defaults,
      colorMode: 'matrix',
    },
  }));
}

function mapEscapePreset(value: any): AnyRecord {
  return {
    label: value.label,
    type: value.type,
    viewport: value.viewport,
    defaults: {
      maxIterations: value.maxIterations,
      bailout: value.bailout ?? 4,
      power: value.power ?? 2,
      cRe: value.c?.re ?? 0,
      cIm: value.c?.im ?? 0,
    },
  };
}

function mapAttractorPreset(value: any): AnyRecord {
  const p = value.params || {};
  const mapped = {
    a: 0,
    b: 0,
    c: 0,
    d: 0,
  };
  if (typeof p.a === 'number') mapped.a = p.a;
  else if (typeof p.u === 'number') mapped.a = p.u;
  else if (typeof p.sigma === 'number') mapped.a = p.sigma;

  if (typeof p.b === 'number') mapped.b = p.b;
  else if (typeof p.rho === 'number') mapped.b = p.rho;

  if (typeof p.c === 'number') mapped.c = p.c;
  else if (typeof p.beta === 'number') mapped.c = p.beta;

  if (typeof p.d === 'number') mapped.d = p.d;
  else if (typeof p.dt === 'number') mapped.d = p.dt;

  return {
    label: value.label,
    type: value.type,
    defaults: {
      iterations: value.iterations,
      discard: value.discard,
      ...mapped,
    },
  };
}

function mapNewtonPreset(value: any): AnyRecord {
  return {
    label: value.label,
    type: value.type,
    viewport: value.viewport,
    defaults: {
      maxIterations: value.maxIterations,
      epsilon: value.epsilon,
    },
  };
}

function mapInversionPreset(value: any): AnyRecord {
  return {
    label: value.label,
    type: value.type,
    defaults: {
      depth: value.depth ?? 8,
      minRadius: value.minRadius ?? 0.003,
      iterations: value.iterations,
      discard: value.discard,
      circles: value.circles,
      seed: value.seed,
      viewport: value.viewport,
    },
  };
}

function normalizeNewtonKeys(input: AnyRecord): AnyRecord {
  const aliases: Record<string, string> = {
    newtonCubic: 'cubic',
    newtonQuartic: 'quartic',
  };
  return normalizeKeys(input, aliases);
}

function normalizeInversionKeys(input: AnyRecord): AnyRecord {
  const aliases: Record<string, string> = {
    apollonianGasket: 'apollonian',
    kleinianSchottkyClassic: 'kleinianClassic',
    kleinianSchottkyNecklace: 'kleinianNecklace',
    kleinianSchottkySymmetric: 'kleinianSymmetric',
  };
  return normalizeKeys(input, aliases);
}

function normalizeKeys(input: AnyRecord, aliases: Record<string, string>): AnyRecord {
  const out = { ...input };
  Object.entries(aliases).forEach(([sourceKey, targetKey]) => {
    if (!out[targetKey] && out[sourceKey]) {
      out[targetKey] = out[sourceKey];
      delete out[sourceKey];
    }
  });
  return out;
}
