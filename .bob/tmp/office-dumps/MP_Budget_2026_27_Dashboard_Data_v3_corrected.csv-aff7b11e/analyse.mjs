import { readFileSync } from "fs";

const lines = readFileSync(".bob/tmp/office-dumps/MP_Budget_2026_27_Dashboard_Data_v3_corrected.csv-aff7b11e/data.txt", "utf8").trim().split("\n");

const colMap = {};
const rows = [];

for (const line of lines) {
  if (!line.trim()) continue;
  const tabIdx = line.indexOf("\t");
  if (tabIdx === -1) continue;
  const header = line.slice(0, tabIdx);
  const cellPart = line.slice(tabIdx + 1);
  const rowMatch = header.match(/row\[(\d+)\]/);
  if (!rowMatch) continue;
  const rowNum = parseInt(rowMatch[1]);

  const record = {};
  for (const cell of cellPart.split("\t")) {
    const eqIdx = cell.indexOf("=");
    if (eqIdx === -1) continue;
    const key = cell.slice(0, eqIdx);
    const val = cell.slice(eqIdx + 1);
    const col = key.replace(/\d+$/, "");
    record[col] = val;
  }

  if (rowNum === 1) {
    for (const [col, name] of Object.entries(record)) colMap[col] = name;
    continue;
  }

  rows.push(record);
}

console.log("=== COLUMN MAP ===");
console.log(colMap);
console.log("\n=== TOTAL ROWS (excl header) ===", rows.length);

// Unique values
const indicators = [...new Set(rows.map(r => r["A"]))];
const categories = [...new Set(rows.map(r => r["B"]))];
const subcategories = [...new Set(rows.map(r => r["C"]))];
const years = [...new Set(rows.map(r => r["D"]))];
const estimateTypes = [...new Set(rows.map(r => r["E"]))];
const units = [...new Set(rows.map(r => r["G"]))];
const sectors = [...new Set(rows.map(r => r["H"] || "(blank)"))];

console.log("\n=== UNIQUE INDICATORS ===", indicators.length);
indicators.forEach(i => console.log(" -", i));

console.log("\n=== UNIQUE CATEGORIES ===", categories.length);
categories.forEach(c => console.log(" -", c));

console.log("\n=== UNIQUE SUBCATEGORIES ===", subcategories.length);
subcategories.forEach(s => console.log(" -", s));

console.log("\n=== UNIQUE YEARS ===", years.length);
years.forEach(y => console.log(" -", y));

console.log("\n=== UNIQUE ESTIMATE TYPES ===", estimateTypes.length);
estimateTypes.forEach(e => console.log(" -", e));

console.log("\n=== UNIQUE UNITS ===", units.length);
units.forEach(u => console.log(" -", u));

console.log("\n=== UNIQUE SECTORS ===", sectors.length);
sectors.forEach(s => console.log(" -", s));

// Missing values
let missingValue = 0, missingUnit = 0, missingEstimate = 0, missingYear = 0;
rows.forEach(r => {
  if (!r["F"] || r["F"].trim() === "") missingValue++;
  if (!r["G"] || r["G"].trim() === "") missingUnit++;
  if (!r["E"] || r["E"].trim() === "") missingEstimate++;
  if (!r["D"] || r["D"].trim() === "") missingYear++;
});
console.log("\n=== MISSING VALUES ===");
console.log("Missing Value (F):", missingValue);
console.log("Missing Unit (G):", missingUnit);
console.log("Missing Estimate_Type (E):", missingEstimate);
console.log("Missing Financial_Year (D):", missingYear);

// Check Notes
const notesPatterns = [...new Set(rows.map(r => r["I"] || "(blank)").slice(0, 50))];
console.log("\n=== SAMPLE NOTES (first 10) ===");
notesPatterns.slice(0, 10).forEach(n => console.log(" -", n));

// Check for rows with numeric issues
let nonNumericValues = 0;
rows.forEach(r => {
  const val = parseFloat(r["F"]);
  if (isNaN(val)) nonNumericValues++;
});
console.log("\n=== NON-NUMERIC VALUE ROWS ===", nonNumericValues);

// Show all rows
console.log("\n=== ALL DATA ROWS ===");
rows.forEach((r, i) => {
  console.log(`Row ${i+2}: Indicator="${r["A"]}" | Cat="${r["B"]}" | Sub="${r["C"]}" | Year="${r["D"]}" | Type="${r["E"]}" | Value="${r["F"]}" | Unit="${r["G"]}" | Sector="${r["H"]||""}" | Notes="${r["I"]||""}"`);
});
