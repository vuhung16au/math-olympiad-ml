import type { FormState, FractalType } from '../types';

type PresetOption = { key: string; label: string };

const TYPE_OPTIONS: Array<{ key: FractalType; label: string }> = [
  { key: 'ifs', label: 'IFS' },
  { key: 'lsystem', label: 'L-system' },
  { key: 'escapeTime', label: 'Escape-time' },
  { key: 'newton', label: 'Newton' },
  { key: 'attractor', label: 'Attractor' },
  { key: 'inversion', label: 'Inversion' },
];

type Props = {
  fractalType: FractalType;
  preset: string;
  presetOptions: PresetOption[];
  form: FormState;
  isRendering?: boolean;
  isCollapsed?: boolean;
  onToggleCollapsed?: () => void;
  isDrawer?: boolean;
  onCloseDrawer?: () => void;
  handlers: {
    onTypeChange: (nextType: FractalType) => void;
    onPresetChange: (nextPreset: string) => void;
    onFormChange: (key: string, value: string) => void;
    onGenerate: () => void;
    onReset: () => void;
  };
};

export function FractalControls({
  fractalType,
  preset,
  presetOptions,
  form,
  isRendering = false,
  isCollapsed = false,
  onToggleCollapsed,
  isDrawer = false,
  onCloseDrawer,
  handlers,
}: Props) {
  const { onTypeChange, onPresetChange, onFormChange, onGenerate, onReset } = handlers;

  if (isCollapsed && !isDrawer) {
    return (
      <aside className="panel panel--collapsed" aria-label="Collapsed fractal controls">
        <button
          type="button"
          className="collapse-handle"
          onClick={onToggleCollapsed}
          aria-label="Expand controls"
          title="Expand controls"
        >
          <span aria-hidden="true">›</span>
        </button>
      </aside>
    );
  }

  const showAppearance = fractalType === 'ifs' || fractalType === 'lsystem';
  const showAdvanced = fractalType === 'escapeTime' || fractalType === 'newton' || fractalType === 'attractor' || fractalType === 'inversion';

  return (
    <aside className={`panel ${isDrawer ? 'panel--drawer' : ''}`}>
      <div className="panel-head">
        <div>
          <h1 className="panel-title">Controls</h1>
          <p className="panel-subtitle">Pick a family, tweak parameters, generate.</p>
        </div>
        {!isDrawer ? (
          <button
            type="button"
            className="collapse-handle"
            onClick={onToggleCollapsed}
            aria-label="Collapse controls"
            title="Collapse controls"
          >
            <span aria-hidden="true">‹</span>
          </button>
        ) : (
          <button type="button" className="icon-button" onClick={onCloseDrawer} aria-label="Close controls" title="Close">
            <svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true">
              <path
                fill="currentColor"
                d="M18.3 5.7a1 1 0 0 0-1.4 0L12 10.6 7.1 5.7a1 1 0 0 0-1.4 1.4l4.9 4.9-4.9 4.9a1 1 0 1 0 1.4 1.4l4.9-4.9 4.9 4.9a1 1 0 0 0 1.4-1.4l-4.9-4.9 4.9-4.9a1 1 0 0 0 0-1.4z"
              />
            </svg>
          </button>
        )}
      </div>

      <details className="accordion" open>
        <summary className="accordion__summary">Core</summary>
        <div className="accordion__body">
          <div className="pill-row" role="tablist" aria-label="Fractal family">
            {TYPE_OPTIONS.map((opt) => (
              <button
                key={opt.key}
                type="button"
                className={`pill ${opt.key === fractalType ? 'pill--active' : ''}`}
                onClick={() => onTypeChange(opt.key)}
                role="tab"
                aria-selected={opt.key === fractalType}
              >
                {opt.label}
              </button>
            ))}
          </div>

          <div className="field">
            <label htmlFor="preset">Preset</label>
            <select id="preset" value={preset} onChange={(e) => onPresetChange(e.target.value)}>
              {presetOptions.map((option) => (
                <option key={option.key} value={option.key}>
                  {option.label}
                </option>
              ))}
            </select>
          </div>

          <div className="actions">
            <button id="generateBtn" className="btn btn-primary" type="button" onClick={onGenerate} disabled={isRendering}>
              {isRendering ? 'Rendering…' : 'Generate'}
            </button>
            <button id="resetBtn" className="btn btn-secondary" type="button" onClick={onReset} disabled={isRendering}>
              Reset Preset
            </button>
          </div>
        </div>
      </details>

      <details className="accordion" open={showAppearance}>
        <summary className="accordion__summary">Appearance</summary>
        <div className="accordion__body" hidden={!showAppearance}>
          {fractalType === 'ifs' ? (
            <>
              <div className="inline">
                <div className="field">
                  <label htmlFor="ifsDensity">Density</label>
                  <input
                    id="ifsDensity"
                    type="number"
                    value={form.ifsDensity}
                    onChange={(e) => onFormChange('ifsDensity', e.target.value)}
                  />
                </div>
                <div className="field">
                  <label htmlFor="ifsPointSize">Point Size</label>
                  <input
                    id="ifsPointSize"
                    type="number"
                    value={form.ifsPointSize}
                    onChange={(e) => onFormChange('ifsPointSize', e.target.value)}
                  />
                </div>
              </div>
              <div className="field">
                <label htmlFor="ifsColor">Color Mode</label>
                <select id="ifsColor" value={form.ifsColor} onChange={(e) => onFormChange('ifsColor', e.target.value)}>
                  <option value="matrix">By Matrix</option>
                  <option value="emerald">Emerald</option>
                  <option value="ink">Black Ink</option>
                </select>
              </div>
            </>
          ) : null}

          {fractalType === 'lsystem' ? (
            <>
              <div className="inline">
                <div className="field">
                  <label htmlFor="lsLineWidth">Line Width</label>
                  <input
                    id="lsLineWidth"
                    type="number"
                    value={form.lsLineWidth}
                    onChange={(e) => onFormChange('lsLineWidth', e.target.value)}
                  />
                </div>
                <div className="field">
                  <label htmlFor="lsColor">Line Color</label>
                  <input id="lsColor" type="color" value={form.lsColor} onChange={(e) => onFormChange('lsColor', e.target.value)} />
                </div>
              </div>
            </>
          ) : null}
        </div>
      </details>

      <details className="accordion" open={showAdvanced}>
        <summary className="accordion__summary">Advanced</summary>
        <div className="accordion__body" hidden={!showAdvanced}>
          {fractalType === 'ifs' ? (
            <div className="field">
              <label htmlFor="ifsIterations">Iterations</label>
              <input
                id="ifsIterations"
                type="number"
                value={form.ifsIterations}
                onChange={(e) => onFormChange('ifsIterations', e.target.value)}
              />
            </div>
          ) : null}

          {fractalType === 'lsystem' ? (
            <>
              <div className="inline">
                <div className="field">
                  <label htmlFor="lsIterations">Iterations</label>
                  <input
                    id="lsIterations"
                    type="number"
                    value={form.lsIterations}
                    onChange={(e) => onFormChange('lsIterations', e.target.value)}
                  />
                </div>
                <div className="field">
                  <label htmlFor="lsDistance">Distance</label>
                  <input
                    id="lsDistance"
                    type="number"
                    value={form.lsDistance}
                    onChange={(e) => onFormChange('lsDistance', e.target.value)}
                  />
                </div>
              </div>
              <div className="inline">
                <div className="field">
                  <label htmlFor="lsAngle">Angle</label>
                  <input id="lsAngle" type="number" value={form.lsAngle} onChange={(e) => onFormChange('lsAngle', e.target.value)} />
                </div>
                <div className="field">
                  <label htmlFor="lsScale">Length Scale</label>
                  <input id="lsScale" type="number" value={form.lsScale} onChange={(e) => onFormChange('lsScale', e.target.value)} />
                </div>
              </div>
              <div className="field">
                <label htmlFor="lsAxiom">Axiom</label>
                <input id="lsAxiom" value={form.lsAxiom} onChange={(e) => onFormChange('lsAxiom', e.target.value)} />
              </div>
              <div className="field">
                <label htmlFor="lsRules">Rules</label>
                <textarea id="lsRules" value={form.lsRules} onChange={(e) => onFormChange('lsRules', e.target.value)} />
              </div>
            </>
          ) : null}

          {fractalType === 'escapeTime' ? (
            <>
              <div className="inline">
                <div className="field">
                  <label htmlFor="etMaxIterations">Max Iterations</label>
                  <input
                    id="etMaxIterations"
                    type="number"
                    value={form.etMaxIterations}
                    onChange={(e) => onFormChange('etMaxIterations', e.target.value)}
                  />
                </div>
                <div className="field">
                  <label htmlFor="etBailout">Bailout</label>
                  <input id="etBailout" type="number" value={form.etBailout} onChange={(e) => onFormChange('etBailout', e.target.value)} />
                </div>
              </div>
              <div className="inline">
                <div className="field">
                  <label htmlFor="etPower">Power</label>
                  <input id="etPower" type="number" value={form.etPower} onChange={(e) => onFormChange('etPower', e.target.value)} />
                </div>
                <div className="field">
                  <label htmlFor="etJuliaRe">Julia c (real)</label>
                  <input id="etJuliaRe" type="number" value={form.etJuliaRe} onChange={(e) => onFormChange('etJuliaRe', e.target.value)} />
                </div>
              </div>
              <div className="field">
                <label htmlFor="etJuliaIm">Julia c (imag)</label>
                <input id="etJuliaIm" type="number" value={form.etJuliaIm} onChange={(e) => onFormChange('etJuliaIm', e.target.value)} />
              </div>
            </>
          ) : null}

          {fractalType === 'newton' ? (
            <div className="inline">
              <div className="field">
                <label htmlFor="ntMaxIterations">Max Iterations</label>
                <input
                  id="ntMaxIterations"
                  type="number"
                  value={form.ntMaxIterations}
                  onChange={(e) => onFormChange('ntMaxIterations', e.target.value)}
                />
              </div>
              <div className="field">
                <label htmlFor="ntEpsilon">Epsilon</label>
                <input id="ntEpsilon" type="number" value={form.ntEpsilon} onChange={(e) => onFormChange('ntEpsilon', e.target.value)} />
              </div>
            </div>
          ) : null}

          {fractalType === 'attractor' ? (
            <>
              <div className="inline">
                <div className="field">
                  <label htmlFor="atIterations">Iterations</label>
                  <input
                    id="atIterations"
                    type="number"
                    value={form.atIterations}
                    onChange={(e) => onFormChange('atIterations', e.target.value)}
                  />
                </div>
                <div className="field">
                  <label htmlFor="atDiscard">Discard</label>
                  <input id="atDiscard" type="number" value={form.atDiscard} onChange={(e) => onFormChange('atDiscard', e.target.value)} />
                </div>
              </div>
              <div className="inline">
                <div className="field">
                  <label htmlFor="atA">a</label>
                  <input id="atA" type="number" value={form.atA} onChange={(e) => onFormChange('atA', e.target.value)} />
                </div>
                <div className="field">
                  <label htmlFor="atB">b</label>
                  <input id="atB" type="number" value={form.atB} onChange={(e) => onFormChange('atB', e.target.value)} />
                </div>
              </div>
              <div className="inline">
                <div className="field">
                  <label htmlFor="atC">c</label>
                  <input id="atC" type="number" value={form.atC} onChange={(e) => onFormChange('atC', e.target.value)} />
                </div>
                <div className="field">
                  <label htmlFor="atD">d</label>
                  <input id="atD" type="number" value={form.atD} onChange={(e) => onFormChange('atD', e.target.value)} />
                </div>
              </div>
            </>
          ) : null}

          {fractalType === 'inversion' ? (
            <div className="inline">
              <div className="field">
                <label htmlFor="ivDepth">Depth</label>
                <input id="ivDepth" type="number" value={form.ivDepth} onChange={(e) => onFormChange('ivDepth', e.target.value)} />
              </div>
              <div className="field">
                <label htmlFor="ivMinRadius">Min Radius</label>
                <input
                  id="ivMinRadius"
                  type="number"
                  value={form.ivMinRadius}
                  onChange={(e) => onFormChange('ivMinRadius', e.target.value)}
                />
              </div>
            </div>
          ) : null}
        </div>
      </details>
    </aside>
  );
}
