let pyodide;
try {
  const {loadPyodide} = await import('https://cdn.jsdelivr.net/pyodide/v314.0.7/full/pyodide.mjs');
  pyodide = await loadPyodide();
  postMessage({type: 'ready'});
} catch (error) {
  postMessage({type: 'init-error', message: String(error)});
}

const harness = `
import contextlib, io, json, traceback
data = json.loads(payload_json)
out = io.StringIO()
scope = {}
error = ''
results = []
def _raises_value_error(fn, *args):
    try:
        fn(*args)
    except ValueError:
        return True
    return False
def _carteiras_independentes(cls):
    first, second = cls(0), cls(0)
    first.depositar(2)
    return first.saldo == 2 and second.saldo == 0
async def _await_result(awaitable, expected):
    return await awaitable == expected
scope.update({'_raises_value_error': _raises_value_error, '_carteiras_independentes': _carteiras_independentes, '_await_result': _await_result})
try:
    with contextlib.redirect_stdout(out):
        exec(data['code'], scope)
        if data['grade']:
            for case in data['tests']:
                try:
                    check = case['check']
                    passed = bool(await eval(check[6:], scope)) if check.startswith('await ') else bool(eval(check, scope))
                    results.append({'label': case['label'], 'passed': passed, 'error': ''})
                except Exception as exc:
                    results.append({'label': case['label'], 'passed': False, 'error': f'{type(exc).__name__}: {exc}'})
except Exception:
    error = traceback.format_exc(limit=3)
json.dumps({'output': out.getvalue()[-4000:], 'error': error, 'results': results}, ensure_ascii=False)
`;

self.onmessage = async ({data}) => {
  if (!pyodide || data.type !== 'execute') return;
  try {
    pyodide.globals.set('payload_json', JSON.stringify(data.payload));
    const result = await pyodide.runPythonAsync(harness);
    postMessage({type: 'result', id: data.id, payload: JSON.parse(result)});
  } catch (error) {
    postMessage({type: 'result', id: data.id, payload: {output: '', error: String(error), results: []}});
  }
};
