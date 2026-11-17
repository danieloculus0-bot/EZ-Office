// Regression for CSV formula injection in the actual EZ Sheets serializer.
// Run: node --test tests/csv_formula_guard.test.cjs
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');

const source = fs.readFileSync(path.join(__dirname, '../apps/sheets.js'), 'utf8');
const begin = source.indexOf('function csvText(rows)');
const end = source.indexOf('function colLabel(i)', begin);
assert.ok(begin >= 0 && end > begin, 'actual CSV serializer must be present');
const csvText = vm.runInNewContext(source.slice(begin, end) + '\ncsvText;');

test('neutralizes formulas without mutating source cells', () => {
  const input = [['=1+1', '+SUM(A1:A2)', '-cmd', '@SUM(1,2)', ' \t=HYPERLINK("x")']];
  const snapshot = JSON.stringify(input);
  const result = csvText(input);
  assert.ok(result.includes("'=1+1"));
  assert.ok(result.includes("'+SUM(A1:A2)"));
  assert.ok(result.includes("'-cmd"));
  assert.ok(result.includes("'@SUM(1,2)"));
  assert.ok(result.includes("' \t=HYPERLINK"));
  assert.equal(JSON.stringify(input), snapshot);
});

test('preserves signed numeric values and ordinary text', () => {
  assert.equal(csvText([['-12.5', '+4', '-1e3', 'plain']]), '-12.5,+4,-1e3,plain\r\n');
});

test('retains correct RFC-style CSV quoting for commas and double quotes', () => {
  assert.equal(csvText([['a,b', 'say "hi"', '=HYPERLINK("x","y")']]),
    '"a,b","say ""hi""","\'=HYPERLINK(""x"",""y"")"\r\n');
});
