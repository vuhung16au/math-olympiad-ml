'use client';

import { useEffect, useMemo, useRef, useState } from 'react';
import { usePathname, useRouter } from 'next/navigation';
import { IFS, radial } from '../src/ifs';
import { LSystem } from '../src/l';
import { AppHeader } from './components/AppHeader';
import { ThemeToggle } from './components/ThemeToggle';
import { FractalControls } from './components/FractalControls';
import { ViewerOverlay } from './components/ViewerOverlay';
import { PRESETS } from './presets';
import type { FormState, FractalType } from './types';

type PresetMap = Record<FractalType, Record<string, any>>;

const FRACTAL_TYPE_SLUGS: Record<FractalType, string> = {
  ifs: 'ifs',
  lsystem: 'lsystem',
  escapeTime: 'escape-time',
  newton: 'newton',
  attractor: 'strange-attractor',
  inversion: 'circle-inversion',
};

const SLUG_TO_FRACTAL_TYPE: Record<string, FractalType> = {
  ifs: 'ifs',
  lsystem: 'lsystem',
  'l-system': 'lsystem',
  escape: 'escapeTime',
  'escape-time': 'escapeTime',
  newton: 'newton',
  attractor: 'attractor',
  'strange-attractor': 'attractor',
  inversion: 'inversion',
  'circle-inversion': 'inversion',
};

const URL_PARAM_TO_FORM: Record<FractalType, Record<string, string>> = {
  ifs: { iterations: 'ifsIterations', density: 'ifsDensity', pointSize: 'ifsPointSize', color: 'ifsColor' },
  lsystem: {
    iterations: 'lsIterations',
    distance: 'lsDistance',
    angle: 'lsAngle',
    lengthScale: 'lsScale',
    lineWidth: 'lsLineWidth',
    lineColor: 'lsColor',
    axiom: 'lsAxiom',
    rules: 'lsRules',
  },
  escapeTime: {
    maxIterations: 'etMaxIterations',
    bailout: 'etBailout',
    power: 'etPower',
    juliaRe: 'etJuliaRe',
    juliaIm: 'etJuliaIm',
  },
  newton: { maxIterations: 'ntMaxIterations', epsilon: 'ntEpsilon' },
  attractor: {
    iterations: 'atIterations',
    discard: 'atDiscard',
    a: 'atA',
    b: 'atB',
    c: 'atC',
    d: 'atD',
  },
  inversion: { depth: 'ivDepth', minRadius: 'ivMinRadius' },
};

const FRACTAL_TYPE_LABELS: Record<FractalType, string> = {
  ifs: 'IFS',
  lsystem: 'L-system',
  escapeTime: 'Escape-time',
  newton: 'Newton',
  attractor: 'Strange Attractor',
  inversion: 'Circle Inversion',
};

function fractalTypeToSlug(fractalType: FractalType): string {
  return FRACTAL_TYPE_SLUGS[fractalType];
}

function parsePathSelection(pathname: string): {
  type?: FractalType;
  preset?: string;
  paramEntries: Array<[string, string]>;
} {
  const segments = pathname
    .split('/')
    .map((segment) => segment.trim())
    .filter(Boolean)
    .map((segment) => decodeURIComponent(segment));
  if (segments.length < 2) {
    return { paramEntries: [] };
  }
  const type = SLUG_TO_FRACTAL_TYPE[segments[0].toLowerCase()];
  if (!type) {
    return { paramEntries: [] };
  }
  const preset = segments[1].replace(/:+$/, '');
  const rawPairs = segments
    .slice(2)
    .flatMap((part) => part.split(','))
    .map((part) => part.trim())
    .filter(Boolean);
  const paramEntries = rawPairs.flatMap((pair) => {
    const idx = pair.indexOf('=');
    if (idx <= 0) return [];
    return [[decodeURIComponent(pair.slice(0, idx)), decodeURIComponent(pair.slice(idx + 1))] as [string, string]];
  });
  return { type, preset, paramEntries };
}

function parseRules(text: string): Record<string, string> {
  return Object.fromEntries(
    text
      .split('\n')
      .map((line) => line.trim())
      .filter(Boolean)
      .map((line) => {
        const idx = line.indexOf('=');
        return [line.slice(0, idx).trim(), line.slice(idx + 1).trim()];
      }),
  );
}

function getTransform(bounds: [number, number, number, number], width: number, height: number, padding = 24) {
  const [maxX, maxY, minX, minY] = bounds;
  const bW = Math.max(1, maxX - minX);
  const bH = Math.max(1, maxY - minY);
  const scale = Math.min((width - 2 * padding) / bW, (height - 2 * padding) / bH);
  const offX = (width - bW * scale) / 2;
  const offY = (height - bH * scale) / 2;
  return (x: number, y: number): [number, number] => [
    (x - minX) * scale + offX,
    height - ((y - minY) * scale + offY),
  ];
}

function defaultForm(): FormState {
  return {
    ifsIterations: '120000',
    ifsDensity: '65',
    ifsPointSize: '1.2',
    ifsColor: 'matrix',
    lsIterations: '6',
    lsDistance: '4',
    lsAngle: '45',
    lsScale: '1',
    lsLineWidth: '1',
    lsColor: '#14532d',
    lsAxiom: 'F',
    lsRules: 'F=F[+F][-F]F',
    etMaxIterations: '300',
    etBailout: '4',
    etPower: '2',
    etJuliaRe: '-0.8',
    etJuliaIm: '0.156',
    ntMaxIterations: '40',
    ntEpsilon: '0.000001',
    atIterations: '500000',
    atDiscard: '1000',
    atA: '-1.7',
    atB: '1.8',
    atC: '-1.9',
    atD: '-0.4',
    ivDepth: '8',
    ivMinRadius: '0.003',
  };
}

function seededRandom(seed: number): () => number {
  let state = seed >>> 0;
  return () => {
    state = (1664525 * state + 1013904223) >>> 0;
    return state / 0x100000000;
  };
}

function buildRandomIfsMatrices(config: { seed?: number; count?: number } = {}): Array<Record<string, number>> {
  const count = Math.max(3, Math.min(6, Math.round(config.count ?? 4)));
  const random = seededRandom(config.seed ?? 1337);
  const p = 1 / count;
  const matrices = [];
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

export default function HomePage() {
  const router = useRouter();
  const pathname = usePathname();
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [presets, setPresets] = useState<PresetMap>(PRESETS as PresetMap);
  const [fractalType, setFractalType] = useState<FractalType>('ifs');
  const [preset, setPreset] = useState('fern');
  const [meta, setMeta] = useState('Ready');
  const [form, setForm] = useState<FormState>(defaultForm());
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false);
  const [isDrawerOpen, setIsDrawerOpen] = useState(false);
  const [isMobile, setIsMobile] = useState(false);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [toast, setToast] = useState<string | null>(null);
  const [isRendering, setIsRendering] = useState(false);
  const CANONICAL_BASE = 'https://fractals-generator-beta.vercel.app';

  const formatTimestamp = (): string => {
    const d = new Date();
    const pad2 = (n: number) => String(n).padStart(2, '0');
    return `${d.getFullYear()}${pad2(d.getMonth() + 1)}${pad2(d.getDate())}-${pad2(d.getHours())}${pad2(d.getMinutes())}${pad2(d.getSeconds())}`;
  };

  const downloadPng = async (): Promise<void> => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const blob: Blob | null = await new Promise((resolve) => canvas.toBlob(resolve, 'image/png'));
    if (!blob) return;
    const filename = `fractals-${fractalTypeToSlug(fractalType)}-${preset}-${formatTimestamp()}.png`;
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
  };

  const copyLink = async (): Promise<void> => {
    const link = `${CANONICAL_BASE}${pathname}`;
    try {
      await navigator.clipboard.writeText(link);
      setToast('Link copied');
    } catch {
      setToast('Copy failed');
    }
  };

  useEffect(() => {
    if (!toast) return;
    const t = window.setTimeout(() => setToast(null), 1600);
    return () => window.clearTimeout(t);
  }, [toast]);

  useEffect(() => {
    document.body.dataset.fullscreen = isFullscreen ? 'true' : 'false';
    return () => {
      document.body.dataset.fullscreen = 'false';
    };
  }, [isFullscreen]);


  useEffect(() => {
    const mq = window.matchMedia('(max-width: 980px)');
    const onChange = () => setIsMobile(mq.matches);
    onChange();
    mq.addEventListener('change', onChange);
    return () => mq.removeEventListener('change', onChange);
  }, []);

  useEffect(() => {
    let cancelled = false;
    fetch('/api/presets')
      .then(async (response) => {
        if (!response.ok) {
          throw new Error(await response.text());
        }
        return response.json();
      })
      .then((data) => {
        if (cancelled || !data?.presets) return;
        const nextPresets = data.presets as PresetMap;
        setPresets(nextPresets);
        const selection = parsePathSelection(pathname);
        const initialType = selection.type && nextPresets[selection.type] ? selection.type : 'ifs';
        const initialPreset = selection.preset && nextPresets[initialType]?.[selection.preset]
          ? selection.preset
          : Object.keys(nextPresets[initialType] ?? {})[0];
        if (initialPreset) {
          setFractalType(initialType);
          setPreset(initialPreset);
          const nextForm = loadPresetWith(nextPresets, initialType, initialPreset);
          if (nextForm && selection.paramEntries.length) {
            const mapping = URL_PARAM_TO_FORM[initialType];
            const merged = { ...nextForm };
            selection.paramEntries.forEach(([urlKey, urlValue]) => {
              const formKey = mapping[urlKey];
              if (formKey) merged[formKey] = urlValue;
            });
            setForm(merged);
          }
        }
      })
      .catch(() => {
        setMeta('Using bundled preset set');
      });
    return () => {
      cancelled = true;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    const selection = parsePathSelection(pathname);
    if (!selection.type || !selection.preset || !presets[selection.type]?.[selection.preset]) {
      return;
    }
    if (selection.type === fractalType && selection.preset === preset) {
      return;
    }
    setFractalType(selection.type);
    setPreset(selection.preset);
    const nextForm = buildFormFromPreset(presets, selection.type, selection.preset, form);
    if (!nextForm) return;
    const mapping = URL_PARAM_TO_FORM[selection.type];
    selection.paramEntries.forEach(([urlKey, urlValue]) => {
      const formKey = mapping[urlKey];
      if (formKey) nextForm[formKey] = urlValue;
    });
    setForm(nextForm);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [pathname, presets, fractalType, preset]);

  const presetOptions = useMemo(
    () => Object.entries(presets[fractalType] ?? {}).map(([key, value]) => ({ key, label: value.label })),
    [fractalType, presets],
  );
  const currentPreset = (presets[fractalType]?.[preset] ?? {
    label: 'Unknown',
    defaults: {},
  }) as {
    label: string;
    defaults: Record<string, string | number>;
    matrices?: unknown;
    randomGenerator?: { seed?: number; count?: number };
    equation?: string;
    rules?: Record<string, string>;
    axiom?: string;
  };

  const buildFormFromPreset = (data: PresetMap, type: FractalType, key: string, base: FormState): FormState | null => {
    const selected = data[type]?.[key] as typeof currentPreset;
    if (!selected) return null;
    const next = { ...base };
    if (type === 'ifs') {
      next.ifsIterations = String(selected.defaults.iterations);
      next.ifsDensity = String(selected.defaults.density);
      next.ifsPointSize = String(selected.defaults.pointSize);
      next.ifsColor = String(selected.defaults.colorMode);
    } else if (type === 'lsystem') {
      next.lsIterations = String(selected.defaults.iterations);
      next.lsDistance = String(selected.defaults.distance);
      next.lsAngle = String(selected.defaults.angle);
      next.lsScale = String(selected.defaults.lengthScale);
      next.lsLineWidth = String(selected.defaults.lineWidth);
      next.lsColor = String(selected.defaults.lineColor);
      next.lsAxiom = String(selected.axiom || 'F');
      const rules = selected.rules || { F: 'F' };
      next.lsRules = Object.entries(rules)
        .map(([k, v]) => `${k}=${v}`)
        .join('\n');
    } else if (type === 'escapeTime') {
      next.etMaxIterations = String(selected.defaults.maxIterations);
      next.etBailout = String(selected.defaults.bailout);
      next.etPower = String(selected.defaults.power);
      next.etJuliaRe = String(selected.defaults.cRe);
      next.etJuliaIm = String(selected.defaults.cIm);
    } else if (type === 'newton') {
      next.ntMaxIterations = String(selected.defaults.maxIterations);
      next.ntEpsilon = String(selected.defaults.epsilon);
    } else if (type === 'attractor') {
      next.atIterations = String(selected.defaults.iterations);
      next.atDiscard = String(selected.defaults.discard);
      next.atA = String(selected.defaults.a);
      next.atB = String(selected.defaults.b);
      next.atC = String(selected.defaults.c);
      next.atD = String(selected.defaults.d);
    } else {
      next.ivDepth = String(selected.defaults.depth);
      next.ivMinRadius = String(selected.defaults.minRadius);
    }
    return next;
  };

  const loadPresetWith = (data: PresetMap, type: FractalType, key: string): FormState | null => {
    const next = buildFormFromPreset(data, type, key, form);
    if (!next) return null;
    setForm(next);
    return next;
  };
  const loadPreset = (type: FractalType, key: string) => loadPresetWith(presets, type, key);

  const buildPathForState = (
    type: FractalType,
    presetKey: string,
    nextForm?: FormState,
    includeParams = false,
  ): string => {
    const basePath = `/${fractalTypeToSlug(type)}/${encodeURIComponent(presetKey)}`;
    if (!includeParams || !nextForm) return basePath;
    const defaultForPreset = buildFormFromPreset(presets, type, presetKey, defaultForm());
    if (!defaultForPreset) return basePath;
    const mapping = URL_PARAM_TO_FORM[type];
    const encodedParams = Object.entries(mapping).flatMap(([urlKey, formKey]) => {
      const current = String(nextForm[formKey] ?? '');
      const initial = String(defaultForPreset[formKey] ?? '');
      if (current === initial) return [];
      return [`${encodeURIComponent(urlKey)}=${encodeURIComponent(current)}`];
    });
    if (!encodedParams.length) return basePath;
    return `${basePath}/${encodedParams.join('/')}`;
  };

  const replacePathIfNeeded = (nextPath: string): void => {
    if (pathname !== nextPath) {
      router.replace(nextPath, { scroll: false });
    }
  };

  const draw = async (override?: { type: FractalType; preset: string; nextForm: FormState }) => {
    const activeType = override?.type ?? fractalType;
    const activePresetKey = override?.preset ?? preset;
    const activeForm = override?.nextForm ?? form;
    const activePreset = (presets[activeType]?.[activePresetKey] ?? currentPreset) as typeof currentPreset;
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    const width = canvas.width;
    const height = canvas.height;
    ctx.fillStyle = '#fff';
    ctx.fillRect(0, 0, width, height);
    setIsRendering(true);
    setMeta('Rendering...');
    // Let the browser paint the loading overlay before heavy work begins.
    await new Promise<void>((resolve) => requestAnimationFrame(() => resolve()));
    try {
      if (activeType === 'ifs') {
        const matrices = activePreset.randomGenerator
          ? buildRandomIfsMatrices(activePreset.randomGenerator)
          : (activePreset.matrices as never[]);
        const f = new IFS({
          matrices: matrices as never[],
          iterations: Number(activeForm.ifsIterations),
          density: Number(activeForm.ifsDensity),
          equation: activePreset.equation === 'radial' ? radial : undefined,
        });
        f.run();
        const map = getTransform(f.bounds, width, height);
        for (const [x, y, m] of f.points) {
          const [px, py] = map(x, y);
          if (activeForm.ifsColor === 'emerald') ctx.fillStyle = '#059669';
          else if (activeForm.ifsColor === 'ink') ctx.fillStyle = '#111827';
          else ctx.fillStyle = `hsl(${120 + m.matrixNum * 20},76%,42%)`;
          ctx.fillRect(px, py, Number(activeForm.ifsPointSize), Number(activeForm.ifsPointSize));
        }
        setMeta(`Rendered ${f.points.length.toLocaleString()} points`);
        return;
      }
      if (activeType === 'lsystem') {
        const f = new LSystem({
          axiom: activeForm.lsAxiom,
          rules: parseRules(activeForm.lsRules),
          iterations: Number(activeForm.lsIterations),
          distance: Number(activeForm.lsDistance),
          angle: Number(activeForm.lsAngle),
          lengthScale: Number(activeForm.lsScale),
        });
        f.run();
        const map = getTransform(f.bounds, width, height, 36);
        ctx.strokeStyle = activeForm.lsColor;
        ctx.lineWidth = Number(activeForm.lsLineWidth);
        ctx.beginPath();
        for (const [x, y, metaData] of f.points) {
          const [px, py] = map(x, y);
          if (metaData.paintable) ctx.lineTo(px, py);
          else ctx.moveTo(px, py);
        }
        ctx.stroke();
        setMeta(`Rendered ${f.points.length.toLocaleString()} points`);
        return;
      }
      const response = await fetch('/api/render', {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ family: activeType, preset: activePresetKey, params: activeForm, width, height }),
      });
      if (!response.ok) throw new Error(await response.text());
      const data = await response.json();
      const image = new ImageData(new Uint8ClampedArray(data.image), width, height);
      ctx.putImageData(image, 0, 0);
      setMeta(data.meta ?? 'Rendered');
    } catch (error) {
      setMeta(`Render failed: ${error instanceof Error ? error.message : String(error)}`);
    } finally {
      setIsRendering(false);
    }
  };

  return (
    <>
      {!isFullscreen ? (
        <AppHeader
          title="Fractals Generator"
          breadcrumbs={`${FRACTAL_TYPE_LABELS[fractalType]} > ${currentPreset.label}`}
          rightSlot={
            <>
              <button
                type="button"
                className="icon-button"
                onClick={() => setIsDrawerOpen(true)}
                aria-label="Open controls"
                title="Controls"
                data-show-on-mobile
              >
                <svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true">
                  <path
                    fill="currentColor"
                    d="M4 7a1 1 0 0 1 1-1h6a1 1 0 0 1 0 2H5a1 1 0 0 1-1-1zm0 10a1 1 0 0 1 1-1h10a1 1 0 1 1 0 2H5a1 1 0 0 1-1-1zm12-6a1 1 0 0 1 1-1h2a1 1 0 1 1 0 2h-2a1 1 0 0 1-1-1z"
                  />
                  <path
                    fill="currentColor"
                    d="M13 12a1 1 0 0 1 1-1h1V9a2 2 0 1 0-4 0v2H8a2 2 0 1 0 0 4h3v2a2 2 0 1 0 4 0v-2h-1a1 1 0 0 1-1-1z"
                    opacity=".15"
                  />
                </svg>
              </button>
              <button
                type="button"
                className="icon-button"
                onClick={() => void copyLink()}
                aria-label="Copy link"
                title="Copy link"
              >
                <svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true">
                  <path
                    fill="currentColor"
                    d="M10.6 13.4a1 1 0 0 1 0-1.4l2.8-2.8a3 3 0 0 1 4.2 4.2l-1.6 1.6a1 1 0 1 1-1.4-1.4l1.6-1.6a1 1 0 1 0-1.4-1.4l-2.8 2.8a1 1 0 0 1-1.4 0z"
                  />
                  <path
                    fill="currentColor"
                    d="M13.4 10.6a1 1 0 0 1 0 1.4l-2.8 2.8a3 3 0 0 1-4.2-4.2l1.6-1.6A1 1 0 0 1 9.4 10L7.8 11.6a1 1 0 1 0 1.4 1.4l2.8-2.8a1 1 0 0 1 1.4 0z"
                  />
                </svg>
              </button>
              <ThemeToggle />
            </>
          }
        />
      ) : null}
      <main className={`layout ${isSidebarCollapsed ? 'layout--collapsed' : ''} ${isFullscreen ? 'layout--fullscreen' : ''}`}>
        {!isMobile ? (
          <FractalControls
            fractalType={fractalType}
            preset={preset}
            presetOptions={presetOptions}
            form={form}
            isRendering={isRendering}
            isCollapsed={isSidebarCollapsed}
            onToggleCollapsed={() => setIsSidebarCollapsed((v) => !v)}
            handlers={{
              onTypeChange: (nextType) => {
                setFractalType(nextType);
                const first = Object.keys(presets[nextType] ?? {})[0];
                setPreset(first);
                const nextForm = loadPreset(nextType, first);
                if (nextForm) {
                  replacePathIfNeeded(buildPathForState(nextType, first));
                  void draw({ type: nextType, preset: first, nextForm });
                }
              },
              onPresetChange: (nextPreset) => {
                setPreset(nextPreset);
                const nextForm = loadPreset(fractalType, nextPreset);
                if (nextForm) {
                  replacePathIfNeeded(buildPathForState(fractalType, nextPreset));
                  void draw({ type: fractalType, preset: nextPreset, nextForm });
                }
              },
              onFormChange: (key, value) => setForm((prev) => ({ ...prev, [key]: value })),
              onGenerate: () => {
                replacePathIfNeeded(buildPathForState(fractalType, preset, form, true));
                void draw();
              },
              onReset: () => {
                const nextForm = loadPreset(fractalType, preset);
                replacePathIfNeeded(buildPathForState(fractalType, preset));
                return nextForm;
              },
            }}
          />
        ) : null}

        {isMobile && isDrawerOpen ? (
          <div className="drawer-backdrop" role="presentation" onClick={() => setIsDrawerOpen(false)}>
            <div className="drawer" role="dialog" aria-label="Fractal controls" onClick={(e) => e.stopPropagation()}>
              <FractalControls
                fractalType={fractalType}
                preset={preset}
                presetOptions={presetOptions}
                form={form}
                isRendering={isRendering}
                isDrawer
                onCloseDrawer={() => setIsDrawerOpen(false)}
                handlers={{
                  onTypeChange: (nextType) => {
                    setFractalType(nextType);
                    const first = Object.keys(presets[nextType] ?? {})[0];
                    setPreset(first);
                    const nextForm = loadPreset(nextType, first);
                    if (nextForm) {
                      replacePathIfNeeded(buildPathForState(nextType, first));
                      void draw({ type: nextType, preset: first, nextForm });
                    }
                  },
                  onPresetChange: (nextPreset) => {
                    setPreset(nextPreset);
                    const nextForm = loadPreset(fractalType, nextPreset);
                    if (nextForm) {
                      replacePathIfNeeded(buildPathForState(fractalType, nextPreset));
                      void draw({ type: fractalType, preset: nextPreset, nextForm });
                    }
                  },
                  onFormChange: (key, value) => setForm((prev) => ({ ...prev, [key]: value })),
                  onGenerate: () => {
                    replacePathIfNeeded(buildPathForState(fractalType, preset, form, true));
                    void draw();
                    setIsDrawerOpen(false);
                  },
                  onReset: () => {
                    const nextForm = loadPreset(fractalType, preset);
                    replacePathIfNeeded(buildPathForState(fractalType, preset));
                    return nextForm;
                  },
                }}
              />
            </div>
          </div>
        ) : null}

        <section className="viewer">
          <div className="viewer-head">
            <h2 id="viewerTitle">Fractal Render - {currentPreset.label}</h2>
            <p id="meta">{meta}</p>
          </div>
          <div className="canvas-wrap">
            <canvas id="canvas" ref={canvasRef} width={980} height={760} />
            <ViewerOverlay
              isRendering={isRendering}
              onDownloadPng={() => void downloadPng()}
              onFullscreenToggle={() => setIsFullscreen((v) => !v)}
              isFullscreen={isFullscreen}
            />
          </div>
        </section>
      </main>
      {!isFullscreen && toast ? (
        <div className="toast" role="status" aria-live="polite">
          {toast}
        </div>
      ) : null}
    </>
  );
}
