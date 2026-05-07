declare global {
  interface Window {
    MathJax?: {
      startup?: { promise?: Promise<void> };
      typesetPromise?: (elements?: HTMLElement[]) => Promise<void>;
    };
  }
}

export async function typesetMath(container: HTMLElement) {
  if (!window.MathJax?.typesetPromise) {
    return;
  }

  if (window.MathJax.startup?.promise) {
    await window.MathJax.startup.promise;
  }

  await window.MathJax.typesetPromise([container]);
}
