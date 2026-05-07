export function logStep(message: string) {
  process.stdout.write(`${message}\n`);
}

export function logWarn(message: string) {
  process.stderr.write(`Warning: ${message}\n`);
}
